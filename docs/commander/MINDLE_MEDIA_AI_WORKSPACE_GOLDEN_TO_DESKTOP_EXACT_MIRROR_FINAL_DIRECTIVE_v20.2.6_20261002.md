# MINDLE MEDIA AI — WORKSPACE GOLDEN UI RESTORE + DESKTOP EXACT-MIRROR FINAL CLOSEOUT DIRECTIVE v20.2.6

Date: 2026-10-02
Status: ACTIVE — FINAL WORKSPACE-FIRST CLOSEOUT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.6

## 0. Representative directive — highest priority

From this cycle forward there is ONLY ONE UI source:

THE CURRENT WORKING REPOSITORY FOLDER.

The Windows desktop is NOT a second UI build.
The desktop is NOT allowed to contain a separately edited UI.
The desktop shortcut must only launch the exact UI files from the working repository.

Workflow:

WORKSPACE UI
→ verify
→ desktop shortcut launches THAT SAME WORKSPACE
→ compare
→ closeout

No independent desktop tuning is allowed.

## 1. Exact known-good workspace UI baseline

The representative identified the workspace UI state before the later row-height clipping changes as the correct basis.

Authoritative geometry baseline commit:

97900cc6c784e74b4224333fa2cc84d29c611f87

Commit message:
fix: fill media left panels to row bottom

At this commit:
- VIDEO/PHOTO left panels had the desired left-panel fill correction
- VIDEO center was preserved from the accepted v20.2.1 state
- VIDEO right was preserved
- PHOTO center was preserved from the accepted v20.2.1 state
- PHOTO right was preserved
- colors were preserved
- Shortform order was preserved

This is the WORKSPACE UI GEOMETRY GOLDEN BASELINE.

## 2. Proven bad geometry change — DO NOT KEEP

The later commit:

2ab174e03dc786c53f38ba956dea95f8e1ccd5a7

introduced a forced row-height system including:
- fixed row heights
- max-height constraints
- min-height:0 overrides
- overflow:hidden on panels
- forced VIDEO grid fitting
- forced PHOTO grid fitting

This caused the representative-visible defect:
content being CUT to make the outer heights appear equal.

The v20.2.5 approach is REJECTED.

Do NOT preserve those clipping rules.

## 3. Workspace restore method — exact, not approximate

Restore UI geometry from the known-good commit.

For:

ui/approved_visual.css

The geometry/style source must be restored EXACTLY from:

97900cc6c784e74b4224333fa2cc84d29c611f87:ui/approved_visual.css

Preferred deterministic command concept:

git show 97900cc6c784e74b4224333fa2cc84d29c611f87:ui/approved_visual.css

and write those exact bytes into the current working tree.

Do NOT manually reconstruct the CSS from memory.
Do NOT selectively keep v20.2.5 clipping rules.
Do NOT add another height patch after restoring.

After restoration, prove the file SHA/content matches the 97900cc version.

Evidence:
WORKSPACE_GOLDEN_CSS_RESTORE.json

## 4. Preserve only later NON-GEOMETRY improvements

Keep these later improvements:

### A. Brand icon assets
Keep:
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.svg
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_1024.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_512.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_256.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_128.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_64.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_48.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_32.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_16.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico

### B. Favicon link
Keep the branded favicon link in ui/index.html.

Do NOT roll ui/index.html back in a way that removes:
- 광고 숏폼
- branded favicon
- current functional controls

### C. Local no-cache headers
Keep the localhost no-cache behavior in:
src/media_ai/product_server.py

### D. Canonical Windows launcher
Keep:
scripts/launch_media_ai_windows.ps1

but update it as required by this directive so it ALWAYS launches the current workspace source.

## 5. PHOTO center — explicit representative requirement

The representative specifically states:

The current workspace PHOTO CENTER was changed again and must return to the earlier correct appearance.

Therefore after restoring approved_visual.css from 97900cc:

Verify PHOTO CENTER matches the prior known-good state:

- large photo Preview occupies the center
- image/preview ratio matches the earlier accepted workspace state
- Preview is not vertically chopped
- bottom photo controls sit directly below the Preview
- center is not forcibly shortened to match left/right
- no overflow:hidden clipping of the photo Preview
- no new grid row sizing from v20.2.5
- the earlier v20.2.1/v20.2.2 photo-center behavior is restored

