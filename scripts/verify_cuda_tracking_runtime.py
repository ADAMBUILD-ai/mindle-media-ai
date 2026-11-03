"""Fail-closed preflight for the CUDA SAM 2.1 product tracking path.

This is deliberately an inspection-only tool: it never invokes pip, downloads
models, starts inference, or modifies a recovered model package.  It creates
one receipt only after checking the interpreter, CUDA runtime and the complete
three-model product vault that ProductJobService requires.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_commit(source: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


class PreflightBlocked(RuntimeError):
    def __init__(self, reason: str, receipt: dict) -> None:
        super().__init__(reason)
        self.receipt = receipt


def block(reason: str, receipt: dict) -> None:
    receipt.update(status="TRACKING_RUNTIME_BLOCKED", reason=reason)
    raise PreflightBlocked(reason, receipt)


def inspect(runtime_root: Path, source: Path) -> dict:
    receipt = {
        "schema_version": "MEDIA_SAM21_CUDA_RUNTIME_PREFLIGHT_V1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "NOT_STARTED",
        "source": {"path": str(source), "commit": source_commit(source)},
        "runtime": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
            "runtime_root": str(runtime_root),
        },
        "models": {"status": "NOT_CHECKED"},
        "inference_started": False,
    }
    if sys.version_info[:2] != (3, 11):
        block("TRACKING_RUNTIME_BLOCKED: Python 3.11 is required", receipt)
    if not runtime_root.is_dir():
        block("TRACKING_RUNTIME_BLOCKED: recovered runtime root is unavailable", receipt)
    source_package = source / "src"
    if not (source_package / "media_ai").is_dir():
        block("TRACKING_RUNTIME_BLOCKED: source media_ai package is unavailable", receipt)
    if str(source_package) not in sys.path:
        sys.path.insert(0, str(source_package))
    try:
        import cv2
        import torch
        import torchvision
        import transformers
    except ImportError as error:
        block(f"TRACKING_RUNTIME_BLOCKED: required CUDA dependency is missing: {error.name}", receipt)
    receipt["runtime"].update(
        torch_version=str(torch.__version__),
        torchvision_version=str(torchvision.__version__),
        transformers_version=str(transformers.__version__),
        opencv_version=str(cv2.__version__),
        cuda_available=bool(torch.cuda.is_available()),
        cuda_runtime=str(torch.version.cuda),
    )
    if not torch.cuda.is_available() or not torch.version.cuda:
        block("TRACKING_RUNTIME_BLOCKED: CUDA PyTorch runtime is required; CPU tracking is forbidden", receipt)
    properties = torch.cuda.get_device_properties(0)
    receipt["runtime"].update(
        cuda_device="cuda:0",
        gpu_name=properties.name,
        vram_total_bytes=int(properties.total_memory),
    )
    existing = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT")
    if existing and Path(existing).resolve() != runtime_root.resolve():
        block("TRACKING_RUNTIME_BLOCKED: environment runtime root differs from requested root", receipt)
    os.environ["MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT"] = str(runtime_root)
    try:
        from media_ai.product_runtime import ProductModelVault
        vault = ProductModelVault(source / ".runtime-preflight", token="")
        vault.verify_local_models()
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        block(f"TRACKING_RUNTIME_BLOCKED: complete immutable model vault verification failed: {error}", receipt)
    receipt["models"] = {
        "status": "VERIFIED_READ_ONLY",
        "required": ["SAM 2.1", "Whisper-small", "Intel SISR 1032"],
    }
    receipt["status"] = "TRACKING_RUNTIME_READY_NO_INFERENCE"
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit("refusing to overwrite an existing preflight receipt")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = inspect(args.runtime_root.resolve(), args.source.resolve())
    except PreflightBlocked as error:
        receipt = error.receipt
        receipt["status"] = "TRACKING_RUNTIME_BLOCKED"
        receipt.setdefault("reason", str(error))
        args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 3
    except RuntimeError as error:
        receipt = {
            "schema_version": "MEDIA_SAM21_CUDA_RUNTIME_PREFLIGHT_V1",
            "status": "TRACKING_RUNTIME_BLOCKED",
            "reason": str(error),
            "inference_started": False,
        }
        args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 3
    args.out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
