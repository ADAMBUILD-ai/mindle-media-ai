# MINDLE MEDIA AI PC Local VIDEO/STT and Approved-UI Completion Directive v32.0

## Starting point

Work from `c5b559793ffaea5e5fc1fb8eaa4c63a7c123fbd2`. Preserve every frozen PASS in the v30 review. Do not re-download or re-package already materialized exact models unless a byte check fails. Do not modify UI SSOT, merge main, force-push, use GPU, Production, or paid compute.

## Required recovery and verification

1. In a fresh PC-local Python 3.11 process, diagnose the reproducible `import torch` termination with a file-backed probe. Keep packages isolated under the task output/runtime directory; do not overwrite the global Python installation.
2. Once the probe reaches `torch-loaded`, use the retained exact SAM 2.1 model and the actual 125-frame / 24fps `big_buck_bunny.mp4` input. Produce 4 evenly-spaced tracking overlays, tracking JSON, a decodable preview, and visual continuity review. Require real non-degenerate masks; do not accept mere process success.
3. Use retained exact Whisper-small and the real FLEURS Korean WAV. Save the transcript, show Hangul output, and calculate WER against the preserved reference. Apply the existing `<= 0.75` quality gate.
4. Materialize the current branch source without altering UI SSOT and run the approved local browser flow: real PHOTO segmentation, repaired Intel SISR 4×, VIDEO tracking, Korean STT, Preview, project save, and export. Preserve screenshot, project, export, hashes, and model receipts.
5. If local quality gates pass, create a final PASS review. Otherwise write an evidence-backed REWORK review naming only the remaining failing gate and the exact next action.

## Required closeout paths

- `evidence/pc_remote/MINDLE_MEDIA_AI_PC_LOCAL_VIDEO_STT_UI_E2E_EVIDENCE_v32_20260925.json`
- `docs/commander/MINDLE_MEDIA_AI_PC_LOCAL_VIDEO_STT_UI_E2E_REVIEW_v32.0_20260925.md`

Commit the evidence and review on this branch and report their paths and commit SHA.
