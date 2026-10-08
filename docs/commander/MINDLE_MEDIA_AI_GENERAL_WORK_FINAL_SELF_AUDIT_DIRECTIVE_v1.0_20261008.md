# MINDLE MEDIA AI — GENERAL WORK FINAL SELF-AUDIT DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — GENERAL WORK FINAL SELF-AUDIT
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-GENERAL-WORK-FINAL-SELF-AUDIT-R1
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926

## 0. PURPOSE

Before any PC Work packaging, General Work must inspect the entire MINDLE MEDIA AI product one more time from end to end.

The purpose is to find the class of defects that remain after a team believes development is complete:
- omitted functions
- dead buttons
- UI controls not connected to runtime
- code paths that exist only in tests
- stale / duplicated / conflicting implementations
- save/reopen omissions
- export omissions
- developer-only dependencies
- aspect-ratio regressions
- hidden external/package assumptions

Do not perform a superficial checklist review.
Run and inspect the actual product.

## 1. STARTING POINT / FROZEN PASS

Reuse valid Evidence unless touched by this audit:
- PHOTO real model segmentation PASS
- PHOTO 4x upscale PASS
- VIDEO tracking backend PASS
- browser mp4v failure root-caused with MediaError.code=4
- H.264 / yuv420p / faststart browser Preview PASS
- actual VIDEO browser playback PASS
- Korean STT + UI visibility PASS
- Save / full close / Reopen PASS
- base Export download / SHA / ZIP CRC PASS
- product runner Python 66 PASS / UI 2 PASS
- approved UI visual identity preserved
- main unchanged
- PR #23 HOLD / DO NOT MERGE

External Marketing/AVORA live integration is DEFERRED for this cycle and must not block General Work closeout.

## 2. OWNER UI LOCK — AUDIT AGAINST THIS

Audit actual implementation against all of the following:

### VIDEO
- approved VIDEO layout remains unchanged except proven defect fixes
- original aspect ratio preserved
- no forced vertical/horizontal stretch
- Preview actually decodes and plays
- timeline and transport remain functional
- VIDEO editing controls are connected, not decorative
- AI conversational command path is connected
- 광고 숏폼 entry remains present

### PHOTO
- landscape-first Preview
- original aspect ratio preserved
- portrait image Auto Fit and centered with natural side margins
- no forced stretch/crop just to fill the box
- brightness
- contrast
- highlights
- shadows
- saturation
- color temperature
- sharpness
- crop
- resize
- rotate
- flip where currently approved
- AI correction
- segmentation/background removal
- color/style/portrait tools where currently exposed
- upscale
- similar/reference image path where currently exposed
- every visible control must have an implemented behavior or be explicitly classified and removed/disabled before PASS

### PRODUCT HEADER / IDENTITY
- title is MINDLE MEDIA AI
- no product title labeled SSOT
- approved dark navy identity preserved
- VIDEO blue/cyan family and PHOTO purple/magenta family preserved
- no broad redesign

## 3. COMPLETE FUNCTION INVENTORY

Build a machine-readable and human-readable inventory from the actual repository and actual UI.

For every visible action and every backend/runtime capability record:
- feature name
- UI entry point
- source implementation path
- runtime/API path
- model/program dependency if any
- input
- output
- persistence behavior
- error behavior
- Evidence status

Classify each:
PASS
PARTIAL
FAIL
NOT_IMPLEMENTED
DEFERRED_EXTERNAL

No UNKNOWN items may remain at final PASS.

Required inventory categories:
- import / media loading
- VIDEO transport
- VIDEO editing tools
- VIDEO tracking
- PHOTO corrections
- PHOTO segmentation
- PHOTO upscale
- Korean STT / subtitle behavior
- AI conversational commands
- project create/save
- close/reopen
- storage paths
- export
- error reporting
- duplicate-job prevention
- retry/idempotency behavior
- browser media compatibility
- external Shortform bridge presence only; live external execution = DEFERRED_EXTERNAL
- update/relaunch behavior needed for local runtime
- process/server lifecycle relevant to later PC Work

## 4. CODE AUDIT

Inspect for:
- dead code
- unreachable routes
- duplicate handlers
- duplicate UI event binding
- hard-coded localhost assumptions that break normal runtime
- dev-only absolute paths
- repo-root assumptions
- Git dependency
- system Python dependency
- pip-at-runtime dependency
- HF token dependency in employee/runtime mode
- external model-cache dependency where local runtime is expected
- stale package assumptions from the abandoned complex employee-installer plan
- OpenCV / NumPy / OpenVINO / Torch version conflicts
- FFmpeg / ffprobe assumptions
- browser codec mismatches
- Windows path quoting / spaces
- UTF-8 / Korean text handling
- port collision / orphan server process
- duplicate server launch
- close/relaunch cleanup
- save-data overwrite/deletion risk
- missing error surfaces
- test-only mocks leaking into runtime
- old Control Plane branches or stale code that can unexpectedly execute

