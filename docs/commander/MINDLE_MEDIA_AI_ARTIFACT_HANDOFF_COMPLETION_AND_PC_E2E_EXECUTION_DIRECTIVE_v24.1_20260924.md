# MINDLE MEDIA AI — ARTIFACT HANDOFF COMPLETION & PC E2E EXECUTION DIRECTIVE v24.1
Date: 2026-09-24
Status: EXECUTE / ONE MANUAL TRANSFER IF REQUIRED
Base: PR #17 head 047b8755830bf1f77bf0321e3dae49dc1d990205

## Commander verdict
v23.1 = PARTIAL PASS + REWORK.

PASS:
- authenticated connector retrieval of artifact metadata/reference
- exact artifact identity/size/digest preserved
- actual offline dependency/cache searches performed
- no fabricated local PASS, no legacy fallback, no UI/SSOT change

REWORK:
- artifact bytes are still not present in the PC staging directory
- no local digest verification/extraction
- no recovered source inputs
- no PC-local lane execution
These items remain mandatory.

## 1. Complete the artifact handoff
Target artifact:
- run 35596903385
- artifact 10636679053
- size 228,710,107 bytes
- expected SHA-256 aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5

If Work can surface the approved GitHub artifact Download control, do so now.
Ask the user only to save the ZIP into the project-approved local transfer folder and confirm/select the resulting file.
Do not ask for credentials.
Do not repeat network/download experiments already proven blocked unless the environment changed.

## 2. Verify before extraction
Once the local ZIP exists:
- record exact path
- verify exact bytes
- calculate SHA-256
- compare to expected digest
Mismatch => REWORK, no extraction.

## 3. Extract and inventory
Extract to a new project-local staging folder.
Inventory:
- approved source photo
- approved source video if present
- approved 16 kHz Korean speech if present
- prior output evidence
- model/cache payloads if included
Record bytes/hash/provenance for each.
Do not overwrite prior Evidence.

## 4. Restore adopted runtime assets
Restore only verified adopted SAM 2.1, whisper-small and Intel SISR 1032.
If the artifact does not contain model payloads, use its evidence/manifests to drive the approved Private HF/cache restore path.
Verify exact identity before load.
No legacy fallback.

## 5. Dependencies
Use existing/portable/offline free CPU dependencies when available.
If OpenVINO or ffmpeg is still absent after local artifact/package inventory, surface one precise installer/package action rather than a generic blocker.
No GPU or paid compute.

## 6. Execute lanes
Run each lane as soon as ready:
PHOTO -> SAM segmentation -> actual output -> Preview -> save -> export.
UPSCALE -> Intel SISR -> actual 4x -> dimensions/reopen/hash -> Preview -> save -> export.
VIDEO -> recovered approved source video or one user-selected video -> SAM tracking -> continuity/decode -> Preview -> save -> export.
KOREAN STT -> recovered approved spoken Korean or one user-selected/recorded sample -> whisper-small -> transcript -> Preview -> save/export.

## 7. Quality
PHOTO boundary usability; VIDEO continuity; UPSCALE artifact/detail and true dimensions; STT transcript errors; Preview/export consistency.
Actual evidence required for PASS.

## 8. Regression
Run Python/UI/server/evidence/package regressions. Preserve prior PASS baseline.

## 9. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_ARTIFACT_HANDOFF_PC_E2E_REVIEW_v24.1_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_ARTIFACT_HANDOFF_PC_E2E_EVIDENCE_v24_1_20260924.json
Include local ZIP verification, extraction inventory, restored models/dependencies, lane outputs/hashes/quality, Preview/save/export and regression.

## 10. Verdict
PASS only what actually passed.
REWORK any failed restore/runtime/quality item.
If a human action remains, state exactly one concrete action and continue all other lanes.

## 11. Automatic next directive
After verification, immediately create and commit the next directive under docs/commander and report path + commit SHA.

## Protection
UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or Evidence overwrite.
