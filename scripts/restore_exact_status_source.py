"""Restore the monitored source bytes on an ephemeral Actions runner only.

Git archive bypasses checkout CRLF filters/stat caching. Never adjusts expected
hashes, product state, installed models or a user's local working tree.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PATHS=('src','ui','docs/evidence/media-ai-core-e2e-r2-20261025/SOURCE_VALIDATION.json',
       'docs/evidence/media-ai-core-e2e-r1-20261025/SOURCE_BINDING.json',
       'docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json')


def restore(root,paths=PATHS):
    root=Path(root).resolve()
    archive=subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.eol=lf','archive','--format=zip','HEAD','--',*paths],cwd=root)
    tree=subprocess.check_output(['git','ls-tree','-r','-z','HEAD','--',*paths],cwd=root)
    expected_blobs={}
    for row in tree.split(b'\0'):
        if not row:continue
        entry,name=row.split(b'\t',1);mode,kind,blob=entry.decode('ascii').split()
        if kind=='blob':
            if mode not in ('100644','100755'):raise ValueError('UNSUPPORTED_MONITORED_GIT_MODE')
            expected_blobs[name.decode('utf-8')]=blob
    records=[]
    with zipfile.ZipFile(io.BytesIO(archive)) as package:
        if package.testzip() is not None:raise ValueError('EXACT_SOURCE_ARCHIVE_CRC_FAILED')
        for info in package.infolist():
            target=(root/info.filename).resolve()
            if not target.is_relative_to(root):raise ValueError('EXACT_SOURCE_PATH_OUTSIDE_CHECKOUT')
            if info.is_dir():target.mkdir(parents=True,exist_ok=True);continue
            raw=package.read(info.filename)
            git_sha=hashlib.sha1(b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw).hexdigest()
            if git_sha!=expected_blobs.get(info.filename):raise ValueError('ARCHIVE_NOT_EXACT_GIT_BLOB: '+info.filename)
            before=target.read_bytes() if target.is_file() else None
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            expected=hashlib.sha256(raw).hexdigest();actual=hashlib.sha256(target.read_bytes()).hexdigest()
            if actual!=expected:raise ValueError('EXACT_SOURCE_RESTORE_FAILED: '+info.filename)
            records.append({'path':info.filename,'bytes':len(raw),'sha256':actual,'git_blob_sha':git_sha,'changed_working_bytes':before!=raw})
    return {'status':'PASS_EXACT_GIT_SOURCE_BYTES','source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,encoding='utf-8').strip(),
            'archive_sha256':hashlib.sha256(archive).hexdigest(),'files':records,'expected_hashes_modified':False,'models_modified':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    if os.environ.get('GITHUB_ACTIONS')!='true':raise SystemExit('EPHEMERAL_RUNNER_ONLY_REFUSE_LOCAL_OVERWRITE')
    value=restore(ROOT);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(value['status'],len(value['files']))


if __name__=='__main__':main()
