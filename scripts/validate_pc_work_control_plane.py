#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
EXPECTED_EPOCH="MEDIA-AI-20261002-V20.2.7"
EXPECTED_DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_DESKTOP_SHORTCUT_REACTIVATION_ONLY_DIRECTIVE_v20.2.7_20261002.md"
EXPECTED_CONTRACT="docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.7_20261002.json"
LOCK=ROOT/"CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
CURRENT=ROOT/"CURRENT_PC_WORK_DIRECTIVE.md"
STATE=ROOT/"CURRENT_PC_WORK_STATE.json"
REG_MD=ROOT/"docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md"
REG_JSON=ROOT/"docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json"
def fail(msg):
    print(f"CONTROL_PLANE_MISMATCH_BLOCKED: {msg}",file=sys.stderr)
    raise SystemExit(2)
for p in (LOCK,CURRENT,STATE,REG_MD,REG_JSON):
    if not p.exists(): fail(f"missing {p.relative_to(ROOT)}")
lock=json.loads(LOCK.read_text(encoding="utf-8"))
state=json.loads(STATE.read_text(encoding="utf-8"))
registry=json.loads(REG_JSON.read_text(encoding="utf-8"))
checks=[
("lock epoch",lock.get("epoch"),EXPECTED_EPOCH),
("state epoch",state.get("control_plane_epoch"),EXPECTED_EPOCH),
("registry epoch",registry.get("control_plane_epoch"),EXPECTED_EPOCH),
("lock directive",lock.get("active_directive"),EXPECTED_DIRECTIVE),
("state directive",state.get("active_directive"),EXPECTED_DIRECTIVE),
("registry directive",registry.get("active",{}).get("directive"),EXPECTED_DIRECTIVE),
("lock contract",lock.get("evidence_contract"),EXPECTED_CONTRACT),
("state contract",state.get("evidence_contract"),EXPECTED_CONTRACT),
("registry contract",registry.get("active",{}).get("evidence_contract"),EXPECTED_CONTRACT),
]
for label,a,e in checks:
    if a!=e: fail(f"{label}: expected {e!r}, got {a!r}")
print("CONTROL_PLANE_PASS")
