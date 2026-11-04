import json
from pathlib import Path
import shutil

import pytest

from media_ai.candidate_reuse_gate import evaluate_rebuild_request, validate_test_r2_reuse


ROOT = Path(__file__).resolve().parents[1]


def _copy_gate_fixture(destination):
    relatives = [
        "docs/commander/MINDLE_MEDIA_AI_TEST_R2_REUSE_AND_REBUILD_GATE_20261024.json",
        "docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json",
        "docs/commander/WINDOWS_AI_CANDIDATE_20261024_AUTHORIZATION.json",
        "docs/evidence/windows-ai-candidate-20261024-r1/FINAL_DELIVERY.json",
        "CURRENT_PC_WORK_STATE.json", "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json",
        "CURRENT_GENERAL_WORK_STATE.json", "CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json",
    ]
    sources = [ROOT / relative for relative in relatives]
    sources.extend((ROOT / ".github/workflows").glob("windows-ai-candidate*20261024.yml"))
    for source in sources:
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def test_current_test_r2_identity_remains_valid_as_successor_base():
    decision = validate_test_r2_reuse(ROOT,require_closed_gate=False)
    assert decision.status == "REUSE_TEST_R2"
    assert decision.candidate["source"] == "2e5e9197d78c9b975686c1e419d2b68ce5f65226"
    assert len(set(decision.stages.values())) == 3


def test_tampered_candidate_hash_is_rejected(tmp_path):
    copied = tmp_path / "repo"
    _copy_gate_fixture(copied)
    contract = copied / "docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json"
    value = json.loads(contract.read_text(encoding="utf-8")); value["zip_sha256"] = "0" * 64
    contract.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="policy/contract mismatch"):
        validate_test_r2_reuse(copied)


def test_connection_problem_cannot_authorize_rebuild_even_with_open_gate(tmp_path):
    copied = tmp_path / "repo"
    _copy_gate_fixture(copied)
    for name in ("CURRENT_PC_WORK_STATE.json", "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json",
                 "CURRENT_GENERAL_WORK_STATE.json", "CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json"):
        path=copied/name; value=json.loads(path.read_text()); value["package_build_allowed"]=True
        path.write_text(json.dumps(value))
    request = {
        "approval_id": "NEW-APPROVAL", "authorized_parent": "a" * 40, "attempts_allowed": 1,
        "changed_files": ["work-window-connection"],
        "unresolved_by_test_r2": {"work-window-connection": "window disconnected"},
        "package_build_allowed": True,
    }
    decision = evaluate_rebuild_request(copied, request)
    assert decision.status == "REBUILD_REJECTED_MISSING_SCOPE"


def test_consumed_successor_authorization_closes_rebuild_gate():
    request=json.loads((ROOT/"docs/commander/MINDLE_MEDIA_AI_REBUILD_REQUEST_20261024_R3.json").read_text(encoding="utf-8"))
    assert evaluate_rebuild_request(ROOT,request).status=="REBUILD_REJECTED_GATE_FALSE"


def test_incomplete_rebuild_request_is_rejected_before_any_build():
    decision = evaluate_rebuild_request(ROOT, {"approval_id": "x"})
    assert decision.status == "REBUILD_REJECTED_INCOMPLETE_REQUEST"


def test_future_rebuild_contract_requires_all_gates_and_new_approval(tmp_path):
    copied = tmp_path / "repo"
    _copy_gate_fixture(copied)
    for name in (
        "CURRENT_PC_WORK_STATE.json", "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json",
        "CURRENT_GENERAL_WORK_STATE.json", "CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json",
    ):
        path = copied / name
        value = json.loads(path.read_text(encoding="utf-8")); value["package_build_allowed"] = True
        path.write_text(json.dumps(value), encoding="utf-8")
    request = {
        "approval_id": "MEDIA-AI-FUTURE-UNCONSUMED", "authorized_parent": "b" * 40,
        "attempts_allowed": 1, "changed_files": ["src/media_ai/new_feature.py"],
        "unresolved_by_test_r2": {"src/media_ai/new_feature.py": "TEST R2 predates the approved feature"},
        "package_build_allowed": True,
    }
    feature=copied/"src/media_ai/new_feature.py";feature.parent.mkdir(parents=True,exist_ok=True);feature.write_text("# approved fixture\n")
    assert evaluate_rebuild_request(copied, request).status == "REBUILD_AUTHORIZATION_CONTRACT_COMPLETE"
