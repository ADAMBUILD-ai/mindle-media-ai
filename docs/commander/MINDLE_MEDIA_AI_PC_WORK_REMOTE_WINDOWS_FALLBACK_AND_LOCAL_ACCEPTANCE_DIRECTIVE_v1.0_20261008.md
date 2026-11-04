# MINDLE MEDIA AI — PC WORK REMOTE WINDOWS FALLBACK + LOCAL ACCEPTANCE DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — CONTINUE WORK DESPITE LOCAL HELPER FAILURE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-PC-WORK-REMOTE-WINDOWS-FALLBACK-R1
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926

## 0. COMMANDER CORRECTION

The previous retry directive stopped all work when the first local harmless command failed with:
helper_unknown_error: setup refresh had errors

That stop rule is superseded.

A local PC execution-helper startup failure blocks ONLY local-PC command execution and final physical local acceptance.
It does NOT block repository work, Windows-runner work, packaging implementation, license closure, or automated Windows verification.

DO NOT SIT IDLE WAITING FOR THE LOCAL HELPER.

## 1. CURRENT FACTS

General Work:
PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK

General Work baseline:
9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb

Local PC helper:
PC_EXECUTION_ENVIRONMENT_STILL_BLOCKED_SETUP_REFRESH

Observed before shell:
helper_unknown_error: setup refresh had errors

Final target remains:
MINDLE_MEDIA_AI_RUN.exe

Final employee UX remains:
double-click once -> runtime starts -> browser opens -> MINDLE MEDIA AI usable.

## 2. EXECUTION MODES

### MODE A — LOCAL PC
Use whenever the PC execution helper works.
Purpose:
- final real-user double-click acceptance
- target-PC process/port/profile tests
- target-PC cold relaunch
- final physical host evidence

### MODE B — REMOTE WINDOWS FALLBACK
Use whenever local helper is blocked.
Use GitHub Actions Windows runner and GitHub repository tools to continue all work that does not require the owner's physical desktop.

MODE B is ACTIVE NOW.

## 3. LOCAL HELPER FAILURE RULE — NO FULL STOP

If local Get-Location fails before shell with setup refresh:
1. record LOCAL_HELPER_BLOCKED_SETUP_REFRESH
2. do NOT modify product UI
3. do NOT claim local Windows acceptance
4. immediately switch to MODE B
5. continue repository implementation and Windows Runner validation

Forbidden response:
"stop product work and wait"

Required response:
"continue through remote Windows fallback; local acceptance remains pending"

## 4. REMOTE WINDOWS FALLBACK WORK — EXECUTE NOW

Continue the one-click package work through GitHub Windows Runner.

Required order:

1. Run the PC Control Plane validator on windows-latest.
2. Capture Windows runner identity, PowerShell version, user, TEMP, LOCALAPPDATA and path behavior.
3. Audit existing Windows launcher/package scripts.
4. Close VC Runtime dependency inventory and redistribution strategy.
5. Close FFmpeg distribution strategy and exact build/license/source evidence.
6. Implement the one-click launcher build path for:
   MINDLE_MEDIA_AI_RUN.exe
7. Build the EXE on the Windows runner.
8. Validate package manifest and hashes.
9. Start packaged runtime on Windows runner without repo-relative runtime dependency.
10. Verify server health and single-instance behavior.
11. Verify browser endpoint/UI serving where GUI interaction is automatable.
12. Run PHOTO/VIDEO/STT/Save-Reopen/Export automated Windows runtime tests that can run on the runner.
13. Publish EXE/package artifact and Evidence.
14. Mark only physical-local-only gates as LOCAL_ACCEPTANCE_PENDING.

Do not postpone 1–13 because the local helper is broken.

## 5. VC RUNTIME WORK

Do not copy DLLs from System32.

Perform an exact dependency inventory on the Windows Runner:
- Python runtime DLLs
- NumPy/OpenCV/OpenVINO/native wheel DLLs
- Microsoft VC runtime dependencies
- which DLLs are already legitimately embedded upstream
- which host prerequisites remain

Select a compliant final strategy:
A. legally redistributable official Microsoft runtime bundled/bootstrapped automatically, or
B. remove/replace dependency requiring unsupported host runtime, or
C. explicit blocker with exact component and evidence

Normal employee flow must not contain a manual repair step.

## 6. FFMPEG WORK

The old unresolved Gyan GPL candidate cannot be silently promoted.

