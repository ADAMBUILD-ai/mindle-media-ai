"""Fail-closed CPU Adapter for the pinned Qualcomm Real-ESRGAN x4plus ONNX model."""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class RealESRGANIdentity:
    repo_id: str
    revision: str
    license: str
    archive_name: str
    archive_size_bytes: int
    archive_sha256: str
    onnx_name: str
    onnx_size_bytes: int
    onnx_sha256: str
    data_name: str
    data_size_bytes: int
    data_sha256: str

    def verify(self, archive: Path, onnx: Path, data: Path) -> None:
        expected = (
            (archive, self.archive_name, self.archive_size_bytes, self.archive_sha256),
            (onnx, self.onnx_name, self.onnx_size_bytes, self.onnx_sha256),
            (data, self.data_name, self.data_size_bytes, self.data_sha256),
        )
        for path, name, size, digest in expected:
            path = Path(path)
            if not path.is_file() or path.name != name:
                raise ValueError(f"verified RealESRGAN artifact is unavailable: {name}")
            if path.stat().st_size != size:
                raise ValueError(f"verified RealESRGAN byte count changed: {name}")
            if sha256_file(path) != digest:
                raise ValueError(f"verified RealESRGAN SHA-256 changed: {name}")


class RealESRGANX4PlusVerifiedAdapter:
    adapter_id = "mindle.realesrgan-x4plus.verified.onnx.cpu"
    adapter_version = "1.0.0"
    runtime_backend = "onnxruntime"
    device_requirement = "cpu"
    scale = 4

    def __init__(self, archive: Path, onnx: Path, data: Path, identity: RealESRGANIdentity) -> None:
        import onnxruntime as ort

        identity.verify(archive, onnx, data)
        self.archive = Path(archive)
        self.onnx = Path(onnx)
        self.data = Path(data)
        self.identity = identity
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(
            str(self.onnx), sess_options=options, providers=["CPUExecutionProvider"]
        )
        self.providers = self.session.get_providers()
        if self.providers != ["CPUExecutionProvider"]:
            raise RuntimeError(f"CPU-only provider enforcement failed: {self.providers}")
        inputs = self.session.get_inputs()
        outputs = self.session.get_outputs()
        if len(inputs) != 1 or len(outputs) < 1:
            raise RuntimeError("unexpected RealESRGAN ONNX input/output signature")
        self.input_name = inputs[0].name
        self.output_name = outputs[0].name
        self.input_shape = list(inputs[0].shape)
        self.output_shape = list(outputs[0].shape)

    def upscale(self, input_path: Path, output_path: Path) -> dict:
        import numpy as np
        from PIL import Image

        input_path = Path(input_path)
        output_path = Path(output_path)
        if not input_path.is_file() or input_path.stat().st_size == 0:
            raise RuntimeError("RealESRGAN photo input is unavailable")
        input_sha_before = sha256_file(input_path)
        with Image.open(input_path) as source:
            source.load()
            input_format = source.format
            input_mode = source.mode
            input_size = source.size
            rgb = source.convert("RGB")
        if input_size[0] <= 0 or input_size[1] <= 0 or max(input_size) > 512:
            raise RuntimeError(f"input dimensions are outside the validated CPU envelope: {input_size}")
        tensor = np.asarray(rgb, dtype=np.float32).transpose(2, 0, 1)[None] / 255.0
        started = time.perf_counter()
        result = self.session.run([self.output_name], {self.input_name: tensor})[0]
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        if result.ndim != 4 or result.shape[0] != 1 or result.shape[1] != 3:
            raise RuntimeError(f"unexpected RealESRGAN output tensor: {result.shape}")
        expected_size = (input_size[0] * self.scale, input_size[1] * self.scale)
        actual_size = (int(result.shape[3]), int(result.shape[2]))
        if actual_size != expected_size:
            raise RuntimeError(f"invalid RealESRGAN scale: expected {expected_size}, got {actual_size}")
        pixels = np.clip(result[0].transpose(1, 2, 0) * 255.0, 0, 255).round().astype(np.uint8)
        if int(pixels.max()) <= int(pixels.min()) or float(pixels.std()) < 1.0:
            raise RuntimeError("RealESRGAN produced a blank or degenerate image")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(pixels, mode="RGB").save(output_path, format="PNG")
        with Image.open(output_path) as check:
            check.verify()
        with Image.open(output_path) as check:
            check.load()
            reopened_size = check.size
            reopened_mode = check.mode
            reopened_format = check.format
        if reopened_size != expected_size or reopened_mode != "RGB" or reopened_format != "PNG":
            raise RuntimeError("RealESRGAN output reopen validation failed")
        input_sha_after = sha256_file(input_path)
        if input_sha_after != input_sha_before:
            raise RuntimeError("RealESRGAN input was modified during inference")
        return {
            "status": "TESTED_PASS",
            "input": {
                "file_name": input_path.name,
                "bytes": input_path.stat().st_size,
                "sha256": input_sha_before,
                "format": input_format,
                "mode": input_mode,
                "width": input_size[0],
                "height": input_size[1],
                "unchanged_after_inference": True,
            },
            "output": {
                "file_name": output_path.name,
                "path": str(output_path),
                "bytes": output_path.stat().st_size,
                "sha256": sha256_file(output_path),
                "format": reopened_format,
                "mode": reopened_mode,
                "width": reopened_size[0],
                "height": reopened_size[1],
                "reopen_validated": True,
                "pixel_min": int(pixels.min()),
                "pixel_max": int(pixels.max()),
                "pixel_stddev": round(float(pixels.std()), 6),
            },
            "scale_factor": self.scale,
            "elapsed_ms": elapsed_ms,
            "runtime": {
                "backend": self.runtime_backend,
                "providers": self.providers,
                "input_name": self.input_name,
                "output_name": self.output_name,
                "declared_input_shape": self.input_shape,
                "declared_output_shape": self.output_shape,
                "actual_input_tensor_shape": list(tensor.shape),
                "actual_output_tensor_shape": list(result.shape),
            },
        }

