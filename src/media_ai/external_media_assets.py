"""Fail-closed adapters for MEDIA-owned external production assets.

The module does not install programs or download model weights.  It verifies a
local registry and constructs narrowly-scoped requests for already materialized
assets so external tools cannot become an arbitrary command execution surface.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ASSET_STATES = {
    "SOURCE_APPROVED_PENDING_MATERIALIZATION",
    "RUNTIME_READY",
    "PRODUCT_RUNTIME_VERIFIED",
    "DEFERRED_HARDWARE",
}


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class ExternalAsset:
    asset_id: str
    kind: str
    state: str
    source_url: str
    upstream_revision: str
    license_id: str
    license_url: str
    enabled: bool
    local_path: str | None = None
    sha256: str | None = None
    notes: str = ""

    def validate(self, root: Path) -> None:
        if self.state not in ASSET_STATES:
            raise ValueError(f"invalid asset state: {self.asset_id}")
        if not all((self.asset_id, self.kind, self.source_url, self.upstream_revision,
                    self.license_id, self.license_url)):
            raise ValueError(f"incomplete asset identity: {self.asset_id}")
        if self.enabled and self.state not in {"RUNTIME_READY", "PRODUCT_RUNTIME_VERIFIED"}:
            raise ValueError(f"unverified asset cannot be enabled: {self.asset_id}")
        if self.local_path or self.sha256:
            if not self.local_path or not self.sha256:
                raise ValueError(f"path and SHA-256 must be paired: {self.asset_id}")
            path = (root / self.local_path).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"asset file is unavailable: {self.asset_id}")
            if file_sha256(path) != self.sha256:
                raise ValueError(f"asset SHA-256 mismatch: {self.asset_id}")


def load_asset_registry(path: Path) -> dict[str, ExternalAsset]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported external asset registry schema")
    assets: dict[str, ExternalAsset] = {}
    for raw in payload.get("assets", []):
        asset = ExternalAsset(**raw)
        if asset.asset_id in assets:
            raise ValueError(f"duplicate asset id: {asset.asset_id}")
        asset.validate(path.parent)
        assets[asset.asset_id] = asset
    if not assets:
        raise ValueError("external asset registry is empty")
    return assets


@dataclass(frozen=True)
class BlenderRenderRequest:
    blend_file: Path
    camera: str
    output_dir: Path
    frame_start: int
    frame_end: int
    fps: int = 24
    width: int = 1920
    height: int = 1080


class BlenderCameraAdapter:
    """Builds a Blender command that can invoke only the owned render driver."""

    def __init__(self, executable: Path, driver: Path, driver_sha256: str, owned_job_root: Path) -> None:
        self.executable = executable.resolve()
        self.driver = driver.resolve()
        self.owned_job_root = owned_job_root.resolve()
        if not self.driver.is_file() or file_sha256(self.driver) != driver_sha256:
            raise ValueError("Blender driver identity mismatch")

    def build_command(self, request: BlenderRenderRequest, request_json: Path, receipt_json: Path) -> list[str]:
        if not request.blend_file.is_file() or request.blend_file.suffix.lower() != ".blend":
            raise ValueError("a local .blend source is required")
        if not request.camera or len(request.camera) > 128:
            raise ValueError("a bounded existing camera name is required")
        if not (1 <= request.frame_start <= request.frame_end <= 1_000_000):
            raise ValueError("invalid Blender frame range")
        if not (1 <= request.fps <= 120 and 64 <= request.width <= 8192 and 64 <= request.height <= 8192):
            raise ValueError("invalid Blender render settings")
        output_dir = request.output_dir.resolve()
        request_json = request_json.resolve()
        receipt_json = receipt_json.resolve()
        if any(not path.is_relative_to(self.owned_job_root) for path in (output_dir, request_json, receipt_json)):
            raise ValueError("Blender job files must stay inside the owned job root")
        payload = {
            "schema_version": 1,
            "blend_file_sha256": file_sha256(request.blend_file),
            "camera": request.camera,
            "owned_job_root": str(self.owned_job_root),
            "output_dir": str(output_dir),
            "frame_start": request.frame_start,
            "frame_end": request.frame_end,
            "fps": request.fps,
            "width": request.width,
            "height": request.height,
        }
        request_json.parent.mkdir(parents=True, exist_ok=True)
        request_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return [str(self.executable), "--background", str(request.blend_file.resolve()), "--python", str(self.driver), "--", "--request", str(request_json), "--receipt", str(receipt_json)]


class ComfyUIWanAdapter:
    """Submits a hash-pinned graph to an isolated loopback ComfyUI instance."""

    def __init__(self, base_url: str, workflow_path: Path, workflow_sha256: str,
                 allowed_overrides: set[tuple[str, str]], isolated_process_owned: bool,
                 transport: Callable[[str, str, dict[str, Any] | None], dict[str, Any]] | None = None) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "::1"} or not parsed.port:
            raise ValueError("ComfyUI must use an explicit loopback HTTP port")
        if not workflow_path.is_file() or file_sha256(workflow_path) != workflow_sha256:
            raise ValueError("ComfyUI workflow identity mismatch")
        self.base_url = base_url.rstrip("/")
        self.workflow_path = workflow_path
        self.allowed_overrides = allowed_overrides
        self.isolated_process_owned = isolated_process_owned
        self.transport = transport or self._http_json
        self._owned_prompts: set[str] = set()

    def render_workflow(self, overrides: dict[tuple[str, str], Any]) -> dict[str, Any]:
        unexpected = set(overrides) - self.allowed_overrides
        if unexpected:
            raise ValueError(f"workflow override is not allowlisted: {sorted(unexpected)!r}")
        graph = deepcopy(json.loads(self.workflow_path.read_text(encoding="utf-8")))
        for (node_id, input_name), value in overrides.items():
            node = graph.get(node_id)
            if not isinstance(node, dict) or not isinstance(node.get("inputs"), dict) or input_name not in node["inputs"]:
                raise ValueError(f"workflow input does not exist: {node_id}.{input_name}")
            node["inputs"][input_name] = value
        return graph

    def submit(self, overrides: dict[tuple[str, str], Any], client_id: str) -> str:
        response = self.transport("POST", "/prompt", {"prompt": self.render_workflow(overrides), "client_id": client_id})
        prompt_id = response.get("prompt_id")
        if not isinstance(prompt_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", prompt_id):
            raise RuntimeError("ComfyUI returned no prompt_id")
        self._owned_prompts.add(prompt_id)
        return prompt_id

    def history(self, prompt_id: str) -> dict[str, Any]:
        if prompt_id not in self._owned_prompts:
            raise PermissionError("prompt is not owned by this adapter")
        return self.transport("GET", f"/history/{prompt_id}", None)

    def interrupt(self, prompt_id: str) -> None:
        if not self.isolated_process_owned:
            raise PermissionError("global ComfyUI interrupt requires an isolated MEDIA-owned process")
        if prompt_id not in self._owned_prompts:
            raise PermissionError("prompt is not owned by this adapter")
        self.transport("POST", "/interrupt", {})

    @staticmethod
    def resolve_output(output_root: Path, relative_name: str) -> Path:
        root = output_root.resolve()
        candidate = (root / relative_name).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            raise ValueError("ComfyUI output is outside the owned output root or unavailable")
        return candidate

    def _http_json(self, method: str, path: str, payload: dict[str, Any] | None) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(self.base_url + path, data=body, method=method, headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))


def probe_program(executable: Path, version_args: tuple[str, ...] = ("-version",), timeout: int = 10) -> dict[str, Any]:
    """Records program identity without treating presence as an E2E PASS."""
    completed = subprocess.run([str(executable), *version_args], capture_output=True, text=True, timeout=timeout, check=False)
    text = (completed.stdout or completed.stderr).splitlines()
    return {"path": str(executable), "exit_code": completed.returncode, "version_line": text[0] if text else "", "executable_sha256": file_sha256(executable) if executable.is_file() else None}
