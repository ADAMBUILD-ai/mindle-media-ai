#!/usr/bin/env python3
"""Validate owned external asset identities and optionally probe local programs."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from media_ai.external_media_assets import load_asset_registry, probe_program  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=ROOT / "external_assets/media-production/ASSET_REGISTRY.json")
    parser.add_argument("--ffmpeg", type=Path)
    parser.add_argument("--blender", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    assets = load_asset_registry(args.registry)
    receipt = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "registry": str(args.registry.resolve()),
        "assets": {key: {"state": value.state, "enabled": value.enabled} for key, value in assets.items()},
        "program_probes": {},
        "result": "PASS_REGISTRY_ONLY",
        "runtime_e2e_verified": False,
    }
    if args.ffmpeg:
        receipt["program_probes"]["ffmpeg"] = probe_program(args.ffmpeg)
    if args.blender:
        receipt["program_probes"]["blender"] = probe_program(args.blender, ("--version",))
    if receipt["program_probes"]:
        receipt["result"] = "PASS_IDENTITY_PROBE_ONLY"
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
