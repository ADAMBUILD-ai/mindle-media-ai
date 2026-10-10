"""Employee-visible one-click bootstrap for MINDLE MEDIA AI.

The executable built from this file is the only normal launch action. It
materializes the reviewed payload under LOCALAPPDATA, verifies the payload,
then starts the package-local Python launcher. It never searches for Git,
system Python, pip, or developer worktrees.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

APP_DIR = "MINDLE_MEDIA_AI"
READY_FILE = ".mindle_runtime_ready.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def distribution_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def verify_payload(root: Path, manifest: dict) -> None:
    root = Path(root).resolve()
    for entry in manifest.get("files", []):
        relative = entry["path"]
        path = (root / relative).resolve()
        if root != path and root not in path.parents:
            raise RuntimeError("패키지 경로가 올바르지 않습니다: " + relative)
        if not path.is_file():
            raise RuntimeError("패키지 파일이 없습니다: " + relative)
        if path.stat().st_size != int(entry["bytes"]):
            raise RuntimeError("패키지 파일 크기 검증 실패: " + relative)
        if sha256(path) != entry["sha256"]:
            raise RuntimeError("패키지 파일 해시 검증 실패: " + relative)


class DeployLock:
    def __init__(self, path: Path, timeout: float = 120.0):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = path.open("a+b")
        if path.stat().st_size == 0:
            self.handle.write(b"0")
            self.handle.flush()
        deadline = time.monotonic() + timeout
        while True:
            try:
                self.handle.seek(0)
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    self.handle.close()
                    raise RuntimeError("제품 준비 작업이 이미 진행 중입니다. 잠시 후 다시 실행하세요.")
                time.sleep(0.25)

    def close(self) -> None:
        try:
            self.handle.seek(0)
            msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            self.handle.close()


def materialize(source: Path, manifest: dict, manifest_sha: str, target: Path) -> None:
    ready = target / READY_FILE
    if target.is_dir() and ready.is_file():
        try:
            record = json.loads(ready.read_text(encoding="utf-8"))
        except Exception:
            record = {}
        if record.get("package_manifest_sha256") == manifest_sha:
            return

    verify_payload(source, manifest)
    staging = target.parent / f".{target.name}.staging-{os.getpid()}"
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)
    shutil.copytree(source, staging)
    verify_payload(staging, manifest)
    (staging / READY_FILE).write_text(
        json.dumps(
            {
                "package_manifest_sha256": manifest_sha,
                "runtime_id": manifest.get("runtime_id"),
                "build_commit": manifest.get("build_commit"),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if target.exists():
        shutil.rmtree(target)
    os.replace(staging, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-browser", action="store_true", help="CI verification mode")
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args()

    dist = distribution_root()
    payload = dist / "_payload"
    manifest_path = payload / "PACKAGE_MANIFEST.json"
    if not manifest_path.is_file():
        raise RuntimeError("MINDLE MEDIA AI 실행 패키지의 내부 payload를 찾을 수 없습니다.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("distribution") != "EMPLOYEE_WIN_X64":
        raise RuntimeError("직원용 Windows 패키지 정보가 올바르지 않습니다.")
    manifest_sha = sha256(manifest_path)
    runtime_id = str(manifest.get("runtime_id") or manifest_sha[:24])

    local = Path(os.environ["LOCALAPPDATA"]) / APP_DIR
    target = local / "runtime" / runtime_id
    target.parent.mkdir(parents=True, exist_ok=True)

    lock = DeployLock(local / "deploy.lock")
    try:
        materialize(payload, manifest, manifest_sha, target)
    finally:
        lock.close()

    print(f"MINDLE_RUNTIME_READY {target}")
    if args.materialize_only:
        return 0

    pythonw = target / "runtime" / "python" / "pythonw.exe"
    python = target / "runtime" / "python" / "python.exe"
    launcher = target / "app" / "launcher" / "employee_package_launcher.py"
    executable = python if args.no_browser else pythonw
    if not executable.is_file() or not launcher.is_file():
        raise RuntimeError("패키지 내부 실행 파일이 누락되었습니다.")

    command = [str(executable), str(launcher)]
    if args.no_browser:
        command.append("--no-browser")
        completed = subprocess.run(command, cwd=target, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"제품 실행 확인 실패: exit={completed.returncode}")
        return completed.returncode

    subprocess.Popen(
        command,
        cwd=target,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        close_fds=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        if os.name == "nt":
            ctypes.windll.user32.MessageBoxW(None, str(error), "MINDLE MEDIA AI", 0x10)
        raise
