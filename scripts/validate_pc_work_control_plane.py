#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261007-EMPLOYEE-PACKAGE-FINAL-CLOSEOUT-R2"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_DIRECTIVE_v1.0_20261007.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_EVIDENCE_CONTRACT_v1.0_20261007.json"

current=(ROOT/"CURRENT_PC_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))

def fail(msg):
    print("CONTROL_PLANE_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
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

for token in (EPOCH,DIRECTIVE,CONTRACT):
    if token not in current:
        fail(f"CURRENT missing {token!r}")

if state.get("package_build_allowed") is not True:
    fail("package_build_allowed must be true")

print("CONTROL_PLANE_PASS")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"CONTRACT={CONTRACT}")
