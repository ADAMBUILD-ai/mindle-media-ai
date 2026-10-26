#!/usr/bin/env python3
"""Create a fixed synthetic local A/V fixture and verify MEDIA MP4 delivery."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from media_ai.architectural_video_pipeline import FFmpegDeliveryAdapter  # noqa: E402
from media_ai.external_media_assets import file_sha256  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    ffmpeg_name = shutil.which("ffmpeg")
    ffprobe_name = shutil.which("ffprobe")
    if not ffmpeg_name or not ffprobe_name:
        raise SystemExit("FFmpeg and FFprobe are required")
    ffmpeg, ffprobe = Path(ffmpeg_name), Path(ffprobe_name)
    folder = args.output_dir.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    source = folder / "SMOKE_SOURCE.mkv"
    output = folder / "SMOKE_DELIVERY.mp4"
    subprocess.run([
        str(ffmpeg), "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100", "-t", "1",
        "-c:v", "mpeg4", "-c:a", "pcm_s16le", str(source),
    ], check=True, capture_output=True, timeout=30)
    adapter = FFmpegDeliveryAdapter(ffmpeg, ffprobe, folder, file_sha256(ffmpeg), file_sha256(ffprobe))
    receipt = adapter.finalize(source, output, timeout=60)
    try:
        receipt["output"]["path"] = output.relative_to(ROOT).as_posix()
    except ValueError:
        receipt["output"]["path"] = output.name
    receipt["scope"] = "LOCAL_SYNTHETIC_AV_SMOKE_NOT_MODEL_INFERENCE_NOT_HUMAN_HEARING"
    receipt["source_generation"] = "FFmpeg lavfi testsrc2 + 440 Hz sine"
    receipt["source_path_preserved"] = False
    source.unlink()
    (folder / "FFMPEG_DELIVERY_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
