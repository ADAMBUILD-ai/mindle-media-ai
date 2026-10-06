#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

EPOCH = "MEDIA-AI-20261006-WINDOWS-SANDBOX-ACL-RECOVERY-V1.1"
DIRECTIVE = "docs/commander/MINDLE_MEDIA_AI_PC_WORK_WINDOWS_SANDBOX_ACL_STATE_RECOVERY_DIRECTIVE_v1.1_20261006.md"
CONTRACT = "docs/commander/MINDLE_MEDIA_AI_PC_WORK_WINDOWS_SANDBOX_ACL_STATE_RECOVERY_EVIDENCE_CONTRACT_v1.1_20261006.json"

CURRENT = ROOT / "CURRENT_PC_WORK_DIRECTIVE.md"
LOCK = ROOT / "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
STATE = ROOT / "CURRENT_PC_WORK_STATE.json"
WORKER = ROOT / "CURRENT_WORKER_COORDINATION_LOCK.json"

def fail(message: str) -> None:
    print("CONTROL_PLANE_MISMATCH_BLOCKED: " + message, file=sys.stderr)
    raise SystemExit(2)

for path in (CURRENT, LOCK, STATE, WORKER):
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")

current = CURRENT.read_text(encoding="utf-8")
lock = json.loads(LOCK.read_text(encoding="utf-8"))
state = json.loads(STATE.read_text(encoding="utf-8"))
worker = json.loads(WORKER.read_text(encoding="utf-8"))

checks = [
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
        fail(f"CURRENT_PC_WORK_DIRECTIVE missing {token!r}")

if state.get("product_changes_allowed") is not False:
    fail("product_changes_allowed must remain false during recovery")
if state.get("package_build_allowed") is not False:
    fail("package_build_allowed must remain false during recovery")

print("CONTROL_PLANE_PASS")
print(f"EPOCH={EPOCH}")
print(f"DIRECTIVE={DIRECTIVE}")
print(f"CONTRACT={CONTRACT}")
