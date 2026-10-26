# MINDLE MEDIA AI — PC WORK ONE-CLICK RUNTIME BLOCKER RECOVERY DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — BLOCKER RECOVERY AND BUILD CONTINUATION
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-BLOCKER-RECOVERY-R1
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926

## 0. VERIFIED STARTING POINT

General Work remains frozen PASS:
PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK

General Work baseline:
9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb

Latest PC Work preflight HEAD:
dbc57ebbc6a576b4f5c1089f12797812f538afa3

Current PC Work result:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

No MINDLE_MEDIA_AI_RUN.exe has been built yet.
No Windows one-click E2E PASS has been claimed.

## 1. PURPOSE

Resume the one-click Windows runtime work without returning to the rejected manual installer workflow.

The only final employee experience target remains:

DOUBLE-CLICK MINDLE_MEDIA_AI_RUN.exe
-> runtime prepares automatically
-> exactly one local server starts
-> browser opens automatically
-> MINDLE MEDIA AI is immediately usable

No normal employee flow may require:
- manual ZIP extraction
- Git
- repository clone
- Python installation
- pip
- PowerShell/CMD commands
- HF_TOKEN entry
- manual model download
- manual VC runtime repair
- developer-only paths or worktrees

## 2. FIRST BLOCKER — PC EXEC TOOL RECOVERY

The previous PC run was blocked by:
Failed to create unified exec process: helper_unknown_error: setup refresh had errors

This is an execution-environment blocker, not a product-runtime failure.

When the PC execution tool becomes available:
1. run scripts/validate_pc_work_control_plane.py first
2. record the exact output
3. inspect Windows profile/runtime state
4. continue from the existing preflight; do not restart General Work
5. do not claim PASS merely because the tool recovers

If the PC execution tool is still unavailable:
PC_EXECUTION_ENVIRONMENT_BLOCKED
and stop without fabricating local results.

## 3. VISUAL C++ RUNTIME RULE

Do not copy arbitrary DLLs from C:\Windows\System32 into the package.

Existing unresolved files include:
- msvcp140.dll
- msvcp140_atomic_wait.dll
- vcruntime140_threads.dll

Required action:
- inventory which packaged Python/native wheels already legally include their own runtime DLLs
- identify which Microsoft runtime components are still required from the host
- verify the applicable Microsoft redistribution basis before bundling any official redistributable or DLL
- preserve official Microsoft signature/hash/version Evidence for any approved redistributable
- do not expose a separate manual VC runtime repair step to the employee

If redistribution entitlement/basis cannot be verified:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

Do not call that state a one-click PASS.

## 4. FFMPEG REDISTRIBUTION RULE

The old Gyan FFmpeg 6.1.1 essentials candidate is currently recorded as GPL-3.0 with unresolved corresponding-source/static-dependency conditions.

Do not promote that old candidate to the final one-click delivery until its redistribution obligations are completely closed.

Preferred recovery path:
- replace the final-distribution FFmpeg candidate with an LGPL-compatible build/configuration when technically viable
- avoid GPL-only dependencies in the final distribution path
- on Windows, evaluate Media Foundation H.264 encoding support rather than relying on GPL libx264 for the packaged path
- preserve H.264 / yuv420p / faststart browser compatibility already proven by General Work
- verify ffmpeg.exe and ffprobe.exe from the final packaged runtime

Required Evidence:
- exact FFmpeg version/commit
- exact configure/build options
- license classification
- enabled external libraries
- binary SHA-256
- source/corresponding-source reference or archive
- THIRD_PARTY_NOTICES linkage

If no legally/technically acceptable packaged FFmpeg path can be proven:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

## 5. DO NOT REGRESS PRODUCT BEHAVIOR

Packaging/runtime changes must preserve:
- MINDLE MEDIA AI approved UI
- VIDEO approved structure
- PHOTO landscape-first Preview
- portrait Auto Fit
- PHOTO seven basic correction controls
- VIDEO H.264 browser playback
- PHOTO segmentation
- PHOTO 4x
- Korean STT
- Save / Close / Reopen
- Export
- 광고 숏폼 entry with graceful external-unavailable state

