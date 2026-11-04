#!/usr/bin/env python3
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from media_ai.candidate_reuse_gate import evaluate_rebuild_request, validate_test_r2_reuse  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--rebuild-request", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.rebuild_request:
        request = json.loads(args.rebuild_request.read_text(encoding="utf-8"))
        decision = evaluate_rebuild_request(args.root, request)
    else:
        decision = validate_test_r2_reuse(args.root)
    rendered = json.dumps(asdict(decision), ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if decision.status in {"REUSE_TEST_R2", "REBUILD_AUTHORIZATION_CONTRACT_COMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
