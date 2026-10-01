# MINDLE MEDIA AI — PC RUNTIME RESTORE & REAL LOCAL E2E CLOSEOUT DIRECTIVE v15.0
Date: 2026-09-24
Status: EXECUTE IMMEDIATELY
Repository: ADAMBUILD-ai/mindle-media-ai
Base review: PR #11 / head 169161cecf78c0ac82da2b58321e842c6636cfb3

## 1. Commander decision
PR #11 v14 review is accepted as an honest PC_MANUAL_GATE result, not a final local PASS.
Do not repeat the review. Resolve the recorded blockers and execute the real PC-local E2E.

## 2. Verified v14 blockers
- PHOTO segmentation: PC_MANUAL_GATE — real local photo exists, but adopted SAM runtime/weights and product server are absent in the PC checkout.
- VIDEO tracking: BLOCKED_INPUT — no owned local video fixture; ffmpeg missing from PATH.
- 4x upscale: PC_MANUAL_GATE — real input exists, but adopted Intel SISR runtime/adapter is absent locally.
- Korean STT: BLOCKED_INPUT — only silent WAV exists; no owned spoken-Korean input and adopted Whisper-small runtime absent locally.
- Preview / project save / export: NOT_PROMOTED_TO_LOCAL_PASS.
- UI/UX review: PASS.
- Python regression: 46 PASS.
- UI structure/interaction: PASS.
- UI_SSOT_CHANGED: NO.

## 3. Non-negotiable baseline
Preserve v13 FINAL CLOSEOUT, PR #10 evidence, Private HF immutable model cache, adopted-model manifest, license evidence, and approved UI/SSOT.
No UI redesign.
No main merge, Production deploy, force push, GPU, or paid compute.
Never expose secrets/tokens.

## 4. Execution sequence

### STEP 1 — Materialize the correct product runtime locally
Bring the PR #10/v13 final product runtime tree into the PC-local working checkout without overwriting v13 evidence.
Verify the exact source commit/revision used and record it.
The PC checkout must contain the real product server/backend, adopted adapter code, and UI bridge required by the final Product E2E.

### STEP 2 — Restore adopted verified model cache
Connect the PC runtime to the frozen Private HF adopted-model revision referenced by v13.
Restore only the adopted release models:
- SAM 2.1 for PHOTO/VIDEO segmentation/tracking.
- whisper-small for Korean STT.
- Intel single-image-super-resolution-1032 for 4x upscale.
Verify exact revision/file identity/hash/license manifest before load.
Do not silently fall back to legacy Whisper Large or RealESRGAN.

### STEP 3 — Local dependency preflight
Verify Python/runtime dependencies and CPU providers.
Resolve ffmpeg availability for VIDEO processing using an approved free/local path. Do not install unrelated software.
Record executable/version/path.
Verify local product server startup and health check without changing UI SSOT.

### STEP 4 — Real input acquisition
Use owned/approved real inputs only.
PHOTO: existing real architecture image may be used after hash verification.
UPSCALE: existing benchmark/photo input may be used after hash verification.
VIDEO: search project Work/assets/demo/evidence/test and approved local folders for a usable real video first. If absent, request/provide one explicit PC_MANUAL_INPUT gate; do not fabricate a PASS.
KOREAN_AUDIO: search for a real spoken-Korean recording. Reject silence/synthetic-only evidence as final manual PASS unless explicitly approved for test scope.
For every input record path, bytes, SHA-256 and provenance.

### STEP 5 — PHOTO real local E2E
Approved UI -> upload real photo -> execute SAM segmentation -> real output -> Preview -> project save -> export.
Record output files, bytes, SHA-256, runtime duration, adapter/model identity.
Visually inspect mask boundary usability.

### STEP 6 — VIDEO real local E2E
Approved UI -> upload real video -> execute SAM tracking -> real tracking output -> Preview -> project save -> export.
Verify frame continuity/object retention and output decodability.
Record input/output hashes and ffmpeg/runtime evidence.

### STEP 7 — 4x UPSCALE real local E2E
Approved UI -> real photo -> Intel SISR CPU inference -> 4x output -> Preview -> project save -> export.
Verify actual dimensions, output reopen, bytes/SHA-256, visible artifacts and practical quality.

### STEP 8 — Korean STT real local E2E
Approved UI -> real spoken Korean audio -> whisper-small CPU inference -> actual transcript -> Preview -> project save/export evidence.
Record transcript, input/output hashes, runtime and obvious transcription errors.

### STEP 9 — Product usability verification
Confirm the user path remains simple:
upload/reference -> natural-language instruction/action -> execute -> progress/status -> Preview -> optional undo/redo or retry -> save/export.
Do not expose model/GPU/raw-adapter controls in the beginner path.
Any newly discovered usability issue must be classified REQUIRED / OPTIONAL / REMOVE-HIDE.
Visual SSOT changes require commander approval before modification.

### STEP 10 — Fix/retest loop
Any failure: Evidence -> root cause -> minimal permitted fix -> rerun affected lane -> rerun regression.
Do not stop after restating a blocker if a safe remediation exists.
Do not convert remote GitHub E2E evidence into a local PASS.

### STEP 11 — Regression
Run Python regression, UI structure/interaction, Evidence sync/package validation and relevant local integration tests.
Existing 46 PASS baseline must not regress.

### STEP 12 — Evidence and repository preservation
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_LOCAL_REAL_E2E_CLOSEOUT_v15.0_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_LOCAL_REAL_E2E_v15_20260924.json
Include all input/output hashes, model identities, local dependency versions, Preview/save/export status, and lane verdicts.
Commit to a non-main work branch and create/update a PR.
Verify Actions/Checks when applicable.

## 5. Final gate
Declare PC_LOCAL_FINAL_E2E_PASS only if all are actual local PASS:
- PHOTO segmentation
- VIDEO tracking
- 4x upscale
- Korean STT
- Preview
- project save
- export
- regression
- UI usability final review
- UI_SSOT_CHANGED:NO
- v13 immutable baseline preserved

If any real input still requires the user, report exactly PC_MANUAL_INPUT_REQUIRED with the one missing input and continue every other executable lane.

## 6. Mandatory automatic next-directive rule
Immediately after verification, do not wait for another user request.
1. Produce PASS/REWORK/BLOCKED verdict from actual Evidence.
2. Create the next-stage commander directive based on that verdict.
3. Save that directive under docs/commander/ in this GitHub repository.
4. Commit it to the active non-main work branch.
5. Report the exact directive path and commit SHA.
A verification report without the next directive committed to GitHub is INCOMPLETE.

## 7. Final instruction
Execute now. The objective is not another readiness report; it is to restore the actual adopted runtime on the PC and complete as much real local E2E as physically possible. Preserve all existing PASS evidence. Never claim PASS without real local input/output evidence.
