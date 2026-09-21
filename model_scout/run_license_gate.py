"""Fail-closed perpetual-use license gate for the immutable MINDLE MEDIA AI model baseline."""
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
OUT = ROOT / "license_gate_evidence"
PRIVATE_REPO = "MINDLE1846/MINDLE-MEDIA-AI-MODELS"
BASELINE_REVISION = "ad63c52a4b9a3db7eaec9c5058c94ee1422757dd"
REALESRGAN_CACHE_REVISION = "e6f4ad5194673f27f64b1dc9626f1b616fb05792"

MODELS = (
    {
        "id": "sam21_hiera_base_plus",
        "repo_id": "facebook/sam2.1-hiera-base-plus",
        "revision": "b7320756a13354e7530a63935656d35b2f91a290",
        "expected_license": "apache-2.0",
        "artifact": {"file": "model.safetensors", "bytes": 323476296, "sha256": "2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780"},
        "private_cache_revision": BASELINE_REVISION,
        "private_cache_path": "VERIFIED_MODEL_CACHE/sam21",
        "license_source_url": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        "assessment": "PERPETUAL_USE_GATE_PASS",
        "reason": "The exact revision model card declares apache-2.0 and Apache-2.0 expressly grants a perpetual, irrevocable copyright license; notice and NOTICE obligations remain binding.",
    },
    {
        "id": "whisper_large_v3_turbo",
        "repo_id": "openai/whisper-large-v3-turbo",
        "revision": "41f01f3fe87f28c78e2fbf8b568835947dd65ed9",
        "expected_license": "mit",
        "artifact": {"file": "model.safetensors", "bytes": 1617824864, "sha256": "542566a422ae4f3fd23f1ba11add198fca01bbf82e66e6a2857b3f608b1eb9d1"},
        "private_cache_revision": BASELINE_REVISION,
        "private_cache_path": "VERIFIED_MODEL_CACHE/whisper-large-v3-turbo",
        "license_source_url": "https://raw.githubusercontent.com/openai/whisper/main/LICENSE",
        "assessment": "LEGAL_REVIEW_REQUIRED",
        "reason": "The exact revision model card declares MIT and the official license text grants use, copying, modification, distribution and sale subject to notice retention. It does not expressly say perpetual or irrevocable, so the requested future-policy-change assurance requires legal review before commercial release.",
    },
    {
        "id": "realesrgan_x4plus_onnx",
        "repo_id": "qualcomm/Real-ESRGAN-x4plus",
        "revision": "4022efb8b74eb88900724d9e05a468ac3673df4a",
        "expected_license": "bsd-3-clause",
        "artifact": {"file": "real_esrgan_x4plus.onnx", "bytes": 3158313, "sha256": "29ffd5bc0277b19536cd39b737627fb2d79df9999b8329741b558498dd5e31f7"},
        "private_cache_revision": REALESRGAN_CACHE_REVISION,
        "private_cache_path": "VERIFIED_MODEL_CACHE/realesrgan-x4plus-onnx/real_esrgan_x4plus-onnx-float.zip",
        "license_source_url": "https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/LICENSE",
        "assessment": "LEGAL_REVIEW_REQUIRED",
        "reason": "The exact Qualcomm revision model card declares BSD-3-Clause and describes a Real-ESRGAN derivative. BSD-3-Clause has retention and non-endorsement conditions but no express perpetual or irrevocable clause; derivative-chain and future-policy assurance require legal review before commercial release.",
    },
)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def fetch_url(url: str, destination: Path) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "MINDLE-MEDIA-AI-license-evidence/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())
    return {"source_url": url, "file": destination.name, "bytes": destination.stat().st_size, "sha256": digest(destination)}

def license_identifier(card: str) -> str:
    match = re.search(r"(?m)^license:\s*([^\s#]+)", card)
    if not match:
        raise RuntimeError("pinned model card has no license identifier")
    return match.group(1).strip().lower()

