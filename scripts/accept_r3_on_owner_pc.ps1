$ErrorActionPreference = 'Stop'
$ExpectedExe = '701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5'
$ExpectedManifest = 'ec2b82e15eba653a977ce9ddfcf1fb0b697d2bd701c8a7e65aa37f51b68652ca'
$ExpectedRuntime = '9f5d304ce825-0f8cc3c5d320-ai-r3'
$Candidate = Join-Path $env:LOCALAPPDATA 'MINDLE\PC_TEST_INSTALLS\20261024_R3\MINDLE_MEDIA_AI_PC_TEST_20261024_R3'
$RuntimeRoot = Join-Path $env:LOCALAPPDATA "MINDLE\runtime\$ExpectedRuntime"
$Exe = Join-Path $Candidate 'MINDLE_MEDIA_AI_RUN.exe'
$ManifestPath = Join-Path $Candidate '_payload\PACKAGE_MANIFEST.json'
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$Desktop = [Environment]::GetFolderPath('Desktop')
$Evidence = Join-Path $Desktop "MINDLE_MEDIA_AI_R3_ACCEPTANCE_$Stamp"
New-Item -ItemType Directory -Force -Path $Evidence | Out-Null

function Sha256([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLower() }
function Find-Runtime {
  foreach($port in 18768..18777) {
    try {
      $base = "http://127.0.0.1:$port"
      $identity = Invoke-RestMethod -Uri "$base/api/runtime-identity" -TimeoutSec 2
      if($identity.install_root -eq $RuntimeRoot -and $identity.package_manifest_sha256 -eq $ExpectedManifest) {
        return [ordered]@{base=$base;identity=$identity}
      }
    } catch {}
  }
  throw '정확한 R3 제품 서버를 찾지 못했습니다.'
}
function Find-Mp4($Value) {
  $found = New-Object System.Collections.Generic.List[string]
  function Visit($Node) {
    if($null -eq $Node) { return }
    if($Node -is [string]) {
      if($Node.EndsWith('.mp4',[StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $Node)) { $found.Add($Node) }
      return
    }
    if($Node -is [System.Collections.IDictionary]) { foreach($key in $Node.Keys) { Visit $Node[$key] }; return }
    if($Node -is [System.Collections.IEnumerable]) { foreach($item in $Node) { Visit $item }; return }
    foreach($property in $Node.PSObject.Properties) { Visit $property.Value }
  }
  Visit $Value
  return @($found | Select-Object -Unique)
}
function Save-Json([string]$Name,$Value) {
  $Value | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $Evidence $Name) -Encoding utf8
}
function Post-Json([string]$Uri,$Value,[int]$TimeoutSec=180) {
  $json = $Value | ConvertTo-Json -Depth 30 -Compress
  Invoke-RestMethod -Uri $Uri -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec $TimeoutSec
}

if(!(Test-Path -LiteralPath $Exe) -or !(Test-Path -LiteralPath $ManifestPath)) { throw "R3 설치 폴더가 없습니다: $Candidate" }
if((Sha256 $Exe) -ne $ExpectedExe) { throw 'R3 EXE SHA-256이 다릅니다.' }
if((Sha256 $ManifestPath) -ne $ExpectedManifest) { throw 'R3 manifest SHA-256이 다릅니다.' }
$Manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding utf8 | ConvertFrom-Json
if($Manifest.runtime_id -ne $ExpectedRuntime) { throw 'R3 runtime identity가 다릅니다.' }

$Checked = 0
foreach($item in $Manifest.files) {
  $path = Join-Path (Join-Path $Candidate '_payload') ($item.path -replace '/','\')
  if(!(Test-Path -LiteralPath $path)) { throw "payload 누락: $($item.path)" }
  $file = Get-Item -LiteralPath $path
  if($file.Length -ne $item.bytes -or (Sha256 $path) -ne $item.sha256) { throw "payload 불일치: $($item.path)" }
  $Checked++
  if(($Checked % 500) -eq 0) { Write-Host "파일 검증 $Checked / $($Manifest.files.Count)" }
}

Start-Process -FilePath $Exe -WorkingDirectory $Candidate
$Runtime = $null
foreach($attempt in 1..120) { try {$Runtime=Find-Runtime;break} catch {Start-Sleep -Milliseconds 500} }
if($null -eq $Runtime) { throw 'R3 실행 후 endpoint가 열리지 않았습니다.' }
$Before = Invoke-RestMethod -Uri "$($Runtime.base)/api/runtime/control" -TimeoutSec 5
$Readiness = Invoke-RestMethod -Uri "$($Runtime.base)/api/runtime-readiness" -TimeoutSec 15
$Planner = Invoke-RestMethod -Uri "$($Runtime.base)/api/workflows/capabilities" -TimeoutSec 15
Save-Json '01_RUNTIME_BEFORE.json' ([ordered]@{candidate=$Candidate;runtime_root=$RuntimeRoot;exe_sha256=$ExpectedExe;manifest_sha256=$ExpectedManifest;payload_files_checked=$Checked;endpoint=$Runtime.base;identity=$Runtime.identity;control=$Before;readiness=$Readiness;planner_capabilities=$Planner;captured_at=(Get-Date).ToString('o')})

# A visible window is not acceptance. Create a fresh source and require the
# pinned Qwen planner, Supertonic neural voice and FFmpeg MP4 chain to run now.
$FreshFolder = Join-Path $Evidence 'fresh-ai-runtime'
New-Item -ItemType Directory -Force -Path $FreshFolder | Out-Null
$Ffmpeg = Join-Path $RuntimeRoot 'tools\ffmpeg\ffmpeg.exe'
$Ffprobe = Join-Path $RuntimeRoot 'tools\ffmpeg\ffprobe.exe'
if(!(Test-Path -LiteralPath $Ffmpeg)) { throw 'R3 FFmpeg 실행기가 없습니다.' }
$FreshVideo = Join-Path $FreshFolder 'fresh-input.mp4'
$FfmpegArgs = @('-v','error','-f','lavfi','-i','color=c=blue:s=320x180:r=10','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','4','-c:v','h264_mf','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart','-y',$FreshVideo)
& $Ffmpeg @FfmpegArgs
if($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $FreshVideo)) { throw '새 AI 검증 입력 MP4 생성에 실패했습니다.' }
$FreshImport = Post-Json "$($Runtime.base)/api/media/import" ([ordered]@{kind='video';filename='owner-ai-alive-input.mp4';content_base64=[Convert]::ToBase64String([IO.File]::ReadAllBytes($FreshVideo))})
$FreshCommand = '밝기를 3 높이고 "반갑습니다. 민들레 미디어 AI입니다." 나레이션을 넣고 영상을 연장해 주세요.'
$FreshPlan = Post-Json "$($Runtime.base)/api/workflows/plan" ([ordered]@{command=$FreshCommand}) 300
if($FreshPlan.plan_source -ne 'LOCAL_GENERATIVE_INFERENCE' -or $FreshPlan.model_id -notlike 'Qwen*') { throw 'Qwen 실제 생성형 계획이 확인되지 않았습니다.' }
$Brightness = @($FreshPlan.steps | Where-Object {$_.operation -eq 'video_edit'})[0].options.brightness
$Narration = @($FreshPlan.steps | Where-Object {$_.operation -eq 'narrate'})[0].text
if($Brightness -ne 3 -or $Narration -ne '반갑습니다. 민들레 미디어 AI입니다.') { throw 'Qwen 계획이 요청한 수치 또는 원고를 보존하지 않았습니다.' }
$FreshTask = Post-Json "$($Runtime.base)/api/workflows" ([ordered]@{request_id=[Guid]::NewGuid().ToString();plan_id=$FreshPlan.plan_id;input_job_id=$FreshImport.job_id;job_ids=@($FreshImport.job_id);steps=$FreshPlan.steps;export=$true})
$FreshDeadline = (Get-Date).AddMinutes(15)
while($FreshTask.state -notin @('SUCCEEDED','FAILED','CANCELLED','INTERRUPTED') -and (Get-Date) -lt $FreshDeadline) {
  Start-Sleep -Milliseconds 500
  $FreshTask = Invoke-RestMethod -Uri "$($Runtime.base)/api/workflows/$($FreshTask.workflow_id)" -TimeoutSec 30
}
if($FreshTask.state -ne 'SUCCEEDED') { throw "새 AI 작업 실패: $($FreshTask.state) $($FreshTask.error)" }
$FreshVoice = @($FreshTask.records | Where-Object {$_.operation -eq 'narration'})[-1]
if($FreshVoice.runtime_result.model_inference -ne $true -or $FreshVoice.runtime_result.engine -notlike '*Supertonic*') { throw 'Supertonic 실제 신경망 음성 생성이 확인되지 않았습니다.' }
$FreshOutput = $FreshTask.result.primary_output.path
if(!(Test-Path -LiteralPath $FreshOutput) -or !($FreshOutput.EndsWith('.mp4',[StringComparison]::OrdinalIgnoreCase))) { throw 'AI 작업 MP4가 생성되지 않았습니다.' }
$FreshProbe = $null
if(Test-Path -LiteralPath $Ffprobe) { $FreshProbe = & $Ffprobe -v error -show_streams -show_format -of json -- $FreshOutput | ConvertFrom-Json }
$FreshHasVideo = @($FreshProbe.streams | Where-Object {$_.codec_type -eq 'video'}).Count -gt 0
$FreshHasAudio = @($FreshProbe.streams | Where-Object {$_.codec_type -eq 'audio'}).Count -gt 0
if(!$FreshHasVideo -or !$FreshHasAudio) { throw 'AI 작업 MP4의 영상 또는 오디오 스트림이 없습니다.' }
$FreshAiGate = $true
Save-Json '02_FRESH_AI_RUNTIME_PASS.json' ([ordered]@{status='FRESH_QWEN_SUPERTONIC_FFMPEG_PASS';command=$FreshCommand;plan=$FreshPlan;workflow_id=$FreshTask.workflow_id;project_id=$FreshTask.project_id;qwen_actual_inference=$true;supertonic_actual_inference=$true;mp4_path=$FreshOutput;mp4_sha256=(Sha256 $FreshOutput);mp4_probe=$FreshProbe;captured_at=(Get-Date).ToString('o')})

Start-Process $Runtime.base
Write-Host ''
Write-Host '브라우저에서 사진·영상·자막·나레이션·참고 이미지를 확인하고 프로젝트 저장과 내보내기를 실행하세요.' -ForegroundColor Cyan
Write-Host '내보낸 MP4를 설치된 Windows 플레이어로 재생·탐색하고 실제 소리를 들으세요.' -ForegroundColor Cyan
Read-Host '완료한 뒤 이 창으로 돌아와 Enter를 누르세요'

$LatestBefore = Invoke-RestMethod -Uri "$($Runtime.base)/api/projects/latest" -TimeoutSec 10
$WorkflowsBefore = Invoke-RestMethod -Uri "$($Runtime.base)/api/workflows" -TimeoutSec 10
$ArchitectureBefore = Invoke-RestMethod -Uri "$($Runtime.base)/api/architecture-agent/productions" -TimeoutSec 10
Save-Json '02_PROJECT_BEFORE_RESTART.json' ([ordered]@{latest=$LatestBefore;workflows=$WorkflowsBefore;architecture=$ArchitectureBefore})
$Mp4Before = @(Find-Mp4 ([ordered]@{latest=$LatestBefore;workflows=$WorkflowsBefore;architecture=$ArchitectureBefore}))
if($Mp4Before.Count -lt 1) { throw '저장된 프로젝트에서 재생할 MP4를 찾지 못했습니다.' }
$PlayerFile = $Mp4Before[0]
$MediaProbe = $null
if(Test-Path -LiteralPath $Ffprobe) {
  $MediaProbe = & $Ffprobe -v error -show_streams -show_format -of json -- $PlayerFile | ConvertFrom-Json
}
Save-Json '02_MEDIA_BEFORE_RESTART.json' ([ordered]@{path=$PlayerFile;bytes=(Get-Item -LiteralPath $PlayerFile).Length;sha256=(Sha256 $PlayerFile);ffprobe=$MediaProbe})
Start-Process -FilePath $PlayerFile
Write-Host "Windows 기본 플레이어에서 열었습니다: $PlayerFile" -ForegroundColor Cyan
Read-Host '영상 표시·재생·앞뒤 탐색·실제 소리를 확인한 뒤 Enter를 누르세요'

$headers = @{'X-Mindle-Control'=$Before.control_nonce}
$body = @{server_pid=$Before.server_pid;server_instance_id=$Before.server_instance_id} | ConvertTo-Json
Invoke-RestMethod -Uri "$($Runtime.base)/api/runtime/shutdown" -Method Post -Headers $headers -ContentType 'application/json' -Body $body -TimeoutSec 10 | Out-Null
$Closed = $false
foreach($attempt in 1..80) {
  try { Invoke-RestMethod -Uri "$($Runtime.base)/api/runtime-identity" -TimeoutSec 1 | Out-Null }
  catch {$Closed=$true;break}
  Start-Sleep -Milliseconds 250
}
if(!$Closed) { throw '제품 endpoint가 정상 종료되지 않았습니다.' }

Start-Process -FilePath $Exe -WorkingDirectory $Candidate
$AfterRuntime = $null
foreach($attempt in 1..120) { try {$AfterRuntime=Find-Runtime;break} catch {Start-Sleep -Milliseconds 500} }
if($null -eq $AfterRuntime) { throw 'R3 재실행 endpoint가 열리지 않았습니다.' }
$After = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/runtime/control" -TimeoutSec 5
if($After.server_pid -eq $Before.server_pid -or $After.server_instance_id -eq $Before.server_instance_id) { throw '새 서버 PID 또는 instance identity가 확인되지 않았습니다.' }
$LatestAfter = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/projects/latest" -TimeoutSec 10
$WorkflowsAfter = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/workflows" -TimeoutSec 10
$ArchitectureAfter = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/architecture-agent/productions" -TimeoutSec 10
Save-Json '03_RUNTIME_AFTER.json' ([ordered]@{old_endpoint_closed=$Closed;before=$Before;after=$After;identity=$AfterRuntime.identity;latest=$LatestAfter;workflows=$WorkflowsAfter;architecture=$ArchitectureAfter;captured_at=(Get-Date).ToString('o')})

Start-Process $AfterRuntime.base
Write-Host '재실행된 제품에서 동일 프로젝트와 사진·영상·자막·나레이션·참고 자료를 확인하고 다시 Export하세요.' -ForegroundColor Cyan
Read-Host 'Reopen과 재실행 후 Export를 완료한 뒤 Enter를 누르세요'
$LatestFinal = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/projects/latest" -TimeoutSec 10
$WorkflowsFinal = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/workflows" -TimeoutSec 10
$ProjectId = $LatestFinal.project.project_id
if(!$ProjectId) { throw '재실행 후 복원된 project_id가 없습니다.' }
$ExportReceipt = Invoke-RestMethod -Uri "$($AfterRuntime.base)/api/projects/$ProjectId/export" -Method Post -ContentType 'application/json' -Body '{}' -TimeoutSec 120
$ExportZip = Join-Path $Evidence 'REOPEN_EXPORT.zip'
Invoke-WebRequest -Uri "$($AfterRuntime.base)$($ExportReceipt.download_url)" -OutFile $ExportZip -TimeoutSec 120
$ExportSha = Sha256 $ExportZip
if($ExportReceipt.export.sha256 -and $ExportReceipt.export.sha256 -ne $ExportSha) { throw '재실행 후 Export ZIP 해시가 응답과 다릅니다.' }
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Archive = [IO.Compression.ZipFile]::OpenRead($ExportZip)
try {
  foreach($Entry in $Archive.Entries) {
    if($Entry.Length -eq 0) { continue }
    $Stream = $Entry.Open()
    try { $Stream.CopyTo([IO.Stream]::Null) } finally { $Stream.Dispose() }
  }
  $ExportEntries = $Archive.Entries.Count
} finally { $Archive.Dispose() }
Save-Json '04_REOPEN_EXPORT.json' ([ordered]@{latest=$LatestFinal;workflows=$WorkflowsFinal;export_receipt=$ExportReceipt;export_zip_sha256=$ExportSha;export_zip_entries=$ExportEntries;zip_crc='PASS_ALL_ENTRIES_READ';captured_at=(Get-Date).ToString('o')})
$Heard = (Read-Host 'Windows 플레이어에서 실제 나레이션/소리를 들었습니까? Y 또는 N').Trim().ToUpper() -eq 'Y'
$Seek = (Read-Host 'Windows 플레이어에서 재생과 앞뒤 탐색이 정상입니까? Y 또는 N').Trim().ToUpper() -eq 'Y'
$Ui = (Read-Host '1536x1024 100% 기준 VIDEO 좌측/PHOTO 우측과 전체 UI를 직접 확인했습니까? Y 또는 N').Trim().ToUpper() -eq 'Y'
$SameProject = $LatestBefore.project.project_id -and $LatestBefore.project.project_id -eq $LatestAfter.project.project_id -and $LatestBefore.project.project_id -eq $LatestFinal.project.project_id
$Result = [ordered]@{
  status = if($FreshAiGate -and $Heard -and $Seek -and $Ui -and $SameProject) {'OWNER_PC_ACCEPTANCE_EVIDENCE_COMPLETE'} else {'OWNER_PC_ACCEPTANCE_PARTIAL'}
  source = '9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6'
  candidate = 'MINDLE_MEDIA_AI_PC_TEST_20261024_R3'
  payload_files_checked = $Checked
  old_endpoint_closed = $Closed
  old_pid = $Before.server_pid
  new_pid = $After.server_pid
  same_project_reopened = [bool]$SameProject
  fresh_qwen_supertonic_ffmpeg_chain = [bool]$FreshAiGate
  windows_player_play_seek = [bool]$Seek
  human_hearing = [bool]$Heard
  owner_ui_observed = [bool]$Ui
  inspected_mp4_path = $PlayerFile
  inspected_mp4_sha256 = Sha256 $PlayerFile
  reopen_export_zip_sha256 = $ExportSha
  reopen_export_zip_crc = 'PASS_ALL_ENTRIES_READ'
  approved_ui_pixel_match = $false
  full_product_pass = $false
  pr23_hold_do_not_merge = $true
  evidence_folder = $Evidence
}
Save-Json 'FINAL_OWNER_PC_RESULT.json' $Result
Compress-Archive -Path (Join-Path $Evidence '*') -DestinationPath "$Evidence.zip" -Force
Write-Host "완료: $Evidence.zip" -ForegroundColor Green
Read-Host '창을 닫으려면 Enter를 누르세요'
