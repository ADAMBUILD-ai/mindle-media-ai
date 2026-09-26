"""Direct acquisition and fail-closed verification of perpetual-use alternative models."""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "alternative_model_stage"
PRIVATE_REPO = "MINDLE1846/MINDLE-MEDIA-AI-MODELS"
WHISPER_REPO = "openai/whisper-small"
WHISPER_REVISION = "973afd24965f72e36ca33b3055d56a652f456b4d"
INTEL_REPO = "openvinotoolkit/open_model_zoo"
INTEL_REVISION = "a6946b6d6ce42cbf4278df20275fab199655fc7d"
INTEL_PREFIX = "models/intel/single-image-super-resolution-1032"
WHISPER_FILES = ("config.json", "generation_config.json", "model.safetensors", "preprocessor_config.json", "tokenizer.json", "tokenizer_config.json")
INTEL_FILES = {
    "single-image-super-resolution-1032.xml": ("https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/single-image-super-resolution-1032/FP32/single-image-super-resolution-1032.xml", 78485, "4f355965e070341e1f1df5b954213e0ecca5d43faf8a0c9770efdf04c7442c88fb0aaeb825fc8091b30f0a674c808446"),
    "single-image-super-resolution-1032.bin": ("https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/single-image-super-resolution-1032/FP32/single-image-super-resolution-1032.bin", 119436, "ec5a759c2d43eebf679040638ad765bc6ce5c16253421ddeb8acafd1ab6c8cb406f9f85b274771d9f670efc3d824e926"),
}


def stamp() -> str: return datetime.now(timezone.utc).isoformat()
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()
def sha384(path: Path) -> str:
    h = hashlib.sha384()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()
def rec(path: Path, source_url: str | None = None) -> dict:
    value = {"file": str(path.relative_to(OUT)), "bytes": path.stat().st_size, "sha256": sha256(path)}
    if source_url: value["source_url"] = source_url
    return value
