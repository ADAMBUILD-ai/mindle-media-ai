"""Owner/PC execution runner for one verified 30-second architecture delivery.

It uses only product HTTP APIs. Missing intake stops before any server mutation.
It never builds a package, installs/replaces a model, or invents an asset value.
"""
from __future__ import annotations
import argparse,base64,hashlib,json,subprocess,time,urllib.error,urllib.request,uuid,zipfile
from datetime import datetime,timezone
from pathlib import Path
from media_ai.e2e_intake import validate_intake
from media_ai.source_e2e import audio_command,validate_audio_plan,verify_export,MODEL_SHA,PART_SHA,config_from
from media_ai.workflow_worker import tree_sha
import os,ctypes

TERMINAL={'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED','BLOCKED_INPUT','BLOCKED_ASSET'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block:=stream.read(1024*1024):h.update(block)
    return h.hexdigest()

def write(root,name,value):
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def now():return datetime.now(timezone.utc).isoformat()

def call(base,path,body=None,headers=None,timeout=180,raw=False):
    request=urllib.request.Request(base.rstrip('/')+path,
        data=None if body is None else json.dumps(body,ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type':'application/json',**(headers or {})})
    try:
        with urllib.request.urlopen(request,timeout=timeout) as response:
            return response.read() if raw else json.load(response)
    except urllib.error.HTTPError as error:
        detail=error.read().decode('utf-8','replace')
        raise RuntimeError(f'HTTP {error.code} {path}: {detail}') from error

def wait(base,path,identifier,timeout):
    end=time.monotonic()+timeout;value=call(base,path+'/'+identifier)
    while value.get('state') not in TERMINAL and time.monotonic()<end:
        time.sleep(.5);value=call(base,path+'/'+identifier)
    if value.get('state') not in TERMINAL:
        call(base,path+'/'+identifier+'/cancel',{})
        raise TimeoutError('PRODUCT_TASK_TIMEOUT_CANCEL_REQUESTED: '+path+'/'+identifier)
    return value

def launch(exe,expected_source,evidence,label):
    log=evidence/(label+'.log')
    with log.open('wb') as stream:subprocess.run([str(exe),'--no-browser'],stdout=stream,stderr=subprocess.STDOUT,timeout=1200,check=True)
    for _ in range(120):
        for port in range(18768,18778):
            base='http://127.0.0.1:'+str(port)
            try:
                identity=call(base,'/api/runtime-identity',timeout=2)
                if identity.get('runtime_mode')=='LOCAL_OFFLINE_PACKAGE' and identity.get('build_commit')==expected_source:
                    return base,identity
            except Exception:pass
        time.sleep(.5)
    raise RuntimeError('APPROVED_PACKAGE_ENDPOINT_NOT_FOUND')

def technical_probe(ffprobe,video):
    value=json.loads(subprocess.check_output([str(ffprobe),'-v','error','-show_streams','-show_format','-of','json',str(video)],text=True,encoding='utf-8',timeout=60))
    streams=value.get('streams',[]);v=next((x for x in streams if x.get('codec_type')=='video'),None);a=next((x for x in streams if x.get('codec_type')=='audio'),None)
    duration=float(value.get('format',{}).get('duration',0))
    if not v or not a or v.get('codec_name')!='h264' or v.get('pix_fmt')!='yuv420p' or a.get('codec_name')!='aac' or abs(duration-30)>.15:
        raise RuntimeError('FINAL_MEDIA_TECHNICAL_GATE_FAILED')
    if abs(v['width']/v['height']-16/9)>.002:raise RuntimeError('FINAL_MEDIA_ASPECT_GATE_FAILED')
    decoder=Path(ffprobe).with_name('ffmpeg.exe' if Path(ffprobe).suffix.lower()=='.exe' else 'ffmpeg')
    subprocess.run([str(decoder),'-v','error','-xerror','-i',str(video),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,capture_output=True,timeout=180)
    return {'decoded_video_and_audio':True,'duration_seconds':duration,'width':v.get('width'),'height':v.get('height'),'video_codec':v.get('codec_name'),'pixel_format':v.get('pix_fmt'),'audio_codec':a.get('codec_name')}

def pid_exited(pid):
    if os.name!='nt':
        try:os.kill(pid,0)
        except ProcessLookupError:return True
        return False
    from ctypes import wintypes
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
    kernel.CloseHandle.argtypes=[wintypes.HANDLE]
    handle=kernel.OpenProcess(0x1000,False,pid)
    if not handle:
        if ctypes.get_last_error() in (87,1168):return True
        raise RuntimeError('OLD_PID_EXIT_NOT_VERIFIABLE')
    try:
        code=wintypes.DWORD()
        if not kernel.GetExitCodeProcess(handle,ctypes.byref(code)):raise RuntimeError('OLD_PID_EXIT_NOT_VERIFIABLE')
        return code.value!=259
    finally:kernel.CloseHandle(handle)


def verify_candidate(identity,args,approval):
    if identity.get('build_commit')!=args.expected_source:raise RuntimeError('SOURCE_IDENTITY_MISMATCH')
    root=Path(identity['install_root']).resolve();manifest_path=root/'PACKAGE_MANIFEST.json'
    expected=approval['package_manifest_sha256']
    if sha(manifest_path)!=expected or identity.get('package_manifest_sha256')!=expected:raise RuntimeError('PACKAGE_SEAL_MISMATCH')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['build_commit']!=args.expected_source:raise RuntimeError('PACKAGE_SOURCE_MISMATCH')
    for item in manifest['files']:
        path=(root/item['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:
            raise RuntimeError('INSTALLED_PACKAGE_FILE_MISMATCH: '+item['path'])
    config=config_from(root/'RUNTIME_ENGINES.json');planner=config.get('planner',{});tts=config.get('tts',{})
    parts=planner.get('additional_model_files',[])
    if planner.get('model_sha256')!=MODEL_SHA or len(parts)!=1 or parts[0].get('sha256')!=PART_SHA:raise RuntimeError('PINNED_7B_REQUIRED_NO_1_5B_SUBSTITUTION')
    paths=[planner['model_path'],planner['executable'],parts[0]['path'],tts.get('data_path','')]
    if any(not Path(p).resolve().is_relative_to(root) for p in paths):raise RuntimeError('ENGINE_OUTSIDE_APPROVED_CANDIDATE')
    for path,expected_sha in [(planner['model_path'],MODEL_SHA),(parts[0]['path'],PART_SHA),(planner['executable'],planner.get('executable_sha256'))]:
        if sha(path)!=expected_sha:raise RuntimeError('CANDIDATE_MODEL_IDENTITY_FAILED')
    if tree_sha(Path(planner['executable']).parent)!=planner.get('runtime_sha256'):raise RuntimeError('CANDIDATE_PLANNER_RUNTIME_FAILED')
    if tts.get('engine')!='sherpa-supertonic' or not Path(tts['data_path']).is_dir() or tree_sha(Path(tts['data_path']))!=tts.get('data_sha256'):raise RuntimeError('CANDIDATE_SUPERTONIC_IDENTITY_FAILED')
    return config


def execute(args,manifest,intake,evidence):
    approval=json.loads(args.approval_file.read_text(encoding='utf-8-sig'))
    if not (approval.get('approved') is True and approval.get('scope')=='APPROVED_WINDOWS_CANDIDATE_E2E' and approval.get('source_sha')==args.expected_source and approval.get('manifest_sha256')==intake['manifest_sha256'] and approval.get('windows_7b_adoption_approved') is True):raise RuntimeError('BLOCKED_CANDIDATE_APPROVAL_BINDING')
    payload=args.exe.parent/'_payload/PACKAGE_MANIFEST.json'
    if not args.exe.is_file() or sha(args.exe)!=approval.get('candidate_exe_sha256') or not payload.is_file() or sha(payload)!=approval.get('package_manifest_sha256'):raise RuntimeError('BLOCKED_APPROVED_CANDIDATE_PAYLOAD_IDENTITY')
    def unchanged():
        if sha(args.manifest)!=intake['manifest_sha256'] or validate_intake(manifest,args.manifest.parent)['status']!='PASS_INTAKE_TECHNICAL_ONLY':raise RuntimeError('INPUT_CHANGED_AFTER_PREFLIGHT')
    unchanged()
    if manifest.get('require_rights_evidence') is not True:raise RuntimeError('R2_RIGHTS_EVIDENCE_REQUIRED')
    base,identity=(args.base_url,call(args.base_url,'/api/runtime-identity')) if args.base_url else launch(args.exe,args.expected_source,evidence,'01_LAUNCH')
    config=verify_candidate(identity,args,approval)
    write(evidence,'02_RUNTIME_IDENTITY.json',identity)
    jobs=[]
    for item in manifest['clips']:
        unchanged();path=(args.manifest.parent/item['path']).resolve()
        payload={'request_id':str(uuid.uuid4()),'kind':'video','filename':path.name,'content_base64':base64.b64encode(path.read_bytes()).decode()}
        job=call(base,'/api/media/import',{'request_id':str(uuid.uuid4()),'kind':'video','filename':path.name,'content_base64':base64.b64encode(path.read_bytes()).decode()})
        if job['input']['sha256']!=item['sha256']:raise RuntimeError('IMPORTED_INPUT_SHA_MISMATCH')
        start=item.get('usable_start_seconds',0);end=item.get('usable_end_seconds',item['duration_seconds'])
        if start or abs(end-item['duration_seconds'])>.01:job=call(base,'/api/video-edits',{**payload,'options':{'start':start,'duration':end-start}})
        jobs.append(job)
    project_id=str(uuid.uuid4())
    architecture_command='선택한 실제 영상 자료 모두로 30초 16:9 건축·리조트 홍보 영상을 구성해 주세요.'
    plan=call(base,'/api/architecture-agent/plan',{'command':architecture_command,'project_id':project_id,'job_ids':[x['job_id'] for x in jobs]})
    if plan.get('plan_source')!='LOCAL_GENERATIVE_INFERENCE' or plan.get('total_duration_seconds')!=30 or plan.get('aspect')!='16:9':raise RuntimeError('ARCHITECTURE_PLAN_CONTRACT_MISMATCH')
    if plan.get('model_sha256')!=MODEL_SHA:raise RuntimeError('ACTUAL_PINNED_7B_SCENE_PLAN_REQUIRED')
    if {x['sha256'] for x in plan.get('catalog',[])}!={x['primary_output']['sha256'] for x in jobs}:raise RuntimeError('PLAN_INPUT_BINDING_MISMATCH')
    write(evidence,'03_ARCHITECTURE_PLAN.json',plan)
    production=call(base,'/api/architecture-agent/productions',{'request_id':str(uuid.uuid4()),'plan_id':plan['plan_id']})
    production=wait(base,'/api/architecture-agent/productions',production['production_id'],args.task_timeout)
    write(evidence,'04_ARCHITECTURE_PRODUCTION.json',production)
    if production['state']!='SUCCEEDED':raise RuntimeError('ARCHITECTURE_PRODUCTION_'+production['state'])
    values=manifest['volumes'];policy=manifest['voice_length_policy'];script=manifest['narration_script']
    finish_command=audio_command(manifest)
    finish_plan=call(base,'/api/workflows/plan',{'command':finish_command})
    validate_audio_plan(manifest,finish_plan)
    if finish_plan.get('model_sha256')!=MODEL_SHA:raise RuntimeError('ACTUAL_PINNED_7B_AUDIO_PLAN_REQUIRED')
    unchanged()
    expected={'volume':values['narration'],'original_volume':values['original'],'backgroundVolume':values['bgm'],'length_policy':policy}
    if any(finish_plan.get('validated_edit_values',{}).get(k)!=v for k,v in expected.items()):raise RuntimeError('AUDIO_PLAN_CONTRACT_MISMATCH')
    write(evidence,'05_AUDIO_PLAN.json',finish_plan)
    bgm_path=(args.manifest.parent/manifest['bgm']['path']).resolve()
    workflow=call(base,'/api/workflows',{'request_id':str(uuid.uuid4()),'plan_id':finish_plan['plan_id'],'input_job_id':production['receipt']['job_id'],
        'project_id':production['receipt']['project_id'],'job_ids':[x['job_id'] for x in jobs]+[production['receipt']['job_id']],
        'steps':[{k:v for k,v in step.items() if k!='step_id'} for step in finish_plan['steps']],
        'background':{'filename':bgm_path.name,'content_base64':base64.b64encode(bgm_path.read_bytes()).decode()},'export':True})
    workflow=wait(base,'/api/workflows',workflow['workflow_id'],args.task_timeout)
    write(evidence,'06_AUDIO_WORKFLOW.json',workflow)
    if workflow['state']!='SUCCEEDED':raise RuntimeError('AUDIO_WORKFLOW_'+workflow['state'])
    voice=next(x for x in workflow['records'] if x.get('operation')=='narration')
    v=voice['runtime_result'];mix=workflow['result']['runtime_result']['options']
    if not (v.get('model_inference') is True and 'Supertonic' in v.get('engine','') and v.get('text')==script and v.get('voice_data_sha256')==config['tts']['data_sha256'] and v.get('runtime_sha256')==config['tts']['runtime_sha256']):raise RuntimeError('ACTUAL_SUPERTONIC_SCRIPT_IDENTITY_FAILED')
    if mix.get('narration_job_id')!=voice['job_id'] or mix.get('narrationVolume')!=values['narration'] or mix.get('originalVolume')!=values['original'] or mix.get('backgroundVolume')!=values['bgm']:raise RuntimeError('FINAL_MIX_IDENTITY_OR_VOLUMES_FAILED')
    unchanged()
    before_project=call(base,'/api/projects/'+workflow['project_id'])['project']
    result=workflow['result']['primary_output'];video=Path(result['path'])
    if not video.is_file() or sha(video)!=result['sha256']:raise RuntimeError('FINAL_OUTPUT_IDENTITY_MISMATCH')
    package_root=Path(identity['install_root']);probe=package_root/'tools/ffmpeg/ffprobe.exe'
    tech=technical_probe(probe,video);write(evidence,'07_FINAL_MEDIA.json',{'file':result,'probe':tech,'human_visual':'NOT_EXECUTED','human_hearing':'NOT_EXECUTED'})
    before=call(base,'/api/runtime/control');old_pid=before['server_pid']
    for attempt in range(100):
        try:
            call(base,'/api/runtime/shutdown',{'server_pid':old_pid,'server_instance_id':before['server_instance_id']},{'X-Mindle-Control':before['control_nonce']});break
        except RuntimeError as error:
            if 'HTTP 409' not in str(error) or attempt==99:raise
            time.sleep(.05)
    closed=False
    for _ in range(80):
        try:call(base,'/api/runtime-identity',timeout=1)
        except Exception:closed=True
        if closed and pid_exited(old_pid):break
        time.sleep(.25)
    if not closed or not pid_exited(old_pid):raise RuntimeError('OWNER_SERVER_DID_NOT_STOP')
    base2,identity2=launch(args.exe,args.expected_source,evidence,'08_COLD_RELAUNCH')
    if identity2['server_pid']==old_pid or identity2['server_instance_id']==before['server_instance_id']:raise RuntimeError('COLD_RELAUNCH_IDENTITY_NOT_CHANGED')
    verify_candidate(identity2,args,approval)
    reopened=call(base2,'/api/projects/'+workflow['project_id'])['project']
    if reopened['project_id']!=workflow['project_id'] or not any(x['job_id']==workflow['result']['job_id'] for x in reopened['jobs']):raise RuntimeError('REOPEN_CONTENT_MISMATCH')
    if {x['job_id']:x['primary_output']['sha256'] for x in reopened['jobs']}!={x['job_id']:x['primary_output']['sha256'] for x in before_project['jobs']}:raise RuntimeError('REOPEN_ARTIFACT_IDENTITY_CHANGED')
    exported=call(base2,'/api/projects/'+workflow['project_id']+'/export',{})
    archive=evidence/'09_AFTER_RESTART_EXPORT.zip';archive.write_bytes(call(base2,exported['download_url'],raw=True,timeout=300))
    if sha(archive)!=exported['export']['sha256']:raise RuntimeError('EXPORT_DOWNLOAD_HASH_MISMATCH')
    verify_export(archive,exported['export']['sha256'],workflow['project_id'],reopened['jobs'])
    unchanged()
    return {'status':'TECHNICAL_E2E_PASS_HUMAN_ACCEPTANCE_REQUIRED','source':args.expected_source,'project_id':workflow['project_id'],
            'old_pid':old_pid,'new_pid':identity2['server_pid'],'final_mp4':result,'export_sha256':sha(archive),
            'human_visual':'NOT_EXECUTED','human_hearing':'NOT_EXECUTED','full_product_pass':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('manifest',type=Path);parser.add_argument('--evidence-root',type=Path,required=True)
    parser.add_argument('--expected-source');parser.add_argument('--exe',type=Path);parser.add_argument('--base-url');parser.add_argument('--approval-file',type=Path);parser.add_argument('--task-timeout',type=int,default=900)
    args=parser.parse_args();args.manifest=args.manifest.resolve();evidence=args.evidence_root.resolve();evidence.mkdir(parents=True,exist_ok=False)
    execution_id=str(uuid.uuid4());started_at=now()
    manifest=json.loads(args.manifest.read_text(encoding='utf-8'));intake=validate_intake(manifest,args.manifest.parent)
    intake['manifest_sha256']=sha(args.manifest);write(evidence,'00_INTAKE_RESULT.json',intake)
    if intake['status']!='PASS_INTAKE_TECHNICAL_ONLY':
        write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),'status':'BLOCKED_ASSET_INTAKE','first_blocking_gate':'INPUT_MANIFEST','not_executed':['server mutation','Qwen','FFmpeg assembly','Supertonic','mix','save','restart','reopen','export'],'full_product_pass':False});return 2
    if not args.expected_source or not args.exe:raise ValueError('approved source and EXE are required after intake passes')
    if not args.approval_file:raise ValueError('explicit candidate/model approval file is required')
    try:result=execute(args,manifest,intake,evidence)
    except Exception as error:
        write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),'status':'FAILED','error':str(error),'completed_outputs_preserved':True,'full_product_pass':False});raise
    write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),**result});return 0

if __name__=='__main__':raise SystemExit(main())
