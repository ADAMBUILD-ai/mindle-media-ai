"""Input measurement tests only; synthetic fixtures are not owner acceptance."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare_intake", ROOT / "scripts/prepare_media_production_intake.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


@pytest.fixture(scope="module")
def assets(tmp_path_factory):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("FFmpeg/FFprobe required for input measurement test")
    folder = tmp_path_factory.mktemp("synthetic-intake-not-owner-assets")
    video, audio = folder / "fixture.mp4", folder / "fixture.wav"
    subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "color=c=gray:s=96x54:r=24:d=30",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video)], check=True, timeout=30)
    subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=30", str(audio)], check=True, timeout=30)
    # Rights/origin declarations below belong to a contract test, never real assets.
    rights = {"rights_status": "CONFIRMED", "source_or_owner": "CONTRACT_TEST_ONLY",
              "license_or_permission": "TEST_FIXTURE_ONLY_NOT_PRODUCTION", "rights_evidence": "test fixture declaration"}
    request = {"narration_script": "실제 제작이 아닌 접수 계약시험입니다.", "voice_length_policy": "reject",
               "volumes": {"narration": .8, "original": 0, "bgm": .1},
               "clips": [{"path": str(video), "label": "합성 시험 입력", "origin": "real_capture", **rights}],
               "bgm": {"path": str(audio), "label": "시험 톤", **rights}}
    return request


def run(tmp_path, request):
    path = tmp_path / "input.json"
    path.write_text(json.dumps(request, ensure_ascii=False))
    out = tmp_path / "new-intake"
    return m.prepare(path, out), out


def test_measurement_same_authoritative_validator_and_preserved_inputs(tmp_path, assets):
    request = copy.deepcopy(assets)
    before = {x["path"]: m.sha(x["path"]) for x in [*request["clips"], request["bgm"]]}
    result, out = run(tmp_path, request)
    assert result["status"] == "PASS_INTAKE_TECHNICAL_ONLY"
    manifest = json.loads((out / "INPUT_MANIFEST.json").read_text())
    assert manifest["narration_script"] == request["narration_script"] and manifest["volumes"] == request["volumes"]
    assert manifest["clips"][0]["width"] == 96 and manifest["clips"][0]["height"] == 54
    assert all(m.sha(path) == digest for path, digest in before.items())
    assert json.loads((out / "INTAKE_RESULT.json").read_text()) == json.loads((out / "ASSET_INTAKE.json").read_text())
    assert result["approval_granted"] is result["production_started"] is result["full_product_pass"] is False


def test_empty_template_reports_all_missing_without_inventing_values(tmp_path):
    template = json.loads((ROOT / "docs/handoff/media-production-closeout-r3-20261026/OPERATOR_INPUT.template.json").read_text())
    result, out = run(tmp_path, template)
    assert result["status"] == "BLOCKED_ASSET_INTAKE" and len(result["errors"]) >= 8
    manifest = json.loads((out / "INPUT_MANIFEST.json").read_text())
    assert manifest["narration_script"] is None and manifest["volumes"]["narration"] is None


@pytest.mark.parametrize("field,wrong", [("sha256", "0" * 64), ("bytes", 1), ("duration_seconds", 29), ("width", 100)])
def test_declared_expectations_are_not_silently_repaired(tmp_path, assets, field, wrong):
    request = copy.deepcopy(assets)
    request["clips"][0][field] = wrong
    result, out = run(tmp_path, request)
    assert result["status"] == "BLOCKED_ASSET_INTAKE"
    assert json.loads((out / "INPUT_MANIFEST.json").read_text())["clips"][0][field] == wrong


def test_rights_and_missing_file_remain_blocked(tmp_path, assets):
    request = copy.deepcopy(assets)
    request["clips"][0]["rights_status"] = "PENDING"
    request["bgm"]["path"] = str(tmp_path / "missing.wav")
    result, _ = run(tmp_path, request)
    assert result["status"] == "BLOCKED_ASSET_INTAKE"
    assert any("permission" in x for x in result["errors"]) and any("file" in x for x in result["errors"])


def test_existing_output_directory_never_overwritten(tmp_path, assets):
    request_path = tmp_path / "input.json"
    request_path.write_text(json.dumps(assets))
    out = tmp_path / "existing"
    out.mkdir()
    original = out / "INPUT_MANIFEST.json"
    original.write_bytes(b"preserve owner manifest")
    with pytest.raises(ValueError, match="NEW_OUTPUT_DIRECTORY_REQUIRED"):
        m.prepare(request_path, out)
    assert original.read_bytes() == b"preserve owner manifest"


def test_null_label_does_not_become_literal_none_and_pass(tmp_path, assets):
    request = copy.deepcopy(assets)
    request["clips"][0]["label"] = None
    result, out = run(tmp_path, request)
    assert result["status"] == "BLOCKED_ASSET_INTAKE"
    assert json.loads((out / "INTAKE_RESULT.json").read_text())["status"] == "BLOCKED_ASSET_INTAKE"
    assert json.loads((out / "OPERATOR_INPUT_SNAPSHOT.json").read_text())["clips"][0]["label"] is None


@pytest.mark.parametrize("patch", [{"aspect": "9:16"}, {"duration_seconds": 60}, {"require_rights_evidence": False}, {"surprise_operation": "generate"}])
def test_conflicting_delivery_contract_is_not_auto_fixed(tmp_path, assets, patch):
    request = copy.deepcopy(assets)
    request.update(patch)
    path = tmp_path / "input.json"
    path.write_text(json.dumps(request))
    with pytest.raises(ValueError):
        m.prepare(path, tmp_path / "must-not-be-created")
    assert not (tmp_path / "must-not-be-created").exists()
