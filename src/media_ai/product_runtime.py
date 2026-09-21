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
WHISPER = VerifiedModelIdentity("openai/whisper-large-v3-turbo", "41f01f3fe87f28c78e2fbf8b568835947dd65ed9", "mit", "model.safetensors", 1_617_824_864, "542566a422ae4f3fd23f1ba11add198fca01bbf82e66e6a2857b3f608b1eb9d1")
SAM_FILES = {
    "config.json": (5705, "8e24a93b6a40d4dad86eaec383ce7b4044f37ec6360136460f5ff2ce55f87390"),
    "model.safetensors": (323_476_296, SAM.weight_sha256),
    "preprocessor_config.json": (683, "6ebf229ee259368ce4a8d4f2fe893a72b053023710853e257253939e601f583d"),
    "processor_config.json": (95, "f8a68e865cfad115c1c2763f3d93eca7b1c622da06da2a9273eb437fb2389b6d"),
}
WHISPER_FILES = {
    "config.json": (1256, "c5b526b3e3cd64cd8940dabb45e8ba726629e22d8ed389c29b552f9140daf04a"),
    "generation_config.json": (3772, "cce11bfe3aaa6ae9e072ea2637caaec8795e68d9b67e655a5af16ee509681a4c"),
    "model.safetensors": (1_617_824_864, WHISPER.weight_sha256),
    "preprocessor_config.json": (340, "7ccc62c6f2765af1f3b46c00c9b5894426835a05021c8b9c01eecb6dfb542711"),
    "tokenizer.json": (2_710_337, "297b13372ac43916285644fb9687add3cc62ee2a1adb60da3dc25cc94c1871fd"),
    "tokenizer_config.json": (282_843, "844b642c73a91359722f47b35705f7174686df33d252695d8572cf9ac03a6389"),
}
REALESRGAN = RealESRGANIdentity(
    "qualcomm/Real-ESRGAN-x4plus", "4022efb8b74eb88900724d9e05a468ac3673df4a", "bsd-3-clause",
    "real_esrgan_x4plus-onnx-float.zip", 62_174_026, "e6cb215390f3800b56baa0e9140907d81f5143a4b96c184a635c79dfee2e28df",
    "real_esrgan_x4plus.onnx", 3_158_313, "29ffd5bc0277b19536cd39b737627fb2d79df9999b8329741b558498dd5e31f7",
    "real_esrgan_x4plus.data", 66_737_664, "28fada125730d3c87d504d48dd8332837f65811ec431a570ea4919ba3eee3287",
)
REALESRGAN_CACHE_PATH = "VERIFIED_MODEL_CACHE/realesrgan-x4plus-onnx/real_esrgan_x4plus-onnx-float.zip"


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
        snapshot = self._download_files("sam21", SAM_FILES)
        adapter = Sam21VerifiedAdapter(snapshot, SAM)
        return adapter, {"identity": asdict(SAM), "private_cache": {"repo_id": PRIVATE_REPO, "revision": BASELINE_REVISION, "path": "VERIFIED_MODEL_CACHE/sam21", "read_only": True}}

    def whisper(self) -> tuple[WhisperKoreanVerifiedAdapter, dict]:
        snapshot = self._download_files("whisper-large-v3-turbo", WHISPER_FILES)
        adapter = WhisperKoreanVerifiedAdapter(snapshot, WHISPER)
        return adapter, {"identity": asdict(WHISPER), "private_cache": {"repo_id": PRIVATE_REPO, "revision": BASELINE_REVISION, "path": "VERIFIED_MODEL_CACHE/whisper-large-v3-turbo", "read_only": True}}

    def realesrgan(self) -> tuple[RealESRGANX4PlusVerifiedAdapter, dict]:
        info = self.api.model_info(PRIVATE_REPO, revision=REALESRGAN_CACHE_REVISION, token=self.token, files_metadata=True)
        if info.sha != REALESRGAN_CACHE_REVISION or not bool(getattr(info, "private", False)):
            raise RuntimeError("immutable RealESRGAN cache revision or visibility mismatch")
        archive = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=REALESRGAN_CACHE_PATH, revision=REALESRGAN_CACHE_REVISION, token=self.token, local_dir=str(self.downloads)))
        if archive.stat().st_size != REALESRGAN.archive_size_bytes or realesrgan_sha256(archive) != REALESRGAN.archive_sha256:
            raise RuntimeError("immutable RealESRGAN archive mismatch")
        extracted = self.downloads / "realesrgan-extracted"
        if not (extracted / REALESRGAN.onnx_name).is_file():
            with zipfile.ZipFile(archive) as package:
                for member in package.infolist():
                    name = Path(member.filename)
                    if name.is_absolute() or ".." in name.parts:
                        raise RuntimeError("unsafe RealESRGAN cache archive")
                package.extractall(extracted)
        matches = list(extracted.rglob(REALESRGAN.onnx_name))
        data_matches = list(extracted.rglob(REALESRGAN.data_name))
        if len(matches) != 1 or len(data_matches) != 1:
            raise RuntimeError("RealESRGAN cache layout mismatch")
        adapter = RealESRGANX4PlusVerifiedAdapter(archive, matches[0], data_matches[0], REALESRGAN)
        return adapter, {"identity": asdict(REALESRGAN), "private_cache": {"repo_id": PRIVATE_REPO, "revision": REALESRGAN_CACHE_REVISION, "path": REALESRGAN_CACHE_PATH, "read_only": True}}


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
                result = adapter.segment_photo(source, job_dir / "sam_photo") if operation == "segment" else adapter.track_video(source, job_dir / "sam_video")
                primary = Path(result["outputs"][-1 if operation == "segment" else 0]["path"])
                artifact = adapter.weight
            elif operation == "upscale":
                adapter, model = self.vault.realesrgan()
                output = job_dir / "realesrgan" / "upscaled_4x.png"
                result = adapter.upscale(source, output)
                primary = output; artifact = adapter.onnx
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
