"""Real remote Windows/Chrome/engine acceptance; never certifies office PC/hearing."""
from __future__ import annotations
import base64,csv,hashlib,json,os,subprocess,time,urllib.error,urllib.request,uuid,zipfile
from pathlib import Path

E=Path('evidence-r3');E.mkdir(exist_ok=True)
ROOT=Path('build/MINDLE_MEDIA_AI_PC_TEST_20261024_R3').resolve();EXE=ROOT/'MINDLE_MEDIA_AI_RUN.exe'
M=json.loads((ROOT/'_payload/PACKAGE_MANIFEST.json').read_text());RUNTIME=Path(os.environ['LOCALAPPDATA'])/'MINDLE_MEDIA_AI/runtime'/M['runtime_id']

def write(name,value):(E/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def request(base,path,body=None,headers=None):
    req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body,ensure_ascii=False).encode(),headers={'Content-Type':'application/json',**(headers or {})})
    try:
        with urllib.request.urlopen(req,timeout=180) as r:return json.load(r)
    except urllib.error.HTTPError as error:
        payload=error.read().decode('utf-8','replace')
        write('LAST_HTTP_ERROR.json',{'path':path,'code':error.code,'body':payload})
        raise RuntimeError(f'HTTP {error.code} {path}: {payload}') from error
def launch(label):
    with (E/(label+'.log')).open('wb') as log:subprocess.run([str(EXE),'--no-browser'],stdout=log,stderr=subprocess.STDOUT,timeout=1200,check=True)
    for port in range(18768,18778):
        base='http://127.0.0.1:'+str(port)
        try:
            value=request(base,'/api/runtime-identity')
            if value.get('install_root')==str(RUNTIME) and value.get('package_manifest_sha256')==hashlib.sha256((ROOT/'_payload/PACKAGE_MANIFEST.json').read_bytes()).hexdigest():return base,value
        except Exception:pass
    raise RuntimeError('exact candidate endpoint missing')
def pid_alive(pid):
    result=subprocess.check_output(['tasklist','/FI','PID eq '+str(pid),'/FO','CSV','/NH'],text=True)
    return any(len(row)>1 and row[1]==str(pid) for row in csv.reader(result.splitlines()))
def verify_runtime():
    for item in M['files']:
        p=RUNTIME/item['path'];h=hashlib.sha256()
        with p.open('rb') as f:
            while b:=f.read(1024*1024):h.update(b)
        if p.stat().st_size!=item['bytes'] or h.hexdigest()!=item['sha256']:raise RuntimeError('installed runtime changed: '+item['path'])
    if list(RUNTIME.rglob('*.pyc')):raise RuntimeError('runtime bytecode unexpectedly created')

