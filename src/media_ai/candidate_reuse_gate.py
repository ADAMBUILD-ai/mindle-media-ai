"""Fail-closed TEST R2 reuse and future rebuild authorization policy."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .external_media_assets import file_sha256


CONTROL_FILES = (
    "CURRENT_PC_WORK_STATE.json",
    "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json",
    "CURRENT_GENERAL_WORK_STATE.json",
    "CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json",
)


@dataclass(frozen=True)
class CandidateReuseDecision:
    status: str
    candidate: dict[str, Any]
    reasons: tuple[str, ...]
    stages: dict[str, int]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def validate_test_r2_reuse(root: Path, require_closed_gate: bool = True) -> CandidateReuseDecision:
    root = root.resolve()
    policy = _load(root / "docs/commander/MINDLE_MEDIA_AI_TEST_R2_REUSE_AND_REBUILD_GATE_20261024.json")
    contract = _load(root / "docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json")
    authorization = _load(root / "docs/commander/WINDOWS_AI_CANDIDATE_20261024_AUTHORIZATION.json")
    delivery = _load(root / "docs/evidence/windows-ai-candidate-20261024-r1/FINAL_DELIVERY.json")
    candidate = policy["candidate"]
    mapping = {
        "source": contract["source"], "producer_run": contract["producer_run"],
        "readback_run": contract["readback_run"], "zip_sha256": contract["zip_sha256"],
        "manifest_sha256": contract["manifest_sha256"], "exe_sha256": contract["exe_sha256"],
        "runtime_id": contract["runtime_id"],
    }
    for field, expected in mapping.items():
        if candidate.get(field) != expected:
            raise ValueError(f"TEST R2 policy/contract mismatch: {field}")
    delivery_mapping = {
        "source": delivery["source"], "zip_bytes": delivery["bytes"],
        "zip_sha256": delivery["sha256"], "manifest_sha256": delivery["manifest_sha256"],
        "exe_sha256": delivery["exe_sha256"], "installer_sha256": delivery["installer"]["sha256"],
    }
    for field, expected in delivery_mapping.items():
        if candidate.get(field) != expected:
            raise ValueError(f"TEST R2 policy/delivery mismatch: {field}")
    consumed = policy["consumed_authorization"]
    if consumed["id"] != authorization["id"] or consumed["authorized_parent"] != authorization["authorized_parent"]:
        raise ValueError("consumed approval identity mismatch")
    if consumed["attempts_allowed"] != authorization["attempts_allowed"] or consumed["attempts_allowed"] != 1:
        raise ValueError("single-attempt authorization mismatch")
    if authorization["global_package_build_allowed"] is not False or consumed["package_build_allowed"] is not False:
        raise ValueError("consumed candidate gate must remain closed")
    stages = {"producer": candidate["producer_run"], "readback": candidate["readback_run"], "transport": candidate["transport_run"]}
    if len(set(stages.values())) != 3:
        raise ValueError("producer, readback, and transport runs must remain distinct")
    for relative, expected in policy["workflow_sha256"].items():
        if file_sha256(root / relative) != expected:
            raise ValueError(f"candidate workflow identity changed without duplicate-build evidence: {relative}")
    for relative in CONTROL_FILES:
        control = _load(root / relative)
        owner = control.get("owner_windows_candidate_20261024", {})
        if require_closed_gate and control.get("package_build_allowed") is not False:
            raise ValueError(f"repeat build gate is open: {relative}")
        checks = {
            "authorization": consumed["id"], "authorized_parent": consumed["authorized_parent"],
            "source": candidate["source"], "run": candidate["producer_run"],
            "archive_sha256": candidate["zip_sha256"], "manifest_sha256": candidate["manifest_sha256"],
            "exe_sha256": candidate["exe_sha256"], "runtime_id": candidate["runtime_id"],
            "readback_run": candidate["readback_run"], "transport_run": candidate["transport_run"],
        }
        for field, expected in checks.items():
            if owner.get(field) != expected:
                raise ValueError(f"TEST R2 control identity mismatch: {relative}:{field}")
        if control.get("candidate_attempt_run") != candidate["producer_run"] or control.get("candidate_attempt_source") != candidate["source"]:
            raise ValueError(f"single attempt identity mismatch: {relative}")
    return CandidateReuseDecision(
        "REUSE_TEST_R2",
        candidate,
        ("package_build_allowed=false", "authorized attempt consumed", "office PC acceptance remains pending"),
        stages,
    )


def evaluate_rebuild_request(root: Path, request: dict[str, Any]) -> CandidateReuseDecision:
    current = validate_test_r2_reuse(root, require_closed_gate=False)
    required = {"approval_id", "authorized_parent", "attempts_allowed", "changed_files", "unresolved_by_test_r2", "package_build_allowed"}
    missing = sorted(required - set(request))
    if missing:
        return CandidateReuseDecision("REBUILD_REJECTED_INCOMPLETE_REQUEST", current.candidate, tuple(missing), current.stages)
    if request["package_build_allowed"] is not True:
        return CandidateReuseDecision("REBUILD_REJECTED_GATE_FALSE", current.candidate, ("request package_build_allowed is not true",), current.stages)
    controls = [_load(root.resolve() / path) for path in CONTROL_FILES]
    if any(control.get("package_build_allowed") is not True for control in controls):
        return CandidateReuseDecision("REBUILD_REJECTED_GATE_FALSE", current.candidate, ("repository control planes remain false",), current.stages)
    consumed_id = _load(root.resolve() / "docs/commander/MINDLE_MEDIA_AI_TEST_R2_REUSE_AND_REBUILD_GATE_20261024.json")["consumed_authorization"]["id"]
    if not isinstance(request["approval_id"], str) or not request["approval_id"].strip() or request["approval_id"] == consumed_id:
        return CandidateReuseDecision("REBUILD_REJECTED_CONSUMED_APPROVAL", current.candidate, ("new approval_id required",), current.stages)
    if request["attempts_allowed"] != 1 or not re.fullmatch(r"[0-9a-f]{40}", str(request["authorized_parent"])):
        return CandidateReuseDecision("REBUILD_REJECTED_INVALID_AUTHORIZATION", current.candidate, ("one attempt and exact parent SHA required",), current.stages)
    changed = request["changed_files"]
    reasons = request["unresolved_by_test_r2"]
    if not isinstance(changed, list) or not changed or not isinstance(reasons, dict) or any(not reasons.get(path) for path in changed):
        return CandidateReuseDecision("REBUILD_REJECTED_MISSING_SCOPE", current.candidate, ("every changed file needs a TEST R2 insufficiency reason",), current.stages)
    if any(not isinstance(path,str) or Path(path).is_absolute() or ".." in Path(path).parts or not (root.resolve()/path).is_file() for path in changed):
        return CandidateReuseDecision("REBUILD_REJECTED_MISSING_SCOPE", current.candidate, ("changed_files must be existing repository files",), current.stages)
    return CandidateReuseDecision("REBUILD_AUTHORIZATION_CONTRACT_COMPLETE", current.candidate, (), current.stages)
