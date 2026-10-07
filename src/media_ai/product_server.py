"""Local HTTP product surface for the fixed MINDLE MEDIA AI UI."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import subprocess
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .marketing_shortform_gateway import build_marketing_shortform_request
from .marketing_shortform_client import MarketingAuthRequired, MarketingShortformClient, MarketingShortformClientError
from .product_runtime import ProductJobService


class ProductHttpServer(ThreadingHTTPServer):
    def __init__(self, address, handler, root: Path, data_dir: Path, token: str):
        super().__init__(address, handler)
        self.root, self.data_dir = Path(root), Path(data_dir)
        self.service = ProductJobService(self.data_dir, token)
        self.requests: list[dict] = []

    def runtime_identity(self) -> dict:
        package_root = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip()
        if package_root and self.root.resolve() == (Path(package_root) / 'app').resolve() and (Path(package_root) / "PACKAGE_MANIFEST.json").is_file():
            manifest_path = Path(package_root) / "PACKAGE_MANIFEST.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            return {"product": "MINDLE MEDIA AI", "distribution": "EMPLOYEE_WIN_X64",
                    "package_version": manifest["package_version"], "build_commit": manifest["build_commit"],
                    "package_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                    "ui_fingerprint": manifest["ui_fingerprint"], "model_manifest_hash": manifest["model_manifest_hash"],
                    "install_root": str(Path(package_root).resolve()), "data_root": str(self.data_dir.resolve()),
                    "runtime_mode": "LOCAL_OFFLINE_PACKAGE"}
        files = [
            "ui/index.html",
            "ui/approved_visual.css",
            "ui/interaction.css",
            "ui/interaction.js",
            "ui/product_integration.js",
            "ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico",
        ]
        files.extend(relative for relative in ('ui/photo_workspace.js', 'ui/video_workspace.js') if (self.root / relative).is_file())
        hashes = {relative: hashlib.sha256((self.root / relative).read_bytes()).hexdigest() for relative in files}
        fingerprint = hashlib.sha256("\n".join(f"{key}:{hashes[key]}" for key in files).encode("utf-8")).hexdigest()
        branch = head = None
        git_identity_status = "UNAVAILABLE"
        try:
            branch = subprocess.check_output(["git", "-C", str(self.root), "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL).strip()
            head = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
            git_identity_status = "AVAILABLE"
        except (OSError, subprocess.CalledProcessError):
            # File fingerprints remain authoritative when Git is unavailable to this process.
            branch = head = None
        return {"repo_root": str(self.root), "branch": branch, "head": head, "workspace_ui_fingerprint": fingerprint, "file_hashes": hashes,
                "runtime_mode": 'DEVELOPMENT_UI_WITH_PACKAGE_MODELS' if package_root else 'DEVELOPMENT_UI',
                "model_root": package_root or None, "git_identity_status": git_identity_status}


class Handler(BaseHTTPRequestHandler):
    server: ProductHttpServer

    def log_message(self, _format, *args):
        self.server.requests.append({"method": self.command, "path": self.path, "message": " ".join(str(x) for x in args)})

    def _json(self, code: int, payload: dict) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _file(self, path: Path) -> None:
        if not path.is_file() or self.server.data_dir not in path.resolve().parents:
            self.send_error(HTTPStatus.NOT_FOUND); return
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK); self._no_cache_headers(); self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream"); self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content)

    def _no_cache_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route == "/api/runtime-identity":
            self._json(200, self.server.runtime_identity()); return
        if route == "/api/evidence":
            self._json(200, {"jobs": self.server.service.records, "requests": self.server.requests}); return
        if route == '/api/projects/latest':
            try:
                project = self.server.service.latest_project() if os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT') else None
                if project:
                    for job in project['jobs']:
                        primary = Path(job['primary_output']['path']).resolve()
                        job['preview_url'] = '/files/' + primary.relative_to(self.server.data_dir.resolve()).as_posix()
                        source = Path(job['input']['path']).resolve()
                        job['input_url'] = '/files/' + source.relative_to(self.server.data_dir.resolve()).as_posix()
                self._json(200, {'project': project}); return
            except (OSError, ValueError, KeyError, TypeError) as error:
                self._json(422, {'error': '저장된 프로젝트를 불러올 수 없습니다.', 'status': 'PROJECT_REOPEN_FAILED'}); return
        if route.startswith("/files/"):
            self._file(self.server.data_dir / route.removeprefix("/files/")); return
        relative = "index.html" if route in {"/", ""} else route.lstrip("/")
        path = (self.server.root / "ui" / relative).resolve()
        if self.server.root / "ui" not in path.parents or not path.is_file(): self.send_error(HTTPStatus.NOT_FOUND); return
        content = path.read_bytes()
        self.send_response(200); self._no_cache_headers(); self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "text/plain"); self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_POST(self) -> None:
        try:
            route = unquote(urlparse(self.path).path); body = self._body()
            if route == "/api/integrations/marketing/shortform":
                if os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT"):
                    self._json(503, {"status": "MARKETING_PROVIDER_UNAVAILABLE", "error": "마케팅 AI 연결이 필요합니다. 기본 사진/영상 편집은 계속 사용할 수 있습니다."}); return
                client = MarketingShortformClient.from_env()
                request = build_marketing_shortform_request(
                    str(body.get("command", "")),
                    project_id=body.get("project_id"),
                    context=body.get("context") if isinstance(body.get("context"), dict) else None,
                )
                if any(request[field] is None for field in ("product_or_project", "target", "campaign_goal", "duration", "platform")):
                    self._json(422, {"status": "CONTEXT_REQUIRED", "error": "product/target/campaign context is required", "request": request}); return
                try:
                    result = client.create_contract(request)
                except MarketingAuthRequired as error:
                    self._json(503, {"status": "MARKETING_AUTH_ENV_REQUIRED", "error": str(error), "request": request}); return
                except MarketingShortformClientError as error:
                    self._json(502, {"status": "MARKETING_PROVIDER_UNAVAILABLE", "error": str(error), "request": request}); return
                contract = result.get("contract", result) if isinstance(result, dict) else result
                self._json(200, {"status": "bridge_contract_ready", "contract": contract, "provider_response": result, "request": request}); return
            if route == "/api/video-edits":
                result = self.server.service.edit_video(body)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route == "/api/media/import":
                result = self.server.service.import_media(body)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route == "/api/photo-edits":
                result = self.server.service.store_photo_edit(body)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route == "/api/jobs":
                result = self.server.service.execute_isolated(body)
                primary = Path(result["primary_output"]["path"]).relative_to(self.server.data_dir)
                result["preview_url"] = "/files/" + primary.as_posix()
                self._json(201, result); return
            if route == "/api/projects/save": self._json(201, self.server.service.save_project(body)); return
            if route.startswith("/api/projects/") and route.endswith("/export"):
                result = self.server.service.export_project(route.split("/")[3])
                relative = Path(result["export"]["path"]).relative_to(self.server.data_dir)
                result["download_url"] = "/files/" + relative.as_posix(); self._json(201, result); return
            self.send_error(HTTPStatus.NOT_FOUND)
        except Exception as error:
            self._json(422, {"status": "FAILED", "error": str(error)})


def create_server(root: Path, data_dir: Path, token: str, port: int = 0) -> ProductHttpServer:
    return ProductHttpServer(("127.0.0.1", port), Handler, Path(root), Path(data_dir), token)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, default=Path.cwd()); parser.add_argument("--data-dir", type=Path, required=True); parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(); token = os.environ.get("HF_TOKEN")
    if not token and not os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip():
        raise RuntimeError("HF_TOKEN is required for the read-only private model cache")
    server = create_server(args.root, args.data_dir, token, args.port)
    print(f"http://127.0.0.1:{server.server_port}", flush=True); server.serve_forever()


if __name__ == "__main__": main()
