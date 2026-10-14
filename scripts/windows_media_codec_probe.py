"""Compare exact Windows MF H264 preview in bundled Chromium and installed Chrome."""
import hashlib,http.server,json,os,shutil,subprocess,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
from media_ai.browser_preview import create_preview
root=Path(__file__).resolve().parents[1];out=root/'codec_probe_evidence';out.mkdir(exist_ok=True)
package=root/'codec_probe_runtime';target=package/'tools/ffmpeg';target.mkdir(parents=True,exist_ok=True)
binary=next((root/'codec_probe_ffmpeg').rglob('ffmpeg.exe'))
for f in binary.parent.iterdir():
    if f.is_file():shutil.copy2(f,target/f.name)
os.environ['MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT']=str(package)
source=root/'docs/evidence/media-ai-general-work-final-self-audit-20261008/KOREAN_SUBTITLE_ACTUAL.mp4'
assert source.is_file()
receipt=create_preview(source,hashlib.sha256(source.read_bytes()).hexdigest(),out/'preview.mp4')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),lambda *a,**k:http.server.SimpleHTTPRequestHandler(*a,directory=str(out),**k))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
result={'status':'RUNNING','source_commit':os.environ['GITHUB_SHA'],'preview':receipt,'browsers':[]}
try:
    with sync_playwright() as p:
        for name,channel in [('bundled_chromium',None),('google_chrome','chrome')]:
            row={'browser':name}
            try:
                browser=p.chromium.launch(headless=True,**({'channel':channel} if channel else {}));page=browser.new_page();row['version']=browser.version
                page.goto(f'http://127.0.0.1:{server.server_port}/preview.mp4')
                # Direct media document is served from the same exact preview bytes.
                page.wait_for_selector('video',timeout=10000)
                row['capability']=page.evaluate("""()=>{const v=document.querySelector('video');return {h264:v.canPlayType('video/mp4; codecs="avc1.42E01E"'),aac:v.canPlayType('audio/mp4; codecs="mp4a.40.2"'),userAgent:navigator.userAgent}}""")
                try:page.wait_for_function("()=>{const v=document.querySelector('video');return v.error||v.readyState>=2}",timeout=15000)
                except Exception:pass
                row['before_play']=page.locator('video').evaluate("(v)=>({MediaError_code:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})")
                if row['before_play']['MediaError_code'] is None and row['before_play']['readyState']>=2:
                    page.locator('video').evaluate('(v)=>{v.muted=true;return v.play()}');page.wait_for_timeout(1200)
                row['after_play']=page.locator('video').evaluate("(v)=>({MediaError_code:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})")
                row['status']='PASS' if row['after_play']['currentTime']>0 and row['after_play']['videoWidth']>0 and row['after_play']['MediaError_code'] is None else 'FAIL'
                page.screenshot(path=str(out/(name+'.png')));browser.close()
            except Exception as e:row.update(status='BLOCKED',error=repr(e))
            result['browsers'].append(row);(out/'CODEC_MATRIX.json').write_text(json.dumps(result,indent=2)+'\n')
    chrome=next(x for x in result['browsers'] if x['browser']=='google_chrome')
    result['status']='PASS_OFFICIAL_CHROME_EXACT_H264_PREVIEW' if chrome['status']=='PASS' else 'FAIL_OFFICIAL_CHROME_PREVIEW'
finally:
    server.shutdown();server.server_close();(out/'CODEC_MATRIX.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['status']=='PASS_OFFICIAL_CHROME_EXACT_H264_PREVIEW',result
import base64
from media_ai.product_runtime import ProductJobService
service=ProductJobService(root/'codec_probe_data','')
result['filter_inventory']=subprocess.check_output([str(target/'ffmpeg.exe'),'-hide_banner','-filters'],text=True,stderr=subprocess.STDOUT)
result['malgun_available']=(Path(os.environ.get('SystemRoot','C:/Windows'))/'Fonts/malgun.ttf').is_file()
result['edit_tests']=[]
for name,options in [('brightness_contrast_saturation',{'brightness':18,'contrast':20,'saturation':15}),('denoise',{'denoise':True}),('stabilize',{'stabilize':True}),('effect',{'effect':True}),('fade',{'fade':True}),('korean_subtitle',{'subtitle':'한국어 자막 검증'})]:
    row={'test':name,'options':options}
    try:
        edited=service.edit_video({'filename':source.name,'content_base64':base64.b64encode(source.read_bytes()).decode(),'options':options})
        row.update(status='PASS',result=edited)
    except subprocess.CalledProcessError as e:row.update(status='FAIL',error=repr(e),stderr=e.stderr.decode(errors='replace') if isinstance(e.stderr,bytes) else e.stderr)
    except Exception as e:row.update(status='FAIL',error=repr(e))
    result['edit_tests'].append(row);(out/'CODEC_MATRIX.json').write_text(json.dumps(result,indent=2)+'\\n')
result['status']='PASS_CHROME_AND_LGPL_NATIVE_EDIT_FILTERS' if all(x['status']=='PASS' for x in result['edit_tests']) else 'FAIL_NATIVE_EDIT_FILTERS'
(out/'CODEC_MATRIX.json').write_text(json.dumps(result,indent=2)+'\\n')
assert result['status']=='PASS_CHROME_AND_LGPL_NATIVE_EDIT_FILTERS',result
