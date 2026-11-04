# MINDLE MEDIA AI — PC WORK v21.0A EXECUTION ENFORCEMENT DIRECTIVE v21.0A-R1

Date: 2026-10-05
Status: ACTIVE — EXECUTE NOW
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Parent epoch: MEDIA-AI-20261005-V21.0A

## 0. Commander decision

Previous v21.0A status:
NOT_STARTED_REJECT

Do not create another plan.
Do not write a summary and stop.
Do not produce evidence-only PASS.

Execute the existing v21.0A work in the real Windows machine now.

Base directive:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_SINGLE_RUNTIME_LAUNCHER_AND_UI_COLLISION_REPAIR_DIRECTIVE_v21.0A_20261005.md

This enforcement directive does not replace its technical requirements.
It forces actual execution.

## 1. Mandatory start

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to remote HEAD
4. read CURRENT_WORKER_COORDINATION_LOCK.json
5. confirm Worker A / product-runtime lane
6. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
7. run:
   python scripts/validate_pc_work_control_plane.py
8. require CONTROL_PLANE_PASS

If any step fails:
record the exact blocker and stop.
Do not continue on another branch.

## 2. Phase 1 — desktop/runtime inventory

On the actual Windows desktop, enumerate:

- every MINDLE MEDIA AI *.lnk
- every MINDLE MEDIA AI *.url
- target
- arguments
- working directory
- icon path
- modified time

Also enumerate:

- all TCP listeners on 8768
- owning PID
- owning executable
- command line
- every media_ai.product_server process
- every MEDIA AI browser window/tab URL

Evidence:
DESKTOP_LAUNCH_PATH_INVENTORY.json
PORT_8768_PROCESS_INVENTORY.json

Do not infer.
Capture actual machine state.

## 3. Phase 2 — remove duplicate launch routes

The final desktop must have ONE executable product route.

Forbidden final state:
- .url shortcut that directly opens 127.0.0.1:8768
- second MEDIA AI shortcut
- historical worktree launcher
- copied UI folder launcher
- raw HTML launcher

After inventory:
- remove/archive the direct .url bypass
- preserve project/user data
- keep exactly one final branded .lnk

Evidence:
DIRECT_URL_SHORTCUT_REMOVAL.json

## 4. Phase 3 — install canonical shortcut

Create/use:
scripts/install_media_ai_desktop_shortcut.ps1

It must be idempotent and create:

MINDLE MEDIA AI - 최종 UI.lnk

Target:
Windows PowerShell

Arguments must execute:
scripts/launch_media_ai_windows.ps1

Required:
- -NoProfile
- -ExecutionPolicy Bypass
- WorkingDirectory=current canonical repository
- IconLocation=current branded ICO
- no direct localhost URL as shortcut target

Evidence:
CANONICAL_LNK_METADATA.json

## 5. Phase 4 — one-server enforcement

The canonical launcher must guarantee:

- one canonical repository root
- one canonical branch
- one product_server
- port 8768 belongs to the canonical MEDIA AI runtime
- no stale MEDIA AI process remains

If 8768 is occupied by another MEDIA AI instance:
identify it first, then safely stop only that stale MEDIA AI process.

If 8768 belongs to a non-MEDIA-AI process:
STOP with:
PORT_8768_CONFLICT_NON_MEDIA_AI

Do not kill unrelated software.

## 6. Phase 5 — identity gate

Run A:
canonical workspace launch

Run B:
desktop .lnk launch

Compare actual:

- repo root
- branch
- full HEAD
- UI fingerprint
- index.html SHA
- approved_visual.css SHA
- interaction.css SHA
- interaction.js SHA
- product_integration.js SHA
- icon SHA
- server PID
- server command line
- port
- data directory
- browser executable
- zoom
- viewport
- Windows scale

Required:
WORKSPACE_DESKTOP_IDENTICAL_SOURCE = true

Evidence:
WORKSPACE_DESKTOP_IDENTITY_AFTER_REPAIR.json

If false:
STOP.
Do not edit UI yet.

## 7. Phase 6 — desktop activation 2-of-2

Close MEDIA AI browser window.

Double-click final desktop icon:
Launch #1 must visibly open current MEDIA AI.

Close it.

Double-click final desktop icon again:
Launch #2 must visibly open current MEDIA AI.

Required:
DESKTOP_DOUBLE_CLICK_2_OF_2_PASS

Evidence:
DESKTOP_DOUBLE_CLICK_2_OF_2_AFTER_REPAIR.json

Metadata alone is not PASS.

## 8. Phase 7 — reproduce actual UI overlap/clipping

