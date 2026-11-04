"""Real source browser Save/cold restart/attachment restore/Export; no model calls."""
import argparse, hashlib, io, json, os, subprocess, sys, tempfile, wave, zipfile
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
from playwright.sync_api import sync_playwright

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expect-loss',action='store_true');args=ap.parse_args()
    root=args.root.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    def digest(data):return hashlib.sha256(data).hexdigest()
    result={'scope':'SOURCE_WORKSPACE_ASSET_PERSISTENCE_ONLY','model_inference':False,'packaged_exe_pass':False,'owner_pc_pass':False,'full_product_pass':False}
    sample="""async()=>{const hash=async f=>{if(!f)return null;const b=await f.arrayBuffer();return {name:f.name,bytes:b.byteLength,sha256:Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b))).map(n=>n.toString(16).padStart(2,'0')).join('')}};return {photo:await Promise.all(photoCommand.references.map(r=>hash(r.file))),video:await Promise.all(videoCommand.references.map(r=>hash(r.file))),audio:await hash(window.mindleInputFor('audio'))}}"""
    with tempfile.TemporaryDirectory() as td:
        work=Path(td)
        for name,color in [('main.png',(80,90,100)),('photo-ref.png',(70,50,20)),('video-ref.png',(20,50,70))]:
            Image.new('RGB',(60,90),color).save(work/name)
        with wave.open(str(work/'input-ko.wav'),'wb') as wav:
            wav.setparams((1,2,16000,0,'NONE','not compressed'));wav.writeframes(bytes(3200))
        env=dict(os.environ,PYTHONPATH=str(root/'src'),HF_HUB_OFFLINE='1',PYTHONUTF8='1')
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
        log=(out/'server.log').open('ab');process=None
        def start():
            proc=subprocess.Popen([sys.executable,'-m','media_ai.product_server','--root',str(root),'--data-dir',str(work/'data'),'--port','0'],cwd=root,env=env,stdout=subprocess.PIPE,stderr=log,text=True)
            base=proc.stdout.readline().strip()
            if not base.startswith('http://127.0.0.1:'):
                proc.terminate();proc.wait(timeout=10);raise RuntimeError('source server did not start')
            return proc,base
        try:
            process,base=start();pid1=process.pid
            with urlopen(base+'/api/runtime-identity',timeout=15) as identity_response:result['runtime_identity']=json.load(identity_response)
            with sync_playwright() as pw:
                browser=pw.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True)
                result['chrome']=browser.version
                page.goto(base,wait_until='networkidle');page.wait_for_function('()=>window.mindleRestoreReady===true')
                page.locator('[data-primary-input=photo]').set_input_files(str(work/'main.png'))
                page.wait_for_function("()=>document.querySelector('[data-preview=photo]').dataset.operation==='import'&&!window.mindleEditPending('photo')")
                page.locator('[data-reference-input=photo]').set_input_files(str(work/'photo-ref.png'))
                page.locator('[data-reference-input=video]').set_input_files(str(work/'video-ref.png'))
                page.locator('[data-primary-input=video]').set_input_files(str(work/'input-ko.wav'))
                before=page.evaluate(sample)
                assert len(before['photo'])==len(before['video'])==1 and before['audio']['bytes']>0
                with page.expect_response(lambda r:'/api/projects/save' in r.url and r.request.method=='POST') as response:
                    page.locator('[data-editor=photo] [data-action=save]').click()
                saved=response.value.json();assert response.value.status==201 and saved['status']=='SAVED'
                result['save_response']=saved;result['before']=before
                page.screenshot(path=str(out/'BEFORE_SAVE_CLOSE.png'),full_page=True)
                browser.close()
                process.terminate();process.wait(timeout=10);process.stdout.close();process=None
                try:urlopen(base+'/api/runtime-identity',timeout=2)
                except OSError:result['old_endpoint_closed']=True
                else:raise AssertionError('old source endpoint still responds')
                process,base2=start();assert process.pid!=pid1
                result['first_pid']=pid1;result['second_pid']=process.pid
                browser=pw.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True)
                try:
                    page.goto(base2,wait_until='networkidle');page.wait_for_function('()=>window.mindleRestoreReady===true')
                    after=page.evaluate(sample);result['after']=after
                    with urlopen(base2+'/api/projects/latest',timeout=10) as r:reopened=json.load(r)['project']
                    assert reopened['project_id']==saved['project_id']
                    result['project_id']=reopened['project_id']
                    page.screenshot(path=str(out/'AFTER_COLD_REOPEN.png'),full_page=True)
                    if args.expect_loss:
                        assert after!=before and after['photo']==[] and after['video']==[] and after['audio'] is None
                        result['status']='CONFIRMED_BASELINE_DEFECT_PENDING_ATTACHMENTS_LOST'
                    else:
                        assert after==before,'pending reference/audio bytes were not restored'
                        for item in reopened['workspace']['references']['photo']+reopened['workspace']['references']['video']+[reopened['workspace']['audio']]:
                            with urlopen(base2+item['url'],timeout=10) as response:content=response.read()
                            assert digest(content)==item['sha256'] and len(content)==item['bytes']
                        with page.expect_download(timeout=30000) as download:
                            page.locator('[data-editor=photo] [data-action=export]').click()
                        export=out/'WORKSPACE_UI_EXPORT.zip';download.value.save_as(str(export))
                        assert page.locator('[data-editor=photo]').get_attribute('data-export-sha256')==digest(export.read_bytes())
                        with zipfile.ZipFile(export) as package:
                            assert package.testzip() is None
                            manifest=json.loads(package.read('BUNDLE_MANIFEST.json'))
                            assert {f['role'] for f in manifest['files']}=={'input','output','workspace_reference','workspace_audio'}
                            assert len(manifest['files'])==6
                            for item in manifest['files']:
                                content=package.read(item['archive_path'])
                                assert digest(content)==item['sha256'] and len(content)==item['bytes']
                        result['export']={'sha256':digest(export.read_bytes()),'bytes':export.stat().st_size,'crc':'PASS','manifest_files':len(manifest['files'])}
                        page.evaluate('()=>window.mindleNewProject()')
                        assert page.evaluate(sample)=={'photo':[],'video':[],'audio':None}
                        result['new_project_clears_attachments']=True
                        result['status']='PASS_SOURCE_PENDING_REFERENCES_AUDIO_SAVE_COLD_REOPEN_UI_EXPORT'
                finally:browser.close()
        except Exception as error:
            result['status']='FAIL';result['error']=repr(error);raise
        finally:
            if process is not None:process.terminate();process.wait(timeout=10);process.stdout.close()
            log.close()
            (out/'WORKSPACE_ASSETS_BROWSER.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
