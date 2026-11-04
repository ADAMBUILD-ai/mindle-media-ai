"""Real loopback HTTP and FFmpeg tests. The server is NOT an AI model."""
from contextlib import contextmanager
import copy
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
from uuid import uuid4
import zipfile

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ltx_test_adapter", ROOT / "external_assets/media-production/ltx_remote_adapter.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
PARAMS = {"prompt": "건물 형태를 유지하며 천천히 이동", "model": "ltx-2.5-fast", "resolution": "540p", "duration": 5, "fps": 24,
          "aspectRatio": "16:9", "seed": 7}


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("real FFmpeg is required")
    path = tmp_path_factory.mktemp("ltx-non-ai-fixture") / "fixture.mp4"
    subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=960x540:r=24:d=5",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True, timeout=30)
    return path


@contextmanager
def engine(clip):
    class FakeEngine:
        posts = 0
        uploads = 0
        cancels = 0
        urls = []
        response = None
        mode = "ok"
        video = clip.read_bytes()
        generation = None
        unauthorized = False

    state = FakeEngine()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, data, code=200, kind="application/json", declared=None):
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data) if declared is None else declared))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            state.urls.append(self.path)
            if state.unauthorized or self.headers.get("Authorization") != "Bearer test-session-secret":
                self.send(b"{}", 401)
            elif self.path == "/api/session":
                self.send(b'{"status":"ok"}')
            elif self.path == "/api/generate/models-specs":
                spec = {"capabilities": {"i2v": True}, "supported_resolutions_durations": {"540p": {"fps_to_durations": {"24": [5]}, "aspect_ratios": ["16:9"]}}}
                self.send(json.dumps({"active_offering": "ltx-2.5-fast", "budgetMode": "standard", "local_models": [{"pipeline": "fast", "spec": spec}],
                    "downloaded_local_models": [{"model": "ltx-2.5-fast", "pipeline": "fast", "spec": spec}], "api_models": []}).encode())
            elif self.path.startswith("/api/generations/"):
                self.send(json.dumps(state.generation).encode())
            elif self.path == "/api/assets/video-1":
                url = "/api/assets/video-1/bytes?sig=test-signed-secret"
                if state.mode == "foreign_url":
                    url = "http://192.0.2.1:41955/api/assets/video-1/bytes?sig=test-signed-secret"
                self.send(json.dumps({"id": "video-1", "media_kind": "video", "bytes_url": url}).encode())
            elif self.path.startswith("/api/assets/video-1/bytes"):
                if state.mode == "expired":
                    self.send(b"{}", 403)
                elif state.mode == "redirect":
                    self.send_response(302)
                    self.send_header("Location", "http://192.0.2.1:41955/leak")
                    self.end_headers()
                elif state.mode == "truncated":
                    self.send(state.video[:100], kind="video/mp4", declared=len(state.video))
                    self.close_connection = True
                else:
                    self.send(state.video, kind="video/mp4")
            else:
                self.send(b"{}", 404)

        def do_POST(self):
            state.urls.append(self.path)
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if self.path == "/api/assets/upload":
                state.uploads += 1
                assert b'filename="reference.png"' in body and b"\x89PNG" in body
                self.send(b'{"id":"image-1","media_kind":"image"}')
            elif self.path == "/api/generations/image-to-video":
                state.posts += 1
                payload = json.loads(body)
                # Match the upstream Remote DTO projection: private camera/negative params omitted.
                state.generation = {"id": "generation-1", "feature": "image-to-video", "contract_version": 1,
                    "status": "succeeded", "spec": {"params": {k: v for k, v in payload["params"].items() if k in m.PARAMS},
                    "inputs": payload["inputs"]}, "outputs": [{"id": "video-1", "media_kind": "video", "bytes_url": "/api/assets/video-1/bytes?sig=test-signed-secret"}]}
                if state.response:
                    state.response(state.generation)
                if state.mode == "lost_post":
                    self.close_connection = True
                    self.connection.shutdown(socket.SHUT_RDWR)
                    return
                self.send(json.dumps(state.generation).encode())
            elif self.path.endswith("/cancel"):
                state.cancels += 1
                state.generation["status"] = "cancelling"
                self.send(json.dumps(state.generation).encode())
            else:
                self.send(b"{}", 404)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port), state
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def setup(tmp_path, clip):
    with engine(clip) as (base, state):
        image = tmp_path / "building.png"
        Image.new("RGB", (64, 64), "white").save(image)
        config = {"upstream_revision": m.UPSTREAM, "base_url": base, "execution_approved": True, "approval_id": "CONTRACT-TEST-NOT-MODEL-APPROVAL",
                  "review_scope": "contract_test", "license_reviewed": True, "offline_reviewed": True, "allowed_params": [PARAMS],
                  "output_dimensions": {m.object_hash(PARAMS): [960, 540]}, "identity_files": []}
        for role in ("application", "runtime", "model", "settings", "ffmpeg", "ffprobe"):
            path = Path(shutil.which(role)) if role in {"ffmpeg", "ffprobe"} else tmp_path / (role + ".test-identity")
            if role not in {"ffmpeg", "ffprobe"}:
                path.write_text("CONTRACT TEST IDENTITY ONLY " + role)
            if role == "settings":
                path.write_text(json.dumps({"use_local_text_encoder": True, "prompt_enhancer_enabled": False,
                    "explore_auto_enhance_prompts": False, "user_prefers_ltx_api_video_generations": False,
                    "assistant_provider": "local", "budget_mode": "standard"}))
            config["identity_files"].append({"role": role, "path": str(path), "sha256": m.digest(path), "bytes": path.stat().st_size})
        adapter = m.LtxRemoteAdapter(tmp_path / "adapter", config, "test-session-secret")
        yield adapter, state, image, config
        adapter.close()


