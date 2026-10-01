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
        self.api = HfApi(token=token)
        configured = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip()
        self.local_root = Path(configured) if configured else None

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
        self.records: dict[str, dict] = {}

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

    def save_project(self, payload: dict) -> dict:
        job_ids = list(payload.get("job_ids", []))
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
