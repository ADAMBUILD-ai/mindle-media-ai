"""Persistent, single-owner product workflows; attempts are private until commit."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from uuid import uuid4, UUID

TERMINAL = {'SUCCEEDED', 'FAILED', 'CANCELLED', 'INTERRUPTED'}
OPERATIONS = {'video_edit', 'transcribe', 'narrate', 'mix_narration', 'apply_subtitles'}
EDIT_OPTIONS = {'brightness','contrast','saturation','subtitle','subtitleSegments','volume','mute','aspect','duration','start','speed','fade','effect','rotate','denoise','stabilize'}

def validate_steps(steps):
    if not isinstance(steps,list) or not 1<=len(steps)<=8: raise ValueError('1~8개 실제 작업 단계가 필요합니다.')
    result=[]
    for number,step in enumerate(steps):
        if not isinstance(step,dict) or step.get('operation') not in OPERATIONS: raise ValueError('지원하지 않는 실행 계획입니다.')
        if set(step)-{'operation','options','text','volume','original_volume','background_volume','length_policy','step_id','voice_job_id'}: raise ValueError('실행 계획에 허용되지 않은 필드가 있습니다.')
        item=dict(step);item['step_id']=str(UUID(step['step_id'])) if step.get('step_id') else str(uuid4())
        if any(s['step_id']==item['step_id'] for s in result):raise ValueError('중복 단계ID입니다.')
        options=item.get('options',{})
        if not isinstance(options,dict) or set(options)-EDIT_OPTIONS: raise ValueError('지원하지 않는 영상 옵션입니다.')
        if options.get('aspect') not in {None,'','original','16:9','9:16'}:raise ValueError('지원하는 영상 비율은 원본·16:9·9:16입니다.')
        if step['operation']=='narrate' and (not isinstance(step.get('text'),str) or not 1<=len(step['text'].strip())<=3000): raise ValueError('나레이션 원고는 1~3000자입니다.')
        if step['operation']=='apply_subtitles' and not any(s['operation']=='transcribe' for s in result):raise ValueError('받아쓰기 단계가 먼저 필요합니다.')
        if step['operation']=='mix_narration' and not any(s['operation']=='narrate' for s in result) and not step.get('voice_job_id'): raise ValueError('음성 생성 단계가 먼저 필요합니다.')
        if step.get('length_policy','reject') not in {'reject','extend_video'}: raise ValueError('음성 길이 정책을 확인하세요.')
        if step.get('voice_job_id'):item['voice_job_id']=str(UUID(step['voice_job_id']))
        for field in ('volume','original_volume','background_volume'):
            if field in step and not 0<=float(step[field])<=2: raise ValueError('음량은0~2 범위입니다.')
        result.append(item)
    return result

def is_published(root, identifier):
    if not identifier:return True
    database=Path(root)/'workflows/queue.sqlite3'
    if not database.is_file():return False
    try:
        with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as connection:
            row=connection.execute('SELECT state FROM workflows WHERE id=?',(identifier,)).fetchone()
            return row is not None and row[0]=='SUCCEEDED'
    except sqlite3.Error:return False

class DurableWorkflows:
    def __init__(self,service):
        self.service=service;self.root=service.root/'workflows';self.root.mkdir(exist_ok=True)
        self.lock=threading.RLock();self.wake=threading.Event();self.closed=False;self.process=None
        self.owner=(self.root/'owner.lock').open('a+b');self.owner.seek(0)
        if self.owner.read(1)==b'':self.owner.write(b'0');self.owner.flush()
        self.owner.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(self.owner.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(self.owner,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError:self.owner.close();raise RuntimeError('다른 서버가 이 작업 큐를 사용하고 있습니다.')
        self.db=sqlite3.connect(self.root/'queue.sqlite3',check_same_thread=False)
        self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS workflows (id TEXT PRIMARY KEY, request_key TEXT UNIQUE, fingerprint TEXT, state TEXT, body TEXT, updated REAL)')
        with self.lock:
            for identifier,body in self.db.execute("SELECT id,body FROM workflows WHERE state IN ('RUNNING','RETRY_WAIT','CANCEL_REQUESTED')").fetchall():
                value=json.loads(body);self._rollback(value);value['state']='INTERRUPTED';value['error']='서버 중단. 완료되지 않은 작업은 재개 전 확인해야 합니다.';self._put(value)
        self.thread=threading.Thread(target=self._loop,name='mindle-workflow',daemon=True);self.thread.start()

    def _put(self,value):
        value['updated_at']=time.time();self.db.execute('UPDATE workflows SET state=?,body=?,updated=? WHERE id=?',(value['state'],json.dumps(value,ensure_ascii=False),value['updated_at'],value['workflow_id']));self.db.commit()
    def get(self,identifier):
        with self.lock:
            row=self.db.execute('SELECT body FROM workflows WHERE id=?',(str(UUID(identifier)),)).fetchone()
            if not row:raise ValueError('작업을 찾을 수 없습니다.')
            return json.loads(row[0])
    def list(self):
        with self.lock:return [json.loads(r[0]) for r in self.db.execute('SELECT body FROM workflows ORDER BY updated DESC LIMIT 100')]
    def busy(self):
        with self.lock:return self.db.execute("SELECT 1 FROM workflows WHERE state IN ('QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED') LIMIT 1").fetchone() is not None
    def submit(self,payload):
        source=self.service.records.get(payload.get('input_job_id'))
        if not source or source.get('status')!='TESTED_PASS' or source.get('lane')!='video':raise ValueError('완료된 실제 영상 입력이 필요합니다.')
        from .product_runtime import file_record
        actual=file_record(Path(source.get('preview_output',source['primary_output'])['path']))
        if actual['sha256']!=source.get('preview_output',source['primary_output'])['sha256']:raise ValueError('영상 입력 해시가 달라졌습니다.')
        steps=validate_steps(payload.get('steps'))
        previous_path=self.service.projects/(clean_id+'.json') if (clean_id:=str(UUID(payload['project_id'])) if payload.get('project_id') else None) else None
        previous=json.loads(previous_path.read_text(encoding='utf-8')) if previous_path and previous_path.is_file() else None
        previous_sha=hashlib.sha256(previous_path.read_bytes()).hexdigest() if previous else None
        plan={'plan_source':'STRUCTURED_USER_PLAN_NOT_GENERATIVE'}
        if payload.get('plan_id'):
            plan=json.loads((self.root/'plans'/(str(UUID(payload['plan_id']))+'.json')).read_text(encoding='utf-8'))
            if [{k:v for k,v in item.items() if k!='step_id'} for item in plan['steps']]!=[{k:v for k,v in item.items() if k!='step_id'} for item in steps]:raise ValueError('생성된 계획과 실행 단계가 다릅니다.')
        request_key=str(payload.get('request_id') or uuid4())
        if len(request_key)>128:raise ValueError('요청ID가 너무 깁니다.')
        clean={'input_job_id':source['job_id'],'input_sha256':actual['sha256'],'steps':[{k:v for k,v in s.items() if k!='step_id'} for s in steps],
               'workspace':payload.get('workspace'),'job_ids':list(dict.fromkeys(payload.get('job_ids',[]))),'background':payload.get('background'), 'project_id':str(UUID(payload['project_id'])) if payload.get('project_id') else str(uuid4()),'export':bool(payload.get('export',True))}
        base_records=[self.service.records.get(identifier) for identifier in clean['job_ids']]
        if any(not r or r.get('status')!='TESTED_PASS' for r in base_records):raise ValueError('저장할 완료 작업을 찾을 수 없습니다.')
        for step in steps:
            if step.get('voice_job_id'):
                voice=self.service.records.get(step['voice_job_id'])
                if not voice or voice.get('operation')!='narration' or voice.get('status')!='TESTED_PASS':raise ValueError('완료된 나레이션을 찾을 수 없습니다.')
                if not any(r['job_id']==voice['job_id'] for r in base_records):base_records.append(voice)
        # A generated project UUID must not defeat replay of the same new-project request.
        fingerprint=hashlib.sha256(json.dumps({**clean,'project_id':payload.get('project_id')},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        with self.lock:
            row=self.db.execute('SELECT fingerprint,body FROM workflows WHERE request_key=?',(request_key,)).fetchone()
            if row:
                if row[0]!=fingerprint:raise ValueError('같은 요청ID에 다른 작업을 보낼 수 없습니다.')
                return json.loads(row[1])
            active=self.db.execute("SELECT 1 FROM workflows WHERE state IN ('QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED') LIMIT 1").fetchone()
            if active:raise ValueError('현재 프로젝트 작업이 끝난 뒤 새 작업을 요청하세요.')
            value={**clean,'workflow_id':str(uuid4()),'request_id':request_key,'state':'QUEUED','steps':steps,'records':[], 'attempts':[], 'created_at':time.time(),'current_step':0,'input_record':source,'plan_receipt':plan,'base_records':base_records,'previous_project':previous,'previous_project_sha256':previous_sha,'previous_project_raw':previous_path.read_text(encoding='utf-8') if previous else None}
            if payload.get('workspace') is not None:
                from .product_runtime import ProductJobService
                workspace_service=ProductJobService(self.root/value['workflow_id']/'workspace-inputs','')
                value['workspace']=workspace_service._save_workspace(value['project_id'],payload['workspace'])
            if payload.get('background'):
                import base64
                background=payload['background']
                if not isinstance(background,dict) or len(str(background.get('content_base64','')))>45000000:raise ValueError('BGM 입력이 너무 큽니다.')
                raw=base64.b64decode(background['content_base64'],validate=True)
                if not raw or len(raw)>32*1024*1024:raise ValueError('BGM은1~32MB입니다.')
                suffix=Path(background['filename']).suffix.lower()
                if suffix not in {'.wav','.mp3','.m4a','.flac','.ogg'}:raise ValueError('BGM 형식이 올바르지 않습니다.')
                folder=self.root/value['workflow_id'];folder.mkdir();audio=folder/('background'+suffix);audio.write_bytes(raw)
                from .workflow_worker import probe
                if not any(s['codec_type']=='audio' for s in probe(audio)['streams']):raise ValueError('BGM 오디오 스트림이 없습니다.')
                value['background']=file_record(audio)
            self.db.execute('INSERT INTO workflows VALUES(?,?,?,?,?,?)',(value['workflow_id'],request_key,fingerprint,value['state'],json.dumps(value,ensure_ascii=False),time.time()));self.db.commit();self.wake.set();return value
    def cancel(self,identifier):
        with self.lock:
            value=self.get(identifier)
            if value['state'] in TERMINAL:return value
            value['state']='CANCELLED' if value['state']=='QUEUED' else 'CANCEL_REQUESTED';self._put(value);self.wake.set();return value
    def _stop_process(self,process):
        if process.poll() is not None:return
        if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=10)
        else:
            try:os.killpg(process.pid,signal.SIGTERM)
            except ProcessLookupError:pass
        try:process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            if os.name!='nt':
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
            process.wait(timeout=3)
    def _loop(self):
        while not self.closed:
            with self.lock:
                row=self.db.execute("SELECT id FROM workflows WHERE state='QUEUED' ORDER BY updated LIMIT 1").fetchone()
            if not row:self.wake.wait(.2);self.wake.clear();continue
            try:self._run(row[0])
            except Exception as error:
                with self.lock:
                    value=self.get(row[0]);self._rollback(value);value.update(state='INTERRUPTED' if self.closed else 'FAILED',error=str(error));self._put(value)
    def _command(self,path):return [sys.executable,'-B','-X','utf8','-m','media_ai.workflow_worker',str(path)]
    def _run(self,identifier):
        with self.lock:
            value=self.get(identifier)
            if value['state']!='QUEUED':return
            value['state']='RUNNING';self._put(value)
        for index,step in enumerate(value['steps']):
            for attempt in range(1,4):
                with self.lock:
                    value=self.get(identifier)
                    if self.closed or value['state']=='CANCEL_REQUESTED':self._finish_cancel(value);return
                    value.update(state='RUNNING',current_step=index)
                    folder=self.root/identifier/f'{index:02d}-{attempt}';folder.mkdir(parents=True,exist_ok=False)
                    request={'root':str(folder),'step':step,'input_record':value['input_record'],'records':value['records'],'base_records':value.get('base_records',[]),'parent_pid':os.getpid(),'engines':__import__('media_ai.workflow_worker',fromlist=['engines_config']).engines_config(self.service.root),'background':value.get('background')}
                    path=folder/'request.json';path.write_text(json.dumps(request,ensure_ascii=False),encoding='utf-8')
                    receipt={'step_id':step['step_id'],'attempt':attempt,'started_at':time.time(),'state':'RUNNING'};value['attempts'].append(receipt);self._put(value)
                environment=dict(os.environ);environment['PYTHONPATH']=str(Path(__file__).resolve().parents[1])+os.pathsep+environment.get('PYTHONPATH','')
                with (folder/'worker.log').open('wb') as log:
                    process=subprocess.Popen(self._command(path),stdout=log,stderr=subprocess.STDOUT,env=environment,
                        start_new_session=os.name!='nt',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name=='nt' else 0)
                    self.process=process;deadline=time.monotonic()+900
                    with self.lock:
                        live=self.get(identifier);live['attempts'][-1]['worker_pid']=process.pid;self._put(live)
                    while process.poll() is None:
                        with self.lock:cancel=self.closed or self.get(identifier)['state']=='CANCEL_REQUESTED'
                        if cancel or time.monotonic()>deadline:self._stop_process(process);break
                        self.wake.wait(.05);self.wake.clear()
                    self.process=None
                with self.lock:
                    value=self.get(identifier);receipt=value['attempts'][-1];receipt['finished_at']=time.time();receipt['worker_pid']=process.pid;receipt['returncode']=process.returncode
                    if self.closed or value['state']=='CANCEL_REQUESTED':receipt['state']='CANCELLED';self._finish_cancel(value);return
                    response_path=folder/'response.json'
                    response=json.loads(response_path.read_text(encoding='utf-8')) if response_path.exists() else {'error':'worker exited without a result','retryable':False}
                    if process.returncode==0 and response.get('record'):
                        record=response['record'];self._verify_record(record);record=self._seal_record(record,folder);value['records'].append(record);receipt['state']='SUCCEEDED';self._put(value);break
                    receipt['state']='FAILED';value['error']=response.get('error','worker failed')
                    if not response.get('retryable') or attempt==3:value['state']='FAILED';self._put(value);return
                    value['state']='RETRY_WAIT';receipt['retry_after_seconds']=attempt;self._put(value)
                end=time.monotonic()+attempt
                while time.monotonic()<end and not self.closed:
                    self.wake.wait(min(.1,end-time.monotonic()));self.wake.clear()
                    with self.lock:
                        value=self.get(identifier)
                        if value['state']=='CANCEL_REQUESTED':self._finish_cancel(value);return
        with self.lock:
            value=self.get(identifier)
            if self.closed or value['state']=='CANCEL_REQUESTED':self._finish_cancel(value);return
            # Save/Export operate on an isolated service catalog until every file verifies.
            from .product_runtime import ProductJobService
            staging=ProductJobService(self.root/identifier/'commit','')
            previous=value.get('previous_project')
            destination=self.service.projects/(value['project_id']+'.json')
            if previous:
                if not destination.is_file() or hashlib.sha256(destination.read_bytes()).hexdigest()!=value['previous_project_sha256']:raise ValueError('저장된 프로젝트가 변경됐습니다. 이전 파일을 덮어쓰지 않습니다.')
                (staging.projects/destination.name).write_text(json.dumps(previous,ensure_ascii=False),encoding='utf-8')
            elif destination.exists():raise ValueError('같은 프로젝트 파일이 새로 생성됐습니다. 덮어쓰지 않습니다.')
            if value.get('workspace') is not None:
                base_project=dict(previous or {});base_project['workspace']=value['workspace'];(staging.projects/destination.name).write_text(json.dumps(base_project,ensure_ascii=False),encoding='utf-8')
            records=[*(previous or {}).get('jobs',[]),*value.get('base_records',[]),value['input_record'],*value['records']]
            staging.records={r['job_id']:r for r in records}
            saved=staging.save_project({'project_id':value['project_id'],'job_ids':list(staging.records)})
            published_project=Path(saved['project']['path']);project_value=json.loads(published_project.read_text(encoding='utf-8'));project_value['workflow_id']=identifier;published_project.write_text(json.dumps(project_value,ensure_ascii=False),encoding='utf-8')
            exported=staging.export_project(value['project_id']) if value['export'] else None
            for record in value['records']:
                record['workflow_id']=identifier
                target=self.service.jobs/record['job_id'];target.mkdir(exist_ok=True)
                temp=target/'JOB_EVIDENCE.tmp';temp.write_text(json.dumps(record,ensure_ascii=False),encoding='utf-8');os.replace(temp,target/'JOB_EVIDENCE.json')
            project_source=Path(saved['project']['path']);project_target=self.service.projects/project_source.name
            # Never overwrite a pre-existing project until all workflow outputs and ZIP validate.
            temp=project_target.with_suffix('.workflow.tmp');temp.write_bytes(project_source.read_bytes());os.replace(temp,project_target)
            value.update(state='SUCCEEDED',result=next((r for r in reversed(value['records']) if r['lane']=='video'),value['input_record']),project_id=saved['project_id'],export=exported,finished_at=time.time());self._put(value)
            for record in value['records']:self.service.records[record['job_id']]=record
    def _rollback(self,value):
        path=self.service.projects/(value['project_id']+'.json')
        if not path.is_file():return
        try:owned=json.loads(path.read_text(encoding='utf-8')).get('workflow_id')==value['workflow_id']
        except (OSError,ValueError):return
        if not owned:return
        if value.get('previous_project_raw') is not None:
            temp=path.with_suffix('.rollback.tmp');temp.write_text(value['previous_project_raw'],encoding='utf-8');os.replace(temp,path)
        else:path.unlink()
    def _seal_record(self,record,attempt):
        from .product_runtime import file_record
        # Publish byte-verified snapshots, never the paths held by encoder processes.
        folder=attempt/'sealed'/record['job_id'];folder.mkdir(parents=True,exist_ok=False)
        mapped={}
        for field in ['input','primary_output','preview_output','outputs']:
            items=record.get(field,[]) if field=='outputs' else [record.get(field)]
            updated=[]
            for item in items:
                if not item:continue
                source=Path(item['path'])
                if str(source) not in mapped:
                    content=source.read_bytes()
                    if len(content)!=item['bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']:raise ValueError('출력 게시 중 원본 해시가 달라졌습니다.')
                    destination=folder/source.name
                    if destination.exists():raise ValueError('봉인 파일명이 중복되었습니다.')
                    temp=destination.with_suffix(destination.suffix+'.tmp');temp.write_bytes(content);os.replace(temp,destination)
                    mapped[str(source)]=file_record(destination)
                updated.append({**item,**mapped[str(source)]})
            if updated:record[field]=updated if field=='outputs' else updated[0]
        record['sealed_artifacts']=True
        return record
    def published_file(self,identifier,path):
        value=self.get(identifier)
        if value['state']!='SUCCEEDED':return False
        allowed=[]
        for record in value['records']:
            allowed.extend(record.get('outputs',[]));allowed.extend(record.get(field) for field in ['input','primary_output','preview_output'] if record.get(field))
        workspace=value.get('workspace') or {}
        for lane in ('photo','video'):allowed.extend(workspace.get('references',{}).get(lane,[]))
        if workspace.get('audio'):allowed.append(workspace['audio'])
        if value.get('export'):allowed.append(value['export']['export'])
        return Path(path).resolve() in {Path(item['path']).resolve() for item in allowed}
    def _verify_record(self,record):
        from .product_runtime import file_record
        if record.get('status')!='TESTED_PASS':raise ValueError('미완료 출력을 게시할 수 없습니다.')
        for item in [record['primary_output'],*record['outputs']]:
            path=Path(item['path']).resolve()
            if self.root.resolve() not in path.parents:raise ValueError('작업 출력 경로가 작업영역 밖입니다.')
            actual=file_record(path)
            if actual['sha256']!=item['sha256'] or actual['bytes']!=item['bytes']:raise ValueError('작업 출력 해시가 다릅니다.')
    def _finish_cancel(self,value):
        value['state']='INTERRUPTED' if self.closed else 'CANCELLED';value['finished_at']=time.time();self._put(value)
    def close(self):
        self.closed=True;self.wake.set();self.thread.join(timeout=15)
        if self.thread.is_alive():raise RuntimeError('작업 프로세스가 아직 종료되지 않았습니다.')
        self.db.close()
        if os.name=='nt':
            import msvcrt
            self.owner.seek(0);msvcrt.locking(self.owner.fileno(),msvcrt.LK_UNLCK,1)
        self.owner.close()
