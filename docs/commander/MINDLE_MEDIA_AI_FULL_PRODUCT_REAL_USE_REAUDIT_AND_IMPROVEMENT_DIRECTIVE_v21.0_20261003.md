# MINDLE MEDIA AI — FULL PRODUCT REAL-USE REAUDIT & IMPROVEMENT DIRECTIVE v21.0

Date: 2026-10-03
Status: ACTIVE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261003-V21.0

## 0. Why this cycle exists

Prior cycles produced metadata/test PASS results, but representative real-use testing still found:
- desktop shortcut/icon sometimes inactive
- workspace launch and desktop launch did not always show the same visual result
- UI geometry was repeatedly changed by later fixes
- some PASS claims relied on metadata/runtime identity without representative-visible execution proof

Therefore all final-closeout claims are reopened.

Representative real-use result overrides earlier metadata-only PASS.

No item may be marked PASS unless it is actually executed in the real Windows runtime or backed by direct executable evidence.

## 1. Single source of truth

ONE product only:

Current repository workspace
ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

Desktop shortcut is only a launcher.
It must never represent another copied UI/build/worktree.

Required chain:

Desktop shortcut
→ canonical launcher
→ current repository product_server
→ current repository ui/
→ current repository assets

No copied UI folder.
No historical worktree.
No stale server instance.
No old ui_refresh URL.
No desktop-specific CSS.

## 2. Freeze before audit

Before changing anything:
- record current HEAD
- record all UI file hashes
- record launcher hash
- record icon hash
- record runtime identity
- record current desktop shortcut metadata
- record port 8768 owning PID/process/command line

Do not modify UI until the baseline is captured.

## 3. Duplicate/stale instance audit

Find every possible MEDIA AI local runtime source on Windows:
- processes listening on 8768
- media_ai.product_server processes on any other ports
- stale worktrees
- copied ui directories
- desktop .lnk/.url files
- historical launcher scripts
- browser tabs/windows using older ui_refresh/ui_build URLs

Produce:
RUNTIME_INSTANCE_INVENTORY.json

If more than one executable product source exists:
mark DUPLICATE_RUNTIME_SOURCE_FOUND
and clean up safely.

Keep only the canonical current workspace runtime.

## 4. Desktop shortcut real activation test

Do not stop at shortcut metadata.

Actual steps:
1. close all MEDIA AI browser windows
2. verify current canonical server state
3. double-click the real desktop shortcut
4. prove browser window appears
5. prove current workspace UI appears
6. close it
7. double-click again
8. prove second launch also works

If any double-click does nothing:
FAIL and repair shortcut/launcher until repeatable.

Required result:
DESKTOP_DOUBLE_CLICK_2_OF_2_PASS

## 5. Workspace vs desktop identity

Launch once directly from workspace.
Launch once from desktop shortcut.

Compare:
- repo root
- branch
- HEAD
- index.html SHA
- approved_visual.css SHA
- interaction.css SHA
- interaction.js SHA
- product_integration.js SHA
- icon SHA
- runtime fingerprint
- viewport
- browser zoom

Required:
IDENTICAL_SOURCE_IDENTITY = true

If visuals differ while identity is equal:
investigate browser cache/viewport/state.
If identity differs:
fix launch path, not UI.

## 6. UI visual audit

Use final authority:
F27E base
+
Shortform Addendum
+
representative-approved later workspace corrections

Verify:
- VIDEO upper section
- PHOTO lower section
- left / center / right proportions
- no clipping
- no hidden controls
- no forced overflow hiding
- natural-language areas visible
- VIDEO Timeline complete
- PHOTO Preview complete
- right controls complete
- Shortform button present in correct order

Do not change geometry unless a visible defect is reproduced in the canonical workspace runtime.

## 7. VIDEO real function audit

Execute in Windows runtime:

- 영상 불러오기
- AI 자동 편집
- 광고 숏폼
- 자연어 입력
- 참고 이미지 추가
- Preview
- Timeline
- 프로젝트 저장
- 내보내기

For each:
record click path, input, visible result, output artifact, PASS/FAIL.

No DOM-presence-only PASS.

## 8. PHOTO real function audit

