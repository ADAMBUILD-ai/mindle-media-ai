"""Exercise the installed HTTP product, never import application source directly."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def request(url, route, body=None):
    payload = None if body is None else json.dumps(body, ensure_ascii=False).encode('utf-8')
    req = Request(url + route, data=payload, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=1200) as response:
        return json.load(response)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def checked_output(record, data):
    path = Path(record['path']).resolve()
    if data not in path.parents or not path.is_file():
        raise RuntimeError('Output must exist inside installed data root')
    if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
        raise RuntimeError('Output hash or size mismatch')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reopen', action='store_true')
    parser.add_argument('--operations', nargs='+', default=['tracking', 'transcribe', 'segment', 'upscale'])
    args = parser.parse_args()
    result = {'status': 'RUNNING', 'method': 'INSTALLED_PRODUCT_HTTP', 'executable': sys.executable,
              'python_search_paths': sys.path, 'checks': {}, 'jobs': [], 'started_at': time.time()}
    def save():
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    save()
    try:
        identity = request(args.url, '/api/runtime-identity')
        root = args.package_root.resolve()
        if Path(sys.executable).resolve().parent != root / 'runtime/python':
            raise RuntimeError('Function gate must run with the installed package Python')
        for entry in sys.path:
            search = Path(entry).resolve()
            if search != root and root not in search.parents:
                raise RuntimeError('Python search path escapes installed package: ' + entry)
        data = Path(identity['data_root']).resolve()
        if identity.get('runtime_mode') != 'LOCAL_OFFLINE_PACKAGE' or Path(identity['install_root']).resolve() != root:
            raise RuntimeError('Installed package runtime identity mismatch')
        result['identity'] = identity
        result['checks']['identity'] = 'PASS'
        if args.reopen:
            prior = json.loads((args.output.parent / 'INSTALLED_FUNCTION_TEST.json').read_text(encoding='utf-8'))
            project = request(args.url, '/api/projects/latest')['project']
            if not project or project['project_id'] != prior['saved_project']['project_id']:
                raise RuntimeError('Saved project was not restored after server restart')
            if project['job_ids'] != [job['job_id'] for job in prior['jobs']]:
                raise RuntimeError('Restored project jobs mismatch')
            for job in project['jobs']:
                checked_output(job['primary_output'], data)
            result['checks']['save_close_reopen'] = 'PASS_SERVER_RESTART'
            result['project_id'] = project['project_id']
        else:
            manifest = json.loads((args.fixtures / 'FIXTURE_MANIFEST.json').read_text(encoding='utf-8'))
            specs = {
                'tracking': ('video', 'video.mp4', '영상의 대상을 추적해 주세요'),
                'transcribe': ('korean_audio', 'korean.wav', '한국어 음성을 자막으로 변환해 주세요'),
                'segment': ('photo', 'photo.png', '왼쪽 인물을 분리해 주세요'),
                'upscale': ('photo', 'sisr_480x270.png', '사진을 4배 확대해 주세요'),
            }
            for operation in args.operations:
                lane, name, command = specs[operation]
                source = args.fixtures / name
                pin = next(item for item in manifest['files'] if item['name'] == name)
                if digest(source) != pin['sha256'] or source.stat().st_size != pin['bytes']:
                    raise RuntimeError('Fixture integrity failure: ' + name)
                job = request(args.url, '/api/jobs', dict(lane=lane, operation=operation, filename=name,
                    command=command, content_base64=base64.b64encode(source.read_bytes()).decode('ascii')))
                if job.get('status') != 'TESTED_PASS':
                    raise RuntimeError('Installed job failed: ' + operation)
                primary = checked_output(job['primary_output'], data)
                with urlopen(args.url + job['preview_url'], timeout=60) as response:
                    preview = response.read()
                if hashlib.sha256(preview).hexdigest() != job['primary_output']['sha256']:
                    raise RuntimeError('HTTP preview differs from actual output')
                if operation == 'transcribe' and not re.search('[가-힣]', job['runtime_result'].get('text', '')):
                    raise RuntimeError('Korean transcript is empty or lacks Hangul')
                if operation in {'tracking', 'segment', 'upscale'}:
                    ffmpeg = root / 'tools/ffmpeg/ffmpeg.exe'
                    decoded = subprocess.run([str(ffmpeg), '-v', 'error', '-i', str(primary), '-f', 'null', '-'],
                                             capture_output=True, timeout=120)
                    if decoded.returncode:
                        raise RuntimeError('Package FFmpeg preview decode failed: ' + decoded.stderr.decode(errors='replace'))
                if operation == 'upscale':
                    ffprobe = root / 'tools/ffmpeg/ffprobe.exe'
                    probe = subprocess.run([str(ffprobe), '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height', '-of', 'json', str(primary)], capture_output=True, check=True, timeout=60)
                    stream = json.loads(probe.stdout)['streams'][0]
                    if (stream['width'], stream['height']) != (1920, 1080):
                        raise RuntimeError('Intel 4x dimensions mismatch')
                result['jobs'].append(job)
                result['checks'][operation] = 'PASS_INSTALLED_HTTP_AND_OUTPUT_VERIFICATION'
                save()
                print(operation + ': PASS_INSTALLED_HTTP', flush=True)
            result['saved_project'] = request(args.url, '/api/projects/save', {'job_ids': [j['job_id'] for j in result['jobs']]})
            result['checks']['save'] = 'PASS'
            result['project_id'] = result['saved_project']['project_id']
        exported = request(args.url, '/api/projects/' + result['project_id'] + '/export', {})
        archive = checked_output(exported['export'], data)
        with urlopen(args.url + exported['download_url'], timeout=60) as response:
            if hashlib.sha256(response.read()).hexdigest() != exported['export']['sha256']:
                raise RuntimeError('Downloaded export hash mismatch')
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None or 'project.json' not in z.namelist():
                raise RuntimeError('Export ZIP corrupt or project absent')
        result['export'] = exported
        result['checks']['export'] = 'PASS_CONTENT_AND_DOWNLOAD_HASH'
        try:
            request(args.url, '/api/integrations/marketing/shortform', {'command': '광고 숏폼을 만들어 주세요'})
            raise RuntimeError('Offline Shortform unexpectedly succeeded')
        except HTTPError as error:
            body = json.load(error)
            if error.code != 503 or body.get('status') != 'MARKETING_PROVIDER_UNAVAILABLE':
                raise RuntimeError('Incorrect Shortform graceful handling')
            result['shortform'] = {'http_status': error.code, 'body': body}
        request(args.url, '/api/runtime-identity')
        request(args.url, '/api/projects/latest')
        result['checks']['shortform_and_base_continuation'] = 'PASS'
        result['status'] = 'INSTALLED_FUNCTION_GATE_PASS'
        result['full_offline_distribution_pass'] = False
        save()
        print(result['status'], flush=True)
        return 0
    except Exception as error:
        result.update(status='CLEAN_WINDOWS_TEST_FAILED', error=repr(error))
        save()
        print(str(error), file=sys.stderr, flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
