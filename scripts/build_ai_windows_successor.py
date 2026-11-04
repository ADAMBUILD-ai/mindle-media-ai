"""Create one source-only successor from the byte-verified TEST R2 package.

The Qwen, llama.cpp, Supertonic, sherpa-onnx, FFmpeg and Python runtime bytes
are copied from TEST R2 and verified before current product source is overlaid.
No model or engine is downloaded or rebuilt here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import zipfile

BASE_NAME = "MINDLE_MEDIA_AI_PC_TEST_20261024_R1"
BASE_SHA256 = "c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606"
BASE_MANIFEST_SHA256 = "2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07"
BASE_EXE_SHA256 = "701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5"
NAME = "MINDLE_MEDIA_AI_PC_TEST_20261024_R3"


def sha(path: Path) -> str:
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def stable(relative: Path) -> bool:
    return "__pycache__" not in relative.parts and relative.suffix.lower() not in {".pyc", ".pyo"} and not any(
        part.startswith(".") and part != ".f2py_f2cmap" for part in relative.parts
    )


def files(root: Path):
    return sorted((p for p in root.rglob("*") if p.is_file() and stable(p.relative_to(root))), key=lambda p: p.relative_to(root).as_posix())


def tree_sha(root: Path) -> str:
    return hashlib.sha256("\n".join(p.relative_to(root).as_posix() + ":" + sha(p) for p in files(root)).encode()).hexdigest()


def record(root: Path, path: Path) -> dict:
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_member(name: str) -> PurePosixPath:
    value = PurePosixPath(name)
    if value.is_absolute() or ".." in value.parts or "\\" in name or ":" in name:
        raise ValueError("unsafe archive member")
    return value


def verify_base(parts_root: Path, work: Path) -> Path:
    parts = sorted(parts_root.rglob("*.zip.part-*"))
    suffixes = [p.name.rsplit("-", 1)[-1] for p in parts]
    if suffixes != [f"{index:02d}" for index in range(7)]:
        raise RuntimeError(f"exact TEST R2 parts 00..06 required: {suffixes}")
    archive = work / "test-r2.zip"
    with archive.open("wb") as output:
        for part in parts:
            with part.open("rb") as source:
                shutil.copyfileobj(source, output, 1024 * 1024)
    if sha(archive) != BASE_SHA256:
        raise RuntimeError("TEST R2 archive identity mismatch")
    extracted = work / "extracted"
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("TEST R2 CRC failure")
        for item in bundle.infolist():
            safe_member(item.filename)
        manifest_bytes = bundle.read(BASE_NAME + "/_payload/PACKAGE_MANIFEST.json")
        if hashlib.sha256(manifest_bytes).hexdigest() != BASE_MANIFEST_SHA256:
            raise RuntimeError("TEST R2 manifest identity mismatch")
        if hashlib.sha256(bundle.read(BASE_NAME + "/MINDLE_MEDIA_AI_RUN.exe")).hexdigest() != BASE_EXE_SHA256:
            raise RuntimeError("TEST R2 launcher identity mismatch")
        manifest = json.loads(manifest_bytes)
        for item in manifest["files"]:
            digest=hashlib.sha256();length=0
            with bundle.open(BASE_NAME + "/_payload/" + item["path"]) as source:
                while body:=source.read(1024*1024):digest.update(body);length+=len(body)
            if length != item["bytes"] or digest.hexdigest() != item["sha256"]:
                raise RuntimeError("TEST R2 payload mismatch: " + item["path"])
        bundle.extractall(extracted)
    return extracted / BASE_NAME


def verify_engine_space(payload: Path) -> dict:
    settings = json.loads((payload / "RUNTIME_ENGINES.json").read_text(encoding="utf-8"))
    planner = settings["planner"]
    executable = payload / planner["executable"]
    model = payload / planner["model_path"]
    if sha(executable) != planner["executable_sha256"] or sha(model) != planner["model_sha256"]:
        raise RuntimeError("Qwen or llama.cpp identity mismatch")
    if tree_sha(executable.parent) != planner["runtime_sha256"]:
        raise RuntimeError("llama.cpp runtime tree mismatch")
    tts = settings["tts"]
    data = payload / tts["data_path"]
    library = payload / "runtime/site-packages/sherpa_onnx/lib"
    if tree_sha(data) != tts["data_sha256"] or tree_sha(library) != tts["runtime_sha256"]:
        raise RuntimeError("Supertonic or sherpa-onnx identity mismatch")
    return {
        "planner_model_id": planner["model_id"],
        "planner_model_sha256": planner["model_sha256"],
        "planner_executable_sha256": planner["executable_sha256"],
        "tts_engine": tts["engine"],
        "tts_data_sha256": tts["data_sha256"],
        "engine_bytes_reused": True,
    }


def assemble(args) -> None:
    repo = Path(args.repo).resolve()
    output = Path(args.output).resolve()
    evidence = Path(args.evidence).resolve()
    work = output.parent / "successor-work"
    if output.exists() or work.exists():
        raise RuntimeError("fresh successor output required")
    work.mkdir(parents=True)
    base = verify_base(Path(args.parts).resolve(), work)
    shutil.copytree(base, output)
    payload = output / "_payload"
    engine_receipt_before = verify_engine_space(payload)
    for folder in ("src", "ui", "external_assets"):
        target = payload / "app" / folder
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(repo / folder, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    shutil.copy2(repo / "scripts/employee_package_launcher.py", payload / "app/launcher/employee_package_launcher.py")
    engine_receipt_after = verify_engine_space(payload)
    if engine_receipt_before != engine_receipt_after:
        raise RuntimeError("verified engine space changed during source overlay")
    source = os.environ["GITHUB_SHA"]
    ui_fingerprint = tree_sha(payload / "app/ui")
    manifest_path = payload / "PACKAGE_MANIFEST.json"
    old = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest = {
        **old,
        "build_commit": source,
        "runtime_id": source[:12] + "-" + ui_fingerprint[:12] + "-ai-r3",
        "ui_fingerprint": ui_fingerprint,
        "data_directory_name": "MEDIA_AI_CANDIDATE_20261024_R3",
        "release_channel": "OWNER_DEVELOPMENT_VERIFICATION_NOT_FINAL_RELEASE",
        "package_version": "AI_WINDOWS_20261024_R3",
        "base_candidate_source": old["build_commit"],
        "base_candidate_sha256": BASE_SHA256,
        "approved_ui_exact_match": False,
        "native_windows_acceptance": "PENDING",
    }
    manifest["files"] = [record(payload, path) for path in files(payload) if path != manifest_path]
    write(manifest_path, manifest)
    delivery = {
        "source": source,
        "base_candidate_sha256": BASE_SHA256,
        "runtime_id": manifest["runtime_id"],
        "exe_sha256": sha(output / "MINDLE_MEDIA_AI_RUN.exe"),
        "manifest_sha256": sha(manifest_path),
        "files": len(manifest["files"]),
        "engine_space": engine_receipt_after,
        "office_pc_acceptance": False,
        "human_hearing": False,
        "full_product_pass": False,
    }
    write(output / "DELIVERY_MANIFEST.json", delivery)
    (output / "DELIVERY_ARTIFACT_SHA256.txt").write_text(
        delivery["exe_sha256"] + "  MINDLE_MEDIA_AI_RUN.exe\n" + delivery["manifest_sha256"] + "  _payload/PACKAGE_MANIFEST.json\n",
        encoding="ascii",
    )
    write(evidence / "SUCCESSOR_ASSEMBLY.json", delivery)
    shutil.rmtree(work)
    print("SUCCESSOR_ASSEMBLED", output, flush=True)


def make_starter(root: Path, parts: list[dict], archive_sha: str, exe_sha: str) -> Path:
    starter = root / "MINDLE_MEDIA_AI_START_20261024_R3.zip"
    ps = f"""$ErrorActionPreference='Stop'
