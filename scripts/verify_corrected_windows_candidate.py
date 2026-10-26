"""Read-only independent byte verification of the corrected Windows candidate."""
import hashlib,json,os,zipfile
from pathlib import Path,PurePosixPath
root=Path(__file__).resolve().parents[1]
parts_root=root/'candidate_readback/parts';metadata=root/'candidate_readback/metadata';out=root/'candidate_readback/evidence';out.mkdir(parents=True,exist_ok=True)
record=json.loads(next(metadata.rglob('DELIVERY_PARTS.json')).read_text(encoding='utf-8-sig'))
name=record['zip'];assert PurePosixPath(name).name==name and name.endswith('.zip')
parts=sorted(parts_root.rglob(name+'.part-*'));assert len(parts)==record['parts']
for i,p in enumerate(parts):assert p.name==name+f'.part-{i:02d}'
archive=root/'candidate_readback'/name
digest=hashlib.sha256()
with archive.open('wb') as target:
    for part in parts:
        with part.open('rb') as source:
            for block in iter(lambda:source.read(1024*1024),b''):target.write(block);digest.update(block)
assert digest.hexdigest()==record['sha256'],'delivery ZIP hash mismatch'
prefix=name[:-4]+'/'
def hash_entry(z,name):
    h=hashlib.sha256();count=0
    with z.open(name) as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block);count+=len(block)
    return h.hexdigest(),count
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None,'CRC failure'
    for item in z.namelist():
        assert '..' not in PurePosixPath(item).parts and not item.startswith('/'),'unsafe archive path'
    delivery=json.loads(z.read(prefix+'DELIVERY_MANIFEST.json'))
    manifest_bytes=z.read(prefix+'_payload/PACKAGE_MANIFEST.json')
    manifest=json.loads(manifest_bytes)
    assert delivery['build_commit']==manifest['build_commit']=='0e4e12a9e4c758f202c6ebb5085df5a542bb6314'
    assert hashlib.sha256(manifest_bytes).hexdigest()==delivery['payload_manifest']['sha256']
    actual,size=hash_entry(z,prefix+delivery['launcher']['path'])
    assert actual==delivery['launcher']['sha256'] and size==delivery['launcher']['bytes']
    checked=0
    for item in manifest['files']:
        path=item['path'];assert '..' not in PurePosixPath(path).parts and not path.startswith('/')
        actual,size=hash_entry(z,prefix+'_payload/'+path)
        assert actual==item['sha256'] and size==item['bytes'],path
        assert 'ci-test-only-ffmpeg' not in path
        checked+=1
    result={'status':'PASS_WINDOWS_CANDIDATE_ZIP_CRC_AND_ALL_MANIFEST_BYTES','source_commit':manifest['build_commit'],'producer_run':38497304486,'verifier_source':os.environ['GITHUB_SHA'],'zip_name':name,'zip_sha256':digest.hexdigest(),'zip_bytes':archive.stat().st_size,'parts':len(parts),'crc':'PASS','payload_files_checked':checked,'payload_manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),'launcher_sha256':delivery['launcher']['sha256'],'runtime_id':manifest['runtime_id'],'ui_fingerprint':manifest['ui_fingerprint'],'office_pc_pass':False,'full_product_pass':False,'scope':'CORRECTED_DEVELOPMENT_CANDIDATE_ONLY_NOT_FINAL_EMPLOYEE_RELEASE'}
(out/'INDEPENDENT_CANDIDATE_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
