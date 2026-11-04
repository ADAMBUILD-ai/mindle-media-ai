@echo off
setlocal EnableExtensions
chcp 65001 >nul
title MINDLE MEDIA AI FINAL ONE CLICK
set "BASE=%USERPROFILE%\Downloads\MINDLE_MEDIA_AI_FINAL"
if not exist "%BASE%" mkdir "%BASE%"
echo MINDLE MEDIA AI final verified launcher
echo First run downloads about 2GB and may take several minutes.
echo.
echo Downloading part 00/04...
curl.exe -L --fail --retry 3 --retry-delay 2 "https://sdmntprjapaneast.oaiusercontent.com/files/00000000-9fa4-8209-8a9e-76efe50d0da9/raw?se=2026-10-13T07%3A21%3A21Z&sp=r&sv=2026-02-06&sr=b&scid=e6cf8197-af71-5c02-a9b0-7e5eb54ecebc&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-13T00%3A10%3A57Z&ske=2026-10-14T00%3A10%3A57Z&sks=b&skv=2026-02-06&sig=WFm1QReYgjxpQJaKO6ygsq4cIZAMiP%2BlIblhkPibSk0%3D" -o "%BASE%\artifact-00.zip"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$h=(Get-FileHash -LiteralPath '%BASE%\artifact-00.zip' -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne '2081322d5186538b18d52b977be6c5881a2055d4abb2be22d98485ee58f3c988'){exit 2}"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$d='%BASE%\artifact-00'; if(Test-Path $d){Remove-Item -Recurse -Force $d}; Expand-Archive -LiteralPath '%BASE%\artifact-00.zip' -DestinationPath $d -Force"
if errorlevel 1 goto :fail
echo Downloading part 01/04...
curl.exe -L --fail --retry 3 --retry-delay 2 "https://sdmntprjapaneast.oaiusercontent.com/files/00000000-184c-8209-86ac-01f8958a5e91/raw?se=2026-10-13T07%3A21%3A42Z&sp=r&sv=2026-02-06&sr=b&scid=fd3db3f9-0f75-56be-909f-2f0b969cced9&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-12T23%3A41%3A38Z&ske=2026-10-13T23%3A41%3A38Z&sks=b&skv=2026-02-06&sig=MfrnMu2FJAudsIeqzDgB6jutn45JD6FTG38P2u6lAgs%3D" -o "%BASE%\artifact-01.zip"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$h=(Get-FileHash -LiteralPath '%BASE%\artifact-01.zip' -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne 'd31e3b3dda04dbba7b1aa79242200a04b26685056bcefe40270740b2e192f529'){exit 2}"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$d='%BASE%\artifact-01'; if(Test-Path $d){Remove-Item -Recurse -Force $d}; Expand-Archive -LiteralPath '%BASE%\artifact-01.zip' -DestinationPath $d -Force"
if errorlevel 1 goto :fail
echo Downloading part 02/04...
curl.exe -L --fail --retry 3 --retry-delay 2 "https://sdmntprindiasocentral.oaiusercontent.com/files/00000000-59f8-8211-8df1-8a80c82c887c/raw?se=2026-10-13T07%3A21%3A40Z&sp=r&sv=2026-02-06&sr=b&scid=b029d191-768e-5e39-b752-8994af859a2c&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-12T22%3A57%3A51Z&ske=2026-10-13T22%3A57%3A51Z&sks=b&skv=2026-02-06&sig=Fhv6TuXMHE8CNd5JgXF%2BHM9LOBuUp/yNLl4Zs7VmnYc%3D" -o "%BASE%\artifact-02.zip"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$h=(Get-FileHash -LiteralPath '%BASE%\artifact-02.zip' -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne '62e7f4704d20d6bb048f5f9e1593c1084771407b9ea707ac4d51598929c599c4'){exit 2}"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$d='%BASE%\artifact-02'; if(Test-Path $d){Remove-Item -Recurse -Force $d}; Expand-Archive -LiteralPath '%BASE%\artifact-02.zip' -DestinationPath $d -Force"
if errorlevel 1 goto :fail
echo Downloading part 03/04...
curl.exe -L --fail --retry 3 --retry-delay 2 "https://sdmntprnorthcentralus.oaiusercontent.com/files/00000000-d910-822f-9d4a-2327803cbf70/raw?se=2026-10-13T07%3A21%3A56Z&sp=r&sv=2026-02-06&sr=b&scid=336aadd9-1dcc-5037-946d-8f2ecf3ae0fd&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-12T23%3A41%3A43Z&ske=2026-10-13T23%3A41%3A43Z&sks=b&skv=2026-02-06&sig=GD7SUilpHHcpfpFwGaz3rWQQSb2PwF97CfCpJV%2BVRQE%3D" -o "%BASE%\artifact-03.zip"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$h=(Get-FileHash -LiteralPath '%BASE%\artifact-03.zip' -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne '9a32c5d9c83176f9661ed61ebb5bdf7c01c348250dd44c637365efb4e6dd8312'){exit 2}"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$d='%BASE%\artifact-03'; if(Test-Path $d){Remove-Item -Recurse -Force $d}; Expand-Archive -LiteralPath '%BASE%\artifact-03.zip' -DestinationPath $d -Force"
if errorlevel 1 goto :fail
echo Downloading part 04/04...
curl.exe -L --fail --retry 3 --retry-delay 2 "https://sdmntprjapaneast.oaiusercontent.com/files/00000000-e370-8209-a506-7796399e997c/raw?se=2026-10-13T07%3A21%3A07Z&sp=r&sv=2026-02-06&sr=b&scid=69e5a3b0-1786-5566-bbf0-3f62322914f9&skoid=fe2e0858-51c5-47e9-acb7-46ebb9a0f396&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-10-13T00%3A14%3A51Z&ske=2026-10-14T00%3A14%3A51Z&sks=b&skv=2026-02-06&sig=5wf6h/WBJtbTxe5B96LRszgZ0YvbxC/5KaI8LGh5qwM%3D" -o "%BASE%\artifact-04.zip"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$h=(Get-FileHash -LiteralPath '%BASE%\artifact-04.zip' -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne '39ae66ad4f3a9317d9eecbd28375ef99b02cf061a00e6b2122fc320ca9f743f1'){exit 2}"
if errorlevel 1 goto :fail
powershell.exe -NoProfile -Command "$d='%BASE%\artifact-04'; if(Test-Path $d){Remove-Item -Recurse -Force $d}; Expand-Archive -LiteralPath '%BASE%\artifact-04.zip' -DestinationPath $d -Force"
if errorlevel 1 goto :fail
echo Assembling final package...
powershell.exe -NoProfile -Command "$dirs=0..4|%%{Join-Path '%BASE%' ('artifact-{0:D2}' -f $_)}; $parts=@(); for($n=0;$n -lt 5;$n++){ $p=Get-ChildItem $dirs[$n] -Recurse -File|?{$_.Name -like ('*.part-{0:D2}' -f $n)}|select -First 1; if(-not $p){exit 3}; $parts+=$p.FullName }; $z=Join-Path '%BASE%' 'MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip'; $o=[IO.File]::Open($z,[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::None); try{foreach($p in $parts){$x=[IO.File]::OpenRead($p);try{$x.CopyTo($o)}finally{$x.Dispose()}}}finally{$o.Dispose()}; $h=(Get-FileHash $z -Algorithm SHA256).Hash.ToLowerInvariant(); if($h -ne '7136c1512001b371cce86883b0f63a2373d4a77c720ec31d926001dc3d344061'){exit 4}"
if errorlevel 1 goto :fail
echo Extracting...
powershell.exe -NoProfile -Command "Expand-Archive -LiteralPath '%BASE%\MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip' -DestinationPath '%BASE%' -Force"
if errorlevel 1 (
  tar.exe -xf "%BASE%\MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip" -C "%BASE%"
  if errorlevel 1 goto :fail
)
for /r "%BASE%" %%F in (MINDLE_MEDIA_AI_RUN.exe) do (
  echo Launching MINDLE MEDIA AI...
  start "" "%%F"
  exit /b 0
)
:fail
echo.
echo FAILED - keep this window open and report the error shown above.
pause
exit /b 1