def submit(adapter, image, request_id=None):
    return adapter.submit(request_id or str(uuid4()), image, m.digest(image), "기준 건물 홍보 장면", copy.deepcopy(PARAMS))


def test_http_collection_product_save_reopen_export(setup, tmp_path, monkeypatch):
    from media_ai.product_runtime import ProductJobService
    monkeypatch.delenv("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", raising=False)
    a, state, image, _ = setup
    value = submit(a, image)
    request_id = value["request_id"]
    assert value["state"] == "PROVIDER_SUCCEEDED_UNVERIFIED"
    collected = a.collect(request_id)
    assert collected["technical_review"]["decoded"]
    assert collected["model_inference_verified"] is False
    service = ProductJobService(tmp_path / "product", "")
    record = a.import_to_product(request_id, service)
    assert record["runtime_result"]["model_inference"] is False
    assert record["generation_provenance"]["review_scope"] == "contract_test"
    saved = service.save_project({"job_ids": [record["job_id"]]})
    # New service loads the same persisted jobs; process restart is checked separately.
    reopened = ProductJobService(tmp_path / "product", "")
    assert reopened.records[record["job_id"]]["generation_provenance"] == record["generation_provenance"]
    exported = reopened.export_project(saved["project_id"])
    with zipfile.ZipFile(exported["export"]["path"]) as z:
        assert z.testzip() is None
        manifest = json.loads(z.read("BUNDLE_MANIFEST.json"))
        assert any(x["role"] == "reference" for x in manifest["files"])
        for item in manifest["files"]:
            assert hashlib.sha256(z.read(item["archive_path"])).hexdigest() == item["sha256"]
        receipt_name = next(x for x in z.namelist() if x.endswith("GENERATION_SOURCE_RECEIPT.json"))
        receipt = z.read(receipt_name)
        assert b"test-session-secret" not in receipt and b"test-signed-secret" not in receipt
        assert json.loads(receipt)["full_product_pass"] is False
    assert state.posts == state.uploads == 1
    assert a.import_to_product(request_id, reopened)["job_id"] == record["job_id"]


def test_duplicate_and_changed_request(setup):
    a, state, image, _ = setup
    first = submit(a, image)
    assert submit(a, image, first["request_id"])["provider_job_id"] == "generation-1"
    with pytest.raises(m.AdapterError, match="DIFFERENT_INPUT"):
        a.submit(first["request_id"], image, m.digest(image), "다른 원고", PARAMS)
    assert state.posts == state.uploads == 1


def test_lost_post_never_retried_after_adapter_restart(setup):
    a, state, image, config = setup
    state.mode = "lost_post"
    request_id = str(uuid4())
    with pytest.raises(m.AdapterError, match="TRANSPORT"):
        submit(a, image, request_id)
    assert a.get(request_id)["state"] == "SUBMISSION_UNKNOWN"
    b = m.LtxRemoteAdapter(a.root, config, "test-session-secret")
    try:
        assert submit(b, image, request_id)["state"] == "SUBMISSION_UNKNOWN"
    finally:
        b.close()
    assert state.posts == 1


@pytest.mark.parametrize("field,wrong", [("prompt", "다른 원고"), ("duration", 10), ("aspectRatio", "9:16"), ("model", "other"), ("seed", 8), ("fps", 30), ("resolution", "720p")])
def test_changed_provider_plan_rejected(setup, field, wrong):
    a, state, image, _ = setup
    state.response = lambda v: v["spec"]["params"].update({field: wrong})
    request_id = str(uuid4())
    with pytest.raises(m.AdapterError, match="PLAN_MISMATCH"):
        submit(a, image, request_id)
    assert a.get(request_id)["state"] == "BLOCKED_PROVIDER_CONTRACT"
    assert not list(a.root.glob("*.mp4"))


