"""Synthetic replies exercise gates, not actual model capability."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import pytest
from media_ai import workflow_planner as planner
from media_ai.product_runtime import ProductJobService
from media_ai.durable_workflows import DurableWorkflows


def generated(tmp_path,monkeypatch):
    decision={'steps':[{'operation':'video_edit','options':{'brightness':3}}]}
    raw=json.dumps(decision)
    settings={'model_sha256':'a'*64,'revision':'b'*40,'license':'fixture','executable_sha256':'c'*64}
    monkeypatch.setattr(planner,'invoke_local_json_plan',lambda *a,**k:(decision,raw,settings))
    return planner.make_plan(tmp_path,{'command':'밝기 3 높여 줘'})


@pytest.mark.parametrize('fault',['saved_steps','raw','command'])
def test_normal_generated_workflow_rejects_modified_plan_before_queue(tmp_path,monkeypatch,fault):
    service=ProductJobService(tmp_path/'data','')
    source=tmp_path/'input.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=32x18:r=4','-t','1','-c:v','libx264',str(source)],check=True)
    job=service.import_media({'kind':'video','filename':source.name,'content_base64':base64.b64encode(source.read_bytes()).decode()})
    plan=generated(service.root,monkeypatch);folder=service.root/'workflows/plans'
    if fault=='saved_steps':plan['steps'][0]['options']['brightness']=4
    elif fault=='raw':(folder/(plan['plan_id']+'.response.txt')).write_bytes(b'{"steps":[]}')
    else:plan['command']='밝기 4 높여 줘'
    (folder/(plan['plan_id']+'.json')).write_text(json.dumps(plan),encoding='utf-8')
    queue=DurableWorkflows(service)
    try:
        with pytest.raises(ValueError,match='PLANNER_(RESPONSE|COMMAND)'):
            queue.submit({'input_job_id':job['job_id'],'plan_id':plan['plan_id'],'steps':plan['steps']})
        assert queue.list()==[]
        assert not list(service.projects.glob('*.json'))
    finally:queue.close()


def test_valid_generated_binding_and_utf8_prompt_preserved(tmp_path,monkeypatch):
    plan=generated(tmp_path,monkeypatch)
    planner.validate_generated_binding(tmp_path,plan)
    assert '밝기 3' in (tmp_path/'workflows/plans'/(plan['plan_id']+'.prompt.txt')).read_text(encoding='utf-8')


@pytest.mark.parametrize('failure',['timeout','invalid_json','process_error'])
def test_inference_fault_preserves_partial_reply_and_failure(tmp_path,monkeypatch,failure):
    executable=tmp_path/'runner';executable.write_bytes(b'fixture');model=tmp_path/'model';model.write_bytes(b'fixture')
    sha=hashlib.sha256(b'fixture').hexdigest()
    settings={'executable':str(executable),'executable_sha256':sha,'model_path':str(model),'model_sha256':sha,'revision':'a'*40,'license':'fixture'}
    monkeypatch.setattr(planner,'engines_config',lambda root:{'planner':settings})
    def fail(*args,**kwargs):
        if failure=='timeout':raise subprocess.TimeoutExpired('fixture',1,output=b'{"steps":[',stderr=b'timeout-fixture')
        if failure=='process_error':raise subprocess.CalledProcessError(2,'fixture',output=b'partial reply',stderr=b'fixture-error')
        return 'not json, fixture'
    monkeypatch.setattr(planner.subprocess,'check_output',fail)
    with pytest.raises((ValueError,subprocess.TimeoutExpired,subprocess.CalledProcessError)):
        planner.invoke_local_json_plan(tmp_path,'실제 원고가 아닌 시험 prompt',{})
    audit=next((tmp_path/'workflows/inference-audit').iterdir())
    record=json.loads((audit/'INFERENCE.json').read_text(encoding='utf-8'))
    assert record['status']=='FAILED'
    assert record['response_sha256']==hashlib.sha256((audit/'response.txt').read_bytes()).hexdigest()
    assert (audit/'response.txt').stat().st_size>0
    assert (audit/'prompt.txt').exists()
