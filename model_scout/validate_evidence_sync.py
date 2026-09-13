"""Fail closed when the evidence registry, artifacts, and matrix disagree."""
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
REGISTRY = ROOT / "evidence" / "model_scout" / "registry.json"
MATRIX = ROOT / "docs" / "06_MODEL_SCOUT_VALIDATION_MATRIX.md"
HUMAN_REVIEW = ROOT / "evidence" / "model_scout" / "HUMAN_QUALITY_REVIEW_RESULTS.json"
WHISPER_KO = ROOT / "evidence" / "model_scout" / "WHISPER_KO_BENCHMARK_RESULTS.json"
MATTING = ROOT / "evidence" / "model_scout" / "MATTING_SCOUT_RESULTS.json"

REVIEW_FIELDS = {"fixture_id", "status", "defect_type", "severity", "reviewer_note", "recommended_action"}

def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matrix = MATRIX.read_text(encoding="utf-8")
    if "evidence absent locally" in matrix:
        raise SystemExit("matrix contains a retired evidence-absent status")
    for candidate in registry["candidates"]:
        evidence = candidate.get("evidence")
        if evidence and evidence.endswith(".json") and evidence.startswith(".."):
            path = (REGISTRY.parent / evidence).resolve()
            if not path.exists(): raise SystemExit(f"missing evidence: {candidate['candidate']}: {path}")
        if candidate["adapter_enabled"]: raise SystemExit(f"adapter may not be enabled before production gate: {candidate['candidate']}")
        if candidate["decision"] not in matrix: raise SystemExit(f"matrix missing decision {candidate['decision']}")
    review = json.loads(HUMAN_REVIEW.read_text(encoding="utf-8"))
    expected = {"super_resolution", "mask_and_tracking", "inpaint"}
    if {item["capability"] for item in review["models"]} != expected:
        raise SystemExit("human review capability coverage mismatch")
    for item in review["models"]:
        if len(item["fixtures"]) != 5:
            raise SystemExit(f"human review fixture count mismatch: {item['capability']}")
        for fixture in item["fixtures"]:
            if not REVIEW_FIELDS.issubset(fixture):
                raise SystemExit(f"human review schema mismatch: {item['capability']}")
    whisper = json.loads(WHISPER_KO.read_text(encoding="utf-8"))
    if whisper["status"] != "BLOCKED_MISSING_LICENSED_KOREAN_AUDIO" or whisper["fixtures"]:
        raise SystemExit("Whisper Korean benchmark must remain fail-closed without licensed fixtures")
    matting = json.loads(MATTING.read_text(encoding="utf-8"))
    if matting["rejected_candidate"]["decision"] != "SOURCE_REVIEW_REJECT" or matting["candidates"]:
        raise SystemExit("Matting scout must remain fail-closed before safe-candidate review")
    print("evidence sync pass")

if __name__ == "__main__": main()
