import json
from pathlib import Path

import pytest

from media_ai.external_media_assets import (
    BlenderCameraAdapter,
    BlenderRenderRequest,
    ComfyUIWanAdapter,
    file_sha256,
    load_asset_registry,
)


ROOT = Path(__file__).resolve().parents[1]


def test_owned_registry_is_complete_and_fail_closed():
    assets = load_asset_registry(ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    assert {"external.blender.runtime", "external.ffmpeg.runtime", "external.comfyui.runtime", "external.wan22.ti2v-5b", "external.ltx.desktop"} <= set(assets)
    assert assets["external.ffmpeg.runtime"].enabled is True
    assert all(not assets[name].enabled for name in ("external.blender.runtime", "external.comfyui.runtime", "external.wan22.ti2v-5b", "external.ltx.desktop"))


def test_registry_rejects_enabled_unverified_asset(tmp_path):
    registry = {"schema_version": 1, "assets": [{
        "asset_id": "bad", "kind": "model", "state": "SOURCE_APPROVED_PENDING_MATERIALIZATION",
        "source_url": "https://example.invalid", "upstream_revision": "abc", "license_id": "Apache-2.0",
        "license_url": "https://example.invalid/license", "enabled": True
    }]}
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match="unverified asset"):
        load_asset_registry(path)


def test_blender_command_uses_only_owned_driver_and_structured_request(tmp_path):
    blend = tmp_path / "resort.blend"
    blend.write_bytes(b"BLENDER-fixture")
    driver = ROOT / "external_assets/media-production/blender/media_ai_blender_camera_render.py"
    adapter = BlenderCameraAdapter(tmp_path / "blender.exe", driver, file_sha256(driver), tmp_path / "job")
    request_path = tmp_path / "job/request.json"
    receipt_path = tmp_path / "job/receipt.json"
    command = adapter.build_command(BlenderRenderRequest(blend, "Camera_Main", tmp_path / "job/frames", 1, 48), request_path, receipt_path)
    assert command[1:5] == ["--background", str(blend), "--python", str(driver)]
    assert "--python-expr" not in command
    payload = json.loads(request_path.read_text(encoding="utf-8"))
    assert payload["camera"] == "Camera_Main"
    assert payload["blend_file_sha256"] == file_sha256(blend)


def test_blender_job_artifacts_cannot_escape_owned_root(tmp_path):
    blend = tmp_path / "resort.blend"
    blend.write_bytes(b"BLENDER-fixture")
    driver = ROOT / "external_assets/media-production/blender/media_ai_blender_camera_render.py"
    adapter = BlenderCameraAdapter(tmp_path / "blender.exe", driver, file_sha256(driver), tmp_path / "owned")
    with pytest.raises(ValueError, match="owned job root"):
        adapter.build_command(BlenderRenderRequest(blend, "Camera", tmp_path / "outside", 1, 2), tmp_path / "owned/request.json", tmp_path / "owned/receipt.json")


def _workflow(tmp_path):
    path = tmp_path / "wan_api.json"
    path.write_text(json.dumps({"6": {"class_type": "CLIPTextEncode", "inputs": {"text": "original", "clip": ["1", 0]}}, "9": {"class_type": "SaveAnimatedWEBP", "inputs": {"filename_prefix": "MINDLE"}}}), encoding="utf-8")
    return path


def test_comfyui_is_loopback_hash_pinned_and_override_allowlisted(tmp_path):
    workflow = _workflow(tmp_path)
    calls = []
    def transport(method, path, payload):
        calls.append((method, path, payload))
        return {"prompt_id": "job_123"}
    adapter = ComfyUIWanAdapter("http://127.0.0.1:8188", workflow, file_sha256(workflow), {("6", "text")}, True, transport)
    prompt_id = adapter.submit({("6", "text"): "한국 건축 리조트"}, "client-1")
    assert prompt_id == "job_123"
    assert calls[0][2]["prompt"]["6"]["inputs"]["text"] == "한국 건축 리조트"
    with pytest.raises(ValueError, match="not allowlisted"):
        adapter.render_workflow({("9", "filename_prefix"): "escape"})
    with pytest.raises(ValueError, match="loopback"):
        ComfyUIWanAdapter("http://192.168.0.5:8188", workflow, file_sha256(workflow), set(), True, transport)


def test_comfyui_global_interrupt_requires_isolated_owned_process(tmp_path):
    workflow = _workflow(tmp_path)
    transport = lambda method, path, payload: {"prompt_id": "owned_1"}
    shared = ComfyUIWanAdapter("http://127.0.0.1:8188", workflow, file_sha256(workflow), {("6", "text")}, False, transport)
    prompt_id = shared.submit({("6", "text"): "test"}, "client")
    with pytest.raises(PermissionError, match="isolated"):
        shared.interrupt(prompt_id)
    isolated = ComfyUIWanAdapter("http://127.0.0.1:8189", workflow, file_sha256(workflow), set(), True, transport)
    with pytest.raises(PermissionError, match="not owned"):
        isolated.interrupt(prompt_id)


def test_comfyui_output_cannot_escape_owned_root(tmp_path):
    root = tmp_path / "output"
    root.mkdir()
    good = root / "clip.mp4"
    good.write_bytes(b"video")
    assert ComfyUIWanAdapter.resolve_output(root, "clip.mp4") == good
    outside = tmp_path / "secret.mp4"
    outside.write_bytes(b"secret")
    with pytest.raises(ValueError, match="outside"):
        ComfyUIWanAdapter.resolve_output(root, "../secret.mp4")
