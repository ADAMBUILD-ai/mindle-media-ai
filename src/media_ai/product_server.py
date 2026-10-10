"""Local HTTP product surface for the fixed MINDLE MEDIA AI UI."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import subprocess
import threading
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
        self.job_lock = threading.Lock()
        self.completed_requests: dict[str, tuple[str, dict]] = {}

    def run_once(self, route: str, body: dict, action) -> dict:
        """Serialize mutations; replay only an identical successful request in this session."""
        request_id = str(body.get('request_id', ''))
        fingerprint = hashlib.sha256((route + json.dumps(body, sort_keys=True)).encode()).hexdigest()
        with self.job_lock:
            previous = self.completed_requests.get(request_id) if request_id else None
            if previous:
                if previous[0] != fingerprint:
                    raise ValueError('같은 요청 ID에 다른 작업을 보낼 수 없습니다.')
                return previous[1]
            result = action(body)
            if request_id:
                self.completed_requests[request_id] = (fingerprint, result)
            return result

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
        files.extend(relative for relative in ('ui/photo_workspace.js', 'ui/video_workspace.js', 'ui/workspace_shell.js') if (self.root / relative).is_file())
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
        size = path.stat().st_size
        start, end, code = 0, size - 1, HTTPStatus.OK
        requested = self.headers.get('Range')
        if requested:
            import re
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested.strip())
            try:
                if not match or not any(match.groups()):raise ValueError('invalid range')
                first, last = match.groups()
                if first:
                    start = int(first);end = min(int(last), size-1) if last else size-1
                else:
                    length = int(last)
                    if length <= 0:raise ValueError('invalid suffix range')
                    start = max(0, size-length)
                if start > end or start >= size:raise ValueError('unsatisfiable range')
                code = HTTPStatus.PARTIAL_CONTENT
            except ValueError:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0');self.end_headers();return
        self.send_response(code);self._no_cache_headers()
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length',str(max(0,end-start+1)))
        if code == HTTPStatus.PARTIAL_CONTENT:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        with path.open('rb') as stream:
            stream.seek(start);remaining=end-start+1
            while remaining > 0:
                block=stream.read(min(65536,remaining))
                if not block:break
                try:self.wfile.write(block)
                except (BrokenPipeError, ConnectionResetError):break
                remaining-=len(block)

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
        if route == '/api/projects':
            projects = []
            for path in sorted(self.server.service.projects.glob('*.json'), key=lambda p:p.stat().st_mtime, reverse=True):
                try:
                    project = json.loads(path.read_text(encoding='utf-8'))
                    projects.append({'project_id':project['project_id'], 'saved_at':project['saved_at'], 'job_count':len(project['job_ids'])})
                except (OSError, ValueError, KeyError, TypeError):
                    continue
            self._json(200, {'projects':projects, 'data_root':str(self.server.data_dir.resolve())}); return
        if route == '/api/projects/latest' or route.startswith('/api/projects/'):
            try:
                if route == '/api/projects/latest':
                    project = self.server.service.latest_project()
                else:
                    from uuid import UUID
                    project_id = str(UUID(route.rsplit('/', 1)[1]))
                    project = json.loads((self.server.service.projects / (project_id+'.json')).read_text(encoding='utf-8'))
                if project:
                    for job in project['jobs']:
                        primary = Path(job.get('preview_output', job['primary_output'])['path']).resolve()
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
            self.server.requests.append({'method':'POST','path':route,'lane':body.get('lane'),
                                         'operation':body.get('operation'),'request_id':body.get('request_id')})
            if route == "/api/integrations/marketing/shortform":
                if os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT") or os.environ.get('MINDLE_DEFER_EXTERNAL_SHORTFORM') == '1':
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
                result = self.server.run_once(route, body, self.server.service.edit_video)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route == "/api/media/import":
                result = self.server.run_once(route, body, self.server.service.import_media)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route == "/api/photo-edits":
                result = self.server.run_once(route, body, self.server.service.store_photo_edit)
                primary = Path(result['primary_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route.startswith('/api/jobs/') and route.endswith('/preview'):
                result = self.server.service.prepare_browser_preview(route.split('/')[3])
                primary = Path(result['preview_output']['path']).relative_to(self.server.data_dir)
                result['preview_url'] = '/files/' + primary.as_posix()
                self._json(201, result); return
            if route.startswith('/api/jobs/') and route.endswith('/background'):
                result = self.server.service.prepare_photo_background(route.split('/')[3])
                result['preview_url'] = '/files/' + Path(result['preview_output']['path']).relative_to(self.server.data_dir).as_posix()
                self._json(201, result); return
            if route == "/api/jobs":
                result = self.server.run_once(route, body, self.server.service.execute_isolated)
                if result.get("operation") == "tracking":
                    result = self.server.service.prepare_browser_preview(result["job_id"])
                if result.get('operation') == 'segment' and any(word in str(body.get('command', '')) for word in ('배경', 'background')):
                    result = self.server.service.prepare_photo_background(result['job_id'])
                primary = Path(result.get("preview_output", result["primary_output"])["path"]).relative_to(self.server.data_dir)
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
    server = create_server(args.root, args.data_dir, token or '', args.port)
    print(f"http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__": main()

