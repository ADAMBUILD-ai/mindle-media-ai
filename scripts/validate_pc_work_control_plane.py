#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261008-PC-WORK-REMOTE-WINDOWS-FALLBACK-R1"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_REMOTE_WINDOWS_FALLBACK_AND_LOCAL_ACCEPTANCE_DIRECTIVE_v1.0_20261008.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_REMOTE_WINDOWS_FALLBACK_EVIDENCE_CONTRACT_v1.0_20261008.json"

current=(ROOT/"CURRENT_PC_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))
general=json.loads((ROOT/"CURRENT_GENERAL_WORK_STATE.json").read_text(encoding="utf-8"))

def fail(msg):
    print("PC_WORK_CONTROL_PLANE_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
    raise SystemExit(2)

checks=[
 ("lock epoch",lock.get("epoch"),EPOCH),
 ("state epoch",state.get("control_plane_epoch"),EPOCH),
 ("worker epoch",worker.get("active_control_plane_epoch"),EPOCH),
 ("lock directive",lock.get("active_directive"),DIRECTIVE),
 ("state directive",state.get("active_directive"),DIRECTIVE),
 ("lock contract",lock.get("evidence_contract"),CONTRACT),
 ("state contract",state.get("evidence_contract"),CONTRACT),
]
for label,actual,expected in checks:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, got {actual!r}")

if general.get("final_result") != "PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK":
    fail("General Work PASS missing")
if state.get("work_must_continue") is not True:
    fail("work_must_continue must be true")
if state.get("execution_mode") != "REMOTE_WINDOWS_FALLBACK":
    fail("execution_mode must be REMOTE_WINDOWS_FALLBACK")
if state.get("package_build_allowed") is not True:
    fail("remote package build must be allowed")
if state.get("package_build_location") != "GITHUB_WINDOWS_RUNNER":
    fail("package build location must be GitHub Windows Runner")
if state.get("local_physical_acceptance_allowed") is not False:
    fail("local physical acceptance must remain pending while helper is blocked")
if state.get("external_marketing_avora_required") is not False:
    fail("external integration must remain deferred")
if state.get("employee_manual_install_steps_allowed") is not False:
    fail("manual employee setup must remain forbidden")
if worker.get("pr23_hold_do_not_merge") is not True:
    fail("PR #23 must remain HOLD / DO NOT MERGE")

for token in (
 EPOCH,DIRECTIVE,CONTRACT,
 "PC_EXECUTION_ENVIRONMENT_STILL_BLOCKED_SETUP_REFRESH",
 "REMOTE_WINDOWS_FALLBACK",
 "PASS_REMOTE_WINDOWS_ONE_CLICK_BUILD_AND_AUTOMATION_READY_LOCAL_ACCEPTANCE_PENDING",
 "PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E"
):
    if token not in current:
        fail(f"CURRENT missing {token!r}")

print("PC_WORK_REMOTE_WINDOWS_FALLBACK_PASS")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"CONTRACT={CONTRACT}")
print("LOCAL_HELPER=BLOCKED_SETUP_REFRESH")
print("REMOTE_WORK=CONTINUE")
