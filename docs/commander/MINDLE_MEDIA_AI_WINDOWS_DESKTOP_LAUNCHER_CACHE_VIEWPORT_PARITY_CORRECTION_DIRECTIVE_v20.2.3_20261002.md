# MINDLE MEDIA AI — WINDOWS DESKTOP LAUNCHER / CACHE / VIEWPORT PARITY CORRECTION DIRECTIVE v20.2.3

Date: 2026-10-02
Status: ACTIVE — LAUNCH PATH PARITY FIX
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.3

## 0. Commander ruling

Representative reports:

A. Current worker-opened live UI:
- visually correct
- current v20.2.2 left-panel correction is visible
- no major bottom clipping defect

B. Existing Windows desktop icon/shortcut:
- opens MEDIA AI with a different/clipped lower layout
- bottom area appears cut / stale
- behavior differs from the current worker-opened UI

This means the remaining problem is NOT the approved UI geometry itself.

Primary diagnosis:
LAUNCH_PATH_PARITY_DEFECT

The desktop launcher/shortcut is likely not reproducing the same:
- URL
- current static root
- current server process
- cache state
- viewport/window state

Do NOT redesign the UI again.

## 1. HARD FREEZE — current good UI

Freeze the current v20.2.2 UI as the visual baseline for this launcher repair.

Do NOT change:
- VIDEO left/center/right geometry
- PHOTO left/center/right geometry
- color hierarchy
- F27E visual layout
- Shortform button/order
- functional UI controls
- Marketing / MP4 / model/runtime code

Allowed UI-server changes are ONLY those required to guarantee fresh current assets and launcher parity.

## 2. Evidence from representative screenshots

Current correct worker-opened URL visibly uses a fresh UI refresh route similar to:

http://127.0.0.1:8768/?ui_refresh=20261002-left-panel-v2022

Earlier desktop-icon launch visibly used an older UI refresh route similar to:

http://127.0.0.1:8768/?ui_refresh=20261002-photo-final

This must be treated as a possible stale-launch/caching signal.

Do not assume this alone is the root cause.
Verify the actual Windows shortcut target and running server identity.

## 3. Mandatory desktop shortcut forensic check

Inspect the actual representative desktop shortcut/icon used to launch MEDIA AI.

Record WITHOUT changing it first:

- shortcut filename
- shortcut type: .lnk / .url / other
- shortcut TargetPath
- shortcut Arguments
- shortcut WorkingDirectory / Start In
- shortcut icon path
- browser executable, if direct browser shortcut
- URL being opened
- whether old ui_refresh query is hard-coded
- whether it starts the server or only opens a browser
- whether it points to an old worktree/folder
- whether it points to an old port
- whether it opens app mode or standard browser mode
- whether browser window opens maximized/restored/small

Evidence:
DESKTOP_SHORTCUT_BEFORE.json

Never record secrets.

## 4. Verify server identity for BOTH launch paths

Before repair, compare:

### Worker-opened good path
Record:
- process PID
- Python executable
- repository root
- branch
- HEAD
- product server command
- static root
- port
- exact URL
- browser executable
- viewport innerWidth/innerHeight
- devicePixelRatio
- browser zoom if detectable
- CSS resource identity

### Desktop-icon bad path
Record the same fields.

Required Evidence:
WORKER_LAUNCH_IDENTITY.json
DESKTOP_ICON_LAUNCH_IDENTITY.json
LAUNCH_PARITY_DIFF.json

The diff must explicitly identify all mismatches.

## 5. Browser cache diagnosis

Current product_server.py static responses do not explicitly send a no-store cache policy for UI HTML/CSS/JS.

Verify whether the desktop icon path is loading stale:
- index.html
- approved_visual.css
- interaction.css
- interaction.js
- product_integration.js

Check:
- response headers
- browser network/cache behavior where possible
- current file SHA vs served content identity
- hard refresh result
- Incognito/new profile only as a diagnostic, not as the final workaround

If stale cache is confirmed OR cannot be reliably excluded, implement robust local-development cache protection.

Preferred product-server behavior for localhost UI static assets:

Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Expires: 0

Apply to local UI HTML/CSS/JS/static development surface only.
Do not alter model/output file caching behavior unless needed.

The launcher must not depend on manually pressing Ctrl+F5.

## 6. Canonical Windows launcher

Create ONE canonical Windows launcher owned by the repository.

Preferred path:

scripts/launch_media_ai_windows.ps1

Responsibilities:

1. resolve repository root from the script location, not a hard-coded user folder
2. verify canonical branch/worktree identity
3. start the MEDIA AI server from the current repository root if not already running
4. if port 8768 is occupied:
   - verify whether the process is the correct MEDIA AI server
   - reuse only if identity matches
   - otherwise terminate/restart only the stale MEDIA AI local process, not unrelated processes
5. wait until the current UI is reachable
6. generate/open a canonical URL using the CURRENT Git HEAD as cache-busting identity, e.g.
   http://127.0.0.1:8768/?ui_build=<CURRENT_SHORT_HEAD>
7. open the browser in a maximized usable window
8. do not hard-code old ui_refresh tags
9. do not hard-code obsolete worktree paths
10. leave the server process alive

Do not print secrets.

If HF_TOKEN is required:
- inherit it from the existing secure user/process environment
- never write it into the launcher
- if absent, report the exact gate rather than persisting a token

## 7. Browser/window parity

The desktop icon must open the same visual state as the current good worker-opened UI.

Required final behavior:
- browser starts maximized OR explicitly restores a known maximized state
- viewport must be large enough that current v20.2.2 layout is not forced into an unintended compact/clipped geometry
- browser zoom must be 100% unless representative explicitly set another value
- Windows taskbar must not hide the bottom content because of a forced fixed window size
- launcher must not use a hard-coded pixel window size smaller than the current correct UI