@pytest.mark.parametrize("status", ["failed", "cancelled", "mystery"])
def test_no_output_on_non_success(setup, status):
    a, state, image, _ = setup
    state.response = lambda v: v.update(status=status, error_code="CUDA_OOM")
    request_id = str(uuid4())
    if status == "mystery":
        with pytest.raises(m.AdapterError, match="UNKNOWN_PROVIDER_STATE"):
            submit(a, image, request_id)
    else:
        submit(a, image, request_id)
    with pytest.raises(m.AdapterError):
        a.collect(request_id)
    assert not list(a.root.glob("*.mp4"))


@pytest.mark.parametrize("mode", ["foreign_url", "expired", "redirect", "truncated", "bad_video"])
def test_failed_download_preserves_old_project_and_no_publication(setup, mode):
    a, state, image, _ = setup
    value = submit(a, image)
    state.mode = mode
    if mode == "bad_video":
        state.video = b"not a video"
    old = a.root / "existing-project.json"
    old.write_bytes(b"preserve me")
    with pytest.raises((m.AdapterError, OSError)):
        a.collect(value["request_id"])
    assert old.read_bytes() == b"preserve me"
    assert not list(a.root.glob("*.mp4")) and not list(a.root.glob("*.download"))
    assert a.get(value["request_id"])["state"] == "PROVIDER_SUCCEEDED_UNVERIFIED"


def test_cancel_ack_is_not_cancellation_completion(setup):
    a, state, image, _ = setup
    state.response = lambda v: v.update(status="running", outputs=[])
    value = submit(a, image)
    assert a.cancel(value["request_id"])["state"] == "CANCELLING"
    assert a.cancel(value["request_id"])["state"] == "CANCELLING"
    assert state.cancels == 1
    state.generation["status"] = "cancelled"
    assert a.poll(value["request_id"])["state"] == "CANCELLED"


def test_input_and_identity_drift_block_before_network(setup):
    a, state, image, config = setup
    image.write_bytes(b"changed")
    with pytest.raises(m.AdapterError, match="INPUT_CHANGED"):
        a.submit(str(uuid4()), image, "0" * 64, "원고", PARAMS)
    Path(config["identity_files"][0]["path"]).write_text("tampered")
    with pytest.raises(m.AdapterError, match="IDENTITY_CHANGED"):
        submit(a, image)
    assert state.posts == state.uploads == 0


def test_approval_and_no_token_fail_closed(setup):
    a, state, image, config = setup
    c = copy.deepcopy(config)
    c["execution_approved"] = False
    b = m.LtxRemoteAdapter(a.root / "blocked", c, "")
    try:
        with pytest.raises(m.AdapterError, match="APPROVAL"):
            submit(b, image)
    finally:
        b.close()
    a.token = ""
    with pytest.raises(m.AdapterError, match="SESSION_TOKEN_REQUIRED"):
        submit(a, image)
    assert not state.urls


def test_no_live_cli_action_without_execute(setup):
    a, _, _, _ = setup
    result = subprocess.run([sys.executable, str(ROOT / "scripts/run_ltx_source_evaluation.py"), "--config", "missing.json", "--root", str(a.root), "--action", "submit"],
                            capture_output=True, text=True)
    assert result.returncode == 2 and "require --execute" in result.stderr


def test_output_change_and_saved_request_change_rejected(setup):
    a, _, image, _ = setup
    value = submit(a, image)
    a.collect(value["request_id"])
    value = a.get(value["request_id"])
    Path(value["output"]["path"]).write_bytes(b"changed")
    with pytest.raises(m.AdapterError, match="OUTPUT_CHANGED"):
        a.collect(value["request_id"])
    value["params"]["prompt"] = "forged"
    a._save(value)
    with pytest.raises(m.AdapterError, match="BINDING_CHANGED"):
        a.poll(value["request_id"])


