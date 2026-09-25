# MINDLE MEDIA AI — PC MATERIALIZATION REWORK / LOCAL E2E RESUME DIRECTIVE v31.0

Date: 2026-09-25
Branch: work/v28-1-remote-runtime-package-20260924
PR: #22
Head verified: 1cc7dca6f3e036cdb578200a20dd6afa068692c8
UI_SSOT_CHANGED: NO

## Frozen PASS

The following completed work is frozen and must not be repeated:

- Remote verified runtime package run 36080222640: SUCCESS.
- Product E2E run 36080222666: SUCCESS.
- Remote package artifacts:
  - part-00: artifact 10841268185, 419251242 bytes, sha256 `a22e3a19736046ea91d54cbd4c2884f7d9d9927b9ead04c028b6d65e4603e320`.
  - part-01: artifact 10842016031, 418706328 bytes, sha256 `9edd243dcde132017d680bc88a380f00a20ebe4eddc019e2ef4977821d6eae26`.
  - part-02: artifact 10841594538, 78665478 bytes, sha256 `23aa0df8dd5987d0e7fb46c0c8ca17888d61f5153252839c01341b8deada81cd`.
- The package job completed all exact payload, runtime-wheel, manifest, and artifact-upload steps.
- Product E2E completed real-input/output capture, FINAL_PASS validation, and Evidence preservation.
- No UI redesign, main merge, Production deployment, force push, GPU, paid compute, or credential exposure occurred.

## Current REWORK finding

PC_LOCAL_FINAL_E2E is not PASS.

- part-00 was materialized to the approved PC output folder:
  `outputs/artifact-10841268185.zip`
- Its local size is 419251242 bytes and its local SHA-256 matches the authoritative artifact digest.
- part-01 and part-02 are not yet materialized. Direct signed-download access is blocked by the Windows socket policy; the in-app browser reports `ERR_BLOCKED_BY_CLIENT`.
- Because the three-part package is incomplete, extraction/reassembly, exact SAM 2.1 / whisper-small / Intel SISR / OpenVINO inventory, local CPU loading, adapter correction, and local PHOTO/UPSCALE/VIDEO/Korean-STT quality gates remain open.
- The existing wrong PHOTO target selection and black 4x upscale output remain rejected Evidence; they are not promoted to PASS.
- Preview, project save, export, and local regression closeout are not claimed.

## Next execution

1. Keep part-00 and its verified digest frozen.
2. Materialize only missing part-01 and part-02 through an approved GitHub Artifact download path; do not restart the successful remote workflow.
3. Verify each local byte size and SHA-256 before extraction.
4. Reassemble/extract the package and inventory exact pinned models and free CPU OpenVINO runtime.
5. Run PHOTO segmentation quality rework, correcting target selection and adapter preprocessing/postprocessing.
6. Run 4x upscale quality rework, correcting normalization, layout, range, channel, and encoding handling.
7. Run recovered VIDEO tracking and Korean STT locally on CPU.
8. For every lane, verify actual output -> Preview -> project save -> export -> quality review.
9. Preserve all previous Evidence, append actual local paths and hashes, then run regressions.
10. Create the next commander review immediately after the local gate changes.

## Verdict

- REMOTE_PACKAGE_AND_PRODUCT_E2E: PASS / FROZEN
- PC_LOCAL_FINAL_E2E: REWORK / TRANSFER_INCOMPLETE
- Do not declare overall PASS until missing parts are digest-verified and all four local quality lanes plus Preview/save/export pass.

Protection: UI_SSOT_CHANGED:NO. No main merge, Production deployment, force push, GPU, paid compute, credential exposure, or Evidence overwrite.
