"""Pinned-weight, isolated CPU revalidation for OpenCV LaMa ONNX."""
import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
from huggingface_hub import HfApi, hf_hub_download
from PIL import Image, ImageDraw

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
ROOT = Path(__file__).parent / "artifacts" / "lama"
REPO_ID = "opencv/inpainting_lama"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    api = HfApi()
    revision = api.model_info(REPO_ID).sha
    model_path = Path(hf_hub_download(REPO_ID, "inpainting_lama_2025jan.onnx", revision=revision, local_dir=ROOT))
    license_path = Path(hf_hub_download(REPO_ID, "LICENSE", revision=revision, local_dir=ROOT))

    input_path, mask_path, output_path = ROOT / "input.png", ROOT / "mask.png", ROOT / "output.png"
    image = Image.new("RGB", (512, 512), (225, 226, 220))
    draw = ImageDraw.Draw(image)
    for x in range(32, 512, 64): draw.line((x, 0, x, 512), fill=(55, 65, 80), width=5)
    for y in range(64, 512, 64): draw.line((0, y, 512, y), fill=(80, 90, 100), width=3)
    draw.rectangle((190, 230, 330, 310), fill=(210, 45, 35))
    mask = Image.new("L", (512, 512), 0)
    ImageDraw.Draw(mask).rectangle((190, 230, 330, 310), fill=255)
    image.save(input_path); mask.save(mask_path)

    image_tensor = np.asarray(image, dtype=np.float32).transpose(2, 0, 1)[None] / 127.5 - 1.0
    mask_tensor = np.asarray(mask, dtype=np.float32)[None, None] / 255.0
    session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
    started = time.perf_counter()
    output = session.run(None, {"image": image_tensor, "mask": mask_tensor})[0]
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    Image.fromarray(np.clip((output[0].transpose(1, 2, 0) + 1) * 127.5, 0, 255).astype(np.uint8)).save(output_path)

    result = {
        "status": "TECHNICAL_SMOKE_PASS",
        "repo_id": REPO_ID,
        "revision": revision,
        "runtime": {"onnxruntime": ort.__version__, "provider": "CPUExecutionProvider"},
        "duration_ms": duration_ms,
        "model_sha256": sha256(model_path),
        "license_sha256": sha256(license_path),
        "input_sha256": sha256(input_path),
        "mask_sha256": sha256(mask_path),
        "output_sha256": sha256(output_path),
        "visual_note": "Synthetic grid reconstruction has localized purple artifacts at the repaired central intersection; it is not a quality approval.",
        "quality_gate": "VERIFY_REQUIRED: synthetic technical smoke only; real architectural photo A/B and human review remain required."
    }
    (ROOT / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
