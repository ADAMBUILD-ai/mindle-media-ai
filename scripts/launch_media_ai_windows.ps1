param()
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedBranch = 'feature/ad-shortform-bridge-p0-20260926'
$branch = (& git -C $RepoRoot branch --show-current).Trim()
if ($branch -ne $ExpectedBranch) { throw "MEDIA AI launcher blocked: expected $ExpectedBranch, got $branch" }
$fullHead = (& git -C $RepoRoot rev-parse HEAD).Trim()
$head = $fullHead.Substring(0, 7)
$identityFiles = @('ui/index.html','ui/approved_visual.css','ui/interaction.css','ui/interaction.js','ui/product_integration.js','ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico')
$hashLines = foreach ($relative in $identityFiles) { "${relative}:$((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $RepoRoot $relative)).Hash.ToLower())" }
$workspaceFingerprint = (([System.Security.Cryptography.SHA256]::Create()).ComputeHash([Text.Encoding]::UTF8.GetBytes(($hashLines -join "`n"))) | ForEach-Object { $_.ToString('x2') }) -join ''
$port = 8768
$base = "http://127.0.0.1:$port/"
$url = "$base`?ui_build=$head"
$healthy = $false
function Get-Identity {
  try { return (Invoke-RestMethod -UseBasicParsing -Uri "$base`api/runtime-identity" -TimeoutSec 2) } catch { return $null }
}
try {
  $identity = Get-Identity
  $healthy = ($identity -and $identity.repo_root -eq $RepoRoot -and $identity.branch -eq $ExpectedBranch -and $identity.head -eq $fullHead -and $identity.workspace_ui_fingerprint -eq $workspaceFingerprint)
} catch { $healthy = $false }
if (-not $healthy) {
  $listeners = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort $port -State Listen -ErrorAction SilentlyContinue
  foreach ($listener in $listeners) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($listener.OwningProcess)" -ErrorAction SilentlyContinue
    if ($proc -and $proc.CommandLine -match 'media_ai\.product_server') { Stop-Process -Id $listener.OwningProcess -Force }
  }
  $python = (Get-Command python.exe -ErrorAction Stop).Source
  $dataDir = Join-Path $RepoRoot 'work-data\v20_2-ui-data'
  New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
  $args = "-m media_ai.product_server --root `"$RepoRoot`" --data-dir `"$dataDir`" --port $port"
  $env:PYTHONPATH = Join-Path $RepoRoot 'src'
  if (-not $env:HF_TOKEN) { $env:HF_TOKEN = 'local-v20.2-runtime' }
  Start-Process -FilePath $python -ArgumentList $args -WorkingDirectory $RepoRoot -WindowStyle Hidden | Out-Null
  $deadline = (Get-Date).AddSeconds(15)
  do {
    Start-Sleep -Milliseconds 250
    try { $identity = Get-Identity; $healthy = ($identity -and $identity.repo_root -eq $RepoRoot -and $identity.branch -eq $ExpectedBranch -and $identity.head -eq $fullHead -and $identity.workspace_ui_fingerprint -eq $workspaceFingerprint) } catch { $healthy = $false }
  } while (-not $healthy -and (Get-Date) -lt $deadline)
  if (-not $healthy) { throw 'MEDIA AI server did not become healthy on port 8768' }
}
$browserCandidates = @(
  (Join-Path $env:ProgramFiles 'Microsoft\Edge\Application\msedge.exe'),
  (Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'),
  (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
  (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe')
)
$browser = $browserCandidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if ($browser) { Start-Process -FilePath $browser -ArgumentList "--new-window", "--start-maximized", $url }
else { Start-Process $url }
