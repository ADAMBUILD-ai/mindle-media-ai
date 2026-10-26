@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0accept_r3_on_owner_pc.ps1"
if errorlevel 1 (
  echo.
  echo R3 PC acceptance failed. Keep this window and the Desktop evidence folder.
)
pause
