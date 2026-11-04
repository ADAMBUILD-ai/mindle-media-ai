import asyncio,json,sys,hashlib,base64,zipfile,traceback,os
from pathlib import Path
from datetime import datetime,timezone,timedelta
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
OUT=Path(os.environ.get('MINDLE_ACCEPTANCE_EVIDENCE','outputs/TRANSITION_BROWSER_20261017_R1')).resolve();INP=Path('outputs/EVIDENCE_20261015_CANDIDATE_R1/inputs').resolve();BASE=os.environ.get('MINDLE_ACCEPTANCE_URL','http://127.0.0.1:18788')
events=[];cases=[];downloads=[];page_errors=[]
def now():return datetime.now(timezone(timedelta(hours=9))).isoformat()
def write(n,v):(OUT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def audit_request(req):
 u=req.url.removeprefix(BASE);r={'url':u,'method':req.method,'time':now()}
 if req.method=='POST':
  try:
   v=req.post_data_json;r['project_id']=v.get('project_id');r['job_ids']=v.get('job_ids');r['filename']=v.get('filename');r['command']=v.get('command');r['options']=v.get('options')
   if v.get('workspace'):
    r['workspace']={'references':{k:[{'filename':f['filename'],'sha256':hashlib.sha256(base64.b64decode(f['content_base64'])).hexdigest()} for f in fs] for k,fs in v['workspace'].get('references',{}).items()},'audio':None}
    a=v['workspace'].get('audio')
    if a:r['workspace']['audio']={'filename':a['filename'],'sha256':hashlib.sha256(base64.b64decode(a['content_base64'])).hexdigest()}
  except Exception as e:r['audit_error']=str(e)
 events.append(r);write('HTTP_REQUESTS.json',events)
def count(url,method=None):return sum(e['url']==url and (method is None or e['method']==method) for e in events)
async def shot(n):await page.screenshot(path=str(OUT/(n+'.png')),full_page=True)
async def idle():await page.wait_for_function('()=>window.mindleRestoreReady===true && !window.mindleEditPending("photo") && !window.mindleEditPending("video")')
async def state():
 return await page.evaluate('''()=>({previews:[...document.querySelectorAll('[data-preview]')].map(h=>({kind:h.dataset.preview,job:h.dataset.jobId||null,src:h.firstElementChild?.getAttribute('src')||null})),files:['photo','video'].map(k=>{const f=window.mindleInputFor(k);return f?{kind:k,name:f.name,size:f.size}:null}),references:[...document.querySelectorAll('[data-reference-list]')].map(v=>v.textContent)})''')
async def menu():await page.locator('[data-shell="projects"]').first.click();await page.locator('dialog').wait_for()
async def close_menu():
 if await page.locator('dialog[open]').count():await page.locator('dialog[open]').get_by_role('button',name='닫기',exact=True).click();await page.wait_for_timeout(75)
async def new():
 await menu();await page.locator('dialog').get_by_role('button',name='새 프로젝트',exact=True).click();await page.wait_for_timeout(100);ok=not await page.locator('dialog[open]').count()
 await close_menu();return ok
async def opened(pid,wait=True):
 await menu();await page.locator('dialog button').filter(has_text=pid).click()
 if wait:
  await page.wait_for_function('()=>window.mindleRestoreReady===true');await page.locator('dialog').wait_for(state='detached')
async def blocked_switch(pid):
 before=await state();n=count('/api/projects/'+pid,'GET');assert not await new(),'New must reject busy transition';assert await state()==before
 await opened(pid,False);await page.wait_for_timeout(150);assert await page.locator('dialog').count()==1,'Rejected Open must retain dialog';await close_menu();assert count('/api/projects/'+pid,'GET')==n,'Open emitted a competing GET';assert await state()==before
 return {'before':before,'after':await state(),'rejected_open_requests':0,'rejected_dialog_retained':True}
async def load(lane,name):
 async with page.expect_file_chooser() as fc:await page.locator(f'[data-editor="{lane}"] [data-action="load"]').click()
 if name.endswith('.wav'):
  await (await fc.value).set_files(str(INP/name));return
 async with page.expect_response(lambda r:'/api/media/import' in r.url and r.request.method=='POST') as resp:await (await fc.value).set_files(str(INP/name))
 r=await resp.value;assert r.ok,await r.text();await idle()
async def save(lane='photo'):
 async with page.expect_response(lambda r:r.url.endswith('/api/projects/save') and r.request.method=='POST') as resp:await page.locator(f'[data-editor="{lane}"] [data-action="save"]').click()
 r=await resp.value;v=await r.json();assert r.ok,v;await idle();return v['project_id']
async def refs(lane):
 async with page.expect_file_chooser() as f:await page.locator(f'[data-action="{lane}-reference"]').click()
 await (await f.value).set_files([str(INP/'portrait_autofit.png'),str(INP/'reference_architecture_crop.png')]);await page.wait_for_timeout(100)
class Gate:
 def __init__(self,path,fail=False):self.path=path;self.started=asyncio.Event();self.release=asyncio.Event();self.done=asyncio.Event();self.fail=fail;self.calls=0;self.responses=[]
 async def handler(self,route):
  self.calls+=1
  try:
   response=await route.fetch();self.responses.append({'url':response.url,'status':response.status,'body':await response.json()});self.started.set();await self.release.wait()
   if self.fail:await route.fulfill(status=503,json={'error':'ACCEPTANCE_INJECTED_RESTORE_FAILURE'})
   else:await route.fulfill(response=response)
  finally:self.done.set()
 async def start(self):await page.route(BASE+self.path,self.handler)
 async def finish(self):self.release.set();await self.done.wait();await page.unroute(BASE+self.path,self.handler);await page.wait_for_timeout(250)
async def check(name,fn):
 row={'case':name,'started_at':now()}
 try:row['evidence']=await fn();row['status']='PASS'
 except Exception as e:row['status']='FAIL';row['error']=repr(e);row['traceback']=traceback.format_exc();await shot(name+'_FAIL');traceback.print_exc()
 row['finished_at']=now();cases.append(row);write('CASES.json',cases);print(name,row['status'],flush=True)
async def main():
 global page,A,B,C
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel='chrome',headless=False);page=await browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True);page.set_default_timeout(30000)
  page.on('request',audit_request);page.on('download',lambda d:downloads.append(d));page.on('pageerror',lambda e:page_errors.append(str(e)))
  await page.goto(BASE);await idle();identity=await (await page.request.get(BASE+'/api/runtime-identity')).json();assert identity['head']=='ef56f956db5cdaf9e9dd455a5a8c065ce4f15a56';assert identity['runtime_mode']=='DEVELOPMENT_UI_WITH_PACKAGE_MODELS'
  write('BROWSER_SESSION.json',{'started_at':now(),'browser':browser.version,'actual_url':page.url,'identity':identity,'scope':'SOURCE_REAL_SERVER_OFFICIAL_CHROME_NOT_C37_PACKAGE','models_executed':False})
  await load('photo','portrait_autofit.png');await load('video','video_original.mp4');await refs('photo');await refs('video');await load('video','korean_original.wav');A=await save();assert await new();await load('photo','portrait_autofit.png');B=await save();await opened(A);await idle();write('SEED_PROJECTS.json',{'A':A,'B':B});await shot('BASELINE')
  async def edit_race(lane):
   await opened(A);await idle();g=Gate('/api/photo-edits' if lane=='photo' else '/api/video-edits');await g.start()
   try:
    if lane=='photo':
     await page.locator('[data-photo-adjust="brightness"]').fill('15');await page.locator('[data-photo-adjust="brightness"]').dispatch_event('input');await page.locator('[data-photo-apply]').click()
    else:await page.locator('[data-video-tool="effect"]').click()
    await asyncio.wait_for(g.started.wait(),60);keep=await blocked_switch(B);await shot('EDIT_'+lane+'_BLOCKED');await g.finish();await idle();saved=await save();assert saved==A
    await opened(B);await idle();await opened(A);await idle();return {'retained':keep,'save_project_id':saved,'actual_backend_responses':g.responses,'switch_after_completion':True}
   finally:g.release.set();await page.unroute(BASE+g.path,g.handler)
  await check('01_PHOTO_EDIT_NEW_OPEN',lambda:edit_race('photo'))
  await check('01_VIDEO_EDIT_NEW_OPEN',lambda:edit_race('video'))
  async def delayed_save():
   await opened(A);await idle();g=Gate('/api/projects/save');await g.start()
   try:
    await page.locator('[data-editor="photo"] [data-action="save"]').click();await asyncio.wait_for(g.started.wait(),30);keep=await blocked_switch(B)
    await page.locator('[data-editor="video"] [data-action="save"]').click();assert g.calls==1;await g.finish();await idle();assert g.responses[0]['body']['project_id']==A
    old=OUT/'data/projects'/f'{A}.json';oldhash=digest(old);assert await new();await load('photo','portrait_autofit.png');start=len(events);fresh=await save();first=next(e for e in events[start:] if e['url']=='/api/projects/save' and e['method']=='POST');assert first['project_id'] is None;assert fresh not in [A,B];assert digest(old)==oldhash
    write('FIRST_SAVE_OLD_PROJECT_PRESERVED.json',{'previous_project':A,'new_project':fresh,'first_save_request':first,'old_file_sha256_before':oldhash,'old_file_sha256_after':digest(old)})
    return {'held':keep,'same_old_save_id':A,'new_id':fresh,'first_save_id':None,'old_file_preserved':True,'response':g.responses}
   finally:g.release.set();await page.unroute(BASE+g.path,g.handler)
  await check('02_SAVE_DELAY_NEW_OPEN_AND_05_FIRST_SAVE',delayed_save)
  async def restore_race():
   g=Gate('/api/projects/'+A,fail=True);await g.start()
   try:
    await opened(A,False);await asyncio.wait_for(g.started.wait(),30);await close_menu();start=count('/api/projects/save','POST');keep=await blocked_switch(B);await page.locator('[data-editor="photo"] [data-action="save"]').click();assert count('/api/projects/save','POST')==start;assert g.calls==1
    await g.finish();await idle();await opened(A);await idle();assert not await page.locator('dialog').count();saved=await save();assert saved==A
    return {'blocked':keep,'restore_calls_while_pending':1,'save_requests_while_pending':0,'failure_injected':503,'normal_retry_saved_project':saved}
   finally:g.release.set();await page.unroute(BASE+g.path,g.handler)
  await check('03_REOPEN_NEW_OPEN_SAVE_FAILURE_RETRY',restore_race)
  async def export_race():
   await opened(A);await idle();path='/api/projects/'+A+'/export';g=Gate(path);await g.start();initial=count(path,'POST');initialsave=count('/api/projects/save','POST')
   try:
    await page.locator('[data-editor="photo"] [data-action="export"]').click();await asyncio.wait_for(g.started.wait(),30);keep=await blocked_switch(B)
    await page.locator('[data-editor="video"] [data-action="export"]').click();await page.wait_for_timeout(200);assert g.calls==1;assert count('/api/projects/save','POST')==initialsave+1;assert not await new(),'Duplicate Export released guard';await g.finish();await idle();assert count(path,'POST')==initial+1;assert await new();await opened(A);await idle()
    return {'retained':keep,'actual_export_calls':1,'duplicate_export_guard_retained':True,'normal_transition_after':True,'response':g.responses}
   finally:g.release.set();await page.unroute(BASE+g.path,g.handler)
  await check('04_EXPORT_NEW_OPEN_DUPLICATE_GUARD',export_race)
  async def normal():
   await opened(A);await idle();await page.locator('[data-command="photo"]').fill('따뜻하게 보정해줘')
   async with page.expect_response(lambda r:r.url.endswith('/api/photo-edits') and r.request.method=='POST') as response:await page.locator('[data-editor="photo"] .send-button').click()
   result=await response.value;assert result.ok;normal_edit=await result.json();await idle();await page.locator('[data-video-tool="trim"]').click();assert await page.locator('[data-video-controls]').is_visible()
   await page.locator('[data-shell="cloud"]').click();cloud=await page.locator('dialog').inner_text();assert '연결되어 있지 않습니다' in cloud;await close_menu();await page.locator('[data-shell="storage"]').first.click();local=await page.locator('dialog').inner_text();assert str(OUT/'data') in local;await close_menu()
   await save();response=await page.request.get(BASE+'/api/projects/'+A);project=(await response.json())['project'];write('FINAL_SAVED_PROJECT.json',project)
   await page.reload();await idle();restored=await state();assert len(await page.locator('[data-preview] img').all())==1;assert await page.locator('[data-preview] video').count()==1
   workspace=project['workspace'];verified=[]
   for lane,files in workspace['references'].items():
    for item in files:assert digest(item['path'])==item['sha256'];verified.append({'lane':lane,'file':item['file_name'],'sha256':item['sha256']})
   audio=workspace['audio'];assert digest(audio['path'])==audio['sha256']==digest(INP/'korean_original.wav')
   async with page.expect_download(timeout=30000) as dl:await page.locator('[data-editor="photo"] [data-action="export"]').click()
   down=await dl.value;p=OUT/'NORMAL_EXPORT.zip';await down.save_as(p)
   with zipfile.ZipFile(p) as z:assert z.testzip() is None;names=z.namelist();assert 'project.json' in names;assert len([n for n in names if n.startswith('workspace/references/')])==4;assert len([n for n in names if n.startswith('workspace/audio/')])==1
   await shot('FINAL_NORMAL_REOPEN_EXPORT');return {'project_id':A,'restored':restored,'reference_hashes':verified,'audio_sha256':audio['sha256'],'cloud':cloud,'storage':local,'zip_sha256':digest(p),'zip_bytes':p.stat().st_size,'zip_crc':'PASS','names':names,'natural_language_real_photo_edit':normal_edit}
  await check('06_NORMAL_IMPORT_ATTACH_SAVE_REOPEN_EXPORT_CLOUD_NL',normal)
  await shot('END');write('PAGE_ERRORS.json',page_errors);write('SUMMARY.json',{'source_sha':identity['head'],'browser':browser.version,'cases':len(cases),'pass':sum(c['status']=='PASS' for c in cases),'fail':sum(c['status']=='FAIL' for c in cases),'runtime_scope':'REAL_SOURCE_SERVER_AND_OFFICIAL_CHROME','candidate_contains_fix':False,'package_build_allowed':False,'models_rerun':False,'owner_pc_c37_pass':False,'full_product_pass':False,'finished_at':now()});await browser.close()
asyncio.run(main())