If a browser command is used:
- detect installed Edge/Chrome path safely
- prefer the representative's current default/known browser when practical
- use a maximized launch strategy
- do not use kiosk mode
- do not hide browser controls unless the final approved launcher intentionally requires app mode

## 8. Desktop shortcut replacement

After canonical launcher is verified:

Replace/update the representative's desktop MEDIA AI shortcut so it points ONLY to the canonical launcher.

Recommended:
Target:
PowerShell executable

Arguments:
-ExecutionPolicy Bypass -File "<repo-resolved or stable launcher path>"

Working directory:
repository root or stable launcher directory

Do NOT point the desktop shortcut directly to:
- old ui_refresh URL
- old browser tab/session
- historical worker folder
- stale worktree
- raw localhost URL without server/bootstrap logic

Use the current icon only as a temporary shortcut icon if one already exists.

The final icon-design phase remains blocked until representative UI approval.
Do not create new icon candidates in this cycle.

## 9. Same-screen parity test

Run both launch methods after repair:

A. repository canonical launcher directly
B. Windows desktop icon/shortcut

They must resolve to:
- same server identity
- same branch
- same HEAD
- same static root
- same CSS/JS identity
- equivalent maximized viewport
- same UI geometry
- same visible lower VIDEO/PHOTO content

Capture:
CANONICAL_LAUNCH_AFTER.png
DESKTOP_ICON_LAUNCH_AFTER.png
PARITY_SIDE_BY_SIDE.png

The representative must be able to see that both are visually the same.

## 10. Bottom clipping hard gate

Specifically verify:

VIDEO:
- full left command card visible
- Timeline lower edge visible
- right panel lower controls visible

PHOTO:
- full left command/reference/chips area visible
- center Preview + lower transport visible
- right panel lower actions visible

At 100% browser zoom and maximized normal Windows view:
NO required control may be clipped by the viewport bottom.

If scrolling is part of the approved full product page:
- it must be intentional
- scroll position 0 must not create the false impression that UI is cut
- representative must be able to reach the full PHOTO section normally

Do not solve clipping by shrinking all UI text/controls again.

## 11. Regression protection

Run:
python scripts/validate_pc_work_control_plane.py

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve v20.2.2 UI.

No geometry redesign in this cycle.

## 12. Required Evidence

Human Review:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_REVIEW_v20.2.3_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_EVIDENCE_v20_2_3_20261002.json

Detail:
evidence/pc_remote/media-ai-launcher-parity-v20_2_3-20261002/

Required files:
1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. DESKTOP_SHORTCUT_BEFORE.json
4. WORKER_LAUNCH_IDENTITY.json
5. DESKTOP_ICON_LAUNCH_IDENTITY.json
6. LAUNCH_PARITY_DIFF.json
7. CACHE_DIAGNOSIS.json
8. SERVER_STATIC_CACHE_POLICY.json
9. CANONICAL_LAUNCHER_VERIFY.json
10. DESKTOP_SHORTCUT_AFTER.json
11. CANONICAL_LAUNCH_AFTER.png
12. DESKTOP_ICON_LAUNCH_AFTER.png
13. PARITY_SIDE_BY_SIDE.png
14. VIEWPORT_PARITY.json
15. BOTTOM_CLIPPING_AUDIT.json
16. V20_2_2_UI_PRESERVATION.json
17. SHORTFORM_PRESERVATION.json
18. REGRESSION_TEST_RESULTS.txt
19. OUTPUT_HASHES.sha256
20. REMOTE_PUSH_VERIFY.txt

## 13. Pass condition

LAUNCHER_PARITY_READY_FOR_REPRESENTATIVE:
- canonical launcher and desktop icon resolve to same current server/root/HEAD
- stale old ui_refresh/old path removed
- fresh UI assets guaranteed
- desktop icon opens maximized usable UI
- no bottom clipping difference
- current v20.2.2 UI remains unchanged
- desktop icon and direct worker launch are visually equivalent
- screenshots/Evidence published
- repaired desktop icon remains available for representative click test

LAUNCHER_PARITY_CORRECTION_REQUIRED:
- shortcut still resolves differently
- stale cache/path persists
- bottom clipping remains
- launcher opens smaller/restored geometry
- current UI was unnecessarily redesigned

## 14. Representative click test

After repair, leave the desktop icon visible.

Ask the representative to close the current browser and launch MEDIA AI by DOUBLE-CLICKING ONLY the desktop icon.

Required question:

"신작가님, 지금 바탕화면 MEDIA AI 아이콘으로 다시 연 화면이 작업 중 정상 화면과 똑같이 나오고, 하단 잘림도 없어졌습니까?"

Do not claim final UI approval until this click test succeeds.

## 15. Icon design phase

Still blocked.

ICON PHASE = BLOCKED_PENDING_UI_AND_LAUNCHER_APPROVAL

The existing desktop icon is only the launcher under test.
Do not confuse it with the final approved application icon design.

## Final governing sentence

DO NOT REDESIGN THE GOOD UI. MAKE THE DESKTOP ICON LAUNCH THE EXACT SAME CURRENT SERVER, CURRENT HEAD, CURRENT STATIC ASSETS, FRESH CACHE STATE, AND MAXIMIZED VIEWPORT AS THE WORKER-OPENED GOOD UI. PROVE PARITY BY RUNNING BOTH PATHS SIDE-BY-SIDE, THEN LET THE REPRESENTATIVE CLICK THE DESKTOP ICON HIMSELF.
