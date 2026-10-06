param([Parameter(Mandatory=$true)][string]$InstallRoot,[Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference = 'Stop'
$Python = Join-Path $InstallRoot 'runtime\python\python.exe'
New-Item -ItemType Directory -Force -Path $EvidenceDirectory | Out-Null
$env:HF_TOKEN = $null; $env:PYTHONPATH = $null; $env:PYTHONHOME = $null
$env:HF_HUB_OFFLINE='1'; $env:TRANSFORMERS_OFFLINE='1'
$env:PATH = Join-Path $env:SystemRoot 'System32'
& $Python (Join-Path $InstallRoot 'app\launcher\employee_package_launcher.py') --verify-only
if ($LASTEXITCODE -ne 0) { throw 'Package file verification failed' }
& $Python -c "import sys,torch,transformers,openvino,cv2,safetensors; assert sys.flags.isolated; assert torch.version.cuda is None; print('PACKAGE_RUNTIME_IMPORT_PASS')" *> (Join-Path $EvidenceDirectory 'runtime-imports.txt')
if ($LASTEXITCODE -ne 0) { throw 'Bundled isolated CPU runtime imports failed' }
@{status='PACKAGE_RUNTIME_SMOKE_PASS_ONLY'; clean_windows_e2e='NOT_RUN'; remaining='Desktop 2/2, four model operations, preview, save/reopen/export and uninstall/reinstall require actual end-to-end verification.'} | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDirectory 'RUNTIME_SMOKE_TEST.json')
Write-Host 'Bundled runtime smoke passed. Full employee E2E is still required.'
