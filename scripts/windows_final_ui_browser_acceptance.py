"""Headless browser acceptance for the packaged final MINDLE MEDIA AI UI."""
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

def locate(root: Path, name: str) -> Path:
    matches=list(root.rglob(name))
    if len(matches)!=1:
        raise RuntimeError(f"fixture {name!r} expected once, found {len(matches)}")
    return matches[0]

def find_server() -> str:
    deadline=time.monotonic()+120
    while time.monotonic()<deadline:
        for port in range(18768,18778):
            try:
                base=f"http://127.0.0.1:{port}"
                with urlopen(base+"/api/runtime-identity",timeout=2) as r:
                    if json.loads(r.read().decode("utf-8")).get("runtime_mode")=="LOCAL_OFFLINE_PACKAGE":
                        return base
            except Exception:
                pass
        time.sleep(.5)
    raise RuntimeError("packaged server not found")

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--skip-model-inference",action="store_true")
    ap.add_argument("--fixture-root",type=Path,required=True)
    ap.add_argument("--evidence-root",type=Path,required=True)
    args=ap.parse_args()
    args.evidence_root.mkdir(parents=True,exist_ok=True)
    photo=locate(args.fixture_root,"36b38c8b-2ebd-4c8e-b26d-6f70f016f5b1_intel_sisr_1032_street_480x270.png")
    video=locate(args.fixture_root,"448197c5-ae84-421a-89a6-713b2880171e_big_buck_bunny.mp4")
    base=find_server()
    result={"status":"FAIL","base_url":base,"checks":{}}
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="chrome",headless=True)
        result["browser"]={"channel":"chrome","version":browser.version}
        page=browser.new_page(viewport={"width":1536,"height":1024},device_scale_factor=1)
        http=[];errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('response',lambda response:http.append({'url':response.url,'status':response.status}) if '/api/' in response.url or '/files/' in response.url else None)
        try:
            page.goto(base,wait_until="networkidle",timeout=120000)
            page.wait_for_function("() => window.mindleRestoreReady===true",timeout=120000)
            result['codec_capability']=page.evaluate("""()=>{const v=document.createElement('video');return {h264:v.canPlayType('video/mp4; codecs="avc1.42E01E"'),aac:v.canPlayType('audio/mp4; codecs="mp4a.40.2"'),userAgent:navigator.userAgent}}""")
            if not result['codec_capability']['h264'] or not result['codec_capability']['aac']:raise RuntimeError('Official Chrome media codec preflight failed')
            body=page.locator("body").inner_text()
            for marker in ("MINDLE MEDIA AI","Create. Edit. Together.","VIDEO","PHOTO","AI가 만드는 더 큰 가능성","for a better tomorrow","신작가님"):
                if marker not in body:
                    raise RuntimeError("final UI marker missing: "+marker)
            if "사진과 영상을 더 멋지게, 더 쉬운 작업" in body:
                raise RuntimeError("legacy UI shipped")
            vb=page.locator('[data-editor="video"]').bounding_box()
            pb=page.locator('[data-editor="photo"]').bounding_box()
            if not vb or not pb or not (vb["x"]<pb["x"] and abs(vb["y"]-pb["y"])<8 and vb["width"]>550 and pb["width"]>550):
                raise RuntimeError(f"VIDEO/PHOTO not side-by-side: {vb} {pb}")
            ph=page.locator('[data-preview="photo"]').bounding_box()
            if not ph or ph["width"]/ph["height"]<1.45:
                raise RuntimeError(f"PHOTO preview is not landscape-first: {ph}")
            page.screenshot(path=str(args.evidence_root/"FINAL_UI_RUNTIME_SCREENSHOT.png"),full_page=True)
            result["checks"]["final_ui_geometry"]="PASS"
    
            page.locator('[data-editor="photo"] [data-primary-input="photo"]').set_input_files(str(photo))
            page.wait_for_function("() => document.querySelector('[data-preview=photo]').dataset.previewStatus === 'actual-output'",timeout=120000)
            preview=page.locator('[data-preview="photo"]')
            before=preview.screenshot()
            page.locator('[data-photo-adjust="brightness"]').fill("35")
            page.wait_for_timeout(250)
            after=preview.screenshot()
            if sha(before)==sha(after):
                raise RuntimeError("photo live correction did not visibly change preview")
            if page.locator('[data-photo-adjust="brightness"] + output').text_content().strip()!="35":
                raise RuntimeError("photo slider output did not move")
            for key,value in (("contrast","20"),("highlights","15"),("shadows","18"),("saturation","22"),("temperature","14"),("sharpness","12")):
                page.locator(f'[data-photo-adjust="{key}"]').fill(value)
                if page.locator(f'[data-photo-adjust="{key}"] + output').text_content().strip()!=value:
                    raise RuntimeError("photo slider did not move: "+key)
            page.locator('[data-photo-apply]').click()
            page.wait_for_function("() => document.querySelector('[data-photo-status]').textContent.includes('보정 적용 완료')",timeout=120000)
            result["checks"]["photo_live_and_apply"]="PASS"
    
            if not args.skip_model_inference:
                page.locator('[data-photo-tool="segment"]').click()
                page.wait_for_function("""() => {
                  const t=document.querySelector('[data-editor=photo] [data-command-error]').textContent;
                  return t.includes('편집 완료') || t.includes('배경 제거 완료');
                }""",timeout=240000)
                result["checks"]["photo_background_button"]="PASS"
        
            page.wait_for_function("() => !window.mindleEditPending('photo')&&!window.mindleEditPending('video')",timeout=120000)
            old_video_job=page.locator('[data-preview=video]').get_attribute('data-job-id')
            page.locator('[data-editor="video"] [data-primary-input="video"]').set_input_files(str(video))
            page.wait_for_function("""old => {
              const host=document.querySelector('[data-preview=video]');
              const message=document.querySelector('[data-editor=video] [data-command-error]');
              if(message.dataset.result==='error' && message.textContent) throw new Error(message.textContent);
              const v=host.querySelector('video');
              return host.dataset.jobId!==old&&host.dataset.operation==='import'&&!window.mindleEditPending('video')&&v&&v.readyState>=2&&v.videoWidth>0&&!v.error;
            }""",arg=old_video_job,timeout=120000)
            result['media_before_play']=page.locator('[data-preview=video] video').evaluate('(v)=>({MediaError_code:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})')
            page.locator('[data-video-play]').click()
            page.wait_for_timeout(1600)
            current=page.locator('[data-preview="video"] video').evaluate("(v)=>v.currentTime")
            result['media_after_play']=page.locator('[data-preview=video] video').evaluate('(v)=>({MediaError_code:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime})')
            if current<=0:
                raise RuntimeError("video play button produced no movement")
            page.locator('[data-video-play]').click()
            page.locator('[data-video-option="brightness"]').fill("18")
            filt=page.locator('[data-preview="video"] video').evaluate("(v)=>getComputedStyle(v).filter")
            if not filt or filt=="none":
                raise RuntimeError("video live correction did not update preview")
            page.locator('[data-video-apply]').click()
            page.wait_for_function("() => document.querySelector('[data-editor=video] [data-command-error]').textContent.includes('영상 편집 완료')",timeout=240000)
            result["checks"]["video_play_and_edit"]="PASS"
            from PIL import Image
            portrait=args.evidence_root/"portrait-r9-fixture.png"
            Image.new("RGB",(90,160),(190,80,30)).save(portrait)
            page.locator('[data-editor="photo"] [data-primary-input="photo"]').set_input_files(str(portrait))
            page.wait_for_function("() => {const i=document.querySelector('[data-preview=photo] img');return i&&i.naturalWidth===90&&i.naturalHeight===160&&!window.mindleEditPending('photo')}",timeout=30000)
            fit=page.locator('[data-preview=photo]').evaluate("""h=>{const i=h.querySelector('img'),a=h.getBoundingClientRect(),b=i.getBoundingClientRect(),c=getComputedStyle(i);return {host:{x:a.x,y:a.y,width:a.width,height:a.height},image:{x:b.x,y:b.y,width:b.width,height:b.height},objectFit:c.objectFit,objectPosition:c.objectPosition,natural:[i.naturalWidth,i.naturalHeight]}}""")
            a,b=fit["host"],fit["image"]
            assert fit["objectFit"]=="contain" and b["x"]>=a["x"] and b["y"]>=a["y"] and b["x"]+b["width"]<=a["x"]+a["width"]+1 and b["y"]+b["height"]<=a["y"]+a["height"]+1
            result["checks"]["portrait_auto_fit"]="PASS"
            result["portrait_geometry"]=fit
            page.screenshot(path=str(args.evidence_root/"FINAL_UI_FUNCTION_AFTER.png"),full_page=True)
        except Exception as error:
            result['error']=repr(error)
            result['media_diagnostics']=page.evaluate("""() => {const v=document.querySelector('[data-preview=video] video');return {media:v?{MediaError_code:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,videoHeight:v.videoHeight,currentSrc:v.currentSrc,currentTime:v.currentTime}:null,preview:document.querySelector('[data-preview=video]').dataset.previewStatus,videoMessage:document.querySelector('[data-editor=video] [data-command-error]').textContent,photoMessage:document.querySelector('[data-editor=photo] [data-command-error]').textContent,pendingVideo:window.mindleEditPending('video'),pendingPhoto:window.mindleEditPending('photo')}}""")
            page.screenshot(path=str(args.evidence_root/'BROWSER_FAILURE.png'),full_page=True)
            raise
        finally:
            result['http_responses']=http;result['page_errors']=errors
            (args.evidence_root/'FINAL_UI_BROWSER_ACCEPTANCE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        browser.close()
    result["status"]="FINAL_UI_BROWSER_FUNCTION_PASS"
    (args.evidence_root/"FINAL_UI_BROWSER_ACCEPTANCE.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

