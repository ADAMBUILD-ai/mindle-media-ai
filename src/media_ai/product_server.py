"""Local HTTP product surface for the fixed MINDLE MEDIA AI UI."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import secrets
import subprocess
import sys
import threading
from datetime import datetime, timezone
from uuid import uuid4
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
        # File containment and generated URLs must share one canonical root.
        # Relative and Windows 8.3 roots otherwise differ from resolved files.
        self.root, self.data_dir = Path(root).resolve(), Path(data_dir).resolve()
        self.service = ProductJobService(self.data_dir, token)
        self.requests: list[dict] = []
        self.job_lock = threading.Lock()
        self.completed_requests: dict[str, tuple[str, dict]] = {}
        self.instance_id = str(uuid4())
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.control_nonce = secrets.token_urlsafe(32)
        self.lifecycle_lock = threading.Lock()
        self.active_requests = 0
        self.stopping = False
        self.workflows = None
        self.workflow_init_lock = threading.Lock()
        if (self.data_dir/'workflows/queue.sqlite3').is_file():
            try:self.workflow_queue()
            except Exception:
                self.server_close();raise

    def workflow_queue(self):
        from .durable_workflows import DurableWorkflows
        with self.workflow_init_lock:
            if self.workflows is None:self.workflows=DurableWorkflows(self.service)
            return self.workflows

    def server_close(self):
        try:
            if self.workflows is not None:self.workflows.close()
        finally:super().server_close()

    def begin_request(self) -> bool:
        with self.lifecycle_lock:
            if self.stopping:
                return False
            self.active_requests += 1
            return True

    def end_request(self) -> None:
        with self.lifecycle_lock:
            self.active_requests -= 1

    def run_once(self, route: str, body: dict, action) -> dict:
        """Serialize mutations; replay only an identical successful request in this session."""
        request_id = str(body.get('request_id', ''))
        fingerprint = hashlib.sha256((route + json.dumps(body, sort_keys=True)).encode()).hexdigest()
        with self.job_lock:
            if self.workflows is not None and self.workflows.busy():raise ValueError('순차 작업이 진행 중입니다. 완료하거나 취소한 뒤 편집·저장하세요.')
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
        return self._runtime_identity() | {
            'server_pid': os.getpid(), 'server_instance_id': self.instance_id,
            'server_started_at': self.started_at,
            'server_command': [sys.executable, *sys.argv],
            'owner_shutdown_supported': True,
        }

    def _runtime_identity(self) -> dict:
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
        files.extend(relative for relative in ('ui/photo_workspace.js', 'ui/video_workspace.js', 'ui/workspace_shell.js', 'ui/timeline_preview.js', 'ui/workflow_execution.js') if (self.root / relative).is_file())
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
        self.send_response(code); self._no_cache_headers(); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)

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

    def _local_control_request(self) -> bool:
        hosts = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        host = self.headers.get('Host', '')
        origin = self.headers.get('Origin')
        return (self.client_address[0] == '127.0.0.1' and host in hosts
                and (origin is None or origin == 'http://' + host)
                and self.headers.get('Sec-Fetch-Site') != 'cross-site')

    def do_GET(self) -> None:
        if not self.server.begin_request():
            self._json(503, {'status': 'RUNTIME_STOPPING'}); return
        try:
            self._do_GET()
        finally:
            self.server.end_request()

    def _do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route == '/api/runtime/control':
            if not self._local_control_request():
                self._json(403, {'status': 'LOCAL_CONTROL_REQUIRED'}); return
            self._json(200, {'server_pid': os.getpid(), 'server_instance_id': self.server.instance_id,
                             'control_nonce': self.server.control_nonce}); return
        if route == '/api/workflows/capabilities':
            from .workflow_planner import capabilities
            self._json(200,capabilities(self.server.data_dir));return
        if route == '/api/workflows':
            self._json(200,{'workflows':self.server.workflow_queue().list()});return
        if route.startswith('/api/workflows/'):
            try:
                value=self.server.workflow_queue().get(route.rsplit('/',1)[1])
                if value['state']=='SUCCEEDED':
                    value['result']['preview_url']='/files/'+Path(value['result']['primary_output']['path']).relative_to(self.server.data_dir).as_posix()
                    if value.get('export'):value['export']['download_url']='/files/'+Path(value['export']['export']['path']).relative_to(self.server.data_dir).as_posix()
                self._json(200,value)
            except ValueError as error:self._json(404,{'error':str(error)})
            return
        if route.startswith('/files/workflows/'):
            try:
                value=self.server.workflow_queue().get(route.split('/')[3])
                if value['state']!='SUCCEEDED' or not self.server.workflow_queue().published_file(value['workflow_id'],self.server.data_dir/route.removeprefix('/files/')):self._json(403,{'status':'WORKFLOW_OUTPUT_NOT_PUBLISHED'});return
            except ValueError:self._json(404,{'status':'NOT_FOUND'});return
        if route == "/api/runtime-identity":
            self._json(200, self.server.runtime_identity()); return
        if route == '/api/runtime-readiness':
            import shutil
            package = os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', '').strip()
            ffmpeg = str(Path(package)/'tools/ffmpeg/ffmpeg.exe') if package else shutil.which('ffmpeg')
            self._json(200, {'product':'MINDLE MEDIA AI', 'models': self.server.service.model_readiness,
                             'video_tool_present': bool(ffmpeg and Path(ffmpeg).is_file()),
                             'auto_edit_engine':'OpenCV measured scene window + FFmpeg',
                             'auto_edit_model_inference':False, 'generative_provider':'NOT_CONNECTED',
                             'physical_owner_acceptance':'NOT_VERIFIED'}); return
        if route == "/api/evidence":
            self._json(200, {"jobs": self.server.service.records, "requests": self.server.requests}); return
        if route.startswith('/api/tasks/'):
            identifier=route.rsplit('/',1)[1]
            report=self.server.service.active_reports.get(identifier)
            if report:
                try:value=json.loads(report.read_text(encoding='utf-8'))
                except (OSError,ValueError):value={'status':'RUNNING','state':'worker_starting','request_id':identifier}
                self._json(200,value);return
            completed=next((item for item in self.server.service.records.values() if item.get('request_id')==identifier),None)
            self._json(200 if completed else 404,completed or {'status':'NOT_FOUND'});return
        if route.startswith('/api/jobs/'):
            job=self.server.service.records.get(route.rsplit('/',1)[1])
            self._json(200 if job else 404, {'job':job});return
        if route == '/api/assets':
            assets=[]
            for record in self.server.service.records.values():
                if record.get('operation') != 'import': continue
                item=dict(record)
                path=Path(item['primary_output']['path']).resolve()
                if path.is_file() and self.server.data_dir.resolve() in path.parents:
                    item['preview_url']='/files/'+path.relative_to(self.server.data_dir.resolve()).as_posix()
                    assets.append(item)
            self._json(200, {'assets':assets}); return
        if route == '/api/projects':
            projects = []
            for path in sorted(self.server.service.projects.glob('*.json'), key=lambda p:p.stat().st_mtime, reverse=True):
                try:
                    project = json.loads(path.read_text(encoding='utf-8'))
                    from .durable_workflows import is_published
                    if not is_published(self.server.data_dir,project.get('workflow_id')):continue
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
                    from .durable_workflows import is_published
                    if not is_published(self.server.data_dir,project.get('workflow_id')):raise ValueError('미완료 작업')
                    for job in project['jobs']:
                        primary = Path(job.get('preview_output', job['primary_output'])['path']).resolve()
                        job['preview_url'] = '/files/' + primary.relative_to(self.server.data_dir.resolve()).as_posix()
                        source = Path(job['input']['path']).resolve()
                        job['input_url'] = '/files/' + source.relative_to(self.server.data_dir.resolve()).as_posix()
                        job['reference_urls']=[{'url':'/files/'+Path(ref['path']).resolve().relative_to(self.server.data_dir.resolve()).as_posix(),'name':ref.get('original_filename',ref['file_name'])} for ref in job.get('reference_artifacts',[])]
                    workspace = project.get('workspace', {})
                    assets = [ref for lane in ('photo', 'video') for ref in workspace.get('references', {}).get(lane, [])]
                    if workspace.get('audio'):
                        assets.append(workspace['audio'])
                    for asset in assets:
                        asset['url'] = '/files/' + Path(asset['path']).resolve().relative_to(self.server.data_dir).as_posix()
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

    def _owner_shutdown(self) -> None:
        if (not self._local_control_request() or not secrets.compare_digest(
                self.headers.get('X-Mindle-Control', '').encode('utf-8'), self.server.control_nonce.encode('utf-8'))):
            self._json(403, {'status': 'LOCAL_CONTROL_REQUIRED'}); return
        try:
            body = self._body()
        except Exception:
            self._json(400, {'status': 'INVALID_CONTROL_REQUEST'}); return
        if not isinstance(body, dict):
            self._json(400, {'status': 'INVALID_CONTROL_REQUEST'}); return
        if body.get('server_pid') != os.getpid() or body.get('server_instance_id') != self.server.instance_id:
            self._json(409, {'status': 'RUNTIME_IDENTITY_MISMATCH'}); return
        with self.server.lifecycle_lock:
            if self.server.active_requests or self.server.stopping or (self.server.workflows is not None and self.server.workflows.busy()):
                self._json(409, {'status': 'RUNTIME_BUSY'}); return
            self.server.stopping = True
        try:
            self._json(202, {'status': 'RUNTIME_STOPPING', 'server_pid': os.getpid(),
                             'server_instance_id': self.server.instance_id})
        finally:
            # An owner disconnect after acceptance must not strand a draining server.
            threading.Thread(target=self.server.shutdown, daemon=True).start()

    def do_POST(self) -> None:
        if unquote(urlparse(self.path).path) == '/api/runtime/shutdown':
            self._owner_shutdown(); return
        if not self.server.begin_request():
            self._json(503, {'status': 'RUNTIME_STOPPING'}); return
        try:
            self._do_POST()
        finally:
            self.server.end_request()

    def _do_POST(self) -> None:
        try:
            route = unquote(urlparse(self.path).path); body = self._body()
            self.server.requests.append({'method':'POST','path':route,'lane':body.get('lane'),
                                         'operation':body.get('operation'),'request_id':body.get('request_id')})
            if route.startswith('/api/workflows'):
                if not self._local_control_request():self._json(403,{'status':'LOCAL_CONTROL_REQUIRED'});return
                if route == '/api/workflows/plan':
                    from .workflow_planner import make_plan
                    self._json(200,make_plan(self.server.data_dir,body));return
                if route == '/api/workflows':
                    with self.server.job_lock:value=self.server.workflow_queue().submit(body)
                    self._json(202,value);return
                if route.endswith('/cancel'):
                    self._json(200,self.server.workflow_queue().cancel(route.split('/')[3]));return
                self.send_error(404);return
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
            if route == "/api/projects/save": self._json(201, self.server.run_once(route,body,self.server.service.save_project)); return
            if route.startswith("/api/projects/") and route.endswith("/export"):
                result = self.server.run_once(route,body,lambda _body:self.server.service.export_project(route.split("/")[3]))
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



