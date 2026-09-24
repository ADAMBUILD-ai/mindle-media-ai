# MINDLE MEDIA AI — Adopted Runtime Restore and Quality Rerun Directive v27.0

Date: 2026-09-24  
Status: REWORK — RESTORE EXACT ASSETS

Base: v26.1 PC E2E review

1. Restore only the frozen adopted assets: SAM 2.1 Hiera Base Plus, whisper-small, and Intel SISR 1032. Use the verified Private HF/cache route or an authenticated offline package. Verify revision, weight identity, and hashes before load.
2. Restore a free CPU OpenVINO runtime and ffmpeg from an approved offline/portable/authenticated package route. Do not repeat a blocked public pip attempt as the only method.
3. Rerun PHOTO segmentation on the recovered photo and fix the boundary quality failure.
4. Rerun Intel SISR 4× and reject black/invalid output; verify dimensions, non-black content, and visual detail.
5. Rerun VIDEO tracking and Korean STT locally using the recovered inputs. Preserve the input hashes.
6. Complete actual Preview -> save -> export for each lane and record output hashes.
7. Run Python/UI/server/evidence/package regressions. Preserve all prior Evidence and keep `UI_SSOT_CHANGED:NO`.
8. No legacy fallback, GPU, paid compute, credentials in evidence, main merge, Production deploy, or force push.
9. Create a new review and machine-readable Evidence after the rerun. PASS only actual local quality-verified results.
