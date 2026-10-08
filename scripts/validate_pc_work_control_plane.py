#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
EPOCH="MEDIA-AI-20261008-PRODUCT-E2E-VIDEO-PREVIEW-TO-FULL-PASS-R1"
DIRECTIVE="docs/commander/MINDLE_MEDIA_AI_PRODUCT_E2E_VIDEO_PREVIEW_TO_FULL_PASS_DIRECTIVE_v1.0_20261008.md"
CONTRACT="docs/commander/MINDLE_MEDIA_AI_PRODUCT_E2E_VIDEO_PREVIEW_TO_FULL_PASS_EVIDENCE_CONTRACT_v1.0_20261008.json"

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

if state.get("product_changes_allowed") is not True:
    fail("product_changes_allowed must be true")
if state.get("package_build_allowed") is not False:
    fail("package_build_allowed must be false for this product E2E lane")
if state.get("ui_changes_allowed") is not False:
    fail("ui_changes_allowed must remain false for visual/layout changes")
if worker.get("pr23_hold_do_not_merge") is not True:
    fail("PR #23 must remain HOLD / DO NOT MERGE")

print("CONTROL_PLANE_PASS")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"CONTRACT={CONTRACT}")
