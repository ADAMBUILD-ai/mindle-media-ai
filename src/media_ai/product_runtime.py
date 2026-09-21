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

    def _alternatives(self) -> tuple[str, dict]:
        revision = os.environ.get("MINDLE_ALTERNATIVE_CACHE_REVISION", "").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise RuntimeError("perpetual-use alternative cache revision is required")
        info = self.api.model_info(PRIVATE_REPO, revision=revision, token=self.token, files_metadata=True)
        if info.sha != revision or not bool(getattr(info, "private", False)):
            raise RuntimeError("alternative private cache revision or visibility mismatch")
        manifest_path = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=f"ALTERNATIVE_MODEL_EVIDENCE/{os.environ.get('GITHUB_RUN_ID','local')}/ALTERNATIVE_MODEL_MANIFEST.json", revision=revision, token=self.token, local_dir=str(self.downloads)))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("gate_result") != "PERPETUAL_USE_EVIDENCE_READY":
            raise RuntimeError("alternative perpetual-use gate is not closed")
        return revision, manifest

    def _alternative_files(self, revision: str, folder: str, artifacts: list[dict]) -> Path:
        destination = self.downloads / ALT_CACHE_PREFIX / folder
        for item in artifacts:
            name, size, digest = Path(item["file"]).name, item["bytes"], item["sha256"]
            path = Path(hf_hub_download(repo_id=PRIVATE_REPO, filename=f"{ALT_CACHE_PREFIX}/{folder}/{name}", revision=revision, token=self.token, local_dir=str(self.downloads)))
            if path.stat().st_size != size or sha256_file(path) != digest:
                raise RuntimeError(f"alternative immutable cache mismatch: {folder}/{name}")
        return destination

    def whisper(self) -> tuple[WhisperKoreanVerifiedAdapter, dict]:
        revision, manifest = self._alternatives()
        item = manifest["alternatives"]["korean_stt"]
        snapshot = self._alternative_files(revision, "whisper-small", item["artifacts"])
        weight = next(x for x in item["artifacts"] if x["file"].endswith("model.safetensors"))
        identity = VerifiedModelIdentity(item["source"]["repo_id"], item["source"]["revision"], item["source"]["license"].lower(), "model.safetensors", weight["bytes"], weight["sha256"])
        adapter = WhisperKoreanVerifiedAdapter(snapshot, identity)
        return adapter, {"identity": asdict(identity), "private_cache": {"repo_id": PRIVATE_REPO, "revision": revision, "path": f"{ALT_CACHE_PREFIX}/whisper-small", "read_only": True}, "perpetual_use_gate": item["perpetual_use_gate"]}

    def realesrgan(self) -> tuple[IntelSISR1032VerifiedAdapter, dict]:
        revision, manifest = self._alternatives()
        item = manifest["alternatives"]["photo_upscale_4x"]
        snapshot = self._alternative_files(revision, "intel-sisr-1032", item["artifacts"])
        weight = next(x for x in item["artifacts"] if x["file"].endswith(".bin"))
        identity = VerifiedModelIdentity(item["source"]["repo_id"], item["source"]["revision"], item["source"]["license"].lower(), Path(weight["file"]).name, weight["bytes"], weight["sha256"])
        adapter = IntelSISR1032VerifiedAdapter(snapshot / "single-image-super-resolution-1032.xml", snapshot / "single-image-super-resolution-1032.bin", identity)
        return adapter, {"identity": asdict(identity), "private_cache": {"repo_id": PRIVATE_REPO, "revision": revision, "path": f"{ALT_CACHE_PREFIX}/intel-sisr-1032", "read_only": True}, "perpetual_use_gate": item["perpetual_use_gate"]}
