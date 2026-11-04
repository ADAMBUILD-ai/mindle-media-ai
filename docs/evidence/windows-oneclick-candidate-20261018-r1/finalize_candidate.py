"""Finish a stopped assembly after excluding host copy staging files."""
from pathlib import Path
import sys,json,hashlib,re,zipfile
R=Path.cwd();sys.path.insert(0,str(R/'product/src'));from media_ai.workflow_worker import tree_sha
D=R/'delivery/MINDLE_MEDIA_AI_PC_TEST_20261018_R1';P=D/'_payload';E=R/'product/docs/evidence/windows-oneclick-candidate-20261018-r1'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def transient(p):return bool(re.fullmatch(r'\..+\.[A-Za-z0-9]{6}\.[A-Za-z0-9]{6}',p.name))
def files(root):return [p for p in sorted(root.rglob('*')) if p.is_file() and not transient(p)]
def write(p,s):
 if p.exists():p.unlink()
 p.write_text(s,encoding='utf-8')
(E/'ASSEMBLY_BEFORE_TRANSIENT_FILTER.txt').write_text((E/'ASSEMBLY_STDOUT.txt').read_text())
# Retain the verified complete base ZIP and extracted base; remove only redundant transport copies.
for pattern in ['artifact0?.zip','*.zip.part-*']:
 for p in (R/'windows-candidate-input').glob(pattern):p.unlink()
settings=json.loads((P/'RUNTIME_ENGINES.json').read_text());settings['planner']['runtime_sha256']=tree_sha((P/settings['planner']['executable']).parent);settings['tts']['runtime_sha256']=tree_sha(P/'runtime/site-packages/sherpa_onnx/lib');settings['tts']['data_sha256']=tree_sha(P/settings['tts']['data_path'])
write(P/'RUNTIME_ENGINES.json',json.dumps(settings,indent=2)+'\n')
models=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for top in ['models','omz'] for p in files(P/top)]
write(P/'MODEL_MANIFEST.json',json.dumps(models,indent=2)+'\n')
manifest=json.loads((P/'PACKAGE_MANIFEST.json').read_text());manifest['model_manifest_hash']=sha(P/'MODEL_MANIFEST.json');manifest['files']=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files(P) if p!=P/'PACKAGE_MANIFEST.json']
write(P/'PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
delivery=json.loads((D/'DELIVERY_MANIFEST.json').read_text());delivery.update(package_manifest_sha256=sha(P/'PACKAGE_MANIFEST.json'),files=len(manifest['files']),engine_manifest=settings)
write(D/'DELIVERY_MANIFEST.json',json.dumps(delivery,ensure_ascii=False,indent=2)+'\n');write(D/'DELIVERY_ARTIFACT_SHA256.txt',sha(D/'MINDLE_MEDIA_AI_RUN.exe')+'  MINDLE_MEDIA_AI_RUN.exe\n'+sha(P/'PACKAGE_MANIFEST.json')+'  _payload/PACKAGE_MANIFEST.json\n')
(E/'ASSEMBLY.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
for item in manifest['files']:
 p=P/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],item['path']
print('FINAL MANIFEST PASS',len(manifest['files']),flush=True)
base=Path(delivery['base_readback']['base_path']);old=json.loads((base/'_payload/PACKAGE_MANIFEST.json').read_text())
for item in old['files']:
 p=base/'_payload'/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'BASE_CHANGED '+item['path']
print('BASE PRESERVED PASS',len(old['files']),flush=True)
archive=D.with_suffix('.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
 for p in files(D):z.write(p,D.name+'/'+p.relative_to(D).as_posix())
print('ZIP CREATED',archive.stat().st_size,flush=True)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
receipt={'file':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'zip_crc':'PASS','source':manifest['build_commit'],'manifest_files_verified':len(manifest['files']),'base_files_preserved':len(old['files']),'native_windows_acceptance':'PENDING','full_product_pass':False}
(E/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
