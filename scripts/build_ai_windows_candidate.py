"""One owner-authorized development candidate, sealed from frozen Windows inputs."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, urllib.request, zipfile
from pathlib import Path, PurePosixPath

NAME='MINDLE_MEDIA_AI_PC_TEST_20261024_R1'
BASE_SHA='5291760966d87089259de4d1030879fdf0a1a878d7b9f1fd12f7918f36656b30'
BASE_MANIFEST='7a31da30969b9e7901da8f109c467f281e2550171c15e9ddf3a8ddf215ab3377'
QWEN_SHA='6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
QWEN_REV='91cad51170dc346986eccefdc2dd33a9da36ead9'
TTS_SHA='82fa96f91c4ef8abaae3a14a3f4153facf88bed821d1f7331cec2700f432c427'
LLAMA_SHA='79b143075ab87fb5aff6f8f8ca80500a984f4120b5199fa9f9b70b284f17428e'

def sha(p):
    with Path(p).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stable(p):return '__pycache__' not in p.parts and p.suffix.lower() not in {'.pyc','.pyo'} and not any(x.startswith('.') and x!='.f2py_f2cmap' for x in p.parts)
def files(root):return sorted((p for p in root.rglob('*') if p.is_file() and stable(p.relative_to(root))),key=lambda p:p.relative_to(root).as_posix())
def tree_sha(root):return hashlib.sha256('\n'.join(p.relative_to(root).as_posix()+':'+sha(p) for p in files(root)).encode()).hexdigest()
def record(root,p):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def download(url,p,expected=None):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with urllib.request.urlopen(url,timeout=60) as response,p.open('wb') as target:shutil.copyfileobj(response,target,1024*1024)
    digest=sha(p)
    if expected and digest!=expected:raise RuntimeError('download SHA mismatch: '+p.name)
    print('ACQUIRED',p.name,p.stat().st_size,digest,flush=True)
    return {'url':url,'bytes':p.stat().st_size,'sha256':digest}
def safe_name(name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:raise ValueError('unsafe archive member')
    return p

def base_extract(parts,output,evidence):
    chunks=sorted(Path(parts).glob('*.zip.part-*'))
    if len(chunks)!=5 or [x.name.rsplit('-',1)[1] for x in chunks]!=['00','01','02','03','04']:raise RuntimeError('exact five c37 parts required')
    archive=Path(parts)/'verified-c37.zip'
    with archive.open('wb') as out:
        for p in chunks:
            with p.open('rb') as stream:shutil.copyfileobj(stream,out,1024*1024)
    if sha(archive)!=BASE_SHA:raise RuntimeError('c37 archive identity mismatch')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();manifests=[n for n in names if n.endswith('/_payload/PACKAGE_MANIFEST.json')]
        if len(manifests)!=1:raise RuntimeError('base manifest ambiguous')
        manifest_bytes=z.read(manifests[0])
        if hashlib.sha256(manifest_bytes).hexdigest()!=BASE_MANIFEST:raise RuntimeError('base manifest mismatch')
        old=json.loads(manifest_bytes);prefix=manifests[0].removesuffix('PACKAGE_MANIFEST.json')
        # Streaming reads independently check CRC, bytes and every old manifest SHA.
        for item in old['files']:
            h=hashlib.sha256();length=0
            with z.open(prefix+item['path']) as stream:
                while data:=stream.read(1024*1024):h.update(data);length+=len(data)
            if length!=item['bytes'] or h.hexdigest()!=item['sha256']:raise RuntimeError('base file mismatch: '+item['path'])
        base_root=prefix.split('/')[0]
        for item in z.infolist():
            safe_name(item.filename)
            relative=PurePosixPath(item.filename).relative_to(base_root)
            if item.is_dir():continue
            target=output/Path(relative)
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(item) as stream,target.open('wb') as out:shutil.copyfileobj(stream,out,1024*1024)
    write(evidence/'BASE_READBACK.json',{'source':'c37c7819b1454996f3510f92184b1ef62faf3c78','archive_sha256':BASE_SHA,'manifest_sha256':BASE_MANIFEST,'verified_files':len(old['files']),'zip_crc':'PASS_MANIFEST_ENTRIES_AND_EXTRACTED_MEMBERS'})
    archive.unlink()
    for p in chunks:p.unlink() # Only disposable runner inputs; no user's installation.
    return old

def assemble(args):
    output=Path(args.output);evidence=Path(args.evidence);repo=Path(args.repo)
    if output.exists():raise RuntimeError('fresh output required')
    output.mkdir(parents=True);old=base_extract(args.parts,output,evidence);payload=output/'_payload'
    for folder in ('src','ui'):
        shutil.rmtree(payload/'app'/folder)
        shutil.copytree(repo/folder,payload/'app'/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
    shutil.copy2(repo/'scripts/employee_package_launcher.py',payload/'app/launcher/employee_package_launcher.py')
    shutil.copy2(args.exe,output/'MINDLE_MEDIA_AI_RUN.exe')
    receipts=[];downloads=output.parent/'acquired';downloads.mkdir(exist_ok=True)
    llama=downloads/'llama.zip'
    receipts.append(download('https://github.com/ggml-org/llama.cpp/releases/download/b11716/llama-b11716-bin-win-cpu-x64.zip',llama,LLAMA_SHA))
    with zipfile.ZipFile(llama) as z:
        for n in z.namelist():safe_name(n)
        z.extractall(payload/'tools/llama')
    exe=next((payload/'tools/llama').rglob('llama-completion.exe'))
    model=payload/'models/qwen2.5-1.5b-instruct/model.gguf'
    receipts.append(download('https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/'+QWEN_REV+'/qwen2.5-1.5b-instruct-q4_k_m.gguf',model,QWEN_SHA))
    for name in ('LICENSE','README.md'):receipts.append(download('https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/'+QWEN_REV+'/'+name,model.parent/name))
    archive=downloads/'supertonic.tar.bz2'
    receipts.append(download('https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2',archive,TTS_SHA))
    import tarfile
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            safe_name(m.name)
            if not (m.isfile() or m.isdir()):raise RuntimeError('nonregular neural asset')
        t.extractall(downloads/'tts',filter='data')
    tts=payload/'models/supertonic3';shutil.copytree(next((downloads/'tts').iterdir()),tts)
    receipts.append(download('https://huggingface.co/Supertone/supertonic-3/resolve/3cadd1ee6394adea1bd021217a0e650ede09a323/LICENSE',tts/'MODEL_LICENSE_OpenRAIL-M.txt'))
    site=payload/'runtime/site-packages'
    subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--no-compile','--no-deps','--upgrade','--target',str(site),'sherpa-onnx==1.13.8','sherpa-onnx-core==1.13.8'],check=True)
    removed=[]
    for p in sorted(payload.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_file() and not stable(p.relative_to(payload)):
            removed.append(p.relative_to(payload).as_posix());p.unlink()
        elif p.is_dir() and p.name=='__pycache__':shutil.rmtree(p)
    settings={'planner':{'executable':exe.relative_to(payload).as_posix(),'executable_sha256':sha(exe),'runtime_sha256':tree_sha(exe.parent),'model_path':model.relative_to(payload).as_posix(),'model_sha256':QWEN_SHA,'revision':QWEN_REV,'model_id':'Qwen/Qwen2.5-1.5B-Instruct-GGUF','license':'Apache-2.0'},'tts':{'engine':'sherpa-supertonic','data_path':tts.relative_to(payload).as_posix(),'data_sha256':tree_sha(tts),'runtime_version':'1.13.8','runtime_sha256':tree_sha(site/'sherpa_onnx/lib'),'model_revision':'3cadd1ee6394adea1bd021217a0e650ede09a323','archive_sha256':TTS_SHA,'license':'OpenRAIL-M (model); MIT (upstream code)'}}
    write(payload/'RUNTIME_ENGINES.json',settings)
    write(payload/'MODEL_MANIFEST.json',[record(payload,p) for folder in ('models','omz') for p in files(payload/folder)])
    write(payload/'LICENSES/LOCAL_ENGINE_LICENSES.json',{'Qwen':'Apache-2.0; models/qwen2.5-1.5b-instruct/LICENSE','Supertonic':'OpenRAIL-M model; models/supertonic3/MODEL_LICENSE_OpenRAIL-M.txt','sherpa-onnx':'Apache-2.0; bundled wheel notices','llama.cpp':'MIT; bundled upstream notices'})
    ui=payload/'app/ui';fingerprint=tree_sha(ui)
    manifest={**old,'build_commit':os.environ['GITHUB_SHA'],'runtime_id':os.environ['GITHUB_SHA'][:12]+'-'+fingerprint[:12]+'-ai-r2','ui_fingerprint':fingerprint,'data_directory_name':'MEDIA_AI_CANDIDATE_20261024_R1','release_channel':'OWNER_DEVELOPMENT_VERIFICATION_NOT_FINAL_RELEASE','package_version':'AI_WINDOWS_20261024_R1','model_manifest_hash':sha(payload/'MODEL_MANIFEST.json'),'approved_ui_exact_match':False,'native_windows_acceptance':'PENDING'}
    manifest['files']=[record(payload,p) for p in files(payload) if p!=payload/'PACKAGE_MANIFEST.json']
    write(payload/'PACKAGE_MANIFEST.json',manifest)
    write(output/'DELIVERY_MANIFEST.json',{'source':os.environ['GITHUB_SHA'],'base_source':'c37c7819b1454996f3510f92184b1ef62faf3c78','runtime_id':manifest['runtime_id'],'exe_sha256':sha(output/'MINDLE_MEDIA_AI_RUN.exe'),'manifest_sha256':sha(payload/'PACKAGE_MANIFEST.json'),'files':len(manifest['files']),'office_pc_acceptance':False,'human_hearing':False,'full_product_pass':False})
    (output/'DELIVERY_ARTIFACT_SHA256.txt').write_text(sha(output/'MINDLE_MEDIA_AI_RUN.exe')+'  MINDLE_MEDIA_AI_RUN.exe\n'+sha(payload/'PACKAGE_MANIFEST.json')+'  _payload/PACKAGE_MANIFEST.json\n',encoding='ascii')
    write(evidence/'ASSEMBLY.json',json.loads((output/'DELIVERY_MANIFEST.json').read_text()))
    write(evidence/'ACQUISITIONS.json',receipts);write(evidence/'EXCLUDED_CACHES.json',removed)
    shutil.rmtree(downloads)
    print('ASSEMBLED',output,flush=True)

def seal(args):
    output=Path(args.output);payload=output/'_payload';evidence=Path(args.evidence)
    manifest=json.loads((payload/'PACKAGE_MANIFEST.json').read_text())
    for item in manifest['files']:
        p=payload/item['path']
        if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:raise RuntimeError('post-runtime payload changed: '+item['path'])
    if any(p.is_file() and ('__pycache__' in p.parts or p.suffix=='.pyc') for p in payload.rglob('*')):raise RuntimeError('runtime wrote bytecode into sealed payload')
    archive=output.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
        for p in files(output):z.write(p,output.name+'/'+p.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
    digest=sha(archive);parts=[]
    with archive.open('rb') as f:
        index=0
        while b:=f.read(500*1024*1024):
            p=archive.with_name(archive.name+f'.part-{index:02}');p.write_bytes(b);parts.append(record(archive.parent,p));index+=1
    write(evidence/'DELIVERY.json',{'name':archive.name,'bytes':archive.stat().st_size,'sha256':digest,'parts':parts,'payload_files':len(manifest['files']),'post_runtime_hashes':'PASS','zip_crc':'PASS','source':manifest['build_commit'],'office_pc_acceptance':False,'human_hearing':False})
    starter=make_starter(archive,parts,digest,sha(output/'MINDLE_MEDIA_AI_RUN.exe'))
    write(evidence/'INSTALLER.json',record(archive.parent,starter))
    print('SEALED',digest,flush=True)

def make_starter(archive,parts,digest,exe_sha):
    starter=archive.parent/'MINDLE_MEDIA_AI_START_20261024_R1.zip'
    ps=r"""$ErrorActionPreference='Stop'
