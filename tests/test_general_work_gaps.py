import base64
import io
import json
from pathlib import Path
from uuid import uuid4

import pytest
from PIL import Image
from media_ai.product_runtime import ProductJobService
from media_ai.product_server import ProductHttpServer


def photo_payload():
    stream = io.BytesIO()
    Image.new('RGB', (16, 9), (40, 110, 180)).save(stream, 'PNG')
    return {'content_base64': base64.b64encode(stream.getvalue()).decode()}


def test_unknown_jobs_and_invalid_project_id_cannot_overwrite(tmp_path):
    service = ProductJobService(tmp_path, '')
    job = service.store_photo_edit(photo_payload())
    saved = service.save_project({'job_ids': [job['job_id']]})
    original = Path(saved['project']['path']).read_bytes()
    with pytest.raises(ValueError):
        service.save_project({'project_id': saved['project_id'], 'job_ids': [job['job_id'], 'absent']})
    with pytest.raises(ValueError):
        service.save_project({'project_id': '../outside', 'job_ids': [job['job_id']]})
    assert Path(saved['project']['path']).read_bytes() == original
    assert not list(service.projects.glob('*.tmp'))


@pytest.mark.parametrize('failure', ['missing', 'changed'])
def test_export_rejects_missing_or_changed_media(tmp_path, failure):
    service = ProductJobService(tmp_path, '')
    job = service.store_photo_edit(photo_payload())
    saved = service.save_project({'job_ids': [job['job_id']]})
    path = Path(job['primary_output']['path'])
    if failure == 'missing':
        path.unlink()
    else:
        path.write_bytes(b'corruption')
    with pytest.raises(ValueError):
        service.export_project(saved['project_id'])
    assert not (service.projects / (saved['project_id'] + '_export.zip')).exists()


def test_windows_filename_is_sanitized_on_any_os(tmp_path):
    service = ProductJobService(tmp_path, '')
    path = service._store_input(r'C:\사용자 폴더\사진.png', photo_payload()['content_base64'])
    assert path.name.endswith('_사진.png') and '\\' not in path.name
    assert path.parent == service.inputs


def test_same_request_replayed_and_conflict_rejected(tmp_path):
    import threading
    server = object.__new__(ProductHttpServer)
    server.job_lock = threading.Lock()
    server.completed_requests = {}
    service = ProductJobService(tmp_path, '')
    payload = {**photo_payload(), 'request_id': str(uuid4())}
    first = server.run_once('/api/photo-edits', payload, service.store_photo_edit)
    second = server.run_once('/api/photo-edits', payload, service.store_photo_edit)
    assert first['job_id'] == second['job_id'] and len(service.records) == 1
    with pytest.raises(ValueError):
        server.run_once('/api/photo-edits', {**payload, 'command': 'different'}, service.store_photo_edit)


def test_failed_request_is_retryable(tmp_path):
    import threading
    server = object.__new__(ProductHttpServer)
    server.job_lock = threading.Lock()
    server.completed_requests = {}
    service = ProductJobService(tmp_path, '')
    payload = {**photo_payload(), 'request_id': str(uuid4())}
    def unavailable(_):
        raise ValueError('unavailable')
    with pytest.raises(ValueError):
        server.run_once('/api/photo-edits', payload, unavailable)
    assert server.run_once('/api/photo-edits', payload, service.store_photo_edit)['status'] == 'TESTED_PASS'


def test_base_product_needs_no_hf_token(tmp_path, monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    service = ProductJobService(tmp_path, '')
    job = service.import_media({'kind': 'photo', 'filename': '사진.png', **photo_payload()})
    assert job['runtime_result']['result_size'] == [16, 9]
    with pytest.raises(RuntimeError, match='AI 모델'):
        service.vault._download_files('sam21', {})


def test_subtitle_font_and_split_validation_use_actual_ffmpeg(tmp_path):
    import shutil
    import subprocess
    if not shutil.which('ffmpeg'):
        pytest.skip('FFmpeg runtime unavailable')
    source = tmp_path / 'video.mp4'
    subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=160x90:rate=12', '-t', '1', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(source)], check=True, capture_output=True)
    service = ProductJobService(tmp_path / '작업 폴더', '')
    payload = {'filename': '영상 파일.mp4', 'content_base64': base64.b64encode(source.read_bytes()).decode()}
    with pytest.raises(ValueError, match='분할'):
        service.edit_video({**payload, 'options': {'split': True, 'start': 0}})
    fonts = list(Path('/usr/share/fonts').rglob('*CJK*'))
    if not fonts:
        pytest.skip('Korean font runtime unavailable')
    result = service.edit_video({**payload, 'options': {'subtitle': '한국어 자막 검증'}})
    assert result['runtime_result']['options']['subtitle'] == '한국어 자막 검증'
    assert result['primary_output']['sha256'] != __import__('hashlib').sha256(source.read_bytes()).hexdigest()


def test_legacy_video_concat_newlines_and_original_ratio(tmp_path):
    import shutil
    import subprocess
    from media_ai.video import process_video
    from media_ai.browser_preview import probe
    if not shutil.which('ffmpeg'):
        pytest.skip('FFmpeg runtime unavailable')
    source=tmp_path / "영상 ' 원본.mp4"
    subprocess.run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=120x240:rate=12','-t','1','-c:v','libx264','-pix_fmt','yuv420p',str(source)],check=True,capture_output=True)
    output=tmp_path/'결과.mp4'
    process_video(source,output,{'clips':[str(source)]})
    result=probe(output)
    assert [result['streams'][0]['width'],result['streams'][0]['height']]==[120,240]
    assert float(result['format']['duration'])>=2
