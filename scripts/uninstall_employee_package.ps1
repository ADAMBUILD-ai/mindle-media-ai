param([switch]$DeleteUserData)
$ErrorActionPreference = 'Stop'
$Base = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'MINDLE'))
$InstallRoot = [IO.Path]::GetFullPath((Join-Path $Base 'MEDIA_AI'))
$DataRoot = [IO.Path]::GetFullPath((Join-Path $Base 'MEDIA_AI_DATA'))
if ((Split-Path $InstallRoot -Parent) -ne $Base -or (Split-Path $DataRoot -Parent) -ne $Base) { throw '안전한 삭제 경로를 확인할 수 없습니다.' }
# Refuse while the package is serving; never kill another application.
$Running = Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^pythonw?\.exe$' -and $_.ExecutablePath -eq (Join-Path $InstallRoot 'runtime\python\python.exe') }
foreach ($Process in $Running) { Stop-Process -Id $Process.ProcessId -ErrorAction Stop }
if (Test-Path -LiteralPath $InstallRoot) { Remove-Item -LiteralPath $InstallRoot -Recurse -Force }
foreach ($Link in @((Join-Path ([Environment]::GetFolderPath('Desktop')) 'MINDLE MEDIA AI.lnk'),(Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs\MINDLE\MINDLE MEDIA AI.lnk'))) {
  if (Test-Path -LiteralPath $Link) { Remove-Item -LiteralPath $Link -Force }
}
if ($DeleteUserData -and (Test-Path -LiteralPath $DataRoot)) { Remove-Item -LiteralPath $DataRoot -Recurse -Force }
Write-Host '삭제 완료. 기본 설정에서는 작업 데이터가 보존됩니다.'