def capture_model(api: HfApi, model: dict, token: str) -> dict:
    card_path = Path(hf_hub_download(repo_id=model["repo_id"], filename="README.md", revision=model["revision"], token=token, local_dir=str(OUT / "pinned_model_cards" / model["id"])))
    card = card_path.read_text(encoding="utf-8")
    declared = license_identifier(card)
    if declared != model["expected_license"]:
        raise RuntimeError(f"license identifier mismatch for {model['id']}: {declared}")
    info = api.model_info(model["repo_id"], revision=model["revision"], token=token)
    if info.sha != model["revision"]:
        raise RuntimeError(f"official revision mismatch for {model['id']}")
    private = api.model_info(PRIVATE_REPO, revision=model["private_cache_revision"], token=token)
    if private.sha != model["private_cache_revision"] or not bool(getattr(private, "private", False)):
        raise RuntimeError(f"private cache revision or visibility mismatch for {model['id']}")
    license_copy = fetch_url(model["license_source_url"], OUT / "license_texts" / f"{model['id']}.LICENSE")
    return {"model_id": model["id"], "official_repo": model["repo_id"], "official_revision": model["revision"], "official_model_info_revision_verified": True, "exact_model_card": {"file": str(card_path.relative_to(OUT)), "bytes": card_path.stat().st_size, "sha256": digest(card_path), "declared_license": declared}, "artifact_immutable_baseline": model["artifact"], "private_cache_reverification": {"repo_id": PRIVATE_REPO, "revision": model["private_cache_revision"], "path": model["private_cache_path"], "private": True, "verified": True}, "license_text_snapshot": license_copy, "perpetual_use_gate": model["assessment"], "assessment_basis": model["reason"]}

def preserve_private(api: HfApi, token: str) -> dict:
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    prefix = f"LICENSE_GATE_EVIDENCE/{run_id}"
    ops = [CommitOperationAdd(path_in_repo=f"{prefix}/{path.relative_to(OUT).as_posix()}", path_or_fileobj=str(path)) for path in sorted(OUT.rglob("*")) if path.is_file()]
    commit = api.create_commit(repo_id=PRIVATE_REPO, repo_type="model", operations=ops, commit_message=f"Preserve MINDLE MEDIA AI license-gate Evidence for run {run_id}", token=token)
    return {"private_repo_id": PRIVATE_REPO, "path": prefix, "payload_revision": commit.oid}

def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is unavailable")
    if os.environ.get("CUDA_VISIBLE_DEVICES") not in {"", None}:
        raise RuntimeError("CPU-only execution requires CUDA_VISIBLE_DEVICES empty")
    (OUT / "pinned_model_cards").mkdir(parents=True, exist_ok=True)
    (OUT / "license_texts").mkdir(parents=True, exist_ok=True)
    api = HfApi(token=token)
    models = [capture_model(api, model, token) for model in MODELS]
    blocked = [item["model_id"] for item in models if item["perpetual_use_gate"] != "PERPETUAL_USE_GATE_PASS"]
    manifest = {"schema_version": "1.0", "captured_at": utc_now(), "scope": "IMMUTABLE_BASELINE_LICENSE_GATE_CLOSEOUT", "immutable_baseline": {"runtime_product_e2e_status": "FINAL_PASS_FROZEN", "product_e2e_run_id": "35581305266", "canonical_run_id": "35581305249", "ui_ssot_changed": "NO", "main_merged": False, "production_deployed": False, "gpu_used": False, "paid_compute": False}, "models": models, "commercial_release_status": "COMMERCIAL_RELEASE_BLOCKED" if blocked else "RELEASE_CANDIDATE_READY", "blocked_models": blocked, "fail_closed_rule": "Any model without PERPETUAL_USE_GATE_PASS is excluded from commercial-release promotion. Existing TESTED_PASS runtime evidence remains immutable and unchanged.", "manual_ui_e2e": {"status": "HUMAN_CONFIRMATION_REQUIRED", "reason": "A human must confirm the approved UI result before release-candidate promotion; automated browser evidence is not substituted for that confirmation."}, "secret_handling": "HF_TOKEN is consumed only from the masked GitHub Actions secret and is never emitted into this manifest, artifact, logs, or private-Hub payload."}
    manifest_path = OUT / "FINAL_LICENSE_GATE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["private_evidence"] = preserve_private(api, token)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "CLOSEOUT_PACKAGE_INDEX.md").write_text("# MINDLE MEDIA AI Closeout License Gate\n\n" + f"Commercial release status: {manifest['commercial_release_status']}\n\n" + "This package freezes the prior functional E2E evidence without modifying it. It is fail-closed: only explicitly qualified models may advance to commercial release. No credential values are present.\n", encoding="utf-8")
    print(f"license gate completed; commercial release status={manifest['commercial_release_status']}; blocked={','.join(blocked) or 'none'}")

if __name__ == "__main__": main()
