# MINDLE MEDIA AI — PC Artifact Materialization Gate and Offline E2E Resume Directive v24.0

Date: 2026-09-24  
Status: WAITING FOR ONE TRANSFER ACTION  
Base: v23.1 review branch `work/v23-1-materialization-review-20260924`

## Required continuation

Resume immediately when the approved artifact ZIP is available at the user-provided local path.

1. Verify the ZIP size is 228,710,107 bytes and SHA-256 is `aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5`.
2. Extract into a project-local staging directory without modifying prior Evidence.
3. Inventory and hash any approved photo, video, and 16 kHz Korean speech inputs and their output evidence.
4. Restore only the adopted SAM 2.1, whisper-small, and Intel SISR 1032 assets; verify revisions and hashes against the frozen manifest.
5. Use free CPU runtime only. Recheck offline locations for OpenVINO and ffmpeg; install only from an already available local package or approved authenticated workflow artifact.
6. Run each lane as soon as its prerequisites exist: PHOTO segmentation, VIDEO tracking, 4x upscale, and Korean STT. Each lane requires actual output, Preview, save, export, and quality review.
7. Record exact paths, sizes, hashes, runtime versions, lane results, and any missing source media. If the archive contains evidence but no source video, request only that missing video via file picker.
8. Keep `UI_SSOT_CHANGED:NO`; no main merge, production deployment, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.

## Verdict

Remote evidence must not be used as a PC-local PASS. A PC-local PASS requires verified local bytes and actual CPU execution for the relevant lane.
