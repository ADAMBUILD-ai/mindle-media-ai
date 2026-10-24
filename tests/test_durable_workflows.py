"""Real local subprocess/FFmpeg queue tests. Faults are injected only at worker launch."""
import base64,hashlib,json,os,subprocess,sys,time,zipfile
from pathlib import Path
import pytest
from media_ai.product_runtime import ProductJobService
from media_ai.durable_workflows import DurableWorkflows,validate_steps
from media_ai.workflow_planner import make_plan

@pytest.fixture
def video(tmp_path):
    path=tmp_path/'fixture.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=160x90:r=10','-t','2','-c:v','libx264','-pix_fmt','yuv420p','-y',str(path)],check=True)
    return path
@pytest.fixture
def service(tmp_path,video,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    service=ProductJobService(tmp_path/'data','')
    source=service.import_media({'kind':'video','filename':'fixture.mp4','content_base64':base64.b64encode(video.read_bytes()).decode()})
    return service,source

def wait(queue,identifier,states=None,timeout=20):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        value=queue.get(identifier)
        if value['state'] in (states or {'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'}):return value
        time.sleep(.025)
    pytest.fail('workflow state timeout: '+str(value))
def submit(queue,source,**kw):
    return queue.submit({'request_id':'one','input_job_id':source['job_id'],'steps':[{'operation':'video_edit','options':{'brightness':10}}],**kw})
def test_real_worker_commit_replay_and_reopen(service):
    service,source=service;queue=DurableWorkflows(service)
    try:
        task=submit(queue,source);same=submit(queue,source);assert task['workflow_id']==same['workflow_id']
        with pytest.raises(ValueError,match='같은 요청ID'):submit(queue,source,steps=[{'operation':'video_edit','options':{'brightness':20}}])
        result=wait(queue,task['workflow_id']);assert result['state']=='SUCCEEDED',result
        assert len(result['attempts'])==1
        with zipfile.ZipFile(result['export']['export']['path']) as archive:assert archive.testzip() is None
        assert result['result']['primary_output']['sha256']!=source['primary_output']['sha256']
    finally:queue.close()
    reloaded=ProductJobService(service.root,'');assert reloaded.latest_project()['project_id']==result['project_id'];assert result['result']['job_id'] in reloaded.records
    again=DurableWorkflows(reloaded)
    try:assert again.get(task['workflow_id'])['state']=='SUCCEEDED'
    finally:again.close()
def test_cancel_own_real_process_and_no_publication(service,monkeypatch):
    service,source=service;queue=DurableWorkflows(service)
    monkeypatch.setattr(queue,'_command',lambda p:[sys.executable,'-c','import time;time.sleep(25)'])
    before=set(service.records)
    try:
        task=submit(queue,source)
        end=time.monotonic()+5
        while time.monotonic()<end:
            value=queue.get(task['workflow_id'])
            if value['attempts'] and value['attempts'][-1].get('worker_pid'):break
            time.sleep(.02)
        assert queue.cancel(task['workflow_id'])['state']=='CANCEL_REQUESTED'
        result=wait(queue,task['workflow_id']);assert result['state']=='CANCELLED';assert result['attempts'][-1]['returncode']!=0
        assert set(service.records)==before;assert not list(service.projects.glob('*.json'))
    finally:queue.close()
def test_real_transient_retry_then_actual_ffmpeg_success(service,monkeypatch):
    service,source=service;queue=DurableWorkflows(service);normal=queue._command
    def command(path):
        if path.parent.name.endswith('-1'):
            return [sys.executable,'-c',"import pathlib,json;pathlib.Path(__import__('sys').argv[1]).write_text(json.dumps({'error':'injected EBUSY boundary','retryable':True}))",str(path.parent/'response.json')]
        return normal(path)
    monkeypatch.setattr(queue,'_command',command)
    try:
        task=submit(queue,source);result=wait(queue,task['workflow_id']);assert result['state']=='SUCCEEDED',result
        assert [r['state'] for r in result['attempts']]==['FAILED','SUCCEEDED']
    finally:queue.close()
def test_cancel_retry_wait_prevents_second_attempt(service,monkeypatch):
    service,source=service;queue=DurableWorkflows(service)
    monkeypatch.setattr(queue,'_command',lambda p:[sys.executable,'-c',"import pathlib,json;pathlib.Path(__import__('sys').argv[1]).write_text(json.dumps({'error':'injected transient','retryable':True}))",str(p.parent/'response.json')])
    try:
        task=submit(queue,source);wait(queue,task['workflow_id'],{'RETRY_WAIT'});queue.cancel(task['workflow_id']);result=wait(queue,task['workflow_id']);assert result['state']=='CANCELLED';assert len(result['attempts'])==1
    finally:queue.close()
def test_permanent_missing_tts_does_not_retry_or_change_saved_project(service):
    service,source=service;saved=service.save_project({'job_ids':[source['job_id']]});path=service.projects/(saved['project_id']+'.json');original=path.read_bytes();queue=DurableWorkflows(service)
    try:
        task=submit(queue,source,project_id=saved['project_id'],steps=[{'operation':'narrate','text':'안녕하세요'}]);result=wait(queue,task['workflow_id']);assert result['state']=='FAILED';assert len(result['attempts'])==1;assert 'TTS_ENGINE_UNAVAILABLE' in result['error'];assert path.read_bytes()==original
    finally:queue.close()
def test_owner_lock_blocks_competing_queue(service):
    service,_=service;queue=DurableWorkflows(service)
    try:
        with pytest.raises(RuntimeError,match='다른 서버'):DurableWorkflows(service)
    finally:queue.close()
def test_close_interruption_is_not_success(service,monkeypatch):
    service,source=service;queue=DurableWorkflows(service);monkeypatch.setattr(queue,'_command',lambda p:[sys.executable,'-c','import time;time.sleep(25)'])
    task=submit(queue,source);wait(queue,task['workflow_id'],{'RUNNING'});queue.close();reopened=DurableWorkflows(service)
    try:assert reopened.get(task['workflow_id'])['state']=='INTERRUPTED'
    finally:reopened.close()
def test_planner_is_fail_closed_and_steps_are_allowlisted(tmp_path):
    with pytest.raises(ValueError,match='LOCAL_GENERATIVE_MODEL_UNAVAILABLE'):make_plan(tmp_path,{'command':'밝게 편집 후 나레이션과 MP4'})
    with pytest.raises(ValueError):validate_steps([{'operation':'shell','command':'anything'}])
    with pytest.raises(ValueError):validate_steps([{'operation':'video_edit','options':{'command':'anything'}}])
    with pytest.raises(ValueError):validate_steps([{'operation':'mix_narration'}])
    plan=make_plan(tmp_path,{'steps':[{'operation':'narrate','text':'한국어 원고'}]})
    assert plan['plan_source']=='STRUCTURED_USER_PLAN_NOT_GENERATIVE';assert plan['plan_id']

def test_queued_cancel_has_no_attempt(service):
    service,source=service;queue=DurableWorkflows(service)
    try:
        with queue.lock:
            task=submit(queue,source);assert queue.cancel(task['workflow_id'])['state']=='CANCELLED'
        assert queue.get(task['workflow_id'])['attempts']==[]
    finally:queue.close()

def test_retry_is_bounded_to_three_attempts(service,monkeypatch):
    service,source=service;queue=DurableWorkflows(service)
    monkeypatch.setattr(queue,'_command',lambda p:[sys.executable,'-c',"import pathlib,json;pathlib.Path(__import__('sys').argv[1]).write_text(json.dumps({'error':'injected transient','retryable':True}))",str(p.parent/'response.json')])
    try:
        task=submit(queue,source);result=wait(queue,task['workflow_id']);assert result['state']=='FAILED';assert len(result['attempts'])==3
    finally:queue.close()

def test_interrupted_commit_rolls_back_previous_exact_bytes(service):
    service,source=service;saved=service.save_project({'job_ids':[source['job_id']]});path=service.projects/(saved['project_id']+'.json');original=path.read_text(encoding='utf-8')
    queue=DurableWorkflows(service)
    try:
        with queue.lock:
            task=submit(queue,source,project_id=saved['project_id']);task['state']='RUNNING';queue._put(task)
            replaced=json.loads(original);replaced['workflow_id']=task['workflow_id'];path.write_text(json.dumps(replaced),encoding='utf-8')
    finally:queue.close()
    reopened=DurableWorkflows(service)
    try:assert reopened.get(task['workflow_id'])['state']=='INTERRUPTED';assert path.read_text(encoding='utf-8')==original
    finally:reopened.close()

def test_sealed_results_survive_native_attempt_file_change(service):
    service,source=service;queue=DurableWorkflows(service)
    try:
        task=submit(queue,source);result=wait(queue,task['workflow_id']);assert result['state']=='SUCCEEDED'
        published=Path(result['result']['primary_output']['path']);original=published.read_bytes();assert '/sealed/' in published.as_posix()
        native=queue.root/task['workflow_id']/'00-1/jobs'/result['result']['job_id']/'edited_video.mp4'
        native.write_bytes(b'encoder staging changed')
        assert published.read_bytes()==original
        assert not queue.published_file(task['workflow_id'],native)
        assert queue.published_file(task['workflow_id'],published)
        with zipfile.ZipFile(service.export_project(result['project_id'])['export']['path']) as archive:assert archive.testzip() is None
    finally:queue.close()

@pytest.mark.parametrize('aspect,size',[('9:16',(360,640)),('16:9',(640,360))])
def test_explicit_video_ratios_preserve_original_bytes(service,aspect,size):
    from media_ai.workflow_worker import probe
    service,source=service;path=Path(source['primary_output']['path']);original=path.read_bytes()
    edited=service.edit_video({'filename':'input.mp4','content_base64':base64.b64encode(original).decode(),'options':{'aspect':aspect}})
    stream=next(s for s in probe(Path(edited['primary_output']['path']))['streams'] if s['codec_type']=='video')
    assert (stream['width'],stream['height'])==size;assert path.read_bytes()==original

def test_packaged_engine_manifest_resolves_without_employee_setup(tmp_path,monkeypatch):
    from media_ai.workflow_worker import engines_config
    package=tmp_path/'package';package.mkdir();data=tmp_path/'data';data.mkdir()
    (package/'RUNTIME_ENGINES.json').write_text(json.dumps({'tts':{'engine':'espeak-ng','executable':'tools/espeak-ng/espeak-ng.exe','data_path':'tools/espeak-ng'}}))
    monkeypatch.setenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',str(package))
    configured=engines_config(data)
    assert configured['tts']['executable']==str(package/'tools/espeak-ng/espeak-ng.exe')
    (package/'RUNTIME_ENGINES.json').write_text(json.dumps({'tts':{'executable':'../outside.exe'}}))
    with pytest.raises(ValueError,match='OUTSIDE_PACKAGE'):engines_config(data)

def test_unpublished_workflow_records_not_loaded_as_success(service):
    from media_ai.durable_workflows import is_published
    service,source=service
    fake=dict(source,job_id='not-published',workflow_id='not-completed')
    folder=service.jobs/fake['job_id'];folder.mkdir();(folder/'JOB_EVIDENCE.json').write_text(json.dumps(fake))
    assert not is_published(service.root,'not-completed')
    assert fake['job_id'] not in ProductJobService(service.root,'').records
