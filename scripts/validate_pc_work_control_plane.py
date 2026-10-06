#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_AND_ENVIRONMENT_DIAGNOSTIC_DIRECTIVE_v1.0_20261006.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261006.json"
CURRENT=ROOT/"CURRENT_PC_WORK_DIRECTIVE.md"
LOCK=ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
STATE=ROOT/"CURRENT_PC_WORK_STATE.json"
WORKER=ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json"
REG=ROOT/"docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json"

def fail(msg):
    print("CONTROL_PLANE_MISMATCH_BLOCKED: "+msg, file=sys.stderr)
    raise SystemExit(2)

for p in (CURRENT,LOCK,STATE,WORKER,REG):
    if not p.is_file():
        fail("missing "+str(p.relative_to(ROOT)))

current=CURRENT.read_text(encoding="utf-8")
lock=json.loads(LOCK.read_text(encoding="utf-8"))
state=json.loads(STATE.read_text(encoding="utf-8"))
worker=json.loads(WORKER.read_text(encoding="utf-8"))
reg=json.loads(REG.read_text(encoding="utf-8"))

checks=[
 ("lock epoch",lock.get("epoch"),EPOCH),
 ("state epoch",state.get("control_plane_epoch"),EPOCH),
 ("worker epoch",worker.get("active_control_plane_epoch"),EPOCH),
 ("registry epoch",reg.get("control_plane_epoch"),EPOCH),
 ("lock directive",lock.get("active_directive"),DIRECTIVE),
 ("state directive",state.get("active_directive"),DIRECTIVE),
 ("registry directive",reg.get("active",{}).get("directive"),DIRECTIVE),
 ("lock contract",lock.get("evidence_contract"),CONTRACT),
 ("state contract",state.get("evidence_contract"),CONTRACT),
 ("registry contract",reg.get("active",{}).get("evidence_contract"),CONTRACT),
]
for label,actual,expected in checks:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, got {actual!r}")

for token in (EPOCH,DIRECTIVE,CONTRACT):
    if token not in current:
        fail("CURRENT missing "+token)

if state.get("active_preflight") is not None:
    fail("stale active_preflight still present")
if state.get("parent_directive") is not None:
    fail("stale parent_directive still active")
if state.get("technical_base_directive") is not None:
    fail("stale technical_base_directive still active")
if worker.get("collision_status") != "NO_ACTIVE_COLLISION":
    fail("worker lane collision still active")
if reg.get("active_preflight") is not None or reg.get("parent_directive") is not None or reg.get("technical_base_directive") is not None:
    fail("registry still activates historical chain")

print("CONTROL_PLANE_PASS")
print("EPOCH="+EPOCH)
print("DIRECTIVE="+DIRECTIVE)
print("CONTRACT="+CONTRACT)
