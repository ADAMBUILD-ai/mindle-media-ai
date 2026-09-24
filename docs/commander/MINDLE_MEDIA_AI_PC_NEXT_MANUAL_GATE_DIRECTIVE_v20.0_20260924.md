# MINDLE MEDIA AI — PC NEXT MANUAL GATE DIRECTIVE v20.0

Date: 2026-09-24
Status: WAITING_FOR_EXPLICIT_LOCAL_USER_ACTION
Base: v19 execution review and evidence

## Commander verdict

v19 correctly reached the smallest unavoidable manual gate. Do not repeat readiness review and do not redesign the UI.

## Exact actions required

1. Use the approved secure local credential UI to make the existing scoped Hugging Face credential available to the PC-local process. Never paste the token into chat, terminal history, source, logs, PR, or Evidence.
2. Use the local file picker to select one owned/approved moving-subject video.
3. Use the local file picker to select or record one owned/approved spoken-Korean audio sample.

Do not use silent audio or unrelated personal media.

## After the three actions

- Verify credential availability only as a boolean.
- Materialize and hash-verify the frozen SAM 2.1, whisper-small, and Intel SISR caches.
- Expose/install only free local dependencies actually required: OpenVINO CPU and ffmpeg first; Selenium/Chrome only if UI automation is needed; PyArrow only if required by the selected path.
- Execute PHOTO and 4x UPSCALE immediately using the existing approved inputs.
- Execute VIDEO and Korean STT after the selected files are available.
- Validate Preview, original/result comparison, save, export, output hashes, dimensions/continuity, and transcript notes.
- Run Python/UI/server/evidence regressions.
- Create the next review and next directive with exact commit/PR/Actions status.

## Protection

UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, secret exposure, legacy fallback, or prior Evidence overwrite.
