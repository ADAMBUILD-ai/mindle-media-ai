@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0FINAL_EMPLOYEE_PACKAGE_HOST_GATE.ps1"
set "RESULT=%errorlevel%"
pause
exit /b %RESULT%
