param([switch]$DeleteUserData,[string]$ShortcutRoot)
$ErrorActionPreference = 'Stop'
$Base = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'MINDLE'))
$InstallRoot = [IO.Path]::GetFullPath((Join-Path $Base 'MEDIA_AI'))
$DataRoot = [IO.Path]::GetFullPath((Join-Path $Base 'MEDIA_AI_DATA'))
if ((Split-Path $InstallRoot -Parent) -ne $Base -or (Split-Path $DataRoot -Parent) -ne $Base) { throw '안전한 삭제 경로를 확인할 수 없습니다.' }
# Refuse while the package is serving; never kill another application.
$Running = Get-Process python,pythonw -ErrorAction SilentlyContinue | Where-Object { $_.Path -in @((Join-Path $InstallRoot 'runtime\python\python.exe'),(Join-Path $InstallRoot 'runtime\python\pythonw.exe')) }
foreach ($Process in $Running) { Stop-Process -Id $Process.Id -ErrorAction Stop }
if (Test-Path -LiteralPath $InstallRoot) { Remove-Item -LiteralPath $InstallRoot -Recurse -Force }
$Desktop = [Environment]::GetFolderPath('Desktop')
$Menu = Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\MINDLE'
if ($ShortcutRoot) { $Desktop = Join-Path $ShortcutRoot 'Desktop'; $Menu = Join-Path $ShortcutRoot 'StartMenu\Programs\MINDLE' }
foreach ($Link in @((Join-Path $Desktop 'MINDLE MEDIA AI.lnk'),(Join-Path $Menu 'MINDLE MEDIA AI.lnk'))) {
  if (Test-Path -LiteralPath $Link) { Remove-Item -LiteralPath $Link -Force }
}
if ($DeleteUserData -and (Test-Path -LiteralPath $DataRoot)) { Remove-Item -LiteralPath $DataRoot -Recurse -Force }
Write-Host '삭제 완료. 기본 설정에서는 작업 데이터가 보존됩니다.'
