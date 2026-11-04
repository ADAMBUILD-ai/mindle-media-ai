from pathlib import Path
import json,hashlib
b=Path(__file__).resolve().parent;m=json.loads((b/'REMOTE_DELIVERY.json').read_text(encoding='utf-8'))
for z in m['split_zips']:
 p=b/z['original_path'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  assert p.stat().st_size==z['original_bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==z['original_sha256'];continue
 data=b''.join((b/n).read_bytes() for n in z['parts'])
 assert len(data)==z['original_bytes'] and hashlib.sha256(data).hexdigest()==z['original_sha256']
 p.write_bytes(data);print('RECONSTRUCTED_SHA256_PASS',z['original_path'],z['original_sha256'])
