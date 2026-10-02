# MINDLE MEDIA AI — FINAL WINDOWS LAUNCHER + BRAND ICON + PRODUCT CLOSEOUT DIRECTIVE v20.2.4

Date: 2026-10-02
Status: ACTIVE — FINAL PRODUCT CLOSEOUT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.4

## 0. Commander ruling

The current v20.2.2 worker-opened UI is accepted as the visual baseline.

Representative confirms the remaining visible problem is the desktop launcher/icon experience:

1. the desktop-launched screen must match the current good worker-opened screen
2. the current desktop icon is visually unacceptable because it is essentially a plain white/default file icon
3. the final MEDIA AI product must have a recognizable branded app icon

This cycle supersedes unexecuted v20.2.3 and completes both:
- Windows launcher parity
- final MEDIA AI brand icon

Do NOT redesign the good UI.

## 1. Frozen product baseline

Freeze:
- current VIDEO left/center/right geometry
- current PHOTO left/center/right geometry
- F27E dark navy / cyan / blue / violet / pink visual hierarchy
- Shortform additive button
- VIDEO action order:
  영상 불러오기 → AI 자동 편집 → 광고 숏폼 → 프로젝트 저장 → 내보내기
- v20.1 live Shortform MP4 PASS
- current runtime/model/Marketing integrations

Any UI geometry change outside launcher/cache parity is forbidden.

## 2. Phase A — repair Windows launcher parity

Before icon styling, ensure the desktop launcher opens the exact same current UI.

Inspect the existing desktop shortcut:
- filename
- type
- TargetPath
- Arguments
- WorkingDirectory
- URL/query
- icon location
- browser executable
- window state

Compare against the worker-opened good UI:
- repository root
- branch
- HEAD
- server process
- port
- static root
- browser viewport
- browser zoom
- CSS/JS identity

Do not assume the current shortcut is correct.

## 3. Canonical launcher

Create repository-owned:

scripts/launch_media_ai_windows.ps1

Responsibilities:
- resolve repository root from its own location
- verify canonical branch/worktree
- start/reuse only the correct MEDIA AI server
- use port 8768
- verify correct server identity before reuse
- open the current UI with a cache-busting value derived from current Git HEAD
- open browser maximized
- never use a historical hard-coded ui_refresh value
- never point to an old worktree
- inherit secure runtime ENV only
- never persist secrets
- leave server running

Canonical URL pattern:

http://127.0.0.1:8768/?ui_build=<CURRENT_SHORT_HEAD>

## 4. Local UI cache policy

For localhost UI static responses, ensure fresh UI assets.

Apply where appropriate:

Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Expires: 0

Scope this to the local UI development surface:
- index.html
- CSS
- JS
- UI static assets where stale UI would cause visual mismatch

Do not change model/output caching unless needed.

## 5. Desktop shortcut

Replace/update the existing desktop shortcut:

Name:
MINDLE MEDIA AI - 최종 UI

The shortcut must point to the canonical launcher, not directly to a stale localhost URL.

After replacement:
- close current browser
- double-click desktop shortcut
- verify current good UI opens
- verify maximized window
- verify no bottom clipping
- verify current VIDEO/PHOTO UI matches worker-opened state

## 6. Phase B — final branded MEDIA AI icon

The current plain white/default file icon is NOT acceptable.

Create a dedicated original MINDLE MEDIA AI application icon.

### Required visual direction

Background:
- dark navy / near-black rounded-square app tile

Primary mark:
- a clear media symbol combining:
  - VIDEO play triangle
  - PHOTO/image frame or landscape shape
  - one small AI sparkle/star accent

Color:
- electric blue
- cyan
- violet
- optional restrained magenta/pink accent

Style:
- modern
- professional
- B2B
- clean
- recognizable at small Windows sizes
- consistent with the approved MEDIA AI UI

The icon should visually communicate:
MEDIA + PHOTO + VIDEO + AI

### Forbidden

- plain white document/page icon
- generic folder
- generic browser icon
- stock icon
- third-party logo
- copied application logo
- excessive detail that disappears at 16/32 px
- tiny text as the primary mark

Text "MINDLE MEDIA AI" may appear only in large preview artwork if useful.
Do NOT rely on tiny text inside the actual icon.

## 7. Icon construction rule

Use vector-like clean shapes.

Recommended composition:

- rounded dark navy square
- center: cyan/blue outlined image-frame shape
- overlay: violet/blue play triangle
- upper-right or lower-right: small AI sparkle
- subtle blue-to-violet glow
- optional small magenta accent line

The final icon must have strong silhouette recognition at 32×32.

## 8. Production asset set

Create:

ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_1024.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_512.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_256.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_128.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_64.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_48.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_32.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_16.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico

ICO must include the normal Windows size set, including:
16 / 32 / 48 / 64 / 128 / 256 where supported.

No white default page glyph may remain.

## 9. Apply icon

Apply the final icon to:

1. Windows desktop shortcut
2. browser favicon / local product tab
3. any real repository-owned launcher surface that supports an icon

Do NOT create a fake EXE.

If product remains a local web application:
- desktop shortcut launches PowerShell canonical launcher
- shortcut uses the final ICO
- favicon uses final branded icon assets
- actual product remains browser/local-web based

## 10. Small-size icon QA

Verify icon at:
- 256×256
- 128×128
- 64×64
- 48×48
- 32×32
- 16×16

