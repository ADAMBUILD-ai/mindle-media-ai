param([string]$PackageRoot = $PSScriptRoot,[string]$ShortcutRoot)
$ErrorActionPreference = 'Stop'
try {
  $PackageRoot = (Resolve-Path -LiteralPath $PackageRoot).Path
  $InstallRoot = Join-Path $env:LOCALAPPDATA 'MINDLE\MEDIA_AI'
  $DataRoot = Join-Path $env:LOCALAPPDATA 'MINDLE\MEDIA_AI_DATA'
  $Python = Join-Path $PackageRoot 'runtime\python\python.exe'
  & $Python (Join-Path $PackageRoot 'app\launcher\employee_package_launcher.py') --verify-only
  if ($LASTEXITCODE -ne 0) { throw '패키지 검증 실패. 설치를 중단합니다.' }
  New-Item -ItemType Directory -Force -Path $InstallRoot,(Join-Path $DataRoot 'logs') | Out-Null
  if ($PackageRoot -ne $InstallRoot) {
    & robocopy $PackageRoot $InstallRoot /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP
    if ($LASTEXITCODE -ge 8) { throw '설치 파일 복사 실패' }
  }
  & (Join-Path $InstallRoot 'runtime\python\python.exe') (Join-Path $InstallRoot 'app\launcher\employee_package_launcher.py') --verify-only
  if ($LASTEXITCODE -ne 0) { throw '설치된 파일 검증 실패' }
  $Shell = New-Object -ComObject WScript.Shell
  $Desktop = [Environment]::GetFolderPath('Desktop')
  $Menu = Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\MINDLE'
  if ($ShortcutRoot) {
    $Desktop = Join-Path $ShortcutRoot 'Desktop'
    $Menu = Join-Path $ShortcutRoot 'StartMenu\Programs\MINDLE'
    New-Item -ItemType Directory -Force -Path $Desktop | Out-Null
  }
  New-Item -ItemType Directory -Force -Path $Menu | Out-Null
  foreach ($Link in @((Join-Path $Desktop 'MINDLE MEDIA AI.lnk'),(Join-Path $Menu 'MINDLE MEDIA AI.lnk'))) {
    $Shortcut = $Shell.CreateShortcut($Link)
    $Shortcut.TargetPath = Join-Path $InstallRoot 'runtime\python\pythonw.exe'
    $Shortcut.Arguments = '"' + (Join-Path $InstallRoot 'app\launcher\employee_package_launcher.py') + '" --data-root "' + $DataRoot + '"'
    $Shortcut.WorkingDirectory = $InstallRoot
    $Shortcut.IconLocation = (Join-Path $InstallRoot 'assets\brand\MINDLE_MEDIA_AI_APP_ICON.ico') + ',0'
    $Shortcut.Save()
  }
  $Manifest = Get-Content -Raw -LiteralPath (Join-Path $InstallRoot 'PACKAGE_MANIFEST.json') | ConvertFrom-Json
  @{package_version=$Manifest.package_version; installed_at=(Get-Date).ToString('o'); manifest_sha256=(Get-FileHash (Join-Path $InstallRoot 'PACKAGE_MANIFEST.json')).Hash; data_preserved=$true} | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $DataRoot 'install_receipt.json')
  '설치 완료. 바탕화면의 MINDLE MEDIA AI 아이콘을 실행하세요.' | Tee-Object -FilePath (Join-Path $DataRoot 'logs\install.log')
} catch { Write-Host ('설치 실패: ' + $_.Exception.Message) -ForegroundColor Red; exit 1 }
exit 0
