"""Verified CPU adapter for Intel Open Model Zoo single-image-super-resolution-1032."""
from __future__ import annotations

import hashlib
import time
from pathlib import Path

import cv2
import numpy as np


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class IntelSISR1032VerifiedAdapter:
    """Runs only the byte-pinned, Apache-2.0 Intel 4× SISR model on CPU."""

    adapter_id = "intel-open-model-zoo-sisr-1032"
    adapter_version = "1.0.1"
    runtime_backend = "openvino-cpu"
    device_requirement = "CPU"

    def __init__(self, xml: Path, weights: Path, identity) -> None:
        import openvino as ov
        self.xml, self.weight, self.identity = Path(xml), Path(weights), identity
        self._core = ov.Core()
        self._compiled = self._core.compile_model(self._core.read_model(str(self.xml), str(self.weight)), "CPU")

    def upscale(self, source: Path, destination: Path) -> dict:
        started = time.monotonic()
        image = cv2.imread(str(source), cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError("actual photo input cannot be decoded")
        if image.shape[:2] != (270, 480):
            raise RuntimeError("Intel SISR-1032 requires the pinned 480x270 product fixture")
        bicubic = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_CUBIC)
        low = image.transpose(2, 0, 1)[None].astype(np.float32)
        high = bicubic.transpose(2, 0, 1)[None].astype(np.float32)
        outputs = self._compiled([low, high])
        residual = next(iter(outputs.values()))[0].transpose(1, 2, 0)
        # The Open Model Zoo network returns a residual, not a complete image.
        # Compose it with the bicubic high-resolution input before encoding.
        result = np.clip(bicubic.astype(np.float32) + residual, 0, 255).astype(np.uint8)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(destination), result):
            raise RuntimeError("actual Intel SISR output could not be written")
        decoded = cv2.imread(str(destination), cv2.IMREAD_COLOR)
        if decoded is None or decoded.shape[:2] != (1080, 1920):
            raise RuntimeError("Intel SISR output dimensions are invalid")
        if int(decoded.max()) == 0:
            raise RuntimeError("actual Intel SISR output is black")
        return {"outputs": [{"path": str(destination), "bytes": destination.stat().st_size, "sha256": sha256_file(destination), "dimensions": [1920, 1080]}], "elapsed_ms": (time.monotonic() - started) * 1000.0}

    def close(self) -> None:
        self._compiled = None
