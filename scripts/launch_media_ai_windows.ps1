param()
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedBranch = 'feature/ad-shortform-bridge-p0-20260926'
$branch = (& git -C $RepoRoot branch --show-current).Trim()
if ($branch -ne $ExpectedBranch) { throw "MEDIA AI launcher blocked: expected $ExpectedBranch, got $branch" }
$head = (& git -C $RepoRoot rev-parse --short HEAD).Trim()
$port = 8768
$base = "http://127.0.0.1:$port/"
$url = "$base`?ui_build=$head"
$healthy = $false
try {
  $response = Invoke-WebRequest -UseBasicParsing -Uri $base -TimeoutSec 2
  $healthy = ($response.StatusCode -eq 200 -and $response.Content -match 'approved_visual\.css' -and $response.Content -match 'MINDLE MEDIA AI')
} catch { $healthy = $false }
if (-not $healthy) {
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
    try { $response = Invoke-WebRequest -UseBasicParsing -Uri $base -TimeoutSec 2; $healthy = ($response.StatusCode -eq 200 -and $response.Content -match 'approved_visual\.css') } catch { $healthy = $false }
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
if ($browser) { Start-Process -FilePath $browser -ArgumentList "--start-maximized", $url }
else { Start-Process $url }
