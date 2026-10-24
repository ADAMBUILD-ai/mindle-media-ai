"""Validate new office-PC evidence completeness; never award product PASS.

Usage: python scripts/validate_local_pc_acceptance.py EVIDENCE_DIR/receipt.json
All evidence paths are relative to the receipt directory. No credentials needed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

SOURCE = "0e4e12a9e4c758f202c6ebb5085df5a542bb6314"
ZIP_SHA = "8d844a686fdd2f8630b97384cf8d224fbb4195061819a5a79f4576097aeaf527"
RUNTIME = "0e4e12a9e4c7-e533e9ff57d4"
OPERATIONS = {"segment", "upscale", "track", "transcribe"}


def validate(receipt: dict, root: Path) -> list[str]:
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def proof(value, label):
        if not isinstance(value, dict):
            errors.append(label + ": missing file evidence")
            return
        rel = value.get("path", "")
        target = (root / rel).resolve()
        if not rel or Path(rel).is_absolute() or not target.is_relative_to(root.resolve()):
            errors.append(label + ": invalid evidence path")
            return
        if not target.is_file():
            errors.append(label + ": evidence file missing")
            return
        h = hashlib.sha256()
        with target.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(block)
        require(h.hexdigest() == value.get("sha256"), label + ": SHA256 mismatch")
        require(target.stat().st_size == value.get("bytes") and target.stat().st_size > 0,
                label + ": invalid evidence size")

    require(receipt.get("scope") == "OFFICE_PC_NEW_EXECUTION", "wrong execution scope")
    require(receipt.get("source_sha") == SOURCE, "wrong candidate source")
    require(receipt.get("zip_sha256") == ZIP_SHA, "wrong candidate ZIP")
    require(receipt.get("runtime_id") == RUNTIME, "wrong runtime identity")
    require(receipt.get("full_product_pass") is False, "full product PASS prohibited")
    for key in ("execution_id", "started_at", "finished_at", "browser_version"):
        require(bool(receipt.get(key)), "missing " + key)
    proof(receipt.get("runtime_identity"), "runtime identity")
    proof(receipt.get("environment"), "execution environment")
    proof(receipt.get("approved_ui_screenshot"), "approved UI")
    inputs = receipt.get("inputs", [])
    require(len(inputs) == 8 and len({x.get("id") for x in inputs}) == 8,
            "eight unique prepared inputs required")
    for item in inputs:
        proof(item.get("file"), "input " + str(item.get("id")))
        proof(item.get("result"), "input result " + str(item.get("id")))
    buttons = receipt.get("buttons", [])
    require(len(buttons) == 60 and len({x.get("id") for x in buttons}) == 60,
            "60 unique button dispositions required")
    for item in buttons:
        label = "button " + str(item.get("id"))
        kind = item.get("disposition")
        require(kind in {"active", "disabled", "status-only", "unsupported"}, label + ": invalid disposition")
        require(bool(item.get("selector")) and bool(item.get("reason")), label + ": missing selector/reason")
        proof(item.get("evidence"), label)
        if kind == "active":
            require(item.get("result") in {"PASS", "FAIL", "BLOCKED"}, label + ": missing actual outcome")
    jobs = receipt.get("model_jobs", [])
    require({x.get("operation") for x in jobs} == OPERATIONS, "all four model operations required")
    for job in jobs:
        require(job.get("execution_id") == receipt.get("execution_id"), "model job belongs to another execution")
        require(bool(job.get("request_id")) and bool(job.get("job_id")), "model job identities missing")
        proof(job.get("receipt"), "model job")
        proof(job.get("output"), "model output")
    media = receipt.get("media", {})
    require(all(k in media for k in ("MediaError_code", "readyState", "videoWidth", "currentSrc", "before_time", "after_time")),
            "mandatory browser media diagnostics missing")
    # FAIL runs may be submitted. Completeness is separate from runtime success.
    proof(media.get("evidence"), "media diagnostics")
    for key in ("single_instance", "save", "cold_close", "reopen", "export_zip", "export_mp4", "play_seek_audio"):
        proof(receipt.get("lifecycle", {}).get(key), "lifecycle " + key)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.receipt.read_text(encoding="utf-8-sig"))
        errors = validate(value, args.receipt.parent)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        errors = [str(error)]
    print(json.dumps({"status": "EVIDENCE_INCOMPLETE" if errors else "EVIDENCE_COMPLETE_REQUIRES_RUNTIME_REVIEW",
                      "errors": errors, "owner_pc_pass": False, "full_product_pass": False}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