$parts=Get-ChildItem -LiteralPath $env:MINDLE_PARTS_DIR -Filter '{NAME}.zip.part-*' | Sort-Object Name
if($parts.Count -ne {len(parts)}){{throw 'Missing candidate parts'}}
$homeDir=Join-Path $env:LOCALAPPDATA 'MINDLE\\PC_TEST_INSTALLS\\20261024_R3'
New-Item -ItemType Directory -Force -Path $homeDir | Out-Null
$archive=Join-Path $homeDir 'candidate.zip';$out=[IO.File]::Create($archive)
try{{foreach($p in $parts){{$input=[IO.File]::OpenRead($p.FullName);try{{$input.CopyTo($out)}}finally{{$input.Dispose()}}}}}}finally{{$out.Dispose()}}
if((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne '{archive_sha}'){{throw 'Candidate archive SHA mismatch'}}
& "$env:SystemRoot\\System32\\tar.exe" -xf $archive -C $homeDir
if($LASTEXITCODE -ne 0){{throw 'Extraction failed'}}
$folder=Join-Path $homeDir '{NAME}';$exe=Join-Path $folder 'MINDLE_MEDIA_AI_RUN.exe'
if((Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLower() -ne '{exe_sha}'){{throw 'Candidate EXE SHA mismatch'}}
$shell=New-Object -ComObject WScript.Shell;$link=$shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'MINDLE MEDIA AI TEST R3.lnk'))
$link.TargetPath=$exe;$link.WorkingDirectory=$folder;$link.IconLocation=$exe;$link.Save();Start-Process -FilePath $exe -WorkingDirectory $folder
"""
    cmd = "@echo off\r\nsetlocal\r\nset \"MINDLE_PARTS_DIR=%~dp0\"\r\npowershell.exe -NoProfile -Command \"& ([ScriptBlock]::Create([IO.File]::ReadAllText((Join-Path $env:MINDLE_PARTS_DIR 'INSTALL_COMMAND.txt'))))\"\r\nif errorlevel 1 echo Installation failed. Keep this window for PC Work.\r\npause\r\n"
    with zipfile.ZipFile(starter, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("START_MINDLE_MEDIA_AI.cmd", cmd.encode("ascii"))
        bundle.writestr("INSTALL_COMMAND.txt", ps.encode("utf-8-sig"))
        bundle.writestr("DELIVERY_PARTS.json", json.dumps({"sha256": archive_sha, "parts": parts}, indent=2))
        bundle.writestr("README_KO.txt", "모든 R3 part 파일과 이 ZIP을 같은 폴더에 두고 압축 해제 후 START_MINDLE_MEDIA_AI.cmd를 두 번 클릭하세요. 기존 설치·프로젝트는 보존됩니다. 원격 Windows PASS는 사무실 PC 청취와 최종 제품 승인을 대신하지 않습니다.")
    return starter


def seal(args) -> None:
    output = Path(args.output).resolve()
    evidence = Path(args.evidence).resolve()
    payload = output / "_payload"
    manifest = json.loads((payload / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = payload / item["path"]
        if path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
            raise RuntimeError("post-runtime payload changed: " + item["path"])
    archive = output.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as bundle:
        for path in files(output):
            bundle.write(path, NAME + "/" + path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("successor ZIP CRC failure")
    parts = []
    with archive.open("rb") as stream:
        index = 0
        while body := stream.read(500 * 1024 * 1024):
            path = archive.with_name(archive.name + f".part-{index:02d}")
            path.write_bytes(body)
            parts.append(record(archive.parent, path))
            index += 1
    digest = sha(archive)
    starter = make_starter(archive.parent, parts, digest, sha(output / "MINDLE_MEDIA_AI_RUN.exe"))
    write(evidence / "SUCCESSOR_DELIVERY.json", {
        "name": archive.name, "bytes": archive.stat().st_size, "sha256": digest, "parts": parts,
        "source": manifest["build_commit"], "manifest_sha256": sha(payload / "PACKAGE_MANIFEST.json"),
        "exe_sha256": sha(output / "MINDLE_MEDIA_AI_RUN.exe"), "installer": record(archive.parent, starter),
        "payload_files": len(manifest["files"]), "post_runtime_hashes": "PASS", "zip_crc": "PASS",
        "office_pc_acceptance": False, "human_hearing": False, "full_product_pass": False,
    })
    print("SUCCESSOR_SEALED", digest, len(parts), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["assemble", "seal"])
    parser.add_argument("--output", default="build/" + NAME)
    parser.add_argument("--evidence", default="evidence-r3")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--parts", default="build/base-r2")
    arguments = parser.parse_args()
    (assemble if arguments.action == "assemble" else seal)(arguments)
