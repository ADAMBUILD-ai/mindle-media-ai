param([switch]$InspectOnly,[string]$OutputDirectory = (Join-Path $env:TEMP 'MindleVCRuntime'))
$ErrorActionPreference = 'Stop'
$Required = @('msvcp140.dll','msvcp140_atomic_wait.dll','vcruntime140_threads.dll')
$Missing = @($Required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $env:SystemRoot ('System32\' + $_))) })
if ($InspectOnly) {
  @{mode='ONLINE_PREREQUISITE_ONLY';missing=$Missing;offline_full_package_pass=$false} | ConvertTo-Json
  exit 0
}
Write-Host '이 보조 설치기는 완전 오프라인 패키지가 아닙니다.'
Write-Host 'Microsoft 공식 사이트에서 Visual C++ x64 런타임을 내려받아 설치합니다.'
Write-Host '관리자 권한 요청이 표시될 수 있습니다. Microsoft 사용권 조항이 적용됩니다.'
if ((Read-Host '다운로드와 설치에 동의하면 INSTALL을 입력하세요') -cne 'INSTALL') { Write-Host '동의하지 않아 중단했습니다.'; exit 2 }
try {
  New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
  $Path = Join-Path $OutputDirectory 'vc_redist.x64.exe'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  Invoke-WebRequest -Uri 'https://aka.ms/vc14/vc_redist.x64.exe' -OutFile $Path -UseBasicParsing
  $Signature = Get-AuthenticodeSignature -LiteralPath $Path
  if ($Signature.Status -ne 'Valid' -or $Signature.SignerCertificate.Subject -notmatch '(^|,\s*)O=Microsoft Corporation(,|$)') { throw 'Microsoft 서명 검증 실패' }
  $Record = @{mode='ONLINE_BOOTSTRAP';source_url='https://aka.ms/vc14/vc_redist.x64.exe';sha256=(Get-FileHash -LiteralPath $Path).Hash.ToLower();version=(Get-Item -LiteralPath $Path).VersionInfo.FileVersion;signature=[string]$Signature.Status;publisher=$Signature.SignerCertificate.Subject;license_reference='https://visualstudio.microsoft.com/license-terms/';consent='INSTALL';offline_full_package_pass=$false}
  $Record | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $OutputDirectory 'VC_RUNTIME_INSTALL_RESULT.json') -Encoding UTF8
  $Process = Start-Process -FilePath $Path -ArgumentList '/install','/quiet','/norestart' -WindowStyle Hidden -Wait -PassThru
  $Record.exit_code = $Process.ExitCode
  $Record.status = if ($Process.ExitCode -in @(0,1638,3010)) {'PREREQUISITE_INSTALLER_COMPLETED'} else {'FAILED'}
  $Record | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $OutputDirectory 'VC_RUNTIME_INSTALL_RESULT.json') -Encoding UTF8
  if ($Process.ExitCode -eq 3010) { Write-Host 'Windows를 재시작한 후 호스트 검증 도구를 실행하세요.'; exit 3010 }
  if ($Record.status -eq 'FAILED') { throw ('Microsoft 설치기 오류: ' + $Process.ExitCode) }
  foreach ($Name in $Required) { if (-not (Test-Path -LiteralPath (Join-Path $env:SystemRoot ('System32\' + $Name)))) { throw ('필수 런타임 미확인: ' + $Name) } }
  Write-Host '공식 온라인 런타임 설치 완료. 완전 오프라인 배포 승인을 의미하지 않습니다.'
} catch { Write-Error $_; exit 1 }
