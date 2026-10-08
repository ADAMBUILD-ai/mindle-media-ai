"""Fail-closed product job execution from the immutable MINDLE model vault.

This module is deliberately separate from the model-acquisition scripts.  It
only reads the three pinned cache revisions and refuses to execute when a
byte-level identity differs from the TESTED_PASS baseline.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import platform
import shutil
import sys
import zipfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from huggingface_hub import HfApi, hf_hub_download

from .contracts import MediaJob, MediaType
from .model_scout_integration import (
    InputArtifactIntake,
    IntegrationStatus,
    ModelScoutAdapterRegistry,
    ModelScoutHandoff,
    RuntimeIntegrationGate,
)
from .intel_sisr_verified_adapter import IntelSISR1032VerifiedAdapter
from .realesrgan_verified_adapter import (
    RealESRGANIdentity,
    RealESRGANX4PlusVerifiedAdapter,
    sha256_file as realesrgan_sha256,
)
from .runtime_orchestration import RuntimeOrchestrator
from .verified_model_adapters import (
    Sam21VerifiedAdapter,
    VerifiedModelIdentity,
    WhisperKoreanVerifiedAdapter,
    sha256_file,
)


PRIVATE_REPO = "MINDLE1846/MINDLE-MEDIA-AI-MODELS"
BASELINE_REVISION = "ad63c52a4b9a3db7eaec9c5058c94ee1422757dd"
REALESRGAN_CACHE_REVISION = "e6f4ad5194673f27f64b1dc9626f1b616fb05792"
SAM = VerifiedModelIdentity("facebook/sam2.1-hiera-base-plus", "b7320756a13354e7530a63935656d35b2f91a290", "apache-2.0", "model.safetensors", 323_476_296, "2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780")
WHISPER = VerifiedModelIdentity("openai/whisper-small", "973afd24965f72e36ca33b3055d56a652f456b4d", "mit", "model.safetensors", 966_995_080, "1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b")
SAM_FILES = {
    "config.json": (5705, "8e24a93b6a40d4dad86eaec383ce7b4044f37ec6360136460f5ff2ce55f87390"),
    "model.safetensors": (323_476_296, SAM.weight_sha256),
    "preprocessor_config.json": (683, "6ebf229ee259368ce4a8d4f2fe893a72b053023710853e257253939e601f583d"),
    "processor_config.json": (95, "f8a68e865cfad115c1c2763f3d93eca7b1c622da06da2a9273eb437fb2389b6d"),
}
WHISPER_FILES = {
    "config.json": (1967, "e6a2b489da1b5aed65a8eb8d1e7466fa867ad5643a8bc138ba708bd56b2875c4"),
    "generation_config.json": (3868, "71565b8ef50d0bf7a1193ed4bbed195b94e70c18894d81bba2f1233dcec3ab53"),
    "model.safetensors": (966_995_080, WHISPER.weight_sha256),
    "preprocessor_config.json": (184990, "9b5cd03a36fbb8a627c64d98a5b5b126ead95a77720723944487311f0110b666"),
    "tokenizer.json": (2_480_466, "27fc476bfe7f17299480be2273fc0608e4d5a99aba2ab5dec5374b4482d1a566"),
    "tokenizer_config.json": (282_683, "2a4c4281cf9f51ac6ccc406fdc711a087afe6530f671fa7b80953edc498275ce"),
}
REALESRGAN = RealESRGANIdentity(
    "qualcomm/Real-ESRGAN-x4plus", "4022efb8b74eb88900724d9e05a468ac3673df4a", "bsd-3-clause",
    "real_esrgan_x4plus-onnx-float.zip", 62_174_026, "e6cb215390f3800b56baa0e9140907d81f5143a4b96c184a635c79dfee2e28df",
    "real_esrgan_x4plus.onnx", 3_158_313, "29ffd5bc0277b19536cd39b737627fb2d79df9999b8329741b558498dd5e31f7",
    "real_esrgan_x4plus.data", 66_737_664, "28fada125730d3c87d504d48dd8332837f65811ec431a570ea4919ba3eee3287",
)
REALESRGAN_CACHE_PATH = "VERIFIED_MODEL_CACHE/realesrgan-x4plus-onnx/real_esrgan_x4plus-onnx-float.zip"
ALT_CACHE_PREFIX = "VERIFIED_MODEL_CACHE/perpetual-use-alternatives"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_record(path: Path) -> dict:
    return {"file_name": path.name, "path": str(path), "bytes": path.stat().st_size, "sha256": sha256_file(path)}


class ProductModelVault:
    """Read-only, one-process cache materializer for the three immutable models."""

    def __init__(self, root: Path, token: str) -> None:
        self.root, self.token = Path(root), token
        self.downloads = self.root / "verified_model_cache"
        self.downloads.mkdir(parents=True, exist_ok=True)
        configured = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip()
        self.local_root = Path(configured) if configured else None
        self.api = None if self.local_root else HfApi(token=token)

    def verify_local_models(self) -> None:
        """Verify every adopted model before accepting any employee request."""
        if self.local_root is None:
            raise RuntimeError("local package root is required")
        self._local_snapshot("sam21", SAM_FILES)
        self._local_snapshot("whisper-small", WHISPER_FILES)
        directory = self.local_root / "omz/intel/single-image-super-resolution-1032/FP32"
        for name, digest in {
            "single-image-super-resolution-1032.xml": "4f355965e070341e1f1df5b954213e0ecca5d43faf8a0c9770efdf04c7442c88fb0aaeb825fc8091b30f0a674c808446",
            "single-image-super-resolution-1032.bin": "ec5a759c2d43eebf679040638ad765bc6ce5c16253421ddeb8acafd1ab6c8cb406f9f85b274771d9f670efc3d824e926",
        }.items():
            path = directory / name
            if not path.is_file() or hashlib.sha384(path.read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"local Intel SISR SHA-384 mismatch: {name}")

    def _local_snapshot(self, cache_name: str, expected: dict[str, tuple[int, str]]) -> Path | None:
        """Use only an explicitly supplied, byte-pinned recovered package."""
        if self.local_root is None:
            return None
        snapshot = self.local_root / "models" / ("whisper-small" if cache_name == "whisper-small" else cache_name)
        if not snapshot.is_dir():
            raise RuntimeError(f"configured recovered model snapshot is unavailable: {snapshot}")
        for name, (size, digest) in expected.items():
            path = snapshot / name
            if not path.is_file() or path.stat().st_size != size or sha256_file(path) != digest:
                raise RuntimeError(f"recovered local cache mismatch: {cache_name}/{name}")
        return snapshot

    def _download_files(self, cache_name: str, expected: dict[str, tuple[int, str]]) -> Path:
        if self.local_root is not None:
            raise RuntimeError("network acquisition is disabled in local package mode")
        info = self.api.model_info(PRIVATE_REPO, revision=BASELINE_REVISION, token=self.token, files_metadata=True)
        if info.sha != BASELINE_REVISION or not bool(getattr(info, "private", False)):
            raise RuntimeError("immutable private SAM/Whisper cache revision or visibility mismatch")
        destination = self.downloads / "VERIFIED_MODEL_CACHE" / cache_name
        for name, (size, digest) in expected.items():
            path = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=f"VERIFIED_MODEL_CACHE/{cache_name}/{name}", revision=BASELINE_REVISION, token=self.token, local_dir=str(self.downloads)))
            if path.stat().st_size != size or sha256_file(path) != digest:
                raise RuntimeError(f"immutable cache mismatch: {cache_name}/{name}")
        return destination

    def sam(self) -> tuple[Sam21VerifiedAdapter, dict]:
        local = self._local_snapshot("sam21", SAM_FILES)
        if local is not None:
            return Sam21VerifiedAdapter(local, SAM), {"identity": asdict(SAM), "local_recovered_package": {"root": str(self.local_root), "path": str(local), "read_only": True}}
        snapshot = self._download_files("sam21", SAM_FILES)
        adapter = Sam21VerifiedAdapter(snapshot, SAM)
        return adapter, {"identity": asdict(SAM), "private_cache": {"repo_id": PRIVATE_REPO, "revision": BASELINE_REVISION, "path": "VERIFIED_MODEL_CACHE/sam21", "read_only": True}}

    def _alternatives(self) -> tuple[str, dict]:
        if self.local_root is not None:
            raise RuntimeError("network acquisition is disabled in local package mode")
        revision = os.environ.get("MINDLE_ALTERNATIVE_CACHE_REVISION", "").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", revision): raise RuntimeError("perpetual-use alternative cache revision is required")
        info = self.api.model_info(PRIVATE_REPO, revision=revision, token=self.token, files_metadata=True)
        if info.sha != revision or not bool(getattr(info, "private", False)): raise RuntimeError("alternative private cache revision or visibility mismatch")
        filename = f"ALTERNATIVE_MODEL_EVIDENCE/{os.environ.get('GITHUB_RUN_ID','local')}/ALTERNATIVE_MODEL_MANIFEST.json"
        path = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=filename, revision=revision, token=self.token, local_dir=str(self.downloads)))
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("gate_result") != "PERPETUAL_USE_EVIDENCE_READY": raise RuntimeError("alternative perpetual-use gate is not closed")
        return revision, manifest

    def _alternative_files(self, revision: str, folder: str, artifacts: list[dict]) -> Path:
        if self.local_root is not None:
            raise RuntimeError("network acquisition is disabled in local package mode")
        destination = self.downloads / ALT_CACHE_PREFIX / folder
        for item in artifacts:
            name = Path(item["file"]).name
            path = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=f"{ALT_CACHE_PREFIX}/{folder}/{name}", revision=revision, token=self.token, local_dir=str(self.downloads)))
            if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]: raise RuntimeError(f"alternative immutable cache mismatch: {folder}/{name}")
        return destination

    def whisper(self) -> tuple[WhisperKoreanVerifiedAdapter, dict]:
        local = self._local_snapshot("whisper-small", WHISPER_FILES)
        if local is not None:
            adapter = WhisperKoreanVerifiedAdapter(local, WHISPER)
            return adapter, {"identity": asdict(WHISPER), "local_recovered_package": {"root": str(self.local_root), "path": str(local), "read_only": True}}
        revision, manifest = self._alternatives(); item = manifest["alternatives"]["korean_stt"]
        snapshot = self._alternative_files(revision, "whisper-small", item["artifacts"])
        weight = next(x for x in item["artifacts"] if x["file"].endswith("model.safetensors"))
        identity = VerifiedModelIdentity(item["source"]["repo_id"], item["source"]["revision"], item["source"]["license"].lower(), "model.safetensors", weight["bytes"], weight["sha256"])
        adapter = WhisperKoreanVerifiedAdapter(snapshot, identity)
        return adapter, {"identity": asdict(identity), "private_cache": {"repo_id": PRIVATE_REPO, "revision": revision, "path": f"{ALT_CACHE_PREFIX}/whisper-small", "read_only": True}, "perpetual_use_gate": item["perpetual_use_gate"]}

    def realesrgan(self) -> tuple[IntelSISR1032VerifiedAdapter, dict]:
        if self.local_root is not None:
            snapshot = self.local_root / "omz" / "intel" / "single-image-super-resolution-1032" / "FP32"
            xml, weights = snapshot / "single-image-super-resolution-1032.xml", snapshot / "single-image-super-resolution-1032.bin"
            expected = {
                xml: "4f355965e070341e1f1df5b954213e0ecca5d43faf8a0c9770efdf04c7442c88fb0aaeb825fc8091b30f0a674c808446",
                weights: "ec5a759c2d43eebf679040638ad765bc6ce5c16253421ddeb8acafd1ab6c8cb406f9f85b274771d9f670efc3d824e926",
            }
            for path, digest in expected.items():
                if not path.is_file():
                    raise RuntimeError(f"recovered Intel SISR artifact is unavailable: {path}")
                hasher = hashlib.sha384(); hasher.update(path.read_bytes())
                if hasher.hexdigest() != digest:
                    raise RuntimeError(f"recovered Intel SISR SHA-384 mismatch: {path.name}")
            identity = VerifiedModelIdentity("openvinotoolkit/open_model_zoo", "a6946b6d6ce42cbf4278df20275fab199655fc7d", "apache-2.0", weights.name, weights.stat().st_size, hashlib.sha256(weights.read_bytes()).hexdigest())
            return IntelSISR1032VerifiedAdapter(xml, weights, identity), {"identity": asdict(identity), "local_recovered_package": {"root": str(self.local_root), "path": str(snapshot), "read_only": True, "sha384_verified": True}}
        revision, manifest = self._alternatives(); item = manifest["alternatives"]["photo_upscale_4x"]
        snapshot = self._alternative_files(revision, "intel-sisr-1032", item["artifacts"])
        weight = next(x for x in item["artifacts"] if x["file"].endswith(".bin"))
        identity = VerifiedModelIdentity(item["source"]["repo_id"], item["source"]["revision"], item["source"]["license"].lower(), Path(weight["file"]).name, weight["bytes"], weight["sha256"])
        adapter = IntelSISR1032VerifiedAdapter(snapshot / "single-image-super-resolution-1032.xml", snapshot / "single-image-super-resolution-1032.bin", identity)
        return adapter, {"identity": asdict(identity), "private_cache": {"repo_id": PRIVATE_REPO, "revision": revision, "path": f"{ALT_CACHE_PREFIX}/intel-sisr-1032", "read_only": True}, "perpetual_use_gate": item["perpetual_use_gate"]}


class ProductJobService:
    def __init__(self, root: Path, token: str) -> None:
        self.root = Path(root)
        self.inputs, self.jobs, self.projects = self.root / "inputs", self.root / "jobs", self.root / "projects"
        for path in (self.inputs, self.jobs, self.projects): path.mkdir(parents=True, exist_ok=True)
        self.vault = ProductModelVault(self.root, token)
        if self.vault.local_root is not None:
            self.vault.verify_local_models()
        self.records: dict[str, dict] = {}
        for saved in self.projects.glob('*.json'):
            try:
                record = json.loads(saved.read_text(encoding='utf-8'))
                for job in record.get('jobs', []):
                    if job.get('status') == 'TESTED_PASS':
                        self.records[job['job_id']] = job
            except (OSError, ValueError, KeyError, TypeError):
                continue

    def prepare_browser_preview(self, job_id: str) -> dict:
        from .browser_preview import create_preview
        record = self.records[job_id]
        if record.get('lane') != 'video' or record.get('operation') != 'tracking':
            raise ValueError('tracking video required')
        original = record['primary_output']
        source = Path(original['path'])
        result = create_preview(source, original['sha256'], source.with_name(source.stem+'_browser_h264.mp4'))
        derivative = result['output']
        updated = {**record, 'preview_output':derivative, 'preview_derivative':result,
                   'outputs':[item for item in record['outputs'] if item['path'] != derivative['path']] + [derivative]}
        evidence = source.parent / 'PREVIEW_DERIVATIVE_EVIDENCE.json'
        evidence.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        self.records[job_id] = updated
        return updated

    def latest_project(self) -> dict | None:
        saved = sorted(self.projects.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not saved:
            return None
        return json.loads(saved[0].read_text(encoding='utf-8'))

    def _store_input(self, filename: str, content_b64: str) -> Path:
        safe = Path(filename).name
        if not safe or safe in {".", ".."}: raise ValueError("invalid input filename")
        payload = base64.b64decode(content_b64, validate=True)
        if not payload: raise ValueError("input payload is empty")
        path = self.inputs / f"{uuid4()}_{safe}"
        path.write_bytes(payload)
        return path

    def _handoff(self, lane: MediaType, operation: str, model: dict, artifact: Path, adapter) -> ModelScoutHandoff:
        identity = model["identity"]
        return ModelScoutHandoff(
            request_id=f"product-{uuid4()}", issue_id="PR-10", lane=lane, operation=operation,
            model_or_program_id=identity["repo_id"], source="MINDLE private VERIFIED_MODEL_CACHE",
            revision=identity["revision"], license_evidence=identity["license"], artifact_path=artifact,
            artifact_filename=artifact.name, artifact_size_bytes=artifact.stat().st_size, artifact_sha256=sha256_file(artifact),
            runtime_backend=adapter.runtime_backend, device_requirement=adapter.device_requirement,
            adapter_id=adapter.adapter_id, adapter_version=adapter.adapter_version,
            verification_status=IntegrationStatus.VERIFIED, issued_at=now(),
        )

    @staticmethod
    def _photo_target_point(command: str, source: Path) -> tuple[int, int]:
        """Resolve the approved command's intended subject without changing UI SSOT."""
        from PIL import Image

        with Image.open(source) as image:
            width, height = image.size
        normalized = command.replace(" ", "")
        if "왼쪽" in normalized or "인물" in normalized:
            return (round(width * 0.26), round(height * 0.54))
        if "오른쪽" in normalized:
            return (round(width * 0.74), round(height * 0.54))
        return (width // 2, height // 2)

    def execute_isolated(self, request: dict) -> dict:
        """Release native model runtimes between jobs and isolate OpenMP libraries."""
        import subprocess
        report = self.jobs / f'worker-result-{uuid4()}.json'
        source_root = str(Path(__file__).resolve().parents[1])
        worker = (
            'import sys,json,os;from pathlib import Path\n'
            'def deny_network(event,args):\n'
            ' if event == "socket.connect": raise PermissionError("Offline model worker forbids network connections")\n'
            'if os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip(): sys.addaudithook(deny_network)\n'
            'try:\n'
            ' from openvino_telemetry.main import Telemetry\n'
            ' Telemetry.opt_out(tid=None)\n'
            'except ImportError: pass\n'
            f'sys.path.insert(0,{source_root!r})\n'
            'from media_ai.product_runtime import ProductJobService;'
            'service=ProductJobService(Path(sys.argv[1]),os.environ.get("HF_TOKEN",""));'
            'result=service.execute(json.load(sys.stdin));'
            'Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False),encoding="utf-8")'
        )
        environment = dict(os.environ)
        (self.root / 'runtime-profile/appdata').mkdir(parents=True, exist_ok=True)
        environment.update(OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
                           HF_HUB_DISABLE_TELEMETRY='1', LOCALAPPDATA=str(self.root / 'runtime-profile'),
                           APPDATA=str(self.root / 'runtime-profile/appdata'))
        if self.vault.local_root is not None:
            environment.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                               HF_HOME=str(self.root / 'offline-worker-cache'))
            for key in ('HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN'):
                environment.pop(key, None)
        else:
            # The CI vault reads immutable private revisions; it is not an offline package.
            environment.pop('HF_HUB_OFFLINE', None)
            environment.pop('TRANSFORMERS_OFFLINE', None)
            environment['HF_TOKEN'] = self.vault.token
        try:
            result = subprocess.run([sys.executable, '-X', 'utf8', '-c', worker, str(self.root), str(report)],
                                    input=json.dumps(request, ensure_ascii=False), encoding='utf-8',
                                    capture_output=True, errors='replace', timeout=900, env=environment)
            if result.returncode or not report.is_file():
                raise RuntimeError('AI 작업을 완료하지 못했습니다. ' + result.stderr[-1200:])
            record = json.loads(report.read_text(encoding='utf-8'))
            self.records[record['job_id']] = record
            return record
        except subprocess.TimeoutExpired as error:
            raise RuntimeError('AI 작업 시간이 초과되었습니다. 작업을 다시 실행하세요.') from error
        finally:
            report.unlink(missing_ok=True)

    def execute(self, request: dict) -> dict:
        lane = MediaType(request["lane"])
        operation, command = str(request["operation"]), str(request["command"]).strip()
        if not command: raise ValueError("natural-language command is required")
        source = self._store_input(str(request["filename"]), str(request["content_base64"]))
        job_dir = self.jobs / str(uuid4()); job_dir.mkdir()
        job = MediaJob(request=command, input_path=source, media_type=lane, requested_operation=operation, project_id=request.get("project_id"), source_provenance={"source_path": str(source), "sha256": sha256_file(source), "ingress": "approved-ui"})
        adapter = None
        try:
            if operation in {"segment", "tracking"}:
                adapter, model = self.vault.sam()
                result = (adapter.segment_photo(source, job_dir / "sam_photo", self._photo_target_point(command, source)) if operation == "segment" else adapter.track_video(source, job_dir / "sam_video"))
                primary = Path(result["outputs"][-1 if operation == "segment" else 0]["path"])
                artifact = adapter.weight
            elif operation == "upscale":
                adapter, model = self.vault.realesrgan()
                output = job_dir / "intel_sisr_1032" / "upscaled_4x.png"
                result = adapter.upscale(source, output)
                primary = output; artifact = adapter.weight
            elif operation == "transcribe":
                if source.suffix.lower() != '.wav':
                    import subprocess
                    package = os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT')
                    ffmpeg = str(Path(package) / 'tools/ffmpeg/ffmpeg.exe') if package else 'ffmpeg'
                    audio = job_dir / 'subtitle_audio.wav'
                    subprocess.run([ffmpeg, '-y', '-i', str(source), '-vn', '-ac', '1', '-ar', '16000', str(audio)],
                                   check=True, capture_output=True, timeout=600)
                    original = file_record(source)
                    source = audio
                    job.input_path = source
                    job.source_provenance = {"source_path": str(source), "sha256": sha256_file(source),
                                             "ingress": "approved-ui-extracted-audio", "derived_from": original}
                adapter, model = self.vault.whisper()
                result = adapter.transcribe(source, job_dir / "whisper", request.get("reference"))
                primary = Path(result["outputs"][0]["path"]); artifact = adapter.weight
            else:
                raise ValueError(f"unsupported verified product operation: {operation}")

            registry, intake = ModelScoutAdapterRegistry(), InputArtifactIntake()
            handoff = self._handoff(lane, operation, model, artifact, adapter)
            registry.ingest(handoff); intake.ingest(lane, source, job.source_provenance)
            gate = RuntimeIntegrationGate(registry, intake)
            if gate.readiness(job) is not IntegrationStatus.RUNTIME_READY: raise RuntimeError("verified adapter did not reach RUNTIME_READY")
            orchestrator = RuntimeOrchestrator(registry.runtime_registry)
            if orchestrator.preflight(job).status.value != "PREFLIGHT_READY": raise RuntimeError(job.error or "product preflight failed")
            orchestrator.dispatch(job); orchestrator.start(job)
            receipt = orchestrator.complete(job, primary)
            if not receipt.valid: raise RuntimeError(receipt.reason or "output validation failed")
            input_sha = sha256_file(source)
            output_sha = sha256_file(primary)
            callback = {"request_id": handoff.request_id, "issue_id": handoff.issue_id, "callback_id": f"callback-{uuid4()}", "job_id": job.id, "evidence_id": job.evidence_id, "lane": lane, "revision": handoff.revision, "artifact_sha256": handoff.artifact_sha256, "adapter_id": handoff.adapter_id, "adapter_version": handoff.adapter_version, "status": IntegrationStatus.TESTED_PASS, "input_sha256": input_sha, "output_sha256": output_sha, "output_path": str(primary), "elapsed_ms": float(result.get("elapsed_ms", 0.0)), "runtime_backend": handoff.runtime_backend, "device_requirement": handoff.device_requirement, "sent_at": now()}
            delivery = gate.accept_callback(job, callback)
            outputs = [file_record(path) for path in sorted(job_dir.rglob("*")) if path.is_file()]
            record = {"status": "TESTED_PASS", "job_id": job.id, "evidence_id": job.evidence_id, "lane": lane.value, "operation": operation, "command": command, "state_history": [state.value for state in job.state_history], "model": model, "adapter": {"id": adapter.adapter_id, "version": adapter.adapter_version, "runtime_backend": adapter.runtime_backend, "device_requirement": adapter.device_requirement}, "input": file_record(source), "runtime_result": result, "primary_output": file_record(primary), "outputs": outputs, "backend": {"api_status": 201, "delivery_gate": delivery, "job_evidence": job.evidence}, "execution_environment": {"hardware": "CPU", "gpu_used": False, "paid_compute": False, "platform": platform.platform(), "python": platform.python_version(), "process": sys.version.split()[0]}}
            (job_dir / "JOB_EVIDENCE.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.records[job.id] = record
            return record
        except Exception as error:
            record = {"status": "FAILED", "job_id": job.id, "lane": lane.value, "operation": operation, "error": str(error), "input": file_record(source), "state": job.state.value}
            (job_dir / "JOB_EVIDENCE.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.records[job.id] = record
            raise
        finally:
            if adapter is not None and hasattr(adapter, "close"):
                adapter.close()

    def edit_video(self, payload: dict) -> dict:
        """Run explicit local FFmpeg edits; never interpret them as model inference."""
        import subprocess
        source = self._store_input(str(payload['filename']), str(payload['content_base64']))
        job_id = str(uuid4()); job_dir = self.jobs / job_id; job_dir.mkdir()
        options = payload.get('options', {})
        package = os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT')
        ffmpeg = str(Path(package) / 'tools/ffmpeg/ffmpeg.exe') if package else 'ffmpeg'
        output = job_dir / 'edited_video.mp4'
        if options.get('highlight'):
            import cv2
            capture = cv2.VideoCapture(str(source))
            fps = capture.get(cv2.CAP_PROP_FPS) or 1
            duration = capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps
            scores = []
            previous = None
            for second in range(0, int(duration), max(1, int(duration / 300))):
                capture.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
                ok, frame = capture.read()
                if not ok: continue
                gray = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY)
                if previous is not None:
                    scores.append((float(cv2.absdiff(gray, previous).mean()), second))
                previous = gray
            capture.release()
            peak = max(scores)[1] if scores else 0
            length = min(30, duration)
            options = {**options, 'start': max(0, min(duration-length, peak-length/2)),
                       'duration': length, 'highlight_method': 'frame_difference'}
        speed = float(options.get('speed', 1))
        if not .5 <= speed <= 2: raise ValueError('속도는 0.5~2배 범위입니다.')
        vf = ['scale=trunc(iw/2)*2:trunc(ih/2)*2']
        if options.get('rotate'): vf.append('transpose=1')
        if speed != 1: vf.append(f'setpts=PTS/{speed}')
        if options.get('aspect') == '9:16':
            vf.append('scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2,setsar=1')
        vf.append(f"eq=brightness={float(options.get('brightness',0))/100}:contrast={1+float(options.get('contrast',0))/100}:saturation={1+float(options.get('saturation',0))/100}")
        if options.get('fade'): vf.append('fade=t=in:st=0:d=0.4')
        if options.get('effect'): vf.append('vignette=PI/6')
        if options.get('denoise'): vf.append('hqdn3d')
        if options.get('stabilize'): vf.append('deshake')
        subtitle = str(options.get('subtitle', '')).strip()
        if subtitle:
            text_path = job_dir / 'subtitle.txt'; text_path.write_text(subtitle, encoding='utf-8')
            escape = lambda path: str(path).replace('\\','/').replace(':','\\:').replace("'", "\\'")
            font = Path(os.environ.get('SystemRoot', 'C:/Windows')) / 'Fonts/malgun.ttf'
            vf.append(f"drawtext=fontfile='{escape(font)}':textfile='{escape(text_path)}':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-text_h-20")
        command = [ffmpeg, '-y', '-i', str(source)]
        background = payload.get('background')
        background_source = None
        if background:
            background_source = self._store_input(str(background['filename']), str(background['content_base64']))
            command.extend(['-stream_loop', '-1', '-i', str(background_source)])
        if options.get('start'): command.extend(['-ss', str(max(0,float(options['start'])))])
        if options.get('duration'): command.extend(['-t', str(max(.1,float(options['duration'])))])
        command.extend(['-vf', ','.join(vf), '-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p'])
        if options.get('mute'): command.append('-an')
        elif background_source:
            ffprobe = str(Path(package) / 'tools/ffmpeg/ffprobe.exe') if package else 'ffprobe'
            probe = subprocess.run([ffprobe,'-v','error','-select_streams','a','-show_entries','stream=index','-of','json',str(source)],check=True,capture_output=True,text=True)
            background_volume = max(0, min(1, float(options.get('backgroundVolume', .35))))
            if json.loads(probe.stdout)['streams']:
                mix = f"[0:a]volume={max(0,float(options.get('volume',1)))},atempo={speed}[original];[1:a]volume={background_volume}[music];[original][music]amix=inputs=2:duration=first[mixed]"
                command.extend(['-filter_complex',mix,'-map','0:v:0','-map','[mixed]','-c:a','aac','-shortest'])
            else:
                command.extend(['-map','0:v:0','-map','1:a:0','-af',f'volume={background_volume}','-c:a','aac','-shortest'])
        else:
            af = [f"volume={max(0,float(options.get('volume',1)))}"]
            if speed != 1: af.append(f'atempo={speed}')
            command.extend(['-af',','.join(af),'-c:a','aac'])
        command.extend(['-movflags','+faststart',str(output)])
        subprocess.run(command, check=True, capture_output=True, timeout=600)
        extra_outputs = []
        if options.get('split'):
            split_at = float(options.get('start', 0))
            if split_at <= 0: raise ValueError('분할할 위치를 시작 초에 입력하세요.')
            first = job_dir / 'split_1.mp4'; second = job_dir / 'split_2.mp4'
            for path, trim in ((first, ['-t', str(split_at)]), (second, ['-ss', str(split_at)])):
                subprocess.run([ffmpeg,'-y','-i',str(source),*trim,'-c:v','libx264','-preset','veryfast',
                                '-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(path)],
                               check=True,capture_output=True,timeout=600)
            output = first
            extra_outputs.append(file_record(second))
        record = {'status':'TESTED_PASS','job_id':job_id,'lane':'video','operation':'video_edit',
                  'command':str(payload.get('command','영상 편집')), 'input':file_record(source),
                  'primary_output':file_record(output),'outputs':[file_record(output)] + extra_outputs + ([file_record(background_source)] if background_source else []),
                  'runtime_result':{'engine':'FFmpeg','options':options,'model_inference':False,'sampled_frames':0}}
        (job_dir/'JOB_EVIDENCE.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        self.records[job_id]=record
        return record

    def import_media(self, payload: dict) -> dict:
        """Decode browser-compatible video without cropping and retain original input."""
        import subprocess
        from PIL import Image
        kind = payload.get('kind')
        if kind not in {'photo', 'video'}:
            raise ValueError('사진 또는 영상만 불러올 수 있습니다.')
        source = self._store_input(str(payload['filename']), str(payload['content_base64']))
        job_id = str(uuid4()); job_dir = self.jobs / job_id; job_dir.mkdir()
        if kind == 'photo':
            from PIL import ImageOps
            output = job_dir / 'original_photo.png'
            with Image.open(source) as image:
                image = ImageOps.exif_transpose(image)
                image.save(output, format='PNG'); dimensions = list(image.size)
        else:
            output = job_dir / 'original_video_preview.mp4'
            package = os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT')
            ffmpeg = str(Path(package) / 'tools/ffmpeg/ffmpeg.exe') if package else 'ffmpeg'
            ffprobe = str(Path(package) / 'tools/ffmpeg/ffprobe.exe') if package else 'ffprobe'
            command = [ffmpeg, '-y', '-i', str(source), '-map', '0:v:0', '-map', '0:a?',
                       '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264',
                       '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                       '-movflags', '+faststart', str(output)]
            subprocess.run(command, check=True, capture_output=True, timeout=600)
            probe = subprocess.run([ffprobe, '-v', 'error', '-select_streams', 'v:0',
                                    '-show_entries', 'stream=width,height', '-of', 'json', str(output)],
                                   check=True, capture_output=True, text=True)
            info = json.loads(probe.stdout)['streams'][0]
            dimensions = [info['width'], info['height']]
        record = {'status':'TESTED_PASS', 'job_id':job_id, 'lane':kind, 'operation':'import',
                  'command':'원본 불러오기', 'input':file_record(source), 'primary_output':file_record(output),
                  'outputs':[file_record(source), file_record(output)],
                  'runtime_result':{'result_size':dimensions, 'model_inference':False, 'sampled_frames':0}}
        (job_dir/'JOB_EVIDENCE.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        self.records[job_id] = record
        return record

    def store_photo_edit(self, payload: dict) -> dict:
        """Persist a decoded real pixel edit as a project artifact, without model claims."""
        from PIL import Image
        source = self._store_input('photo_edit.png', str(payload['content_base64']))
        job_id = str(uuid4())
        job_dir = self.jobs / job_id
        job_dir.mkdir()
        output = job_dir / 'edited_photo.png'
        with Image.open(source) as image:
            image.load()
            if image.width * image.height > 40_000_000:
                raise ValueError('사진은 최대 4천만 화소까지 지원합니다.')
            image.save(output, format='PNG')
            dimensions = list(image.size)
        record = {'status': 'TESTED_PASS', 'job_id': job_id, 'lane': 'photo',
                  'operation': 'photo_edit', 'command': str(payload.get('command', '사진 보정')),
                  'input': file_record(source), 'primary_output': file_record(output),
                  'outputs': [file_record(output)],
                  'runtime_result': {'engine': 'browser_canvas_pixels_verified_by_Pillow',
                                     'result_size': dimensions, 'options': payload.get('options', {}),
                                     'model_inference': False}}
        (job_dir / 'JOB_EVIDENCE.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        self.records[job_id] = record
        return record

    def save_project(self, payload: dict) -> dict:
        job_ids = list(dict.fromkeys(payload.get("job_ids", [])))
        selected = [self.records[job_id] for job_id in job_ids if job_id in self.records]
        if not selected or any(item["status"] != "TESTED_PASS" for item in selected): raise ValueError("only completed real jobs can be saved")
        project_id = str(payload.get("project_id") or uuid4())
        path = self.projects / f"{project_id}.json"
        record = {"project_id": project_id, "saved_at": now(), "job_ids": job_ids, "jobs": selected, "status": "SAVED"}
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"status": "SAVED", "project_id": project_id, "project": file_record(path)}

    def export_project(self, project_id: str) -> dict:
        source = self.projects / f"{project_id}.json"
        if not source.is_file(): raise ValueError("saved project is unavailable")
        export = self.projects / f"{project_id}_export.zip"
        project = json.loads(source.read_text(encoding="utf-8"))
        with zipfile.ZipFile(export, "w", compression=zipfile.ZIP_DEFLATED) as package:
            package.write(source, "project.json")
            for job in project["jobs"]:
                for output in job["outputs"]:
                    path = Path(output["path"])
                    if path.is_file(): package.write(path, f"jobs/{job['job_id']}/{path.name}")
        if not zipfile.is_zipfile(export): raise RuntimeError("export archive validation failed")
        return {"status": "EXPORTED", "project_id": project_id, "export": file_record(export)}


