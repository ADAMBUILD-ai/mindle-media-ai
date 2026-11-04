"""Measured visual-risk assessment for locally supplied video inputs.

This is an admission signal, not an AI restoration claim.  It never alters the
source and never substitutes a synthetic frame for the original architecture.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

from .verified_model_adapters import sha256_file


def _ffprobe(ffprobe: str, source: Path) -> dict:
    completed = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries",
         "stream=codec_name,width,height,avg_frame_rate,bit_rate:format=bit_rate,duration,size",
         "-of", "json", str(source)],
        check=True, capture_output=True, text=True, timeout=30,
    )
    return json.loads(completed.stdout)


def _rate(value: str | None) -> float:
    try:
        left, right = str(value or "").split("/", 1)
        return float(left) / float(right) if float(right) else 0.0
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def _block_grid_risk(frame: np.ndarray) -> float:
    """Measure grid-edge discontinuities; a risk signal, never a quality verdict."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    boundary, neighbours = [], []
    for axis in (0, 1):
        pixels = gray if axis == 0 else gray.T
        for grid in (8, 16):
            if pixels.shape[1] <= grid + 1:
                continue
            boundary.append(np.abs(pixels[:, grid::grid] - pixels[:, grid - 1::grid]).mean())
            neighbours.append(np.abs(pixels[:, grid - 1::grid] - pixels[:, grid - 2::grid]).mean())
    if not boundary:
        return 0.0
    return max(0.0, float(np.mean(boundary) - np.mean(neighbours)))


def assess_video_input(source: Path, evidence_path: Path, ffprobe: str) -> dict:
    """Write immutable visual-risk evidence before model work begins."""
    source = Path(source)
    probe = _ffprobe(ffprobe, source)
    video = next((item for item in probe.get("streams", []) if item.get("width") and item.get("height")), None)
    if not video:
        raise RuntimeError("INPUT_QUALITY_BLOCKED: a decodable video stream is required")
    width, height = int(video["width"]), int(video["height"])
    fps = _rate(video.get("avg_frame_rate"))
    if fps <= 0:
        raise RuntimeError("INPUT_QUALITY_BLOCKED: video frame rate is unavailable")
    bitrate = int(video.get("bit_rate") or probe.get("format", {}).get("bit_rate") or 0)
    bits_per_pixel_frame = bitrate / float(width * height * fps) if bitrate else None

    capture = cv2.VideoCapture(str(source))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    indexes = sorted(set(np.linspace(0, max(0, frame_count - 1), num=min(5, max(1, frame_count)), dtype=int).tolist()))
    block_risks, sharpness = [], []
    for index in indexes:
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(index))
        ok, frame = capture.read()
        if not ok:
            continue
        block_risks.append(_block_grid_risk(frame))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sharpness.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))
    capture.release()
    if not block_risks:
        raise RuntimeError("INPUT_QUALITY_BLOCKED: representative video frames could not be decoded")

    signals = []
    if bits_per_pixel_frame is not None and bits_per_pixel_frame < 0.055:
        signals.append("LOW_BITS_PER_PIXEL_PER_FRAME")
    if float(np.mean(block_risks)) > 1.5:
        signals.append("COMPRESSION_GRID_DISCONTINUITY")
    status = "INPUT_QUALITY_REVIEW_REQUIRED" if signals else "INPUT_QUALITY_MEASURED_REVIEW_REQUIRED"
    receipt = {
        "schema_version": "MEDIA_VIDEO_INPUT_QUALITY_V1",
        "status": status,
        "source": {"path": str(source), "sha256": sha256_file(source), "bytes": source.stat().st_size},
        "video": {"codec": video.get("codec_name"), "width": width, "height": height,
                  "fps": fps, "bitrate_bits_per_second": bitrate,
                  "bits_per_pixel_per_frame": bits_per_pixel_frame, "frame_count": frame_count},
        "measurements": {"sampled_frame_indexes": indexes,
                         "mean_grid_discontinuity": float(np.mean(block_risks)),
                         "mean_laplacian_variance": float(np.mean(sharpness))},
        "risk_signals": signals,
        "promotion_eligible_without_restoration": False,
        "human_visual_review_required": True,
        "note": "Measured compression risk is not a claim that AI restoration recovered lost architectural detail.",
    }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt
