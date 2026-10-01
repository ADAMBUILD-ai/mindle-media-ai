#!/usr/bin/env python3
"""Validate the MINDLE MEDIA AI PC Work control plane before execution."""

from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_EPOCH = "MEDIA-AI-20261001-V20.2"
EXPECTED_DIRECTIVE = "docs/commander/MINDLE_MEDIA_AI_WINDOWS_ONSCREEN_UI_REPRESENTATIVE_VISUAL_FUNCTION_AUDIT_DIRECTIVE_v20.2_20261001.md"
EXPECTED_CONTRACT = "docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2_20261001.json"

LOCK = ROOT / "CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json"
CURRENT = ROOT / "CURRENT_PC_WORK_DIRECTIVE.md"
STATE = ROOT / "CURRENT_PC_WORK_STATE.json"
REG_MD = ROOT / "docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md"
REG_JSON = ROOT / "docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json"

def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(message: str) -> None:
    print(f"CONTROL_PLANE_MISMATCH_BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(2)

for path in (LOCK, CURRENT, STATE, REG_MD, REG_JSON):
    if not path.exists():
        fail(f"missing required control-plane file: {path.relative_to(ROOT)}")

lock = load_json(LOCK)
state = load_json(STATE)
registry = load_json(REG_JSON)
current_text = CURRENT.read_text(encoding="utf-8")
registry_text = REG_MD.read_text(encoding="utf-8")

checks = [
    ("lock epoch", lock.get("epoch"), EXPECTED_EPOCH),
    ("state epoch", state.get("control_plane_epoch"), EXPECTED_EPOCH),
    ("registry epoch", registry.get("control_plane_epoch"), EXPECTED_EPOCH),
    ("lock directive", lock.get("active_directive"), EXPECTED_DIRECTIVE),
    ("state directive", state.get("active_directive"), EXPECTED_DIRECTIVE),
    ("registry directive", registry.get("active", {}).get("directive"), EXPECTED_DIRECTIVE),
    ("lock contract", lock.get("evidence_contract"), EXPECTED_CONTRACT),
    ("state contract", state.get("evidence_contract"), EXPECTED_CONTRACT),
    ("registry contract", registry.get("active", {}).get("evidence_contract"), EXPECTED_CONTRACT),
]

for label, actual, expected in checks:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, got {actual!r}")

for token in (EXPECTED_EPOCH, EXPECTED_DIRECTIVE, EXPECTED_CONTRACT):
    if token not in current_text:
        fail(f"CURRENT_PC_WORK_DIRECTIVE.md missing {token!r}")

if EXPECTED_EPOCH not in registry_text:
    fail("Rule Registry MD missing current epoch")
if EXPECTED_DIRECTIVE not in registry_text:
    fail("Rule Registry MD missing current directive")
if EXPECTED_CONTRACT not in registry_text:
    fail("Rule Registry MD missing current contract")

active_start = registry_text.find("## 2. ACTIVE")
active_end = registry_text.find("## 3.", active_start)
if active_start < 0 or active_end < 0:
    fail("Rule Registry MD ACTIVE section not found")
active_section = registry_text[active_start:active_end]

for stale in ("v20.1_20261001.md", "v20.1_20261001.json", "v20.0_20261001.md", "v19.0_20261001.md"):
    if stale in active_section:
        fail(f"stale cycle appears in ACTIVE section: {stale}")

if EXPECTED_DIRECTIVE not in active_section or EXPECTED_CONTRACT not in active_section:
    fail("ACTIVE section does not contain the expected v20.2 execution pair")

print("CONTROL_PLANE_PASS")
print(f"EPOCH={EXPECTED_EPOCH}")
print(f"DIRECTIVE={EXPECTED_DIRECTIVE}")
print(f"CONTRACT={EXPECTED_CONTRACT}")