PC Work must choose and prove one final route:
- LGPL-compatible FFmpeg distribution with full required notices/source obligations closed, or
- another technically verified legally distributable media path that preserves required codecs/features.

Required:
- exact binary/version
- configure/build flags or upstream package identity
- enabled external libraries
- license classification
- source/corresponding-source location
- SHA-256
- ffmpeg/ffprobe behavior
- H.264/yuv420p/faststart browser compatibility

Do not remove working product capabilities merely to make licensing easier without explicit evidence and review.

## 7. ONE-CLICK EXE IMPLEMENTATION

MINDLE_MEDIA_AI_RUN.exe must:
- be the only normal employee launch action
- not expose a console in normal use
- materialize/verify its runtime automatically
- start exactly one server
- wait for health
- auto-open default browser/approved browser route
- on second launch, reuse/focus/open existing runtime rather than starting a duplicate
- use persistent data outside replaceable runtime payload
- work from paths containing spaces
- not depend on repo checkout, Git, system Python, pip, HF_TOKEN, or manual model download

The old complex INSTALL_MINDLE_MEDIA_AI flow is legacy and not the final normal UX.

## 8. REMOTE WINDOWS PASS LEVEL

When the Windows Runner completes all remotely executable work, report:

PASS_REMOTE_WINDOWS_ONE_CLICK_BUILD_AND_AUTOMATION_READY_LOCAL_ACCEPTANCE_PENDING

This means:
- EXE built
- package integrity proven
- remote Windows runtime tests pass
- local physical acceptance still pending

It is NOT final release PASS.

## 9. FINAL LOCAL ACCEPTANCE

When the local PC helper eventually recovers, do NOT restart the project.
Download/use the exact remotely proven artifact and perform only the remaining local acceptance:

1. clean/default employee-style profile
2. double-click MINDLE_MEDIA_AI_RUN.exe
3. browser auto-opens
4. one runtime only
5. PHOTO/VIDEO/STT quick practical
6. Save/Reopen
7. Export
8. second double-click duplicate prevention
9. cold relaunch/data preservation

Only after that:
PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E

## 10. REQUIRED EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_REMOTE_WINDOWS_FALLBACK_REVIEW_v1.0_20261008.md

Evidence root:
docs/evidence/media-ai-pc-work-remote-windows-fallback-20261008/

Required:
- LOCAL_HELPER_STATUS.json
- REMOTE_WINDOWS_RUNNER_PROFILE.json
- CONTROL_PLANE_VALIDATOR_RESULT.txt
- VC_RUNTIME_DEPENDENCY_AUDIT.json
- FFMPEG_DISTRIBUTION_AUDIT.json
- ONE_CLICK_BUILD_RESULT.json
- PACKAGE_MANIFEST.json
- DELIVERY_ARTIFACT_SHA256.txt
- REMOTE_WINDOWS_RUNTIME_E2E.json
- SINGLE_INSTANCE_RESULT.json
- REMOTE_EXPORT_INTEGRITY.json
- LOCAL_ACCEPTANCE_STATUS.json
- REGRESSION_RESULT.json
- REMOTE_READBACK.txt

## 11. STATUS VOCABULARY

Local helper still broken but remote work continuing:
ACTIVE_REMOTE_WINDOWS_FALLBACK_LOCAL_HELPER_BLOCKED

Remote build/test complete, local final acceptance pending:
PASS_REMOTE_WINDOWS_ONE_CLICK_BUILD_AND_AUTOMATION_READY_LOCAL_ACCEPTANCE_PENDING

Final local acceptance complete:
PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E

Real redistribution blocker:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

Do not use PC_EXECUTION_ENVIRONMENT_BLOCKED as a reason to stop remote-safe work.

## 12. PROTECTION

- General Work baseline frozen
- approved UI frozen
- main merge forbidden
- force push forbidden
- new repo/worktree/branch forbidden
- PR #23 HOLD / DO NOT MERGE
- Marketing/AVORA DEFERRED_EXTERNAL

## FINAL COMMAND

LOCAL HELPER FAILURE DOES NOT STOP THE PROJECT.

SWITCH TO GITHUB WINDOWS RUNNER AND CONTINUE NOW.

BUILD AND AUTOMATE EVERYTHING POSSIBLE REMOTELY.
LEAVE ONLY PHYSICAL LOCAL DOUBLE-CLICK ACCEPTANCE PENDING.
