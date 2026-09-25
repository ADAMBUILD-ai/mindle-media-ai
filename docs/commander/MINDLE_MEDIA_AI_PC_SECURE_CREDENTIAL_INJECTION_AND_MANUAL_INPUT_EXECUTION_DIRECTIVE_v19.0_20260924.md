# MINDLE MEDIA AI — PC SECURE CREDENTIAL INJECTION & MANUAL INPUT EXECUTION DIRECTIVE v19.0
Date: 2026-09-24
Status: EXECUTE UNTIL TRUE MANUAL GATE
Base: PR #13 head 2f3f45dbf2776ffb64f615c0696a2d1e5cba9ada

## 1. Commander verification
v17 Evidence is accepted as honest REWORK. Do not repeat readiness review.
Confirmed preserved PASS:
- v13 immutable closeout evidence
- v14 UI/UX review
- v15 Python 46 PASS
- UI structure/interaction PASS
- product server health HTTP 200
- UI_SSOT_CHANGED:NO

The remaining blockers are external/manual: secure HF credential injection to the PC process, frozen cache materialization, local free dependencies, one owned moving-subject video, and one approved spoken-Korean recording.

## 2. Objective
Advance every executable item now. Stop only at the smallest unavoidable user action. Do not return another generic blocker report.

## 3. Secure credential injection
1. Detect the approved local secret/credential mechanism available in the PC Work environment.
2. If an existing scoped HF credential can be injected without revealing it, use that path.
3. If user interaction is required, open the secure credential/secret input UI and request only that single action.
4. Never ask the user to paste the token into chat, terminal history, source files, logs, PR, or Evidence.
5. Verify only boolean availability/authentication success; never print the secret.

## 4. Cache materialization immediately after auth
Using the frozen Private HF revision from the v13 adopted-model manifest, materialize:
- SAM 2.1
- whisper-small
- Intel single-image-super-resolution-1032
For every required file verify revision, filename, exact bytes and recorded hash before use.
Mismatch => fail closed. No legacy fallback.
Record local cache paths without secret data.

## 5. Free local dependencies
Install/expose only what the actual runtime requires:
- OpenVINO CPU for Intel SISR
- ffmpeg for video decode/encode
- Selenium + Chrome/Chromedriver only if UI automation is required
- PyArrow only if the chosen input route requires it
Record version/path and rerun health checks.
No GPU and no paid compute.

## 6. Inputs — use what exists first
PHOTO and UPSCALE inputs already exist. As soon as cache/dependencies are ready, execute these two lanes immediately; do not wait for VIDEO/AUDIO.

PHOTO:
approved UI -> real architecture photo -> SAM segmentation -> real output -> Preview -> save -> export -> hashes/quality notes.

UPSCALE:
approved UI -> approved photo -> Intel SISR CPU -> actual 4x output -> reopen/dimension validation -> Preview -> save -> export -> hashes/quality notes.

## 7. VIDEO and Korean audio manual gate
Search approved project folders one final time only if new material has appeared since v17.
If still absent, present the user with exactly two file-picker actions:
A. Select one owned/approved moving-subject video.
B. Select or record one owned/approved spoken-Korean audio sample.
Do not ask for paths typed into chat if a secure/local file picker is available.
Do not use silent audio or unrelated personal media.

## 8. Execute remaining lanes immediately after selection
VIDEO:
real video -> SAM tracking -> output decode/continuity -> Preview -> save -> export.

KOREAN STT:
real spoken Korean -> whisper-small CPU -> transcript -> Preview -> save/export.

Record input/output bytes, hashes, runtime, adapter/model identity and practical quality notes.

## 9. Integrated PC-local E2E
When all four lanes have real outputs, verify the actual user flow:
upload/reference -> natural-language/action -> execute/status -> Preview/original-result -> optional undo/redo/retry -> project save -> export.
No remote Evidence may substitute for local output.

## 10. Regression and evidence
Run Python/UI/server/evidence regressions.
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_LOCAL_FINAL_EXECUTION_REVIEW_v19.0_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_LOCAL_FINAL_EXECUTION_v19_20260924.json
Preserve all prior Evidence.

## 11. Verdict
Only actual local evidence can produce PC_LOCAL_FINAL_E2E_PASS.
If credential UI or two files still require the user, report exactly which one-click/manual action remains, while preserving any PHOTO/UPSCALE PASS already achieved.

## 12. Automatic next-directive rule
After verification, immediately create and commit the next directive under docs/commander/ and report its path + commit SHA. A review without a committed next directive is incomplete.

## 13. Protection
UI_SSOT_CHANGED:NO.
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, secret exposure, legacy fallback, or Evidence overwrite.
