# MINDLE MEDIA AI PC runtime restore next directive v16.0

Date: 2026-09-24  
Status: `PC_MANUAL_INPUT_AND_RUNTIME_CACHE_REQUIRED`  
Base Evidence: `evidence/pc_remote/MINDLE_MEDIA_AI_PC_LOCAL_REAL_E2E_v15_20260924.json`

## Objective

Resume the real PC-local E2E without changing the approved UI/SSOT or replacing adopted models with legacy, mock, or synthetic results.

## Required before rerun

1. Make the PR #10 adopted private cache available to the PC runtime through the approved credential/cache path. Keep exact revisions and hashes unchanged; do not paste or log the token.
2. Provide one owned/approved moving-subject video file for VIDEO tracking and one owned/approved spoken-Korean recording for STT. Record provenance, bytes, and SHA-256.
3. Install or expose only the approved free/local dependencies needed by the restored runtime: OpenVINO CPU, Selenium/Chrome for UI E2E, PyArrow for the FLEURS input reader, and an approved local ffmpeg path.
4. Re-run the server health check, then PHOTO, VIDEO, 4× upscale, and Korean STT lanes independently.
5. Promote Preview/save/export only after a real `TESTED_PASS` job has produced validated output.

## Gate

If any required input or runtime artifact is still absent, keep that lane at `PC_MANUAL_INPUT_REQUIRED` and report the exact missing item. Do not declare `PC_LOCAL_FINAL_E2E_PASS` until all four real local lanes and Preview/save/export have evidence.

## Protection

`UI_SSOT_CHANGED:NO`; preserve v13/v14 Evidence; no main merge, Production deployment, force push, GPU, paid compute, or secret output.

