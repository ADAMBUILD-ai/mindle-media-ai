#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-BLOCKER-RECOVERY-R1"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_DIRECTIVE_v1.0_20261008.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261008.json"
NOTICE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_EXECUTION_ENVIRONMENT_BLOCKED_NOTICE_v1.0_20261008.md"

current=(ROOT/"CURRENT_PC_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))

def fail(msg):
    print("PC_WORK_CONTROL_PLANE_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
    raise SystemExit(2)

if lock.get("epoch") != EPOCH or state.get("control_plane_epoch") != EPOCH or worker.get("active_control_plane_epoch") != EPOCH:
    fail("epoch mismatch")
if lock.get("status") != "BLOCKED_PC_EXECUTION_ENVIRONMENT":
    fail("lock must be blocked on PC execution environment")
if state.get("status") != "BLOCKED_PC_EXECUTION_ENVIRONMENT":
    fail("state must be blocked on PC execution environment")
if lock.get("active_directive") != DIRECTIVE or state.get("active_directive") != DIRECTIVE:
    fail("directive mismatch")
if lock.get("evidence_contract") != CONTRACT or state.get("evidence_contract") != CONTRACT:
    fail("contract mismatch")
if lock.get("block_notice") != NOTICE or state.get("block_notice") != NOTICE:
    fail("block notice mismatch")
if state.get("package_build_allowed") is not False:
    fail("package build must remain disabled while exec tool is blocked")
if state.get("product_changes_allowed") is not False:
    fail("product changes must remain disabled while exec tool is blocked")
if state.get("current_result") != "PC_EXECUTION_ENVIRONMENT_BLOCKED":
    fail("current blocked result missing")
if worker.get("pr23_hold_do_not_merge") is not True:
    fail("PR #23 must remain HOLD / DO NOT MERGE")

for token in (EPOCH,DIRECTIVE,CONTRACT,NOTICE,"PC_EXECUTION_ENVIRONMENT_BLOCKED","helper_unknown_error: setup refresh had errors"):
    if token not in current:
        fail(f"CURRENT missing {token!r}")

print("PC_WORK_EXECUTION_ENVIRONMENT_BLOCKED")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"NOTICE={NOTICE}")
print("RESUME_FIRST_ACTION=run scripts/validate_pc_work_control_plane.py after execution-tool recovery")
