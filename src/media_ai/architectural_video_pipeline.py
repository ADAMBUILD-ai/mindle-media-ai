"""Contracts that connect owned scene assets to the existing MEDIA MP4 lane."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path
import sqlite3
import subprocess
import threading
import time
from typing import Any
from uuid import UUID, uuid4

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
        return self._validate_receipt(output, ((source, before),), 1)

    def assemble_existing_clips(self, scenes: tuple[ArchitectureScene, ...], output: Path,
                                aspect: str, width: int, height: int, timeout: int = 900) -> dict[str, Any]:
        if not 1 <= len(scenes) <= 12 or any(scene.engine != "existing_clip" for scene in scenes):
            raise ValueError("assembly accepts 1 to 12 existing clips")
        if not (64 <= width <= 3840 and 64 <= height <= 3840 and width % 2 == height % 2 == 0):
            raise ValueError("assembly resolution must use bounded even dimensions")
        if aspect == "16:9" and width * 9 != height * 16:
            raise ValueError("16:9 output dimensions do not match")
        if aspect == "9:16" and width * 16 != height * 9:
            raise ValueError("9:16 output dimensions do not match")
        if aspect not in {"original", "16:9", "9:16"}:
            raise ValueError("unsupported assembly aspect")
        output = output.resolve()
        if not output.is_relative_to(self.owned_root) or output.suffix.lower() != ".mp4":
            raise ValueError("assembly output must stay inside the owned root")
        command = [str(self.ffmpeg), "-y"]
        filters, concat_inputs, hashes = [], [], []
        for index, scene in enumerate(scenes):
            source = scene.source.resolve()
            if not source.is_relative_to(self.owned_root) or not source.is_file():
                raise ValueError("assembly source must stay inside the owned root")
            if source == output:
                raise ValueError("assembly output must differ from every scene source")
            actual_hash = file_sha256(source)
            if actual_hash != scene.source_sha256:
                raise ValueError(f"scene source identity mismatch: {scene.scene_id}")
            info = self.probe(source)
            if not any(stream.get("codec_type") == "video" for stream in info.get("streams", [])):
                raise ValueError(f"scene has no video stream: {scene.scene_id}")
            hashes.append((source, actual_hash))
            command += ["-i", str(source)]
            duration = float(scene.duration_seconds)
            filters.append(
                f"[{index}:v:0]fps=24,scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=30,trim=duration={duration},setpts=PTS-STARTPTS[v{index}]"
            )
            if any(stream.get("codec_type") == "audio" for stream in info["streams"]):
                filters.append(f"[{index}:a:0]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad,atrim=duration={duration},asetpts=PTS-STARTPTS[a{index}]")
            else:
                filters.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={duration},asetpts=PTS-STARTPTS[a{index}]")
            concat_inputs.extend((f"[v{index}]", f"[a{index}]"))
        filters.append("".join(concat_inputs) + f"concat=n={len(scenes)}:v=1:a=1[vout][aout]")
        output.parent.mkdir(parents=True, exist_ok=True)
        command += [
            "-filter_complex", ";".join(filters), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-movflags", "+faststart", str(output),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"FFmpeg scene assembly failed: {completed.stderr[-2000:]}")
        if any(file_sha256(path) != digest for path, digest in hashes):
            output.unlink(missing_ok=True)
            raise ValueError("a scene source changed during assembly")
        receipt = self._validate_receipt(output, hashes, len(scenes))
        expected_duration = sum(float(scene.duration_seconds) for scene in scenes)
        if abs(receipt["runtime"]["duration_seconds"] - expected_duration) > 0.15:
            raise ValueError("assembled duration differs from the scene plan")
        receipt["scene_order"] = [scene.scene_id for scene in scenes]
        receipt["aspect"] = aspect
        receipt["resolution"] = {"width": width, "height": height}
        return receipt

    def _validate_receipt(self, output: Path, source_hashes: tuple[tuple[Path, str], ...] | list[tuple[Path, str]], scene_count: int) -> dict[str, Any]:
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
            "source_sha256": source_hashes[0][1] if len(source_hashes) == 1 else None,
            "scene_source_sha256s": [digest for _path, digest in source_hashes],
            "scene_count": scene_count,
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


class ArchitectureProductionLedger:
    """Persistent state ledger; engine execution remains in an owned worker."""

    ACTIVE = {"QUEUED", "RUNNING", "CANCEL_REQUESTED"}
    TERMINAL = {"SUCCEEDED", "FAILED", "CANCELLED", "INTERRUPTED", "BLOCKED_INPUT", "BLOCKED_ASSET"}

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(self.root / "architecture-productions.sqlite3", check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("CREATE TABLE IF NOT EXISTS productions (id TEXT PRIMARY KEY, request_key TEXT UNIQUE, fingerprint TEXT, state TEXT, body TEXT, updated REAL)")
        rows = self.db.execute("SELECT id, body FROM productions WHERE state IN ('RUNNING','CANCEL_REQUESTED')").fetchall()
        for identifier, raw in rows:
            value = json.loads(raw)
            value.update(state="INTERRUPTED", error="서버 중단. 외부 엔진 결과를 재검증한 뒤 새 작업으로 실행해야 합니다.", updated_at=time.time())
            self._put(value)

    @staticmethod
    def _plan_value(plan: ArchitectureVideoPlan) -> dict[str, Any]:
        return {
            "project_id": plan.project_id, "aspect": plan.aspect, "output": str(plan.output.resolve()),
            "scenes": [{
                "scene_id": scene.scene_id, "engine": scene.engine, "source": str(scene.source.resolve()),
                "source_sha256": scene.source_sha256, "duration_seconds": scene.duration_seconds,
                "prompt": scene.prompt, "camera": scene.camera,
            } for scene in plan.scenes],
        }

    def submit(self, request_key: str, plan: ArchitectureVideoPlan, preflight: ProductionPreflight) -> dict[str, Any]:
        if not request_key or len(request_key) > 128:
            raise ValueError("a bounded request key is required")
        plan_value = self._plan_value(plan)
        fingerprint = file_sha256_bytes(json.dumps(plan_value, sort_keys=True, ensure_ascii=False).encode())
        with self.lock:
            row = self.db.execute("SELECT fingerprint, body FROM productions WHERE request_key=?", (request_key,)).fetchone()
            if row:
                if row[0] != fingerprint:
                    raise ValueError("the request key already identifies another production")
                return json.loads(row[1])
            state = "QUEUED" if preflight.status is ProductionStatus.READY else preflight.status.value
            value = {
                "production_id": str(uuid4()), "request_key": request_key, "fingerprint": fingerprint,
                "state": state, "plan": plan_value, "required_assets": list(preflight.required_assets),
                "missing": list(preflight.missing), "created_at": time.time(), "updated_at": time.time(),
            }
            self.db.execute("INSERT INTO productions VALUES(?,?,?,?,?,?)", (value["production_id"], request_key, fingerprint, state, json.dumps(value, ensure_ascii=False), value["updated_at"]))
            self.db.commit()
            return value

    def get(self, identifier: str) -> dict[str, Any]:
        with self.lock:
            row = self.db.execute("SELECT body FROM productions WHERE id=?", (str(UUID(identifier)),)).fetchone()
            if not row:
                raise ValueError("architecture production was not found")
            return json.loads(row[0])

    def start(self, identifier: str) -> dict[str, Any]:
        with self.lock:
            value = self.get(identifier)
            if value["state"] != "QUEUED":
                raise ValueError("only a queued production can start")
            value.update(state="RUNNING", started_at=time.time())
            self._put(value)
            return value

    def cancel(self, identifier: str) -> dict[str, Any]:
        with self.lock:
            value = self.get(identifier)
            if value["state"] == "QUEUED":
                value["state"] = "CANCELLED"
            elif value["state"] == "RUNNING":
                value["state"] = "CANCEL_REQUESTED"
            elif value["state"] not in self.TERMINAL:
                raise ValueError("production cannot be cancelled from its current state")
            self._put(value)
            return value

    def complete(self, identifier: str, receipt: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            value = self.get(identifier)
            if value["state"] != "RUNNING":
                raise ValueError("only a running production can complete")
            output = Path(value["plan"]["output"]).resolve()
            recorded = receipt.get("output", {})
            if receipt.get("status") != "TESTED_PASS" or Path(recorded.get("path", "")).resolve() != output:
                raise ValueError("delivery receipt does not match the production output")
            if not output.is_file() or recorded.get("sha256") != file_sha256(output) or recorded.get("bytes") != output.stat().st_size:
                raise ValueError("delivery output identity mismatch")
            value.update(state="SUCCEEDED", receipt=receipt, finished_at=time.time())
            self._put(value)
            return value

    def _put(self, value: dict[str, Any]) -> None:
        with self.lock:
            value["updated_at"] = time.time()
            self.db.execute("UPDATE productions SET state=?, body=?, updated=? WHERE id=?", (value["state"], json.dumps(value, ensure_ascii=False), value["updated_at"], value["production_id"]))
            self.db.commit()

    def close(self) -> None:
        with self.lock:
            self.db.close()


def file_sha256_bytes(content: bytes) -> str:
    from hashlib import sha256
    return sha256(content).hexdigest()
