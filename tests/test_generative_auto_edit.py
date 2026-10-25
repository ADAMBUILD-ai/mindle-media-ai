"""Faults and inference fixtures are explicit; fixture replies are not real Qwen evidence."""
import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import time

import pytest
from media_ai.product_runtime import ProductJobService
from media_ai.durable_workflows import DurableWorkflows
from media_ai import generative_auto_edit as auto
from media_ai.ai_core_status import summarize_ai_core


@pytest.fixture
def source(tmp_path, monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    path=tmp_path/'input.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=160x90:rate=12',
                    '-t','1','-c:v','libx264','-pix_fmt','yuv420p',str(path)],check=True)
    service=ProductJobService(tmp_path/'data','')
    record=service.import_media({'kind':'video','filename':'input.mp4','content_base64':base64.b64encode(path.read_bytes()).decode()})
    return service,record


def infer_fixture(monkeypatch, decision=None):
    from media_ai import workflow_planner
    value=decision or {'start':0,'brightness':3,'contrast':0,'saturation':0,'reason':'Fixture: measured exposure supports a bounded brightness correction.'}
    raw=json.dumps(value)+'\n'
    settings={'model_id':'fixture-not-executed','model_sha256':'a'*64,'revision':'b'*40,'license':'fixture','executable_sha256':'c'*64}
    def infer(root,prompt,schema,**kwargs):
        assert 'MEASUREMENTS=' in prompt and 'semantic vision' in prompt
        return deepcopy(value),raw,settings
    monkeypatch.setattr(workflow_planner,'invoke_local_json_plan',infer)


def plan_for(source, monkeypatch):
    infer_fixture(monkeypatch)
    service,record=source
    return auto.make_auto_plan(service,{'command':'자동 편집','input_job_id':record['job_id']})


def test_without_local_model_auto_edit_fails_closed_without_jobs(source):
    service,record=source
    before=set(service.records)
    with pytest.raises(ValueError,match='LOCAL_GENERATIVE_MODEL_UNAVAILABLE'):
        auto.make_auto_plan(service,{'command':'자동 편집','input_job_id':record['job_id']})
    assert set(service.records)==before
    assert not list((service.root/'workflows/plans').glob('*.json'))


@pytest.mark.parametrize('key,value',[('start',.4),('brightness',13),('contrast',True),('saturation',float('nan')),('reason','')])
def test_model_cannot_invent_unmeasured_ranges_or_excessive_corrections(source,monkeypatch,key,value):
    decision={'start':0,'brightness':3,'contrast':0,'saturation':0,'reason':'fixture'}
    decision[key]=value
    infer_fixture(monkeypatch,decision)
    with pytest.raises(ValueError,match='AI_AUTO_'):
        service,record=source
        auto.make_auto_plan(service,{'command':'자동 편집','input_job_id':record['job_id']})


def test_auto_request_cannot_drop_unrelated_user_intent(source):
    service,record=source
    with pytest.raises(ValueError,match='AI_AUTO_EXPLICIT_INTENT_REQUIRED'):
        auto.make_auto_plan(service,{'command':'자동 편집하고 원본 삭제해줘','input_job_id':record['job_id']})


def test_plan_is_bound_to_input_and_exact_model_response(source,monkeypatch):
    service,record=source
    plan=plan_for(source,monkeypatch)
    actual=plan['input_artifact']
    auto.validate_auto_binding(service.root,plan,record,actual)
    with pytest.raises(ValueError,match='AI_AUTO_PLAN_INPUT_MISMATCH'):
        auto.validate_auto_binding(service.root,plan,{**record,'job_id':'foreign'},actual)
    path=service.root/'workflows/plans'/(plan['plan_id']+'.response.txt')
    path.write_bytes(b'changed response')
    with pytest.raises(ValueError,match='AI_AUTO_INFERENCE_RESPONSE_CHANGED'):
        auto.validate_auto_binding(service.root,plan,record,actual)


