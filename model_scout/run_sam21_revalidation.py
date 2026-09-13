"""Pinned SAM 2.1 technical mask smoke in the isolated scout environment."""
import hashlib
import json
import os
import time
from pathlib import Path

import torch
from PIL import Image, ImageDraw
from transformers import AutoModelForMaskGeneration, AutoProcessor

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
ROOT = Path(__file__).parent / "artifacts" / "sam21"
REPO_ID = "facebook/sam2.1-hiera-base-plus"
REVISION = "b7320756a13354e7530a63935656d35b2f91a290"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    input_path, output_path = ROOT / "input.png", ROOT / "mask.png"
    image = Image.new("RGB", (512, 512), (237, 239, 235))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 511, 511), outline=(100, 110, 115), width=6)
    draw.ellipse((145, 130, 365, 375), fill=(35, 105, 175), outline=(20, 50, 90), width=5)
    image.save(input_path)
    processor = AutoProcessor.from_pretrained(REPO_ID, revision=REVISION)
    model = AutoModelForMaskGeneration.from_pretrained(REPO_ID, revision=REVISION).eval()
    inputs = processor(images=image, input_points=[[[[256, 250]]]], return_tensors="pt")
    started = time.perf_counter()
    with torch.no_grad():
        result = model(**inputs)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    index = int(result.iou_scores[0, 0].argmax().item())
    raw = result.pred_masks[0, 0, index][None, None]
    mask = torch.nn.functional.interpolate(raw, size=(512, 512), mode="bilinear", align_corners=False)[0, 0]
    Image.fromarray((mask.detach().cpu().numpy() > 0).astype("uint8") * 255).save(output_path)
    evidence = {
        "status": "TECHNICAL_SMOKE_PASS", "repo_id": REPO_ID, "revision": REVISION,
        "runtime": {"torch": torch.__version__, "transformers": __import__("transformers").__version__, "provider": "CPU"},
        "duration_ms": duration_ms, "input_sha256": sha256(input_path), "mask_sha256": sha256(output_path),
        "raw_mask_shape": list(result.pred_masks.shape), "selected_mask_index": index,
        "quality_gate": "VERIFY_REQUIRED: synthetic prompt mask only; real category benchmark and license review remain required."
    }
    (ROOT / "result.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__": main()
