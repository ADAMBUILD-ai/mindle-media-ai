from pathlib import Path
import hashlib,json,zipfile
R=Path.cwd();source=R/'delivery/MINDLE_MEDIA_AI_PC_TEST_20261018_R1.zip';out=R/'delivery/split';out.mkdir(exist_ok=True);base=source.name
expected='715c351a3733aea2ffd87fa0113cc6e554920faabe430c74f941b7b6e5feac8c';whole=hashlib.sha256();rows=[]
with source.open('rb') as src:
 for i in range(7):
  p=out/(base+'.part-%02d'%i);left=500*1024*1024;digest=hashlib.sha256();size=0
  with p.open('wb') as f:
   while left and (b:=src.read(min(left,8*1024*1024))):f.write(b);digest.update(b);whole.update(b);left-=len(b);size+=len(b)
  assert size>0
  rows.append({'name':p.name,'bytes':size,'sha256':digest.hexdigest()});print(p.name,size,flush=True)
 assert src.read(1)==b''
assert whole.hexdigest()==expected
powershell="""$ErrorActionPreference='Stop';try{$p=$env:MINDLE_PARTS_DIR;$names=0..6|ForEach-Object{Join-Path $p ('MINDLE_MEDIA_AI_PC_TEST_20261018_R1.zip.part-{0:D2}' -f $_)};foreach($n in $names){if(!(Test-Path -LiteralPath $n)){throw ('Missing part: '+$n)}};$homeDir=Join-Path $env:LOCALAPPDATA 'MINDLE\\PC_TEST_INSTALLS\\20261018_R1';New-Item -ItemType Directory -Force -Path $homeDir|Out-Null;$z=Join-Path $homeDir 'candidate.zip';$w=[IO.File]::Open($z,[IO.FileMode]::Create,[IO.FileAccess]::Write);try{foreach($n in $names){$s=[IO.File]::OpenRead($n);try{$s.CopyTo($w)}finally{$s.Dispose()}}}finally{$w.Dispose()};if((Get-FileHash -LiteralPath $z -Algorithm SHA256).Hash.ToLower() -ne '715c351a3733aea2ffd87fa0113cc6e554920faabe430c74f941b7b6e5feac8c'){throw 'Archive SHA256 mismatch. Do not run.'};$tar=Join-Path $env:SystemRoot 'System32\\tar.exe';if(!(Test-Path -LiteralPath $tar)){throw 'Windows 10/11 tar.exe is required'};& $tar -xf $z -C $homeDir;if($LASTEXITCODE -ne 0){throw 'Archive extraction failed'};$folder=Join-Path $homeDir 'MINDLE_MEDIA_AI_PC_TEST_20261018_R1';$exe=Join-Path $folder 'MINDLE_MEDIA_AI_RUN.exe';if(!(Test-Path -LiteralPath $exe)){throw 'Launcher missing'};try{$desktop=[Environment]::GetFolderPath('DesktopDirectory');$shell=New-Object -ComObject WScript.Shell;$link=$shell.CreateShortcut((Join-Path $desktop 'MINDLE MEDIA AI TEST R1.lnk'));$link.TargetPath=$exe;$link.WorkingDirectory=$folder;$link.IconLocation=$exe;$link.Save()}catch{Write-Host 'Desktop shortcut could not be created; opening the app directly.'};Start-Process -FilePath $exe -WorkingDirectory $folder;Write-Host 'MINDLE MEDIA AI started. Desktop shortcut: MINDLE MEDIA AI TEST R1.'}catch{Write-Host $_.Exception.Message -ForegroundColor Red;exit 1}"""
assert len(powershell)<6000 and 'ExecutionPolicy' not in powershell and '-Verb' not in powershell
cmd='@echo off\r\nsetlocal\r\nset "MINDLE_PARTS_DIR=%~dp0"\r\nif not exist "%MINDLE_PARTS_DIR%'+base+'.part-00" set "MINDLE_PARTS_DIR=%~dp0.."\r\necho MINDLE MEDIA AI: verify, install and open. Please wait.\r\npowershell.exe -NoProfile -Command "'+powershell+'"\r\nif errorlevel 1 (echo Installation did not complete. Keep this error message.)\r\npause\r\n'
readme='MINDLE MEDIA AI — Windows 64비트 개발 검증 후보\n\n1. 분할 파일 7개(.part-00~06)를 모두 같은 폴더에 다운로드합니다. 파일 이름은 바꾸지 마세요.\n2. 이 설치 ZIP을 압축 해제합니다. 분할 파일이 있는 폴더 또는 바로 아래 폴더에서 START_MINDLE_MEDIA_AI.cmd를 더블클릭하세요.\n3. 자동으로 합치기→SHA256 확인→압축 해제→실행합니다. 바탕화면에 MINDLE MEDIA AI TEST R1 바로가기도 만듭니다. 다음부터 그 바로가기를 더블클릭하세요.\n\nWindows 10/11 64비트·여유 공간 35GB 이상 권장. 별도 Python·pip·Git 설치 명령 입력 없음.\n기존 c37·기존 자료는 변경하지 않습니다. 새 작업 자료는 LOCALAPPDATA\\MINDLE\\MEDIA_AI_CANDIDATE_20261018_R1에 따로 저장합니다.\n승인 UI 최종 일치와 이 후보의 실제 Windows 실행·소리 청취 인수는 미완료인 개발 검증본입니다.\n자동 설치는 사용자 LOCALAPPDATA의 MINDLE\\PC_TEST_INSTALLS\\20261018_R1만 사용합니다. 보안 설정·실행 정책 변경, 관리자 권한 우회, lock 삭제를 하지 않습니다.\n'
manifest={'full_zip':base,'full_zip_bytes':source.stat().st_size,'full_zip_sha256':expected,'parts':rows,'source':'e00e6e0b82994fca628d6ca3cf039f7dc43c15c6','native_windows_acceptance':'PENDING'}
installer=out/'MINDLE_MEDIA_AI_START_20261018_R1.zip'
with zipfile.ZipFile(installer,'w',compression=zipfile.ZIP_DEFLATED) as z:
 z.writestr('START_MINDLE_MEDIA_AI.cmd',cmd.encode('ascii'));z.writestr('INSTALL_README_KO.txt',readme.encode('utf-8-sig'));z.writestr('DELIVERY_PARTS.json',json.dumps(manifest,indent=2));z.writestr('INSTALL_COMMAND_READABLE.txt',powershell)
with zipfile.ZipFile(installer) as z:assert z.testzip() is None;assert z.read('START_MINDLE_MEDIA_AI.cmd').decode('ascii')==cmd
# Independent re-read of parts: prove the installer will reconstruct the verified exact ZIP.
h=hashlib.sha256()
for row in rows:
 p=out/row['name'];d=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(8*1024*1024):h.update(b);d.update(b)
 assert d.hexdigest()==row['sha256']
assert h.hexdigest()==expected
E=R/'product/docs/evidence/windows-oneclick-candidate-20261018-r1';(E/'SPLIT_DELIVERY.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'delivery/upload-request.json').write_text(json.dumps({'uploads':[{'local_path':str(installer),'purpose':'create_library_file','library_artifact_type':'other'},*[{'local_path':str(out/x['name']),'purpose':'create_library_file','library_artifact_type':'other'} for x in rows]]}))
print('SPLIT REASSEMBLY SHA256 PASS; 8 files ready',flush=True)
