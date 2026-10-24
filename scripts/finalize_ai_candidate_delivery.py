"""Independent artifact readback; repair only exterior stale checksum metadata."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
from build_ai_windows_candidate import NAME,sha,write,record,make_starter

root=Path('final-delivery');root.mkdir(exist_ok=True)
evidence=Path('readback-evidence');evidence.mkdir(exist_ok=True)
source=Path('producer-evidence');receipt=json.loads(next(source.rglob('DELIVERY.json')).read_text(encoding='utf-8-sig'))
assembly=json.loads(next(source.rglob('ASSEMBLY.json')).read_text(encoding='utf-8-sig'))
acceptance=json.loads(next(source.rglob('ACCEPTANCE.json')).read_text(encoding='utf-8-sig'))
assert receipt['source']==assembly['source']==acceptance['source']=='2e5e9197d78c9b975686c1e419d2b68ce5f65226'
assert receipt['sha256']=='b8f16230463e14cfff72e9dd241028a8d47329f98c168097ba2cdb58d07cfee3'
assert acceptance['status']=='REMOTE_WINDOWS_EXE_CHROME_QWEN_NEURAL_TTS_RESTART_EXPORT_PASS'
archive=root/(NAME+'.zip')
with archive.open('wb') as output:
 for item in receipt['parts']:
  part=Path('producer-delivery')/item['path'];assert sha(part)==item['sha256'] and part.stat().st_size==item['bytes']
  with part.open('rb') as stream:
   while b:=stream.read(1024*1024):output.write(b)
assert sha(archive)==receipt['sha256']
with zipfile.ZipFile(archive) as z:
 names=z.namelist();assert len(names)==len(set(names))
 prefix=NAME+'/_payload/'
 manifest_bytes=z.read(prefix+'PACKAGE_MANIFEST.json');assert hashlib.sha256(manifest_bytes).hexdigest()==assembly['manifest_sha256']
 manifest=json.loads(manifest_bytes)
 assert hashlib.sha256(z.read(NAME+'/MINDLE_MEDIA_AI_RUN.exe')).hexdigest()==assembly['exe_sha256']
 for item in manifest['files']:
  h=hashlib.sha256();size=0
  with z.open(prefix+item['path']) as stream:
   while b:=stream.read(1024*1024):h.update(b);size+=len(b)
  assert h.hexdigest()==item['sha256'] and size==item['bytes'],item['path']
 assert not any('/__pycache__/' in n or n.endswith('.pyc') for n in names)
 old=z.read(NAME+'/DELIVERY_ARTIFACT_SHA256.txt')
 new=(assembly['exe_sha256']+'  MINDLE_MEDIA_AI_RUN.exe\n'+assembly['manifest_sha256']+'  _payload/PACKAGE_MANIFEST.json\n').encode('ascii')
 write(evidence/'SOURCE_READBACK.json',{'producer_archive_sha256':receipt['sha256'],'source':receipt['source'],'all_payload_files_checked':len(manifest['files']),'manifest_sha256':assembly['manifest_sha256'],'exe_sha256':assembly['exe_sha256'],'office_pc_acceptance':False,'human_hearing':False})
if old!=new:
 (evidence/'ORIGINAL_EXTERIOR_CHECKSUM.txt').write_bytes(old)
 patchroot=Path('checksum-metadata')/NAME;patchroot.mkdir(parents=True,exist_ok=True)
 (patchroot/'DELIVERY_ARTIFACT_SHA256.txt').write_bytes(new)
 subprocess.run(['zip','-q','-u',str(archive.resolve()),NAME+'/DELIVERY_ARTIFACT_SHA256.txt'],cwd='checksum-metadata',check=True)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))
 assert z.read(NAME+'/DELIVERY_ARTIFACT_SHA256.txt')==new
 assert hashlib.sha256(z.read(prefix+'PACKAGE_MANIFEST.json')).hexdigest()==assembly['manifest_sha256']
 assert hashlib.sha256(z.read(NAME+'/MINDLE_MEDIA_AI_RUN.exe')).hexdigest()==assembly['exe_sha256']
 # Validate all unchanged per-file payload hashes again after exterior metadata update.
 for item in manifest['files']:
  h=hashlib.sha256();size=0
  with z.open(prefix+item['path']) as stream:
   while b:=stream.read(1024*1024):h.update(b);size+=len(b)
  assert h.hexdigest()==item['sha256'] and size==item['bytes'],item['path']
parts=[]
with archive.open('rb') as stream:
 i=0
 while b:=stream.read(500*1024*1024):
  p=root/(archive.name+f'.part-{i:02}');p.write_bytes(b);parts.append(record(root,p));i+=1
h=sha(archive);starter=make_starter(archive,parts,h,assembly['exe_sha256'])
write(evidence/'FINAL_DELIVERY.json',{'name':archive.name,'bytes':archive.stat().st_size,'sha256':h,'parts':parts,'source_archive_sha256':receipt['sha256'],'source':receipt['source'],'manifest_sha256':assembly['manifest_sha256'],'exe_sha256':assembly['exe_sha256'],'exterior_checksum_metadata_corrected':old!=new,'product_payload_changed':False,'post_update_all_payload_hashes':'PASS','zip_crc':'PASS','installer':record(root,starter),'office_pc_acceptance':False,'human_hearing':False,'full_product_pass':False})
print('FINAL_DELIVERY_READBACK_PASS',h,len(parts),flush=True)
