"""Owner/PC execution runner for one verified 30-second architecture delivery.

It uses only product HTTP APIs. Missing intake stops before any server mutation.
It never builds a package, installs/replaces a model, or invents an asset value.
"""
from __future__ import annotations
import argparse,base64,hashlib,json,subprocess,time,urllib.error,urllib.request,uuid,zipfile
from datetime import datetime,timezone
from pathlib import Path
from media_ai.e2e_intake import validate_intake

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
    if value.get('state') not in TERMINAL:raise TimeoutError('PRODUCT_TASK_TIMEOUT: '+path+'/'+identifier)
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
    return {'duration_seconds':duration,'width':v.get('width'),'height':v.get('height'),'video_codec':v.get('codec_name'),'pixel_format':v.get('pix_fmt'),'audio_codec':a.get('codec_name')}

def execute(args,manifest,intake,evidence):
    base,identity=(args.base_url,call(args.base_url,'/api/runtime-identity')) if args.base_url else launch(args.exe,args.expected_source,evidence,'01_LAUNCH')
    if identity.get('build_commit')!=args.expected_source:raise RuntimeError('SOURCE_IDENTITY_MISMATCH')
    write(evidence,'02_RUNTIME_IDENTITY.json',identity)
    jobs=[]
    for item in manifest['clips']:
        path=(args.manifest.parent/item['path']).resolve()
        job=call(base,'/api/media/import',{'request_id':str(uuid.uuid4()),'kind':'video','filename':path.name,'content_base64':base64.b64encode(path.read_bytes()).decode()})
        if job['input']['sha256']!=item['sha256']:raise RuntimeError('IMPORTED_INPUT_SHA_MISMATCH')
        jobs.append(job)
    project_id=str(uuid.uuid4())
    architecture_command='선택한 실제 영상 자료 모두로 30초 16:9 건축·리조트 홍보 영상을 구성해 주세요.'
    plan=call(base,'/api/architecture-agent/plan',{'command':architecture_command,'project_id':project_id,'job_ids':[x['job_id'] for x in jobs]})
    if plan.get('plan_source')!='LOCAL_GENERATIVE_INFERENCE' or plan.get('total_duration_seconds')!=30 or plan.get('aspect')!='16:9':raise RuntimeError('ARCHITECTURE_PLAN_CONTRACT_MISMATCH')
    if {x['sha256'] for x in plan.get('catalog',[])}!={x['sha256'] for x in manifest['clips']}:raise RuntimeError('PLAN_INPUT_BINDING_MISMATCH')
    write(evidence,'03_ARCHITECTURE_PLAN.json',plan)
    production=call(base,'/api/architecture-agent/productions',{'request_id':str(uuid.uuid4()),'plan_id':plan['plan_id']})
    production=wait(base,'/api/architecture-agent/productions',production['production_id'],args.task_timeout)
    write(evidence,'04_ARCHITECTURE_PRODUCTION.json',production)
    if production['state']!='SUCCEEDED':raise RuntimeError('ARCHITECTURE_PRODUCTION_'+production['state'])
    values=manifest['volumes'];policy=manifest['voice_length_policy'];script=manifest['narration_script']
    extension=' 영상을 음성에 맞춰 연장해 주세요.' if policy=='extend_video' else ' 음성이 영상보다 길면 거부해 주세요.'
    finish_command=(f'"{script}" 나레이션과 배경음악을 넣어 주세요. '
        f'나레이션 음량 {values["narration"]*100:g}%, 원본 소리 음량 {values["original"]*100:g}%, '
        f'BGM 음량 {values["bgm"]*100:g}%.'+extension)
    finish_plan=call(base,'/api/workflows/plan',{'command':finish_command})
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
    result=workflow['result']['primary_output'];video=Path(result['path'])
    if not video.is_file() or sha(video)!=result['sha256']:raise RuntimeError('FINAL_OUTPUT_IDENTITY_MISMATCH')
    package_root=Path(identity['install_root']);probe=package_root/'tools/ffmpeg/ffprobe.exe'
    tech=technical_probe(probe,video);write(evidence,'07_FINAL_MEDIA.json',{'file':result,'probe':tech,'human_visual':'NOT_EXECUTED','human_hearing':'NOT_EXECUTED'})
    before=call(base,'/api/runtime/control');old_pid=before['server_pid']
    call(base,'/api/runtime/shutdown',{'server_pid':old_pid,'server_instance_id':before['server_instance_id']},{'X-Mindle-Control':before['control_nonce']})
    closed=False
    for _ in range(80):
        try:call(base,'/api/runtime-identity',timeout=1)
        except Exception:closed=True;break
        time.sleep(.25)
    if not closed:raise RuntimeError('OWNER_SERVER_DID_NOT_STOP')
    base2,identity2=launch(args.exe,args.expected_source,evidence,'08_COLD_RELAUNCH')
    if identity2['server_pid']==old_pid or identity2['server_instance_id']==before['server_instance_id']:raise RuntimeError('COLD_RELAUNCH_IDENTITY_NOT_CHANGED')
    reopened=call(base2,'/api/projects/'+workflow['project_id'])['project']
    if reopened['project_id']!=workflow['project_id'] or not any(x['job_id']==workflow['result']['job_id'] for x in reopened['jobs']):raise RuntimeError('REOPEN_CONTENT_MISMATCH')
    exported=call(base2,'/api/projects/'+workflow['project_id']+'/export',{})
    archive=evidence/'09_AFTER_RESTART_EXPORT.zip';archive.write_bytes(call(base2,exported['download_url'],raw=True,timeout=300))
    if sha(archive)!=exported['export']['sha256']:raise RuntimeError('EXPORT_DOWNLOAD_HASH_MISMATCH')
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None or 'project.json' not in package.namelist():raise RuntimeError('EXPORT_ZIP_INVALID')
    return {'status':'TECHNICAL_E2E_PASS_HUMAN_ACCEPTANCE_REQUIRED','source':args.expected_source,'project_id':workflow['project_id'],
            'old_pid':old_pid,'new_pid':identity2['server_pid'],'final_mp4':result,'export_sha256':sha(archive),
            'human_visual':'NOT_EXECUTED','human_hearing':'NOT_EXECUTED','full_product_pass':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('manifest',type=Path);parser.add_argument('--evidence-root',type=Path,required=True)
    parser.add_argument('--expected-source');parser.add_argument('--exe',type=Path);parser.add_argument('--base-url');parser.add_argument('--task-timeout',type=int,default=900)
    args=parser.parse_args();args.manifest=args.manifest.resolve();evidence=args.evidence_root.resolve();evidence.mkdir(parents=True,exist_ok=True)
    execution_id=str(uuid.uuid4());started_at=now()
    manifest=json.loads(args.manifest.read_text(encoding='utf-8'));intake=validate_intake(manifest,args.manifest.parent)
    intake['manifest_sha256']=sha(args.manifest);write(evidence,'00_INTAKE_RESULT.json',intake)
    if intake['status']!='PASS_INTAKE_TECHNICAL_ONLY':
        write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),'status':'BLOCKED_ASSET_INTAKE','first_blocking_gate':'INPUT_MANIFEST','not_executed':['server mutation','Qwen','FFmpeg assembly','Supertonic','mix','save','restart','reopen','export'],'full_product_pass':False});return 2
    if not args.expected_source or not args.exe:raise ValueError('approved source and EXE are required after intake passes')
    try:result=execute(args,manifest,intake,evidence)
    except Exception as error:
        write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),'status':'FAILED','error':str(error),'completed_outputs_preserved':True,'full_product_pass':False});raise
    write(evidence,'RESULT.json',{'execution_id':execution_id,'started_at':started_at,'ended_at':now(),**result});return 0

if __name__=='__main__':raise SystemExit(main())
