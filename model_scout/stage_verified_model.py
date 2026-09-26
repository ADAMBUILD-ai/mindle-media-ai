"""Stage an already acquired, pinned model snapshot without network access."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
ARTIFACTS = ROOT / "artifacts"
EVIDENCE = ROOT.parent / "evidence" / "model_scout" / "LOCAL_MODEL_STAGE_MANIFEST.json"

SNAPSHOTS = {
    "sam21": {
        "repo_id": "facebook/sam2.1-hiera-base-plus",
        "weight_file": "model.safetensors",
        "target": ARTIFACTS / "sam21",
        "required": {"config.json", "model.safetensors", "preprocessor_config.json", "processor_config.json"},
        "revision": "b7320756a13354e7530a63935656d35b2f91a290",
    },
    "whisper": {
        "repo_id": "openai/whisper-large-v3-turbo",
        "weight_file": "model.safetensors",
        "target": ARTIFACTS / "whisper_turbo",
        "required": {"config.json", "generation_config.json", "model.safetensors", "preprocessor_config.json", "tokenizer.json", "tokenizer_config.json"},
        "revision": "41f01f3fe87f28c78e2fbf8b568835947dd65ed9",
    },
    "realesrgan": {
        "repo_id": "qualcomm/Real-ESRGAN-x4plus",
        "weight_file": "real_esrgan_x4plus-onnx-float.zip",
        "target": ARTIFACTS / "realesrgan_qualcomm" / "real_esrgan_x4plus-onnx-float",
        "required": {"real_esrgan_x4plus.onnx", "real_esrgan_x4plus.data"},
        "revision": "4022efb8b74eb88900724d9e05a468ac3673df4a",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract(source: Path, target: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        for member in archive.infolist():
            destination = (target / member.filename).resolve()
            if not destination.is_relative_to(target.resolve()):
                raise ValueError(f"unsafe archive member: {member.filename}")
        archive.extractall(target)


def stage_snapshot(model: str, source: Path, expected_size: int, expected_sha256: str) -> dict:
    if not source.is_dir():
        raise ValueError("SAM and Whisper require a complete local snapshot directory")
    target = SNAPSHOTS[model]["target"]
    target.mkdir(parents=True, exist_ok=True)
    source_files = {entry.name for entry in source.iterdir() if entry.is_file()}
    missing = SNAPSHOTS[model]["required"] - source_files
    if missing:
        raise ValueError(f"snapshot is incomplete: {', '.join(sorted(missing))}")
    if any(entry.suffix == ".pt" for entry in source.iterdir() if entry.is_file()):
        raise ValueError("pickle-based .pt files are prohibited in staged snapshots")
    model_file = source / "model.safetensors"
    actual_size = model_file.stat().st_size
    if actual_size != expected_size:
        raise ValueError("model.safetensors size does not match the supplied expected value")
    actual_sha256 = sha256(model_file)
    if actual_sha256 != expected_sha256.lower():
        raise ValueError("model.safetensors SHA-256 does not match the supplied expected value")
    for entry in source.iterdir():
        if entry.is_file():
            shutil.copy2(entry, target / entry.name)
    return {"status": "VERIFIED_MODEL_CACHE", "model": model, "repo_id": SNAPSHOTS[model]["repo_id"], "revision": SNAPSHOTS[model]["revision"], "file_name": "model.safetensors", "source": str(source), "target": str(target), "size_bytes": actual_size, "weight_sha256": actual_sha256}


def stage_realesrgan(source: Path, expected_size: int, expected_sha256: str) -> dict:
    if not source.is_file() or source.suffix.lower() != ".zip":
        raise ValueError("Real-ESRGAN requires the pinned ONNX float release zip")
    if source.name != SNAPSHOTS["realesrgan"]["weight_file"]:
        raise ValueError("release zip filename does not match the pinned release asset")
    actual_size = source.stat().st_size
    if actual_size != expected_size:
        raise ValueError("release zip size does not match the supplied expected value")
    actual_sha256 = sha256(source)
    if actual_sha256 != expected_sha256.lower():
        raise ValueError("release zip SHA-256 does not match the supplied expected value")
    target = SNAPSHOTS["realesrgan"]["target"]
    target.mkdir(parents=True, exist_ok=True)
    safe_extract(source, target)
    required = SNAPSHOTS["realesrgan"]["required"]
    candidate_roots = [target, target / source.stem]
    payload_root = next(
        (root for root in candidate_roots if all((root / name).is_file() for name in required)),
        None,
    )
    if payload_root is None:
        discovered = sorted(str(path.relative_to(target)) for path in target.rglob("*") if path.is_file())
        raise ValueError(f"release archive is incomplete or has an unexpected layout: {discovered}")
    return {"status": "VERIFIED_MODEL_CACHE", "model": "realesrgan", "repo_id": SNAPSHOTS["realesrgan"]["repo_id"], "revision": SNAPSHOTS["realesrgan"]["revision"], "file_name": source.name, "source": str(source), "target": str(payload_root), "size_bytes": actual_size, "release_sha256": actual_sha256, "model_sha256": sha256(payload_root / "real_esrgan_x4plus.onnx")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=SNAPSHOTS)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--expected-size", required=True, type=int)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    record = stage_realesrgan(args.source, args.expected_size, args.expected_sha256) if args.model == "realesrgan" else stage_snapshot(args.model, args.source, args.expected_size, args.expected_sha256)
    existing = json.loads(EVIDENCE.read_text(encoding="utf-8")) if EVIDENCE.exists() else {"schema_version": "1.0", "staged": []}
    existing["staged"] = [item for item in existing["staged"] if item["model"] != args.model] + [record]
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
