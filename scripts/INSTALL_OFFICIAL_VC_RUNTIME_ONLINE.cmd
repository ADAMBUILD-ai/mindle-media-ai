@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL_OFFICIAL_VC_RUNTIME_ONLINE.ps1"
set "RESULT=%errorlevel%"
pause
exit /b %RESULT%
