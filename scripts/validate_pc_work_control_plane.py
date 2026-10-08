#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
PC_EPOCH="MEDIA-AI-20261008-PC-WORK-PAUSED-PENDING-GENERAL-AUDIT-R1"
GENERAL_EPOCH="MEDIA-AI-20261008-GENERAL-WORK-FINAL-SELF-AUDIT-R1"
GENERAL_DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_DIRECTIVE_v1.0_20261008.md"

current=(ROOT/"CURRENT_PC_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))

def fail(msg):
    print("PC_WORK_CONTROL_PLANE_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
    raise SystemExit(2)

if lock.get("epoch") != PC_EPOCH:
    fail("PC pause epoch mismatch")
if state.get("control_plane_epoch") != PC_EPOCH:
    fail("PC state epoch mismatch")
if worker.get("active_control_plane_epoch") != GENERAL_EPOCH:
    fail("General Work must be active while PC Work is paused")
if lock.get("status") != "PAUSED_WAITING_GENERAL_WORK_PASS":
    fail("PC lock must remain paused")
if state.get("status") != "PAUSED_WAITING_GENERAL_WORK_PASS":
    fail("PC state must remain paused")
if state.get("package_build_allowed") is not False:
    fail("package_build_allowed must be false")
if state.get("product_changes_allowed") is not False:
    fail("PC product changes must be false while paused")
for token in (PC_EPOCH,GENERAL_EPOCH,GENERAL_DIRECTIVE,"ONE-CLICK RUNTIME PACKAGE"):
    if token not in current:
        fail(f"CURRENT missing {token!r}")
if worker.get("pr23_hold_do_not_merge") is not True:
    fail("PR #23 must remain HOLD / DO NOT MERGE")

print("PC_WORK_PAUSED_WAITING_GENERAL_WORK_PASS")
print(f"PC_EPOCH={PC_EPOCH}")
print(f"ACTIVE_GENERAL_EPOCH={GENERAL_EPOCH}")
print(f"GENERAL_DIRECTIVE={GENERAL_DIRECTIVE}")