def http(url: str, target: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "MINDLE-MEDIA-AI-alternative-verifier/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r: target.write_bytes(r.read())
def license_from_card(card: str) -> str:
    found = re.search(r"(?m)^license:\s*([^\s#]+)", card)
    if not found: raise RuntimeError("official pinned model card has no license declaration")
    return found.group(1).lower()


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token: raise RuntimeError("HF_TOKEN unavailable")
    if os.environ.get("CUDA_VISIBLE_DEVICES") not in {"", None}: raise RuntimeError("CPU-only staging refused")
    api = HfApi(token=token)
    whisper_dir, intel_dir, legal_dir = OUT / "whisper-small", OUT / "intel-sisr-1032", OUT / "license"
    for d in (whisper_dir, intel_dir, legal_dir): d.mkdir(parents=True, exist_ok=True)

    info = api.model_info(WHISPER_REPO, revision=WHISPER_REVISION, token=token, files_metadata=True)
    if info.sha != WHISPER_REVISION: raise RuntimeError("official Whisper source revision mismatch")
    for name in WHISPER_FILES:
        fetched = Path(hf_hub_download(repo_id=WHISPER_REPO, filename=name, revision=WHISPER_REVISION, token=token, local_dir=str(whisper_dir)))
        if fetched.stat().st_size <= 0: raise RuntimeError(f"empty Whisper source artifact: {name}")
    card = Path(hf_hub_download(repo_id=WHISPER_REPO, filename="README.md", revision=WHISPER_REVISION, token=token, local_dir=str(whisper_dir)))
    if license_from_card(card.read_text(encoding="utf-8")) != "apache-2.0": raise RuntimeError("Whisper alternative license declaration mismatch")
    sibling = next((x for x in info.siblings if x.rfilename == "model.safetensors"), None)
    expected_lfs = getattr(getattr(sibling, "lfs", None), "sha256", None)
    if not expected_lfs or sha256(whisper_dir / "model.safetensors") != expected_lfs: raise RuntimeError("Whisper alternative exact weight SHA-256 mismatch")

    yml = legal_dir / "intel_model.yml"
    license_copy = legal_dir / "Apache-2.0.txt"
    http(f"https://raw.githubusercontent.com/{INTEL_REPO}/{INTEL_REVISION}/{INTEL_PREFIX}/model.yml", yml)
    http("https://www.apache.org/licenses/LICENSE-2.0.txt", license_copy)
    if "license: https://raw.githubusercontent.com/openvinotoolkit/open_model_zoo/master/LICENSE" not in yml.read_text(encoding="utf-8"):
        raise RuntimeError("Intel model license binding is absent")
    for name, (url, size, expected_sha384) in INTEL_FILES.items():
        target = intel_dir / name; http(url, target)
        if target.stat().st_size != size or sha384(target) != expected_sha384:
            raise RuntimeError(f"Intel exact artifact mismatch: {name}")

    manifest = {
        "schema_version": "1.0", "captured_at": stamp(), "scope": "DIRECT_ALTERNATIVE_ACQUISITION_CPU_ONLY",
        "resource_boundary": {"hardware": "CPU", "gpu_used": False, "paid_compute": False, "timeout_minutes": 15, "automatic_repeat": False},
        "alternatives": {
            "korean_stt": {"status": "VERIFIED_MODEL_CACHE", "source": {"repo_id": WHISPER_REPO, "revision": WHISPER_REVISION, "official_revision_verified": True, "license": "Apache-2.0", "license_binding": "pinned official model-card declaration plus Apache-2.0 text"}, "artifacts": [rec(whisper_dir / n) for n in WHISPER_FILES], "model_weight_lfs_sha256": expected_lfs, "perpetual_use_gate": "PERPETUAL_USE_EVIDENCE_READY"},
            "photo_upscale_4x": {"status": "VERIFIED_MODEL_CACHE", "source": {"repo_id": INTEL_REPO, "revision": INTEL_REVISION, "official_revision_verified": True, "license": "Apache-2.0", "license_binding": "pinned Intel model.yml explicitly binds Apache-2.0"}, "artifacts": [rec(intel_dir / n, url) | {"sha384": expected} for n, (url, _, expected) in INTEL_FILES.items()], "perpetual_use_gate": "PERPETUAL_USE_EVIDENCE_READY"},
        },
        "license_evidence": [rec(card), rec(yml), rec(license_copy, "https://www.apache.org/licenses/LICENSE-2.0.txt")],
        "gate_result": "PERPETUAL_USE_EVIDENCE_READY",
        "fail_closed": "Only this manifest's exact private cache revision and file SHA-256 values may be selected by the product runtime.",
        "secret_handling": "HF_TOKEN is read only from the masked GitHub Actions secret and is never serialized or printed.",
    }
    (OUT / "ALTERNATIVE_MODEL_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ops = []
    for path in sorted(OUT.rglob("*")):
        if not path.is_file() or ".cache" in path.relative_to(OUT).parts: continue
        if path.parent == whisper_dir: dest = f"VERIFIED_MODEL_CACHE/perpetual-use-alternatives/whisper-small/{path.name}"
        elif path.parent == intel_dir: dest = f"VERIFIED_MODEL_CACHE/perpetual-use-alternatives/intel-sisr-1032/{path.name}"
        else: dest = f"ALTERNATIVE_MODEL_EVIDENCE/{os.environ.get('GITHUB_RUN_ID','local')}/{path.relative_to(OUT).as_posix()}"
        ops.append(CommitOperationAdd(path_in_repo=dest, path_or_fileobj=str(path)))
    commit = api.create_commit(repo_id=PRIVATE_REPO, repo_type="model", operations=ops, commit_message=f"Stage perpetual-use alternatives for Actions run {os.environ.get('GITHUB_RUN_ID','local')}", token=token)
    env = os.environ.get("GITHUB_ENV")
    if not env: raise RuntimeError("GITHUB_ENV unavailable")
    Path(env).open("a", encoding="utf-8").write(f"MINDLE_ALTERNATIVE_CACHE_REVISION={commit.oid}\n")
    print("alternative models staged; cache revision exported to subsequent steps; gate=PERPETUAL_USE_EVIDENCE_READY")


if __name__ == "__main__": main()
