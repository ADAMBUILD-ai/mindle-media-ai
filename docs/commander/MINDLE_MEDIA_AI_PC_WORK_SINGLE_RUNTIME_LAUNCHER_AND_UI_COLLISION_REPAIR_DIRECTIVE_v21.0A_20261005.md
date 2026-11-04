# MINDLE MEDIA AI — PC WORK IMMEDIATE REPAIR ADDENDUM v21.0A

Date: 2026-10-05
Status: EXECUTE UNDER ACTIVE v21.0
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Parent cycle: MEDIA-AI-20261003-V21.0

## 0. Reason for this addendum

Representative real-use testing exposed two concrete problems that must be repaired before the remaining v21.0 functional audit can be trusted:

1. A desktop `.url` shortcut can open `127.0.0.1:8768` directly and therefore bypass the canonical launcher identity checks.
2. `ui/approved_visual.css` contains accumulated responsive/fixed-height correction blocks, including repeated `@media (max-width: 1100px)` rules and later fixed editor heights. These may create overlap/clipping on the actual Windows display.

The repair order is mandatory:
SINGLE RUNTIME / SINGLE DESKTOP LAUNCH PATH
→ IDENTICAL SOURCE PROOF
→ UI OVERLAP REPRODUCTION
→ MINIMAL UI REPAIR
→ FULL FUNCTION AUDIT.

Do not reverse this order.

## 1. Preflight and ownership

Before any product write:
- git fetch origin
- confirm current branch exactly `feature/ad-shortform-bridge-p0-20260926`
- read `CURRENT_WORKER_COORDINATION_LOCK.json`
- operate as Worker A / product-runtime lane
- run `python scripts/validate_pc_work_control_plane.py`
- require `CONTROL_PLANE_PASS`
- record remote HEAD before work
- if remote HEAD moved after checkout, re-read the lock and reconcile before writing

Worker B must not edit `ui/**`, `src/**`, `scripts/**`, or the current runtime evidence while this addendum is being executed.

## 2. Confirmed repository facts

Canonical launcher:
`scripts/launch_media_ai_windows.ps1`

The launcher already verifies:
- canonical branch
- full Git HEAD
- repo root
- UI file SHA-256 set
- workspace UI fingerprint
- `/api/runtime-identity`
- port 8768 runtime identity

The product server already returns no-cache/no-store headers for UI files.

Therefore:
- browser cache is not the primary suspected cause
- a direct desktop `.url` is not an acceptable final launcher
- desktop launch must pass through the canonical PowerShell launcher

## 3. Desktop launcher repair — highest priority

### 3.1 Inventory first

Record every matching desktop item:
- `MINDLE MEDIA AI*.lnk`
- `MINDLE MEDIA AI*.url`

For each item record:
- full path
- file type
- target
- arguments
- working directory
- icon location
- modified time

Also record:
- every listener on 127.0.0.1:8768
- owning PID
- process path
- command line
- all `media_ai.product_server` processes on any port

Output:
`DESKTOP_LAUNCH_PATH_INVENTORY.json`

### 3.2 Remove the bypass path

The final desktop product MUST NOT use a `.url` file that opens `http://127.0.0.1:8768` directly.

After evidence capture:
- remove or archive the temporary direct `.url` shortcut
- keep exactly one final desktop app shortcut
- do not delete project data

### 3.3 Create one canonical .lnk

Worker A shall add and use a repository-owned installer:
`scripts/install_media_ai_desktop_shortcut.ps1`

The installer must create exactly one Windows `.lnk` whose target is PowerShell and whose arguments execute:
`scripts/launch_media_ai_windows.ps1`

Required behavior:
- `-NoProfile`
- `-ExecutionPolicy Bypass`
- hidden/minimized shell flash where practical
- WorkingDirectory = canonical repository root
- IconLocation = `ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico`
- shortcut name = one approved MINDLE MEDIA AI desktop name only
- idempotent: running installer twice does not create duplicates

A direct browser URL is forbidden as the shortcut target.

### 3.4 Launcher hardening

Review `scripts/launch_media_ai_windows.ps1` and minimally harden it so:
- if 8768 is occupied by a mismatched MEDIA AI product_server, terminate only that stale MEDIA AI process and restart canonical runtime
- if 8768 is occupied by an unrelated process, do NOT kill it; report `PORT_8768_CONFLICT_NON_MEDIA_AI`
- browser is opened only after runtime identity equals canonical repo/branch/full HEAD/UI fingerprint
- repeated double-clicks never create multiple product servers
- every launch opens a visible product window
- only one canonical data directory is used

