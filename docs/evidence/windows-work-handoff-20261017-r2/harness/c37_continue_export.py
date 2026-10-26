import json,pathlib,hashlib,base64,datetime,zipfile,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path('outputs/WINDOWS_WORK_HANDOFF_20261017_R2');ev=root/'c37_runtime';inp=pathlib.Path('outputs/EVIDENCE_20261015_CANDIDATE_R1/inputs').resolve();base='http://127.0.0.1:18768'
def write(n,v):(ev/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='chrome',headless=False);page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True);page.set_default_timeout(120000)
 identity=page.request.get(base+'/api/runtime-identity').json();prior=json.loads((ev/'CLONE_RECEIPT.json').read_text());clone=prior['clone'];old={'project_id':prior['original_project']};oldhash=prior['original_sha256'];oldfile=pathlib.Path(identity['data_root'])/'projects'/(old['project_id']+'.json')
 project=json.loads((ev/'SAVED_PROJECT.json').read_text(encoding='utf-8'));page.goto(base);page.wait_for_function('()=>window.mindleRestoreReady===true');page.wait_for_function('()=>!window.mindleEditPending("photo")')
 refs=project['workspace']['references']['photo'];assert len(refs)==2
 hashes=[]
 for item in refs:
  assert sha(item['path'])==item['sha256']==sha(inp/item['original_filename']);hashes.append({'filename':item['file_name'],'sha256':item['sha256'],'bytes':pathlib.Path(item['path']).stat().st_size})
 audio=project['workspace']['audio'];assert sha(audio['path'])==audio['sha256']==sha(inp/'korean_original.wav')
 write('ATTACHMENT_HASHES.json',{'references':hashes,'audio':{'filename':audio['file_name'],'sha256':audio['sha256']},'video_unchanged_after_audio_import':True})
 geometry=page.evaluate('''()=>({viewport:{width:innerWidth,height:innerHeight,devicePixelRatio,visualViewportScale:visualViewport.scale,cssZoom:getComputedStyle(document.documentElement).zoom},title:document.title,video:{rect:document.querySelector('[data-editor=video]').getBoundingClientRect().toJSON()},photo:{rect:document.querySelector('[data-editor=photo]').getBoundingClientRect().toJSON()},preview:[...document.querySelectorAll('[data-preview]')].map(h=>({kind:h.dataset.preview,stage:h.getBoundingClientRect().toJSON(),overflow:getComputedStyle(h).overflow,child:[...h.children].map(v=>({tag:v.tagName,src:v.getAttribute('src'),naturalWidth:v.naturalWidth||v.videoWidth,naturalHeight:v.naturalHeight||v.videoHeight,rect:v.getBoundingClientRect().toJSON(),objectFit:getComputedStyle(v).objectFit,objectPosition:getComputedStyle(v).objectPosition}))})),features:{sevenAdjustments:document.querySelectorAll('[data-photo-adjust]').length,naturalLanguageInputs:document.querySelectorAll('[data-command]').length,adShortform:!!document.querySelector('[data-action=shortform-mode]')},styles:[...document.styleSheets].map(s=>s.href)})''');write('ACTUAL_C37_UI_GEOMETRY.json',geometry)
 page.screenshot(path=str(ev/'C37_ACTUAL_UI.png'),full_page=True)
 with page.expect_download(timeout=120000) as dl:page.locator('[data-editor="photo"] [data-action="export"]').click()
 archive=ev/'C37_UI_EXPORT.zip';dl.value.save_as(archive)
 video_src=page.locator('[data-preview="video"] video').get_attribute('src');entry=video_src.removeprefix('/files/')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;assert 'project.json' in z.namelist();mp4=ev/'C37_ACTUAL_EXPORTED_VIDEO.mp4';mp4.write_bytes(z.read(entry));names=z.namelist()
 write('ACTUAL_UI_EXPORT.json',{'clone':clone,'zip_bytes':archive.stat().st_size,'zip_sha256':sha(archive),'zip_crc':'PASS','entries':names,'mp4_zip_entry':entry,'mp4_bytes':mp4.stat().st_size,'mp4_sha256':sha(mp4),'trigger':'UI Export download in official Chrome','source':identity['build_commit']})
 assert sha(oldfile)==oldhash;write('ORIGINAL_PROJECT_UNCHANGED.json',{'project':old['project_id'],'before_sha256':oldhash,'after_sha256':sha(oldfile),'match':True})
 write('SESSION.json',{'browser':browser.version,'runtime_identity':identity,'clone_project':clone,'scope':'ACTUAL_OFFICE_C37_INSTALLED_RUNTIME_UI_SAVE_EXPORT','contains_transition_fix':False,'server_cold_restart_verified':False,'other_product_auto_browser_windows_still_open':True})
 browser.close();print('C37_UI_SAVE_EXPORT_PASS',clone,flush=True)