Use the representative’s earlier accepted workspace image as the visual check.

Do NOT touch PHOTO left/right to force them onto the center.
The objective is to RESTORE the known-good workspace UI, not invent a new equal-height system.

## 6. VIDEO — preserve known-good workspace behavior

After the CSS restore:

Verify VIDEO remains as in 97900cc:

- left panel uses full-height workflow
- center Preview / transport / Timeline are not clipped
- right editor panel remains intact
- no forced hidden overflow cuts the left or center content
- Shortform button remains present

Do NOT reintroduce v20.2.5 row-height clipping.

## 7. One source only — no desktop UI copy

Search the representative Windows machine for any old MEDIA AI UI copies used by the desktop shortcut.

Identify:
- copied ui folder
- exported UI folder
- old worktree
- historical local build
- stale HTML file
- direct .url file pointing to an old query
- shortcut targeting an old directory
- old launcher script outside the canonical repository

The final architecture must be:

Desktop shortcut
→ canonical launcher inside current working repository
→ product_server root = current working repository root
→ ui/ files served directly from current working repository

There must be NO:

Desktop shortcut
→ copied UI folder

and NO:

Desktop shortcut
→ historical worktree

and NO:

Desktop shortcut
→ old hard-coded HTML file

and NO:

Desktop shortcut
→ separately modified desktop CSS

Evidence:
DESKTOP_DUPLICATE_UI_AUDIT.json

## 8. Canonical workspace launcher — strengthen exact source guarantee

Update:

scripts/launch_media_ai_windows.ps1

so it explicitly proves the server is serving the SAME current working repository.

Requirements:

1. $RepoRoot resolved from $PSScriptRoot/..
2. branch must equal feature/ad-shortform-bridge-p0-20260926
3. compute current full HEAD
4. compute workspace UI fingerprint from at least:
   - ui/index.html
   - ui/approved_visual.css
   - ui/interaction.css
   - ui/interaction.js
   - ui/product_integration.js
5. start MEDIA AI server with:
   --root "$RepoRoot"
6. do NOT copy ui files anywhere
7. do NOT stage a separate desktop build
8. do NOT use a historical worktree
9. desktop shortcut points to this launcher only

## 9. Stale server prevention

Port 8768 may already have an older MEDIA AI server process.

Do NOT merely check:
HTTP 200

Before reusing an existing 8768 process, verify it serves the CURRENT workspace build identity.

Implement a local runtime identity mechanism.

Preferred:
GET /api/runtime-identity

Response contains no secrets and reports:
- repository root identifier/path
- branch
- current HEAD
- workspace UI fingerprint

If an existing 8768 server reports a different identity:
- stop ONLY that stale MEDIA AI process
- restart product_server from the current workspace

If identity endpoint is unavailable on an old process:
treat it as stale and restart only after confirming it is the MEDIA AI local process.

The desktop must never show an old process simply because port 8768 responds 200.

## 10. Workspace UI fingerprint

Create one deterministic fingerprint file:

evidence/pc_remote/media-ai-workspace-mirror-v20_2_6-20261002/WORKSPACE_UI_HASH_MANIFEST.json

Record SHA-256 for:

- ui/index.html
- ui/approved_visual.css
- ui/interaction.css
- ui/interaction.js
- ui/product_integration.js
- ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico

Also record:
- branch
- HEAD
- repo root
- golden geometry commit = 97900cc...

The server identity and desktop launcher must reference the same fingerprint.

## 11. Working-folder visual verification FIRST

Before touching the desktop shortcut:

Launch MEDIA AI directly from the current working folder.

Use:
- current product_server
- current workspace
- current restored CSS
- current browser at 100% zoom
- maximized normal Windows window

Verify visually:

### VIDEO
- no left clipping
- no center clipping
- Timeline complete
- right intact

### PHOTO
- photo center restored to the previous correct state
- left visible
- center visible
- right visible
- no content cut solely to enforce equal height

Capture:

WORKSPACE_FINAL_UI_TOP.png
WORKSPACE_FINAL_UI_PHOTO.png

This WORKSPACE view is the only visual truth.

If the workspace itself is not correct:
STOP.
Do NOT edit desktop behavior.
Fix only the workspace until correct.