def test_queue_refuses_model_decision_step_drift(source,monkeypatch):
    service,record=source
    plan=plan_for(source,monkeypatch)
    path=service.root/'workflows/plans'/(plan['plan_id']+'.json')
    plan['steps'][0]['options']['brightness']=4
    path.write_text(json.dumps(plan))
    queue=DurableWorkflows(service)
    try:
        with pytest.raises(ValueError,match='AI_AUTO_DECISION_EXECUTION_MISMATCH'):
            queue.submit({'input_job_id':record['job_id'],'plan_id':plan['plan_id'],'steps':plan['steps']})
        assert queue.list()==[]
    finally:queue.close()


def run(queue,record,plan):
    task=queue.submit({'request_id':'auto-test','input_job_id':record['job_id'],'plan_id':plan['plan_id'],'steps':plan['steps']})
    until=time.monotonic()+20
    while time.monotonic()<until:
        task=queue.get(task['workflow_id'])
        if task['state'] in {'SUCCEEDED','FAILED','INTERRUPTED'}:return task
        time.sleep(.025)
    pytest.fail('auto edit workflow timeout')


def test_real_ffmpeg_auto_workflow_quality_gate_and_evidence(source,monkeypatch):
    service,record=source
    plan=plan_for(source,monkeypatch)
    queue=DurableWorkflows(service)
    try:
        task=run(queue,record,plan)
        assert task['state']=='SUCCEEDED',task
        assert task['technical_quality']['status']=='PASS_TECHNICAL_ONLY'
        assert task['technical_quality']['semantic_quality']=='NOT_EVALUATED'
        status=summarize_ai_core({},[task],[],[],data_root=service.root)
        assert status['state']=='AI_EDIT_EXECUTION_VERIFIED'  # Fixture inference, actual FFmpeg only.
        assert status['auto_edit_evidence']['full_product_pass'] is False
        Path(task['result']['primary_output']['path']).unlink()
        assert summarize_ai_core({},[task],[],[],data_root=service.root)['state']!='AI_EDIT_EXECUTION_VERIFIED'
    finally:queue.close()


def test_quality_failure_never_publishes_project_or_jobs(source,monkeypatch):
    service,record=source
    plan=plan_for(source,monkeypatch)
    before=set(service.records)
    def reject(*args):raise ValueError('AI_AUTO_OUTPUT_QUALITY_REJECTED: injected technical fault')
    monkeypatch.setattr(auto,'assess_auto_output',reject)
    queue=DurableWorkflows(service)
    try:
        task=run(queue,record,plan)
        assert task['state']=='FAILED'
        assert 'AI_AUTO_OUTPUT_QUALITY_REJECTED' in task['error']
        assert set(service.records)==before
        assert not list(service.projects.glob('*.json'))
    finally:queue.close()


def test_black_output_cannot_pass_technical_quality(source,monkeypatch):
    from media_ai.product_runtime import file_record
    service,record=source
    plan=plan_for(source,monkeypatch)
    black=service.root/'black.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=black:s=160x90:r=12',
                    '-t','1','-c:v','libx264','-pix_fmt','yuv420p',str(black)],check=True)
    with pytest.raises(ValueError,match='AI_AUTO_OUTPUT_QUALITY_REJECTED'):
        auto.assess_auto_output(plan,{'primary_output':file_record(black)})


def test_auto_plan_actual_http_refuses_missing_model_without_publication(source):
    import threading
    from urllib.request import Request,urlopen
    from urllib.error import HTTPError
    from media_ai.product_server import create_server
    service,record=source
    server=create_server(Path(__file__).resolve().parents[1],service.root,'')
    server.service.records[record['job_id']]=record
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        request=Request(f'http://127.0.0.1:{server.server_port}/api/workflows/auto-plan',
                        data=json.dumps({'command':'자동 편집','input_job_id':record['job_id']}).encode(),
                        headers={'Content-Type':'application/json'})
        with pytest.raises(HTTPError) as error:urlopen(request,timeout=15)
        assert error.value.code==422
        assert 'LOCAL_GENERATIVE_MODEL_UNAVAILABLE' in json.load(error.value)['error']
        assert server.workflow_queue().list()==[]
        assert not list(server.service.projects.glob('*.json'))
    finally:server.shutdown();thread.join();server.server_close()