Execute:
- 사진 불러오기
- 자연어 입력
- 참고 이미지 추가
- PHOTO Preview
- AI 보정
- segmentation route
- 4x upscale route
- 프로젝트 저장
- 내보내기

Record visible result and output.

No DOM-presence-only PASS.

## 9. Shortform real function audit

Execute:
- 광고 숏폼 mode
- Marketing bridge connectivity
- approved contract retrieval
- scene/timeline display
- Preview
- final MP4 invocation/export

Preserve known v20.1 PASS unless current regression is reproduced.

Voiceover audio remains separate:
VOICE_AUDIO_DEPENDENCY_VERIFY_REQUIRED
Do not fake TTS PASS.

## 10. Save / reopen / persistence

Test:
1. open media
2. make one VIDEO change
3. make one PHOTO change
4. save project
5. close product
6. reopen via desktop shortcut
7. reopen saved project
8. verify state persists

Required:
SAVE_REOPEN_PERSISTENCE_PASS

## 11. Icon audit

Verify actual Windows desktop:
- branded icon displayed
- no white generic page icon
- shortcut clickable
- icon remains after reboot/re-login style refresh where possible
- favicon visible
- shortcut icon and launcher target remain canonical

## 12. Error and recovery audit

Test:
- server not running → desktop shortcut starts it
- stale 8768 process → launcher detects mismatch and recovers
- browser already open → launcher still opens MEDIA AI visibly
- repeated double-click does not spawn conflicting product servers
- invalid file input produces visible error without crashing
- missing optional dependency fails clearly

## 13. Regression suite

Run:
python scripts/validate_pc_work_control_plane.py
pytest -q
node --test ui/ssot_structure.test.js ui/interaction.test.js

But automated tests are SUPPORTING evidence only.
They cannot replace real Windows function execution.

## 14. Final result vocabulary

FULL_REAL_USE_PASS
- all required runtime functions work
- desktop shortcut 2/2
- workspace/desktop identical
- no duplicate runtime source
- save/reopen works
- icon active
- no representative-visible UI defect

IMPROVEMENT_REQUIRED
- any non-blocking defect remains

BLOCKED
- environment/access prevents required runtime verification

FAIL
- key product function or canonical launch path fails

## 15. Exact Evidence

Review:
docs/commander/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_REVIEW_v21.0_20261003.md

Machine:
evidence/pc_remote/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_EVIDENCE_v21_0_20261003.json

Detail:
evidence/pc_remote/media-ai-full-reaudit-v21_0-20261003/

Required evidence:
1. BASELINE_IDENTITY.json
2. RUNTIME_INSTANCE_INVENTORY.json
3. DUPLICATE_SOURCE_AUDIT.json
4. DESKTOP_SHORTCUT_ACTIVATION.json
5. DESKTOP_DOUBLE_CLICK_2_OF_2.json
6. WORKSPACE_DESKTOP_IDENTITY.json
7. UI_VISUAL_AUDIT.json
8. VIDEO_REAL_FUNCTION_AUDIT.json
9. PHOTO_REAL_FUNCTION_AUDIT.json
10. SHORTFORM_REAL_FUNCTION_AUDIT.json
11. SAVE_REOPEN_PERSISTENCE.json
12. ICON_FAVICON_AUDIT.json
13. ERROR_RECOVERY_AUDIT.json
14. REGRESSION_TEST_RESULTS.txt
15. REPRESENTATIVE_OPEN_SCREEN_GATE.json
16. OUTPUT_HASHES.sha256
17. REMOTE_PUSH_VERIFY.txt

## 16. Representative-visible closeout gate

At the end:
- leave MEDIA AI open from desktop shortcut
- leave desktop icon visible
- do not close the server

Final question:

"신작가님, 지금 바탕화면 아이콘으로 직접 연 MEDIA AI가 작업 폴더와 동일하게 보이고, 실제 사용 기능도 정상적으로 동작합니까?"

No final closeout before representative confirmation.

## Final rule

REAL USER TESTS OVERRIDE METADATA. ONE WORKSPACE, ONE RUNTIME, ONE DESKTOP LAUNCH PATH. VERIFY EVERY IMPORTANT CONTROL IN THE REAL WINDOWS PRODUCT BEFORE PASS.
