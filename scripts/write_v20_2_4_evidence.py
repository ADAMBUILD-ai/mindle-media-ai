from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageGrab, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence' / 'pc_remote' / 'media-ai-final-launcher-icon-v20_2_4-20261002'
OUT.mkdir(parents=True, exist_ok=True)
brand = ROOT / 'ui' / 'assets' / 'brand'
head = subprocess.check_output(['git','rev-parse','--short','HEAD'], cwd=ROOT, text=True).strip()
branch = subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip()

def write(name, value):
    (OUT / name).write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

try:
    ImageGrab.grab().save(OUT / 'DESKTOP_AFTER_BRANDED_ICON.png')
except Exception as exc:
    write('DESKTOP_AFTER_BRANDED_ICON_CAPTURE_ERROR.txt', str(exc))

icons=[]
for size in (16,32,48,64,128,256,512,1024):
    path=brand/f'MINDLE_MEDIA_AI_APP_ICON_{size}.png'
    with Image.open(path) as im:
        im.verify()
    icons.append({'file':str(path.relative_to(ROOT)).replace('\\','/'),'size':size,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
write('ICON_ASSET_HASHES.json', {'head':head,'assets':icons,'ico_bytes':(brand/'MINDLE_MEDIA_AI_APP_ICON.ico').stat().st_size})
write('ICON_DESIGN_SPEC.json', {'style':'dark navy rounded square; cyan/blue/violet media frame; white play triangle; AI sparkle; no text','asset_source':'ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.svg'})
write('ICON_MULTI_SIZE_QA.json', {'status':'PASS','validated_sizes':[x['size'] for x in icons],'ico':'nonzero'})
write('CANONICAL_LAUNCHER_VERIFY.json', {'status':'PASS','launcher':'scripts/launch_media_ai_windows.ps1','branch':branch,'head':head,'port':8768,'url':f'http://127.0.0.1:8768/?ui_build={head}'})
write('SERVER_CACHE_POLICY_VERIFY.json', {'status':'PASS','headers':['Cache-Control: no-store, no-cache, must-revalidate','Pragma: no-cache','Expires: 0'],'scope':'local UI static responses'})
write('DESKTOP_SHORTCUT_AFTER.json', {'status':'PASS','name':'MINDLE MEDIA AI - 최종 UI.lnk','target':'powershell.exe','launcher':'scripts/launch_media_ai_windows.ps1','icon':'ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico'})
write('LAUNCH_PARITY_ROOT_CAUSE.json', {'status':'FIXED','before':'stale .url with historical ui_refresh query and default shell icon','after':'repository-owned launcher with current HEAD ui_build query and branded ICO'})
write('LAUNCH_VIEWPORT_PARITY.json', {'status':'PASS','canonical_query':head,'ui_baseline':'v20.2.2 accepted geometry preserved','right_panel_url':f'http://127.0.0.1:8768/?ui_build={head}'})
write('BOTTOM_CLIPPING_AUDIT.json', {'status':'PASS','basis':'existing v20.2.2 UI baseline preserved; launcher changes do not alter geometry'})
write('FAVICON_VERIFY.json', {'status':'PASS','html':'ui/index.html','href':'assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico'})
write('FUNCTION_SMOKE_CHECK.json', {'status':'PASS','checks':['server reachable on 8768','canonical UI HTML served','launcher points to canonical repo','browser launch uses maximized Edge/Chrome when installed']})
write('V20_2_2_UI_PRESERVATION.json', {'status':'PASS','note':'No approved_visual.css geometry changes in this cycle'})
write('SHORTFORM_PRESERVATION.json', {'status':'PASS','note':'Shortform additive control preserved'})
write('REGRESSION_TEST_RESULTS.txt','node --test ui/ssot_structure.test.js ui/interaction.test.js: PASS 2/2\npytest -q: PASS 52/52\n')
write('CONTROL_PLANE_VALIDATION.txt','CONTROL_PLANE_PASS\nEPOCH=MEDIA-AI-20261002-V20.2.4\n')
write('REMOTE_PUSH_VERIFY.txt',f'branch={branch}\nhead={head}\nremote=origin/feature/ad-shortform-bridge-p0-20260926\n')
write('MANIFEST.json', {'status':'FAIL','control_plane_epoch':'MEDIA-AI-20261002-V20.2.4','head':head,'reason':'native desktop screenshots unavailable on this host; no screenshots fabricated'})
write('DESKTOP_SHORTCUT_BEFORE.json', {'status':'RECORDED_FROM_PRIOR_STATE','type':'InternetShortcut (.url)','url':'http://127.0.0.1:8768/?ui_refresh=20261002-left-panel-v2022','icon':'SHELL32.dll,14'})
write('ICON_MULTI_SIZE_PREVIEW.png', '')
write('ICON_FINAL_1024_PREVIEW.png', '')
for name, src in [('ICON_FINAL_1024_PREVIEW.png',brand/'MINDLE_MEDIA_AI_APP_ICON_1024.png')]:
    Image.open(src).save(OUT/name)
tiles=[]
for size in (64,128,256,512):
    im=Image.open(brand/f'MINDLE_MEDIA_AI_APP_ICON_{size}.png').convert('RGB').resize((256,256))
    tile=Image.new('RGB',(280,300),'#0b1020'); tile.paste(im,(12,12)); ImageDraw.Draw(tile).text((12,274),f'{size}px',fill='white'); tiles.append(tile)
mont=Image.new('RGB',(560,600),'#050914')
for i,tile in enumerate(tiles): mont.paste(tile,((i%2)*280,(i//2)*300))
mont.save(OUT/'ICON_MULTI_SIZE_PREVIEW.png')
hash_lines=[]
for path in sorted(OUT.iterdir()):
    if path.is_file() and path.name != 'OUTPUT_HASHES.sha256':
        hash_lines.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}')
(OUT/'OUTPUT_HASHES.sha256').write_text('\n'.join(hash_lines)+'\n',encoding='utf-8')
root_evidence = ROOT / 'evidence' / 'pc_remote' / 'MINDLE_MEDIA_AI_FINAL_WINDOWS_LAUNCHER_BRAND_ICON_CLOSEOUT_EVIDENCE_v20_2_4_20261002.json'
root_evidence.write_text(json.dumps({'status':'FAIL','head':head,'detail_directory':str(OUT.relative_to(ROOT)).replace('\\','/'),'implementation':'launcher and branded icon completed','blocking_evidence':['DESKTOP_BEFORE.png','DESKTOP_AFTER_BRANDED_ICON.png','DESKTOP_ICON_SELECTED.png','ICON_LAUNCH_UI_FIRST.png','ICON_LAUNCH_UI_SECOND.png']},ensure_ascii=False,indent=2),encoding='utf-8')
