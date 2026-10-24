"""Remove copy staging leftovers, preserving complete models and the frozen base."""
from pathlib import Path
import re,json,hashlib,subprocess,zipfile,sys
R=Path.cwd();sys.path.insert(0,str(R/'product/src'));from media_ai.workflow_worker import tree_sha
D=R/'delivery/MINDLE_MEDIA_AI_PC_TEST_20261018_R1';P=D/'_payload';E=R/'product/docs/evidence/windows-oneclick-candidate-20261018-r1';archive=D.with_suffix('.zip')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def stage(p):return bool(re.fullmatch(r'\..+\.[A-Za-z0-9]{6}(?:\.[A-Za-z0-9]{6})?',p.name))
def write(p,obj):
 if p.exists():p.unlink()
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
removed=[]
for p in list(P.rglob('*')):
 if p.is_file() and stage(p):
  removed.append({'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)});p.unlink()
(E/'PRUNED_COPY_STAGING_FILES.json').write_text(json.dumps({'reason':'Unreferenced hidden copy staging files; complete model/executable paths retained. Original frozen base preserved.','files':removed},indent=2)+'\n')
settings=json.loads((P/'RUNTIME_ENGINES.json').read_text());settings['planner']['runtime_sha256']=tree_sha((P/settings['planner']['executable']).parent);settings['tts']['runtime_sha256']=tree_sha(P/'runtime/site-packages/sherpa_onnx/lib');settings['tts']['data_sha256']=tree_sha(P/settings['tts']['data_path']);write(P/'RUNTIME_ENGINES.json',settings)
models=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for top in ['models','omz'] for p in sorted((P/top).rglob('*')) if p.is_file()];write(P/'MODEL_MANIFEST.json',models)
m=json.loads((P/'PACKAGE_MANIFEST.json').read_text());m['model_manifest_hash']=sha(P/'MODEL_MANIFEST.json');m['files']=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file() and p!=P/'PACKAGE_MANIFEST.json'];write(P/'PACKAGE_MANIFEST.json',m)
delivery=json.loads((D/'DELIVERY_MANIFEST.json').read_text());delivery.update(files=len(m['files']),package_manifest_sha256=sha(P/'PACKAGE_MANIFEST.json'),engine_manifest=settings,pruned_copy_staging_files=len(removed));write(D/'DELIVERY_MANIFEST.json',delivery);(E/'ASSEMBLY.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
p=D/'DELIVERY_ARTIFACT_SHA256.txt';p.unlink();p.write_text(sha(D/'MINDLE_MEDIA_AI_RUN.exe')+'  MINDLE_MEDIA_AI_RUN.exe\n'+sha(P/'PACKAGE_MANIFEST.json')+'  _payload/PACKAGE_MANIFEST.json\n')
subprocess.run(['zip','-q','-d',str(archive),*[D.name+'/_payload/'+x['path'] for x in removed]],check=True)
changed=['_payload/RUNTIME_ENGINES.json','_payload/MODEL_MANIFEST.json','_payload/PACKAGE_MANIFEST.json','DELIVERY_MANIFEST.json','DELIVERY_ARTIFACT_SHA256.txt']
subprocess.run(['zip','-q','-1',str(archive),*[D.name+'/'+x for x in changed]],cwd=D.parent,check=True)
print('ZIP STAGING CLEANED',len(removed),archive.stat().st_size,flush=True)
with zipfile.ZipFile(archive) as z:
 prefix=D.name+'/_payload/'
 actual={n[len(prefix):] for n in z.namelist() if n.startswith(prefix) and not n.endswith('/') and n!=prefix+'PACKAGE_MANIFEST.json'}
 assert actual=={x['path'] for x in m['files']}
 for x in m['files']:
  h=hashlib.sha256();size=0
  with z.open(prefix+x['path']) as f:
   while b:=f.read(1024*1024):h.update(b);size+=len(b)
  assert size==x['bytes'] and h.hexdigest()==x['sha256'],x['path']
 for name in z.namelist():
  if not name.startswith(prefix):z.read(name)
 assert sha(P/'models/qwen2.5-1.5b-instruct/model.gguf')=='6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
print('ALL ZIP PAYLOAD SHA256 AND CRC PASS',len(m['files']),flush=True)
receipt={'file':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'zip_crc':'PASS_ALL_ENTRIES','zip_manifest_hashes':'PASS_ALL_PAYLOAD_FILES','source':m['build_commit'],'manifest_files_verified':len(m['files']),'base_files_preserved':delivery['base_readback']['manifest_verified_files'],'pruned_copy_staging_files':len(removed),'native_windows_acceptance':'PENDING','full_product_pass':False}
(E/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