$parts=Get-ChildItem -LiteralPath $env:MINDLE_PARTS_DIR -Filter 'MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-*' | Sort-Object Name
if($parts.Count -ne PART_COUNT){throw 'Missing candidate parts'}
$homeDir=Join-Path $env:LOCALAPPDATA 'MINDLE\PC_TEST_INSTALLS\20261024_R1'
New-Item -ItemType Directory -Force -Path $homeDir | Out-Null
$archive=Join-Path $homeDir 'candidate.zip'
$out=[IO.File]::Create($archive)
try {foreach($p in $parts){$input=[IO.File]::OpenRead($p.FullName);try{$input.CopyTo($out)}finally{$input.Dispose()}}}finally{$out.Dispose()}
if((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne 'ARCHIVE_SHA'){throw 'Candidate archive SHA mismatch'}
& "$env:SystemRoot\System32\tar.exe" -xf $archive -C $homeDir
if($LASTEXITCODE -ne 0){throw 'Extraction failed'}
$folder=Join-Path $homeDir 'MINDLE_MEDIA_AI_PC_TEST_20261024_R1'
$exe=Join-Path $folder 'MINDLE_MEDIA_AI_RUN.exe'
if((Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLower() -ne 'EXE_SHA'){throw 'Candidate EXE SHA mismatch'}
$shell=New-Object -ComObject WScript.Shell
$link=$shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'MINDLE MEDIA AI TEST R2.lnk'))
$link.TargetPath=$exe;$link.WorkingDirectory=$folder;$link.IconLocation=$exe;$link.Save()
Start-Process -FilePath $exe -WorkingDirectory $folder
""".replace('PART_COUNT',str(len(parts))).replace('ARCHIVE_SHA',digest).replace('EXE_SHA',exe_sha)
    cmd='@echo off\r\nsetlocal\r\nset "MINDLE_INSTALLER_DIR=%~dp0"\r\nset "MINDLE_PARTS_DIR=%~dp0"\r\nif not exist "%MINDLE_PARTS_DIR%MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-00" set "MINDLE_PARTS_DIR=%~dp0.."\r\npowershell.exe -NoProfile -Command "& ([ScriptBlock]::Create([IO.File]::ReadAllText((Join-Path $env:MINDLE_INSTALLER_DIR \'INSTALL_COMMAND.txt\'))))"\r\nif errorlevel 1 echo Installation failed. Keep this window for PC Work.\r\npause\r\n'
    with zipfile.ZipFile(starter,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('START_MINDLE_MEDIA_AI.cmd',cmd.encode('ascii'))
        z.writestr('INSTALL_COMMAND.txt',ps.encode('utf-8-sig'))
        z.writestr('DELIVERY_PARTS.json',json.dumps({'sha256':digest,'parts':parts},indent=2))
        z.writestr('README_KO.txt','모든 part 파일과 이 ZIP을 같은 폴더에 두고, 이 ZIP만 압축 해제한 뒤 START_MINDLE_MEDIA_AI.cmd를 두 번 클릭하세요. 기존 TEST R1·자료는 보존됩니다. 새 바탕화면 TEST R2로 실행합니다. 원격 Windows 검수는 사무실 PC 인수·사람 청취·승인 UI 전체 일치와 다릅니다. 기존 프로젝트를 자동 이전하지 않습니다.')
    return starter

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['assemble','seal']);p.add_argument('--output',default='build/'+NAME);p.add_argument('--evidence',default='evidence-new');p.add_argument('--repo',default='.');p.add_argument('--parts',default='build/base-parts');p.add_argument('--exe',default='dist/MINDLE_MEDIA_AI_RUN.exe');args=p.parse_args()
    (assemble if args.action=='assemble' else seal)(args)
