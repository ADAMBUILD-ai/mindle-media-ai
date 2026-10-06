param([Parameter(Mandatory=$true)][string]$ZipPath,[string]$OutputDirectory,[int]$PartMiB=300)
$ErrorActionPreference = 'Stop'
if ($PartMiB -lt 1 -or $PartMiB -gt 1024) { throw 'PartMiB must be 1..1024' }
$ZipPath = (Resolve-Path -LiteralPath $ZipPath).Path
if (-not $OutputDirectory) { $OutputDirectory = Join-Path (Split-Path $ZipPath -Parent) 'transfer_parts' }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
if (Get-ChildItem -LiteralPath $OutputDirectory -Filter '*.zip.*' -ErrorAction SilentlyContinue) { throw 'Output directory already has parts; use a fresh directory.' }
$InputStream = [IO.File]::OpenRead($ZipPath)
$Parts = @(); $Buffer = New-Object byte[] (1MB); $Index = 0
try {
  while ($InputStream.Position -lt $InputStream.Length) {
    $Index++; $Name = ([IO.Path]::GetFileName($ZipPath)) + '.' + $Index.ToString('000')
    $PartPath = Join-Path $OutputDirectory $Name; $OutputStream = [IO.File]::Create($PartPath); $Written = [long]0
    try { while ($Written -lt ([long]$PartMiB * 1MB)) {
      $Read = $InputStream.Read($Buffer,0,[int][Math]::Min($Buffer.Length,([long]$PartMiB * 1MB)-$Written))
      if ($Read -eq 0) { break }; $OutputStream.Write($Buffer,0,$Read); $Written += $Read
    }} finally { $OutputStream.Dispose() }
    $Parts += @{name=$Name; bytes=$Written; sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $PartPath).Hash.ToLower()}
  }
} finally { $InputStream.Dispose() }
@{zip_name=[IO.Path]::GetFileName($ZipPath); zip_bytes=(Get-Item -LiteralPath $ZipPath).Length; zip_sha256=(Get-FileHash -LiteralPath $ZipPath).Hash.ToLower(); parts=$Parts} | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $OutputDirectory 'SPLIT_PARTS_MANIFEST.json')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'reassemble_employee_package.ps1') -Destination (Join-Path $OutputDirectory 'REASSEMBLE_AND_INSTALL.ps1')
'@echo off','powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REASSEMBLE_AND_INSTALL.ps1"','set "RESULT=%errorlevel%"','pause','exit /b %RESULT%' | Set-Content -Encoding ASCII (Join-Path $OutputDirectory 'REASSEMBLE_AND_INSTALL.cmd')
