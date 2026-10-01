"""Validate and apply a completed human-review packet without enabling adapters."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
TARGET = ROOT / "evidence/model_scout/HUMAN_QUALITY_REVIEW_RESULTS.json"
CAPABILITIES = {"super_resolution", "mask_and_tracking", "inpaint"}
REQUIRED_FIELDS = {"fixture_id", "status", "defect_type", "severity", "reviewer_note", "recommended_action"}
TERMINAL = {"KEEP", "REPLACE"}


def validate(packet: dict) -> None:
    if {model["capability"] for model in packet["models"]} != CAPABILITIES:
        raise ValueError("review packet capability coverage mismatch")
    if not packet.get("reviewer") or not packet.get("reviewed_at"):
        raise ValueError("reviewer and reviewed_at are required")
    for model in packet["models"]:
        if len(model["fixtures"]) != 5:
            raise ValueError(f"fixture count mismatch: {model['capability']}")
        if any(not REQUIRED_FIELDS.issubset(fixture) for fixture in model["fixtures"]):
            raise ValueError(f"fixture fields missing: {model['capability']}")
        if any(fixture["status"] not in TERMINAL for fixture in model["fixtures"]):
            raise ValueError(f"non-terminal fixture decision: {model['capability']}")
        if model["decision"] not in TERMINAL:
            raise ValueError(f"non-terminal model decision: {model['capability']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    packet = json.loads(args.source.read_text(encoding="utf-8"))
    validate(packet)
    if args.apply:
        TARGET.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("human review packet valid" if not args.apply else "human review packet applied; adapters remain disabled")


if __name__ == "__main__":
    main()
