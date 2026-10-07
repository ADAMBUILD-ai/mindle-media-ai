"""Package-only entry point; stdlib bootstrap, no Git or user Python lookup."""
from __future__ import annotations
import argparse
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import urlopen


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify(root):
    if os.name == 'nt' and not str(root).startswith('\\\\?\\'):
        root = Path('\\\\?\\' + str(root.resolve()))
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('distribution') != 'EMPLOYEE_WIN_X64':
        raise RuntimeError('직원용 패키지 정보가 올바르지 않습니다.')
    for entry in manifest['files']:
        path = (root / entry['path']).resolve()
        if root not in path.parents or not path.is_file():
            raise RuntimeError('패키지 파일이 없거나 경로가 잘못되었습니다: ' + entry['path'])
        if path.stat().st_size != entry['bytes'] or sha256(path) != entry['sha256']:
            raise RuntimeError('패키지 검증 실패: ' + entry['path'])
    return manifest


def identity(port):
    try:
        with urlopen(f'http://127.0.0.1:{port}/api/runtime-identity', timeout=1) as response:
            return json.load(response)
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--server', action='store_true')
    parser.add_argument('--port', type=int)
    parser.add_argument('--data-root', type=Path)
    parser.add_argument('--deny-path', action='append', default=[])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    blocked = json.loads(os.environ.get('MINDLE_TEST_BLOCKED_PATHS', '[]'))
    blocked.extend(args.deny_path)
    if blocked:
        os.environ['MINDLE_TEST_BLOCKED_PATHS'] = json.dumps(blocked)
    if blocked:
        def audit(event, values):
            if event in {'open', 'os.listdir', 'os.scandir', 'os.chdir'} and values and isinstance(values[0], (str, bytes, os.PathLike)):
                path = os.path.normcase(os.path.abspath(os.fsdecode(values[0]))).removeprefix('\\\\?\\')
                for forbidden in blocked:
                    prefix = os.path.normcase(os.path.abspath(forbidden)).removeprefix('\\\\?\\')
                    if path == prefix or path.startswith(prefix + os.sep):
                        raise PermissionError('E2E process is denied access to the development repository/cache')
            if event == 'socket.connect' and len(values) > 1 and isinstance(values[1], tuple):
                if values[1][0] not in {'127.0.0.1', '::1', 'localhost'}:
                    raise PermissionError('E2E process forbids non-loopback network connections')
        sys.addaudithook(audit)
        for forbidden in blocked:
            try:
                with open(Path(forbidden) / 'README.md', 'rb'):
                    pass
            except PermissionError:
                continue
            raise RuntimeError('E2E development repository access denial was not enforced')
    manifest = verify(root)
    if args.verify_only:
        print('PACKAGE_HASH_VERIFICATION_PASS')
        return
    data = args.data_root or (Path(os.environ['LOCALAPPDATA']) / 'MINDLE/MEDIA_AI_DATA')
    data.mkdir(parents=True, exist_ok=True)
    (data / 'logs').mkdir(exist_ok=True)
    for key in list(os.environ):
        if key in {'HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN', 'PYTHONPATH', 'PYTHONHOME'} or key.startswith('MARKETING_'):
            os.environ.pop(key, None)
    os.environ.update(MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT=str(root), HF_HUB_OFFLINE='1',
                      TRANSFORMERS_OFFLINE='1', HF_HOME=str(data / 'offline-cache'),
                      PYTHONNOUSERSITE='1', PATH=str(root / 'tools/ffmpeg') + os.pathsep + str(Path(os.environ['SystemRoot']) / 'System32'))
    if args.server:
        from media_ai.product_server import create_server
        server = create_server(root / 'app', data, '', args.port)
        server.serve_forever()
        return
    lock = open(data / 'launch.lock', 'a+b')
    if lock.tell() == 0:
        lock.write(b'0'); lock.flush()
    deadline = time.monotonic() + 90
    while True:
        try:
            lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1); break
        except OSError:
            if time.monotonic() > deadline:
                raise RuntimeError('다른 실행 요청을 기다리는 중입니다. 잠시 후 다시 실행하세요.')
            time.sleep(.25)
    try:
        expected = sha256(root / 'PACKAGE_MANIFEST.json')
        port = None
        for candidate in range(18768, 18778):
            current = identity(candidate)
            if current and current.get('install_root') == str(root) and current.get('package_manifest_sha256') == expected:
                port = candidate; break
        if port is None:
            import socket
            for candidate in range(18768, 18778):
                try:
                    with socket.socket() as probe:
                        probe.bind(('127.0.0.1', candidate))
                    log = open(data / 'logs/server.log', 'ab')
                    server_env = dict(os.environ)
                    server_env.update(LOCALAPPDATA=str(data), APPDATA=str(data / 'appdata'),
                                      HF_HUB_DISABLE_TELEMETRY='1')
                    process = subprocess.Popen([sys.executable, str(Path(__file__)), '--server', '--port', str(candidate), '--data-root', str(data)],
                                               cwd=root, env=server_env, stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW)
                    log.close()
                    # Full model/runtime integrity checks can exceed 90s on a cold disk.
                    # Keep the verification intact and allow it to finish on employee PCs.
                    until = time.monotonic() + 900
                    while time.monotonic() < until:
                        current = identity(candidate)
                        if current and current.get('package_manifest_sha256') == expected and current.get('install_root') == str(root):
                            port = candidate; break
                        if process.poll() is not None:
                            raise RuntimeError('제품 실행에 실패했습니다. logs/server.log를 확인하세요.')
                        time.sleep(.25)
                    if port is not None: break
                    process.terminate()
                    raise RuntimeError('제품 시작 시간이 초과됐습니다.')
                except OSError:
                    continue
            if port is None:
                raise RuntimeError('사용 가능한 제품 포트가 없습니다.')
        url = f'http://127.0.0.1:{port}/?ui_build={manifest["ui_fingerprint"]}'
        candidates = [Path(os.environ.get(key, '')) / suffix for key in ('ProgramFiles', 'ProgramFiles(x86)')
                      for suffix in ('Microsoft/Edge/Application/msedge.exe', 'Google/Chrome/Application/chrome.exe')]
        browser = next((p for p in candidates if p.is_file()), None)
        if browser:
            subprocess.Popen([str(browser), '--app=' + url])
        else:
            os.startfile(url)
    finally:
        lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1); lock.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, str(error), 'MINDLE MEDIA AI', 0x10)
        raise
