@echo off
chcp 65001 >nul
title MINDLE MEDIA AI FINAL
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0MINDLE_MEDIA_AI_FINAL_RUN.ps1"
if errorlevel 1 (echo FAILED & pause & exit /b 1)
