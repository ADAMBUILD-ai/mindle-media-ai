"""Fail closed until owned E2E and Korean-audio inputs are supplied."""
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]

MANIFESTS = (
    (ROOT / "evidence/e2e/PHOTO_INPUT_MANIFEST.json", [f"F{index}" for index in range(1, 7)], "input_path"),
    (ROOT / "evidence/e2e/VIDEO_INPUT_MANIFEST.json", [f"V{index}" for index in range(1, 6)], "input_path"),
    (ROOT / "evidence/model_scout/WHISPER_KO_INPUT_MANIFEST.json", [f"KO{index}" for index in range(1, 4)], "audio_path"),
)


def main() -> None:
    for path, expected_ids, input_field in MANIFESTS:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        fixtures = manifest["fixtures"]
        if manifest["required_count"] != len(expected_ids) or [item["fixture_id"] for item in fixtures] != expected_ids:
            raise SystemExit(f"fixture coverage mismatch: {path.name}")
        for fixture in fixtures:
            if fixture["status"].startswith("BLOCKED_"):
                if fixture["source_or_license"] is not None or fixture["ownership"] is not None or fixture[input_field] is not None:
                    raise SystemExit(f"blocked fixture contains unverified source data: {path.name} {fixture['fixture_id']}")
            elif not all(fixture.get(field) for field in ("source_or_license", "ownership", input_field)):
                raise SystemExit(f"ready fixture lacks provenance: {path.name} {fixture['fixture_id']}")
    print("intake manifests pass")


if __name__ == "__main__":
    main()
