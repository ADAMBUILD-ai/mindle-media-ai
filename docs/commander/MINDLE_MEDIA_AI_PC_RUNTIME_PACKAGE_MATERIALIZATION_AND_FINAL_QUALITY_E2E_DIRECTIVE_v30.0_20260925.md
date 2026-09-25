# MINDLE MEDIA AI — PC RUNTIME PACKAGE MATERIALIZATION & FINAL QUALITY E2E DIRECTIVE v30.0
Date: 2026-09-25
Status: EXECUTE IMMEDIATELY
Base: PR #22 head 16e16f06f217110131afcb01b9ecb02a93e6a19a

## Commander verified PASS — DO NOT REDO
The following remote stage is closed as PASS:
- Remote Runtime Package run 36083578677: SUCCESS
- Product E2E run 36083578769: SUCCESS
- Canonical run 36083578635: SUCCESS
- License Gate run 36083578662: SUCCESS
- runtime artifacts part-00/01/02 created and available

Do not repeat remote model acquisition or packaging unless local digest verification fails.

## 1. Download all three verified runtime artifacts to PC
Materialize:
- part-00 artifact 10843068098
- part-01 artifact 10842833582
- part-02 artifact 10843043178
Use the proven GitHub artifact download route.
Store in one approved project staging directory.

## 2. Verify before extraction
Verify local sizes and artifact digests against GitHub records.
Any failed part: redownload only that part.
All verified parts: continue automatically.

## 3. Extract/reassemble runtime package
Follow package manifest.
Inventory and verify exact adopted assets:
- SAM 2.1
- whisper-small
- Intel SISR 1032
- packaged OpenVINO CPU runtime
Verify revision/bytes/hash/provenance before load.
No legacy fallback.

## 4. Local runtime health
Load all three adopted models on CPU.
Verify OpenVINO runtime.
Use existing OpenCV video path where valid; ffmpeg must not block VIDEO if OpenCV path satisfies adapter requirements.
Record load/runtime health.

## 5. PHOTO — mandatory quality fix
Use recovered approved photo.
Run actual local SAM 2.1.
The previous wrong-subject overlay is REJECTED and cannot be reused.
Inspect/fix resize, coordinate mapping, prompt point/box mapping, mask selection and overlay transform.
PASS only when intended subject has practically usable boundary.
Record before/after output and hash.

## 6. UPSCALE — mandatory quality fix
Use recovered approved photo.
Run actual local Intel SISR/OpenVINO.
The previous black 4x image is REJECTED and cannot be reused.
Inspect/fix normalization, dtype, NCHW/NHWC, tensor names, output range, channel order, clipping and encoding.
PASS requires true 4x dimensions, non-black content, reopen success and useful visual detail.

## 7. VIDEO local tracking
Use recovered valid 125-frame / 24fps video.
Run actual local SAM tracking.
Validate continuity, decodability and output hash.
Then Preview -> project save -> export.

## 8. Korean STT local execution
Use recovered valid 16kHz / 12.48s Korean speech.
Run actual local whisper-small.
Review transcript quality and obvious errors.
Then Preview -> save/export.

## 9. Approved UI full E2E
Execute all four functions through the approved UI/runtime:
real input -> execute/status -> real output -> Preview -> save -> export.
UI_SSOT_CHANGED:NO.

## 10. Quality gate
Process SUCCESS alone is not PASS.
PHOTO boundary, VIDEO continuity, UPSCALE detail/non-black, STT transcript, Preview/export consistency must each be evidence-backed PASS.
Any failed lane => fix adapter/runtime and rerun only that lane.

## 11. Regression
Run Python/UI/server/evidence/package regressions.
Preserve all prior Evidence and remote PASS baselines.

## 12. Final Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_FINAL_QUALITY_E2E_REVIEW_v30.0_20260925.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_FINAL_QUALITY_E2E_EVIDENCE_v30_20260925.json
Include local artifact paths/digests, extraction inventory, model/runtime identity, adapter fixes, actual input/output hashes, quality verdicts, Preview/save/export, regression, commit/PR/Actions.

## 13. Final verdict
If all four lanes + Preview + save + export + regression pass:
PC_LOCAL_FINAL_E2E_PASS: PASS
MINDLE_MEDIA_AI_PC_FINAL_QUALITY_CLOSEOUT: PASS

If any lane fails, mark only that lane REWORK and continue immediately. Do not reopen already-PASS remote packaging.

## 14. Automatic next directive
After review, immediately create/commit the next directive under docs/commander and report path + commit SHA without waiting for the user.

## Protection
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.
