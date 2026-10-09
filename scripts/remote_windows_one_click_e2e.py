"""Actual Windows package-runtime E2E for the one-click candidate.

Runs against the server started by MINDLE_MEDIA_AI_RUN.exe --no-browser.
Uses previously verified General Work fixtures, but executes the packaged
Windows runtime/models again and records fresh outputs/hashes.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import zipfile


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def request_json(url: str, payload: dict | None = None, timeout: int = 900) -> dict:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="GET" if payload is None else "POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code} {url}: {body}") from error


def post_file(base: str, path: str, lane: str, operation: str, command: str, source: Path) -> dict:
    return request_json(
        base + path,
        {
            "lane": lane,
            "operation": operation,
            "command": command,
            "filename": source.name,
            "content_base64": base64.b64encode(source.read_bytes()).decode("ascii"),
        },
    )


def locate(base_root: Path, name: str) -> Path:
    matches = list(base_root.rglob(name))
    if len(matches) != 1:
        raise RuntimeError(f"fixture {name!r} expected once, found {len(matches)}")
    return matches[0]


def find_server() -> tuple[str, dict]:
    deadline = time.monotonic() + 120
    last = None
    while time.monotonic() < deadline:
        for port in range(18768, 18778):
            try:
                base = f"http://127.0.0.1:{port}"
                identity = request_json(base + "/api/runtime-identity", timeout=2)
                if identity.get("runtime_mode") == "LOCAL_OFFLINE_PACKAGE":
                    return base, identity
            except Exception as error:
                last = error
        time.sleep(0.5)
    raise RuntimeError(f"packaged server not found: {last}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-root", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_root.mkdir(parents=True, exist_ok=True)

    base, identity = find_server()
    with urlopen(base + "/", timeout=15) as response:
        html = response.read().decode("utf-8", errors="replace")
    if "MINDLE MEDIA AI" not in html:
        raise RuntimeError("approved product title missing from packaged UI")

    segment_input = locate(args.fixture_root, "36b38c8b-2ebd-4c8e-b26d-6f70f016f5b1_intel_sisr_1032_street_480x270.png")
    upscale_input = locate(args.fixture_root, "f3b9b84a-f627-4ae5-b147-76ee8c1ef530_photo_overlay.png") if list(args.fixture_root.rglob("f3b9b84a-f627-4ae5-b147-76ee8c1ef530_photo_overlay.png")) else locate(args.fixture_root, "f3b9b84a-f627-4ae5-bd99-f3f5904ea466_photo_overlay.png")
    tracking_input = locate(args.fixture_root, "448197c5-ae84-421a-89a6-713b2880171e_big_buck_bunny.mp4")
    stt_input = locate(args.fixture_root, "49d9967a-4eb8-4626-9d30-9908913f5de3_fleurs_ko_kr_test_row0.wav")

    basic_photo = request_json(
        base + "/api/photo-edits",
        {
            "command": "Windows 패키지 기본 사진 보정",
            "content_base64": base64.b64encode(segment_input.read_bytes()).decode("ascii"),
            "options": {"brightness": 10},
        },
    )
    if basic_photo.get("status") != "TESTED_PASS":
        raise RuntimeError("basic photo edit did not pass")

    segment = post_file(base, "/api/jobs", "photo", "segment", "왼쪽 인물을 실제로 분할해줘", segment_input)
    upscale = post_file(base, "/api/jobs", "photo", "upscale", "사진을 실제 4배 업스케일해줘", upscale_input)
    tracking = post_file(base, "/api/jobs", "video", "tracking", "대상을 실제 추적해줘", tracking_input)
    transcript = post_file(base, "/api/jobs", "video", "transcribe", "한국어 음성을 실제 텍스트로 변환해줘", stt_input)

    for name, record in {
        "segment": segment,
        "upscale": upscale,
        "tracking": tracking,
        "transcribe": transcript,
    }.items():
        if record.get("status") != "TESTED_PASS":
            raise RuntimeError(f"{name} packaged inference did not pass: {record}")

    project = request_json(
        base + "/api/projects/save",
        {
            "job_ids": [
                basic_photo["job_id"],
                segment["job_id"],
                upscale["job_id"],
                tracking["job_id"],
                transcript["job_id"],
            ]
        },
    )
    if project.get("status") != "SAVED":
        raise RuntimeError("project save failed")
    project_id = project["project_id"]

    latest = request_json(base + "/api/projects/latest")
    if latest.get("project_id") != project_id:
        raise RuntimeError("saved project was not readable from runtime")

    exported = request_json(base + f"/api/projects/{project_id}/export", {})
    if exported.get("status") != "EXPORTED":
        raise RuntimeError("project export failed")
    export_path = Path(exported["export"]["path"])
    if not export_path.is_file():
        raise RuntimeError("export ZIP missing")
    with zipfile.ZipFile(export_path) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError("export ZIP CRC failure: " + bad)
        entries = archive.namelist()
        if "project.json" not in entries:
            raise RuntimeError("project.json missing from export")

    result = {
        "status": "REMOTE_WINDOWS_PACKAGED_RUNTIME_E2E_PASS",
        "base_url": base,
        "runtime_identity": identity,
        "ui_title": "MINDLE MEDIA AI",
        "jobs": {
            "basic_photo": basic_photo,
            "segment": segment,
            "upscale": upscale,
            "tracking": tracking,
            "transcribe": transcript,
        },
        "project_id": project_id,
        "latest_project": latest,
        "export": {
            **exported,
            "sha256": digest(export_path),
            "zip_crc": "PASS",
            "entry_count": len(entries),
        },
    }
    destination = args.evidence_root / "REMOTE_WINDOWS_RUNTIME_E2E.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "project_id": project_id, "export_sha256": result["export"]["sha256"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
