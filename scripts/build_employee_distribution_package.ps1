param(
  [Parameter(Mandatory=$true)][string]$PythonRoot,
  [Parameter(Mandatory=$true)][string]$ModelRoot,
  [Parameter(Mandatory=$true)][string]$FFmpegRoot,
  [Parameter(Mandatory=$true)][string]$RuntimeLock,
  [int]$PartMiB=300
)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
& (Join-Path $PythonRoot 'python.exe') (Join-Path $PSScriptRoot 'build_employee_distribution_package.py') --repo $Repo --python-root $PythonRoot --model-root $ModelRoot --ffmpeg-root $FFmpegRoot --runtime-lock $RuntimeLock
if ($LASTEXITCODE -ne 0) { throw '직원용 패키지 빌드 전제조건 또는 파일 검증 실패. 완성 패키지를 만들지 않았습니다.' }
& (Join-Path $PSScriptRoot 'split_employee_package.ps1') -ZipPath (Join-Path $Repo 'dist\MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip') -PartMiB $PartMiB