Only after identity PASS:

Use the actual Windows display.

Record:
- resolution
- Windows scaling
- browser
- zoom
- viewport width/height

Reproduce the user-observed:
- panel overlap
- bottom clipping
- mismatched VIDEO/PHOTO heights

Capture actual screen evidence.

Evidence:
UI_OVERLAP_REPRODUCTION.json

If the defect does not reproduce:
do not modify CSS.
Record NOT_REPRODUCED and continue functional testing.

## 9. Phase 8 — minimal UI repair only if reproduced

Known risk area:
ui/approved_visual.css

Inspect:
- duplicate max-width 1100 rules
- duplicate/repeated breakpoint rules
- fixed heights 380/350/330
- preview/timeline min-height conflicts
- overflow behavior

Rules:
- make smallest change
- consolidate duplicate rules when safe
- no overflow:hidden clipping workaround
- no arbitrary shrinking
- no redesign
- preserve F27E + Shortform SSOT
- preserve current branded icon

Evidence:
UI_OVERLAP_REPAIR_DIFF.txt

After repair:
- retest maximized desktop
- retest one narrower window
- confirm no bottom controls hidden
- confirm VIDEO Timeline complete
- confirm PHOTO Preview controls complete
- confirm left/center/right complete

## 10. Phase 9 — real function audit

Do not stop after launcher/UI repair.

VIDEO actual execution:
- 영상 불러오기
- AI 자동 편집
- 광고 숏폼
- 자연어 입력
- 참고 이미지 추가
- Preview
- Timeline
- 프로젝트 저장
- 내보내기

PHOTO actual execution:
- 사진 불러오기
- 자연어 입력
- 참고 이미지 추가
- AI 보정
- segmentation
- 4x upscale
- 프로젝트 저장
- 내보내기

For each:
- click path
- real input
- visible result
- output artifact
- PASS/FAIL

Evidence:
FUNCTIONAL_REAUDIT_AFTER_REPAIR.json

No DOM-only PASS.

## 11. Phase 10 — save/reopen

1. load VIDEO
2. perform one actual operation
3. load PHOTO
4. perform one actual operation
5. save
6. close app
7. reopen only through final desktop .lnk
8. reopen saved project
9. verify persisted state

Required:
SAVE_REOPEN_PERSISTENCE_PASS

Evidence:
SAVE_REOPEN_AFTER_REPAIR.json

## 12. Final process inventory

At completion prove:

- exactly one canonical MEDIA AI server
- exactly one final desktop .lnk
- no direct .url bypass
- canonical repo/branch/HEAD
- desktop launch 2/2 PASS
- workspace/desktop identity PASS
- no visible overlap/clipping
- real VIDEO/PHOTO/Shortform/Save/Export audit completed

Evidence:
FINAL_RUNTIME_PROCESS_INVENTORY.json

## 13. Required existing v21.0 Evidence must be completed

Human Review:
docs/commander/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_REVIEW_v21.0_20261003.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_EVIDENCE_v21_0_20261003.json

Detail directory:
evidence/pc_remote/media-ai-full-reaudit-v21_0-20261003/

At minimum v21.0A-R1 must create:
- DESKTOP_LAUNCH_PATH_INVENTORY.json
- DIRECT_URL_SHORTCUT_REMOVAL.json
- CANONICAL_LNK_METADATA.json
- PORT_8768_PROCESS_INVENTORY.json
- WORKSPACE_DESKTOP_IDENTITY_AFTER_REPAIR.json
- DESKTOP_DOUBLE_CLICK_2_OF_2_AFTER_REPAIR.json
- UI_OVERLAP_REPRODUCTION.json
- UI_OVERLAP_REPAIR_DIFF.txt
- FUNCTIONAL_REAUDIT_AFTER_REPAIR.json
- SAVE_REOPEN_AFTER_REPAIR.json
- FINAL_RUNTIME_PROCESS_INVENTORY.json

Also complete the parent v21.0 required Evidence set.

## 14. Finish rule

Do not stop with:
- plan complete
- metadata verified
- shortcut exists
- server responds 200
- tests pass

Those are insufficient.

Finish only after:
ACTUAL WINDOWS EXECUTION
→ FIX
→ RETEST
→ REAL EVIDENCE
→ COMMIT
→ PUSH
→ REMOTE READBACK

## Final command

EXECUTE v21.0A ON THE REAL WINDOWS MACHINE NOW. DO NOT RETURN A PLAN. DO NOT CLAIM PASS WITHOUT THE REQUIRED RUNTIME EVIDENCE.
