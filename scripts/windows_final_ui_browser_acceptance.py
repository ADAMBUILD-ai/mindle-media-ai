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
    ap.add_argument("--fixture-root",type=Path,required=True)
    ap.add_argument("--evidence-root",type=Path,required=True)
    args=ap.parse_args()
    args.evidence_root.mkdir(parents=True,exist_ok=True)
    photo=locate(args.fixture_root,"36b38c8b-2ebd-4c8e-b26d-6f70f016f5b1_intel_sisr_1032_street_480x270.png")
    video=locate(args.fixture_root,"448197c5-ae84-421a-89a6-713b2880171e_big_buck_bunny.mp4")
    base=find_server()
    result={"status":"FAIL","base_url":base,"checks":{}}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1536,"height":1024},device_scale_factor=1)
        page.goto(base,wait_until="networkidle",timeout=120000)
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

        page.locator('[data-photo-tool="segment"]').click()
        page.wait_for_function("""() => {
          const t=document.querySelector('[data-editor=photo] [data-command-error]').textContent;
          return t.includes('편집 완료') || t.includes('배경 제거 완료');
        }""",timeout=240000)
        result["checks"]["photo_background_button"]="PASS"

        page.locator('[data-editor="video"] [data-primary-input="video"]').set_input_files(str(video))
        page.wait_for_function("() => document.querySelector('[data-preview=video]').dataset.previewStatus === 'actual-output'",timeout=120000)
        page.locator('[data-video-play]').click()
        page.wait_for_timeout(1600)
        current=page.locator('[data-preview="video"] video').evaluate("(v)=>v.currentTime")
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
        page.screenshot(path=str(args.evidence_root/"FINAL_UI_FUNCTION_AFTER.png"),full_page=True)
        browser.close()
    result["status"]="FINAL_UI_BROWSER_FUNCTION_PASS"
    (args.evidence_root/"FINAL_UI_BROWSER_ACCEPTANCE.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
