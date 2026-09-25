# MINDLE MEDIA AI — RETRY PACKAGE VERIFIED / PC DOWNLOAD COMPLETION DIRECTIVE v29.1
Date: 2026-09-25
Status: EXECUTE NOW
Base: PR #22 head aa982d02abdd07b7eaf00bb2b06d07533fc98006

## Commander verification
The retry succeeded remotely. Freeze these as PASS:
- Remote verified runtime package run 35978017242: SUCCESS
- Product E2E run 35978017154: SUCCESS
- Canonical run 35978017407: SUCCESS
- License Gate run 35978017133: SUCCESS

New retry artifacts are the authoritative transfer set:
- part-00 artifact 10799530708 / 419251254 bytes / sha256 0496522c4d9663e52cf0f496bf84873e2d4218d6a3b7ea72631e26f9a525b729
- part-01 artifact 10799495855 / 418706321 bytes / sha256 6fa59e2f27bc00ed98279fe0195de12f2da397e11db0632f0bc85cde5df981c2
- part-02 artifact 10799162472 / 78665471 bytes / sha256 2265d46f5a8987590d4d49c7398de8658990036e31426b047bfe418add34e185

Do not use the older failed/previous transfer artifacts when these retry artifacts are available.

## Mandatory execution
1. Download all three new artifacts to the approved PC staging folder using the proven GitHub artifact UI.
2. If one part fails, retry only that part until its local file exists; do not restart successful parts.
3. Verify each local byte size and SHA-256 against the values above before extraction.
4. Extract/reassemble according to package manifest and inventory exact SAM 2.1, whisper-small, Intel SISR and packaged OpenVINO assets.
5. Verify exact model revisions/hashes/license manifest before load.
6. Install/expose packaged OpenVINO CPU. Use OpenCV video path if supported; do not block solely on ffmpeg.
7. Run PHOTO quality rework first: correct prompt/coordinate/mask selection as needed; old wrong overlay is rejected.
8. Run UPSCALE quality rework second: correct normalization/layout/range/channel/encoding as needed; old black output is rejected.
9. Run recovered VIDEO locally with SAM tracking.
10. Run recovered Korean speech locally with whisper-small.
11. Every lane must reach actual local output -> Preview -> project save -> export -> quality review.
12. Run Python/UI/server/evidence/package regressions.

## Failure handling
Do not stop at “download failed”. Re-open the exact failed artifact Download control and retry that part.
Do not stop at “model missing” after package extraction; reconcile package manifest and extracted paths.
Do not stop at bad output; diagnose adapter/pre/postprocessing and rerun.
If exact model remains unusable only after verified package restore and adapter correction, then direct-shop an official CPU-compatible replacement under the existing perpetual-use license gate.

## Evidence
Create a new review + JSON with local paths, sizes, hashes, extraction inventory, model/runtime load results, adapter fixes, actual outputs, quality, Preview/save/export, regressions and exact failed part if any.

## Verdict
Remote retry package is PASS and must not be redone.
PC_LOCAL_FINAL_E2E_PASS only after all four local lanes and product flow pass quality.

## Automatic next directive
After verification, immediately create/commit next directive under docs/commander.

## Protection
UI_SSOT_CHANGED:NO. No redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.