Fix only verified defects and gaps.
Do not rewrite working subsystems without need.

## 5. ACTUAL RUNTIME SELF-AUDIT

Run the product through the approved UI and prove at minimum:

1. fresh launch
2. PHOTO import landscape
3. PHOTO aspect-ratio preservation
4. PHOTO import portrait
5. portrait Auto Fit / centered margins
6. each visible PHOTO correction control changes the actual output/state as designed
7. PHOTO segmentation
8. PHOTO 4x upscale and browser image decode
9. VIDEO import
10. VIDEO aspect-ratio preservation
11. VIDEO play/pause/seek
12. VIDEO tracking and H.264 browser playback
13. Korean STT and visible transcript/subtitle state
14. AI conversational command dispatch for VIDEO
15. AI conversational command dispatch for PHOTO
16. save project
17. fully close
18. reopen
19. restore PHOTO/VIDEO/STT/job state
20. export through actual UI
21. verify exported artifact integrity/hash
22. error-state test for at least one invalid/unsupported input
23. confirm only one product server/runtime instance remains
24. confirm no external Marketing/AVORA call is required for base product operation

If any visible feature cannot be practically tested because its implementation is incomplete, classify it FAIL/PARTIAL and repair it before PASS.

## 6. EXTERNAL SHORTFORM — DEFER, DO NOT DELETE

The following are not part of this General Work PASS:
- real Marketing provider URL/token
- real Marketing HTTP
- approved AVORA asset
- real 9:16 external Shortform Preview
- Representative Approval
- approved advertisement MP4 live export

Requirements during General Work:
- existing button remains
- existing code remains non-destructive
- unavailable external state fails gracefully
- base PHOTO/VIDEO workflow continues
- mark these as DEFERRED_EXTERNAL, not PASS and not FAIL for General Work completion

## 7. REGRESSION

After fixes:
- Python tests >= 66 PASS unless count legitimately changes upward
- UI tests >= 2 PASS
- pip check PASS
- syntax/compile PASS
- Control Plane validator PASS
- targeted tests added for every defect found
- actual runtime receipts for corrected items

Do not claim PASS only from CI if actual runtime was not exercised.

## 8. REQUIRED OUTPUTS

Final Review:
docs/commander/MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_REVIEW_v1.0_20261008.md

Machine Evidence:
docs/evidence/media-ai-general-work-final-self-audit-20261008/EVIDENCE.json

Feature inventory:
docs/evidence/media-ai-general-work-final-self-audit-20261008/FEATURE_INVENTORY.json

Gap register:
docs/evidence/media-ai-general-work-final-self-audit-20261008/GAP_REGISTER.json

UI audit:
docs/evidence/media-ai-general-work-final-self-audit-20261008/UI_RUNTIME_AUDIT.json

Code audit:
docs/evidence/media-ai-general-work-final-self-audit-20261008/CODE_AUDIT.json

Runtime run receipt:
docs/evidence/media-ai-general-work-final-self-audit-20261008/RUNTIME_E2E_RECEIPT.json

Regression:
docs/evidence/media-ai-general-work-final-self-audit-20261008/REGRESSION_RESULT.json

Remote readback:
docs/evidence/media-ai-general-work-final-self-audit-20261008/REMOTE_READBACK.txt

## 9. PASS / FAIL VOCABULARY

Only if all non-external visible/base product functions are complete and evidenced:
PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK

If any product gap is found and not closed:
REWORK_GENERAL_WORK_GAPS_FOUND

If only deferred external Marketing/AVORA items remain:
they must be marked DEFERRED_EXTERNAL and do NOT prevent General Work PASS.

## 10. NEXT STEP AFTER PASS — PC WORK ONLY

Do not build the old complex employee installer.

After General Work PASS, commander will activate PC Work with this target:

ONE-CLICK RUNTIME PACKAGE

Required behavior:
- one launcher/icon
- double-click once
- runtime starts automatically
- browser opens automatically
- MINDLE MEDIA AI is immediately usable
- no Git / clone / Python install / pip / terminal / token entry / model download by employee
- package contains or locates all required runtime dependencies in a controlled way
- safe close and relaunch
- single-instance behavior
- user data preserved

PC Work must not begin before this General Work directive reaches PASS.

## FINAL COMMAND

AUDIT EVERYTHING GENERAL WORK BUILT.
FIND WHAT WAS MISSED.
FIX VERIFIED GAPS.
DO NOT RESTART PASSED WORK WITHOUT CAUSE.
DO NOT WAIT FOR MARKETING OR AVORA.
DO NOT BUILD THE EMPLOYEE PACKAGE YET.
PUBLISH EVIDENCE.
ONLY THEN HAND OFF TO PC WORK.
