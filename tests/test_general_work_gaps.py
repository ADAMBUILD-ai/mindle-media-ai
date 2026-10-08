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


def test_background_removal_uses_mask_without_changing_segmentation(tmp_path):
    from media_ai.product_runtime import file_record
    service=ProductJobService(tmp_path,'')
    original=tmp_path/'inputs/원본.png';Image.new('RGB',(32,18),(120,80,30)).save(original)
    directory=tmp_path/'jobs/sam';directory.mkdir()
    overlay=directory/'photo_overlay.png';Image.new('RGB',(16,9),(255,30,30)).save(overlay)
    mask=directory/'photo_mask.png';alpha=Image.new('L',(16,9),0)
    for y in range(9):
        for x in range(8):alpha.putpixel((x,y),255)
    alpha.save(mask)
    overlay_hash=file_record(overlay)['sha256']
    service.records['seg']={'status':'TESTED_PASS','job_id':'seg','operation':'segment','lane':'photo','input':file_record(original),'primary_output':file_record(overlay),'outputs':[file_record(mask),file_record(overlay)]}
    result=service.prepare_photo_background('seg')
    with Image.open(result['preview_output']['path']) as output:
        assert output.size==(32,18) and output.mode=='RGBA'
        assert output.getpixel((2,2))==(120,80,30,255)
        assert output.getpixel((30,2))==(120,80,30,0)
    assert file_record(overlay)['sha256']==overlay_hash
    assert result['background_removal']['model_rerun'] is False
    saved=service.save_project({'job_ids':['seg']})
    assert ProductJobService(tmp_path,'').latest_project()['jobs'][0]['preview_output']['sha256']==result['preview_output']['sha256']
    assert service.export_project(saved['project_id'])['status']=='EXPORTED'


def test_actual_http_byte_ranges_allow_browser_seek(tmp_path):
    import threading
    import requests
    from media_ai.product_server import create_server
    data=tmp_path/'data';data.mkdir()
    payload=bytes(range(256))*4
    (data/'video.mp4').write_bytes(payload)
    server=create_server(tmp_path,data,'',0)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    url=f'http://127.0.0.1:{server.server_port}/files/video.mp4'
    try:
        for header,expected in [('bytes=100-199',payload[100:200]),('bytes=900-',payload[900:]),('bytes=-10',payload[-10:])]:
            response=requests.get(url,headers={'Range':header},timeout=5)
            assert response.status_code==206 and response.content==expected
            assert response.headers['Accept-Ranges']=='bytes'
            assert response.headers['Content-Range'].endswith('/1024')
        for header in ('bytes=2048-','bytes=-0','bytes=10-5','bytes=0-1,10-20'):
            response=requests.get(url,headers={'Range':header},timeout=5)
            assert response.status_code==416 and response.content==b''
        assert requests.get(url,timeout=5).content==payload
    finally:
        server.shutdown();thread.join(5);server.server_close()