Marketing / AVORA remains DEFERRED_EXTERNAL.

## 6. IMPLEMENT MINDLE_MEDIA_AI_RUN.exe

After the two blocker classes above are resolved enough to proceed:

Build a single employee-visible launcher:
MINDLE_MEDIA_AI_RUN.exe

It must:
- be double-clickable
- show no developer console in the normal flow
- validate/materialize the bundled runtime automatically
- start exactly one product server
- wait for health readiness
- open the browser automatically
- reuse the active runtime on a second double-click
- recover safely from stale PID/lock state
- preserve project/user data across relaunches
- never depend on current working directory or repository paths

## 7. WINDOWS E2E — REQUIRED

On an actual ordinary/default Windows profile, prove:

1. no Git dependency
2. no system Python dependency
3. no pip
4. no terminal step
5. no manual model download
6. no manual VC/runtime repair
7. double-click MINDLE_MEDIA_AI_RUN.exe
8. exactly one runtime starts
9. browser auto-opens
10. approved UI is visible
11. PHOTO landscape import
12. PHOTO portrait Auto Fit
13. one basic PHOTO correction
14. PHOTO segmentation
15. PHOTO 4x upscale
16. VIDEO import and playback
17. VIDEO tracking
18. Korean STT and UI visibility
19. Save
20. safe shutdown
21. cold relaunch by double-click only
22. Reopen saved project
23. Export
24. ZIP/media hash and CRC validation
25. second double-click while already running -> no duplicate server
26. user/project data preserved after relaunch

## 8. REQUIRED EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_REVIEW_v1.0_20261008.md

Machine Evidence:
docs/evidence/media-ai-pc-work-one-click-runtime-blocker-recovery-20261008/EVIDENCE.json

Required detail files:
- PC_EXEC_TOOL_RECOVERY_RESULT.json
- VC_RUNTIME_DEPENDENCY_AUDIT.json
- FFMPEG_REDISTRIBUTION_AUDIT.json
- PACKAGE_MANIFEST.json
- FIRST_DOUBLE_CLICK_RESULT.json
- SECOND_DOUBLE_CLICK_SINGLE_INSTANCE_RESULT.json
- WINDOWS_RUNTIME_FUNCTION_E2E.json
- SAVE_REOPEN_COLD_RELAUNCH_RESULT.json
- EXPORT_INTEGRITY_RESULT.json
- DELIVERY_ARTIFACT_SHA256.txt
- REGRESSION_RESULT.json
- REMOTE_READBACK.txt

## 9. PASS / BLOCK VOCABULARY

Final PASS only:
PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E

If PC execution environment still cannot run:
PC_EXECUTION_ENVIRONMENT_BLOCKED

If VC/FFmpeg redistribution cannot be legally/technically closed:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

If EXE is built but actual Windows employee-style E2E is not completed:
PACKAGE_BUILT_WINDOWS_E2E_NOT_PROVEN

If normal employee use requires manual setup:
FAIL_ONE_CLICK_RUNTIME_USER_FRICTION

## 10. REPOSITORY / SAFETY

- canonical branch only
- no main merge
- no force push
- no new repo/worktree/branch
- PR #23 HOLD / DO NOT MERGE
- preserve General Work PASS Evidence
- preserve approved UI
- preserve historical failed/preflight Evidence
- external Marketing/AVORA remains DEFERRED_EXTERNAL

## FINAL COMMAND

RECOVER THE PC EXECUTION ENVIRONMENT FIRST.

THEN CLOSE VC RUNTIME AND FFMPEG REDISTRIBUTION CONDITIONS WITHOUT PUSHING MANUAL REPAIR STEPS TO THE EMPLOYEE.

BUILD MINDLE_MEDIA_AI_RUN.exe ONLY AFTER THOSE CONDITIONS ARE SATISFIED ENOUGH TO PROCEED.

PROVE THE ACTUAL WINDOWS DOUBLE-CLICK EXPERIENCE END TO END.

DO NOT CLAIM PASS UNTIL:
PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E