try:
    base,first=launch('FIRST_EXE');same,_=launch('SECOND_EXE');assert base==same
    before=request(base,'/api/runtime/control');assert pid_alive(before['server_pid'])
    ffmpeg=ROOT/'_payload/tools/ffmpeg/ffmpeg.exe';fixture=E/'input.mp4'
    subprocess.run([str(ffmpeg),'-v','error','-f','lavfi','-i','color=c=blue:s=320x180:r=10','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','4','-c:v','h264_mf','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart','-y',str(fixture)],check=True,timeout=60)
    from playwright.sync_api import sync_playwright
    command='밝기를 3 높이고 "반갑습니다" 나레이션을 넣고 영상을 연장해 주세요.'
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome',headless=True)
        page=browser.new_page(viewport={'width':1536,'height':1024},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(base,wait_until='networkidle')
        page.locator('[data-editor="video"] [data-primary-input]').set_input_files(str(fixture.resolve()))
        page.wait_for_function("document.querySelector('[data-editor=video] [data-preview]').dataset.jobId",timeout=120000)
        page.locator('[data-command="video"]').fill(command)
        with page.expect_response(lambda r:r.url.endswith('/api/workflows/plan'),timeout=180000) as response:
            page.locator('[data-editor="video"] .send-button').click()
        plan=response.value.json();write('ACTUAL_GENERATIVE_PLAN.json',plan)
        assert response.value.ok,plan
        assert plan['plan_source']=='LOCAL_GENERATIVE_INFERENCE'
        assert any(s['operation']=='video_edit' and s['options']['brightness']==3 for s in plan['steps']),plan
        assert any(s['operation']=='narrate' and s['text']=='반갑습니다' for s in plan['steps']),plan
        end=time.monotonic()+300;task=None
        while time.monotonic()<end:
            workflows=request(base,'/api/workflows')['workflows']
            task=next((x for x in workflows if x.get('request',{}).get('plan_id')==plan['plan_id']),None) if workflows else None
            # Product stores the verified plan in its immutable request; fresh isolated data has exactly one workflow.
            if task is None and len(workflows)==1:task=workflows[0]
            if task and task['state'] in {'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'}:break
            time.sleep(.5)
        write('ACTUAL_WORKFLOW.json',task)
        assert task and task['state']=='SUCCEEDED',task
        page.wait_for_function("document.querySelector('[data-editor=video] [data-command-error]').textContent.includes('순차 작업·저장 완료')",timeout=30000)
        page.screenshot(path=str(E/'CHROME_COMPLETED.png'),full_page=True)
        media=page.locator('[data-editor="video"] video')
        media.evaluate('(v)=>{v.muted=true;return v.play()}');page.wait_for_timeout(900)
        observation=media.evaluate('(v)=>({error:v.error?.code||0,readyState:v.readyState,videoWidth:v.videoWidth,videoHeight:v.videoHeight,currentSrc:v.currentSrc,currentTime:v.currentTime,duration:v.duration})')
        write('BROWSER_MEDIA.json',{'media':observation,'page_errors':errors,'human_hearing':False})
        assert observation['error']==0 and observation['videoWidth']>0 and observation['currentTime']>0
        assert not errors,errors
        browser.close()
    project=request(base,'/api/projects/latest')['project'];assert project['project_id']==task['project_id']
    voices=[j for j in project['jobs'] if j.get('operation')=='narration'];assert voices
    voice=voices[-1];assert voice['runtime_result']['model_inference'] is True and 'Supertonic' in voice['runtime_result']['engine']
    write('ACTUAL_NEURAL_VOICE.json',voice)
    # Run the new architecture-agent path with the same pinned Qwen runtime.
    red=E/'architecture-red.mp4'
    subprocess.run([str(ffmpeg),'-v','error','-f','lavfi','-i','color=c=red:s=320x180:r=10',
                    '-f','lavfi','-i','sine=frequency=660:sample_rate=48000','-t','4','-c:v','h264_mf',
                    '-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart','-y',str(red)],check=True,timeout=60)
    imported=[]
    for source in (fixture,red):
        imported.append(request(base,'/api/media/import',{'kind':'video','filename':source.name,
                        'content_base64':base64.b64encode(source.read_bytes()).decode()}))
    architecture_project=str(uuid.uuid4())
    architecture_plan=request(base,'/api/architecture-agent/plan',{
        'command':'두 영상으로 2초 16:9 건축 홍보 영상을 구성해 주세요.',
        'project_id':architecture_project,'job_ids':[item['job_id'] for item in imported]})
    assert architecture_plan['plan_source']=='LOCAL_GENERATIVE_INFERENCE'
    assert architecture_plan['model_id']=='Qwen/Qwen2.5-1.5B-Instruct-GGUF'
    assert len(architecture_plan['scenes'])==2
    assert all(scene['selection']['model_inference'] is False for scene in architecture_plan['scenes'])
    assert all(scene['start_seconds']>=0 for scene in architecture_plan['scenes'])
    production=request(base,'/api/architecture-agent/productions',{
        'request_id':str(uuid.uuid4()),'plan_id':architecture_plan['plan_id']})
    end=time.monotonic()+300
    while time.monotonic()<end and production['state'] not in {'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED','BLOCKED_INPUT','BLOCKED_ASSET'}:
        time.sleep(.5);production=request(base,'/api/architecture-agent/productions/'+production['production_id'])
    assert production['state']=='SUCCEEDED',production
    assert production['receipt']['planner_model_inference'] is True
    assert len(production['receipt']['scene_ranges'])==2
    write('ACTUAL_ARCHITECTURE_AGENT.json',{'plan':architecture_plan,'production':production})
    verify_runtime()
    control=request(base,'/api/runtime/control');assert control['server_pid']==before['server_pid']
    request(base,'/api/runtime/shutdown',{'server_pid':control['server_pid'],'server_instance_id':control['server_instance_id']},{'X-Mindle-Control':control['control_nonce']})
    end=time.monotonic()+20;closed=False
    while time.monotonic()<end:
        try:request(base,'/api/runtime-identity')
        except Exception:closed=True
        if closed and not pid_alive(control['server_pid']):break
        time.sleep(.25)
    assert closed and not pid_alive(control['server_pid'])
    after_base,after=launch('COLD_RELAUNCH_EXE');after_control=request(after_base,'/api/runtime/control')
    assert after_control['server_pid']!=control['server_pid'] and after_control['server_instance_id']!=control['server_instance_id']
    reopened=request(after_base,'/api/projects/'+project['project_id'])['project']
    assert reopened['project_id']==project['project_id']
    assert any(x['job_id']==voice['job_id'] for x in reopened['jobs'])
    assert request(after_base,'/api/workflows/'+task['workflow_id'])['state']=='SUCCEEDED'
    architecture_reopened=request(after_base,'/api/projects/'+architecture_project)['project']
    assert architecture_reopened['project_id']==architecture_project
    assert request(after_base,'/api/architecture-agent/productions/'+production['production_id'])['state']=='SUCCEEDED'
    architecture_export=request(after_base,'/api/projects/'+architecture_project+'/export',{})
    with urllib.request.urlopen(after_base+architecture_export['download_url'],timeout=120) as response:(E/'ARCHITECTURE_AFTER_RESTART_EXPORT.zip').write_bytes(response.read())
    with zipfile.ZipFile(E/'ARCHITECTURE_AFTER_RESTART_EXPORT.zip') as archive:assert archive.testzip() is None
    exported=request(after_base,'/api/projects/'+project['project_id']+'/export',{})
    with urllib.request.urlopen(after_base+exported['download_url'],timeout=120) as response:(E/'AFTER_RESTART_EXPORT.zip').write_bytes(response.read())
    digest=hashlib.sha256((E/'AFTER_RESTART_EXPORT.zip').read_bytes()).hexdigest();assert digest==exported['export']['sha256']
    with zipfile.ZipFile(E/'AFTER_RESTART_EXPORT.zip') as archive:assert archive.testzip() is None
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome',headless=True)
        page=browser.new_page(viewport={'width':1536,'height':1024},device_scale_factor=1,accept_downloads=True)
        page.goto(after_base,wait_until='networkidle')
        page.wait_for_selector('[data-editor="video"] [data-preview] video',timeout=120000)
        page.locator('[data-editor="video"] [data-preview] video').evaluate('(v)=>{v.muted=true;return v.play()}')
        page.wait_for_timeout(900)
        reopened_media=page.locator('[data-editor="video"] [data-preview] video').evaluate('(v)=>({error:v.error?.code||0,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})')
        assert reopened_media['error']==0 and reopened_media['currentTime']>0
        with page.expect_download(timeout=120000) as download:
            page.locator('[data-editor="video"] [data-action="export"]').click()
        ui_zip=E/'UI_AFTER_RESTART_EXPORT.zip';download.value.save_as(str(ui_zip.resolve()))
        with zipfile.ZipFile(ui_zip) as archive:assert archive.testzip() is None
        page.screenshot(path=str(E/'CHROME_REOPEN_EXPORT.png'),full_page=True)
        write('BROWSER_REOPEN.json',{'media':reopened_media,'ui_export_sha256':hashlib.sha256(ui_zip.read_bytes()).hexdigest(),'human_hearing':False})
        browser.close()
    verify_runtime()
    write('ACCEPTANCE.json',{'status':'REMOTE_WINDOWS_EXE_QWEN_SUPERTONIC_MEASURED_ARCHITECTURE_RESTART_EXPORT_PASS','source':os.environ['GITHUB_SHA'],'old_pid':control['server_pid'],'new_pid':after_control['server_pid'],'old_endpoint_closed':closed,'project_id':project['project_id'],'workflow_id':task['workflow_id'],'architecture_project_id':architecture_project,'architecture_production_id':production['production_id'],'export_sha256':digest,'manifest_files_checked_after_actual_engine_use':len(M['files']),'cache_files_created':0,'office_pc_acceptance':False,'human_hearing':False,'approved_ui_pixel_match':False,'full_product_pass':False})
finally:
    data=Path(os.environ['LOCALAPPDATA'])/'MINDLE'/M['data_directory_name']
    if (data/'logs/server.log').is_file():(E/'server.log').write_bytes((data/'logs/server.log').read_bytes())
