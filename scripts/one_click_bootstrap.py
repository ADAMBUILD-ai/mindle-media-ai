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
VC_REDIST_URL = "https://aka.ms/vc14/vc_redist.x64.exe"
VC_RUNTIME_REQUIRED = ("msvcp140.dll",)


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



def _vc_missing() -> list[str]:
    system_root = Path(os.environ.get("SystemRoot", r"C:\Windows"))
    system32 = system_root / "System32"
    return [name for name in VC_RUNTIME_REQUIRED if not (system32 / name).is_file()]


def ensure_vc_runtime(local: Path) -> dict:
    """Use host VC runtime when present; otherwise install only from Microsoft's signed URL."""
    missing = _vc_missing()
    receipt_dir = local / "prerequisites"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / "VC_RUNTIME_INSTALL_RESULT.json"
    if not missing:
        record = {
            "status": "HOST_VC_RUNTIME_PRESENT",
            "source": "Windows System32",
            "missing_before": [],
            "download_performed": False,
            "system32_copy_performed": False,
        }
        receipt_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return record

    powershell = shutil.which("powershell.exe") or shutil.which("pwsh.exe")
    if not powershell:
        raise RuntimeError("Microsoft Visual C++ Runtime 자동 준비를 위한 PowerShell을 찾을 수 없습니다.")

    installer = receipt_dir / "vc_redist.x64.exe"
    script_path = receipt_dir / "install_vc_runtime.ps1"
    installer_ps = str(installer).replace("'", "''")
    receipt_ps = str(receipt_path).replace("'", "''")
    script = f"""$ErrorActionPreference='Stop'
$Url='{VC_REDIST_URL}'
$Installer='{installer_ps}'
$Receipt='{receipt_ps}'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -UseBasicParsing -Uri $Url -OutFile $Installer
$Sig=Get-AuthenticodeSignature -LiteralPath $Installer
if ($Sig.Status -ne 'Valid' -or $Sig.SignerCertificate.Subject -notmatch '(^|,\\s*)O=Microsoft Corporation(,|$)') {{
  throw 'Microsoft Visual C++ Redistributable signature verification failed'
}}
$Sha=(Get-FileHash -LiteralPath $Installer -Algorithm SHA256).Hash.ToLower()
$Proc=Start-Process -FilePath $Installer -ArgumentList '/install','/quiet','/norestart' -Verb RunAs -Wait -PassThru
$Ok=$Proc.ExitCode -in @(0,1638,3010)
[ordered]@{{
  status=if($Ok){{'OFFICIAL_VC_RUNTIME_INSTALLER_COMPLETED'}}else{{'FAILED'}}
  source_url=$Url
  sha256=$Sha
  signature=[string]$Sig.Status
  publisher=$Sig.SignerCertificate.Subject
  exit_code=$Proc.ExitCode
  reboot_required=($Proc.ExitCode -eq 3010)
  system32_copy_performed=$false
}} | ConvertTo-Json | Set-Content -LiteralPath $Receipt -Encoding UTF8
if (-not $Ok) {{ exit $Proc.ExitCode }}
"""
    script_path.write_text(script, encoding="utf-8-sig")
    completed = subprocess.run(
        [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
        cwd=receipt_dir,
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Microsoft Visual C++ Runtime 자동 설치가 실패했습니다. "
            + (completed.stderr[-1200:] or completed.stdout[-1200:])
        )
    missing_after = _vc_missing()
    if missing_after:
        raise RuntimeError(
            "Microsoft Visual C++ Runtime 설치 후에도 필수 파일이 확인되지 않습니다: "
            + ", ".join(missing_after)
        )
    try:
        record = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception:
        record = {"status": "OFFICIAL_VC_RUNTIME_INSTALLER_COMPLETED"}
    record["missing_before"] = missing
    record["missing_after"] = missing_after
    record["automatic_first_run"] = True
    record["system32_copy_performed"] = False
    receipt_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


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

    # Keep normal employee operation one-click. If the host lacks the single
    # Microsoft C++ runtime dependency, fetch Microsoft's signed redistributable
    # and install it automatically instead of asking the employee to repair DLLs.
    ensure_vc_runtime(local)

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
