$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$base=Join-Path $env:USERPROFILE 'Downloads\MINDLE_MEDIA_AI_FINAL'
New-Item -ItemType Directory -Force -Path $base|Out-Null
$parts=@()
$o=Join-Path $base 'artifact-00.zip';$d=Join-Path $base 'artifact-00'
Write-Host 'Downloading verified part 00/04 ...'
& curl.exe -L --fail --retry 3 --retry-delay 2 -o $o 'https://sdmntprcentralus.oaiusercontent.com/files/00000000-99b0-81f5-84cb-6112ad02c472/raw?se=2026-10-13T05%3A33%3A58Z&sp=r&sv=2026-02-06&sr=b&scid=c68c53a1-115e-5cbf-be4e-871b0d5319b2&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-12T23%3A54%3A37Z&ske=2026-10-13T23%3A54%3A37Z&sks=b&skv=2026-02-06&sig=lE0NTHbJorDbMa%2BSVI8lPw/FwrKSfkNa8GzS9Q4U2jo%3D'
if($LASTEXITCODE-ne 0){throw 'download failed'}
if((Get-FileHash $o -Algorithm SHA256).Hash.ToLowerInvariant()-ne'2081322d5186538b18d52b977be6c5881a2055d4abb2be22d98485ee58f3c988'){throw 'artifact 00 hash failed'}
if(Test-Path $d){Remove-Item -Recurse -Force $d}
Expand-Archive $o $d -Force
$i=Get-ChildItem $d -Recurse -File|Where-Object{$_.Name-like'*.part-00'}|Select-Object -First 1
if(-not $i){throw 'part 00 missing'};$parts+=$i.FullName
$o=Join-Path $base 'artifact-01.zip';$d=Join-Path $base 'artifact-01'
Write-Host 'Downloading verified part 01/04 ...'
& curl.exe -L --fail --retry 3 --retry-delay 2 -o $o 'https://sdmntprnznorth.oaiusercontent.com/files/00000000-c2d8-820b-a8f6-c6d6f613fe8b/raw?se=2026-10-13T05%3A35%3A09Z&sp=r&sv=2026-02-06&sr=b&scid=f820350b-5ac9-571b-9cb8-803baa0eac12&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-13T00%3A42%3A53Z&ske=2026-10-14T00%3A42%3A53Z&sks=b&skv=2026-02-06&sig=6agQmz8WktHYhb2jGWdgJIouEd99YWdWl7kwZiSSmWc%3D'
if($LASTEXITCODE-ne 0){throw 'download failed'}
if((Get-FileHash $o -Algorithm SHA256).Hash.ToLowerInvariant()-ne'd31e3b3dda04dbba7b1aa79242200a04b26685056bcefe40270740b2e192f529'){throw 'artifact 01 hash failed'}
if(Test-Path $d){Remove-Item -Recurse -Force $d}
Expand-Archive $o $d -Force
$i=Get-ChildItem $d -Recurse -File|Where-Object{$_.Name-like'*.part-01'}|Select-Object -First 1
if(-not $i){throw 'part 01 missing'};$parts+=$i.FullName
$o=Join-Path $base 'artifact-02.zip';$d=Join-Path $base 'artifact-02'
Write-Host 'Downloading verified part 02/04 ...'
& curl.exe -L --fail --retry 3 --retry-delay 2 -o $o 'https://sdmntprkoreacentral.oaiusercontent.com/files/00000000-a3b8-8206-9bee-1de9d5597178/raw?se=2026-10-13T05%3A35%3A45Z&sp=r&sv=2026-02-06&sr=b&scid=73b9cd3a-6b29-5fcb-a685-537fd24bf673&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-13T00%3A15%3A57Z&ske=2026-10-14T00%3A15%3A57Z&sks=b&skv=2026-02-06&sig=vbHOrJ8tZIzIJszKogWPMSoP0stvc6%2BEk0qqQpf33rI%3D'
if($LASTEXITCODE-ne 0){throw 'download failed'}
if((Get-FileHash $o -Algorithm SHA256).Hash.ToLowerInvariant()-ne'62e7f4704d20d6bb048f5f9e1593c1084771407b9ea707ac4d51598929c599c4'){throw 'artifact 02 hash failed'}
if(Test-Path $d){Remove-Item -Recurse -Force $d}
Expand-Archive $o $d -Force
$i=Get-ChildItem $d -Recurse -File|Where-Object{$_.Name-like'*.part-02'}|Select-Object -First 1
if(-not $i){throw 'part 02 missing'};$parts+=$i.FullName
$o=Join-Path $base 'artifact-03.zip';$d=Join-Path $base 'artifact-03'
Write-Host 'Downloading verified part 03/04 ...'
& curl.exe -L --fail --retry 3 --retry-delay 2 -o $o 'https://sdmntprkoreacentral.oaiusercontent.com/files/00000000-9f28-8206-9511-7fe493bed624/raw?se=2026-10-13T05%3A36%3A23Z&sp=r&sv=2026-02-06&sr=b&scid=473837ab-3b00-5c81-af10-0c354264f060&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-12T23%3A54%3A37Z&ske=2026-10-13T23%3A54%3A37Z&sks=b&skv=2026-02-06&sig=6H606a9ajWGgW/gterbV9fS3vLn/4l/6L8zlqNF3pL0%3D'
if($LASTEXITCODE-ne 0){throw 'download failed'}
if((Get-FileHash $o -Algorithm SHA256).Hash.ToLowerInvariant()-ne'9a32c5d9c83176f9661ed61ebb5bdf7c01c348250dd44c637365efb4e6dd8312'){throw 'artifact 03 hash failed'}
if(Test-Path $d){Remove-Item -Recurse -Force $d}
Expand-Archive $o $d -Force
$i=Get-ChildItem $d -Recurse -File|Where-Object{$_.Name-like'*.part-03'}|Select-Object -First 1
if(-not $i){throw 'part 03 missing'};$parts+=$i.FullName
$o=Join-Path $base 'artifact-04.zip';$d=Join-Path $base 'artifact-04'
Write-Host 'Downloading verified part 04/04 ...'
& curl.exe -L --fail --retry 3 --retry-delay 2 -o $o 'https://sdmntprjapaneast.oaiusercontent.com/files/00000000-fd70-8209-97a3-bb074b444d11/raw?se=2026-10-13T05%3A36%3A52Z&sp=r&sv=2026-02-06&sr=b&scid=1e912aad-035a-5b2b-8dcd-7ffd39e4423b&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-13T00%3A06%3A46Z&ske=2026-10-14T00%3A06%3A46Z&sks=b&skv=2026-02-06&sig=5hKmRJPJwpzh7hg0NubQicaI%2B5Ng3nCiL4WsfcVe7fo%3D'
if($LASTEXITCODE-ne 0){throw 'download failed'}
if((Get-FileHash $o -Algorithm SHA256).Hash.ToLowerInvariant()-ne'39ae66ad4f3a9317d9eecbd28375ef99b02cf061a00e6b2122fc320ca9f743f1'){throw 'artifact 04 hash failed'}
if(Test-Path $d){Remove-Item -Recurse -Force $d}
Expand-Archive $o $d -Force
$i=Get-ChildItem $d -Recurse -File|Where-Object{$_.Name-like'*.part-04'}|Select-Object -First 1
if(-not $i){throw 'part 04 missing'};$parts+=$i.FullName
$z=Join-Path $base 'MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip'
$out=[IO.File]::Open($z,[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::None);try{foreach($p in $parts){$x=[IO.File]::OpenRead($p);try{$x.CopyTo($out)}finally{$x.Dispose()}}}finally{$out.Dispose()}
if((Get-FileHash $z -Algorithm SHA256).Hash.ToLowerInvariant()-ne'7136c1512001b371cce86883b0f63a2373d4a77c720ec31d926001dc3d344061'){throw 'final package hash failed'}
try{Expand-Archive $z $base -Force}catch{& tar.exe -xf $z -C $base;if($LASTEXITCODE-ne 0){throw}}
$exe=Get-ChildItem $base -Recurse -Filter 'MINDLE_MEDIA_AI_RUN.exe' -File|Select-Object -First 1
if(-not $exe){throw 'MINDLE_MEDIA_AI_RUN.exe missing'}
Start-Process $exe.FullName -WorkingDirectory $exe.DirectoryName
Write-Host 'PASS: MINDLE MEDIA AI launcher started' -ForegroundColor Green
