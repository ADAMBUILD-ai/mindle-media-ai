"""Verify the locally retained LaMa ONNX weight without Hub access."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image


ROOT = Path(__file__).parents[1]
MODEL = ROOT / "model_scout" / "artifacts" / "lama" / "inpainting_lama_2025jan.onnx"
INPUT = ROOT / "model_scout" / "artifacts" / "lama" / "input.png"
MASK = ROOT / "model_scout" / "artifacts" / "lama" / "mask.png"
OUTPUT = ROOT / "evidence" / "model_scout" / "lama_local_offline_output.png"
RESULT = ROOT / "evidence" / "model_scout" / "HF_MODEL_RUNTIME_RESULTS.json"
EXPECTED_MODEL_SHA256 = "7df918ac3921d3daf0aae1d219776cf0dc4e4935f035af81841b40adcf74fdf2"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if sha256(MODEL) != EXPECTED_MODEL_SHA256:
        raise SystemExit("local LaMa weight hash does not match the pinned historical evidence")
    image = Image.open(INPUT).convert("RGB")
    mask = Image.open(MASK).convert("L")
    image_tensor = np.asarray(image, dtype=np.float32).transpose(2, 0, 1)[None] / 127.5 - 1.0
    mask_tensor = np.asarray(mask, dtype=np.float32)[None, None] / 255.0
    session = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    started = time.perf_counter()
    result = session.run(None, {"image": image_tensor, "mask": mask_tensor})[0]
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    Image.fromarray(np.clip((result[0].transpose(1, 2, 0) + 1) * 127.5, 0, 255).astype(np.uint8)).save(OUTPUT)
    evidence = json.loads(RESULT.read_text(encoding="utf-8"))
    evidence["local_lama_offline_smoke"] = {
        "status": "TECHNICAL_SMOKE_PASS",
        "repo_id": "opencv/inpainting_lama",
        "revision": "aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f",
        "weight_path": str(MODEL.relative_to(ROOT)).replace("\\", "/"),
        "weight_sha256": sha256(MODEL),
        "input_sha256": sha256(INPUT),
        "mask_sha256": sha256(MASK),
        "output_path": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "output_sha256": sha256(OUTPUT),
        "duration_ms": duration_ms,
        "runtime": {"onnxruntime": ort.__version__, "provider": "CPUExecutionProvider"},
        "quality_gate": "VERIFY_REQUIRED: technical smoke does not replace real-photo review or remote provenance verification.",
    }
    RESULT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence["local_lama_offline_smoke"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
