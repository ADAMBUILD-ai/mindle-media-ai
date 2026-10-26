"""Explicit source evaluation entry point; never starts/installs an LTX server."""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mindle_ltx_remote", ROOT / "external_assets/media-production/ltx_remote_adapter.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--action", required=True, choices=["preflight", "status", "submit", "poll", "cancel", "collect", "import"])
    parser.add_argument("--request", type=Path)
    parser.add_argument("--request-id")
    parser.add_argument("--product-root", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.action not in {"preflight", "status"} and not args.execute:
        parser.error("network/import actions require --execute and exact approved configuration")
    adapter = None
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        adapter = module.LtxRemoteAdapter(args.root, config, os.environ.get("MINDLE_LTX_DEVICE_SESSION", ""))
        if args.action == "preflight":
            result = adapter.preflight()
        elif args.action == "status":
            result = adapter.get(args.request_id)
        elif args.action == "submit":
            request = json.loads(args.request.read_text(encoding="utf-8"))
            result = adapter.submit(request["request_id"], Path(request["image_path"]), request["image_sha256"], request["command"], request["params"])
        elif args.action == "import":
            if args.product_root is None:
                raise ValueError("PRODUCT_ROOT_REQUIRED")
            sys.path.insert(0, str(ROOT / "src"))
            from media_ai.product_runtime import ProductJobService
            result = adapter.import_to_product(args.request_id, ProductJobService(args.product_root, ""))
        else:
            result = getattr(adapter, args.action)(args.request_id)
        print(json.dumps({"result": result, "full_product_pass": False}, ensure_ascii=False, indent=2))
        return 0
    except (module.AdapterError, ValueError, KeyError, TypeError, OSError) as error:
        # Requests, URLs and session credentials are not printed on failure.
        code = str(error) if isinstance(error, module.AdapterError) else "INVALID_LOCAL_REQUEST_OR_CONFIGURATION"
        print(json.dumps({"status": "BLOCKED_OR_FAILED", "error_code": code, "full_product_pass": False}))
        return 2
    finally:
        if adapter is not None:
            adapter.close()


if __name__ == "__main__":
    raise SystemExit(main())
