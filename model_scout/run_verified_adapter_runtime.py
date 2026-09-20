"""Run fail-closed CPU validation through MINDLE MEDIA AI concrete adapters.

SAM 2.1 and Whisper are read only from the previously verified private cache
revision.  RealESRGAN is independently acquired from its pinned official release
metadata, verified, staged, and added without rewriting either baseline model.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import requests
from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download

from media_ai.contracts import MediaJob, MediaType
from media_ai.model_scout_integration import (
    InputArtifactIntake,
    IntegrationStatus,
    ModelScoutAdapterRegistry,
    ModelScoutHandoff,
    RuntimeIntegrationGate,
)
from media_ai.verified_model_adapters import (
    Sam21VerifiedAdapter,
    VerifiedModelIdentity,
    WhisperKoreanVerifiedAdapter,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "runtime_evidence"
INPUTS = WORK / "inputs"
OUTPUTS = WORK / "outputs"
LOGS = WORK / "logs"
MODELS = WORK / "models"

PRIVATE_BASELINE_REVISION = "ad63c52a4b9a3db7eaec9c5058c94ee1422757dd"
SAM = VerifiedModelIdentity(
    repo_id="facebook/sam2.1-hiera-base-plus",
    revision="b7320756a13354e7530a63935656d35b2f91a290",
    license="apache-2.0",
    weight_name="model.safetensors",
    weight_size_bytes=323_476_296,
    weight_sha256="2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780",
)
WHISPER = VerifiedModelIdentity(
    repo_id="openai/whisper-large-v3-turbo",
    revision="41f01f3fe87f28c78e2fbf8b568835947dd65ed9",
    license="mit",
    weight_name="model.safetensors",
    weight_size_bytes=1_617_824_864,
    weight_sha256="542566a422ae4f3fd23f1ba11add198fca01bbf82e66e6a2857b3f608b1eb9d1",
)
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

REALESRGAN_REPO = "qualcomm/Real-ESRGAN-x4plus"
REALESRGAN_REVISION = "4022efb8b74eb88900724d9e05a468ac3673df4a"
REALESRGAN_LICENSE = "bsd-3-clause"
REALESRGAN_ZIP = "real_esrgan_x4plus-onnx-float.zip"
REALESRGAN_ONNX_SHA = "29ffd5bc0277b19536cd39b737627fb2d79df9999b8329741b558498dd5e31f7"
REALESRGAN_DATA_SHA = "28fada125730d3c87d504d48dd8332837f65811ec431a570ea4919ba3eee3287"

FLEURS_REPO = "google/fleurs"
FLEURS_REVISION = "70bb2e84b976b7e960aa89f1c648e09c59f894dd"
FLEURS_LICENSE = "cc-by-4.0"
FLEURS_PARQUET = "parquet-data/ko_kr/test-00000-of-00001.parquet"

VIDEO_REPO = "opencv/opencv_extra"
VIDEO_REVISION = "9c5eefa1ef66cbeecc9a3d38e1c5308c22ebe830"
VIDEO_PATH = "testdata/highgui/video/big_buck_bunny.mp4"
VIDEO_URL = f"https://raw.githubusercontent.com/{VIDEO_REPO}/{VIDEO_REVISION}/{VIDEO_PATH}"
VIDEO_EXPECTED_BYTES = 315_058


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def card_license(info) -> str:
    card = getattr(info, "card_data", None)
    if card is None:
        return ""
    if hasattr(card, "to_dict"):
        card = card.to_dict()
    if not hasattr(card, "get"):
        return ""
    value = card.get("license", "")
    if isinstance(value, (list, tuple)):
        if len(value) != 1:
            return ""
        value = value[0]
    return str(value).strip().lower()


def remote_identity(sibling) -> tuple[int, str]:
    lfs = getattr(sibling, "lfs", None) or {}
    if hasattr(lfs, "to_dict"):
        lfs = lfs.to_dict()
    sha = str(lfs.get("sha256") or lfs.get("oid") or "").removeprefix("sha256:")
    size = int(lfs.get("size") or getattr(sibling, "size", -1) or -1)
    return size, sha


def choose_private_repo(api: HfApi, token: str) -> str:
    identity = api.whoami(token=token)
    visible = sorted(
        item.id
        for item in api.list_models(author=identity["name"], full=True, token=token)
        if bool(getattr(item, "private", False))
    )
    if len(visible) != 1:
        raise RuntimeError(f"expected exactly one repository-scoped private model repo, found {len(visible)}")
    info = api.model_info(visible[0], token=token)
    if not bool(getattr(info, "private", False)):
        raise RuntimeError("model persistence destination is not private")
    return visible[0]


def fetch_verified_snapshot(
    repo_id: str,
    baseline_revision: str,
    cache_path: str,
    expected: dict[str, tuple[int, str]],
    token: str,
) -> tuple[Path, list[dict]]:
    destination = MODELS / cache_path
    rows = []
    for name, (expected_bytes, expected_sha) in expected.items():
        path = Path(
            hf_hub_download(
                repo_id=repo_id,
                filename=f"VERIFIED_MODEL_CACHE/{cache_path}/{name}",
                revision=baseline_revision,
                token=token,
                local_dir=str(MODELS),
                force_download=True,
            )
        )
        actual = {"name": name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        if actual["bytes"] != expected_bytes or actual["sha256"] != expected_sha:
            raise RuntimeError(f"immutable private cache changed: {cache_path}/{name}")
        rows.append(actual)
    return destination, rows


def assert_remote_baseline(api: HfApi, repo_id: str, token: str, revision: str) -> dict:
    info = api.model_info(repo_id, revision=revision, token=token, files_metadata=True)
    if info.sha != revision or not bool(getattr(info, "private", False)):
        raise RuntimeError("private baseline revision or visibility mismatch")
    siblings = {item.rfilename: item for item in info.siblings}
    checks = {}
    for cache_path, identity in (("sam21", SAM), ("whisper-large-v3-turbo", WHISPER)):
        remote = siblings.get(f"VERIFIED_MODEL_CACHE/{cache_path}/model.safetensors")
        if remote is None:
            raise RuntimeError(f"private baseline is missing {cache_path} weight")
        size, sha = remote_identity(remote)
        if (size, sha) != (identity.weight_size_bytes, identity.weight_sha256):
            raise RuntimeError(f"private baseline identity changed for {cache_path}")
        checks[cache_path] = {"bytes": size, "sha256": sha}
    return {"revision": info.sha, "private": True, "weights": checks}


def find_realesrgan_url(payload: object) -> str:
    candidates: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            context = json.dumps(node, sort_keys=True).lower()
            urls = [value for value in node.values() if isinstance(value, str) and value.startswith("http")]
            if "onnx" in context and "float" in context and "w8a8" not in context:
                candidates.update(url for url in urls if ".zip" in url.lower())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(payload)
    if len(candidates) != 1:
        raise RuntimeError(f"failed closed selecting the pinned ONNX float release URL: {len(candidates)} candidates")
    return next(iter(candidates))


def acquire_realesrgan(api: HfApi, target_repo: str, token: str) -> dict:
    source_info = HfApi().model_info(
        REALESRGAN_REPO, revision=REALESRGAN_REVISION, files_metadata=True
    )
    if source_info.sha != REALESRGAN_REVISION:
        raise RuntimeError("RealESRGAN source revision mismatch")
    license_name = card_license(source_info)
    if license_name != REALESRGAN_LICENSE:
        raise RuntimeError(f"RealESRGAN license mismatch: {license_name!r}")
    metadata_path = Path(
        hf_hub_download(
            repo_id=REALESRGAN_REPO,
            filename="release_assets.json",
            revision=REALESRGAN_REVISION,
            local_dir=str(WORK / "realesrgan-source"),
            force_download=True,
        )
    )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    asset_url = find_realesrgan_url(metadata)
    archive = WORK / "realesrgan-source" / REALESRGAN_ZIP
    with requests.get(asset_url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with archive.open("wb") as target:
            for block in response.iter_content(1024 * 1024):
                if block:
                    target.write(block)
    archive_bytes, archive_sha = archive.stat().st_size, sha256_file(archive)
    with zipfile.ZipFile(archive) as package:
        names = {item.filename for item in package.infolist() if not item.is_dir()}
        basenames = {Path(name).name for name in names}
        required = {"real_esrgan_x4plus.onnx", "real_esrgan_x4plus.data"}
        if not required.issubset(basenames):
            raise RuntimeError(f"official RealESRGAN archive is incomplete: {sorted(names)}")
        for item in package.infolist():
            if Path(item.filename).is_absolute() or ".." in Path(item.filename).parts:
                raise RuntimeError(f"unsafe RealESRGAN archive member: {item.filename}")
    stage = subprocess.run(
        [
            sys.executable,
            "model_scout/stage_verified_model.py",
            "realesrgan",
            "--source",
            str(archive),
            "--expected-size",
            str(archive_bytes),
            "--expected-sha256",
            archive_sha,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    (LOGS / "realesrgan-stage.stdout.log").write_text(stage.stdout, encoding="utf-8")
    (LOGS / "realesrgan-stage.stderr.log").write_text(stage.stderr, encoding="utf-8")
    if stage.returncode != 0:
        raise RuntimeError(f"RealESRGAN fail-closed staging rejected the official archive: {stage.stderr[-500:]}")
    stage_record = json.loads(stage.stdout)
    extracted = Path(stage_record["target"])
    onnx = extracted / "real_esrgan_x4plus.onnx"
    data = extracted / "real_esrgan_x4plus.data"
    if sha256_file(onnx) != REALESRGAN_ONNX_SHA or sha256_file(data) != REALESRGAN_DATA_SHA:
        raise RuntimeError("RealESRGAN extracted official model identity mismatch")
    provenance = {
        "status": "VERIFIED_MODEL_CACHE",
        "official_repo_id": REALESRGAN_REPO,
        "official_revision": REALESRGAN_REVISION,
        "verified_license": license_name,
        "release_metadata_file": "release_assets.json",
        "release_metadata_sha256": sha256_file(metadata_path),
        "asset_url": asset_url,
        "archive": {"name": archive.name, "bytes": archive_bytes, "sha256": archive_sha},
        "extracted": [
            {"name": onnx.name, "bytes": onnx.stat().st_size, "sha256": sha256_file(onnx)},
            {"name": data.name, "bytes": data.stat().st_size, "sha256": sha256_file(data)},
        ],
        "staging": stage_record,
    }
    provenance_path = WORK / "realesrgan-source" / "SOURCE_PROVENANCE.json"
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    prefix = "VERIFIED_MODEL_CACHE/realesrgan-x4plus-onnx"
    head = api.model_info(target_repo, token=token, files_metadata=True)
    sibling_map = {item.rfilename: item for item in head.siblings}
    remote_archive = sibling_map.get(f"{prefix}/{archive.name}")
    if remote_archive is not None and remote_identity(remote_archive) == (archive_bytes, archive_sha):
        cache_revision = head.sha
        persistence = "ALREADY_PRESENT_EXACT_MATCH"
    else:
        commit = api.create_commit(
            repo_id=target_repo,
            repo_type="model",
            operations=[
                CommitOperationAdd(path_in_repo=f"{prefix}/{archive.name}", path_or_fileobj=str(archive)),
                CommitOperationAdd(path_in_repo=f"{prefix}/SOURCE_PROVENANCE.json", path_or_fileobj=str(provenance_path)),
            ],
            commit_message="Store verified pinned RealESRGAN ONNX artifact",
            token=token,
        )
        cache_revision = commit.oid
        persistence = "UPLOADED"
    remote = api.model_info(target_repo, revision=cache_revision, token=token, files_metadata=True)
    remote_file = {item.rfilename: item for item in remote.siblings}.get(f"{prefix}/{archive.name}")
    if remote_file is None or remote_identity(remote_file) != (archive_bytes, archive_sha):
        raise RuntimeError("RealESRGAN private cache round-trip identity mismatch")
    provenance["private_cache"] = {
        "repo_id": target_repo,
        "private": True,
        "path": f"{prefix}/{archive.name}",
        "revision": cache_revision,
        "persistence": persistence,
    }
    return provenance


def download_inputs() -> dict:
    import pyarrow.parquet as pq

    photo = ROOT / "model_scout/artifacts/public_architecture_fixtures/01_42756291.jpg"
    if not photo.is_file():
        raise RuntimeError("licensed real-photo fixture is unavailable")
    video = INPUTS / "big_buck_bunny.mp4"
    response = requests.get(VIDEO_URL, timeout=60)
    response.raise_for_status()
    video.write_bytes(response.content)
    if video.stat().st_size != VIDEO_EXPECTED_BYTES:
        raise RuntimeError("pinned OpenCV video byte count changed")

    dataset = HfApi().dataset_info(FLEURS_REPO, revision=FLEURS_REVISION, files_metadata=True)
    if dataset.sha != FLEURS_REVISION or card_license(dataset) != FLEURS_LICENSE:
        raise RuntimeError("FLEURS revision or license mismatch")
    parquet_path = Path(
        hf_hub_download(
            repo_id=FLEURS_REPO,
            repo_type="dataset",
            filename=FLEURS_PARQUET,
            revision=FLEURS_REVISION,
            local_dir=str(INPUTS / "fleurs"),
            force_download=True,
        )
    )
    batch = next(pq.ParquetFile(parquet_path).iter_batches(batch_size=1, columns=["audio", "transcription", "language"]))
    row = batch.to_pylist()[0]
    audio = row["audio"]
    audio_bytes = audio.get("bytes") if isinstance(audio, dict) else None
    if not audio_bytes:
        raise RuntimeError("pinned FLEURS row did not contain embedded audio bytes")
    wav = INPUTS / "fleurs_ko_kr_test_row0.wav"
    wav.write_bytes(audio_bytes)
    reference = str(row["transcription"]).strip()
    if not reference:
        raise RuntimeError("pinned FLEURS row has no Korean reference text")
    reference_path = INPUTS / "fleurs_ko_kr_test_row0_reference.json"
    reference_path.write_text(
        json.dumps({"reference": reference, "language": row.get("language")}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "photo": {
            "path": str(photo),
            "bytes": photo.stat().st_size,
            "sha256": sha256_file(photo),
            "source": "Wikimedia Commons licensed fixture manifest in repository",
            "license": "CC BY-SA 4.0",
        },
        "video": {
            "path": str(video),
            "bytes": video.stat().st_size,
            "sha256": sha256_file(video),
            "source_repo": VIDEO_REPO,
            "source_revision": VIDEO_REVISION,
            "source_path": VIDEO_PATH,
            "license": "CC BY 3.0 (Big Buck Bunny)",
        },
        "audio": {
            "path": str(wav),
            "bytes": wav.stat().st_size,
            "sha256": sha256_file(wav),
            "source_repo": FLEURS_REPO,
            "source_revision": FLEURS_REVISION,
            "source_path": FLEURS_PARQUET,
            "row": 0,
            "license": FLEURS_LICENSE,
            "reference": reference,
            "reference_file_sha256": sha256_file(reference_path),
        },
    }


def integration_receipt(
    lane: MediaType,
    operation: str,
    identity: VerifiedModelIdentity,
    weight: Path,
    adapter,
    input_path: Path,
    result: dict,
) -> dict:
    issued = utcnow()
    registry = ModelScoutAdapterRegistry()
    intake = InputArtifactIntake()
    handoff = ModelScoutHandoff(
        request_id=f"runtime-{uuid4()}",
        issue_id="PR-10",
        lane=lane,
        operation=operation,
        model_or_program_id=identity.repo_id,
        source="MINDLE private VERIFIED_MODEL_CACHE",
        revision=identity.revision,
        license_evidence=identity.license,
        artifact_path=weight,
        artifact_filename=identity.weight_name,
        artifact_size_bytes=identity.weight_size_bytes,
        artifact_sha256=identity.weight_sha256,
        runtime_backend=adapter.runtime_backend,
        device_requirement=adapter.device_requirement,
        adapter_id=adapter.adapter_id,
        adapter_version=adapter.adapter_version,
        verification_status=IntegrationStatus.VERIFIED,
        issued_at=issued,
    )
    registry.ingest(handoff)
    intake.ingest(lane, input_path, {"source_path": str(input_path)})
    gate = RuntimeIntegrationGate(registry, intake)
    job = MediaJob(
        request=f"verified runtime {operation}",
        input_path=input_path,
        media_type=lane,
        requested_operation=operation,
        source_provenance={"source_path": str(input_path)},
    )
    readiness = gate.readiness(job)
    if readiness != IntegrationStatus.RUNTIME_READY:
        raise RuntimeError(f"adapter integration did not reach RUNTIME_READY: {readiness}")
    primary = result["outputs"][0]
    callback = {
        "request_id": handoff.request_id,
        "issue_id": handoff.issue_id,
        "callback_id": f"callback-{uuid4()}",
        "job_id": job.id,
        "evidence_id": job.evidence_id,
        "lane": lane,
        "revision": identity.revision,
        "artifact_sha256": identity.weight_sha256,
        "adapter_id": adapter.adapter_id,
        "adapter_version": adapter.adapter_version,
        "status": IntegrationStatus.TESTED_PASS,
        "input_sha256": result["input_sha256"],
        "output_sha256": primary["sha256"],
        "output_path": primary["path"],
        "elapsed_ms": float(result.get("elapsed_ms", sum(row["elapsed_ms"] for row in result.get("samples", [])))),
        "runtime_backend": adapter.runtime_backend,
        "device_requirement": adapter.device_requirement,
        "sent_at": utcnow(),
    }
    delivery = gate.accept_callback(job, callback)
    return {
        "readiness": readiness,
        "callback_status": callback["status"],
        "delivery_gate": delivery,
        "adapter_id": adapter.adapter_id,
        "adapter_version": adapter.adapter_version,
        "job_id": job.id,
        "evidence_id": job.evidence_id,
    }


def upload_runtime_evidence(api: HfApi, target_repo: str, token: str, evidence: dict) -> str:
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    prefix = f"TESTED_RUNTIME_EVIDENCE/{run_id}"
    evidence_path = WORK / "RUNTIME_VALIDATION_EVIDENCE.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    operations = []
    for path in sorted(WORK.rglob("*")):
        if path.is_file() and "models" not in path.relative_to(WORK).parts and "realesrgan-source" not in path.relative_to(WORK).parts:
            operations.append(
                CommitOperationAdd(
                    path_in_repo=f"{prefix}/{path.relative_to(WORK).as_posix()}",
                    path_or_fileobj=str(path),
                )
            )
    commit = api.create_commit(
        repo_id=target_repo,
        repo_type="model",
        operations=operations,
        commit_message=f"Preserve TESTED_PASS adapter runtime evidence for Actions run {run_id}",
        token=token,
    )
    evidence["persistence"] = {
        "private_repo_id": target_repo,
        "path": prefix,
        "payload_revision": commit.oid,
    }
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_commit = api.create_commit(
        repo_id=target_repo,
        repo_type="model",
        operations=[
            CommitOperationAdd(
                path_in_repo=f"{prefix}/RUNTIME_VALIDATION_EVIDENCE.json",
                path_or_fileobj=str(evidence_path),
            )
        ],
        commit_message=f"Record final runtime evidence manifest for Actions run {run_id}",
        token=token,
    )
    evidence["persistence"]["manifest_revision"] = manifest_commit.oid
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_commit.oid


def main() -> None:
    for directory in (WORK, INPUTS, OUTPUTS, LOGS, MODELS):
        directory.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("MINDLE_MEDIA_HF_WRITE_TOKEN is unavailable")
    import cv2
    import pyarrow
    import torch
    import transformers

    if torch.cuda.is_available():
        raise RuntimeError("GPU availability is prohibited for this CPU-only validation")
    api = HfApi(token=token)
    target_repo = choose_private_repo(api, token)
    baseline = assert_remote_baseline(api, target_repo, token, PRIVATE_BASELINE_REVISION)
    sam_dir, sam_files = fetch_verified_snapshot(target_repo, PRIVATE_BASELINE_REVISION, "sam21", SAM_FILES, token)
    whisper_dir, whisper_files = fetch_verified_snapshot(
        target_repo, PRIVATE_BASELINE_REVISION, "whisper-large-v3-turbo", WHISPER_FILES, token
    )
    realesrgan = acquire_realesrgan(api, target_repo, token)
    inputs = download_inputs()

    sam_adapter = Sam21VerifiedAdapter(sam_dir, SAM)
    photo_result = sam_adapter.segment_photo(Path(inputs["photo"]["path"]), OUTPUTS / "sam_photo")
    video_result = sam_adapter.track_video(Path(inputs["video"]["path"]), OUTPUTS / "sam_video")
    photo_receipt = integration_receipt(
        MediaType.PHOTO, "segment", SAM, sam_adapter.weight, sam_adapter,
        Path(inputs["photo"]["path"]), photo_result,
    )
    video_receipt = integration_receipt(
        MediaType.VIDEO, "track", SAM, sam_adapter.weight, sam_adapter,
        Path(inputs["video"]["path"]), video_result,
    )
    sam_adapter.close()
    del sam_adapter

    whisper_adapter = WhisperKoreanVerifiedAdapter(whisper_dir, WHISPER)
    whisper_result = whisper_adapter.transcribe(
        Path(inputs["audio"]["path"]), OUTPUTS / "whisper_ko", inputs["audio"]["reference"]
    )
    whisper_receipt = integration_receipt(
        MediaType.KOREAN_AUDIO, "transcribe", WHISPER, whisper_adapter.weight, whisper_adapter,
        Path(inputs["audio"]["path"]), whisper_result,
    )
    whisper_adapter.close()

    after_additions = assert_remote_baseline(api, target_repo, token, api.model_info(target_repo, token=token).sha)
    evidence = {
        "schema_version": "1.0",
        "captured_at": utcnow(),
        "status": "TESTED_PASS",
        "scope": "TEST_ONLY_NO_PRODUCTION_ENABLEMENT",
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
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "opencv": cv2.__version__,
            "pyarrow": pyarrow.__version__,
        },
        "immutable_baseline": {
            "private_repo_id": target_repo,
            "baseline_revision": PRIVATE_BASELINE_REVISION,
            "before": baseline,
            "after_additions": after_additions,
            "sam21": {"identity": SAM.__dict__, "files": sam_files},
            "whisper": {"identity": WHISPER.__dict__, "files": whisper_files},
            "mutation_policy": "SAM 2.1 and Whisper paths were read only; additions use separate paths and commits.",
        },
        "inputs": inputs,
        "results": {
            "sam21_photo_segmentation": {"result": photo_result, "integration_receipt": photo_receipt},
            "sam21_video_tracking": {"result": video_result, "integration_receipt": video_receipt},
            "whisper_korean_stt": {"result": whisper_result, "integration_receipt": whisper_receipt},
        },
        "realesrgan": realesrgan,
        "promotion": {
            "sam21": "TESTED_PASS",
            "whisper": "TESTED_PASS",
            "realesrgan": "VERIFIED_MODEL_CACHE",
            "production_enabled": False,
        },
    }
    upload_runtime_evidence(api, target_repo, token, evidence)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
