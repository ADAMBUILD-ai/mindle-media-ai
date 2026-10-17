param([switch]$VerifyOnly)
$ErrorActionPreference = 'Stop'
try {
  $Manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'SPLIT_PARTS_MANIFEST.json') | ConvertFrom-Json
  if ([IO.Path]::GetFileName($Manifest.zip_name) -ne $Manifest.zip_name) { throw 'Invalid ZIP name' }
  $ZipPath = Join-Path $PSScriptRoot $Manifest.zip_name
  $Verified = @()
  foreach ($Part in $Manifest.parts) {
    if ([IO.Path]::GetFileName($Part.name) -ne $Part.name) { throw 'Invalid part name' }
    $Path = Join-Path $PSScriptRoot $Part.name
    if (-not (Test-Path -LiteralPath $Path) -or (Get-Item -LiteralPath $Path).Length -ne $Part.bytes -or (Get-FileHash -LiteralPath $Path).Hash.ToLower() -ne $Part.sha256) { throw ('분할 파일 검증 실패: ' + $Part.name) }
    $Verified += $Path
  }
  $OutputStream = [IO.File]::Create($ZipPath)
  try { foreach ($Path in $Verified) { $Stream = [IO.File]::OpenRead($Path); try { $Stream.CopyTo($OutputStream) } finally { $Stream.Dispose() } } } finally { $OutputStream.Dispose() }
  if ((Get-Item -LiteralPath $ZipPath).Length -ne $Manifest.zip_bytes -or (Get-FileHash -LiteralPath $ZipPath).Hash.ToLower() -ne $Manifest.zip_sha256) { throw 'ZIP SHA-256 검증 실패' }
  if (-not $VerifyOnly) {
    # Keep extracted dependency paths below legacy Windows path limits.
    $Extract = Join-Path ([IO.Path]::GetTempPath()) ('MindlePkg_' + [guid]::NewGuid().ToString('N').Substring(0,8))
    Expand-Archive -LiteralPath $ZipPath -DestinationPath $Extract
    $Installers = @(Get-ChildItem -LiteralPath $Extract -Filter INSTALL_MINDLE_MEDIA_AI.cmd -Recurse)
    if ($Installers.Count -ne 1) { throw '설치 파일을 확인할 수 없습니다.' }
    & $Installers[0].FullName
    if ($LASTEXITCODE -ne 0) { throw '설치 실패' }
  }
  Write-Host '파일 검증/재조립 완료' -ForegroundColor Green
} catch { Write-Host ('실패: ' + $_.Exception.Message) -ForegroundColor Red; exit 1 }