Preferred product presentation:
- app-style Edge/Chrome window may be used if it is visually stable and still opens the canonical URL
- do not change UI merely to compensate for browser chrome

## 4. Identity gate — must pass before UI edits

Run two paths:

A. workspace/canonical launcher execution  
B. final desktop .lnk execution

For both capture:
- repo_root
- branch
- full HEAD
- workspace_ui_fingerprint
- index.html SHA
- approved_visual.css SHA
- interaction.css SHA
- interaction.js SHA
- product_integration.js SHA
- icon SHA
- port
- PID
- command line
- data-dir
- browser executable
- browser zoom
- viewport
- Windows display scaling

Required:
`WORKSPACE_DESKTOP_IDENTICAL_SOURCE = true`

Then:
- close window
- desktop double-click #1
- prove visible product
- close window
- desktop double-click #2
- prove visible product

Required:
`DESKTOP_DOUBLE_CLICK_2_OF_2_PASS`

If this gate fails, UI editing is forbidden.

## 5. UI overlap/clipping repair — only after identity gate

Known CSS risk:
- repeated `@media (max-width: 1100px)` blocks
- accumulated later geometry corrections
- fixed heights such as 380px / 350px / 330px in the editor layout chain
- multiple minimum-height overrides for VIDEO and PHOTO previews/timelines

Procedure:
1. reproduce the user-visible overlap/clipping on the actual Windows machine
2. capture screenshot and viewport/scale/zoom
3. compare against canonical approved UI authority
4. identify the exact CSS declarations causing overlap
5. make the smallest possible correction
6. consolidate duplicate breakpoint logic when it controls the same elements
7. do not introduce `overflow:hidden` or arbitrary fixed-height clipping as a visual workaround
8. retest at the actual maximized desktop size
9. also retest one narrower window only as regression support; the maximized desktop product remains the primary representative gate

Do not change:
- product information architecture
- VIDEO/PHOTO workflow order
- branding
- approved core layout concept
unless a separate owner decision explicitly changes the SSOT.

Required UI result:
- no overlapping panels
- no hidden bottom controls
- complete VIDEO timeline
- complete PHOTO preview controls
- left/center/right columns visible
- same appearance from workspace and desktop launch

## 6. Functional improvement pass after launch/UI repair

Continue the parent v21.0 real-use audit in this order:

VIDEO:
- 영상 불러오기
- AI 자동 편집
- 광고 숏폼
- 자연어 입력
- 참고 이미지 추가
- Preview
- Timeline
- 프로젝트 저장
- 내보내기

PHOTO:
- 사진 불러오기
- 자연어 입력
- 참고 이미지 추가
- AI 보정
- segmentation route
- 4x upscale route
- 프로젝트 저장
- 내보내기

Persistence:
- save
- close product
- reopen from desktop shortcut
- reopen saved project
- verify VIDEO and PHOTO state

Error recovery:
- server stopped
- stale MEDIA AI server
- repeated double-click
- invalid file
- missing optional dependency

No DOM-only PASS.

## 7. Required evidence

Add to the existing v21.0 detail directory:

1. `DESKTOP_LAUNCH_PATH_INVENTORY.json`
2. `DIRECT_URL_SHORTCUT_REMOVAL.json`
3. `CANONICAL_LNK_METADATA.json`
4. `PORT_8768_PROCESS_INVENTORY.json`
5. `WORKSPACE_DESKTOP_IDENTITY_AFTER_REPAIR.json`
6. `DESKTOP_DOUBLE_CLICK_2_OF_2_AFTER_REPAIR.json`
7. `UI_OVERLAP_REPRODUCTION.json`
8. `UI_OVERLAP_REPAIR_DIFF.txt`
9. `UI_AFTER_REPAIR_SCREENSHOT_README.md`
10. `FUNCTIONAL_REAUDIT_AFTER_REPAIR.json`
11. `SAVE_REOPEN_AFTER_REPAIR.json`
12. `FINAL_RUNTIME_PROCESS_INVENTORY.json`

Update the parent v21.0 Review and machine Evidence; do not create a parallel PASS vocabulary.

## 8. Stop conditions

STOP and report, do not improvise, if:
- branch is not canonical
- control plane validation fails
- lane ownership conflicts
- unrelated process owns 8768
- two different repo roots are serving MEDIA AI
- UI identity differs between workspace and desktop after launcher repair

## Final rule

ONE REPOSITORY.
ONE ACTIVE BRANCH.
ONE PRODUCT SERVER.
ONE DESKTOP .LNK.
NO DIRECT .URL BYPASS.
IDENTITY PASS FIRST, UI REPAIR SECOND, FUNCTION TEST THIRD.
