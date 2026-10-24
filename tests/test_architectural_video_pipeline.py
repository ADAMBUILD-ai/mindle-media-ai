import json
from pathlib import Path
import shutil
import subprocess
from uuid import uuid4

import pytest

from media_ai.architectural_video_pipeline import (
    ArchitectureScene,
    ArchitectureProductionLedger,
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


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="local FFmpeg tools unavailable")
def test_real_two_scene_assembly_preserves_order_and_supplies_silent_audio(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    first, second = owned / "first.mkv", owned / "second.mp4"
    subprocess.run([
        shutil.which("ffmpeg"), "-y", "-f", "lavfi", "-i", "color=c=blue:size=320x180:rate=24",
        "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=44100", "-t", "0.5",
        "-c:v", "mpeg4", "-c:a", "pcm_s16le", str(first),
    ], check=True, capture_output=True, timeout=30)
    subprocess.run([
        shutil.which("ffmpeg"), "-y", "-f", "lavfi", "-i", "color=c=red:size=180x320:rate=24",
        "-t", "0.5", "-c:v", "mpeg4", str(second),
    ], check=True, capture_output=True, timeout=30)
    scenes = (
        ArchitectureScene("arrival", "existing_clip", first, .5, file_sha256(first)),
        ArchitectureScene("villa", "existing_clip", second, .5, file_sha256(second)),
    )
    ffmpeg, ffprobe = Path(shutil.which("ffmpeg")), Path(shutil.which("ffprobe"))
    adapter = FFmpegDeliveryAdapter(ffmpeg, ffprobe, owned, file_sha256(ffmpeg), file_sha256(ffprobe))
    output = owned / "assembled.mp4"
    receipt = adapter.assemble_existing_clips(scenes, output, "16:9", 320, 180, timeout=60)
    assert receipt["scene_order"] == ["arrival", "villa"]
    assert receipt["scene_count"] == 2
    assert receipt["runtime"]["audio_codec"] == "aac"
    assert receipt["runtime"]["duration_seconds"] == pytest.approx(1, abs=.15)
    import cv2
    capture = cv2.VideoCapture(str(output))
    capture.set(cv2.CAP_PROP_POS_MSEC, 250)
    ok_first, frame_first = capture.read()
    capture.set(cv2.CAP_PROP_POS_MSEC, 750)
    ok_second, frame_second = capture.read()
    capture.release()
    assert ok_first and ok_second
    assert frame_first[:, :, 0].mean() > frame_first[:, :, 2].mean()
    assert frame_second[:, :, 2].mean() > frame_second[:, :, 0].mean()
    plan = ArchitectureVideoPlan(str(uuid4()), "16:9", scenes, output)
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    ledger = ArchitectureProductionLedger(tmp_path / "ledger-success")
    task = ledger.submit("two-scene", plan, preflight_production(plan, registry, owned))
    ledger.start(task["production_id"])
    assert ledger.complete(task["production_id"], receipt)["state"] == "SUCCEEDED"
    ledger.close()


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="local FFmpeg tools unavailable")
def test_measured_scene_range_uses_selected_source_window(tmp_path):
    owned=tmp_path/"owned";owned.mkdir();source=owned/"two-colors.mp4"
    subprocess.run([shutil.which("ffmpeg"),"-v","error","-y","-f","lavfi","-i","color=c=blue:s=160x90:r=20:d=0.5",
                    "-f","lavfi","-i","color=c=red:s=160x90:r=20:d=0.5","-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[v]",
                    "-map","[v]","-c:v","libx264","-pix_fmt","yuv420p",str(source)],check=True,timeout=30)
    scene=ArchitectureScene("selected-red","existing_clip",source,.4,file_sha256(source),start_seconds=.55)
    ffmpeg,ffprobe=Path(shutil.which("ffmpeg")),Path(shutil.which("ffprobe"));output=owned/"selected.mp4"
    receipt=FFmpegDeliveryAdapter(ffmpeg,ffprobe,owned,file_sha256(ffmpeg),file_sha256(ffprobe)).assemble_existing_clips(
        (scene,),output,"16:9",160,90,timeout=30)
    import cv2
    capture=cv2.VideoCapture(str(output));ok,frame=capture.read();capture.release()
    assert ok and frame[:,:,2].mean()>frame[:,:,0].mean()
    assert receipt["scene_ranges"]==[{"scene_id":"selected-red","start_seconds":.55,"duration_seconds":.4}]


def test_production_ledger_is_idempotent_and_recovers_running_as_interrupted(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    clip = owned / "clip.mp4"
    clip.write_bytes(b"fixture")
    plan = _plan(tmp_path, "existing_clip", clip)
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    preflight = preflight_production(plan, registry, owned)
    ledger = ArchitectureProductionLedger(tmp_path / "ledger")
    first = ledger.submit("request-1", plan, preflight)
    assert ledger.submit("request-1", plan, preflight)["production_id"] == first["production_id"]
    ledger.start(first["production_id"])
    ledger.close()
    recovered = ArchitectureProductionLedger(tmp_path / "ledger")
    assert recovered.get(first["production_id"])["state"] == "INTERRUPTED"
    recovered.close()


def test_production_ledger_does_not_publish_cancelled_or_mismatched_output(tmp_path):
    owned = tmp_path / "owned"
    owned.mkdir()
    clip = owned / "clip.mp4"
    clip.write_bytes(b"fixture")
    plan = _plan(tmp_path, "existing_clip", clip)
    registry = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    ledger = ArchitectureProductionLedger(tmp_path / "ledger")
    queued = ledger.submit("cancel-me", plan, preflight_production(plan, registry, owned))
    assert ledger.cancel(queued["production_id"])["state"] == "CANCELLED"
    with pytest.raises(ValueError, match="only a running"):
        ledger.complete(queued["production_id"], {"status": "TESTED_PASS", "output": {}})
    ledger.close()
