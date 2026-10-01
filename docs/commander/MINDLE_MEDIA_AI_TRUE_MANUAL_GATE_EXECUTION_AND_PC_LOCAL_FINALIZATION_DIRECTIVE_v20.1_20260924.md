# MINDLE MEDIA AI — TRUE MANUAL GATE EXECUTION & PC LOCAL FINALIZATION DIRECTIVE v20.1
Date: 2026-09-24
Status: EXECUTE NOW
Repository: ADAMBUILD-ai/mindle-media-ai
Base: PR #14 head 0a1aadc6808d2e9de93175ecd3e697cb7e9e6d61

## 1. Commander correction
Do NOT repeat v19 review, v20 readiness report, or prior blocker report.
The next work is execution at the true manual gate.
Existing PASS baselines remain immutable.

## 2. Current verified state
PASS and preserve:
- v13 FINAL CLOSEOUT Evidence
- v14 UI/UX review
- v15 Python regression 46 PASS
- UI structure/interaction PASS
- Product server health HTTP 200
- approved UI/SSOT unchanged

Still required:
A. secure availability of the existing scoped HF credential to the PC-local process
B. one owned/approved moving-subject video
C. one owned/approved spoken-Korean audio sample
D. adopted cache materialization and free local runtime dependencies

## 3. First action — stop document-only looping
Do not create another review merely stating that A/B/C are missing.
Attempt the executable path first.
A report that only repeats the same blockers without opening/performing the next actionable gate is REWORK.

## 4. Secure HF credential gate
Use the existing approved scoped HF credential. Never request the token in chat.
Try approved secure paths in this order:
1. existing PC/Work secret or environment credential already configured;
2. approved GitHub/HF authenticated session available to Work;
3. secure local credential/secret input UI.
If user action is required, surface the secure input UI and ask for only that action.
Record only AUTH_AVAILABLE:true/false. Never print the token.

## 5. Materialize adopted models
Immediately after AUTH_AVAILABLE:true, materialize the frozen adopted Private HF revision and verify exact identities for:
- SAM 2.1
- whisper-small
- Intel single-image-super-resolution-1032
Validate revision, filename, bytes, hash, license/provenance manifest.
No legacy fallback. Any mismatch => fail closed.

## 6. Install/expose free local dependencies
Proceed without additional approval if free/local and within current scope:
- OpenVINO CPU
- ffmpeg
- Selenium/Chrome/Chromedriver only if actually required
- PyArrow only if selected route requires it
Record version/path. No GPU, no paid compute.

## 7. Execute available lanes immediately
PHOTO and UPSCALE already have approved inputs. Once auth/cache/dependencies are ready, run them immediately.
PHOTO: UI -> real photo -> SAM segmentation -> output -> Preview -> project save -> export.
UPSCALE: UI -> real photo -> Intel SISR CPU -> real 4x output -> reopen/dimensions -> Preview -> save -> export.
Preserve input/output hashes and quality notes.

## 8. VIDEO manual input gate
Search only for newly available approved material once. If absent, open local file picker and request:
“Select one owned/approved moving-subject video for final tracking test.”
After selection, record provenance/bytes/SHA and execute SAM tracking through UI to Preview/save/export.

## 9. Korean audio manual input gate
If no approved spoken Korean exists, open local file picker/recording route and request:
“Select or record one owned/approved spoken-Korean sample for final STT test.”
Silent audio is prohibited as PASS evidence.
After selection execute whisper-small CPU STT through UI and validate transcript/Preview/save/export.

## 10. Integrated PC-local E2E
After all four lanes have real outputs, execute the complete real user flow:
upload/reference -> natural-language/action -> execution/status -> Preview/original-result -> undo/redo or retry where applicable -> project save -> export.
Remote GitHub E2E cannot substitute for PC-local evidence.

## 11. Quality gate
PHOTO: segmentation boundary practical usability.
VIDEO: tracking continuity and decodable output.
UPSCALE: true 4x dimensions, reopen, artifacts/detail.
STT: actual Korean transcript and obvious error review.
Preview/export: result consistency.
Record PASS/REWORK by lane.

## 12. Regression
Run Python regression, UI structure/interaction, server health, Evidence/package validation.
Existing 46 PASS baseline must not regress.

## 13. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_TRUE_MANUAL_GATE_FINAL_REVIEW_v20.1_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_TRUE_MANUAL_GATE_EVIDENCE_v20_1_20260924.json
Include auth boolean only, cache identities/hashes, dependency versions, actual input/output hashes, Preview/save/export, quality notes, regression, changed files, commit/PR/Actions.

## 14. Final verdict
PC_LOCAL_FINAL_E2E_PASS only when PHOTO + VIDEO + UPSCALE + KOREAN_STT + Preview + save + export + regression all have real PC-local Evidence.
If user action remains, show the actual secure/file-picker gate; do not substitute another document-only blocker report.

## 15. Automatic next-directive rule
Immediately after verification:
- issue verdict;
- create next directive;
- commit it under docs/commander/;
- report path + commit SHA.
No verification cycle is complete without this.

## 16. Protection
UI_SSOT_CHANGED:NO.
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, secret exposure, legacy fallback, or prior Evidence overwrite.
