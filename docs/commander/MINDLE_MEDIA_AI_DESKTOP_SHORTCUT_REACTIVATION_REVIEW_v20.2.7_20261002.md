# MINDLE MEDIA AI desktop shortcut reactivation review

## Result

Recreated `C:\Users\PC\OneDrive\Desktop\MINDLE MEDIA AI - 최종 UI.lnk` from the current repository root.

- TargetPath: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
- Arguments: `-ExecutionPolicy Bypass -File <current-repository>\scripts\launch_media_ai_windows.ps1`
- WorkingDirectory: current repository root
- IconLocation: current repository `ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico,0`
- Old `.url` shortcut removed
- No UI/CSS/layout/icon design files changed
- Actual shortcut launch verified through the runtime identity endpoint
- Launcher opens a new maximized browser window (`--new-window --start-maximized`) so an existing Edge session cannot hide the result
- Runtime branch: `feature/ad-shortform-bridge-p0-20260926`
- Runtime HEAD: `213080d7a5672dcc9a56101ce85b47348c355139`

## Evidence limitation

Native desktop screenshot capture is unavailable in this host. Shortcut metadata and runtime identity were verified; no screenshot was fabricated.