## 12. Freeze workspace after it is correct

Once the workspace visual check passes:

Create:

WORKSPACE_UI_FINAL_LOCK.json

Record:
- branch
- HEAD
- UI file hashes
- approved_visual.css hash
- timestamp
- result = WORKSPACE_UI_LOCKED

From this moment until desktop parity completes:

NO UI CSS/HTML changes are allowed.

The desktop step may change ONLY:
- launcher script
- shortcut target/arguments
- stale process cleanup
- cache/open parameters

It must not modify UI files.

## 13. Desktop shortcut — pure mirror only

The desktop shortcut:

MINDLE MEDIA AI - 최종 UI

must point to the repository-owned launcher.

The shortcut must NOT have its own UI interpretation.

It may contain:
- PowerShell executable
- launcher script path
- final branded ICO

It may NOT contain:
- old ui_refresh query
- old HTML path
- copied UI directory
- separate CSS
- hard-coded old worktree

## 14. Desktop launch after workspace lock

After the workspace is locked:

1. close all MEDIA AI browser windows
2. stop/restart stale MEDIA AI server if identity mismatches
3. double-click ONLY the desktop shortcut
4. wait for canonical launcher
5. browser opens current workspace UI
6. browser 100% zoom
7. browser maximized
8. capture same sections:

DESKTOP_FINAL_UI_TOP.png
DESKTOP_FINAL_UI_PHOTO.png

## 15. Mandatory workspace-vs-desktop identity comparison

Compare workspace direct launch and desktop launch.

They MUST match:

- same RepoRoot
- same branch
- same HEAD
- same UI fingerprint
- same approved_visual.css SHA
- same index.html SHA
- same static asset hashes
- same port
- same viewport innerWidth/innerHeight
- same devicePixelRatio
- same browser zoom = 100%

Any mismatch:
FAIL.

Evidence:
WORKSPACE_VS_DESKTOP_IDENTITY.json

## 16. Mandatory visual comparison

Create:

WORKSPACE_VS_DESKTOP_TOP_COMPARISON.png
WORKSPACE_VS_DESKTOP_PHOTO_COMPARISON.png

The screenshots must be taken at the same:
- browser
- viewport
- zoom
- page scroll position

The desktop version must not:
- shrink
- clip
- stretch
- change panel heights
- change PHOTO center
- change VIDEO Timeline
- change colors

The desktop should simply be the workspace UI reopened.

## 17. No independent desktop repair

This is a hard prohibition.

If desktop output differs from workspace:

DO NOT edit UI CSS for the desktop.
DO NOT add desktop-only CSS.
DO NOT resize PHOTO separately.
DO NOT alter VIDEO separately.

Instead find the execution mismatch:
- stale server
- old shortcut
- old worktree
- cache
- wrong viewport
- wrong zoom
- wrong URL
- wrong root

Fix the launch mismatch only.

## 18. Branded icon preservation

Keep the currently improved branded MEDIA AI icon.

Do not redesign it again unless it is broken.

Verify:
- desktop shortcut shows branded icon
- favicon shows branded icon
- ICO decodes
- shortcut double-click works

The icon is NOT allowed to point to a separate copied build.

## 19. Cache rules

Keep no-cache UI headers.

Desktop launch must not rely on a historical query string.

Use a build query derived from CURRENT workspace identity, for example:
?ui_build=<ui-fingerprint-short>

Not:
?ui_refresh=20261002-photo-final
Not:
?ui_refresh=20261002-left-panel-v2022

No human-written historical UI tag is allowed.

## 20. Regression tests

Run:

python scripts/validate_pc_work_control_plane.py

pytest -q

node --test ui/ssot_structure.test.js ui/interaction.test.js

Also add tests:

### A. No clipping-rule regression
Assert the final approved_visual.css does NOT contain the rejected v20.2.5 canonical clipping block.

At minimum ensure it does not contain the combination:
- "v20.2.5 canonical row-height system"
- panel overflow:hidden used as row-height equalizer

### B. Golden CSS identity
Assert current ui/approved_visual.css equals the content from 97900cc baseline unless the representative later explicitly authorizes another workspace UI modification.

### C. Desktop no-copy rule
Assert launcher references current repo ui and no copy/stage operation exists.

