"""Browser-driven product E2E: approved UI -> API -> verified CPU model -> preview -> save/export."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from media_ai.product_runtime import PRIVATE_REPO, sha256_file
from media_ai.product_server import create_server


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "product_e2e_evidence"
DATA = WORK / "product_data"
INPUTS = WORK / "inputs"
LOGS = WORK / "logs"
PRIOR = ROOT / "evidence/model_scout/VERIFIED_ADAPTER_RUNTIME_20260920.json"
PRIOR_BYTES = 17_375
PRIOR_SHA = "f75ed10af08456215c00d920e480e2bdbb096d0659c6d7bbabcf5529df7e7bf1"
UI_ASSET = ROOT / "ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png"
FLEURS_REPO = "google/fleurs"
FLEURS_REVISION = "70bb2e84b976b7e960aa89f1c648e09c59f894dd"
FLEURS_PARQUET = "parquet-data/ko_kr/test-00000-of-00001.parquet"
VIDEO_URL = "https://raw.githubusercontent.com/opencv/opencv_extra/9c5eefa1ef66cbeecc9a3d38e1c5308c22ebe830/testdata/highgui/video/big_buck_bunny.mp4"
VIDEO_SHA = "4e28622467284da93f7575189c84f0e762b170bb7cf19667ca52929f93dcc238"


def now() -> str: return datetime.now(timezone.utc).isoformat()
def record(path: Path) -> dict: return {"file_name": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path), "path": str(path)}


def assert_baselines() -> dict:
    if not PRIOR.is_file() or PRIOR.stat().st_size != PRIOR_BYTES or sha256_file(PRIOR) != PRIOR_SHA: raise RuntimeError("immutable SAM/Whisper evidence changed")
    evidence = json.loads(PRIOR.read_text(encoding="utf-8"))
    if evidence["promotion"].get("sam21") != "TESTED_PASS" or evidence["promotion"].get("whisper") != "TESTED_PASS": raise RuntimeError("SAM/Whisper TESTED_PASS baseline unavailable")
    final = json.loads((ROOT / "evidence/model_scout/FINAL_THREE_MODEL_RUNTIME_EVIDENCE_20260920.json").read_text(encoding="utf-8"))
    if final["promotion"].get("realesrgan") != "TESTED_PASS": raise RuntimeError("RealESRGAN TESTED_PASS baseline unavailable")
    if not UI_ASSET.is_file(): raise RuntimeError("approved UI source asset is unavailable")
    return {"sam_whisper_evidence": {"path": str(PRIOR.relative_to(ROOT)), "bytes": PRIOR_BYTES, "sha256": PRIOR_SHA, "unchanged": True}, "final_three_model_evidence": {"path": "evidence/model_scout/FINAL_THREE_MODEL_RUNTIME_EVIDENCE_20260920.json", "sha256": sha256_file(ROOT / "evidence/model_scout/FINAL_THREE_MODEL_RUNTIME_EVIDENCE_20260920.json")}, "approved_ui_asset": {"path": str(UI_ASSET.relative_to(ROOT)), "sha256": sha256_file(UI_ASSET), "bytes": UI_ASSET.stat().st_size}}


def inputs() -> dict:
    import pyarrow.parquet as pq
    INPUTS.mkdir(parents=True, exist_ok=True)
    photo = INPUTS / "intel_sisr_1032_street_480x270.png"; photo.write_bytes(requests.get("https://raw.githubusercontent.com/openvinotoolkit/open_model_zoo/a6946b6d6ce42cbf4278df20275fab199655fc7d/models/intel/single-image-super-resolution-1032/assets/street_480x270.png", timeout=90).content)
    if sha256_file(photo) != "8ecec108e674b51d36d5323dc2f99240a55913b87003aeb754307da8553edb6f": raise RuntimeError("pinned Intel product photo SHA-256 changed")
    video = INPUTS / "big_buck_bunny.mp4"; video.write_bytes(requests.get(VIDEO_URL, timeout=90).content)
    if sha256_file(video) != VIDEO_SHA: raise RuntimeError("pinned video SHA-256 changed")
    parquet = Path(hf_hub_download(repo_id=FLEURS_REPO, repo_type="dataset", filename=FLEURS_PARQUET, revision=FLEURS_REVISION, local_dir=str(INPUTS / "fleurs")))
    row = next(pq.ParquetFile(parquet).iter_batches(batch_size=1, columns=["audio", "transcription"])).to_pylist()[0]
    audio = INPUTS / "fleurs_ko_kr_test_row0.wav"; audio.write_bytes(row["audio"]["bytes"])
    if not row["transcription"].strip(): raise RuntimeError("Korean test transcript is unavailable")
    return {"photo": record(photo) | {"license": "CC BY-SA 4.0"}, "video": record(video) | {"source_revision": "9c5eefa1ef66cbeecc9a3d38e1c5308c22ebe830", "license": "CC BY 3.0"}, "audio": record(audio) | {"source_revision": FLEURS_REVISION, "license": "CC-BY-4.0", "reference": row["transcription"]}}


def wait_preview(driver, editor, expected: str, previous_job_id: str | None = None):
    host = editor.find_element(By.CSS_SELECTOR, "[data-preview]")
    WebDriverWait(driver, 300).until(
        lambda _: host.get_attribute("data-preview-status") == "actual-output"
        and host.get_attribute("data-job-id") != previous_job_id
    )
    element = host.find_element(By.CSS_SELECTOR, ":scope > *")
    if element.tag_name != expected: raise RuntimeError(f"preview type mismatch: expected {expected}, got {element.tag_name}")
    return {"tag": element.tag_name, "job_id": element.get_attribute("data-job-id"), "output_sha256": element.get_attribute("data-output-sha256"), "text": element.text}


def browser_e2e(base_url: str, values: dict) -> dict:
    download = WORK / "downloads"; download.mkdir(exist_ok=True)
    options = Options(); options.add_argument("--headless=new"); options.add_argument("--no-sandbox"); options.add_argument("--disable-dev-shm-usage"); options.add_experimental_option("prefs", {"download.default_directory": str(download), "download.prompt_for_download": False})
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(1600, 1100); driver.get(base_url)
        photo = driver.find_element(By.CSS_SELECTOR, '[data-editor="photo"]'); video = driver.find_element(By.CSS_SELECTOR, '[data-editor="video"]')
        photo.find_element(By.CSS_SELECTOR, '[data-primary-input="photo"]').send_keys(values["photo"]["path"])
        pc = photo.find_element(By.CSS_SELECTOR, '[data-command="photo"]'); pc.send_keys("왼쪽 인물을 실제로 분할해줘", Keys.ENTER)
        photo_segment = wait_preview(driver, photo, "img")
        pc.send_keys("사진을 실제 4배 업스케일해줘", Keys.ENTER)
        photo_upscale = wait_preview(driver, photo, "img", photo_segment["job_id"])
        video.find_element(By.CSS_SELECTOR, '[data-primary-input="video"]').send_keys(values["video"]["path"])
        vc = video.find_element(By.CSS_SELECTOR, '[data-command="video"]'); vc.send_keys("대상을 실제 추적해줘", Keys.ENTER)
        video_tracking = wait_preview(driver, video, "video")
        video.find_element(By.CSS_SELECTOR, '[data-primary-input="video"]').send_keys(values["audio"]["path"])
        vc.send_keys("한국어 음성을 실제 텍스트로 변환해줘", Keys.ENTER)
        whisper = wait_preview(driver, video, "pre", video_tracking["job_id"])
        if not whisper["text"].strip(): raise RuntimeError("empty transcript displayed in UI")
        photo.find_element(By.CSS_SELECTOR, '[data-action="save"]').click(); WebDriverWait(driver, 30).until(lambda _: photo.get_attribute("data-project-status") == "saved")
        photo.find_element(By.CSS_SELECTOR, '[data-action="export"]').click(); WebDriverWait(driver, 30).until(lambda _: photo.get_attribute("data-export-status") == "exported")
        driver.save_screenshot(str(LOGS / "approved_ui_e2e.png"))
        return {"photo_segment_preview": photo_segment, "photo_upscale_preview": photo_upscale, "video_tracking_preview": video_tracking, "whisper_preview": whisper, "project_status": photo.get_attribute("data-project-status"), "export_status": photo.get_attribute("data-export-status"), "export_sha256": photo.get_attribute("data-export-sha256"), "screenshot": record(LOGS / "approved_ui_e2e.png")}
    finally:
        driver.quit()


def preserve_private(token: str, evidence_path: Path) -> dict:
    api = HfApi(token=token); prefix = f"PRODUCT_E2E_EVIDENCE/{os.environ.get('GITHUB_RUN_ID', 'local')}"
    operations = []
    for path in sorted(WORK.rglob("*")):
        relative = path.relative_to(WORK)
        if not path.is_file() or ".cache" in relative.parts or relative.parts[:2] == ("inputs", "fleurs"):
            continue
        if "verified_model_cache" not in path.parts and "realesrgan-extracted" not in path.parts:
            operations.append(CommitOperationAdd(path_in_repo=f"{prefix}/{relative.as_posix()}", path_or_fileobj=str(path)))
    commit = api.create_commit(repo_id=PRIVATE_REPO, repo_type="model", operations=operations, commit_message=f"Preserve MINDLE MEDIA AI product E2E Evidence for run {os.environ.get('GITHUB_RUN_ID', 'local')}", token=token)
    return {"private_repo_id": PRIVATE_REPO, "path": prefix, "payload_revision": commit.oid}


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token: raise RuntimeError("HF_TOKEN is unavailable")
    if os.environ.get("CUDA_VISIBLE_DEVICES") not in {"", None}: raise RuntimeError("CPU-only execution requires CUDA_VISIBLE_DEVICES empty")
    for directory in (WORK, DATA, INPUTS, LOGS): directory.mkdir(parents=True, exist_ok=True)
    baseline = assert_baselines(); fixture = inputs()
    server = create_server(ROOT, DATA, token, 0); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        ui = browser_e2e(f"http://127.0.0.1:{server.server_port}", fixture)
        response = requests.get(f"http://127.0.0.1:{server.server_port}/api/evidence", timeout=30); response.raise_for_status(); api_evidence = response.json()
    finally:
        server.shutdown(); thread.join(timeout=30); server.server_close()
    models = {item["operation"]: item for item in api_evidence["jobs"].values()}
    required = {"segment", "upscale", "tracking", "transcribe"}
    if set(models) != required or any(item["status"] != "TESTED_PASS" for item in models.values()): raise RuntimeError("not every real product job reached TESTED_PASS")
    evidence = {"schema_version": "1.0", "captured_at": now(), "status": "FINAL_PASS", "scope": "APPROVED_UI_REAL_BACKEND_CPU_E2E", "UI_SSOT_CHANGED": "NO", "production_changed": False, "github": {"repository": os.environ.get("GITHUB_REPOSITORY"), "source_commit": os.environ.get("GITHUB_SHA"), "run_id": os.environ.get("GITHUB_RUN_ID"), "pull_request": 10}, "execution_environment": {"provider": "GitHub Actions public standard hosted runner", "hardware": "CPU", "gpu_used": False, "paid_compute": False, "platform": platform.platform(), "python": platform.python_version()}, "immutable_baseline": baseline, "actual_inputs": fixture, "backend_jobs": models, "ui_preview": ui, "save_export": {"project_status": ui["project_status"], "export_status": ui["export_status"], "export_sha256": ui["export_sha256"]}, "server_requests": api_evidence["requests"]}
    path = WORK / "PRODUCT_E2E_EVIDENCE.json"; path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence["persistence"] = preserve_private(token, path)
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if sha256_file(PRIOR) != PRIOR_SHA: raise RuntimeError("immutable SAM/Whisper evidence changed after E2E")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
