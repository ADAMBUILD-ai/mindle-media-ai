"""Local HTTP product surface for the fixed MINDLE MEDIA AI UI."""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .product_runtime import ProductJobService


class ProductHttpServer(ThreadingHTTPServer):
    def __init__(self, address, handler, root: Path, data_dir: Path, token: str):
        super().__init__(address, handler)
        self.root, self.data_dir = Path(root), Path(data_dir)
        self.service = ProductJobService(self.data_dir, token)
        self.requests: list[dict] = []


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
        self.send_response(HTTPStatus.OK); self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream"); self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_GET(self) -> None:
        route = unquote(urlparse(self.path).path)
        if route == "/api/evidence":
            self._json(200, {"jobs": self.server.service.records, "requests": self.server.requests}); return
        if route.startswith("/files/"):
            self._file(self.server.data_dir / route.removeprefix("/files/")); return
        relative = "index.html" if route in {"/", ""} else route.lstrip("/")
        path = (self.server.root / "ui" / relative).resolve()
        if self.server.root / "ui" not in path.parents or not path.is_file(): self.send_error(HTTPStatus.NOT_FOUND); return
        content = path.read_bytes()
        self.send_response(200); self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "text/plain"); self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_POST(self) -> None:
        try:
            route = unquote(urlparse(self.path).path); body = self._body()
            if route == "/api/jobs":
                result = self.server.service.execute(body)
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
    if not token: raise RuntimeError("HF_TOKEN is required for the read-only private model cache")
    server = create_server(args.root, args.data_dir, token, args.port)
    print(f"http://127.0.0.1:{server.server_port}", flush=True); server.serve_forever()


if __name__ == "__main__": main()
