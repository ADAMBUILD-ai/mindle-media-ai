"""Contracts that connect owned scene assets to the existing MEDIA MP4 lane."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path
import subprocess
from typing import Any
from uuid import UUID

from .external_media_assets import ExternalAsset, file_sha256


class ProductionStatus(StrEnum):
    READY = "READY"
    BLOCKED_INPUT = "BLOCKED_INPUT"
    BLOCKED_ASSET = "BLOCKED_ASSET"


@dataclass(frozen=True)
class ArchitectureScene:
    scene_id: str
    engine: str
    source: Path
    duration_seconds: float
    source_sha256: str
    prompt: str | None = None
    camera: str | None = None


@dataclass(frozen=True)
class ArchitectureVideoPlan:
    project_id: str
    aspect: str
    scenes: tuple[ArchitectureScene, ...]
    output: Path


@dataclass(frozen=True)
class ProductionPreflight:
    status: ProductionStatus
    missing: tuple[str, ...]
    required_assets: tuple[str, ...]


ENGINE_ASSETS = {
    "existing_clip": ("external.ffmpeg.runtime",),
    "blender": ("mindle.blender.camera-render-driver.v1", "external.blender.runtime", "external.ffmpeg.runtime"),
    "wan22": ("external.comfyui.runtime", "external.wan22.ti2v-5b", "external.ffmpeg.runtime"),
}


def validate_production_plan(plan: ArchitectureVideoPlan, owned_root: Path) -> ArchitectureVideoPlan:
    UUID(plan.project_id)
    if plan.aspect not in {"original", "16:9", "9:16"}:
        raise ValueError("production aspect must be original, 16:9, or 9:16")
    if not 1 <= len(plan.scenes) <= 12:
        raise ValueError("an architecture production requires 1 to 12 scenes")
    root = owned_root.resolve()
    if not plan.output.resolve().is_relative_to(root) or plan.output.suffix.lower() != ".mp4":
        raise ValueError("production output must be an MP4 inside the owned root")
    seen: set[str] = set()
    for scene in plan.scenes:
        if scene.scene_id in seen or not scene.scene_id or len(scene.scene_id) > 64:
            raise ValueError("scene IDs must be unique and bounded")
        seen.add(scene.scene_id)
        if scene.engine not in ENGINE_ASSETS:
            raise ValueError(f"unsupported scene engine: {scene.engine}")
        if not scene.source.is_file():
            raise ValueError(f"scene source is unavailable: {scene.scene_id}")
        if len(scene.source_sha256) != 64 or file_sha256(scene.source) != scene.source_sha256:
            raise ValueError(f"scene source identity mismatch: {scene.scene_id}")
        if not 0.25 <= float(scene.duration_seconds) <= 30:
            raise ValueError("each scene duration must be between 0.25 and 30 seconds")
        if scene.prompt is not None and (not scene.prompt.strip() or len(scene.prompt) > 2000):
            raise ValueError("generation prompt must contain 1 to 2000 characters")
        if scene.engine == "blender":
            if scene.source.suffix.lower() != ".blend" or not scene.camera:
                raise ValueError("Blender scenes require a .blend source and existing camera name")
        elif scene.engine == "wan22":
            if scene.source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} or not scene.prompt:
                raise ValueError("Wan scenes require a reference image and prompt")
        elif scene.source.suffix.lower() not in {".mp4", ".mov", ".mkv", ".webm"}:
            raise ValueError("existing scenes require a supported video clip")
    return plan


def preflight_production(plan: ArchitectureVideoPlan, registry: dict[str, ExternalAsset], owned_root: Path) -> ProductionPreflight:
    try:
        validate_production_plan(plan, owned_root)
    except ValueError as error:
        return ProductionPreflight(ProductionStatus.BLOCKED_INPUT, (str(error),), ())
    required = tuple(dict.fromkeys(asset for scene in plan.scenes for asset in ENGINE_ASSETS[scene.engine]))
    missing = tuple(asset for asset in required if asset not in registry or not registry[asset].enabled)
    if missing:
        return ProductionPreflight(ProductionStatus.BLOCKED_ASSET, missing, required)
    return ProductionPreflight(ProductionStatus.READY, (), required)


class FFmpegDeliveryAdapter:
    """Produces a browser/player compatible MP4 without shell interpretation."""

    def __init__(self, ffmpeg: Path, ffprobe: Path, owned_root: Path,
                 ffmpeg_sha256: str, ffprobe_sha256: str) -> None:
        self.ffmpeg = ffmpeg.resolve()
        self.ffprobe = ffprobe.resolve()
        self.owned_root = owned_root.resolve()
        for path, expected in ((self.ffmpeg, ffmpeg_sha256), (self.ffprobe, ffprobe_sha256)):
            if not path.is_file() or file_sha256(path) != expected:
                raise ValueError("FFmpeg program identity mismatch")

    def probe(self, path: Path) -> dict[str, Any]:
        return json.loads(subprocess.check_output([
            str(self.ffprobe), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
        ], text=True, timeout=30))

    def finalize(self, source: Path, output: Path, timeout: int = 600) -> dict[str, Any]:
        source = source.resolve()
        output = output.resolve()
        if any(not path.is_relative_to(self.owned_root) for path in (source, output)):
            raise ValueError("FFmpeg source and output must stay inside the owned root")
        if not source.is_file() or output.suffix.lower() != ".mp4" or source == output:
            raise ValueError("a distinct source and MP4 output are required")
        before = file_sha256(source)
        source_info = self.probe(source)
        if not any(stream.get("codec_type") == "video" for stream in source_info.get("streams", [])):
            raise ValueError("source has no video stream")
        output.parent.mkdir(parents=True, exist_ok=True)
        command = [
            str(self.ffmpeg), "-y", "-i", str(source),
            "-map", "0:v:0", "-map", "0:a:0?",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-movflags", "+faststart", str(output),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"FFmpeg delivery failed: {completed.stderr[-2000:]}")
        if file_sha256(source) != before:
            output.unlink(missing_ok=True)
            raise ValueError("source changed during FFmpeg delivery")
        info = self.probe(output)
        video = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
        audio = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
        content = output.read_bytes()
        moov, mdat = content.find(b"moov"), content.find(b"mdat")
        if not video or video.get("codec_name") != "h264" or video.get("pix_fmt") != "yuv420p":
            raise ValueError("delivery MP4 is not H.264/yuv420p")
        if audio and audio.get("codec_name") != "aac":
            raise ValueError("delivery MP4 audio is not AAC")
        if moov < 0 or mdat < 0 or moov > mdat:
            raise ValueError("delivery MP4 is not faststart")
        return {
            "status": "TESTED_PASS",
            "model_inference": False,
            "source_sha256": before,
            "output": {"path": str(output), "bytes": len(content), "sha256": file_sha256(output)},
            "runtime": {
                "ffmpeg_sha256": file_sha256(self.ffmpeg),
                "ffprobe_sha256": file_sha256(self.ffprobe),
                "video_codec": video["codec_name"],
                "pixel_format": video["pix_fmt"],
                "audio_codec": audio["codec_name"] if audio else None,
                "duration_seconds": float(info["format"]["duration"]),
                "faststart": True,
            },
        }
