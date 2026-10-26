"""Receipt fixtures test verdicts only; they are never real model inference evidence."""
from copy import deepcopy
import hashlib
from uuid import uuid4

import pytest

from media_ai.ai_core_status import summarize_ai_core

READY = {"generative_planner": "CONFIGURED_NOT_INFERENCE_VERIFIED", "tts": "CONFIGURED_NOT_SYNTHESIS_VERIFIED", "durable_queue": True, "neural_korean_tts": True}


def artifact(root, name, content=b'fixture bytes, not model output'):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {"path": str(path), "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def workflow(root):
    identifier, plan_id = str(uuid4()), str(uuid4())
    response = artifact(root, f'workflows/plans/{plan_id}.response.txt', b'{"steps":[]}')
    voice = {"status": "TESTED_PASS", "job_id": str(uuid4()), "workflow_id": identifier,
             "operation": "narration", "primary_output": artifact(root, 'voice.wav'),
             "runtime_result": {"model_inference": True}}
    video = {"status": "TESTED_PASS", "job_id": str(uuid4()), "workflow_id": identifier,
             "lane": "video", "operation": "video_edit", "primary_output": artifact(root, 'final.mp4'),
             "runtime_result": {"video_codec": "h264", "audio_codec": "aac", "options": {"narration_job_id": voice['job_id']}},
             "outputs": [artifact(root, 'copied_voice.wav')]}
    return {"workflow_id": identifier, "state": "SUCCEEDED", "plan_receipt": {
        "plan_source": "LOCAL_GENERATIVE_INFERENCE", "plan_id": plan_id,
        "model_sha256": 'a'*64, "raw_response_sha256": response['sha256']},
        "records": [voice, video], "result": deepcopy(video)}


def summary(root, tasks=None, records=None):
    return summarize_ai_core(READY, tasks or [], [], records or [], data_root=root)


def test_configured_engines_are_not_misreported_as_actual_ai_work(tmp_path):
    value = summary(tmp_path)
    assert value['state'] == 'AI_ENGINES_READY_INFERENCE_REQUIRED'
    assert value['shell_only'] is False
    assert value['chain_evidence']['workflow_ids'] == []


def test_same_workflow_response_voice_mix_and_final_bytes_close_chain(tmp_path):
    task = workflow(tmp_path)
    value = summary(tmp_path, [task])
    assert value['state'] == 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'
    assert value['chain_evidence']['workflow_ids'] == [task['workflow_id']]
    assert value['chain_evidence']['full_product_pass'] is False
    assert value['chain_evidence']['human_hearing'] == 'NOT_VERIFIED'


def test_unrelated_successes_cannot_close_chain(tmp_path):
    task = workflow(tmp_path)
    loose = task.pop('records')
    task['records'] = []
    value = summary(tmp_path, [task], loose)
    assert all(value['actual_evidence'][key] for key in ('qwen_or_architecture_plan','neural_korean_voice','mp4_output'))
    assert value['state'] != 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'


@pytest.mark.parametrize('defect', ['voice_link','voice_owner','final_owner','voice_not_mixed','no_audio','result_mismatch','failed','structured','missing_voice','changed_video','changed_voice','changed_response','import'])
def test_invalid_or_stale_evidence_never_closes_chain(tmp_path, defect):
    task = workflow(tmp_path)
    voice, video = task['records']
    if defect == 'voice_link': video['runtime_result']['options']['narration_job_id'] = 'unrelated'
    elif defect == 'voice_owner': voice['workflow_id'] = 'unrelated'
    elif defect == 'final_owner': video['workflow_id'] = 'unrelated'
    elif defect == 'voice_not_mixed': video['outputs'] = []
    elif defect == 'no_audio': video['runtime_result'].pop('audio_codec')
    elif defect == 'result_mismatch': task['result']['job_id'] = 'unrelated'
    elif defect == 'failed': task['state'] = 'FAILED'
    elif defect == 'structured': task['plan_receipt']['plan_source'] = 'STRUCTURED_USER_PLAN_NOT_GENERATIVE'
    elif defect == 'missing_voice': __import__('pathlib').Path(voice['primary_output']['path']).unlink()
    elif defect == 'changed_video': __import__('pathlib').Path(video['primary_output']['path']).write_bytes(b'altered MP4 bytes')
    elif defect == 'changed_voice': __import__('pathlib').Path(voice['primary_output']['path']).write_bytes(b'altered WAV bytes')
    elif defect == 'changed_response': (tmp_path/'workflows/plans'/(task['plan_receipt']['plan_id']+'.response.txt')).write_bytes(b'altered model response')
    elif defect == 'import': video['operation'] = 'import'
    assert summary(tmp_path, [task])['state'] != 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'


def test_imported_mp4_is_not_generated_ai_output(tmp_path):
    imported = {"status":"TESTED_PASS", "operation":"import", "lane":"video", "primary_output":artifact(tmp_path,'import.mp4')}
    assert summary(tmp_path, records=[imported])['actual_evidence']['mp4_output'] is False


def test_static_shell_is_exposed_and_generation_limits_stay_explicit():
    value = summarize_ai_core({}, [], [], [])
    assert value['state'] == 'AI_RUNTIME_INCOMPLETE'
    assert value['shell_only'] is True
    assert value['limitations']['text_to_video_generation'] is False


def test_media_models_require_extant_verified_output_bytes(tmp_path):
    records = [{"status":"TESTED_PASS", "operation":op, "model":{"repo_id":"fixture"},
                "primary_output":artifact(tmp_path,op+'.bin')} for op in ('segment','tracking','transcribe','upscale')]
    keys = ('sam_photo_segmentation','sam_video_tracking','whisper_korean_stt','photo_upscale_4x')
    actual = summary(tmp_path, records=records)['actual_evidence']
    assert all(actual[k] for k in keys)
    for record in records:
        __import__('pathlib').Path(record['primary_output']['path']).unlink()
    actual = summary(tmp_path, records=records)['actual_evidence']
    assert not any(actual[k] for k in keys)


def test_artifacts_outside_product_root_are_not_evidence(tmp_path):
    inside = tmp_path/'inside'
    inside.mkdir()
    task = workflow(tmp_path)
    assert summary(inside, [task])['state'] != 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'


def test_real_http_status_binds_data_directory_and_downgrades_changed_bytes(tmp_path, monkeypatch):
    """Actual HTTP and files; inference receipts are explicit test fixtures."""
    import json
    from pathlib import Path
    import threading
    from urllib.request import urlopen
    from media_ai.product_server import create_server

    root = tmp_path/'data'
    server = create_server(Path(__file__).resolve().parents[1], root, '')
    task = workflow(root)
    monkeypatch.setattr(server.workflow_queue(), 'list', lambda: [task])
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f'http://127.0.0.1:{server.server_port}/api/ai-core/status'
        with urlopen(url, timeout=10) as response:
            assert json.load(response)['chain_evidence']['workflow_ids'] == [task['workflow_id']]
        Path(task['result']['primary_output']['path']).write_bytes(b'changed after initial PASS')
        with urlopen(url, timeout=10) as response:
            assert json.load(response)['state'] != 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def test_actual_ffmpeg_mix_preserves_voice_binding_and_streams(tmp_path, monkeypatch):
    """Real FFmpeg, WAV, sealing and MP4. Planner/TTS inference are NOT executed."""
    import base64
    from pathlib import Path
    import shutil
    import subprocess
    from media_ai.product_runtime import ProductJobService, file_record
    from media_ai.workflow_worker import mix_narration, probe
    from media_ai.durable_workflows import DurableWorkflows

    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        pytest.skip('FFmpeg unavailable')
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    root = tmp_path/'data'
    service = ProductJobService(root, '')
    source = tmp_path/'source.mp4'
    tone = root/'tone.wav'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=160x90:r=10',
                    '-t','1','-c:v','libx264','-pix_fmt','yuv420p',str(source)],check=True)
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:sample_rate=24000',
                    '-t','0.25',str(tone)],check=True)
    video = service.import_media({'kind':'video','filename':'source.mp4',
                                 'content_base64':base64.b64encode(source.read_bytes()).decode()})
    voice = {'job_id':str(uuid4()),'status':'TESTED_PASS','operation':'narration','lane':'korean_audio',
             'primary_output':file_record(tone),'runtime_result':{'model_inference':False,'engine':'test tone'}}
    mixed = mix_narration(service, video, voice, {'length_policy':'reject'})
    queue = DurableWorkflows(service)
    try:
        attempt = root/'workflows/test-sealing'
        sealed = queue._seal_record(mixed, attempt)
        info = probe(Path(sealed['primary_output']['path']))
        assert {s['codec_type'] for s in info['streams']} == {'audio','video'}
        assert sealed['runtime_result']['options']['narration_job_id'] == voice['job_id']
        assert any(a['sha256'] == voice['primary_output']['sha256'] for a in sealed['outputs'])
        task = workflow(root)
        voice['workflow_id'] = task['workflow_id']
        sealed['workflow_id'] = task['workflow_id']
        task.update(records=[voice,sealed], result=deepcopy(sealed))
        assert summary(root,[task])['state'] != 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'
        # Simulated neural receipt tests the connection contract only.
        voice['runtime_result']['model_inference'] = True
        assert summary(root,[task])['state'] == 'AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'
    finally:
        queue.close()


def test_formant_tts_is_not_neural_engine_readiness(tmp_path):
    from media_ai.workflow_planner import capabilities
    import json
    (tmp_path/'runtime-engines.json').write_text(json.dumps({'tts':{'engine':'espeak-ng'}}))
    config = capabilities(tmp_path)
    assert config['neural_korean_tts'] is False
    assert summarize_ai_core(config,[],[],[],data_root=tmp_path)['configured']['neural_korean_tts'] is False
