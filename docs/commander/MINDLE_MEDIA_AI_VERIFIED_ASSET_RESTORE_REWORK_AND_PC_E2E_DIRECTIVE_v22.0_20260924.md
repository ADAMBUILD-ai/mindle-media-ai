# MINDLE MEDIA AI v22 — VERIFIED ASSET RESTORE / REWORK / PC E2E

Date: 2026-09-24
Status: EXECUTE
Base: PR #15

## Commander verdict
The latest Work report is REWORK, not PASS.

Do not treat a missing local copy as a missing product asset. The adopted release models were previously acquired, verified, preserved remotely, and exercised in successful product E2E. Work must reconcile the PC environment with that verified baseline before declaring a blocker.

## Required corrections

### 1. Reconcile against the verified baseline first
Read the v13 final closeout evidence, adopted-model manifest, license evidence, PR #10 product E2E evidence, and Private HF frozen-revision reference already stored in this repository.
Build a reconciliation table:
- adopted model
- verified remote revision
- verified hash
- expected cache location
- current PC-local status
- restore action
Do not write UNAVAILABLE until the restore action has actually failed with evidence.

### 2. Restore, do not rescout
Restore the adopted SAM 2.1, whisper-small, and Intel SISR artifacts through the already-approved authenticated project path.
Do not search for replacement models and do not fall back to legacy models.
Verify restored files against the frozen manifest before runtime use.
Credentials must remain secret and must not appear in reports.

### 3. Missing dependencies are REWORK tasks
For required free/local runtime components, attempt installation or portable exposure before reporting a blocker.
At minimum inspect and resolve the actual requirements for OpenVINO CPU and ffmpeg.
Browser automation/PyArrow are installed only if the chosen runtime path truly requires them.
Record attempt, result, version and path.
No GPU or paid compute.

### 4. Reuse previously approved real E2E inputs when permitted
Before asking the user for new media, inspect the successful prior product-E2E evidence/artifacts and approved project assets for the real video and Korean speech inputs previously used.
If provenance permits reuse, restore them to the PC and record hashes.
If they cannot be retrieved or reuse is not permitted, then and only then open a local file picker for one approved video and one spoken-Korean sample.
Silent audio is invalid.

### 5. Execute available lanes without waiting
PHOTO and UPSCALE inputs already exist.
As soon as the verified cache/runtime is restored:
- PHOTO -> SAM CPU segmentation -> actual output -> Preview -> save -> export
- UPSCALE -> Intel SISR CPU -> actual 4x output -> dimension/reopen/hash -> Preview -> save -> export
Do not wait for VIDEO/AUDIO to finish these two lanes.

### 6. Execute VIDEO and STT
VIDEO -> approved real input -> SAM tracking -> decodable/continuous output -> Preview -> save -> export.
Korean STT -> approved spoken Korean -> whisper-small CPU -> actual transcript -> Preview -> save/export.

### 7. Quality gate
Do not PASS merely because a process exited successfully.
Verify:
- PHOTO boundary usability
- VIDEO tracking continuity
- UPSCALE true 4x dimensions and visible artifact/detail quality
- STT actual Korean transcript and obvious errors
- Preview/export consistency
Any failed lane is REWORK with cause and rerun.

### 8. Regression
Re-run Python, UI structure/interaction, product server, evidence/package validation.
Preserve the established regression baseline.

### 9. Evidence
Create a new review and JSON evidence containing:
- baseline-vs-PC reconciliation table
- every restore/install attempt
- adopted model identities/hashes
- actual input/output hashes
- quality verdict by lane
- Preview/save/export status
- regression
- changed files
- commit/PR/Actions status

### 10. PASS discipline
PASS is allowed only for items supported by actual evidence.
Previously verified remote PASS may remain preserved, but it cannot be relabeled as PC-local PASS without local execution.
Incorrect Work assumptions must be marked REWORK and corrected, not accepted.

### 11. Stop condition
Do not stop on a generic “missing/unavailable” statement.
Stop only if an actual restore/install/retrieval attempt fails and the remaining step genuinely requires a human action. Report the exact failed attempt and the single required action.

### 12. Automatic next directive
After this verification:
1. inspect evidence;
2. issue PASS/REWORK per item;
3. correct any Work error;
4. create the next directive;
5. commit it under docs/commander;
6. report directive path and commit SHA.
Do not wait for another user request.

## Protection
UI_SSOT_CHANGED:NO.
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or overwrite of immutable prior evidence.
