# MINDLE MEDIA AI — Local Artifact Verification and PC E2E Continuation Directive v26.0

Date: 2026-09-24  
Status: WAITING FOR LOCAL ZIP

When the user-saved ZIP exists in `work/v23_1_transfer`:

1. Verify exact size 228,710,107 bytes and SHA-256 `aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5`; abort extraction on mismatch.
2. Extract to a new staging folder and inventory/hash all approved photo, video, Korean 16 kHz speech, prior outputs, evidence, and model payloads.
3. Restore only the adopted SAM 2.1, whisper-small, and Intel SISR 1032 assets using the frozen manifest. No fallback or rescout.
4. Use free CPU dependencies from available offline/portable sources; record OpenVINO and ffmpeg status.
5. Run PHOTO and UPSCALE first, then VIDEO and Korean STT. Every lane must produce actual output, Preview, save, export, quality review, and hashes.
6. Run Python/UI/server/evidence/package regressions and preserve prior Evidence.
7. Publish a new review and JSON; do not claim PC-local PASS from remote evidence.
8. Keep UI_SSOT_CHANGED:NO and protection constraints: no redesign, main merge, production deploy, force push, GPU, paid compute, credentials, or legacy fallback.
