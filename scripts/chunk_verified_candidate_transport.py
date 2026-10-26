"""Bounded transport of the already accepted candidate; no rebuild or inference."""
import hashlib,json
from pathlib import Path
root=Path('transport');root.mkdir(exist_ok=True)
receipt=json.loads(next(Path('verified-metadata').rglob('FINAL_DELIVERY.json')).read_text())
assert receipt['sha256']=='c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606'
chunks=[];whole=hashlib.sha256();index=0;size=0;out=None
for item in receipt['parts']:
 p=Path('verified-parts')/item['path'];part_hash=hashlib.sha256();part_size=0
 with p.open('rb') as stream:
  while b:=stream.read(1024*1024):
   whole.update(b);part_hash.update(b);part_size+=len(b)
   if out is None:target=root/f'transfer-{index:02}.bin';out=target.open('wb');size=0
   out.write(b);size+=len(b)
   if size==64*1024*1024:
    out.close();out=None
    with target.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    chunks.append({'name':target.name,'bytes':size,'sha256':digest});index+=1
 assert part_hash.hexdigest()==item['sha256'] and part_size==item['bytes']
if out:
 out.close()
 with target.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 chunks.append({'name':target.name,'bytes':size,'sha256':digest})
assert whole.hexdigest()==receipt['sha256']
(root/'TRANSPORT.json').write_text(json.dumps({'final_delivery':receipt,'chunks':chunks},indent=2)+'\n')
print('BYTE_IDENTICAL_TRANSPORT',whole.hexdigest(),len(chunks),flush=True)
