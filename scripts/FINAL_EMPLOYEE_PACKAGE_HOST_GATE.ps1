param([string]$PackageRoot = $PSScriptRoot)
$ErrorActionPreference = 'Stop'
$PackageRoot = (Resolve-Path -LiteralPath $PackageRoot).Path
$ExpectedLocal = [Environment]::GetFolderPath('LocalApplicationData')
if ([IO.Path]::GetFullPath($env:LOCALAPPDATA) -ne [IO.Path]::GetFullPath($ExpectedLocal)) { throw '기본 Windows 프로필에서 실행해야 합니다. 임시 프로필은 PASS로 인정하지 않습니다.' }
$InstallRoot = Join-Path $ExpectedLocal 'MINDLE\MEDIA_AI'
$DataRoot = Join-Path $ExpectedLocal 'MINDLE\MEDIA_AI_DATA'
$EvidenceRoot = Join-Path $DataRoot ('host-gates\' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
$DesktopLink = Join-Path ([Environment]::GetFolderPath('Desktop')) 'MINDLE MEDIA AI.lnk'
$MenuLink = Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\MINDLE\MINDLE MEDIA AI.lnk'
$Result = [ordered]@{status='RUNNING';epoch='MEDIA-AI-20261007-EMPLOYEE-PACKAGE-FINAL-CLOSEOUT-R2';default_profile=$true;install_root=$InstallRoot;data_root=$DataRoot;checks=[ordered]@{};offline_full_package_pass=$false;license_gate='OFFLINE_FULL_PACKAGE_LICENSE_GATE_BLOCKED'}
New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null
$ResultPath = Join-Path $EvidenceRoot 'FINAL_HOST_GATE_RESULT.json'
$LogPath = Join-Path $EvidenceRoot 'FINAL_HOST_GATE_LOG.txt'
function Save-Result { $Result | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath $ResultPath -Encoding UTF8 }
function Product-Processes {
  @(Get-Process python,pythonw -ErrorAction SilentlyContinue | Where-Object { $_.Path -in @((Join-Path $InstallRoot 'runtime\python\python.exe'),(Join-Path $InstallRoot 'runtime\python\pythonw.exe')) })
}
function Stop-Product {
  foreach ($Owned in (Product-Processes)) { Stop-Process -Id $Owned.Id -ErrorAction Stop; Wait-Process -Id $Owned.Id -Timeout 30 -ErrorAction SilentlyContinue }
  if ((Product-Processes).Count -ne 0) { throw '제품 프로세스를 완전히 종료하지 못했습니다.' }
}
function Find-Product {
  for ($Port=18768; $Port -lt 18778; $Port++) {
    try {
      $Url='http://127.0.0.1:' + $Port
      $Identity=Invoke-RestMethod -Uri ($Url + '/api/runtime-identity') -TimeoutSec 2
      if ($Identity.install_root -eq $InstallRoot -and $Identity.data_root -eq $DataRoot -and $Identity.runtime_mode -eq 'LOCAL_OFFLINE_PACKAGE') { return @{url=$Url;identity=$Identity} }
    } catch {}
  }
  return $null
}
function Cold-Launch([string]$Label) {
  Stop-Product
  $IdentityBefore = Find-Product
  if ($IdentityBefore) { throw 'cold launch 전에 서버가 남아 있습니다.' }
  $Shell=New-Object -ComObject WScript.Shell
  $Link=$Shell.CreateShortcut($DesktopLink)
  if ($Link.TargetPath -ne (Join-Path $InstallRoot 'runtime\python\pythonw.exe') -or $Link.WorkingDirectory -ne $InstallRoot -or $Link.Arguments -notlike ('*' + $DataRoot + '*')) { throw '바탕화면 바로가기 대상 불일치' }
  # Invoke the actual installed .lnk through Windows Shell, not a direct server command.
  Start-Process -FilePath $DesktopLink
  $Deadline=(Get-Date).AddMinutes(20)
  do {
    Start-Sleep -Seconds 2
    $Found=Find-Product
    if ($Found) { break }
  } while ((Get-Date) -lt $Deadline)
  if (-not $Found) { throw '바탕화면 cold launch 시간 초과. server.log를 확인하세요.' }
  $ServerPids=@(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalAddress -eq '127.0.0.1' -and $_.LocalPort -ge 18768 -and $_.LocalPort -lt 18778 } | Select-Object -ExpandProperty OwningProcess -Unique | Where-Object { (Get-Process -Id $_ -ErrorAction SilentlyContinue).Path -eq (Join-Path $InstallRoot 'runtime\python\pythonw.exe') })
  if ($ServerPids.Count -ne 1) { throw ('제품 서버 수 불일치: ' + $ServerPids.Count) }
  $Result.checks[$Label]=@{status='PASS';method='WINDOWS_SHELL_DESKTOP_LNK';server_count=$ServerPids.Count;identity=$Found.identity}
  Save-Result
  return $Found
}
function Run-InstalledGate([hashtable]$Found,[switch]$Reopen) {
  $Python=Join-Path $InstallRoot 'runtime\python\python.exe'
  $Helper=Join-Path $InstallRoot 'tests\employee_installed_function_gate.py'
  $OutputName=if ($Reopen) {'INSTALLED_REOPEN_TEST.json'} else {'INSTALLED_FUNCTION_TEST.json'}
  $Arguments=@($Helper,'--url',$Found.url,'--package-root',$InstallRoot,'--fixtures',(Join-Path $InstallRoot 'tests\fixtures'),'--output',(Join-Path $EvidenceRoot $OutputName))
  if ($Reopen) { $Arguments += '--reopen' }
  & $Python @Arguments
  if ($LASTEXITCODE -ne 0) { throw ('설치본 기능 시험 실패: ' + $OutputName) }
  $Result.checks[$OutputName]=Get-Content -LiteralPath (Join-Path $EvidenceRoot $OutputName) -Raw | ConvertFrom-Json
  Save-Result
}
function Preserved-Data {
  $Files=@()
  foreach ($Directory in @('inputs','jobs','projects','exports')) {
    $Folder=Join-Path $DataRoot $Directory
    if (Test-Path -LiteralPath $Folder) {
      $Files += @(Get-ChildItem -LiteralPath $Folder -File -Recurse | ForEach-Object { @{path=$_.FullName.Substring($DataRoot.Length+1);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLower()} })
    }
  }
  return $Files
}
Save-Result
Start-Transcript -LiteralPath $LogPath -Force | Out-Null
$PriorBlocked=$env:MINDLE_TEST_BLOCKED_PATHS
try {
  Write-Host '기본 Windows 설치·실행·모델·저장·삭제 후 데이터 보존을 검증합니다.'
  Write-Host '제품 창은 시험 중 여러 번 열립니다. 저장하지 않은 작업을 먼저 저장하세요.'
  if ((Read-Host '시험 실행에 동의하면 TEST를 입력하세요') -cne 'TEST') { $Result.status='USER_CANCELLED'; Save-Result; exit 2 }
  if ($PackageRoot -eq $InstallRoot) { throw '재설치 원본은 설치 폴더와 다른 압축 해제 폴더여야 합니다.' }
  foreach ($Name in @('INSTALL_MINDLE_MEDIA_AI.ps1','tests\employee_installed_function_gate.py','tests\fixtures\FIXTURE_MANIFEST.json')) { if (-not (Test-Path -LiteralPath (Join-Path $PackageRoot $Name))) { throw ('검증 준비 파일 없음: ' + $Name) } }
  $Prerequisites=@('msvcp140.dll','msvcp140_atomic_wait.dll','vcruntime140_threads.dll')
  foreach ($Name in $Prerequisites) { if (-not (Test-Path -LiteralPath (Join-Path $env:SystemRoot ('System32\' + $Name)))) { throw 'Visual C++ 공식 런타임이 필요합니다. 별도 온라인 보조 설치기를 먼저 실행하세요.' } }
  foreach ($Key in @('HF_TOKEN','HUGGING_FACE_HUB_TOKEN','PYTHONPATH','PYTHONHOME')) { [Environment]::SetEnvironmentVariable($Key,$null,'Process') }
  # Only installed code may execute; block source package/repository, user Python and external model caches in launcher/server audit hooks.
  $Blocked=@($PackageRoot,(Join-Path $env:USERPROFILE '.cache\huggingface'),(Join-Path $ExpectedLocal 'Programs\Python'),(Join-Path $env:APPDATA 'Python'),'C:\Users\PC\Documents\Codex\2026-09-30\referenced-chatgpt-conversation-this-is-an-2\work\mindle-media-ai')
  Stop-Product
  & (Join-Path $PackageRoot 'INSTALL_MINDLE_MEDIA_AI.ps1') -PackageRoot $PackageRoot
  if ($LASTEXITCODE -ne 0) { throw '기본 프로필 설치 실패' }
  if (-not (Test-Path -LiteralPath $DesktopLink) -or -not (Test-Path -LiteralPath $MenuLink)) { throw '바탕화면/시작 메뉴 바로가기 누락' }
  $Result.checks.install=@{status='PASS';desktop=$DesktopLink;start_menu=$MenuLink}
  $env:MINDLE_TEST_BLOCKED_PATHS=ConvertTo-Json -InputObject $Blocked -Compress
  $Found=Cold-Launch 'desktop_cold_launch_1'
  Write-Host '제품 창이 열렸는지 확인하고 해당 창을 닫아 주세요.'
  if ((Read-Host '창을 확인하고 닫았으면 YES를 입력하세요') -cne 'YES') { throw '첫 창 확인 미완료' }
  $Found=Cold-Launch 'desktop_cold_launch_2'
  Run-InstalledGate $Found
  # Automated decode is distinct from a human-confirmed rendered UI preview.
  Write-Host '프로젝트를 저장했습니다. 제품 창을 닫아 주세요. 다시 열어 실제 결과 복원을 확인합니다.'
  if ((Read-Host '제품 창을 닫았으면 YES를 입력하세요') -cne 'YES') { throw '창 닫기 미확인' }
  $Found=Cold-Launch 'desktop_saved_project_reopen'
  Run-InstalledGate $Found -Reopen
  Write-Host '제품 창에서 저장된 VIDEO/PHOTO 결과와 한국어 자막이 나타나는지 확인하세요.'
  Write-Host 'VIDEO 재생과 PHOTO 결과 표시를 확인한 후 창을 닫으세요.'
  if ((Read-Host '결과 복원과 VIDEO 재생을 직접 확인했다면 YES를 입력하세요') -cne 'YES') { throw 'UI 복원/재생 확인 실패' }
  $Result.checks.ui_rendered_preview=@{status='PASS_USER_OBSERVED';method='USER_CONFIRMATION_AFTER_INSTALLED_SERVER_RESTART'}
  $Before=@(Preserved-Data)
  if ($Before.Count -lt 17) { throw '보존 검증 파일 수가 17개 미만입니다.' }
  $Before | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $EvidenceRoot 'DATA_BEFORE_UNINSTALL.json') -Encoding UTF8
  Stop-Product
  $env:MINDLE_TEST_BLOCKED_PATHS=$null
  & (Join-Path $InstallRoot 'uninstall\UNINSTALL_MINDLE_MEDIA_AI.ps1')
  if (Test-Path -LiteralPath $InstallRoot) { throw '앱 제거 실패' }
  foreach ($LinkPath in @($DesktopLink,$MenuLink)) { if (Test-Path -LiteralPath $LinkPath) { throw '제거 후 바로가기 잔존' } }
  foreach ($File in $Before) { $Path=Join-Path $DataRoot $File.path; if (-not (Test-Path -LiteralPath $Path) -or (Get-FileHash -LiteralPath $Path).Hash.ToLower() -ne $File.sha256) { throw ('제거 중 데이터 변경: ' + $File.path) } }
  & (Join-Path $PackageRoot 'INSTALL_MINDLE_MEDIA_AI.ps1') -PackageRoot $PackageRoot
  if ($LASTEXITCODE -ne 0) { throw '재설치 실패' }
  foreach ($File in $Before) { $Path=Join-Path $DataRoot $File.path; if (-not (Test-Path -LiteralPath $Path) -or (Get-FileHash -LiteralPath $Path).Hash.ToLower() -ne $File.sha256) { throw ('재설치 후 데이터 변경: ' + $File.path) } }
  $Result.checks.uninstall_reinstall=@{status='PASS';preserved_files=$Before.Count;application_removed=$true;shortcuts_removed=$true;data_hashes_unchanged=$true}
  $Result.checks.dependency_guards=@{status='PASS_INSTALLED_RUNTIME_STARTUP_NEGATIVE_CONTROLS';blocked_paths=$Blocked;non_loopback_network='DENIED_BY_PYTHON_AUDIT_HOOK';external_msvc='KNOWN_ONLINE_PREREQUISITE';full_native_dependency_audit='SEPARATE_RELEASE_GATE_REQUIRED'}
  $Result.status='DEFAULT_PROFILE_HOST_GATE_PASS'
} catch { $Result.status='DEFAULT_PROFILE_HOST_GATE_FAILED'; $Result.error=$_.Exception.Message; Write-Host $Result.error -ForegroundColor Red }
finally {
  $env:MINDLE_TEST_BLOCKED_PATHS=$PriorBlocked
  Save-Result
  Stop-Transcript | Out-Null
  Write-Host ('검증 결과: ' + $Result.status)
  Write-Host ('결과 폴더: ' + $EvidenceRoot)
}
if ($Result.status -ne 'DEFAULT_PROFILE_HOST_GATE_PASS') { exit 1 }
exit 0