## 21. Exact Evidence paths

Human Review:
docs/commander/MINDLE_MEDIA_AI_WORKSPACE_GOLDEN_TO_DESKTOP_MIRROR_FINAL_REVIEW_v20.2.6_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WORKSPACE_GOLDEN_TO_DESKTOP_MIRROR_FINAL_EVIDENCE_v20_2_6_20261002.json

Detail directory:
evidence/pc_remote/media-ai-workspace-mirror-v20_2_6-20261002/

Required files:

1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. GOLDEN_COMMIT_IDENTITY.json
4. WORKSPACE_GOLDEN_CSS_RESTORE.json
5. V20_2_5_CLIPPING_REMOVAL_AUDIT.json
6. WORKSPACE_UI_HASH_MANIFEST.json
7. PHOTO_CENTER_RESTORE_AUDIT.json
8. VIDEO_BASELINE_PRESERVATION.json
9. WORKSPACE_FINAL_UI_TOP.png
10. WORKSPACE_FINAL_UI_PHOTO.png
11. WORKSPACE_UI_FINAL_LOCK.json
12. DESKTOP_DUPLICATE_UI_AUDIT.json
13. DESKTOP_SHORTCUT_TARGET.json
14. RUNTIME_IDENTITY_VERIFY.json
15. STALE_SERVER_PROCESS_AUDIT.json
16. DESKTOP_FINAL_UI_TOP.png
17. DESKTOP_FINAL_UI_PHOTO.png
18. WORKSPACE_VS_DESKTOP_IDENTITY.json
19. WORKSPACE_VS_DESKTOP_TOP_COMPARISON.png
20. WORKSPACE_VS_DESKTOP_PHOTO_COMPARISON.png
21. VIEWPORT_ZOOM_PARITY.json
22. ICON_FAVICON_PRESERVATION.json
23. FUNCTION_SMOKE_CHECK.json
24. REGRESSION_TEST_RESULTS.txt
25. OUTPUT_HASHES.sha256
26. REMOTE_PUSH_VERIFY.txt

All PNGs must be actual Windows captures.
Do not fabricate missing screenshots.

## 22. PASS criteria

FINAL_WORKSPACE_DESKTOP_MIRROR_PASS:

Only if:

### Workspace
- approved_visual.css is restored from 97900cc
- PHOTO center is back to the previously accepted appearance
- VIDEO remains previously accepted
- no v20.2.5 clipping block remains
- workspace UI visually passes

### Desktop
- shortcut points only to canonical workspace launcher
- no separate desktop UI copy
- no historical worktree
- no old ui_refresh
- correct current server identity
- same UI fingerprint
- same viewport/zoom
- screenshots visually match workspace

### Product
- branded icon preserved
- favicon preserved
- tests PASS
- remote Evidence complete

## 23. Failure conditions

WORKSPACE_RESTORE_REQUIRED:
workspace itself is still wrong after rollback.

DESKTOP_MIRROR_MISMATCH:
workspace is correct but desktop differs.

FAIL:
- UI clipping remains
- desktop uses separate UI
- old process/worktree reused
- PHOTO center does not match golden baseline
- Evidence incomplete

## 24. Representative final check

Leave both available.

First show workspace direct launch.

Then close it.

Then double-click desktop icon.

Ask:

"신작가님, 지금 바탕화면 아이콘으로 연 화면이 방금 작업 폴더에서 확인한 화면과 완전히 같고, 사진 편집 중앙도 이전 정상 상태로 돌아와 있습니까?"

Do not perform any more UI edits unless the representative says correction is required.

## Final governing sentence

THE WORKSPACE IS THE ONLY UI. RESTORE THE WORKSPACE GEOMETRY EXACTLY TO THE KNOWN-GOOD 97900CC BASELINE, PRESERVE ONLY THE LATER LAUNCHER/CACHE/BRAND-ICON IMPROVEMENTS, LOCK THE CORRECT WORKSPACE, AND MAKE THE DESKTOP SHORTCUT DO NOTHING EXCEPT LAUNCH THAT SAME WORKSPACE. NO SECOND UI, NO DESKTOP-SPECIFIC CSS, NO HEIGHT PATCH, NO CLIPPING TRICK.
