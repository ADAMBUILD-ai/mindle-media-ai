import base64
import json
import subprocess
import zipfile
from pathlib import Path
import pytest
from media_ai.product_runtime import ProductJobService
from media_ai.video_analysis import analyze_video


def test_scene_analysis_selects_content_and_survives_reopen_export(tmp_path, monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    source = tmp_path/'source.mp4'
    subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=black:size=160x90:rate=10:duration=3',
                    '-f','lavfi','-i','testsrc2=size=160x90:rate=10:duration=5',
                    '-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]','-map','[v]',
                    '-c:v','libx264','-pix_fmt','yuv420p',str(source)],check=True,capture_output=True)
    analysis=analyze_video(source,3)
    assert analysis['start']>=2.5 and analysis['sample_count']>=7
    assert analysis['semantic_understanding'] is False
    service=ProductJobService(tmp_path/'data','')
    job=service.edit_video({'filename':'source.mp4','content_base64':base64.b64encode(source.read_bytes()).decode(),
                            'options':{'auto_edit':True,'duration':3}})
    assert job['runtime_result']['analysis']['start']==analysis['start']
    assert job['runtime_result']['model_inference'] is False
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',job['primary_output']['path']]))
    assert info['streams'][0]['codec_name']=='h264' and info['streams'][0]['pix_fmt']=='yuv420p'
    assert [info['streams'][0]['width'],info['streams'][0]['height']]==[160,90]
    assert 2.9<float(info['format']['duration'])<3.2
    saved=service.save_project({'job_ids':[job['job_id']]})
    reopened=ProductJobService(tmp_path/'data','')
    assert reopened.latest_project()['jobs'][0]['runtime_result']['analysis']==job['runtime_result']['analysis']
    exported=reopened.export_project(saved['project_id'])
    with zipfile.ZipFile(exported['export']['path']) as archive:
        assert archive.testzip() is None
        assert archive.read('jobs/'+job['job_id']+'/edited_video.mp4')==Path(job['primary_output']['path']).read_bytes()


@pytest.mark.parametrize('seconds',[0,-1,float('nan'),float('inf')])
def test_invalid_auto_edit_duration_rejected(tmp_path,seconds):
    with pytest.raises(ValueError):analyze_video(tmp_path/'absent.mp4',seconds)


def test_missing_local_models_keep_base_photo_runtime_but_block_ai(tmp_path,monkeypatch):
    import io
    from PIL import Image
    monkeypatch.setenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',str(tmp_path/'missing-package'))
    service=ProductJobService(tmp_path/'data','')
    assert service.model_readiness['status']=='BLOCKED_MODEL_FILES'
    buf=io.BytesIO();Image.new('RGB',(32,18)).save(buf,'PNG')
    result=service.import_media({'kind':'photo','filename':'original.png','content_base64':base64.b64encode(buf.getvalue()).decode()})
    assert result['status']=='TESTED_PASS'
    with pytest.raises(RuntimeError,match='unavailable'):service.execute_isolated({'operation':'segment'})
