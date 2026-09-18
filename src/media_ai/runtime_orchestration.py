"""Fail-closed preflight and dispatch contracts for real media runtimes."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from subprocess import CalledProcessError, TimeoutExpired, run
from typing import Callable, Iterable

from PIL import Image

from .contracts import JobState, MediaJob, MediaType
from .evidence import orchestration_evidence
from .job_pipeline import requested_operation
from .router import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS


AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}


class PreflightStatus(StrEnum):
    PREFLIGHT_READY = "PREFLIGHT_READY"
    BLOCKED_INPUT = "BLOCKED_INPUT"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"


@dataclass(frozen=True)
class AdapterSpec:
    adapter_id: str
    model_or_program_id: str
    revision: str | None
    license_source: str
    supported_media_type: MediaType
    runtime_backend: str
    device_requirement: str
    available: bool
    adapter_version: str = "builtin"
    artifact_sha256: str | None = None
    artifact_size_bytes: int | None = None


class AdapterRegistry:
    def __init__(self, adapters: dict[tuple[MediaType, str], AdapterSpec] | None = None) -> None:
        self._adapters = adapters or self._default_adapters()
        self._readiness_checks: dict[tuple[MediaType, str], Callable[[], bool]] = {}

    @staticmethod
    def _default_adapters() -> dict[tuple[MediaType, str], AdapterSpec]:
        local_photo = AdapterSpec("pillow_opencv_boundary", "Pillow OpenCV", None, "local program dependency", MediaType.PHOTO, "python", "cpu", True)
        remote_photo = AdapterSpec("photo_model_boundary", "opencv/inpainting_lama", "aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f", "pending runtime verification", MediaType.PHOTO, "onnx", "gpu_or_cpu", False)
        local_video = AdapterSpec("ffmpeg_video_boundary", "ffmpeg", None, "local program dependency", MediaType.VIDEO, "ffmpeg", "cpu", True)
        remote_video = AdapterSpec("video_model_boundary", "facebook/sam2.1-hiera-base-plus", "b7320756a13354e7530a63935656d35b2f91a290", "pending runtime verification", MediaType.VIDEO, "pytorch", "gpu", False)
        korean_audio = AdapterSpec("korean_audio_boundary", "openai/whisper-large-v3-turbo", "41f01f3fe87f28c78e2fbf8b568835947dd65ed9", "pending Korean runtime verification", MediaType.KOREAN_AUDIO, "transformers", "gpu", False)
        return {
            (MediaType.PHOTO, "photo_adjust"): local_photo,
            (MediaType.PHOTO, "object_removal"): remote_photo,
            (MediaType.PHOTO, "restore_upscale"): remote_photo,
            (MediaType.VIDEO, "video_edit"): local_video,
            (MediaType.VIDEO, "interpolation"): local_video,
            (MediaType.VIDEO, "stabilization"): local_video,
            (MediaType.VIDEO, "tracking"): remote_video,
            (MediaType.VIDEO, "mask"): remote_video,
            (MediaType.KOREAN_AUDIO, "korean_transcription"): korean_audio,
        }

    def resolve(self, media_type: MediaType, operation: str) -> AdapterSpec | None:
        return self._adapters.get((media_type, operation))

    def register(self, media_type: MediaType, operation: str, adapter: AdapterSpec, readiness_check: Callable[[], bool] | None = None) -> None:
        if adapter.supported_media_type is not media_type:
            raise ValueError("Adapter media type does not match its registration lane")
        key = (media_type, operation)
        self._adapters[key] = adapter
        if readiness_check is not None:
            self._readiness_checks[key] = readiness_check

    def is_ready(self, media_type: MediaType, operation: str) -> bool:
        check = self._readiness_checks.get((media_type, operation))
        return check() if check else True


@dataclass(frozen=True)
class PreflightReceipt:
    status: PreflightStatus
    lane: MediaType
    missing_requirements: tuple[str, ...]
    input_sha256: str | None
    adapter: AdapterSpec | None


@dataclass(frozen=True)
class ExecutionContext:
    job_id: str
    evidence_id: str
    lane: MediaType
    source_hashes: dict[str, str]
    nl_instruction: str
    reference_images: tuple[str, ...]
    retry_provenance: dict[str, int | str]
    adapter_identity: dict[str, str | None]

    def evidence_value(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class OutputReceipt:
    valid: bool
    artifact: dict
    reason: str | None = None


def artifact_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_output(path: Path, lane: MediaType) -> OutputReceipt:
    path = Path(path)
    if not path.is_file():
        return OutputReceipt(False, {"path": str(path)}, "Output artifact is unavailable")
    if path.stat().st_size == 0:
        return OutputReceipt(False, {"path": str(path)}, "Output artifact is empty")
    allowed_extensions = {
        MediaType.PHOTO: PHOTO_EXTENSIONS,
        MediaType.VIDEO: VIDEO_EXTENSIONS,
        MediaType.KOREAN_AUDIO: AUDIO_EXTENSIONS,
    }[lane]
    if path.suffix.lower() not in allowed_extensions:
        return OutputReceipt(False, {"path": str(path)}, f"Unexpected {lane.value} output type: {path.suffix}")
    try:
        if lane is MediaType.PHOTO:
            with Image.open(path) as image:
                image.verify()
        else:
            run(["ffprobe", "-v", "error", "-show_format", "-show_streams", str(path)], check=True, capture_output=True, text=True, timeout=10)
    except (CalledProcessError, FileNotFoundError, TimeoutExpired, OSError) as error:
        return OutputReceipt(False, {"path": str(path)}, f"Output artifact is not parseable: {error}")
    artifact = {
        "path": str(path),
        "type": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "sha256": artifact_sha256(path),
        "status": "validated",
    }
    return OutputReceipt(True, artifact)


class RuntimeOrchestrator:
    """Coordinates lanes without running or claiming an unverified model."""
    def __init__(self, registry: AdapterRegistry | None = None, max_retries: int = 1) -> None:
        self.registry = registry or AdapterRegistry()
        self.max_retries = max_retries
        self._receipts: dict[str, PreflightReceipt] = {}
        self._contexts: dict[str, ExecutionContext] = {}
        self._started_at: dict[str, str] = {}

    def preflight_many(self, jobs: Iterable[MediaJob]) -> list[PreflightReceipt]:
        return [self.preflight(job) for job in jobs]

    def preflight(self, job: MediaJob) -> PreflightReceipt:
        if job.state in {JobState.BLOCKED_INPUT, JobState.BLOCKED_MODEL, JobState.FAILED}:
            job.transition(JobState.VALIDATING)
        elif job.state is JobState.QUEUED:
            job.transition(JobState.VALIDATING)
        elif job.state is not JobState.VALIDATING:
            raise ValueError(f"Preflight requires a queued, blocked, or failed job: {job.state}")

        missing = self._input_requirements(job)
        if missing:
            return self._blocked_input(job, missing)

        input_sha256 = artifact_sha256(job.input_path)
        expected_sha256 = (job.source_provenance or {}).get("sha256")
        if expected_sha256 and expected_sha256 != input_sha256:
            return self._blocked_input(job, ("source provenance SHA-256 does not match the input artifact",))

        operation = self._operation(job)
        adapter = self.registry.resolve(job.media_type, operation)
        if adapter is None or not adapter.available or not self.registry.is_ready(job.media_type, operation):
            return self._model_unavailable(job, adapter, input_sha256)
        job.transition(JobState.PREFLIGHT_READY)
        receipt = PreflightReceipt(PreflightStatus.PREFLIGHT_READY, job.media_type, (), input_sha256, adapter)
        self._receipts[job.id] = receipt
        job.evidence = orchestration_evidence(job, receipt.status, adapter=adapter, input_sha256=input_sha256)
        return receipt

    def dispatch(self, job: MediaJob) -> ExecutionContext:
        receipt = self._receipts.get(job.id)
        if receipt is None or receipt.status is not PreflightStatus.PREFLIGHT_READY or job.state is not JobState.PREFLIGHT_READY:
            raise ValueError("Dispatch requires a successful preflight")
        adapter = receipt.adapter
        assert adapter is not None
        job.transition(JobState.DISPATCHED)
        context = ExecutionContext(
            job_id=job.id,
            evidence_id=job.evidence_id,
            lane=job.media_type,
            source_hashes={"source": receipt.input_sha256 or ""},
            nl_instruction=job.request,
            reference_images=tuple(job.reference_files),
            retry_provenance={"job_id": job.id, "evidence_id": job.evidence_id, "attempt": job.attempts},
            adapter_identity={
                "adapter_id": adapter.adapter_id,
                "model_or_program_id": adapter.model_or_program_id,
                "revision": adapter.revision,
            },
        )
        self._contexts[job.id] = context
        job.evidence = orchestration_evidence(job, "DISPATCHED", adapter=adapter, input_sha256=receipt.input_sha256, execution_context=context.evidence_value())
        return context

    def start(self, job: MediaJob) -> None:
        if job.state is not JobState.DISPATCHED:
            raise ValueError("Runtime start requires a dispatched job")
        job.transition(JobState.RUNNING)
        job.attempts += 1
        self._started_at[job.id] = datetime.now(timezone.utc).isoformat()

    def cancel(self, job: MediaJob, reason: str = "Cancelled by user") -> None:
        if job.state not in {JobState.QUEUED, JobState.VALIDATING, JobState.PREFLIGHT_READY, JobState.DISPATCHED, JobState.RUNNING, JobState.OUTPUT_VALIDATING}:
            raise ValueError(f"Job cannot be cancelled from {job.state}")
        job.transition(JobState.CANCELLED)
        receipt = self._receipts.get(job.id)
        job.error = reason
        job.evidence = orchestration_evidence(job, "CANCELLED", adapter=receipt.adapter if receipt else None, input_sha256=receipt.input_sha256 if receipt else None, execution_context=self._context_value(job), started_at=self._started_at.get(job.id), reason=reason)

    def timeout(self, job: MediaJob, timeout_seconds: int) -> None:
        if job.state is not JobState.RUNNING:
            raise ValueError("Timeout requires a running job")
        job.error = f"Runtime timed out after {timeout_seconds} seconds"
        job.transition(JobState.FAILED)
        receipt = self._receipts.get(job.id)
        job.evidence = orchestration_evidence(job, "TIMEOUT", adapter=receipt.adapter if receipt else None, input_sha256=receipt.input_sha256 if receipt else None, execution_context=self._context_value(job), started_at=self._started_at.get(job.id), reason=job.error)

    def retry(self, job: MediaJob) -> PreflightReceipt:
        if job.state is not JobState.FAILED:
            raise ValueError("Only failed jobs are retry eligible")
        if job.attempts >= self.max_retries:
            raise ValueError("Retry limit reached")
        return self.preflight(job)

    def complete(self, job: MediaJob, output_path: Path) -> OutputReceipt:
        if job.state is not JobState.RUNNING:
            raise ValueError("Output completion requires a running job")
        receipt = self._receipts[job.id]
        job.transition(JobState.OUTPUT_VALIDATING)
        output = validate_output(Path(output_path), job.media_type)
        if not output.valid:
            job.error = output.reason
            job.transition(JobState.FAILED)
            job.evidence = orchestration_evidence(job, "OUTPUT_INVALID", adapter=receipt.adapter, input_sha256=receipt.input_sha256, execution_context=self._context_value(job), started_at=self._started_at.get(job.id), output_artifact=output.artifact, reason=output.reason)
            return output
        job.output_path = Path(output_path)
        job.transition(JobState.SUCCEEDED)
        job.evidence = orchestration_evidence(job, "OUTPUT_VALIDATED", adapter=receipt.adapter, input_sha256=receipt.input_sha256, execution_context=self._context_value(job), started_at=self._started_at.get(job.id), output_artifact=output.artifact)
        return output

    def accept_model_scout_callback(self, job: MediaJob, callback: dict) -> dict:
        required = {"job_id", "evidence_id", "status"}
        missing = required - callback.keys()
        if missing:
            raise ValueError(f"Model Scout callback is missing: {', '.join(sorted(missing))}")
        if callback["job_id"] != job.id or callback["evidence_id"] != job.evidence_id:
            raise ValueError("Model Scout callback does not correlate to this job evidence")
        if callback["status"] not in {"TESTED_PASS", "TESTED_FAIL"}:
            raise ValueError("Model Scout callback status is invalid")
        accepted = {"status": callback["status"], "received_at": datetime.now(timezone.utc).isoformat()}
        if callback.get("adapter_id"):
            accepted["adapter_id"] = callback["adapter_id"]
        job.evidence = {**job.evidence, "model_scout_callback": accepted}
        return accepted

    def _input_requirements(self, job: MediaJob) -> tuple[str, ...]:
        requirements: list[str] = []
        if not job.request.strip():
            requirements.append("natural-language instruction")
        if not job.input_path.is_file():
            requirements.append("source artifact")
        elif job.input_path.stat().st_size == 0:
            requirements.append("non-empty source artifact")
        if not job.source_provenance or job.source_provenance.get("source_path") != str(job.input_path):
            requirements.append("matching source provenance")
        extensions = {
            MediaType.PHOTO: PHOTO_EXTENSIONS,
            MediaType.VIDEO: VIDEO_EXTENSIONS,
            MediaType.KOREAN_AUDIO: AUDIO_EXTENSIONS,
        }[job.media_type]
        if job.input_path.suffix.lower() not in extensions:
            requirements.append(f"supported {job.media_type.value} input format")
        return tuple(requirements)

    def _operation(self, job: MediaJob) -> str:
        if job.requested_operation:
            return job.requested_operation
        if job.media_type is MediaType.KOREAN_AUDIO:
            job.requested_operation = "korean_transcription"
        else:
            job.requested_operation = requested_operation(job)
        return job.requested_operation

    def _blocked_input(self, job: MediaJob, missing: tuple[str, ...]) -> PreflightReceipt:
        job.error = f"Missing runtime requirements: {', '.join(missing)}"
        job.transition(JobState.BLOCKED_INPUT)
        receipt = PreflightReceipt(PreflightStatus.BLOCKED_INPUT, job.media_type, missing, None, None)
        self._receipts[job.id] = receipt
        job.evidence = orchestration_evidence(job, receipt.status, reason=job.error)
        job.evidence["missing_requirements"] = list(missing)
        return receipt

    def _model_unavailable(self, job: MediaJob, adapter: AdapterSpec | None, input_sha256: str) -> PreflightReceipt:
        job.error = f"Model or program adapter is unavailable for {job.requested_operation}"
        job.transition(JobState.BLOCKED_MODEL)
        receipt = PreflightReceipt(PreflightStatus.MODEL_UNAVAILABLE, job.media_type, ("verified adapter availability",), input_sha256, adapter)
        self._receipts[job.id] = receipt
        job.evidence = orchestration_evidence(job, receipt.status, adapter=adapter, input_sha256=input_sha256, reason=job.error)
        job.evidence["missing_requirements"] = list(receipt.missing_requirements)
        return receipt

    def _context_value(self, job: MediaJob) -> dict | None:
        context = self._contexts.get(job.id)
        return context.evidence_value() if context else None
