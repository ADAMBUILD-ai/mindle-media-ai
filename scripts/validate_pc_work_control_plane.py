#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-BLOCKER-RECOVERY-R1"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_DIRECTIVE_v1.0_20261008.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261008.json"
GENERAL_PASS="PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK"

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

if general.get("final_result") != GENERAL_PASS:
    fail("General Work PASS missing")
if general.get("final_head") != "9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb":
    fail("General Work final HEAD mismatch")
if state.get("package_build_allowed") is not True:
    fail("package_build_allowed must be true")
if state.get("system32_dll_copy_allowed") is not False:
    fail("System32 DLL copy must remain forbidden")
if state.get("old_unresolved_gpl_ffmpeg_final_candidate_allowed") is not False:
    fail("unresolved old GPL FFmpeg candidate cannot be final")
if state.get("external_marketing_avora_required") is not False:
    fail("external Marketing/AVORA must remain deferred")
if state.get("normal_employee_action") != "DOUBLE_CLICK_ONLY":
    fail("normal employee action must be DOUBLE_CLICK_ONLY")
if worker.get("pr23_hold_do_not_merge") is not True:
    fail("PR #23 must remain HOLD / DO NOT MERGE")

for token in (EPOCH,DIRECTIVE,CONTRACT,"dbc57ebbc6a576b4f5c1089f12797812f538afa3","PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E"):
    if token not in current:
        fail(f"CURRENT missing {token!r}")

print("PC_WORK_CONTROL_PLANE_PASS")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"CONTRACT={CONTRACT}")
print("GENERAL_WORK_BASELINE=9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb")
print("PC_PREFLIGHT_BASELINE=dbc57ebbc6a576b4f5c1089f12797812f538afa3")
