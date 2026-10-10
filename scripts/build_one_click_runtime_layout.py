"""Assemble the reviewed Windows one-click distribution layout.

The output contains one employee-visible MINDLE_MEDIA_AI_RUN.exe and a private
_payload directory. The bootstrap automatically materializes _payload into a
versioned LOCALAPPDATA runtime; the employee does not run installers, Python,
pip, Git, or model download commands.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def copytree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".cache"),
    )


def files_manifest(root: Path) -> list[dict]:
    return [
        {
            "path": p.relative_to(root).as_posix(),
            "bytes": p.stat().st_size,
            "sha256": digest(p),
        }
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name != "PACKAGE_MANIFEST.json"
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--python-embed-root", type=Path, required=True)
    parser.add_argument("--site-packages-root", type=Path, required=True)
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--ffmpeg-root", type=Path, required=True)
    parser.add_argument("--launcher-exe", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--build-commit", required=True)
    parser.add_argument("--runtime-lock", type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_root.resolve()
    if output.exists():
        raise RuntimeError("output root already exists: " + str(output))
    output.mkdir(parents=True)
    payload = output / "_payload"
    payload.mkdir()

    launcher = output / "MINDLE_MEDIA_AI_RUN.exe"
    shutil.copy2(args.launcher_exe, launcher)

    copytree(repo / "src", payload / "app" / "src")
    copytree(repo / "ui", payload / "app" / "ui")
    (payload / "app" / "launcher").mkdir(parents=True)
    shutil.copy2(repo / "scripts" / "employee_package_launcher.py", payload / "app" / "launcher")

    python_root = payload / "runtime" / "python"
    copytree(args.python_embed_root.resolve(), python_root)
    site = payload / "runtime" / "site-packages"
    copytree(args.site_packages_root.resolve(), site)
    (python_root / "python311._pth").write_text(
        "python311.zip\n.\n../site-packages\n../../app/src\nimport site\n",
        encoding="ascii",
    )

    models = args.model_root.resolve()
    for relative in (
        Path("models") / "sam21",
        Path("models") / "whisper-small",
        Path("omz") / "intel" / "single-image-super-resolution-1032" / "FP32",
    ):
        source = models / relative
        if not source.is_dir():
            raise RuntimeError("required model directory missing: " + str(source))
        copytree(source, payload / relative)

    ffmpeg_source = args.ffmpeg_root.resolve()
    ffmpeg_bin = ffmpeg_source / "bin"
    if not ffmpeg_bin.is_dir():
        ffmpeg_bin = ffmpeg_source
    ffmpeg_target = payload / "tools" / "ffmpeg"
    ffmpeg_target.mkdir(parents=True)
    for source in ffmpeg_bin.iterdir():
        if source.is_file():
            shutil.copy2(source, ffmpeg_target / source.name)
    for required in ("ffmpeg.exe", "ffprobe.exe"):
        if not (ffmpeg_target / required).is_file():
            raise RuntimeError("FFmpeg payload missing: " + required)

    license_target = payload / "LICENSES"
    if (repo / "LICENSES").is_dir():
        copytree(repo / "LICENSES", license_target)
    else:
        license_target.mkdir()
    ffmpeg_notice = license_target / "FFMPEG"
    ffmpeg_notice.mkdir(parents=True, exist_ok=True)
    for pattern in ("LICENSE*", "COPYING*", "README*"):
        for source in ffmpeg_source.glob(pattern):
            if source.is_file():
                shutil.copy2(source, ffmpeg_notice / source.name)

    python_license = python_root / "LICENSE.txt"
    if python_license.is_file():
        shutil.copy2(python_license, license_target / "PYTHON_LICENSE.txt")
    if args.runtime_lock and args.runtime_lock.is_file():
        shutil.copy2(args.runtime_lock, payload / "RUNTIME_LOCK_EMPLOYEE_WIN_X64.txt")

    model_records = [
        {
            "path": p.relative_to(payload).as_posix(),
            "bytes": p.stat().st_size,
            "sha256": digest(p),
        }
        for folder in (payload / "models", payload / "omz")
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    ]
    model_manifest_path = payload / "MODEL_MANIFEST.json"
    model_manifest_path.write_text(
        json.dumps(model_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    ui_names = [
        "index.html",
        "approved_visual.css",
        "interaction.css",
        "interaction.js",
        "product_integration.js",
        "assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico",
    ]
    ui_hash = hashlib.sha256(
        "\n".join(
            f"ui/{name}:{digest(payload / 'app' / 'ui' / name)}" for name in ui_names
        ).encode("utf-8")
    ).hexdigest()

    runtime_id = f"{args.build_commit[:12]}-{ui_hash[:12]}"
    manifest = {
        "distribution": "EMPLOYEE_WIN_X64",
        "package_version": "ONE_CLICK_RUNTIME_R1",
        "runtime_id": runtime_id,
        "build_commit": args.build_commit,
        "ui_fingerprint": ui_hash,
        "model_manifest_hash": digest(model_manifest_path),
        "launcher": "MINDLE_MEDIA_AI_RUN.exe",
        "normal_user_action": "DOUBLE_CLICK_ONLY",
        "files": files_manifest(payload),
    }
    manifest_path = payload / "PACKAGE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    delivery = {
        "distribution": "MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64",
        "build_commit": args.build_commit,
        "runtime_id": runtime_id,
        "launcher": {
            "path": launcher.name,
            "bytes": launcher.stat().st_size,
            "sha256": digest(launcher),
        },
        "payload_manifest": {
            "path": "_payload/PACKAGE_MANIFEST.json",
            "bytes": manifest_path.stat().st_size,
            "sha256": digest(manifest_path),
            "file_count": len(manifest["files"]),
        },
    }
    (output / "DELIVERY_MANIFEST.json").write_text(
        json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "DELIVERY_ARTIFACT_SHA256.txt").write_text(
        f"{delivery['launcher']['sha256']}  MINDLE_MEDIA_AI_RUN.exe\n"
        f"{delivery['payload_manifest']['sha256']}  _payload/PACKAGE_MANIFEST.json\n",
        encoding="ascii",
    )
    print(json.dumps(delivery, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
