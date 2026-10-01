"""Fail-closed Model Scout supply contracts; no model is loaded here."""
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from .contracts import MediaJob, MediaType
from .runtime_orchestration import AUDIO_EXTENSIONS, AdapterRegistry, AdapterSpec, artifact_sha256
from .router import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS


class IntegrationStatus(StrEnum):
    VERIFIED = "VERIFIED"
    BLOCKED_INPUT = "BLOCKED_INPUT"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    PREFLIGHT_FAILED = "PREFLIGHT_FAILED"
    RUNTIME_READY = "RUNTIME_READY"
    TESTED_PASS = "TESTED_PASS"
    DELIVERED = "DELIVERED"


class HandoffValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ModelScoutHandoff:
    request_id: str
    issue_id: str
    lane: MediaType
    operation: str
    model_or_program_id: str
    source: str
    revision: str
    license_evidence: str
    artifact_path: Path
    artifact_filename: str
    artifact_size_bytes: int
    artifact_sha256: str
    runtime_backend: str
    device_requirement: str
    adapter_id: str
    adapter_version: str
    verification_status: str
    issued_at: str


@dataclass(frozen=True)
class InputArtifactManifest:
    lane: MediaType
    path: Path
    provenance: dict
    sha256: str
    size_bytes: int
    status: str = "PARTIAL_INPUT_READY"


@dataclass(frozen=True)
class AdapterRegistration:
    handoff: ModelScoutHandoff
    adapter: AdapterSpec


