"""Source-only owner-input acceptance orchestrator using the unchanged product HTTP API.

No downloading, installation, model substitution, package build or fixture generation.
A technical completion always leaves human/Windows-candidate acceptance pending.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from uuid import uuid4
import zipfile
from .e2e_intake import intake_result, write_result
from .product_runtime import file_record
from .workflow_worker import tree_sha, probe

STAGES=('intake','engine_identity','import_and_ranges','qwen_scene_plan','assembly','qwen_audio_plan',
        'supertonic_and_mix','output_quality','save','cold_restart','reopen','export')
MODEL_SHA='dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db'
PART_SHA='539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a'
REVISION='bb5d59e06d9551d752d08b292a50eb208b07ab1f'


def require(value,message):
    if not value:raise ValueError(message)


def config_from(path):
    path=Path(path).resolve();config=json.loads(path.read_text(encoding='utf-8-sig'))
    for kind in ('planner','tts'):
        for key in ('executable','data_path','model_path'):
            if config.get(kind,{}).get(key):config[kind][key]=str((path.parent/config[kind][key]).resolve())
        for item in config.get(kind,{}).get('additional_model_files',[]):item['path']=str((path.parent/item['path']).resolve())
    return config


def verify_engines(config):
    planner=config.get('planner',{});tts=config.get('tts',{})
    require(planner.get('model_sha256')==MODEL_SHA and planner.get('revision')==REVISION,'BLOCKED_MODEL_ADOPTION: pinned 7B required; no 1.5B substitution')
    parts=planner.get('additional_model_files',[])
    require(len(parts)==1 and parts[0].get('sha256')==PART_SHA,'BLOCKED_MODEL_ADOPTION: full split identity required')
    identities=[]
    for path,expected in [(planner.get('model_path',''),MODEL_SHA),(parts[0]['path'],PART_SHA),(planner.get('executable',''),planner.get('executable_sha256'))]:
        record=file_record(Path(path));require(record['sha256']==expected,'BLOCKED_ENGINE_IDENTITY: '+str(path));identities.append(record)
    require(bool(planner.get('runtime_sha256')) and tree_sha(Path(planner['executable']).parent)==planner['runtime_sha256'],'BLOCKED_PLANNER_RUNTIME_IDENTITY')
    require(type(planner.get('context_size')) is int and 512<=planner['context_size']<=32768 and bool(planner.get('license')),'BLOCKED_PLANNER_SETTINGS')
    require(tts.get('engine')=='sherpa-supertonic','BLOCKED_NEURAL_TTS_REQUIRED')
    module=importlib.import_module('sherpa_onnx')
    require(module.__version__==tts.get('runtime_version') and bool(tts.get('license')) and bool(tts.get('model_revision')),'BLOCKED_TTS_SETTINGS')
    require(tree_sha(Path(tts['data_path']))==tts.get('data_sha256') and tree_sha(Path(module.__file__).parent/'lib')==tts.get('runtime_sha256'),'BLOCKED_TTS_IDENTITY')
    return {'status':'PASS_IDENTITY_NOT_INFERENCE','planner':planner,'tts':tts,'files':identities}


class SourceSession:
    """Own exactly one child; stop via its authenticated product lifecycle API."""
    def __init__(self,repo,data,evidence):
        self.repo=Path(repo).resolve();self.data=Path(data).resolve();self.evidence=Path(evidence).resolve()
        self.process=None;self.base=None;self.control=None;self.log=None

    def call(self,path,body=None,headers=None):
        request=Request(self.base+path,data=None if body is None else json.dumps(body,ensure_ascii=False).encode('utf-8'),
                        headers={'Content-Type':'application/json',**(headers or {})})
        try:
            with urlopen(request,timeout=180) as response:return json.load(response)
        except HTTPError as error:
            raise RuntimeError(f'PRODUCT_HTTP_{error.code} {path}: '+error.read().decode('utf-8','replace')) from error

    def start(self,label):
        require(self.process is None or self.process.poll() is not None,'OWNED_PROCESS_STILL_RUNNING')
        log_path=self.evidence/(label+'.log');self.log=log_path.open('wb')
        env={**os.environ,'PYTHONPATH':str(self.repo/'src'),'PYTHONUNBUFFERED':'1','HF_HUB_OFFLINE':'1','MINDLE_DEFER_EXTERNAL_SHORTFORM':'1'}
        # Never silently inherit a packaged model root instead of the explicit isolated config.
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
        self.process=subprocess.Popen([sys.executable,'-B','-X','utf8','-m','media_ai.product_server','--root',str(self.repo),
                                      '--data-dir',str(self.data),'--port','0'],cwd=self.repo,env=env,stdout=self.log,stderr=subprocess.STDOUT)
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            require(self.process.poll() is None,'PRODUCT_SERVER_EXITED: '+str(log_path))
            for line in log_path.read_text(encoding='utf-8',errors='replace').splitlines():
                if line.startswith('http://127.0.0.1:'):self.base=line.strip();break
            if self.base:
                try:
                    control=self.call('/api/runtime/control')
                    require(control['server_pid']==self.process.pid,'SERVER_PID_NOT_OWNED_CHILD')
                    self.control=control
                    return {key:value for key,value in control.items() if key!='control_nonce'}
                except (ConnectionError,OSError):pass
            time.sleep(.05)
        raise TimeoutError('PRODUCT_SERVER_START_TIMEOUT')

    def stop(self):
        require(self.process is not None and self.control is not None,'NO_OWNED_SERVER')
        identity={key:self.control[key] for key in ('server_pid','server_instance_id')}
        deadline=time.monotonic()+5
        while True:
            try:
                result=self.call('/api/runtime/shutdown',identity,{'X-Mindle-Control':self.control['control_nonce']});break
            except RuntimeError as error:
                # The previous response may arrive just before end_request runs.
                # Retry only this exact owned runtime's 409; never bypass busy.
                if 'PRODUCT_HTTP_409' not in str(error) or time.monotonic()>=deadline:raise
                time.sleep(.05)
        require(result['status']=='RUNTIME_STOPPING','PRODUCT_SHUTDOWN_NOT_ACCEPTED')
        self.process.wait(timeout=30)
        require(self.process.returncode==0,'PRODUCT_EXIT_FAILED')
        try:self.call('/api/runtime/control')
        except OSError:pass
        else:raise ValueError('OLD_ENDPOINT_STILL_RESPONDS')
        if self.log:self.log.close()
        self.base=None;return identity

    def cleanup(self):
        if self.process is None or self.process.poll() is not None:return
        # Cancel only this isolated run's tasks before requesting orderly shutdown.
        try:
            for route,key,id_key in [('/api/workflows','workflows','workflow_id'),('/api/architecture-agent/productions','productions','production_id')]:
                for task in self.call(route)[key]:
                    if task['state'] in {'QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED'}:self.call(route+'/'+task[id_key]+'/cancel',{})
            deadline=time.monotonic()+15
            while time.monotonic()<deadline:
                try:self.stop();return
                except RuntimeError as error:
                    if 'PRODUCT_HTTP_409' not in str(error):raise
                    time.sleep(.1)
        finally:
            if self.process.poll() is None:
                self.process.terminate();self.process.wait(timeout=10)
            if self.log:self.log.close()


def wait_task(session,route,identifier,output,timeout=600):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        task=session.call(route+'/'+identifier);write_result(output,task)
        if task['state'] in {'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED','BLOCKED_INPUT','BLOCKED_ASSET'}:
            require(task['state']=='SUCCEEDED','PRODUCT_TASK_FAILED: '+str(task.get('error',task['state'])))
            return task
        time.sleep(.2)
    session.call(route+'/'+identifier+'/cancel',{})
    raise TimeoutError('PRODUCT_TASK_TIMEOUT_CANCEL_REQUESTED')


def audio_command(manifest):
    volumes=manifest['volumes'];percent=lambda key:format(volumes[key]*100,'.12g')
    policy='영상 연장' if manifest['voice_length_policy']=='extend_video' else '원본 길이 유지'
    return f'"{manifest["narration_script"]}" 나레이션 음량 {percent("narration")}%, 원본 소리 음량 {percent("original")}%, BGM 음량 {percent("bgm")}%, {policy}'


def validate_audio_plan(manifest,plan):
    from .workflow_planner import validate_plan_scope
    require(plan.get('plan_source')=='LOCAL_GENERATIVE_INFERENCE','ACTUAL_AUDIO_QWEN_REQUIRED')
    steps=plan['steps'];validate_plan_scope(audio_command(manifest),steps)
    require([step['operation'] for step in steps]==['narrate','mix_narration'],'AUDIO_FINISH_MUST_BE_SINGLE_SYNTHESIS_AND_MIX')


def quality(path,manifest):
    info=probe(Path(path));video=next(x for x in info['streams'] if x['codec_type']=='video');audio=next(x for x in info['streams'] if x['codec_type']=='audio')
    duration=float(info['format']['duration'])
    require(video['codec_name']=='h264' and video.get('pix_fmt')=='yuv420p' and audio['codec_name']=='aac','OUTPUT_CODECS_FAILED')
    require(abs(video['width']/video['height']-16/9)<.002,'OUTPUT_ASPECT_FAILED')
    require(abs(duration-30)<=.15,'OUTPUT_NOT_EXACT_30_SECONDS: extended outputs cannot pass fixed-duration acceptance')
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,capture_output=True,timeout=180)
    return {'status':'PASS_TECHNICAL_ONLY','duration_seconds':duration,'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],
            'width':video['width'],'height':video['height'],'decoded_video_and_audio':True,'human_review':'NOT_EXECUTED'}


def verify_export(path,expected,project_id,expected_jobs=None):
    require(file_record(Path(path))['sha256']==expected,'EXPORT_ZIP_IDENTITY_FAILED')
    with zipfile.ZipFile(path) as archive:
        require(archive.testzip() is None,'EXPORT_CRC_FAILED')
        require(len(archive.namelist())==len(set(archive.namelist())),'EXPORT_DUPLICATE_ENTRIES')
        project=json.loads(archive.read('project.json'));bundle=json.loads(archive.read('BUNDLE_MANIFEST.json'))
        require(project['project_id']==bundle['project_id']==project_id,'EXPORT_PROJECT_IDENTITY_FAILED')
        if expected_jobs is not None:
            # HTTP Reopen adds transport URLs; compare every persisted job field.
            persisted=lambda jobs:[{key:value for key,value in job.items() if key not in {'preview_url','input_url','reference_urls'}} for job in jobs]
            require(persisted(project['jobs'])==persisted(expected_jobs),'EXPORT_REOPEN_JOB_IDENTITY_FAILED')
        require(bool(bundle['files']),'EXPORT_MANIFEST_EMPTY')
        for item in bundle['files']:
            data=archive.read(item['archive_path'])
            require(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],'EXPORT_INTERNAL_IDENTITY_FAILED: '+item['archive_path'])
    return {'status':'PASS','file_count':len(bundle['files']),'project_id':project_id,'sha256':expected}


def execute(session,manifest,intake,receipt,output):
    def begin(stage):
        receipt['active_stage']=stage;receipt['stages'][stage]={'status':'RUNNING'};write_result(output/'RUN_RECEIPT.json',receipt)
    def mark(stage,details=None):
        receipt['stages'][stage]={'status':'PASS','details':details};write_result(output/'RUN_RECEIPT.json',receipt)
    def unchanged():
        fresh=intake_result(intake['manifest_path'])
        require(fresh['status']=='PASS_INTAKE_TECHNICAL_ONLY' and fresh['manifest_sha256']==intake['manifest_sha256'],'INPUT_CHANGED_AFTER_PREFLIGHT')
    begin('import_and_ranges')
    source_files=lambda:{str(p.relative_to(session.repo)):file_record(p)['sha256'] for folder in ('src/media_ai','ui') for p in (session.repo/folder).rglob('*') if p.is_file() and p.suffix in {'.py','.js','.html','.css'}}
    source_snapshot=source_files();receipt['source_file_sha256']=source_snapshot
    first=session.start('FIRST_SOURCE_SERVER');receipt['first_process']=first
    identity=session.call('/api/runtime-identity');require(identity.get('head')==receipt['source_commit'],'SOURCE_HEAD_MISMATCH')
    write_result(output/'SOURCE_RUNTIME_IDENTITY.json',identity)
    imported=[]
    for item in (x for x in intake['verified_assets'] if x['role']=='video'):
        unchanged();path=Path(item['path']);payload={'kind':'video','filename':path.name,'content_base64':base64.b64encode(path.read_bytes()).decode('ascii')}
        job=session.call('/api/media/import',payload)
        require(job['primary_output']['sha256']==item['sha256'],'IMPORTED_SOURCE_IDENTITY_FAILED')
        start=item['usable_start_seconds'];end=item['usable_end_seconds']
        if start or abs(end-item['duration_seconds'])>.01:
            job=session.call('/api/video-edits',{**payload,'options':{'start':start,'duration':end-start}})
        imported.append(job)
    mark('import_and_ranges',[job['job_id'] for job in imported])
    project_id=str(uuid4());command='선택한 기존 영상 모두로 30초 16:9 건축 홍보 영상을 구성해 주세요.'
    begin('qwen_scene_plan')
    plan=session.call('/api/architecture-agent/plan',{'command':command,'project_id':project_id,'job_ids':[x['job_id'] for x in imported]})
    require(plan['plan_source']=='LOCAL_GENERATIVE_INFERENCE' and plan['model_sha256']==MODEL_SHA,'ACTUAL_SCENE_QWEN_REQUIRED')
    write_result(output/'ACTUAL_SCENE_PLAN.json',plan);mark('qwen_scene_plan',plan['plan_id'])
    begin('assembly')
    unchanged();task=session.call('/api/architecture-agent/productions',{'plan_id':plan['plan_id'],'request_id':str(uuid4())})
    assembled=wait_task(session,'/api/architecture-agent/productions',task['production_id'],output/'ACTUAL_ASSEMBLY.json')
    mark('assembly',assembled['receipt'])
    begin('qwen_audio_plan')
    command=audio_command(manifest);receipt['audio_command']=command
    plan=session.call('/api/workflows/plan',{'command':command});write_result(output/'ACTUAL_AUDIO_PLAN.json',plan)
    validate_audio_plan(manifest,plan);require(plan['model_sha256']==MODEL_SHA,'AUDIO_MODEL_CHANGED');mark('qwen_audio_plan',plan['plan_id'])
    begin('supertonic_and_mix')
    unchanged();bgm=next(x for x in intake['verified_assets'] if x['role']=='audio');path=Path(bgm['path'])
    task=session.call('/api/workflows',{'request_id':str(uuid4()),'plan_id':plan['plan_id'],'input_job_id':assembled['receipt']['job_id'],
        'project_id':project_id,'job_ids':[x['job_id'] for x in imported],
        'steps':[{key:value for key,value in step.items() if key!='step_id'} for step in plan['steps']],
        'background':{'filename':path.name,'content_base64':base64.b64encode(path.read_bytes()).decode('ascii')},'export':True})
    finish=wait_task(session,'/api/workflows',task['workflow_id'],output/'ACTUAL_AUDIO_WORKFLOW.json')
    voice=next(x for x in finish['records'] if x['operation']=='narration')
    require(voice['runtime_result'].get('model_inference') is True and 'Supertonic' in voice['runtime_result'].get('engine',''),'ACTUAL_SUPERTONIC_REQUIRED')
    require(voice['runtime_result']['text']==manifest['narration_script'],'VOICE_SCRIPT_CHANGED')
    mixed=finish['result'];options=mixed['runtime_result']['options'];volumes=manifest['volumes']
    require(options['narration_job_id']==voice['job_id'] and options['narrationVolume']==volumes['narration'] and options['originalVolume']==volumes['original'] and options['backgroundVolume']==volumes['bgm'],'MIX_IDENTITY_OR_VOLUMES_CHANGED')
    mark('supertonic_and_mix',{'voice_job_id':voice['job_id'],'workflow_id':finish['workflow_id']})
    begin('output_quality')
    record=file_record(Path(mixed['primary_output']['path']));require(record['sha256']==mixed['primary_output']['sha256'],'FINAL_OUTPUT_CHANGED')
    mark('output_quality',quality(record['path'],manifest));receipt['final_mp4']=record
    begin('save')
    saved=session.call('/api/projects/'+project_id)['project'];mark('save',project_id)
    begin('cold_restart')
    before={x['job_id']:x['primary_output']['sha256'] for x in saved['jobs']};session.stop()
    after=session.start('COLD_SOURCE_SERVER')
    require(first['server_pid']!=after['server_pid'] and first['server_instance_id']!=after['server_instance_id'],'COLD_RESTART_IDENTITY_FAILED')
    receipt['second_process']=after;mark('cold_restart',{'first':first,'second':after})
    begin('reopen')
    reopened=session.call('/api/projects/'+project_id)['project']
    require(before=={x['job_id']:x['primary_output']['sha256'] for x in reopened['jobs']},'REOPEN_IDENTITY_FAILED')
    for job in reopened['jobs']:
        for item in job['outputs']:require(file_record(Path(item['path']))['sha256']==item['sha256'],'REOPEN_FILE_IDENTITY_FAILED')
    require(session.call('/api/workflows/'+finish['workflow_id'])['state']=='SUCCEEDED','REOPEN_WORKFLOW_CHANGED')
    mark('reopen',project_id)
    begin('export')
    exported=session.call('/api/projects/'+project_id+'/export',{})
    with urlopen(session.base+exported['download_url'],timeout=120) as response:(output/'AFTER_COLD_RESTART_EXPORT.zip').write_bytes(response.read())
    mark('export',verify_export(output/'AFTER_COLD_RESTART_EXPORT.zip',exported['export']['sha256'],project_id,reopened['jobs']))
    unchanged();require(source_snapshot==source_files(),'SOURCE_CHANGED_DURING_EXECUTION');session.stop()
    receipt.update(status='PASS_SOURCE_TECHNICAL_ONLY',overall='PARTIAL',human_visual_review='NOT_EXECUTED',human_audio_review='NOT_EXECUTED')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest',required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--engine-config');parser.add_argument('--execute',action='store_true');parser.add_argument('--source-sha')
    parser.add_argument('--windows-approval',help='Explicit isolated source evaluation authorization; never a Build Gate')
    args=parser.parse_args();output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=False)
    receipt={'work_id':'MEDIA-AI-CORE-E2E-R2-20261025','status':'PREPARING','overall':'PARTIAL','mode':'ISOLATED_SOURCE_ONLY',
             'package_build':False,'installed_models_changed':False,'full_product_pass':False,'owner_acceptance':False,
             'windows_candidate_acceptance':False,'stages':{key:{'status':'NOT_EXECUTED'} for key in STAGES}}
    session=None
    try:
        intake=intake_result(args.manifest);write_result(output/'INTAKE_RESULT.json',intake);write_result(output/'ASSET_INTAKE.json',intake)
        receipt['manifest_sha256']=intake['manifest_sha256'];receipt['stages']['intake']={'status':'PASS' if not intake['errors'] else 'BLOCKED','details':intake}
        require(not intake['errors'],'BLOCKED_ASSET_INTAKE')
        require(args.engine_config,'BLOCKED_ENGINE_CONFIG_REQUIRED')
        receipt['active_stage']='engine_identity';receipt['stages']['engine_identity']={'status':'RUNNING'}
        config=config_from(args.engine_config);identity=verify_engines(config);write_result(output/'ENGINE_IDENTITY.json',identity)
        receipt['stages']['engine_identity']={'status':'PASS','details':identity}
        if not args.execute:receipt['status']='PREPARED_NOT_EXECUTED';return
        repo=Path(__file__).resolve().parents[2]
        head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True,encoding='utf-8').strip()
        require(args.source_sha and head==args.source_sha,'EXPLICIT_FROZEN_SOURCE_REQUIRED')
        dirty=subprocess.check_output(['git','-C',str(repo),'status','--porcelain','--','src/media_ai','ui'],text=True,encoding='utf-8')
        require(not dirty.strip(),'DIRTY_EXECUTION_SOURCE_BLOCKED')
        require(manifest:=json.loads(Path(args.manifest).read_text(encoding='utf-8-sig')),'MANIFEST_REQUIRED')
        require(manifest.get('require_rights_evidence') is True,'R2_RIGHTS_EVIDENCE_REQUIRED')
        if os.name=='nt':
            require(args.windows_approval,'BLOCKED_WINDOWS_MODEL_ADOPTION_APPROVAL')
            approval=json.loads(Path(args.windows_approval).read_text(encoding='utf-8-sig'))
            config_sha=file_record(Path(args.engine_config))['sha256']
            require(approval.get('approved') is True and approval.get('scope')=='ISOLATED_SOURCE_ONLY' and approval.get('source_sha')==head and approval.get('manifest_sha256')==intake['manifest_sha256'] and approval.get('engine_config_sha256')==config_sha,'BLOCKED_WINDOWS_APPROVAL_BINDING')
        receipt['source_commit']=head;data=output/'isolated-product-data';data.mkdir()
        write_result(data/'runtime-engines.json',config)
        session=SourceSession(repo,data,output);execute(session,manifest,intake,receipt,output)
    except Exception as error:
        if receipt.get('active_stage'):
            receipt['stages'][receipt['active_stage']]={'status':'BLOCKED' if 'BLOCKED' in str(error) else 'FAIL','error':str(error)}
        receipt.update(status='BLOCKED' if 'BLOCKED' in str(error) or 'REQUIRED' in str(error) else 'FAILED',error=str(error),error_type=type(error).__name__)
    finally:
        if session:
            try:session.cleanup()
            except Exception as error:receipt['cleanup_error']=str(error);receipt['status']='FAILED'
        write_result(output/'RUN_RECEIPT.json',receipt);print(receipt['status'])
    return 0 if receipt['status'] in {'PASS_SOURCE_TECHNICAL_ONLY','PREPARED_NOT_EXECUTED'} else 2


if __name__=='__main__':raise SystemExit(main())
