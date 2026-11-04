"""Real source HTTP process restart/export probe. No models or EXE claims."""
import argparse
import base64
import hashlib
import io
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import Request,urlopen
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser',action='store_true',help='Use installed official Chrome for restored source UI and actual Export click')
    args=parser.parse_args()
    out=ROOT/'outputs/r9-source-regression';out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        work=Path(td);data=work/'data';log=(work/'server.log').open('ab')
        env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),HF_HUB_OFFLINE='1')
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
        def start():
            p=subprocess.Popen([sys.executable,'-m','media_ai.product_server','--root',str(ROOT),'--data-dir',str(data),'--port','0'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=log,text=True)
            url=p.stdout.readline().strip()
            if not url.startswith('http://127.0.0.1:'):
                p.terminate();p.wait(timeout=5);raise RuntimeError('source server failed to start')
            return p,url
        def call(url,path,payload=None,raw=False):
            req=Request(url+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urlopen(req,timeout=30) as r:content=r.read()
            return content if raw else json.loads(content)
        p=None
        try:
            p,base=start();pid1=p.pid
            buf=io.BytesIO();Image.new('RGB',(90,160),(190,80,30)).save(buf,'PNG')
            photo=call(base,'/api/photo-edits',{'content_base64':base64.b64encode(buf.getvalue()).decode(),'command':'source restart fixture','options':{'temperature':20}})
            video=work/'source.mp4'
            subprocess.run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=160x90:rate=10:duration=1','-f','lavfi','-i','sine=frequency=440:duration=1','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(video)],check=True,capture_output=True)
            edited=call(base,'/api/video-edits',{'filename':'source.mp4','content_base64':base64.b64encode(video.read_bytes()).decode(),'options':{'brightness':18}})
            saved=call(base,'/api/projects/save',{'job_ids':[photo['job_id'],edited['job_id']]})
            p.terminate();p.wait(timeout=5);p.stdout.close();p=None
            try:call(base,'/api/runtime-identity')
            except OSError:old_endpoint_closed=True
            else:raise AssertionError('old process endpoint still responds')
            p,base2=start();pid2=p.pid
            assert pid1!=pid2
            path_diagnostics={'data_root_supplied':str(data),'data_root_resolved':str(data.resolve())}
            (out/'SOURCE_DATA_ROOT.json').write_text(json.dumps(path_diagnostics,indent=2)+'\n')
            reopened=call(base2,'/api/projects/latest')['project']
            assert reopened['project_id']==saved['project_id']
            expected={j['job_id']:j['primary_output']['sha256'] for j in (photo,edited)}
            for job in reopened['jobs']:
                content=call(base2,job['preview_url'],raw=True)
                assert hashlib.sha256(content).hexdigest()==expected[job['job_id']]
            browser_result=None
            if args.browser:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as pw:
                    browser=pw.chromium.launch(channel='chrome',headless=True)
                    page=browser.new_page(viewport={'width':1536,'height':1024},accept_downloads=True)
                    try:
                        page.goto(base2,wait_until='networkidle',timeout=30000)
                        page.wait_for_function('() => window.mindleRestoreReady===true',timeout=30000)
                        page.wait_for_function('() => {const v=document.querySelector("[data-preview=video] video");return v&&v.readyState>=2&&v.videoWidth>0}',timeout=30000)
                        sample='v=>({MediaError_code:v.error?.code??null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})'
                        before=page.locator('[data-preview=video] video').evaluate(sample)
                        page.locator('[data-video-play]').click()
                        page.wait_for_function('() => document.querySelector("[data-preview=video] video").currentTime>0.05',timeout=10000)
                        after=page.locator('[data-preview=video] video').evaluate(sample)
                        assert after['MediaError_code'] is None and after['currentTime']>before['currentTime']
                        page.locator('[data-preview=video] video').evaluate('v=>v.pause()')
                        audio=page.evaluate('''async()=>{const url=document.querySelector('[data-preview=video] video').currentSrc;
                            const data=await (await fetch(url)).arrayBuffer(),ctx=new AudioContext();
                            try {const decoded=await ctx.decodeAudioData(data);return {channels:decoded.numberOfChannels,samples:decoded.length,sampleRate:decoded.sampleRate}}
                            finally {await ctx.close()}}''')
                        assert audio['channels']>0 and audio['samples']>0
                        photo_box=page.locator('[data-preview=photo]').evaluate('''host=>{const img=host.querySelector('img'),a=host.getBoundingClientRect(),b=img.getBoundingClientRect();
                            return {host:{x:a.x,y:a.y,width:a.width,height:a.height},image:{x:b.x,y:b.y,width:b.width,height:b.height},natural:[img.naturalWidth,img.naturalHeight],objectFit:getComputedStyle(img).objectFit}}''')
                        a,b=photo_box['host'],photo_box['image']
                        assert b['x']>=a['x'] and b['y']>=a['y'] and b['x']+b['width']<=a['x']+a['width']+1 and b['y']+b['height']<=a['y']+a['height']+1
                        assert photo_box['objectFit']=='contain' and photo_box['natural']==[90,160]
                        with page.expect_download(timeout=30000) as download:
                            page.locator('[data-editor=video] [data-action=export]').click()
                        ui_export=out/'SOURCE_UI_EXPORT.zip';download.value.save_as(str(ui_export))
                        ui_sha=hashlib.sha256(ui_export.read_bytes()).hexdigest()
                        assert page.locator('[data-editor=video]').get_attribute('data-export-sha256')==ui_sha
                        with zipfile.ZipFile(ui_export) as z:assert z.testzip() is None
                        browser_result={'status':'PASS_SOURCE_BROWSER_RESTORE_PLAY_AUDIO_DECODE_PHOTO_FIT_EXPORT_CLICK',
                            'browser':browser.version,'media_before':before,'media_after':after,'audio_decode':audio,
                            'actual_audio_hearing_verified':False,'photo':photo_box,'ui_export_sha256':ui_sha}
                        page.screenshot(path=str(out/'SOURCE_BROWSER_AFTER_RESTART.png'),full_page=True)
                    finally:
                        browser.close()
            exported=call(base2,'/api/projects/'+saved['project_id']+'/export',{})
            archive=call(base2,exported['download_url'],raw=True)
            assert hashlib.sha256(archive).hexdigest()==exported['export']['sha256']
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                assert z.testzip() is None
                bundle=json.loads(z.read('BUNDLE_MANIFEST.json'))
                assert bundle['project_id']==saved['project_id']
                assert {item['role'] for item in bundle['files']}=={'input','output'}
                for item in bundle['files']:
                    content=z.read(item['archive_path'])
                    assert hashlib.sha256(content).hexdigest()==item['sha256']
                    assert len(content)==item['bytes']
                for job in reopened['jobs']:
                    content=z.read('jobs/'+job['job_id']+'/'+Path(job['primary_output']['path']).name)
                    assert hashlib.sha256(content).hexdigest()==expected[job['job_id']]
                members=z.namelist()
            result={'status':'PASS_'+platform.system().upper()+'_SOURCE_HTTP_COLD_RESTART_PHOTO_VIDEO_EXPORT',
                    'first_pid':pid1,'second_pid':pid2,'old_endpoint_closed':old_endpoint_closed,
                    'project_id':saved['project_id'],'path_diagnostics':path_diagnostics,'job_output_sha256':expected,'export_sha256':hashlib.sha256(archive).hexdigest(),
                    'zip_crc':'PASS','members':members,'bundle_files_verified':len(bundle['files']),'model_inference':False,
                    'scope':'GENERATED_FIXTURES_'+platform.system().upper()+'_SOURCE_HTTP_ONLY','source_browser':browser_result,'windows_exe_pass':False,
                    'owner_pc_pass':False,'full_product_pass':False}
            (out/'SOURCE_HTTP_EXPORT.zip').write_bytes(archive)
            (out/'SOURCE_HTTP_COLD_RESTART.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result))
        finally:
            if p is not None:
                p.terminate();p.wait(timeout=5);p.stdout.close()
            log.close()


if __name__=='__main__':main()
