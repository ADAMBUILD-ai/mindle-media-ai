"""Verify the existing immutable Windows EXE candidate; never builds or calls models."""
import argparse, hashlib, io, json, os, shutil, socket, subprocess, sys, tempfile, time, wave, zipfile
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
from playwright.sync_api import sync_playwright

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    root=args.root.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    def digest(data):return hashlib.sha256(data).hexdigest()
    result={'scope':'EXACT_DELIVERED_CANDIDATE_ON_GITHUB_WINDOWS_RUNNER_ONLY','model_inference':False,'packaged_exe_pass':False,'owner_pc_pass':False,'full_product_pass':False}
    sample="""async()=>{const hash=async f=>{if(!f)return null;const b=await f.arrayBuffer();return {name:f.name,bytes:b.byteLength,sha256:Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b))).map(n=>n.toString(16).padStart(2,'0')).join('')}};return {photo:await Promise.all(photoCommand.references.map(r=>hash(r.file))),video:await Promise.all(videoCommand.references.map(r=>hash(r.file))),audio:await hash(window.mindleInputFor('audio'))}}"""
    with tempfile.TemporaryDirectory() as td:
        work=Path(td)
        for name,color in [('main.png',(80,90,100)),('photo-ref.png',(70,50,20)),('video-ref.png',(20,50,70))]:
            Image.new('RGB',(60,90),color).save(work/name)
        with wave.open(str(work/'input-ko.wav'),'wb') as wav:
            wav.setparams((1,2,16000,0,'NONE','not compressed'));wav.writeframes(bytes(3200))
        profile=Path(os.environ['RUNNER_TEMP'])/('mindle_followup_'+os.environ['GITHUB_RUN_ID'])
        profile.mkdir(exist_ok=False)
        env=dict(os.environ,LOCALAPPDATA=str(profile),HF_HUB_OFFLINE='1',MINDLE_DIAGNOSTIC_MODE='1')
        env.pop('PYTHONPATH',None)
        result['host']={'hostname':socket.gethostname(),'user':os.environ.get('USERNAME'),'github_actions':os.environ.get('GITHUB_ACTIONS'),'profile':str(profile)}
        runtime_id='c37c7819b145-cfb26b181119'
        def processes():
            command="[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new(); Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*employee_package_launcher.py*--server*' -and $_.CommandLine -like '*"+runtime_id+"*' -and $_.CommandLine -like '*"+profile.name+"*' } | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
            raw=subprocess.check_output(['powershell.exe','-NoProfile','-NonInteractive','-Command',command],encoding='utf-8').strip()
            items=json.loads(raw) if raw else []
            return [items] if isinstance(items,dict) else items
        def stop(proc):
            current=processes()
            assert len(current)==1 and current[0]['ProcessId']==proc['ProcessId'],'refusing to stop an unidentified process'
            subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',"Stop-Process -Id "+str(proc['ProcessId'])],check=True,capture_output=True)
            until=time.monotonic()+20
            while processes() and time.monotonic()<until:time.sleep(.25)
            assert not processes(),'server PID still present'
        
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
        log=(out/'server.log').open('ab');process=None
        def start():
            completed=subprocess.run([str(root/'MINDLE_MEDIA_AI_RUN.exe'),'--no-browser'],env=env,capture_output=True,timeout=300)
            log.write(completed.stdout+completed.stderr);log.flush()
            assert completed.returncode==0,'actual EXE launch failed'
            for port in range(18768,18778):
                try:
                    base='http://127.0.0.1:'+str(port)
                    with urlopen(base+'/api/runtime-identity',timeout=2) as response:identity=json.load(response)
                    if identity.get('package_manifest_sha256')=='7a31da30969b9e7901da8f109c467f281e2550171c15e9ddf3a8ddf215ab3377' and identity.get('build_commit')=='c37c7819b1454996f3510f92184b1ef62faf3c78':
                        found=processes();result['identified_processes']=found;assert len(found)==1,repr(found)
                        return found[0],base
                except OSError:pass
            raise RuntimeError('exact packaged runtime not found')
        try:
            process,base=start();pid1=process['ProcessId']
            with urlopen(base+'/api/runtime-identity',timeout=15) as identity_response:result['runtime_identity']=json.load(identity_response)
            result['first_process']=process
            with sync_playwright() as pw:
                browser=pw.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True)
                result['chrome']=browser.version
                page.goto(base,wait_until='networkidle');page.wait_for_function('()=>window.mindleRestoreReady===true')
                approved=Path(result['runtime_identity']['install_root'])/'app/ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png'
                assert digest(approved.read_bytes())=='f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541'
                shutil.copy2(approved,out/'APPROVED_ORIGINAL_F27E.png')
                result['visual_viewport']=page.evaluate('()=>({width:innerWidth,height:innerHeight,devicePixelRatio,zoom:visualViewport.scale})')
                result['approved_image']={'sha256':digest(approved.read_bytes()),'size':list(Image.open(approved).size)}
                page.screenshot(path=str(out/'CURRENT_UI_1536x1024.png'),full_page=False)
                page.screenshot(path=str(out/'CURRENT_UI_FULL_PAGE.png'),full_page=True)
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
                stop(process);process=None
                try:urlopen(base+'/api/runtime-identity',timeout=2)
                except OSError:result['old_endpoint_closed']=True
                else:raise AssertionError('old packaged endpoint still responds')
                process,base2=start();assert process['ProcessId']!=pid1
                result['first_pid']=pid1;result['second_pid']=process['ProcessId'];result['second_process']=process
                browser=pw.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True)
                try:
                    page.goto(base2,wait_until='networkidle');page.wait_for_function('()=>window.mindleRestoreReady===true')
                    after=page.evaluate(sample);result['after']=after
                    with urlopen(base2+'/api/projects/latest',timeout=10) as r:reopened=json.load(r)['project']
                    assert reopened['project_id']==saved['project_id']
                    result['project_id']=reopened['project_id']
                    page.screenshot(path=str(out/'AFTER_COLD_REOPEN.png'),full_page=True)
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
                    result['status']='PASS_EXACT_PACKAGED_EXE_PENDING_ATTACHMENTS_COLD_REOPEN_UI_EXPORT'
                    result['packaged_exe_pass']=True
                finally:browser.close()
        except Exception as error:
            result['status']='FAIL';result['error']=repr(error);raise
        finally:
            active_error=sys.exc_info()[1]
            try:
                if process is not None:stop(process)
            except Exception as cleanup_error:
                result['cleanup_error']=repr(cleanup_error)
                if result.get('status','').startswith('PASS'):result['status']='FAIL_CLEANUP'
            server_log=profile/'MINDLE/MEDIA_AI_DATA/logs/server.log'
            if server_log.exists():shutil.copy2(server_log,out/'PACKAGED_SERVER.log')
            log.close()
            (out/'WORKSPACE_ASSETS_BROWSER.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(result,ensure_ascii=False))
            if result.get('cleanup_error') and active_error is None:raise RuntimeError(result['cleanup_error'])

if __name__=='__main__':main()
