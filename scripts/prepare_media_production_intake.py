"""Measure supplied local media into a NEW intake folder; never grants execution.

No asset search/download/copy, model start, approval mutation, or package build.
The existing media_ai.e2e_intake remains the authoritative technical validator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from media_ai.e2e_intake import intake_result


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def measure(item, role, base, probe, errors):
    if not isinstance(item, dict):
        errors.append(role + ": invalid entry")
        return item
    value = dict(item)
    for field in ("label", "source_or_owner", "license_or_permission", "rights_evidence"):
        if not isinstance(value.get(field), str):
            errors.append(role + ": textual " + field + " missing or invalid")
            # Null/non-text is missing input, never the literal label 'None'.
            # Keep the original value in OPERATOR_INPUT_SNAPSHOT for review.
            value[field] = ""
    candidate = value.get("path")
    if not isinstance(candidate, str) or not candidate.strip():
        errors.append(role + ": file path missing")
        return value
    path = (base / candidate).resolve()
    value["path"] = str(path)
    if not path.is_file():
        errors.append(role + ": supplied file unavailable")
        return value
    try:
        before = sha(path)
        measured = {"sha256": before, "bytes": path.stat().st_size}
        if probe is None:
            raise ValueError("ffprobe unavailable on PATH")
        result = subprocess.run([probe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                                capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
        info = json.loads(result.stdout)
        stream = next(x for x in info.get("streams", []) if x.get("codec_type") == role)
        duration = float(info["format"]["duration"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("invalid duration")
        measured["duration_seconds"] = duration
        if role == "video":
            measured.update(width=stream["width"], height=stream["height"])
        if sha(path) != before or path.stat().st_size != measured["bytes"]:
            errors.append(role + ": file changed during measurement")
            # A false declared identity ensures the downstream validator also rejects it.
            value["sha256"] = "CHANGED_DURING_MEASUREMENT"
        for field, actual in measured.items():
            # Do not silently repair a supplied expectation. The existing validator
            # will reject any expected SHA/size/duration/dimensions that disagree.
            value.setdefault(field, actual)
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, StopIteration) as error:
        errors.append(role + ": measurement failed (" + type(error).__name__ + ")")
    return value


def prepare(request_path, output):
    request_path, output = Path(request_path).resolve(), Path(output).resolve()
    raw = request_path.read_bytes()
    request = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(request, dict):
        raise ValueError("operator input must be an object")
    permitted = {"narration_script", "voice_length_policy", "volumes", "clips", "bgm", "field_guide", "duration_seconds", "aspect", "require_rights_evidence"}
    if set(request) - permitted:
        raise ValueError("UNSUPPORTED_OPERATOR_FIELDS")
    if request.get("duration_seconds", 30) != 30 or request.get("aspect", "16:9") != "16:9" or request.get("require_rights_evidence", True) is not True:
        raise ValueError("FIXED_DELIVERY_OR_RIGHTS_CONTRACT_CHANGED")
    if output.exists():
        raise ValueError("NEW_OUTPUT_DIRECTORY_REQUIRED")
    errors = []
    probe = shutil.which("ffprobe")
    manifest = {"work_id": "MEDIA-AI-CORE-E2E-R2-20261025", "require_rights_evidence": True,
                "duration_seconds": 30, "aspect": "16:9", "narration_script": request.get("narration_script"),
                "voice_length_policy": request.get("voice_length_policy"),
                "volumes": request.get("volumes", {"narration": None, "original": None, "bgm": None}),
                "clips": [], "bgm": None}
    clips = request.get("clips", [])
    if not isinstance(clips, list) or len(clips) > 12:
        raise ValueError("at most twelve explicitly selected clips required")
    manifest["clips"] = [measure(x, "video", request_path.parent, probe, errors) for x in clips]
    if request.get("bgm") is not None:
        manifest["bgm"] = measure(request["bgm"], "audio", request_path.parent, probe, errors)
    if request_path.read_bytes() != raw:
        raise ValueError("OPERATOR_INPUT_CHANGED_DURING_PREPARATION")
    output.mkdir(parents=True, exist_ok=False)
    write(output / "OPERATOR_INPUT_SNAPSHOT.json", request)
    write(output / "INPUT_MANIFEST.json", manifest)
    result = intake_result(output / "INPUT_MANIFEST.json")
    write(output / "INTAKE_RESULT.json", result)
    write(output / "ASSET_INTAKE.json", result)
    all_errors = list(dict.fromkeys(errors + result["errors"]))
    receipt = {"status": "BLOCKED_ASSET_INTAKE" if all_errors else "PASS_INTAKE_TECHNICAL_ONLY",
               "request_path": str(request_path), "request_sha256": hashlib.sha256(raw).hexdigest(),
               "manifest_sha256": result["manifest_sha256"], "errors": all_errors,
               "ffprobe": {"path": probe, "sha256": sha(probe) if probe else None},
               "scope": "LOCAL_INPUT_MEASUREMENT_NOT_PRODUCTION", "rights_review": "OWNER_DECLARATIONS_ONLY",
               "next_action": "COMPLETE_OPERATOR_INPUT" if all_errors else "RUN_EXACT_SOURCE_ENGINE_PREFLIGHT",
               "production_started": False, "model_started": False, "approval_granted": False,
               "pc_execution_authorized": False, "build_gate": False, "full_product_pass": False}
    write(output / "PREPARATION_RECEIPT.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.request, args.out)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"status": "BLOCKED_INTAKE_PREPARATION", "error_type": type(error).__name__,
                          "output_not_overwritten": True, "full_product_pass": False}))
        return 2
    print(json.dumps({"status": result["status"], "errors": result["errors"], "next_action": result["next_action"],
                      "full_product_pass": False}, ensure_ascii=False, indent=2))
    return 0 if not result["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
