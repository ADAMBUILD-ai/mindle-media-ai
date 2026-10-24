"""Export stable package files; never include host rsync/copy staging namespaces."""
from pathlib import Path
import re,json,hashlib,subprocess,zipfile
R=Path.cwd();D=R/'delivery/MINDLE_MEDIA_AI_PC_TEST_20261018_R1';P=D/'_payload';E=R/'product/docs/evidence/windows-oneclick-candidate-20261018-r1';archive=D.with_suffix('.zip')
def stable(relative):
 parts=Path(relative).parts
 return not any(part.startswith('.') and part!='.f2py_f2cmap' for part in parts)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def selected(root):return [p for p in sorted(root.rglob('*'),key=lambda p:p.relative_to(root).as_posix()) if stable(p.relative_to(root)) and p.is_file()]
def tree(root):return hashlib.sha256('\n'.join(p.relative_to(root).as_posix()+':'+sha(p) for p in selected(root)).encode()).hexdigest()
def write(p,v):
 if p.exists():p.unlink()
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
excluded=[p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and not stable(p.relative_to(P))]
(E/'EXCLUDED_HOST_SYNC_FILES.json').write_text(json.dumps({'files':excluded,'rule':'No hidden copy/rsync namespaces; preserve legitimate numpy .f2py_f2cmap. No core model/algorithm changed.'},indent=2)+'\n')
s=json.loads((P/'RUNTIME_ENGINES.json').read_text());s['planner']['runtime_sha256']=tree((P/s['planner']['executable']).parent);s['tts']['runtime_sha256']=tree(P/'runtime/site-packages/sherpa_onnx/lib');s['tts']['data_sha256']=tree(P/s['tts']['data_path']);write(P/'RUNTIME_ENGINES.json',s)
models=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for top in ['models','omz'] for p in selected(P/top)];write(P/'MODEL_MANIFEST.json',models)
m=json.loads((P/'PACKAGE_MANIFEST.json').read_text());m['model_manifest_hash']=sha(P/'MODEL_MANIFEST.json');m['files']=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in selected(P) if p!=P/'PACKAGE_MANIFEST.json'];write(P/'PACKAGE_MANIFEST.json',m)
d=json.loads((D/'DELIVERY_MANIFEST.json').read_text());d.update(files=len(m['files']),package_manifest_sha256=sha(P/'PACKAGE_MANIFEST.json'),engine_manifest=s,host_sync_staging_excluded=True);write(D/'DELIVERY_MANIFEST.json',d);(E/'ASSEMBLY.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=D/'DELIVERY_ARTIFACT_SHA256.txt';p.unlink();p.write_text(sha(D/'MINDLE_MEDIA_AI_RUN.exe')+'  MINDLE_MEDIA_AI_RUN.exe\n'+sha(P/'PACKAGE_MANIFEST.json')+'  _payload/PACKAGE_MANIFEST.json\n')
prefix=D.name+'/_payload/'
with zipfile.ZipFile(archive) as z:bad=[n for n in z.namelist() if n.startswith(prefix) and not stable(n[len(prefix):])]
if bad:subprocess.run(['zip','-q','-d',str(archive),*bad],check=True)
changed=['_payload/RUNTIME_ENGINES.json','_payload/MODEL_MANIFEST.json','_payload/PACKAGE_MANIFEST.json','DELIVERY_MANIFEST.json','DELIVERY_ARTIFACT_SHA256.txt']
subprocess.run(['zip','-q','-1',str(archive),*[D.name+'/'+x for x in changed]],cwd=D.parent,check=True)
print('STABLE ZIP WRITTEN',archive.stat().st_size,flush=True)
with zipfile.ZipFile(archive) as z:
 actual={n[len(prefix):] for n in z.namelist() if n.startswith(prefix) and not n.endswith('/') and n!=prefix+'PACKAGE_MANIFEST.json'}
 assert actual=={x['path'] for x in m['files']},(actual-{x['path'] for x in m['files']},{x['path'] for x in m['files']}-actual)
 for x in m['files']:
  h=hashlib.sha256();size=0
  with z.open(prefix+x['path']) as f:
   while b:=f.read(1024*1024):h.update(b);size+=len(b)
  assert size==x['bytes'] and h.hexdigest()==x['sha256'],x['path']
 for n in z.namelist():
  if not n.startswith(prefix):z.read(n)
 assert json.loads(z.read(prefix+'PACKAGE_MANIFEST.json'))==m
 # Validate tree pins from exactly the archived files, independently of host temp paths.
 for folder,expected in [((P/s['planner']['executable']).parent,s['planner']['runtime_sha256']),(P/s['tts']['data_path'],s['tts']['data_sha256']),(P/'runtime/site-packages/sherpa_onnx/lib',s['tts']['runtime_sha256'])]:
  rel=folder.relative_to(P).as_posix()+'/'
  rows=sorted((x['path'][len(rel):]+':'+x['sha256'] for x in m['files'] if x['path'].startswith(rel)))
  assert hashlib.sha256('\n'.join(rows).encode()).hexdigest()==expected
print('ZIP ALL PAYLOAD SHA256 CRC AND ENGINE TREE PINS PASS',len(m['files']),flush=True)
receipt={'file':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'zip_crc':'PASS_ALL_ENTRIES','zip_manifest_hashes':'PASS_ALL_PAYLOAD_FILES','engine_tree_pins':'PASS_ARCHIVE_CONTENTS','source':m['build_commit'],'manifest_files_verified':len(m['files']),'base_files_preserved':d['base_readback']['manifest_verified_files'],'native_windows_acceptance':'PENDING','full_product_pass':False}
(E/'DELIVERY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
