"""Run final fail-closed RealESRGAN x4plus CPU inference from the verified private cache."""
from __future__ import annotations

import json
import os
import platform
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download

from media_ai.contracts import MediaJob, MediaType
from media_ai.model_scout_integration import (
    InputArtifactIntake,
    IntegrationStatus,
    ModelScoutAdapterRegistry,
    ModelScoutHandoff,
    RuntimeIntegrationGate,
)
from media_ai.realesrgan_verified_adapter import (
    RealESRGANIdentity,
    RealESRGANX4PlusVerifiedAdapter,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "realesrgan_runtime_evidence"
MODELS = WORK / "models"
OUTPUTS = WORK / "outputs"
LOGS = WORK / "logs"
PRIVATE_REPO = "MINDLE1846/MINDLE-MEDIA-AI-MODELS"
PRIVATE_CACHE_REVISION = "e6f4ad5194673f27f64b1dc9626f1b616fb05792"
PRIVATE_CACHE_PATH = "VERIFIED_MODEL_CACHE/realesrgan-x4plus-onnx/real_esrgan_x4plus-onnx-float.zip"
PRIOR_EVIDENCE = ROOT / "evidence/model_scout/VERIFIED_ADAPTER_RUNTIME_20260920.json"
PRIOR_EVIDENCE_BYTES = 17_375
PRIOR_EVIDENCE_SHA256 = "f75ed10af08456215c00d920e480e2bdbb096d0659c6d7bbabcf5529df7e7bf1"
INPUT = ROOT / "model_scout/artifacts/realesrgan_qualcomm/benchmark/01_input_128.png"
INPUT_BYTES = 38_721
INPUT_SHA256 = "112d9ed220e4a990bc86efaafef8a2575548c65be39b432a67ac95471a73bcd2"

IDENTITY = RealESRGANIdentity(
    repo_id="qualcomm/Real-ESRGAN-x4plus",
    revision="4022efb8b74eb88900724d9e05a468ac3673df4a",
    license="bsd-3-clause",
    archive_name="real_esrgan_x4plus-onnx-float.zip",
    archive_size_bytes=62_174_026,
    archive_sha256="e6cb215390f3800b56baa0e9140907d81f5143a4b96c184a635c79dfee2e28df",
    onnx_name="real_esrgan_x4plus.onnx",
    onnx_size_bytes=3_158_313,
    onnx_sha256="29ffd5bc0277b19536cd39b737627fb2d79df9999b8329741b558498dd5e31f7",
    data_name="real_esrgan_x4plus.data",
    data_size_bytes=66_737_664,
    data_sha256="28fada125730d3c87d504d48dd8332837f65811ec431a570ea4919ba3eee3287",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def remote_identity(sibling) -> tuple[int, str]:
    lfs = getattr(sibling, "lfs", None) or {}
    if hasattr(lfs, "to_dict"):
        lfs = lfs.to_dict()
    digest = str(lfs.get("sha256") or lfs.get("oid") or "").removeprefix("sha256:")
    size = int(lfs.get("size") or getattr(sibling, "size", -1) or -1)
    return size, digest


def assert_prior_baseline() -> dict:
    if not PRIOR_EVIDENCE.is_file():
        raise RuntimeError("SAM/Whisper immutable Evidence is unavailable")
    if PRIOR_EVIDENCE.stat().st_size != PRIOR_EVIDENCE_BYTES or sha256_file(PRIOR_EVIDENCE) != PRIOR_EVIDENCE_SHA256:
        raise RuntimeError("SAM/Whisper immutable Evidence changed")
    evidence = json.loads(PRIOR_EVIDENCE.read_text(encoding="utf-8"))
    if evidence.get("promotion", {}).get("sam21") != "TESTED_PASS":
        raise RuntimeError("SAM 2.1 baseline is not TESTED_PASS")
    if evidence.get("promotion", {}).get("whisper") != "TESTED_PASS":
        raise RuntimeError("Whisper baseline is not TESTED_PASS")
    return {
        "path": str(PRIOR_EVIDENCE.relative_to(ROOT)),
        "bytes": PRIOR_EVIDENCE_BYTES,
        "sha256": PRIOR_EVIDENCE_SHA256,
        "sam21": evidence["immutable_baseline"]["sam21"]["identity"],
        "whisper": evidence["immutable_baseline"]["whisper"]["identity"],
        "sam_runtime_evidence": evidence["results"]["sam21_photo_segmentation"],
        "whisper_runtime_evidence": evidence["results"]["whisper_korean_stt"],
        "unchanged": True,
    }


def fetch_verified_model(api: HfApi, token: str) -> tuple[Path, Path, Path, dict]:
    info = api.model_info(PRIVATE_REPO, revision=PRIVATE_CACHE_REVISION, token=token, files_metadata=True)
    if info.sha != PRIVATE_CACHE_REVISION or not bool(getattr(info, "private", False)):
        raise RuntimeError("RealESRGAN private cache revision or visibility mismatch")
    sibling = {item.rfilename: item for item in info.siblings}.get(PRIVATE_CACHE_PATH)
    expected_archive = (IDENTITY.archive_size_bytes, IDENTITY.archive_sha256)
    if sibling is None or remote_identity(sibling) != expected_archive:
        raise RuntimeError("RealESRGAN private cache archive identity mismatch")
    archive = Path(
        hf_hub_download(
            repo_id=PRIVATE_REPO,
            filename=PRIVATE_CACHE_PATH,
            revision=PRIVATE_CACHE_REVISION,
            token=token,
            local_dir=str(MODELS),
            force_download=True,
        )
    )
    if (archive.stat().st_size, sha256_file(archive)) != expected_archive:
        raise RuntimeError("downloaded RealESRGAN cache archive changed")
    extracted = MODELS / "extracted"
    extracted.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        files = [item for item in package.infolist() if not item.is_dir()]
        for item in files:
            member = Path(item.filename)
            if member.is_absolute() or ".." in member.parts:
                raise RuntimeError(f"unsafe RealESRGAN archive member: {item.filename}")
        package.extractall(extracted)
    onnx_matches = list(extracted.rglob(IDENTITY.onnx_name))
    data_matches = list(extracted.rglob(IDENTITY.data_name))
    if len(onnx_matches) != 1 or len(data_matches) != 1 or onnx_matches[0].parent != data_matches[0].parent:
        raise RuntimeError("RealESRGAN archive layout is not canonical")
    IDENTITY.verify(archive, onnx_matches[0], data_matches[0])
    return archive, onnx_matches[0], data_matches[0], {
        "repo_id": PRIVATE_REPO,
        "private": True,
        "cache_revision": PRIVATE_CACHE_REVISION,
        "cache_path": PRIVATE_CACHE_PATH,
        "round_trip_verified": True,
    }


def integration_receipt(adapter, input_path: Path, result: dict) -> dict:
    issued = utcnow()
    registry = ModelScoutAdapterRegistry()
    intake = InputArtifactIntake()
    request_id = f"realesrgan-runtime-{uuid4()}"
    handoff = ModelScoutHandoff(
        request_id=request_id,
        issue_id="PR-10",
        lane=MediaType.PHOTO,
        operation="upscale",
        model_or_program_id=IDENTITY.repo_id,
        source="MINDLE private VERIFIED_MODEL_CACHE",
        revision=IDENTITY.revision,
        license_evidence=IDENTITY.license,
        artifact_path=adapter.onnx,
        artifact_filename=IDENTITY.onnx_name,
        artifact_size_bytes=IDENTITY.onnx_size_bytes,
        artifact_sha256=IDENTITY.onnx_sha256,
        runtime_backend=adapter.runtime_backend,
        device_requirement=adapter.device_requirement,
        adapter_id=adapter.adapter_id,
        adapter_version=adapter.adapter_version,
        verification_status=IntegrationStatus.VERIFIED,
        issued_at=issued,
    )
    registry.ingest(handoff)
    intake.ingest(MediaType.PHOTO, input_path, {"source_path": str(input_path)})
    gate = RuntimeIntegrationGate(registry, intake)
    job = MediaJob(
        request="verified RealESRGAN x4plus CPU upscale",
        input_path=input_path,
        media_type=MediaType.PHOTO,
        requested_operation="upscale",
        source_provenance={"source_path": str(input_path)},
    )
    readiness = gate.readiness(job)
    if readiness != IntegrationStatus.RUNTIME_READY:
        raise RuntimeError(f"RealESRGAN Adapter did not reach RUNTIME_READY: {readiness}")
    callback = {
        "request_id": request_id,
        "issue_id": "PR-10",
        "callback_id": f"callback-{uuid4()}",
        "job_id": job.id,
        "evidence_id": job.evidence_id,
        "lane": MediaType.PHOTO,
        "revision": IDENTITY.revision,
        "artifact_sha256": IDENTITY.onnx_sha256,
        "adapter_id": adapter.adapter_id,
        "adapter_version": adapter.adapter_version,
        "status": IntegrationStatus.TESTED_PASS,
        "input_sha256": result["input"]["sha256"],
        "output_sha256": result["output"]["sha256"],
        "output_path": result["output"]["path"],
        "elapsed_ms": result["elapsed_ms"],
        "runtime_backend": adapter.runtime_backend,
        "device_requirement": adapter.device_requirement,
        "sent_at": utcnow(),
    }
    delivered = gate.accept_callback(job, callback)
    return {
        "readiness": readiness,
        "callback_status": callback["status"],
        "delivery_gate": delivered,
        "adapter_id": adapter.adapter_id,
        "adapter_version": adapter.adapter_version,
        "job_id": job.id,
        "evidence_id": job.evidence_id,
    }


def persist(api: HfApi, token: str, evidence: dict) -> None:
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    prefix = f"TESTED_RUNTIME_EVIDENCE/{run_id}/realesrgan-final"
    evidence_path = WORK / "REALESRGAN_RUNTIME_EVIDENCE.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    operations = []
    for path in (INPUT, Path(evidence["runtime_result"]["output"]["path"]), LOGS / "runtime.log", evidence_path):
        operations.append(
            CommitOperationAdd(path_in_repo=f"{prefix}/{path.name}", path_or_fileobj=str(path))
        )
    commit = api.create_commit(
        repo_id=PRIVATE_REPO,
        repo_type="model",
        operations=operations,
        commit_message=f"Preserve RealESRGAN TESTED_PASS Evidence for Actions run {run_id}",
        token=token,
    )
    evidence["persistence"] = {
        "private_repo_id": PRIVATE_REPO,
        "path": prefix,
        "payload_revision": commit.oid,
    }
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = api.create_commit(
        repo_id=PRIVATE_REPO,
        repo_type="model",
        operations=[
            CommitOperationAdd(
                path_in_repo=f"{prefix}/{evidence_path.name}", path_or_fileobj=str(evidence_path)
            )
        ],
        commit_message=f"Finalize RealESRGAN TESTED_PASS manifest for Actions run {run_id}",
        token=token,
    )
    evidence["persistence"]["manifest_revision"] = manifest.oid
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for directory in (WORK, MODELS, OUTPUTS, LOGS):
        directory.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("MINDLE_MEDIA_HF_WRITE_TOKEN is unavailable")
    import numpy as np
    import onnxruntime as ort
    from PIL import __version__ as pillow_version

    if "CUDAExecutionProvider" in ort.get_available_providers():
        raise RuntimeError("GPU provider is present; refusing CPU-only validation")
    prior = assert_prior_baseline()
    if not INPUT.is_file() or INPUT.stat().st_size != INPUT_BYTES or sha256_file(INPUT) != INPUT_SHA256:
        raise RuntimeError("existing RealESRGAN photo fixture changed")
    api = HfApi(token=token)
    archive, onnx, data, private_cache = fetch_verified_model(api, token)
    adapter = RealESRGANX4PlusVerifiedAdapter(archive, onnx, data, IDENTITY)
    log_path = LOGS / "runtime.log"
    log_path.write_text(
        f"started_at={utcnow()}\nprovider=CPUExecutionProvider\nadapter={adapter.adapter_id}\n",
        encoding="utf-8",
    )
    result = adapter.upscale(INPUT, OUTPUTS / "01_realesrgan_x4plus_4x.png")
    receipt = integration_receipt(adapter, INPUT, result)
    log_path.write_text(
        log_path.read_text(encoding="utf-8")
        + f"completed_at={utcnow()}\nstatus=TESTED_PASS\nelapsed_ms={result['elapsed_ms']}\n"
        + f"input_sha256={result['input']['sha256']}\noutput_sha256={result['output']['sha256']}\n",
        encoding="utf-8",
    )
    if sha256_file(PRIOR_EVIDENCE) != PRIOR_EVIDENCE_SHA256:
        raise RuntimeError("SAM/Whisper Evidence changed during RealESRGAN validation")
    evidence = {
        "schema_version": "1.0",
        "captured_at": utcnow(),
        "status": "TESTED_PASS",
        "scope": "REAL_ESRGAN_TEST_ONLY_NO_PRODUCTION_ENABLEMENT",
        "github": {
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "source_commit": os.environ.get("GITHUB_SHA"),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "pull_request": 10,
        },
        "execution_environment": {
            "provider": "GitHub Actions public standard hosted runner",
            "hardware": "CPU",
            "gpu_used": False,
            "paid_compute": False,
            "timeout_minutes": 15,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "onnxruntime": ort.__version__,
            "onnxruntime_available_providers": ort.get_available_providers(),
            "onnxruntime_session_providers": adapter.providers,
            "numpy": np.__version__,
            "pillow": pillow_version,
        },
        "immutable_prior_evidence": prior,
        "model": {
            **IDENTITY.__dict__,
            "private_cache": private_cache,
            "archive_local_sha256_verified": sha256_file(archive),
            "onnx_local_sha256_verified": sha256_file(onnx),
            "data_local_sha256_verified": sha256_file(data),
        },
        "input_provenance": {
            "source": "existing repository RealESRGAN benchmark photo fixture",
            "source_fixture": "01_42756291.jpg",
            "source_title": "Baroque ceiling frescoes (Ljubljana Cathedral)",
            "license": "CC BY-SA 4.0",
            "repository_path": str(INPUT.relative_to(ROOT)),
        },
        "runtime_result": result,
        "integration_receipt": receipt,
        "promotion": {
            "sam21": "TESTED_PASS",
            "whisper": "TESTED_PASS",
            "realesrgan": "TESTED_PASS",
            "production_enabled": False,
        },
    }
    persist(api, token, evidence)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

