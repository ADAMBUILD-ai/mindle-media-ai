#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
EXPECTED_EPOCH="MEDIA-AI-20261006-EMPLOYEE-PACKAGE-V1.0"
EXPECTED_DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_FULL_WINDOWS_PACKAGE_DIRECTIVE_v1.0_20261006.md"
EXPECTED_CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_EMPLOYEE_PACKAGE_v1.0_20261006.json"
LOCK=ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
CURRENT=ROOT/"CURRENT_PC_WORK_DIRECTIVE.md"
STATE=ROOT/"CURRENT_PC_WORK_STATE.json"
REG_JSON=ROOT/"docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json"
WORKER_LOCK=ROOT/"CURRENT_WORKER_COORDINATION_LOCK.json"
def fail(msg):
    print(f"CONTROL_PLANE_MISMATCH_BLOCKED: {msg}", file=sys.stderr)
    raise SystemExit(2)
for p in (LOCK,CURRENT,STATE,REG_JSON,WORKER_LOCK):
    if not p.exists(): fail(f"missing {p.relative_to(ROOT)}")
lock=json.loads(LOCK.read_text(encoding="utf-8"))
state=json.loads(STATE.read_text(encoding="utf-8"))
reg=json.loads(REG_JSON.read_text(encoding="utf-8"))
worker=json.loads(WORKER_LOCK.read_text(encoding="utf-8"))
current=CURRENT.read_text(encoding="utf-8")
checks=[
 ("lock epoch",lock.get("epoch"),EXPECTED_EPOCH),
 ("state epoch",state.get("control_plane_epoch"),EXPECTED_EPOCH),
 ("registry epoch",reg.get("control_plane_epoch"),EXPECTED_EPOCH),
 ("worker epoch",worker.get("active_control_plane_epoch"),EXPECTED_EPOCH),
 ("lock directive",lock.get("active_directive"),EXPECTED_DIRECTIVE),
 ("state directive",state.get("active_directive"),EXPECTED_DIRECTIVE),
 ("registry directive",reg.get("active",{}).get("directive"),EXPECTED_DIRECTIVE),
 ("lock contract",lock.get("evidence_contract"),EXPECTED_CONTRACT),
 ("state contract",state.get("evidence_contract"),EXPECTED_CONTRACT),
 ("registry contract",reg.get("active",{}).get("evidence_contract"),EXPECTED_CONTRACT),
]
for label,actual,expected in checks:
    if actual!=expected: fail(f"{label}: expected {expected!r}, got {actual!r}")
for token in (EXPECTED_EPOCH,EXPECTED_DIRECTIVE,EXPECTED_CONTRACT):
    if token not in current: fail(f"CURRENT_PC_WORK_DIRECTIVE missing {token!r}")
print("CONTROL_PLANE_PASS")
print(f"EPOCH={EXPECTED_EPOCH}")
print(f"DIRECTIVE={EXPECTED_DIRECTIVE}")
print(f"CONTRACT={EXPECTED_CONTRACT}")
