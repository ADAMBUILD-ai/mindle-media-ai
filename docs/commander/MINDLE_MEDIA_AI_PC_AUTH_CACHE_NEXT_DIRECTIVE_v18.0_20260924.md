# MINDLE MEDIA AI — PC AUTH CACHE NEXT DIRECTIVE v18.0

Date: 2026-09-24
Status: BLOCKED_PENDING_MINIMUM_USER_INPUT
Base: v17 review and evidence on branch work/pc-runtime-v17-auth-input-gate-20260924

## Commander verdict

v17 is an honest REWORK result. Runtime source and regression gates remain accepted. Do not redesign the UI and do not repeat the readiness review.

## Required minimum user action

Use the approved secure credential path to make the existing scoped Hugging Face credential available to the PC-local process. Never paste or commit the token.

Provide two approved local inputs:
- one owned moving-subject video for VIDEO tracking;
- one owned spoken-Korean audio recording for Korean STT.

Silent audio is not acceptable STT evidence. Unrelated personal media is not acceptable without explicit approval.

## Execution after inputs arrive

1. Materialize and hash-verify the frozen SAM 2.1, whisper-small, and Intel SISR caches. Fail closed on any manifest mismatch.
2. Install or expose only the free local dependencies required by the selected runtime: OpenVINO CPU and ffmpeg; add Selenium/Chrome only if UI automation is actually required; add PyArrow only if the selected input path requires it.
3. Rerun the existing Python, UI structure, UI interaction, server health, and evidence regressions.
4. Run PHOTO segmentation, 4x upscale, VIDEO tracking, and Korean STT through the product UI/runtime.
5. Validate Preview, original/result comparison, project save, export, output hashes, dimensions/continuity, and transcript notes.
6. Preserve v13-v17 evidence and report PASS only with PC-local real outputs.
7. Commit only evidence or minimal permitted fixes to a non-main branch and create/update a draft PR.

## Protection

UI_SSOT_CHANGED:NO. No UI redesign, main merge, production deployment, force push, GPU, paid compute, secret exposure, or overwrite of adopted models/evidence.