def test_real_process_restart_reopens_exports_with_source_receipt(setup, tmp_path):
    a, state, image, config = setup
    value = submit(a, image)
    a.collect(value["request_id"])
    config_path = tmp_path / "approved-contract-test.json"
    config_path.write_text(json.dumps(config))
    product = tmp_path / "cold-product"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "HF_HUB_OFFLINE": "1", "MINDLE_LTX_DEVICE_SESSION": "test-session-secret"}
    env.pop("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", None)
    first_code = '''
import importlib.util,json,os,sys
from pathlib import Path
from media_ai.product_runtime import ProductJobService
s=importlib.util.spec_from_file_location('adapter',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
a=m.LtxRemoteAdapter(Path(sys.argv[2]),json.loads(Path(sys.argv[3]).read_text()),os.environ['MINDLE_LTX_DEVICE_SESSION'])
p=ProductJobService(Path(sys.argv[4]),'');r=a.import_to_product(sys.argv[5],p);v=p.save_project({'job_ids':[r['job_id']]})
print(json.dumps({'pid':os.getpid(),'job_id':r['job_id'],'project_id':v['project_id']}));a.close()
'''
    first = subprocess.run([sys.executable, "-c", first_code, str(ROOT / "external_assets/media-production/ltx_remote_adapter.py"),
                            str(a.root), str(config_path), str(product), value["request_id"]], env=env, check=True, capture_output=True, text=True, timeout=60)
    saved = json.loads(first.stdout)
    second_code = '''
import json,os,sys
from pathlib import Path
from media_ai.product_runtime import ProductJobService
p=ProductJobService(Path(sys.argv[1]),'');r=p.records[sys.argv[2]];v=p.export_project(sys.argv[3])
assert r['generation_provenance']['review_scope']=='contract_test'
print(json.dumps({'pid':os.getpid(),'job_id':r['job_id'],'project_id':sys.argv[3],'export':v['export']}))
'''
    second = subprocess.run([sys.executable, "-c", second_code, str(product), saved["job_id"], saved["project_id"]],
                            env=env, check=True, capture_output=True, text=True, timeout=60)
    reopened = json.loads(second.stdout)
    assert reopened["pid"] != saved["pid"] and reopened["job_id"] == saved["job_id"]
    evidence = {"scope": "SYNTHETIC_HTTP_CONTRACT_NOT_AI_INFERENCE", "full_product_pass": False,
                "first_process": saved, "second_process": reopened, "output": a.get(value["request_id"])["output"],
                "provider_post_count": state.posts, "model_inference_verified": False}
    if os.environ.get("MINDLE_LTX_CONTRACT_EVIDENCE"):
        out = Path(os.environ["MINDLE_LTX_CONTRACT_EVIDENCE"])
        out.mkdir(parents=True, exist_ok=True)
        (out / "SYNTHETIC_PROCESS_LIFECYCLE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")


def test_unauthorized_poll_does_not_promote_completed_state(setup):
    a, state, image, _ = setup
    state.response = lambda v: v.update(status="running", outputs=[])
    value = submit(a, image)
    state.unauthorized = True
    with pytest.raises(m.AdapterError, match="HTTP_401"):
        a.poll(value["request_id"])
    assert a.get(value["request_id"])["state"] == "RUNNING"
    assert state.posts == 1


def test_concurrent_submission_lock_and_config_binding(setup):
    a, state, image, config = setup
    request_id = str(uuid4())
    with a.lease(request_id):
        with pytest.raises(m.AdapterError, match="REQUEST_BUSY"):
            submit(a, image, request_id)
    submit(a, image, request_id)
    changed = copy.deepcopy(config)
    changed["approval_id"] = "OTHER-APPROVAL"
    b = m.LtxRemoteAdapter(a.root, changed, "test-session-secret")
    try:
        with pytest.raises(m.AdapterError, match="CONFIG_BINDING_CHANGED"):
            b.poll(request_id)
    finally:
        b.close()
    assert state.posts == 1


@pytest.mark.parametrize("field,bad", [("use_local_text_encoder", False), ("explore_auto_enhance_prompts", True), ("assistant_provider", "gemini"), ("gemini_api_key", "not-a-real-key")])
def test_nonlocal_settings_block_before_any_http(setup, field, bad):
    a, state, image, config = setup
    settings = next(x for x in config["identity_files"] if x["role"] == "settings")
    path = Path(settings["path"])
    content = json.loads(path.read_text())
    content[field] = bad
    path.write_text(json.dumps(content))
    settings.update(sha256=m.digest(path), bytes=path.stat().st_size)
    b = m.LtxRemoteAdapter(a.root / "blocked-settings", config, "test-session-secret")
    try:
        with pytest.raises(m.AdapterError, match="BLOCKED_"):
            submit(b, image)
    finally:
        b.close()
    assert not state.urls


def test_api_only_capability_is_not_accepted_as_local():
    with pytest.raises(m.AdapterError, match="LOCAL_MODEL"):
        m.LtxRemoteAdapter._capability_check({"active_offering": "ltx-2.5-fast", "budgetMode": "standard", "local_models": [],
            "downloaded_local_models": [], "api_models": [{"pipeline": "fast-2.5"}]}, PARAMS)
