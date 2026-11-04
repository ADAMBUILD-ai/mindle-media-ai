"""Generated-fixture source HTTP cold restart; no EXE, model or hearing claim."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.error import URLError
from urllib.request import Request, urlopen
import wave
import zipfile
from PIL import Image

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); root = args.root.resolve(); args.out.mkdir(parents=True, exist_ok=True)
    result = {'scope': 'REAL_SOURCE_HTTP_PROCESS_LIFECYCLE_GENERATED_FIXTURES',
              'packaged_exe_pass': False, 'office_pc_pass': False, 'model_inference': False}
    def call(base, route, body=None, headers=None):
        data = None if body is None else json.dumps(body).encode()
        req = Request(base + route, data=data, headers={'Content-Type': 'application/json', **(headers or {})})
        with urlopen(req, timeout=10) as r: return json.load(r)
    def image():
        stream = io.BytesIO(); Image.new('RGB', (30, 60), (60, 90, 120)).save(stream, 'PNG')
        return stream.getvalue()
    def attachment(name, data, mime):
        return {'filename': name, 'mime_type': mime, 'content_base64': base64.b64encode(data).decode()}
    with tempfile.TemporaryDirectory(prefix='mindle_owner_stop_') as temp:
        env = dict(os.environ, PYTHONPATH=str(root / 'src'))
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', None)
        env.pop('HF_TOKEN', None)
        processes = []
        def start():
            p = subprocess.Popen([sys.executable, '-m', 'media_ai.product_server', '--root', str(root),
                '--data-dir', temp, '--port', '0'], env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            processes.append(p)
            base = p.stdout.readline().strip()
            if not base.startswith('http://127.0.0.1:'): raise RuntimeError('source server failed to start')
            identity = call(base, '/api/runtime-identity')
            assert identity['server_pid'] == p.pid
            return p, base, identity
        def stop(p, base, identity):
            c = call(base, '/api/runtime/control')
            assert c['server_pid'] == p.pid and c['server_instance_id'] == identity['server_instance_id']
            receipt = call(base, '/api/runtime/shutdown', {k: c[k] for k in ('server_pid', 'server_instance_id')},
                           {'X-Mindle-Control': c['control_nonce']})
            assert receipt['status'] == 'RUNTIME_STOPPING'
            assert p.wait(timeout=10) == 0
            try: urlopen(base + '/api/runtime-identity', timeout=1)
            except URLError: pass
            else: raise AssertionError('old endpoint still responds')
            return {'pid_exited': p.pid, 'exit_code': p.returncode, 'endpoint_closed': True}
        try:
            p, base, first = start()
            photo = image()
            job = call(base, '/api/photo-edits', {'content_base64': base64.b64encode(photo).decode()})
            audio = io.BytesIO()
            with wave.open(audio, 'wb') as wav:
                wav.setparams((1, 2, 16000, 0, 'NONE', 'not compressed')); wav.writeframes(bytes(3200))
            workspace = {'references': {'photo': [attachment('사진.png', photo, 'image/png')],
                         'video': [attachment('참고.png', photo, 'image/png')]},
                         'audio': attachment('입력.wav', audio.getvalue(), 'audio/wav')}
            saved = call(base, '/api/projects/save', {'job_ids': [job['job_id']], 'workspace': workspace})
            before = Path(saved['project']['path']).read_bytes()
            result['first_identity'] = first; result['first_stop'] = stop(p, base, first)
            p2, base2, second = start()
            assert p2.pid != p.pid and first['server_instance_id'] != second['server_instance_id']
            project = call(base2, '/api/projects/latest')['project']
            assert project['project_id'] == saved['project_id']
            assert Path(saved['project']['path']).read_bytes() == before
            for item in project['workspace']['references']['photo'] + project['workspace']['references']['video'] + [project['workspace']['audio']]:
                with urlopen(base2 + item['url'], timeout=5) as r: data = r.read()
                assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256']
            export = call(base2, '/api/projects/' + saved['project_id'] + '/export', {})
            with urlopen(base2 + export['download_url'], timeout=10) as r: archive = r.read()
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                assert z.testzip() is None
                manifest = json.loads(z.read('BUNDLE_MANIFEST.json'))
                for item in manifest['files']:
                    data = z.read(item['archive_path'])
                    assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256']
            result.update(second_identity=second, project_id=saved['project_id'],
                export={'sha256': hashlib.sha256(archive).hexdigest(), 'bytes': len(archive),
                        'crc': 'PASS', 'manifest_files': len(manifest['files'])},
                second_stop=stop(p2, base2, second), status='PASS_SOURCE_PROCESS_OWNER_STOP_RESTART_REOPEN_EXPORT')
        finally:
            for process in processes:
                if process.poll() is None:
                    # Only our own explicitly created test processes; never another runtime.
                    process.terminate(); process.wait(timeout=5)
    (args.out / 'SOURCE_OWNER_LIFECYCLE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(result['status'])

if __name__ == '__main__': main()
