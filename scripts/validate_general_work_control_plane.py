#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261008-GENERAL-WORK-FINAL-SELF-AUDIT-R1"
PC_EPOCH="MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-PACKAGE-R1"
PASS="PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK"

current=(ROOT/"CURRENT_GENERAL_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_GENERAL_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))

def fail(msg):
    print("GENERAL_WORK_HANDOFF_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
    raise SystemExit(2)

if lock.get("epoch") != EPOCH or state.get("control_plane_epoch") != EPOCH:
    fail("General Work epoch mismatch")
if lock.get("status") != "COMPLETE_HANDOFF_TO_PC_WORK":
    fail("General Work lock must be complete")
if state.get("status") != "COMPLETE_HANDOFF_TO_PC_WORK":
    fail("General Work state must be complete")
if lock.get("final_result") != PASS or state.get("final_result") != PASS:
    fail("General Work final PASS missing")
if lock.get("final_head") != "9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb":
    fail("General Work final HEAD mismatch")
if state.get("pc_work_allowed") is not True:
    fail("PC Work must be unblocked")
if worker.get("active_control_plane_epoch") != PC_EPOCH:
    fail("PC Work must be the active worker epoch")
for token in (PASS,"9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb",PC_EPOCH):
    if token not in current:
        fail(f"CURRENT missing {token!r}")

print("GENERAL_WORK_COMPLETE_HANDOFF_TO_PC_WORK")
print(f"GENERAL_EPOCH={EPOCH}")
print(f"PC_EPOCH={PC_EPOCH}")
