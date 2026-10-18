"""Assemble one owner-authorized development candidate from verified frozen inputs.
No native Windows execution or final product PASS is implied.
"""
from pathlib import Path
import os,hashlib,json,shutil,zipfile,urllib.request,sys
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'product/src'))
from media_ai.workflow_worker import tree_sha
SOURCE='e00e6e0b82994fca628d6ca3cf039f7dc43c15c6'
INPUT=ROOT/'windows-candidate-input';BASE=Path(json.loads((INPUT/'BASE_READBACK.json').read_text())['base_path'])
DEST=ROOT/'delivery/MINDLE_MEDIA_AI_PC_TEST_20261018_R1';DEST.parent.mkdir(exist_ok=True)
if DEST.exists():raise RuntimeError('fresh output required')
shutil.copytree(BASE,DEST,copy_function=os.link)
P=DEST/'_payload';E=ROOT/'product/docs/evidence/windows-oneclick-candidate-20261018-r1'
def sha(p,algorithm='sha256'):
 with p.open('rb') as f:return hashlib.file_digest(f,algorithm).hexdigest()
def write(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.unlink()
 if isinstance(data,str):p.write_text(data,encoding='utf-8')
 else:p.write_bytes(data)
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():dst.unlink()
 shutil.copyfile(src,dst)
def gitsha(p):
 h=hashlib.sha1(('blob '+str(p.stat().st_size)+'\0').encode())
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
canonical=json.loads((INPUT/'CANONICAL_FILES.json').read_text());allowed={x['path'] for x in canonical};code_rows=[]
for item in canonical:
 relative=item['path'];target=P/'app'/relative;local=ROOT/'product'/relative
 if local.is_file() and gitsha(local)==item['sha']:copy(local,target)
 elif not target.is_file() or gitsha(target)!=item['sha']:
  with urllib.request.urlopen('https://raw.githubusercontent.com/ADAMBUILD-ai/mindle-media-ai/'+SOURCE+'/'+relative,timeout=30) as response:write(target,response.read())
 assert gitsha(target)==item['sha'],relative
 code_rows.append({'path':relative,'git_blob_sha':item['sha'],'sha256':sha(target)})
for folder in ['src','ui']:
 for f in (P/'app'/folder).rglob('*'):
  if f.is_file() and f.relative_to(P/'app').as_posix() not in allowed:f.unlink()
copy(ROOT/'product/scripts/employee_package_launcher.py',P/'app/launcher/employee_package_launcher.py')
print('CANONICAL SOURCE/UI VERIFIED',len(code_rows),flush=True)
# New native Windows runtime, not the Linux validation binaries.
llama=P/'tools/llama';llama.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(INPUT/'llama-b11716-bin-win-cpu-x64.zip') as z:
 assert z.testzip() is None;z.extractall(llama)
cli=next(llama.rglob('llama-completion.exe'))
site=P/'runtime/site-packages';wheel_rows=[]
for wheel in sorted((INPUT/'windows-wheels').glob('*.whl')):
 with zipfile.ZipFile(wheel) as z:
  assert z.testzip() is None
  for name in z.namelist():
   if name.endswith('/'):continue
   if '..' in Path(name).parts:raise RuntimeError('invalid wheel path')
   write(site/name,z.read(name))
 wheel_rows.append({'name':wheel.name,'bytes':wheel.stat().st_size,'sha256':sha(wheel)})
assert (site/'sherpa_onnx/lib/_sherpa_onnx.cp311-win_amd64.pyd').is_file()
assert (site/'sherpa_onnx/lib/onnxruntime.dll').is_file()
# Preserve original PHOTO/STT/SISR weights byte for byte; append new local engines.
qwen=P/'models/qwen2.5-1.5b-instruct';qwen.mkdir(parents=True,exist_ok=True)
copy(ROOT/'local-engines/qwen15.gguf',qwen/'model.gguf')
copy(ROOT/'product/docs/evidence/media-ai-local-engines-closeout-20261018/QWEN15_LICENSE',qwen/'LICENSE')
copy(ROOT/'product/docs/evidence/media-ai-local-engines-closeout-20261018/QWEN15_README.md',qwen/'README.md')
neural=P/'models/supertonic3';shutil.copytree(ROOT/'local-engines/supertonic-verified/sherpa-onnx-supertonic-3-tts-int8-2026-05-11',neural)
copy(ROOT/'local-engines/SUPERTONIC_LICENSE',neural/'MODEL_LICENSE_OpenRAIL-M.txt')
settings={'planner':{'executable':cli.relative_to(P).as_posix(),'executable_sha256':sha(cli),'runtime_sha256':tree_sha(cli.parent),'model_path':(qwen/'model.gguf').relative_to(P).as_posix(),'model_sha256':sha(qwen/'model.gguf'),'revision':'91cad51170dc346986eccefdc2dd33a9da36ead9','model_id':'Qwen/Qwen2.5-1.5B-Instruct-GGUF','license':'Apache-2.0'},'tts':{'engine':'sherpa-supertonic','data_path':neural.relative_to(P).as_posix(),'data_sha256':tree_sha(neural),'runtime_version':'1.13.8','runtime_sha256':tree_sha(site/'sherpa_onnx/lib'),'model_revision':'3cadd1ee6394adea1bd021217a0e650ede09a323','archive_sha256':'82fa96f91c4ef8abaae3a14a3f4153facf88bed821d1f7331cec2700f432c427','license':'OpenRAIL-M (model); MIT (upstream code)'}}
assert settings['planner']['model_sha256']=='6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
write(P/'RUNTIME_ENGINES.json',json.dumps(settings,ensure_ascii=False,indent=2)+'\n')
write(P/'LICENSES/LOCAL_ENGINE_NOTICES.txt','Qwen model: Apache-2.0. llama.cpp: MIT (bundled LICENSE). sherpa-onnx/core: Apache-2.0 (wheel notices retained). Supertonic model: OpenRAIL-M; upstream code MIT. See models/supertonic3/MODEL_LICENSE_OpenRAIL-M.txt. No model licence is replaced by the code licence.\n')
old=json.loads((P/'PACKAGE_MANIFEST.json').read_text());copy(P/'MODEL_MANIFEST.json',P/'BASE_C37_MODEL_MANIFEST.json')
models=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for top in ['models','omz'] for p in sorted((P/top).rglob('*')) if p.is_file()]
write(P/'MODEL_MANIFEST.json',json.dumps(models,indent=2)+'\n')
ui_names=['index.html','approved_visual.css','interaction.css','interaction.js','product_integration.js','photo_workspace.js','video_workspace.js','workspace_shell.js','timeline_preview.js','workflow_execution.js','assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico']
fingerprint=hashlib.sha256('\n'.join('ui/'+n+':'+sha(P/'app/ui'/n) for n in ui_names).encode()).hexdigest()
manifest={**old,'build_commit':SOURCE,'runtime_id':SOURCE[:12]+'-'+fingerprint[:12]+'-pc-test-r1','ui_fingerprint':fingerprint,'model_manifest_hash':sha(P/'MODEL_MANIFEST.json'),'release_channel':'OWNER_DEVELOPMENT_VERIFICATION_NOT_FINAL_RELEASE','data_directory_name':'MEDIA_AI_CANDIDATE_20261018_R1','bootstrap_reused_from':'c37c7819b1454996f3510f92184b1ef62faf3c78','native_windows_acceptance':'PENDING','approved_ui_exact_match':False}
manifest['files']=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file() and p.relative_to(P).as_posix()!='PACKAGE_MANIFEST.json']
write(P/'PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
exe=DEST/'MINDLE_MEDIA_AI_RUN.exe';assert sha(exe)=='24fe0ad565a5568b392b32040d7789cbd8abce7b60e8dade97666bbd1ec2888c'
delivery={'source_commit':SOURCE,'runtime_id':manifest['runtime_id'],'release_channel':manifest['release_channel'],'launcher_sha256':sha(exe),'package_manifest_sha256':sha(P/'PACKAGE_MANIFEST.json'),'files':len(manifest['files']),'native_windows_execution':'NOT_RUN_HERE','base_readback':json.loads((INPUT/'BASE_READBACK.json').read_text()),'windows_wheels':wheel_rows,'canonical_source_files':code_rows,'engine_manifest':settings,'authorization':'Owner request 2026-10-18 KST: make and send a double-click Windows UI/product candidate for laptop/desktop; one development candidate only. No merge/final employee release.'}
write(DEST/'DELIVERY_MANIFEST.json',json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
write(DEST/'DELIVERY_ARTIFACT_SHA256.txt',sha(exe)+'  MINDLE_MEDIA_AI_RUN.exe\n'+sha(P/'PACKAGE_MANIFEST.json')+'  _payload/PACKAGE_MANIFEST.json\n')
write(DEST/'먼저_읽어주세요.txt','MINDLE MEDIA AI — 2026-10-18 개발 검증 후보 R1\n\n1. ZIP을 짧은 경로의 폴더에 모두 압축 해제합니다. ZIP 안에서 직접 실행하지 마세요.\n2. MINDLE_MEDIA_AI_RUN.exe를 더블클릭합니다. 첫 실행은 대용량 모델·파일 검증과 자동 준비 때문에 시간이 걸립니다.\n3. 제품 화면이 열리면 사용합니다. Python·pip·Git·모델 다운로드 명령을 직접 입력할 필요가 없습니다.\n\nWindows 10/11 64비트용. 압축 해제와 별도 실행 환경 복사를 위해 여유 공간 약 35GB 이상을 권장합니다.\n기존 c37 설치·자료는 덮어쓰지 않습니다. 이번 후보의 작업 자료는 LOCALAPPDATA\\MINDLE\\MEDIA_AI_CANDIDATE_20261018_R1에 별도 저장합니다. 기존 프로젝트를 자동 복사하지 않습니다.\n최신 소스·생성형 Qwen·한국어 신경망 TTS와 기존 사진·영상 모델을 포함했습니다. 현재 승인 UI와 남은 차이가 있고, 이 후보 자체의 Windows EXE 실행·실제 소리 청취 인수는 미완료입니다. 최종 승인 배포본이 아닙니다.\n실행 오류가 나면 창의 오류 문구와 위 별도 데이터 폴더의 logs/server.log를 보존해 주세요. 다른 Python/Chrome을 일괄 종료하거나 lock을 삭제하지 마세요.\n')
(E/'ASSEMBLY.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
print('CANDIDATE ASSEMBLED',len(manifest['files']),flush=True)
# Re-read every final package file and original base file before publishing.
for item in manifest['files']:
 p=P/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],item['path']
for item in old['files']:
 p=BASE/'_payload'/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'BASE_CHANGED '+item['path']
print('FINAL AND BASE MANIFESTS PASS',flush=True)
archive=DEST.with_suffix('.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 for p in sorted(DEST.rglob('*')):
  if p.is_file():z.write(p,DEST.name+'/'+p.relative_to(DEST).as_posix())
print('ZIP CREATED',archive.stat().st_size,flush=True)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
receipt={'file':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'zip_crc':'PASS','source':SOURCE,'manifest_files_verified':len(manifest['files']),'base_files_preserved':len(old['files']),'native_windows_acceptance':'PENDING','full_product_pass':False}
(E/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
