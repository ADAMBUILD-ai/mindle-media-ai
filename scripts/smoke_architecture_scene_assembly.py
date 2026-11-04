#!/usr/bin/env python3
"""Run a real two-scene MEDIA assembly with mixed audio availability."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from media_ai.architectural_video_pipeline import (  # noqa: E402
    ArchitectureProductionLedger,
    ArchitectureScene,
    ArchitectureVideoPlan,
    FFmpegDeliveryAdapter,
    preflight_production,
)
from media_ai.external_media_assets import file_sha256, load_asset_registry  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    ffmpeg_name, ffprobe_name = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg_name or not ffprobe_name:
        raise SystemExit("FFmpeg and FFprobe are required")
    folder = args.output_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    first, second = folder / "arrival-source.mkv", folder / "villa-source.mp4"
    subprocess.run([
        ffmpeg_name, "-y", "-f", "lavfi", "-i", "color=c=blue:size=320x180:rate=24",
        "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=44100", "-t", "0.5",
        "-c:v", "mpeg4", "-c:a", "pcm_s16le", str(first),
    ], check=True, capture_output=True, timeout=30)
    subprocess.run([
        ffmpeg_name, "-y", "-f", "lavfi", "-i", "color=c=red:size=180x320:rate=24",
        "-t", "0.5", "-c:v", "mpeg4", str(second),
    ], check=True, capture_output=True, timeout=30)
    scenes = (
        ArchitectureScene("arrival", "existing_clip", first, .5, file_sha256(first)),
        ArchitectureScene("villa", "existing_clip", second, .5, file_sha256(second)),
    )
    output = folder / "ARCHITECTURE_TWO_SCENE_SMOKE.mp4"
    ffmpeg, ffprobe = Path(ffmpeg_name), Path(ffprobe_name)
    adapter = FFmpegDeliveryAdapter(ffmpeg, ffprobe, folder, file_sha256(ffmpeg), file_sha256(ffprobe))
    receipt = adapter.assemble_existing_clips(scenes, output, "16:9", 320, 180, timeout=60)
    import cv2
    capture = cv2.VideoCapture(str(output))
    order_probe = []
    for position in (250, 750):
        capture.set(cv2.CAP_PROP_POS_MSEC, position)
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError("assembled frame order probe failed")
        order_probe.append({"position_ms": position, "mean_bgr": [float(frame[:, :, channel].mean()) for channel in range(3)]})
    capture.release()
    if not (order_probe[0]["mean_bgr"][0] > order_probe[0]["mean_bgr"][2]
            and order_probe[1]["mean_bgr"][2] > order_probe[1]["mean_bgr"][0]):
        raise RuntimeError("assembled scene order differs from the plan")
    plan = ArchitectureVideoPlan(str(uuid4()), "16:9", scenes, output)
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    preflight = preflight_production(plan, registry, folder)
    with tempfile.TemporaryDirectory(prefix="mindle-ledger-") as ledger_dir:
        ledger = ArchitectureProductionLedger(Path(ledger_dir))
        task = ledger.submit("owned-two-scene-smoke", plan, preflight)
        ledger.start(task["production_id"])
        task = ledger.complete(task["production_id"], receipt)
        ledger.close()
    for source in (first, second):
        source.unlink()
    for item in task["plan"]["scenes"]:
        item["source"] = Path(item["source"]).name
    task["plan"]["output"] = output.name
    receipt["output"]["path"] = output.name
    result = {
        "scope": "REAL_FFMPEG_TWO_SCENE_ASSEMBLY_NOT_MODEL_INFERENCE_NOT_HUMAN_HEARING",
        "preflight": preflight.status.value,
        "visual_order_probe": order_probe,
        "task": task,
    }
    (folder / "SCENE_ASSEMBLY_RECEIPT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
