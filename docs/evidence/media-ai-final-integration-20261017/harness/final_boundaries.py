import asyncio,sys,os,json,threading,base64,hashlib,zipfile,subprocess,traceback
from pathlib import Path
from datetime import datetime,timezone
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2]; REPO=Path(__file__).parent/'source'
sys.path.insert(0,str(REPO/'src'));sys.path.append(str(ROOT/'work/site-packages'))
os.environ['MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT']=str(ROOT/'work/candidate_38497304486_20261015/fresh_candidate/MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0/_payload')
from media_ai.product_server import create_server
OUT=ROOT/'outputs'/sys.argv[1];OUT.mkdir(exist_ok=False)
INP=ROOT/'outputs/EVIDENCE_20261015_CANDIDATE_R1/inputs'
server=create_server(REPO,OUT/'data','',0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();BASE=f'http://127.0.0.1:{server.server_port}'
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel='chrome',headless=False);p=await browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True);p.set_default_timeout(15000)
  errors=[];p.on('pageerror',lambda e:errors.append(str(e)));await p.goto(BASE)
  async def idle():await p.wait_for_function('window.mindleRestoreReady && !window.mindleEditPending("photo") && !window.mindleEditPending("video")')
  async def snap():return await p.evaluate('''()=>({files:['photo','video','audio'].map(k=>{const f=window.mindleInputFor(k);return f?{name:f.name,size:f.size}:null}),previews:[...document.querySelectorAll('[data-preview]')].map(h=>({job:h.dataset.jobId,operation:h.dataset.operation,children:h.childElementCount})),tracks:[...document.querySelectorAll('.track')].map(x=>x.textContent),time:document.querySelector('[data-video-time]').textContent,duration:document.querySelector('[data-video-duration]').textContent,ruler:document.querySelector('.timeline-ruler').textContent,seek:document.querySelector('[data-video-seek]').value,inputs:[...document.querySelectorAll('input[type=file]')].map(x=>({key:x.getAttribute('data-primary-input')||x.getAttribute('data-bgm-input')||x.getAttribute('data-reference-input'),files:[...x.files].map(f=>f.name)})),refs:['photo','video'].map(k=>window.mindleReferenceFiles(k).map(f=>f.name)),projectStatus:[...document.querySelectorAll('[data-editor]')].map(x=>x.dataset.projectStatus)})''')
  async def save():
   async with p.expect_response(lambda r:r.url.endswith('/api/projects/save') and r.request.method=='POST') as rr:await p.locator('[data-editor="photo"] [data-action="save"]').click()
   r=await rr.value;v=await r.json();assert r.ok,v;await idle();return v['project_id']
  async def op(pid):ok=await p.evaluate('(id)=>window.mindleOpenProject(id)',pid);await idle();return ok
  async def imp(kind,file):
   async with p.expect_response(lambda r:r.url.endswith('/api/media/import')) as rr:await p.locator(f'[data-primary-input="{kind}"]').set_input_files(str(INP/file))
   assert (await rr.value).ok;await idle()
  async def export():
   async with p.expect_download() as dl:await p.locator('[data-editor="photo"] [data-action="export"]').click()
   path=OUT/f'export_{len(exports)}.zip'
   try:await (await dl.value).save_as(path)
   except Exception as error:
    exports.append({'ui_download':'BLOCKED','error':str(error),'download_url':(await dl.value).url})
    response=await p.request.get((await dl.value).url);assert response.ok;path.write_bytes(await response.body())
   await idle()
   with zipfile.ZipFile(path) as z:assert z.testzip() is None;assert 'project.json' in z.namelist()
   exports.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'crc':'PASS'})
  exports=[];await idle();await imp('photo','portrait_autofit.png');B=await save()
  assert await p.evaluate('window.mindleNewProject()');await imp('photo','portrait_autofit.png')
  await imp('video','video_original.mp4')
  body={'filename':'video_original.mp4','content_base64':base64.b64encode((INP/'video_original.mp4').read_bytes()).decode(),'options':{'effect':True,'subtitle':'Boundary subtitle','duration':2},'command':'Boundary seed real FFmpeg edit'}
  rr=await p.request.post(BASE+'/api/video-edits',data=body);job=await rr.json();assert rr.ok,job;await p.evaluate('(j)=>window.mindleAcceptResult(j)',job)
  await p.locator('[data-primary-input="video"]').set_input_files(str(INP/'korean_original.wav'));await idle()
  await p.locator('[data-editor="photo"] [data-reference-input]').set_input_files(str(INP/'reference_architecture_crop.png'))
  await p.wait_for_timeout(100);A=await save();oldhash=hashlib.sha256((OUT/'data/projects'/f'{A}.json').read_bytes()).hexdigest()
  baseline=await snap();await p.screenshot(path=str(OUT/'BASELINE.png'),full_page=True)
  cases=[]
  await op(B);s=await snap();cases.append({'case':'open_photo_only_clears_video_state','before':baseline,'after':s,'pass':s['files'][1] is None and s['files'][2] is None and 'Boundary subtitle' not in str(s['tracks']) and '영상 효과' not in str(s['tracks']) and s['duration']=='/ 00:00:00' and all(not x['files'] for x in s['inputs'])});write('CASES.json',cases);await p.screenshot(path=str(OUT/'PHOTO_ONLY.png'),full_page=True)
  await op(A);assert await p.evaluate('window.mindleNewProject()');s=await snap();cases.append({'case':'new_clears_all_project_state','after':s,'pass':all(x is None for x in s['files']) and all(not x['files'] for x in s['inputs']) and '영상 효과' not in str(s['tracks']) and not any(s['projectStatus']) and all(not x['job'] for x in s['previews'])});write('CASES.json',cases);await p.screenshot(path=str(OUT/'NEW.png'),full_page=True)
  failures=[]
  for dependency in ['preview','reference','audio']:
   assert await op(A);before=await snap(); project=(await (await p.request.get(BASE+'/api/projects/'+A)).json())['project']
   if dependency=='preview':url=project['jobs'][0]['preview_url']
   elif dependency=='reference':url=project['workspace']['references']['photo'][0]['url']
   else:url=project['workspace']['audio']['url']
   async def fail(route):await route.fulfill(status=503,body='injected acceptance failure')
   await p.route(BASE+url,fail);ok=await op(A);after=await snap();await p.unroute(BASE+url,fail);saved=await save();await export();retry=await op(A)
   failures.append({'dependency':dependency,'open_return':ok,'preserved':before==after,'saved_project_id':saved,'retry':retry,'pass':not ok and before==after and saved==A and retry})
  cases.append({'case':'restore_dependency_failure_preserves_save_export_retry','details':failures,'pass':all(x['pass'] for x in failures)})
  for height in [1024,720]:
   await p.set_viewport_size({'width':1536,'height':height})
   await p.evaluate('''()=>{for(const kind of ['photo','video']){const grid=document.querySelector(`[data-editor="${kind}"] .asset-grid`);for(let i=0;i<60;i++){const n=document.createElement('button');n.textContent='Acceptance dense asset '+i;grid.append(n)}}}''')
   accessible=[]
   for selector in ['[data-editor="photo"] [data-command]','[data-editor="video"] [data-command]','[data-editor="photo"] [data-action="save"]','[data-editor="video"] [data-action="export"]']:
    loc=p.locator(selector);await loc.scroll_into_view_if_needed();accessible.append({'selector':selector,'visible':await loc.is_visible(),'box':await loc.bounding_box()})
   geometry=await p.evaluate('''()=>({viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,zoom:getComputedStyle(document.body).zoom},grids:[...document.querySelectorAll('.asset-grid')].map(x=>({height:x.clientHeight,scrollHeight:x.scrollHeight,overflow:getComputedStyle(x).overflowY})),photo:{stage:document.querySelector('[data-preview="photo"]').getBoundingClientRect().toJSON(),fit:getComputedStyle(document.querySelector('[data-preview="photo"] img')).objectFit,position:getComputedStyle(document.querySelector('[data-preview="photo"] img')).objectPosition}})''')
   cases.append({'case':f'dense_ui_{height}','fixture':'DOM only added asset buttons to stress existing CSS; no production fixture/code','accessible':accessible,'geometry':geometry,'pass':all(x['visible'] for x in accessible) and all(x['height']<400 and x['scrollHeight']>x['height'] for x in geometry['grids'])});await p.screenshot(path=str(OUT/f'DENSE_{height}.png'),full_page=True)
  write('RESULT.json',{'source':subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),'browser':browser.version,'scope':'ISOLATED_SOURCE_REAL_CHROME_NOT_PACKAGED_PC_ACCEPTANCE','cases':cases,'exports':exports,'page_errors':errors,'identity':server.runtime_identity(),'models_executed':0,'preserved_original_project_sha_before':oldhash,'full_product_pass':False,'at':datetime.now(timezone.utc).isoformat()});print(json.dumps([{'case':x['case'],'pass':x['pass']} for x in cases]),flush=True);await browser.close()
try:asyncio.run(main())
except Exception:
 (OUT/'EXCEPTION.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
finally:
 server.shutdown();server.server_close();thread.join(timeout=5);write('HTTP_LOG.json',server.requests)
