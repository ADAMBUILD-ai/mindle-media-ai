import json
from pathlib import Path
import shutil
import subprocess
from uuid import uuid4

import pytest

from media_ai.architectural_video_pipeline import (
    ArchitectureScene,
    ArchitectureVideoPlan,
    FFmpegDeliveryAdapter,
    ProductionStatus,
    preflight_production,
)
from media_ai.external_media_assets import file_sha256, load_asset_registry


ROOT = Path(__file__).resolve().parents[1]


def _plan(tmp_path, engine, source, **scene_options):
    return ArchitectureVideoPlan(str(uuid4()), "16:9", (
        ArchitectureScene("scene-01", engine, source, 2, file_sha256(source), **scene_options),
    ), tmp_path / "owned/final.mp4")


def test_existing_clip_is_ready_but_pending_ai_engines_fail_closed(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    clip = owned / "clip.mp4"
    clip.write_bytes(b"fixture")
    image = owned / "reference.jpg"
    image.write_bytes(b"fixture")
    blend = owned / "resort.blend"
    blend.write_bytes(b"fixture")
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    assert preflight_production(_plan(tmp_path, "existing_clip", clip), registry, owned).status is ProductionStatus.READY
    wan = preflight_production(_plan(tmp_path, "wan22", image, prompt="리조트 외관 항공 이동"), registry, owned)
    assert wan.status is ProductionStatus.BLOCKED_ASSET
    assert set(wan.missing) == {"external.comfyui.runtime", "external.wan22.ti2v-5b"}
    blender = preflight_production(_plan(tmp_path, "blender", blend, camera="Camera_Main"), registry, owned)
    assert blender.status is ProductionStatus.BLOCKED_ASSET


def test_generation_contract_rejects_missing_semantics_and_output_escape(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    image = owned / "reference.jpg"
    image.write_bytes(b"fixture")
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    missing_prompt = _plan(tmp_path, "wan22", image)
    assert preflight_production(missing_prompt, registry, owned).status is ProductionStatus.BLOCKED_INPUT
    escaped = ArchitectureVideoPlan(str(uuid4()), "16:9", (ArchitectureScene("one", "wan22", image, 2, file_sha256(image), prompt="test"),), tmp_path / "outside.mp4")
    assert preflight_production(escaped, registry, owned).status is ProductionStatus.BLOCKED_INPUT
    changed = _plan(tmp_path, "wan22", image, prompt="test")
    image.write_bytes(b"changed")
    assert preflight_production(changed, registry, owned).status is ProductionStatus.BLOCKED_INPUT


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="local FFmpeg tools unavailable")
def test_real_ffmpeg_delivery_has_h264_yuv420p_faststart_and_aac(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    source = owned / "source.mkv"
    subprocess.run([
        shutil.which("ffmpeg"), "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100", "-t", "1",
        "-c:v", "mpeg4", "-c:a", "pcm_s16le", str(source),
    ], check=True, capture_output=True, timeout=30)
    ffmpeg = Path(shutil.which("ffmpeg"))
    ffprobe = Path(shutil.which("ffprobe"))
    adapter = FFmpegDeliveryAdapter(ffmpeg, ffprobe, owned, file_sha256(ffmpeg), file_sha256(ffprobe))
    receipt = adapter.finalize(source, owned / "delivery.mp4", timeout=60)
    assert receipt["status"] == "TESTED_PASS"
    assert receipt["runtime"]["video_codec"] == "h264"
    assert receipt["runtime"]["pixel_format"] == "yuv420p"
    assert receipt["runtime"]["audio_codec"] == "aac"
    assert receipt["runtime"]["faststart"] is True
    assert receipt["source_sha256"] == file_sha256(source)
