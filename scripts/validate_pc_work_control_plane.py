#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_AND_ENVIRONMENT_DIAGNOSTIC_DIRECTIVE_v1.0_20261006.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261006.json"

current=(ROOT/"CURRENT_PC_WORK_DIRECTIVE.md").read_text(encoding="utf-8")
lock=json.loads((ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json").read_text(encoding="utf-8"))
state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text(encoding="utf-8"))
worker=json.loads((ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json").read_text(encoding="utf-8"))

def fail(message):
    print("CONTROL_PLANE_MISMATCH_BLOCKED: "+message, file=sys.stderr)
    raise SystemExit(2)

checks=[
    ("lock epoch", lock.get("epoch"), EPOCH),
    ("state epoch", state.get("control_plane_epoch"), EPOCH),
    ("worker epoch", worker.get("active_control_plane_epoch"), EPOCH),
    ("lock directive", lock.get("active_directive"), DIRECTIVE),
    ("state directive", state.get("active_directive"), DIRECTIVE),
    ("lock contract", lock.get("evidence_contract"), CONTRACT),
    ("state contract", state.get("evidence_contract"), CONTRACT),
]
for label, actual, expected in checks:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, got {actual!r}")

for token in (EPOCH, DIRECTIVE, CONTRACT):
    if token not in current:
        fail("CURRENT missing "+token)

if state.get("active_preflight") is not None:
    fail("stale preflight still active")
if state.get("parent_directive") is not None:
    fail("stale parent directive still active")
if state.get("technical_base_directive") is not None:
    fail("stale technical-base directive still active")
if worker.get("collision_status") != "NO_ACTIVE_COLLISION":
    fail("worker lane collision still active")

print("CONTROL_PLANE_PASS")