def validate_handoff(handoff: ModelScoutHandoff) -> None:
    required = {
        "request_id": handoff.request_id, "issue_id": handoff.issue_id,
        "operation": handoff.operation, "model_or_program_id": handoff.model_or_program_id,
        "source": handoff.source, "revision": handoff.revision,
        "license_evidence": handoff.license_evidence, "artifact_filename": handoff.artifact_filename,
        "runtime_backend": handoff.runtime_backend, "device_requirement": handoff.device_requirement,
        "adapter_id": handoff.adapter_id, "adapter_version": handoff.adapter_version,
        "issued_at": handoff.issued_at,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise HandoffValidationError(f"Missing Model Scout handoff fields: {', '.join(missing)}")
    if handoff.verification_status != IntegrationStatus.VERIFIED:
        raise HandoffValidationError("Only VERIFIED handoffs may enter the adapter cache")
    if not handoff.artifact_path.is_file() or handoff.artifact_path.name != handoff.artifact_filename:
        raise HandoffValidationError("Handoff artifact is unavailable or filename does not match")
    if handoff.artifact_path.stat().st_size != handoff.artifact_size_bytes:
        raise HandoffValidationError("Handoff artifact size does not match")
    if artifact_sha256(handoff.artifact_path) != handoff.artifact_sha256:
        raise HandoffValidationError("Handoff artifact SHA-256 does not match")


class ModelScoutAdapterRegistry:
    """Promotes only verified, locally materialized handoffs into the runtime registry."""
    def __init__(self, runtime_registry: AdapterRegistry | None = None) -> None:
        self.runtime_registry = runtime_registry or AdapterRegistry()
        self._registrations: dict[tuple[MediaType, str], AdapterRegistration] = {}

    def ingest(self, handoff: ModelScoutHandoff) -> AdapterRegistration:
        validate_handoff(handoff)
        adapter = AdapterSpec(
            handoff.adapter_id, handoff.model_or_program_id, handoff.revision,
            handoff.license_evidence, handoff.lane, handoff.runtime_backend,
            handoff.device_requirement, True, handoff.adapter_version,
            handoff.artifact_sha256, handoff.artifact_size_bytes,
        )
        registration = AdapterRegistration(handoff, adapter)
        key = (handoff.lane, handoff.operation)
        self._registrations[key] = registration
        self.runtime_registry.register(handoff.lane, handoff.operation, adapter, lambda: self.readiness(handoff.lane, handoff.operation) is IntegrationStatus.RUNTIME_READY)
        return registration

    def get(self, lane: MediaType, operation: str) -> AdapterRegistration | None:
        return self._registrations.get((lane, operation))

    def readiness(self, lane: MediaType, operation: str, backends: set[str] | None = None, devices: set[str] | None = None) -> IntegrationStatus:
        registration = self.get(lane, operation)
        if registration is None:
            return IntegrationStatus.MODEL_UNAVAILABLE
        handoff = registration.handoff
        try:
            validate_handoff(handoff)
        except HandoffValidationError:
            return IntegrationStatus.PREFLIGHT_FAILED
        available_backends = backends or {handoff.runtime_backend}
        available_devices = devices or {handoff.device_requirement}
        if handoff.runtime_backend not in available_backends or handoff.device_requirement not in available_devices:
            return IntegrationStatus.MODEL_UNAVAILABLE
        return IntegrationStatus.RUNTIME_READY


class InputArtifactIntake:
    def __init__(self) -> None:
        self._manifests: dict[MediaType, InputArtifactManifest] = {}

    def ingest(self, lane: MediaType, path: Path, provenance: dict | None = None) -> InputArtifactManifest:
        path = Path(path)
        extensions = {MediaType.PHOTO: PHOTO_EXTENSIONS, MediaType.VIDEO: VIDEO_EXTENSIONS, MediaType.KOREAN_AUDIO: AUDIO_EXTENSIONS}[lane]
        if not path.is_file() or path.stat().st_size == 0:
            raise HandoffValidationError(f"{lane.value} input artifact is unavailable")
        if path.suffix.lower() not in extensions:
            raise HandoffValidationError(f"Unsupported {lane.value} input format")
        provenance = dict(provenance or {"source_path": str(path)})
        if provenance.get("source_path") != str(path):
            raise HandoffValidationError("Input provenance does not match the artifact")
        manifest = InputArtifactManifest(lane, path, provenance, artifact_sha256(path), path.stat().st_size)
        self._manifests[lane] = manifest
        return manifest

    def get(self, lane: MediaType) -> InputArtifactManifest | None:
        return self._manifests.get(lane)


class RuntimeIntegrationGate:
    def __init__(self, registry: ModelScoutAdapterRegistry, intake: InputArtifactIntake) -> None:
        self.registry = registry
        self.intake = intake

    def readiness(self, job: MediaJob) -> IntegrationStatus:
        manifest = self.intake.get(job.media_type)
        if manifest is None:
            return IntegrationStatus.BLOCKED_INPUT
        if manifest.path != job.input_path or manifest.sha256 != artifact_sha256(job.input_path):
            return IntegrationStatus.PREFLIGHT_FAILED
        registration = self.registry.get(job.media_type, job.requested_operation or "")
        if registration is None:
            return IntegrationStatus.MODEL_UNAVAILABLE
        return self.registry.readiness(job.media_type, job.requested_operation or "")

    def accept_callback(self, job: MediaJob, callback: dict) -> IntegrationStatus:
        registration = self.registry.get(job.media_type, job.requested_operation or "")
        manifest = self.intake.get(job.media_type)
        if registration is None:
            raise HandoffValidationError("Callback adapter has not been registered")
        required = {"request_id", "issue_id", "callback_id", "job_id", "evidence_id", "lane", "revision", "artifact_sha256", "adapter_id", "adapter_version", "status", "input_sha256", "output_sha256", "output_path", "elapsed_ms", "runtime_backend", "device_requirement", "sent_at"}
        missing = required - callback.keys()
        if missing:
            raise HandoffValidationError(f"Callback fields missing: {', '.join(sorted(missing))}")
        handoff = registration.handoff
        expected = {
            "request_id": handoff.request_id, "issue_id": handoff.issue_id, "job_id": job.id,
            "evidence_id": job.evidence_id, "lane": job.media_type, "revision": handoff.revision,
            "artifact_sha256": handoff.artifact_sha256, "adapter_id": handoff.adapter_id,
            "adapter_version": handoff.adapter_version, "runtime_backend": handoff.runtime_backend,
            "device_requirement": handoff.device_requirement,
        }
        if any(callback[key] != value for key, value in expected.items()):
            raise HandoffValidationError("Callback identity, lane, revision, hash, or adapter does not correlate")
        if datetime.fromisoformat(callback["sent_at"]) < datetime.fromisoformat(handoff.issued_at):
            raise HandoffValidationError("Stale Model Scout callback")
        if callback["status"] != IntegrationStatus.TESTED_PASS:
            raise HandoffValidationError("Only a complete TESTED_PASS receipt may pass the delivery gate")
        if not manifest or callback["input_sha256"] != manifest.sha256 or not callback["output_sha256"] or not callback["output_path"] or callback["elapsed_ms"] < 0:
            raise HandoffValidationError("TESTED_PASS evidence is incomplete or does not match the input")
        job.evidence = {**job.evidence, "model_scout_delivery": {"status": IntegrationStatus.DELIVERED, "callback_id": callback["callback_id"], "input_sha256": callback["input_sha256"], "output_sha256": callback["output_sha256"], "output_path": callback["output_path"], "elapsed_ms": callback["elapsed_ms"]}}
        return IntegrationStatus.DELIVERED
