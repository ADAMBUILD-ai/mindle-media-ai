#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
EXPECTED_EPOCH="MEDIA-AI-20261003-V21.0"
EXPECTED_DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_FULL_PRODUCT_REAL_USE_REAUDIT_AND_IMPROVEMENT_DIRECTIVE_v21.0_20261003.md"
EXPECTED_CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v21.0_20261003.json"
LOCK=ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
CURRENT=ROOT/"CURRENT_PC_WORK_DIRECTIVE.md"
STATE=ROOT/"CURRENT_PC_WORK_STATE.json"
REG_JSON=ROOT/"docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json"
def fail(m):
    print(f"CONTROL_PLANE_MISMATCH_BLOCKED: {m}",file=sys.stderr); raise SystemExit(2)
for p in (LOCK,CURRENT,STATE,REG_JSON):
    if not p.exists(): fail(f"missing {p.relative_to(ROOT)}")
lock=json.loads(LOCK.read_text(encoding="utf-8")); state=json.loads(STATE.read_text(encoding="utf-8")); reg=json.loads(REG_JSON.read_text(encoding="utf-8"))
checks=[("lock epoch",lock.get("epoch"),EXPECTED_EPOCH),("state epoch",state.get("control_plane_epoch"),EXPECTED_EPOCH),("registry epoch",reg.get("control_plane_epoch"),EXPECTED_EPOCH),("lock directive",lock.get("active_directive"),EXPECTED_DIRECTIVE),("state directive",state.get("active_directive"),EXPECTED_DIRECTIVE),("registry directive",reg.get("active",{}).get("directive"),EXPECTED_DIRECTIVE),("lock contract",lock.get("evidence_contract"),EXPECTED_CONTRACT),("state contract",state.get("evidence_contract"),EXPECTED_CONTRACT),("registry contract",reg.get("active",{}).get("evidence_contract"),EXPECTED_CONTRACT)]
for label,a,e in checks:
    if a!=e: fail(f"{label}: expected {e!r}, got {a!r}")
print("CONTROL_PLANE_PASS")
