# MINDLE MEDIA AI — PC MANUAL GATE HANDOFF & IMMEDIATE RESUME DIRECTIVE v21.1
Date: 2026-09-24
Status: USER_ACTION_REQUIRED_THEN_AUTO_RESUME
Base: PR #15 head 93f6d8dd88524636a97c41d9f08e37ccb4e91a9b

## 1. Commander verdict
v20.1 Evidence verified. REWORK_TRUE_MANUAL_GATE is correct.
Do not run another environment/readiness review before the manual actions.
Do not create another blocker-only report.

## 2. Preserve
Keep v13 closeout, v14 UI review, v15 46-pass regression, UI tests and server health unchanged.
UI_SSOT_CHANGED:NO.

## 3. Present exactly three manual actions in the PC Work UI
A. SECURE HF CREDENTIAL
Open the approved secure credential/secret entry path for the existing scoped HF token.
The user must never paste the token into chat or terminal.
After entry, record only AUTH_AVAILABLE:true/false.

B. VIDEO INPUT
Open the local file picker and ask the user to select one owned/approved moving-subject video.

C. KOREAN AUDIO INPUT
Open the local file picker or recording control and ask the user to select/record one owned/approved spoken-Korean sample.

Do not ask the user to manually copy paths when a picker is available.
Do not use silent audio.

## 4. Automatic resume after A/B/C
Do not wait for another commander directive after the three actions.
Immediately:
1. authenticate to the frozen Private HF cache;
2. materialize SAM 2.1, whisper-small, Intel SISR;
3. verify exact revision/bytes/hash/provenance;
4. install/expose free local OpenVINO CPU and ffmpeg; Selenium/Chrome/PyArrow only if actually needed;
5. rerun health/preflight.

## 5. Execute four lanes
PHOTO: existing real architecture photo -> SAM segmentation -> Preview -> save -> export.
UPSCALE: approved photo -> Intel SISR CPU -> true 4x output -> Preview -> save -> export.
VIDEO: selected video -> SAM tracking -> continuity/decode -> Preview -> save -> export.
KOREAN STT: selected/recorded speech -> whisper-small -> transcript -> Preview -> save/export.

## 6. Quality and Evidence
Record actual input/output bytes + hashes, model identities, runtime, quality notes.
PHOTO boundary; VIDEO continuity; UPSCALE dimensions/artifacts; STT transcript accuracy; Preview/export consistency.

## 7. Regression
Python/UI/server/evidence/package regression must remain PASS.

## 8. Final Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_MANUAL_GATE_COMPLETION_REVIEW_v21.1_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_MANUAL_GATE_COMPLETION_EVIDENCE_v21_1_20260924.json
Commit to non-main branch and create/update draft PR.

## 9. Final verdict
Only declare PC_LOCAL_FINAL_E2E_PASS when all four lanes + Preview + project save + export + regression have actual PC-local Evidence.

## 10. Automatic next directive
Immediately after verification, create/commit the next directive under docs/commander and report path + SHA.
No repeated readiness loop.

## 11. Protection
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, legacy fallback, secret exposure, or prior Evidence overwrite.
