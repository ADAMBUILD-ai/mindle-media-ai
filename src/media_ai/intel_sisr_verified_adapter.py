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
    adapter_version = "1.1.0"
    runtime_backend = "openvino-cpu"
    device_requirement = "CPU"

    def __init__(self, xml: Path, weights: Path, identity) -> None:
        import openvino as ov
        self.xml, self.weight, self.identity = Path(xml), Path(weights), identity
        self._core = ov.Core()
        self._compiled = self._core.compile_model(self._core.read_model(str(self.xml), str(self.weight)), "CPU")

    def upscale(self, source: Path, destination: Path) -> dict:
        started = time.monotonic()
        raw = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
        image = None if raw is None else cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR) if raw.ndim == 2 else raw[:, :, :3]
        alpha = raw[:, :, 3] if raw is not None and raw.ndim == 3 and raw.shape[2] == 4 else None
        if image is None:
            raise RuntimeError("actual photo input cannot be decoded")
        height, width = image.shape[:2]
        if height * width > 8_000_000:
            raise RuntimeError('CPU 4배 해상도 향상은 최대 800만 화소 사진을 지원합니다.')
        def infer(tile):
            bicubic = cv2.resize(tile, (1920, 1080), interpolation=cv2.INTER_CUBIC)
            low = tile.transpose(2, 0, 1)[None].astype(np.float32)
            high = bicubic.transpose(2, 0, 1)[None].astype(np.float32)
            residual = next(iter(self._compiled([low, high]).values()))[0].transpose(1, 2, 0)
            return np.clip(bicubic.astype(np.float32) + residual, 0, 255).astype(np.uint8)
        tiles = 1
        if (height, width) == (270, 480):
            result = infer(image)
        else:
            # Keep each model input shape pinned; crop context from results rather
            # than stretching arbitrary photos into the model's fixed canvas.
            margin, core_w, core_h = 32, 416, 206
            padded = cv2.copyMakeBorder(image, margin, 270, margin, 480, cv2.BORDER_REPLICATE)
            result = np.empty((height * 4, width * 4, 3), dtype=np.uint8)
            tiles = 0
            for y in range(0, height, core_h):
                for x in range(0, width, core_w):
                    tile = infer(padded[y:y + 270, x:x + 480])
                    valid_w, valid_h = min(core_w, width-x), min(core_h, height-y)
                    result[y*4:(y+valid_h)*4, x*4:(x+valid_w)*4] = tile[margin*4:(margin+valid_h)*4, margin*4:(margin+valid_w)*4]
                    tiles += 1
        destination.parent.mkdir(parents=True, exist_ok=True)
        if alpha is not None:
            result = np.dstack((result, cv2.resize(alpha, (width * 4, height * 4), interpolation=cv2.INTER_LINEAR)))
        if not cv2.imwrite(str(destination), result):
            raise RuntimeError("actual Intel SISR output could not be written")
        decoded = cv2.imread(str(destination), cv2.IMREAD_COLOR)
        if decoded is None or decoded.shape[:2] != (height * 4, width * 4):
            raise RuntimeError("Intel SISR output dimensions are invalid")
        if int(decoded.max()) == 0:
            raise RuntimeError("actual Intel SISR output is black")
        return {"outputs": [{"path": str(destination), "bytes": destination.stat().st_size, "sha256": sha256_file(destination), "dimensions": [width * 4, height * 4]}], "tiles": tiles, "scale": 4, "elapsed_ms": (time.monotonic() - started) * 1000.0}

    def close(self) -> None:
        self._compiled = None
