"""Assemble the portable MINDLE MEDIA AI one-click Windows runtime."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import shutil


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def copytree(src: Path, dst: Path) -> None:
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".cache"),
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--python-embed", type=Path, required=True)
    p.add_argument("--site-packages", type=Path, required=True)
    p.add_argument("--model-root", type=Path, required=True)
    p.add_argument("--ffmpeg-root", type=Path, required=True)
    p.add_argument("--launcher-exe", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--build-commit", required=True)
    args = p.parse_args()

    repo = args.repo.resolve()
    out = args.output.resolve()
    if out.exists():
        raise RuntimeError(f"output already exists: {out}")
    out.mkdir(parents=True)

    copytree(repo / "src", out / "app" / "src")
    copytree(repo / "ui", out / "app" / "ui")
    (out / "app" / "launcher").mkdir(parents=True)
    shutil.copy2(repo / "scripts" / "employee_package_launcher.py", out / "app" / "launcher" / "employee_package_launcher.py")

    copytree(args.python_embed.resolve(), out / "runtime" / "python")
    copytree(args.site_packages.resolve(), out / "runtime" / "site-packages")
    (out / "runtime" / "python" / "python311._pth").write_text(
        "python311.zip\n.\n../site-packages\n../../app/src\nimport site\n",
        encoding="ascii",
    )
    for required in ("python.exe", "pythonw.exe", "python311.dll"):
        if not (out / "runtime" / "python" / required).is_file():
            raise RuntimeError(f"embedded Python missing {required}")

    for folder in ("models/sam21", "models/whisper-small", "omz/intel/single-image-super-resolution-1032/FP32"):
        src = args.model_root.resolve() / folder
        if not src.is_dir():
            raise RuntimeError(f"model payload missing: {src}")
        copytree(src, out / folder)

    copytree(args.ffmpeg_root.resolve(), out / "tools" / "ffmpeg")
    if not (out / "tools" / "ffmpeg" / "ffmpeg.exe").is_file():
        raise RuntimeError("packaged ffmpeg.exe missing")
    if not (out / "tools" / "ffmpeg" / "ffprobe.exe").is_file():
        raise RuntimeError("packaged ffprobe.exe missing")

    if (repo / "LICENSES").is_dir():
        copytree(repo / "LICENSES", out / "LICENSES")
    else:
        (out / "LICENSES").mkdir()

    shutil.copy2(args.launcher_exe.resolve(), out / "MINDLE_MEDIA_AI_RUN.exe")

    model_records = []
    for base in ("models", "omz"):
        for file in sorted((out / base).rglob("*")):
            if file.is_file():
                model_records.append({
                    "path": file.relative_to(out).as_posix(),
                    "bytes": file.stat().st_size,
                    "sha256": digest(file),
                })
    (out / "MODEL_MANIFEST.json").write_text(
        json.dumps(model_records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    distributions = []
    for dist in metadata.distributions(path=[str(out / "runtime" / "site-packages")]):
        name = dist.metadata.get("Name") or "UNKNOWN"
        distributions.append({"name": name, "version": dist.version})
    distributions.sort(key=lambda x: x["name"].lower())
    (out / "RUNTIME_LOCK_EMPLOYEE_WIN_X64.json").write_text(
        json.dumps(distributions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    ui_names = [
        "index.html", "approved_visual.css", "interaction.css", "interaction.js",
        "product_integration.js", "assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico",
    ]
    ui_hash = hashlib.sha256("\n".join(
        f"ui/{name}:{digest(out / 'app' / 'ui' / name)}" for name in ui_names
    ).encode()).hexdigest()

    files = []
    for file in sorted(out.rglob("*")):
        if file.is_file():
            files.append({
                "path": file.relative_to(out).as_posix(),
                "bytes": file.stat().st_size,
                "sha256": digest(file),
            })

    manifest = {
        "distribution": "EMPLOYEE_WIN_X64",
        "package_version": "ONE_CLICK_REMOTE_R1",
        "build_commit": args.build_commit,
        "ui_fingerprint": ui_hash,
        "model_manifest_hash": digest(out / "MODEL_MANIFEST.json"),
        "normal_user_action": "DOUBLE_CLICK_MINDLE_MEDIA_AI_RUN_EXE",
        "runtime_mode": "PORTABLE_OFFLINE_FOLDER",
        "external_marketing_avora": "DEFERRED_EXTERNAL",
        "files": files,
        "release_gate": "REMOTE_WINDOWS_AUTOMATION_THEN_LOCAL_ACCEPTANCE",
    }
    (out / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "status": "ONE_CLICK_PACKAGE_ASSEMBLED",
        "package_root": str(out),
        "file_count": len(files),
        "package_manifest_sha256": digest(out / "PACKAGE_MANIFEST.json"),
        "launcher_sha256": digest(out / "MINDLE_MEDIA_AI_RUN.exe"),
        "build_commit": args.build_commit,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
