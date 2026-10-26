"""Opt-in LTX Desktop 1.3.1 image-to-video adapter; no installation or fallback.

Remote success is a provider claim, not independently attested model inference.
This isolated source adapter is deliberately not enabled in the product UI.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager
import hashlib
from http.client import HTTPException
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler
from uuid import UUID, uuid4

UPSTREAM = "8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b"
STATES = {"queued", "running", "cancelling", "succeeded", "failed", "cancelled"}
PARAMS = {"prompt", "model", "resolution", "duration", "fps", "aspectRatio", "seed"}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def object_hash(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value):
        raise ValueError("INVALID_PROVIDER_ID")
    return value


def redact(value):
    if isinstance(value, dict):
        return {k: ("REDACTED" if any(x in k.lower() for x in ("token", "secret", "authorization", "bytes_url", "thumbnail_url")) else redact(v))
                for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


class AdapterError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class LtxRemoteAdapter:
    """Persistent request binding and real, authenticated HTTP transport.

    Every write is preceded by a durable intent. Ambiguous POSTs are never retried.
    Only a separately approved loopback engine can be contacted.
    """

    def __init__(self, root: Path, config: dict, token: str):
        self.root = Path(root).resolve()
        self.config = json.loads(canonical(config))
        self.token = token
        self.base = str(config.get("base_url", "")).rstrip("/")
        parsed = urlsplit(self.base)
        try:
            local = ipaddress.ip_address(parsed.hostname or "").is_loopback
            port = parsed.port
        except ValueError:
            local, port = False, None
        if not (local and parsed.scheme == "http" and port and not parsed.username and not parsed.password
                and parsed.path == "" and not parsed.query and not parsed.fragment):
            raise ValueError("APPROVED_LOOPBACK_ORIGIN_REQUIRED")
        if any(c.isspace() for c in token):
            raise ValueError("DEVICE_SESSION_TOKEN_REQUIRED")
        if config.get("upstream_revision") != UPSTREAM:
            raise ValueError("UNSUPPORTED_UPSTREAM_REVISION")
        self.config_hash = object_hash(config)
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root / "ltx-jobs.sqlite3", timeout=10)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, body TEXT NOT NULL)")
        self.db.commit()
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def close(self):
        self.db.close()

    @contextmanager
    def lease(self, request_id):
        request_id = str(UUID(request_id))
        lock = self.root / (request_id + ".lock")
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise AdapterError("REQUEST_BUSY_OR_INTERRUPTED_REVIEW_REQUIRED") from None
        try:
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            yield
        finally:
            lock.unlink(missing_ok=True)

    def preflight(self):
        c = self.config
        if not (c.get("execution_approved") is True and c.get("license_reviewed") is True
                and c.get("offline_reviewed") is True and c.get("approval_id")):
            raise AdapterError("BLOCKED_EXECUTION_APPROVAL")
        if c.get("review_scope") not in {"source_evaluation", "contract_test"}:
            raise AdapterError("BLOCKED_REVIEW_SCOPE")
        files = c.get("identity_files", [])
        if not files or not {"application", "runtime", "model", "settings", "ffprobe", "ffmpeg"}.issubset({x.get("role") for x in files}):
            raise AdapterError("BLOCKED_ENGINE_IDENTITY_INCOMPLETE")
        for item in files:
            p = Path(item["path"])
            if not p.is_file() or p.stat().st_size != item["bytes"] or digest(p) != item["sha256"]:
                raise AdapterError("BLOCKED_ENGINE_IDENTITY_CHANGED")
        settings_files = [x for x in files if x["role"] == "settings"]
        if len(settings_files) != 1:
            raise AdapterError("BLOCKED_SETTINGS_IDENTITY")
        try:
            settings = json.loads(Path(settings_files[0]["path"]).read_text(encoding="utf-8"))
        except (ValueError, OSError):
            raise AdapterError("BLOCKED_SETTINGS_FORMAT") from None
        expected = {"use_local_text_encoder": True, "prompt_enhancer_enabled": False,
                    "explore_auto_enhance_prompts": False, "user_prefers_ltx_api_video_generations": False,
                    "assistant_provider": "local", "budget_mode": "standard"}
        if any(settings.get(k) != v or type(settings.get(k)) is not type(v) for k, v in expected.items()):
            raise AdapterError("BLOCKED_NONLOCAL_OR_MUTATING_PROMPT_SETTINGS")
        if any(settings.get(k) for k in ("ltx_api_key", "gemini_api_key", "fal_api_key")):
            raise AdapterError("BLOCKED_EXTERNAL_API_CREDENTIALS_PRESENT")
        if not c.get("allowed_params"):
            raise AdapterError("BLOCKED_MODEL_CAPABILITY_APPROVAL")
        return {"status": "LOCAL_FILES_VERIFIED", "config_sha256": self.config_hash,
                "runtime_attestation": "NOT_AVAILABLE_FROM_REMOTE_API"}

    def _url(self, path):
        url = urljoin(self.base + "/", path)
        parsed = urlsplit(url)
        base = urlsplit(self.base)
        if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc) or parsed.fragment:
            raise AdapterError("CROSS_ORIGIN_OR_FRAGMENT_REJECTED")
        return url

    def _open(self, method, path, body=None, content_type=None):
        if not self.token:
            raise AdapterError("DEVICE_SESSION_TOKEN_REQUIRED")
        headers = {"Authorization": "Bearer " + self.token, "Accept": "application/json"}
        if content_type:
            headers["Content-Type"] = content_type
        try:
            return self.opener.open(Request(self._url(path), data=body, headers=headers, method=method), timeout=30)
        except HTTPError as e:
            # Never expose a signed URL, Bearer token, or an untrusted error body.
            raise AdapterError("PROVIDER_HTTP_" + str(e.code)) from None
        except (URLError, OSError, TimeoutError, HTTPException):
            raise AdapterError("PROVIDER_TRANSPORT_ERROR") from None

    def _json(self, method, path, body=None, content_type=None):
        if isinstance(body, dict):
            body, content_type = canonical(body).encode(), "application/json"
        try:
            with self._open(method, path, body, content_type) as response:
                data = response.read(2 * 1024 * 1024 + 1)
        except (HTTPException, OSError):
            raise AdapterError("PROVIDER_TRUNCATED_JSON") from None
        if len(data) > 2 * 1024 * 1024:
            raise AdapterError("PROVIDER_JSON_TOO_LARGE")
        try:
            result = json.loads(data)
        except (ValueError, UnicodeError):
            raise AdapterError("PROVIDER_INVALID_JSON") from None
        if not isinstance(result, dict):
            raise AdapterError("PROVIDER_OBJECT_REQUIRED")
        return result

    def get(self, request_id):
        row = self.db.execute("SELECT body FROM jobs WHERE id=?", (str(UUID(request_id)),)).fetchone()
        if not row:
            raise AdapterError("REQUEST_NOT_FOUND")
        value = json.loads(row[0])
        if value["config_sha256"] != self.config_hash:
            raise AdapterError("CONFIG_BINDING_CHANGED")
        return value

    def _save(self, value):
        value["updated_at"] = time.time()
        self.db.execute("INSERT OR REPLACE INTO jobs VALUES (?,?,?)", (value["request_id"], value["fingerprint"], canonical(value)))
        self.db.commit()
        path = self.root / (value["request_id"] + ".json")
        pending = path.with_suffix(".tmp")
        pending.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(pending, path)

    def _input_check(self, value):
        binding = {k: value[k] for k in ("image_path", "image_sha256", "command", "params", "config_sha256")}
        if object_hash(binding) != value["fingerprint"]:
            raise AdapterError("SAVED_REQUEST_BINDING_CHANGED")
        if "submitted_payload" in value and object_hash(value["submitted_payload"]) != value["submitted_spec_sha256"]:
            raise AdapterError("SAVED_SUBMISSION_CHANGED")
        p = Path(value["image_path"])
        if not p.is_file() or digest(p) != value["image_sha256"]:
            raise AdapterError("INPUT_CHANGED")

    def submit(self, request_id, image, image_sha256, command, params):
        request_id = str(UUID(request_id))
        self.preflight()
        image = Path(image).resolve()
        if not isinstance(command, str) or not command.strip() or len(command) > 12000:
            raise ValueError("ORIGINAL_COMMAND_REQUIRED")
        if set(params) != PARAMS or not isinstance(params["prompt"], str) or not params["prompt"].strip():
            raise ValueError("EXACT_I2V_PARAMS_REQUIRED")
        if (type(params["duration"]) is not int or params["duration"] not in {2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20}
                or type(params["fps"]) is not int or params["fps"] != 24
                or type(params["seed"]) is not int or not 0 <= params["seed"] < 2**31
                or params["aspectRatio"] != "16:9"
                or params["resolution"] not in {"270p", "360p", "540p", "720p", "1080p"}
                or params["model"] not in {"ltx-2.3-fast", "ltx-2.5-fast"}):
            raise ValueError("BOUNDED_I2V_PARAMETERS_REQUIRED")
        # Initial scope: fixed neutral camera, no negative-prompt or Enhance API.
        if params not in self.config["allowed_params"]:
            raise AdapterError("PARAMETERS_OUTSIDE_APPROVAL")
        dimensions = self.config.get("output_dimensions", {}).get(object_hash(params))
        if not (isinstance(dimensions, list) and len(dimensions) == 2
                and all(type(x) is int and 64 <= x <= 3840 and x % 2 == 0 for x in dimensions)):
            raise AdapterError("EXACT_OUTPUT_DIMENSIONS_REQUIRED")
        if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} or not image.is_file() or not 0 < image.stat().st_size <= 16 * 1024 * 1024:
            raise ValueError("BOUNDED_REFERENCE_IMAGE_REQUIRED")
        if digest(image) != image_sha256:
            raise AdapterError("INPUT_CHANGED")
        body = {"image_path": str(image), "image_sha256": image_sha256, "command": command, "params": params,
                "config_sha256": self.config_hash}
        fingerprint = object_hash(body)
        with self.lease(request_id):
            try:
                previous = self.get(request_id)
            except AdapterError as e:
                if str(e) != "REQUEST_NOT_FOUND":
                    raise
            else:
                if previous["fingerprint"] != fingerprint:
                    raise AdapterError("REQUEST_ID_REUSED_WITH_DIFFERENT_INPUT")
                return previous  # No POST retry even when result was lost.
            value = {**body, "request_id": request_id, "fingerprint": fingerprint,
                     "state": "UPLOAD_INTENT", "created_at": time.time(), "events": [],
                     "provider_job_id": None, "full_product_pass": False, "model_inference_verified": False,
                     "review_scope": self.config["review_scope"]}
            self._save(value)
            try:
                self._json("GET", "/api/session")
                specs = self._json("GET", "/api/generate/models-specs")
                self._capability_check(specs, params)
                value["capability_response_sha256"] = object_hash(specs)
                boundary = "mindle" + uuid4().hex
                data = image.read_bytes()
                if hashlib.sha256(data).hexdigest() != image_sha256:
                    raise AdapterError("INPUT_CHANGED")
                multipart = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="reference{image.suffix.lower()}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()
                             + data + f"\r\n--{boundary}--\r\n".encode())
                asset = self._json("POST", "/api/assets/upload", multipart, "multipart/form-data; boundary=" + boundary)
                asset_id = identifier(asset.get("id"))
                if asset.get("media_kind") != "image":
                    raise AdapterError("REFERENCE_ASSET_KIND_MISMATCH")
                self._input_check(value)
                value["input_asset_id"] = asset_id
                payload = {"params": {**params, "cameraMotion": "none", "negativePrompt": "", "promptProvenance": "typed"},
                           "inputs": {"startFrame": {"assetId": asset_id}}, "contract_version": 1}
                value.update(state="SUBMISSION_UNKNOWN", submitted_payload=payload, submitted_spec_sha256=object_hash(payload))
                self._save(value)  # Durable before POST; crash/timeout cannot trigger duplicate generation.
                result = self._json("POST", "/api/generations/image-to-video", payload)
                value["provider_job_id"] = identifier(result.get("id"))
                self._apply(value, result)
            except (AdapterError, ValueError, TypeError, KeyError) as error:
                if value["state"] == "UPLOAD_INTENT":
                    value["state"] = "UPLOAD_FAILED"
                value["error_code"] = str(error) if isinstance(error, AdapterError) else "PROVIDER_CONTRACT_ERROR"
                self._save(value)
                raise AdapterError(value["error_code"]) from None
            return value

    @staticmethod
    def _capability_check(specs, params):
        if specs.get("budgetMode") != "standard" or specs.get("active_offering") != params["model"]:
            raise AdapterError("BLOCKED_LOCAL_MODEL_CAPABILITY")
        installed = [x for x in specs.get("downloaded_local_models", []) if x.get("model") == params["model"]]
        if len(installed) != 1 or not installed[0].get("pipeline"):
            raise AdapterError("BLOCKED_LOCAL_MODEL_NOT_AVAILABLE")
        # Model offering and pipeline are separate identities. Both model versions
        # may advertise the same 'fast' pipeline; never infer it from a model name.
        local = [x for x in specs.get("local_models", []) if x.get("pipeline") == installed[0]["pipeline"]]
        if len(local) != 1:
            raise AdapterError("BLOCKED_LOCAL_MODEL_NOT_AVAILABLE")
        spec = local[0].get("spec", {})
        cell = spec.get("supported_resolutions_durations", {}).get(params["resolution"], {})
        if (spec.get("capabilities", {}).get("i2v") is not True
                or params["duration"] not in cell.get("fps_to_durations", {}).get(str(params["fps"]), [])
                or params["aspectRatio"] not in cell.get("aspect_ratios", [])):
            raise AdapterError("BLOCKED_LOCAL_MODEL_CAPABILITY")

    def _apply(self, value, response):
        value["events"].append({"at": time.time(), "response_sha256": object_hash(response), "response": redact(response)})
        status = response.get("status")
        if status not in STATES:
            value["state"] = "BLOCKED_PROVIDER_CONTRACT"
            self._save(value)
            raise AdapterError("UNKNOWN_PROVIDER_STATE")
        spec = response.get("spec", {})
        returned = spec.get("params", {})
        wanted = value["params"]
        if (response.get("id") != value["provider_job_id"] or response.get("feature") != "image-to-video"
                or response.get("contract_version") != 1
                or any(returned.get(k) != v for k, v in wanted.items())
                or spec.get("inputs", {}).get("startFrame", {}).get("assetId") != value["input_asset_id"]):
            value["state"] = "BLOCKED_PROVIDER_CONTRACT"
            self._save(value)
            raise AdapterError("RETURNED_PLAN_MISMATCH")
        value["provider_status"] = status
        value["state"] = {"succeeded": "PROVIDER_SUCCEEDED_UNVERIFIED", "failed": "FAILED", "cancelled": "CANCELLED",
                          "queued": "QUEUED", "running": "RUNNING", "cancelling": "CANCELLING"}[status]
        value["returned_spec_sha256"] = object_hash(spec)
        value["provider_error_code"] = response.get("error_code")
        value["provider_output_ids"] = [identifier(x.get("id")) for x in response.get("outputs", []) if x.get("media_kind") == "video"]
        self._save(value)

    def poll(self, request_id):
        self.preflight()
        with self.lease(request_id):
            value = self.get(request_id)
            self._input_check(value)
            if value["state"] in {"COLLECTED_TECHNICAL_ONLY", "IMPORTED_TECHNICAL_ONLY", "FAILED", "CANCELLED", "BLOCKED_PROVIDER_CONTRACT"}:
                return value
            job = identifier(value.get("provider_job_id"))
            result = self._json("GET", "/api/generations/" + job)
            self._apply(value, result)
            return value

    def cancel(self, request_id):
        self.preflight()
        with self.lease(request_id):
            value = self.get(request_id)
            if value["state"] not in {"QUEUED", "RUNNING", "CANCELLING", "CANCEL_REQUEST_UNKNOWN"}:
                raise AdapterError("CANCEL_NOT_ALLOWED_FOR_STATE")
            if value["state"] in {"CANCELLING", "CANCEL_REQUEST_UNKNOWN"}:
                return value  # Query first; never repeat an ambiguous POST.
            job = identifier(value.get("provider_job_id"))
            value["state"] = "CANCEL_REQUEST_UNKNOWN"
            self._save(value)
            result = self._json("POST", "/api/generations/" + job + "/cancel")
            self._apply(value, result)
            return value

    def _program(self, role):
        return next(x["path"] for x in self.config["identity_files"] if x["role"] == role)

    def _technical_check(self, path, params):
        try:
            p = subprocess.run([self._program("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                               capture_output=True, check=True, timeout=30)
            info = json.loads(p.stdout)
            videos = [x for x in info["streams"] if x.get("codec_type") == "video"]
            if len(videos) != 1:
                raise ValueError("video stream count")
            v = videos[0]
            rate = v["avg_frame_rate"].split("/")
            fps = float(rate[0]) / float(rate[1])
            duration = float(info["format"]["duration"])
            width, height = int(v["width"]), int(v["height"])
            if not math.isfinite(duration) or abs(duration - params["duration"]) > .15 or abs(fps - params["fps"]) > .01:
                raise ValueError("duration or fps")
            aw, ah = map(int, params["aspectRatio"].split(":"))
            if abs(width / height - aw / ah) > .02:
                raise ValueError("aspect")
            if [width, height] != self.config["output_dimensions"][object_hash(params)]:
                raise ValueError("resolution")
            subprocess.run([self._program("ffmpeg"), "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
                           capture_output=True, check=True, timeout=120)
        except (subprocess.SubprocessError, OSError, ValueError, KeyError, ZeroDivisionError):
            raise AdapterError("OUTPUT_TECHNICAL_VALIDATION_FAILED") from None
        return {"duration": duration, "fps": fps, "width": width, "height": height, "decoded": True}

    def collect(self, request_id):
        self.preflight()
        with self.lease(request_id):
            value = self.get(request_id)
            self._input_check(value)
            if value["state"] in {"COLLECTED_TECHNICAL_ONLY", "IMPORTED_TECHNICAL_ONLY"}:
                output = value["output"]
                if not Path(output["path"]).is_file() or digest(output["path"]) != output["sha256"]:
                    raise AdapterError("COLLECTED_OUTPUT_CHANGED")
                return value
            if value["state"] != "PROVIDER_SUCCEEDED_UNVERIFIED" or len(value["provider_output_ids"]) != 1:
                raise AdapterError("SINGLE_VERIFIED_PROVIDER_OUTPUT_REQUIRED")
            asset_id = identifier(value["provider_output_ids"][0])
            asset = self._json("GET", "/api/assets/" + asset_id)
            if asset.get("id") != asset_id or asset.get("media_kind") != "video":
                raise AdapterError("OUTPUT_ASSET_MISMATCH")
            url = self._url(str(asset.get("bytes_url", "")))
            parsed = urlsplit(url)
            if unquote(parsed.path) != "/api/assets/" + asset_id + "/bytes":
                raise AdapterError("OUTPUT_URL_PATH_MISMATCH")
            output = self.root / (value["request_id"] + ".mp4")
            pending = output.with_suffix(".download")
            if output.exists():
                raise AdapterError("UNREGISTERED_OUTPUT_EXISTS")
            limit = 128 * 1024 * 1024
            try:
                with self._open("GET", url) as response, pending.open("xb") as stream:
                    total = 0
                    declared = response.headers.get("Content-Length")
                    for block in iter(lambda: response.read(1024 * 1024), b""):
                        total += len(block)
                        if total > limit:
                            raise AdapterError("OUTPUT_TOO_LARGE")
                        stream.write(block)
                    if not total or declared is not None and total != int(declared):
                        raise AdapterError("OUTPUT_EMPTY_OR_TRUNCATED")
                technical = self._technical_check(pending, value["params"])
                self.preflight()
                self._input_check(value)
                os.replace(pending, output)
                value.update(state="COLLECTED_TECHNICAL_ONLY", output={"path": str(output), "sha256": digest(output), "bytes": total},
                             technical_review=technical, provider_generation_claim=True,
                             human_quality_review="NOT_EXECUTED", runtime_attestation="NOT_AVAILABLE_FROM_REMOTE_API",
                             unobservable_remote_params=["cameraMotion", "negativePrompt"])
                self._save(value)
            except (HTTPException, OSError, ValueError) as error:
                raise AdapterError("OUTPUT_TRANSFER_OR_STORAGE_FAILED") from None
            finally:
                pending.unlink(missing_ok=True)
            return value

    def import_to_product(self, request_id, service):
        """Use the existing import API; carry original evidence through project Export."""
        self.preflight()
        with self.lease(request_id):
            value = self.get(request_id)
            if value["state"] == "IMPORTED_TECHNICAL_ONLY":
                if value["product_job_id"] not in service.records:
                    raise AdapterError("IMPORTED_PRODUCT_RECORD_MISSING")
                return service.records[value["product_job_id"]]
            if value["state"] != "COLLECTED_TECHNICAL_ONLY":
                raise AdapterError("COLLECT_BEFORE_IMPORT")
            self._input_check(value)
            source = Path(value["output"]["path"])
            if digest(source) != value["output"]["sha256"]:
                raise AdapterError("COLLECTED_OUTPUT_CHANGED")
            # A durable intent prevents duplicate imports if process termination occurs.
            value["state"] = "IMPORT_REVIEW_REQUIRED"
            self._save(value)
            content = source.read_bytes()
            if hashlib.sha256(content).hexdigest() != value["output"]["sha256"]:
                raise AdapterError("COLLECTED_OUTPUT_CHANGED")
            record = service.import_media({"kind": "video", "filename": "ltx_" + value["request_id"] + ".mp4",
                                           "content_base64": base64.b64encode(content).decode()})
            folder = service.jobs / record["job_id"]
            receipt = folder / "GENERATION_SOURCE_RECEIPT.json"
            receipt.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            record["reference_artifacts"] = [{"path": str(receipt), "file_name": receipt.name,
                                                "bytes": receipt.stat().st_size, "sha256": digest(receipt)}]
            record["generation_provenance"] = {"adapter_id": "ltx-desktop-remote-i2v-v1.3.1", "request_id": value["request_id"],
                "provider_job_id": value["provider_job_id"], "provider_generation_claim": True,
                "model_inference_verified": False, "review_scope": value["review_scope"], "full_product_pass": False}
            record["command"] = value["command"]
            pending = folder / "JOB_EVIDENCE.pending"
            pending.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(pending, folder / "JOB_EVIDENCE.json")
            service.records[record["job_id"]] = record
            value.update(state="IMPORTED_TECHNICAL_ONLY", product_job_id=record["job_id"])
            self._save(value)
            return record
