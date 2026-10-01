import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "model_scout"))

from import_human_review import validate
from validate_intake_manifests import main as validate_intake_manifests


def test_pending_input_manifests_are_fail_closed():
    validate_intake_manifests()


def test_human_review_import_requires_terminal_fixture_decisions():
    fixture = {
        "fixture_id": "01",
        "status": "REVIEW_REQUIRED",
        "defect_type": None,
        "severity": None,
        "reviewer_note": None,
        "recommended_action": None,
    }
    packet = {
        "reviewer": "reviewer",
        "reviewed_at": "2026-09-15T00:00:00Z",
        "models": [
            {"capability": capability, "decision": "KEEP", "fixtures": [deepcopy(fixture) for _ in range(5)]}
            for capability in ("super_resolution", "mask_and_tracking", "inpaint")
        ],
    }
    with pytest.raises(ValueError, match="non-terminal fixture decision"):
        validate(packet)
