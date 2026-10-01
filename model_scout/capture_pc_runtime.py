"""Capture the local runtime evidence without enabling unapproved adapters."""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def command_result(command: list[str]) -> dict[str, object]:
    executable = shutil.which(command[0])
    if executable is None:
        return {"available": False, "command": command, "reason": "not_on_path"}
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "available": completed.returncode == 0,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def module_result(module: str, expression: str) -> dict[str, object]:
    return command_result([sys.executable, "-c", f"import {module}; print({expression})"])


def capture() -> dict[str, object]:
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "ffmpeg": command_result(["ffmpeg", "-version"]),
        "nvidia_smi": command_result(["nvidia-smi"]),
        "opencv": module_result("cv2", "cv2.__version__"),
        "torch": module_result("torch", "{'version': torch.__version__, 'cuda_available': torch.cuda.is_available()}"),
        "onnxruntime": module_result("onnxruntime", "{'version': onnxruntime.__version__, 'providers': onnxruntime.get_available_providers()}"),
        "adapter_activation": "NOT_ATTEMPTED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(capture(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