Check:
- main symbol still identifiable
- blue/cyan/violet distinction remains visible
- sparkle does not become noise
- no transparent-edge artifacts
- no white square/page fallback
- Windows shortcut displays the actual ICO

If the icon becomes unreadable at 16/32:
simplify the mark and regenerate within this cycle.

## 11. Final launcher + icon double-click test

Mandatory test:

1. close all MEDIA AI browser windows
2. ensure no stale browser session is being reused
3. double-click ONLY:
   MINDLE MEDIA AI - 최종 UI
4. verify:
   - branded icon visible on desktop
   - canonical launcher runs
   - correct current server starts/reuses
   - correct current HEAD opens
   - browser opens maximized
   - current good UI appears
   - no lower clipping
   - 광고 숏폼 button present
   - VIDEO/PHOTO left/center/right remain current baseline
5. close and repeat once

Both launches must match.

## 12. Functional smoke check after icon launch

From the icon-launched UI verify:
- VIDEO load
- AI 자동 편집
- 광고 숏폼 mode
- VIDEO natural-language field
- VIDEO reference input
- Timeline visible
- PHOTO load
- PHOTO natural-language field
- PHOTO reference input
- Save
- Export

This is a smoke check only.
Do not reopen model/runtime development.

## 13. Final visual Evidence

Capture actual Windows screenshots:

A. desktop before icon replacement
B. desktop after branded icon replacement
C. icon 1024 preview
D. icon multi-size comparison
E. desktop icon selected/highlighted
F. icon double-click launched full MEDIA AI UI
G. second-launch parity screenshot
H. favicon/tab icon visible where possible

The final screenshot must visibly prove:
- branded icon
- current UI
- no lower clipping

## 14. Final product status

If all passes:

RESULT =
FINAL_CLOSEOUT_READY_FOR_COMMANDER

This means:
- base MEDIA AI PASS
- Shortform live MP4 PASS except approved TTS voiceover dependency
- final UI baseline preserved
- desktop launcher parity PASS
- branded app icon applied
- double-click launch PASS
- no stale shortcut/cache issue
- remote Evidence PASS

The separate voiceover/TTS dependency remains documented and does not invalidate launcher/icon closeout.

## 15. Exact Evidence

Human Review:
docs/commander/MINDLE_MEDIA_AI_FINAL_WINDOWS_LAUNCHER_BRAND_ICON_CLOSEOUT_REVIEW_v20.2.4_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FINAL_WINDOWS_LAUNCHER_BRAND_ICON_CLOSEOUT_EVIDENCE_v20_2_4_20261002.json

Detail directory:
evidence/pc_remote/media-ai-final-launcher-icon-v20_2_4-20261002/

Required files:

1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. DESKTOP_SHORTCUT_BEFORE.json
4. LAUNCH_PARITY_ROOT_CAUSE.json
5. CANONICAL_LAUNCHER_VERIFY.json
6. SERVER_CACHE_POLICY_VERIFY.json
7. DESKTOP_SHORTCUT_AFTER.json
8. ICON_DESIGN_SPEC.json
9. ICON_ASSET_HASHES.json
10. ICON_MULTI_SIZE_QA.json
11. DESKTOP_BEFORE.png
12. DESKTOP_AFTER_BRANDED_ICON.png
13. ICON_FINAL_1024_PREVIEW.png
14. ICON_MULTI_SIZE_PREVIEW.png
15. DESKTOP_ICON_SELECTED.png
16. ICON_LAUNCH_UI_FIRST.png
17. ICON_LAUNCH_UI_SECOND.png
18. LAUNCH_VIEWPORT_PARITY.json
19. BOTTOM_CLIPPING_AUDIT.json
20. FAVICON_VERIFY.json
21. FUNCTION_SMOKE_CHECK.json
22. V20_2_2_UI_PRESERVATION.json
23. SHORTFORM_PRESERVATION.json
24. REGRESSION_TEST_RESULTS.txt
25. OUTPUT_HASHES.sha256
26. REMOTE_PUSH_VERIFY.txt

All PNG/ICO/product icon files must be non-zero and decodable.

## 16. Regression

Run:
python scripts/validate_pc_work_control_plane.py

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve:
- current good UI
- F27E base + Shortform Addendum
- v20.1 MP4
- model identities
- Save/Export behavior

## 17. Failure rules

LAUNCHER_CORRECTION_REQUIRED:
desktop shortcut still opens stale/different UI.

ICON_CORRECTION_REQUIRED:
icon remains generic/plain, unreadable at small sizes, or fails Windows application.

FAIL:
current UI regresses, shortcut does not launch, Evidence incomplete, or wrong branch/root is used.

## Final governing sentence

KEEP THE CURRENT GOOD UI. REPAIR THE DESKTOP LAUNCH PATH SO IT OPENS THAT EXACT UI EVERY TIME, THEN REPLACE THE PLAIN WHITE FILE ICON WITH A REAL MINDLE MEDIA AI BRAND ICON USING DARK NAVY + BLUE/CYAN + VIOLET MEDIA/PHOTO/VIDEO/AI SYMBOLS. APPLY IT TO THE WINDOWS SHORTCUT AND FAVICON, DOUBLE-CLICK TEST TWICE, CAPTURE THE REAL WINDOWS RESULT, AND CLOSE THE PRODUCT ONLY WHEN THE BRANDED ICON AND CURRENT UI BOTH WORK TOGETHER.
