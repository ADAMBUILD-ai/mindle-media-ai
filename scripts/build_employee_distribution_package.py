"""Build only from an explicitly pinned, already proven Windows CPU runtime.

No dependency installation or upgrades occur here. RuntimeLock is pip-freeze
formatted input from the approved runtime, not a request to resolve packages.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import zipfile

NAME = 'MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0'
MANDATORY = {'torch', 'transformers', 'safetensors', 'huggingface-hub', 'numpy', 'pillow',
             'opencv-python-headless', 'openvino', 'tokenizers'}


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''): h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    for name in ('repo', 'python-root', 'model-root', 'ffmpeg-root', 'runtime-lock'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--build-commit', help='Immutable published source commit for this package')
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors = []
    if platform.system() != 'Windows' or platform.machine().lower() not in {'amd64', 'x86_64'}:
        errors.append('Windows x64 builder required')
    if sys.version_info[:2] != (3, 11): errors.append('Python 3.11 required')
    import torch
    if torch.version.cuda is not None: errors.append('CPU-only PyTorch required; observed ' + torch.__version__)
    if not args.runtime_lock.is_file():
        errors.append('approved exact working runtime lock required')
        locked = {}
    else:
        locked = dict(line.strip().split('==', 1) for line in args.runtime_lock.read_text(encoding='utf-8').splitlines()
                      if line.strip() and not line.startswith('#'))
        locked = {key.lower().replace('_', '-'): value for key, value in locked.items()}
    for name in MANDATORY:
        if name not in locked: errors.append('required pinned dependency missing: ' + name)
    distributions = {}
    for name, version in locked.items():
        try:
            dist = metadata.distribution(name)
            distributions[name] = dist
            if dist.version != version: errors.append('runtime lock version mismatch: ' + name)
        except metadata.PackageNotFoundError:
            errors.append('runtime dependency absent: ' + name)
    from packaging.requirements import Requirement
    for name, dist in distributions.items():
        for spec in dist.requires or []:
            required = Requirement(spec)
            if required.marker and not required.marker.evaluate({'extra': ''}): continue
            key = required.name.lower().replace('_', '-')
            if key not in locked or locked[key] not in required.specifier:
                errors.append(f'locked dependency closure incomplete: {name} requires {spec}')
    # Import every required backend from the actual builder runtime before copy.
    for name in ('transformers', 'cv2', 'openvino', 'safetensors', 'tokenizers'):
        try: __import__(name)
        except Exception as error: errors.append(name + ' import failed: ' + str(error))
    for name in ('python.exe', 'pythonw.exe', 'python311.dll', 'LICENSE.txt'):
        if not (args.python_root / name).is_file(): errors.append('Python runtime file absent: ' + name)
    for name in ('ffmpeg.exe', 'ffprobe.exe'):
        if not (args.ffmpeg_root / name).is_file(): errors.append('FFmpeg file absent: ' + name)
    if not (args.ffmpeg_root / 'LICENSES').is_dir(): errors.append('FFmpeg redistribution notices/source offer required')
    for model in ('sam21', 'whisper-small'):
        if not any(path.is_file() for path in (args.model_root / 'models' / model).glob('*LICENSE*')):
            errors.append('upstream redistribution license absent: ' + model)
    sys.path.insert(0, str(repo / 'src'))
    import os
    os.environ['MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT'] = str(args.model_root.resolve())
    from media_ai.product_runtime import ProductModelVault
    try: ProductModelVault(repo / 'work-data/employee-build-check', '').verify_local_models()
    except Exception as error: errors.append('model verification: ' + str(error))
    detail = repo / 'evidence/pc_remote/media-ai-employee-package-v1_0-20261006'
    detail.mkdir(parents=True, exist_ok=True)
    write_json(detail / 'BUILD_PREFLIGHT.json', {'status': 'BLOCKED' if errors else 'PREREQUISITES_VERIFIED',
               'python': sys.version, 'torch': torch.__version__, 'cuda': torch.version.cuda, 'errors': errors})
    if errors:
        print(json.dumps({'status': 'BLOCKED', 'errors': errors}, ensure_ascii=False, indent=2))
        return 2
    # Wheel paths exceed MAX_PATH in deeply nested build checkouts.
    # The archive still uses ordinary relative paths and installs per-user.
    root = Path('\\\\?\\' + str((repo / 'dist' / NAME).resolve()))
    if root.exists(): raise RuntimeError('build output already exists; use a fresh reviewed output directory')
    root.mkdir(parents=True)
    copy_ignore = shutil.ignore_patterns('__pycache__', '*.pyc', '.cache', '.git', '*.pth')
    shutil.copytree(repo / 'src', root / 'app/src', ignore=copy_ignore)
    shutil.copytree(repo / 'ui', root / 'app/ui', ignore=copy_ignore)
    shutil.copytree(repo / 'ui/assets/brand', root / 'assets/brand', ignore=copy_ignore)
    (root / 'app/launcher').mkdir()
    shutil.copy2(repo / 'scripts/employee_package_launcher.py', root / 'app/launcher')
    py = root / 'runtime/python'; py.mkdir(parents=True)
    for pattern in ('*.exe', '*.dll', '*.zip', 'LICENSE.txt'):
        for path in args.python_root.glob(pattern): shutil.copy2(path, py / path.name)
    shutil.copytree(args.python_root / 'DLLs', py / 'DLLs', ignore=copy_ignore)
    shutil.copytree(args.python_root / 'Lib', py / 'Lib', ignore=shutil.ignore_patterns('site-packages', '__pycache__', '*.pyc', 'test', 'idlelib'))
    site = root / 'runtime/site-packages'; site.mkdir()
    notices = root / 'LICENSES'; notices.mkdir()
    for name, dist in distributions.items():
        for relative in dist.files or []:
            # Wheel RECORD paths outside site-packages are development tools.
            if '..' in relative.parts: continue
            source = Path(dist.locate_file(relative))
            if not source.is_file() or source.suffix in {'.pyc', '.pth'}: continue
            destination = site / str(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            if 'license' in source.name.lower() or 'notice' in source.name.lower() or 'licenses' in relative.parts:
                license_path = notices / name / str(relative)
                license_path.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, license_path)
    (py / 'python311._pth').write_text('Lib\nDLLs\n.\n../site-packages\n../../app/src\n', encoding='ascii')
    for folder in ('models/sam21', 'models/whisper-small', 'omz/intel/single-image-super-resolution-1032/FP32'):
        shutil.copytree(args.model_root / folder, root / folder, ignore=copy_ignore)
    shutil.copytree(args.ffmpeg_root, root / 'tools/ffmpeg', ignore=copy_ignore)
    shutil.copy2(args.python_root / 'LICENSE.txt', notices / 'PYTHON_LICENSE.txt')
    shutil.copy2(args.runtime_lock, root / 'RUNTIME_LOCK_EMPLOYEE_WIN_X64.txt')
    (root / 'tests').mkdir()
    shutil.copy2(repo / 'scripts/employee_smoke_test.ps1', root / 'tests/employee_smoke_test.ps1')
    (root / 'uninstall').mkdir()
    shutil.copy2(repo / 'scripts/uninstall_employee_package.ps1', root / 'uninstall/UNINSTALL_MINDLE_MEDIA_AI.ps1')
    shutil.copy2(repo / 'scripts/install_employee_package.ps1', root / 'INSTALL_MINDLE_MEDIA_AI.ps1')
    for action in ('INSTALL', 'UNINSTALL'):
        target = 'INSTALL_MINDLE_MEDIA_AI.ps1' if action == 'INSTALL' else 'uninstall\\UNINSTALL_MINDLE_MEDIA_AI.ps1'
        (root / f'{action}_MINDLE_MEDIA_AI.cmd').write_text('@echo off\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0' + target + '"\nset "RESULT=%errorlevel%"\npause\nexit /b %RESULT%\n', encoding='ascii')
    guide = '1. 파일을 한 폴더에 모읍니다.\n2. 분할본이면 REASSEMBLE_AND_INSTALL.cmd를 더블클릭합니다.\n3. 단일 ZIP이면 압축을 풀고 INSTALL_MINDLE_MEDIA_AI.cmd를 더블클릭합니다.\n4. 설치 후 바탕화면의 MINDLE MEDIA AI 아이콘을 더블클릭합니다.\n5. 사진/영상을 불러와 사용합니다.\n6. 오류가 나면 설치 폴더를 지우지 말고 %LOCALAPPDATA%\\MINDLE\\MEDIA_AI_DATA\\logs 폴더를 전달합니다.\n'
    (root / 'README_FIRST_KO.txt').write_text(guide, encoding='utf-8-sig')
    docs = root / 'docs'; docs.mkdir()
    (docs / 'MINDLE_MEDIA_AI_USER_GUIDE_KO.html').write_text('<!doctype html><meta charset="utf-8"><title>MINDLE MEDIA AI</title><h1>MINDLE MEDIA AI</h1><pre>' + html.escape(guide) + '</pre>', encoding='utf-8')
    source_guide = repo / 'docs/MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md'
    if not source_guide.is_file():
        matches = list((repo / 'docs').rglob(source_guide.name))
        if len(matches) != 1: raise RuntimeError('approved Korean user guide missing or ambiguous')
        source_guide = matches[0]
    shutil.copy2(source_guide, docs / source_guide.name)
    model_records = [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)}
                     for folder in ('models', 'omz') for p in sorted((root / folder).rglob('*')) if p.is_file()]
    write_json(root / 'MODEL_MANIFEST.json', model_records)
    # Retain the model source licenses checked by the preflight.
    write_json(notices / 'MODEL_LICENSE_MANIFEST.json', {'sam21': 'Apache-2.0', 'whisper-small': 'MIT', 'intel-sisr-1032': 'Apache-2.0'})
    (notices / 'THIRD_PARTY_NOTICES.txt').write_text('Python, PyTorch, Transformers, OpenVINO and transitive libraries: see retained LICENSES and runtime dist-info notices. FFmpeg: see tools/ffmpeg/LICENSES. Models: see MODEL_LICENSE_MANIFEST.json and model source licenses.\n', encoding='utf-8')
    files = [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in sorted(root.rglob('*')) if p.is_file()]
    ui_names = ['index.html', 'approved_visual.css', 'interaction.css', 'interaction.js', 'product_integration.js', 'assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico']
    ui_hash = hashlib.sha256('\n'.join('ui/' + n + ':' + digest(root / 'app/ui' / n) for n in ui_names).encode()).hexdigest()
    commit = args.build_commit or subprocess.check_output(['git', '-c', 'safe.directory=' + repo.as_posix(), '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if len(commit) != 40 or any(c not in '0123456789abcdef' for c in commit):
        raise RuntimeError('build commit must be a full immutable Git SHA')
    manifest = {'distribution': 'EMPLOYEE_WIN_X64', 'package_version': '1.0', 'build_commit': commit, 'ui_fingerprint': ui_hash,
                'model_manifest_hash': digest(root / 'MODEL_MANIFEST.json'), 'files': files, 'release_gate': 'CLEAN_WINDOWS_TEST_REQUIRED'}
    write_json(root / 'PACKAGE_MANIFEST.json', manifest)
    (root / 'PACKAGE_SHA256SUMS.txt').write_text('\n'.join(f'{entry["sha256"]}  {entry["path"]}' for entry in files) + '\n', encoding='utf-8')
    subprocess.run([str(py / 'python.exe'), str(root / 'app/launcher/employee_package_launcher.py'), '--verify-only'], check=True)
    archive = root.parent / (root.name + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as output:
        for path in root.rglob('*'):
            if path.is_file(): output.write(path, NAME + '/' + path.relative_to(root).as_posix())
    write_json(detail / 'PACKAGE_BUILD_MANIFEST.json', {'status': 'PACKAGE_BUILD_PARTIAL', 'zip_sha256': digest(archive), 'zip_bytes': archive.stat().st_size, 'manifest': manifest})
    print('PACKAGE_BUILT_CLEAN_WINDOWS_TEST_REQUIRED')
    return 0


if __name__ == '__main__': raise SystemExit(main())
