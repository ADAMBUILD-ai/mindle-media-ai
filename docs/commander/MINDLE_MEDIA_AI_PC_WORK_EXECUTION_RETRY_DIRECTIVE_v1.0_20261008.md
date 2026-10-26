# MINDLE MEDIA AI — PC WORK EXECUTION RETRY DIRECTIVE v1.0

Date: 2026-10-08
Status: EXECUTE NOW — PC WORK ENVIRONMENT RETRY
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-PC-WORK-EXECUTION-RETRY-R1

## 1. PURPOSE

Do not wait. Immediately retry the Windows PC Work execution environment.

This directive does not reopen product development and does not change the approved UI.
It exists only to restore the PC Work command execution path and then continue the already-approved one-click runtime package work.

## 2. IMMEDIATE EXECUTION ORDER

1. Start a fresh PC Work execution session.
2. Run the first harmless command:
   `Get-Location`
3. If that succeeds, run:
   `whoami`
4. If that succeeds, create and delete one temporary file.
5. Then run:
   `python scripts/validate_pc_work_control_plane.py`
6. If validator passes, immediately continue the existing blocker-recovery directive:
   `docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_BLOCKER_RECOVERY_DIRECTIVE_v1.0_20261008.md`
7. Continue in the same work session through:
   - VC Runtime redistribution check
   - FFmpeg redistribution-compliant configuration check
   - MINDLE_MEDIA_AI_RUN.exe build
   - actual Windows double-click E2E
   - PHOTO / VIDEO / STT / Save-Reopen / Export
   - second-launch duplicate prevention
   - cold relaunch and data retention

## 3. FAILURE RULE

If the first harmless command fails again before shell execution with:
`helper_unknown_error: setup refresh had errors`

stop product work and report exactly:

`PC_EXECUTION_ENVIRONMENT_STILL_BLOCKED_SETUP_REFRESH`

Do not modify MEDIA product code.
Do not claim EXE build failure.
Do not claim Windows E2E failure.
Do not fall back to manual installer workflow.

## 4. FROZEN BASELINES

General Work PASS remains frozen:
`PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK`

General Work baseline:
`9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb`

PC Work control baseline:
`a6af2de1e43c4e83f86809e4b3ef046250520022`

Marketing and AVORA remain DEFERRED_EXTERNAL.
PR #23 remains HOLD / DO NOT MERGE.
No main merge.

## 5. ONLY FINAL PASS

Only after the actual employee-style Windows double-click flow passes end-to-end may PC Work report:

`PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E`

Until then, no PASS.
