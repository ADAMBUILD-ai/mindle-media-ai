import base64,json,subprocess,sys,threading,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import pytest
from media_ai.product_server import create_server


def call(base,path,body=None,headers=None):
    request=Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
    with urlopen(request,timeout=10) as r:return r.status,json.load(r)

def test_actual_http_cancel_busy_shutdown_and_private_output(tmp_path,monkeypatch):
    repo=Path(__file__).resolve().parents[1];server=create_server(repo,tmp_path/'data','');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base='http://127.0.0.1:'+str(server.server_port)
    try:
        video=tmp_path/'fixture.mp4';subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=160x90:r=10','-t','1','-c:v','libx264','-pix_fmt','yuv420p','-y',str(video)],check=True)
        _,record=call(base,'/api/media/import',{'kind':'video','filename':'input.mp4','content_base64':base64.b64encode(video.read_bytes()).decode()})
        _,saved=call(base,'/api/projects/save',{'job_ids':[record['job_id']]});project=server.service.projects/(saved['project_id']+'.json');before=project.read_bytes()
        queue=server.workflow_queue();normal=queue._command
        monkeypatch.setattr(queue,'_command',lambda p:[sys.executable,'-c',"import pathlib,time,sys;pathlib.Path(sys.argv[1]).write_bytes(b'private incomplete MP4');time.sleep(25)",str(p.parent/'partial.mp4')])
        body={'request_id':'cancel-http','project_id':saved['project_id'],'input_job_id':record['job_id'],'steps':[{'operation':'video_edit','options':{'brightness':10}}]}
        status,task=call(base,'/api/workflows',body);assert status==202
        end=time.monotonic()+5
        while time.monotonic()<end:
            _,task=call(base,'/api/workflows/'+task['workflow_id'])
            if task['attempts'] and task['attempts'][-1].get('worker_pid'):break
            time.sleep(.02)
        with pytest.raises(HTTPError) as blocked:call(base,'/files/workflows/'+task['workflow_id']+'/00-1/partial.mp4')
        assert blocked.value.code==403
        _,control=call(base,'/api/runtime/control')
        with pytest.raises(HTTPError) as busy:call(base,'/api/runtime/shutdown',{'server_pid':control['server_pid'],'server_instance_id':control['server_instance_id']},{'X-Mindle-Control':control['control_nonce']})
        assert busy.value.code==409
        with pytest.raises(HTTPError):call(base,'/api/projects/save',{'job_ids':[record['job_id']]})
        _,cancel=call(base,'/api/workflows/'+task['workflow_id']+'/cancel',{});assert cancel['state']=='CANCEL_REQUESTED'
        end=time.monotonic()+5
        while time.monotonic()<end:
            _,value=call(base,'/api/workflows/'+task['workflow_id'])
            if value['state']=='CANCELLED':break
            time.sleep(.02)
        assert value['state']=='CANCELLED';assert value['attempts'][-1]['returncode']!=0;assert project.read_bytes()==before
        assert len(call(base,'/api/assets')[1]['assets'])==1
        monkeypatch.setattr(queue,'_command',normal);body['request_id']='after-cancel';_,next_task=call(base,'/api/workflows',body)
        end=time.monotonic()+10
        while time.monotonic()<end:
            _,value=call(base,'/api/workflows/'+next_task['workflow_id'])
            if value['state'] in {'SUCCEEDED','FAILED'}:break
            time.sleep(.02)
        assert value['state']=='SUCCEEDED',value
        assert call(base,'/api/projects/'+saved['project_id'])[1]['project']['workflow_id']==next_task['workflow_id']
    finally:server.shutdown();thread.join();server.server_close()

def test_workflow_foreign_origin_and_unknown_operation_rejected(tmp_path):
    server=create_server(Path(__file__).resolve().parents[1],tmp_path/'data','');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base='http://127.0.0.1:'+str(server.server_port)
    try:
        with pytest.raises(HTTPError) as e:call(base,'/api/workflows/plan',{'steps':[{'operation':'narrate','text':'한국어'}]},{'Origin':'https://foreign.invalid'})
        assert e.value.code==403
        with pytest.raises(HTTPError) as e:call(base,'/api/workflows/plan',{'steps':[{'operation':'shell'}]})
        assert e.value.code==422
        with pytest.raises(HTTPError) as e:call(base,'/api/workflows/plan',{'command':'생성형 계획으로 편집'})
        assert e.value.code==422;assert 'LOCAL_GENERATIVE_MODEL_UNAVAILABLE' in json.load(e.value)['error']
    finally:server.shutdown();thread.join();server.server_close()
