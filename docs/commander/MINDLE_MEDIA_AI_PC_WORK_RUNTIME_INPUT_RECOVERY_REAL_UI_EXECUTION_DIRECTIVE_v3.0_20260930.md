# MINDLE MEDIA AI — PC WORK RUNTIME/INPUT RECOVERY & REAL UI LANE EXECUTION DIRECTIVE v3.0
Date: 2026-09-30
Status: REWORK — EXECUTE IMMEDIATELY
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## Mandatory inherited operating rule
Read and obey first:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

Do not ask where to save, whether to commit, or whether to push.

## Commander verification of latest evidence
Verified remote evidence commit: 2bd209e435106b0b40d71d2452a5d2c7818b5d21.

FREEZE PASS:
- real local product server reachable at http://127.0.0.1:8765/
- approved UI shell/hierarchy
- project-save fail-closed gate behavior
- approved 광고 숏폼 entry
- shortform missing-contract route now explicit 503 VERIFY_REQUIRED
- Python syntax validation
- UI_SSOT_CHANGED:NO

Do NOT redo these unless regression proves breakage.

REWORK/VERIFY_REQUIRED:
- native chooser
- PHOTO segmentation
- PHOTO 4x
- VIDEO tracking
- Korean STT
- actual Preview
- completed project save
- Export
- Shortform live E2E only when approved Contract v1/assets exist

## 1. Do not accept “no approved media fixture” without searching the repository/evidence
Before declaring media unavailable, inventory the existing repository and prior verified evidence for already-approved/recovered real inputs used in earlier PC E2E cycles.
Check at minimum:
- evidence/e2e/PHOTO_INPUT_MANIFEST.json
- evidence/e2e/VIDEO_INPUT_MANIFEST.json
- evidence/model_scout/WHISPER_KO_INPUT_MANIFEST.json
- evidence/pc_remote prior v22-v32 evidence/reviews for recovered local paths/hashes
- existing project test/evidence media folders

Use an input only when its identity/hash and prior approval/evidence are traceable. Do not fabricate new approval.
If a referenced local file is absent, use the existing verified artifact/materialization route from prior evidence rather than declaring the entire lane blocked.

## 2. Runtime/model recovery
Do not start a new Model Scout cycle.
Inspect prior verified local/runtime evidence and the already-established runtime package/materialization records.
Recover/reuse the pinned model/runtime cache that previously produced PASS results.
For HF_TOKEN:
- never print/store token in evidence
- first check whether the already-authorized environment/cache can load pinned local files offline
- if a token is genuinely required only for a missing private payload, mark the exact missing model/file/revision and authentication boundary; do not generalize all lanes as blocked
- PHOTO/4x/VIDEO/STT must be assessed independently because prior evidence shows different runtimes/assets.

## 3. Native chooser
Use the actual approved UI at http://127.0.0.1:8765/.
Click existing import control.
If automation can surface but cannot populate the Windows native chooser, leave the chooser open and request only the minimal human file selection action; after selection continue automatically.
Do not replace the chooser or add a bypass UI.

## 4. Execute lanes independently
For each available verified input/runtime, execute immediately through the real UI:
A. PHOTO segmentation
B. PHOTO 4x upscale
C. VIDEO tracking
D. Korean STT

Do not block A/B/C/D together because one prerequisite is missing.
For each lane capture:
input path/hash -> UI action -> request/job -> service log -> visible result/Preview -> output path/hash -> quality verdict.

## 5. Preview/save/export
For every completed real job:
- verify actual Preview
- save project and verify persisted state/ID
- export through existing UI
- reopen exported output
- record bytes/hash and decode/playback where applicable

## 6. Shortform boundary
Keep the new 503 VERIFY_REQUIRED behavior.
Do not spend this cycle searching for or inventing an upstream Contract.
If a Marketing AI-approved Contract v1 + approved asset handoff is actually present, execute it.
Otherwise report SHORTFORM separately as VERIFY_REQUIRED; it must not prevent completion of independent base MEDIA AI lanes.

## 7. Evidence locations — EXACT
This cycle MUST create and push:
Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_RUNTIME_INPUT_RECOVERY_REAL_UI_REVIEW_v3.0_20260930.md

Machine evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_RUNTIME_INPUT_RECOVERY_REAL_UI_EVIDENCE_v3_0_20260930.json

Cycle folder:
evidence/pc_remote/pc-work-runtime-input-recovery-v3-20260930/

Inside cycle folder save manifest plus screenshots/log references/output manifests as available.

## 8. Commit/push — MANDATORY
At cycle end:
git status
git add authorized source/current evidence/next directive only
git diff --cached --check
git commit
git push origin feature/ad-shortform-bridge-p0-20260926
git rev-parse HEAD
verify origin branch HEAD equals local HEAD
verify the MD + JSON + cycle manifest are visible on remote.

Local save alone is NOT completion.
Do not ask permission to commit/push.

## 9. Next directive — SAME CYCLE
After remote verification, create the next directive under docs/commander based on actual v3 evidence.
Freeze PASS lanes and carry forward only remaining lanes.
Commit and push that next directive before ending the cycle.

## 10. Time discipline
If one route has no measurable progress for 10 minutes, preserve evidence and change route.
Do not wait repeatedly at the same blocker.

## 11. Completion verdict
MEDIA_AI_PC_UI_FINAL:PASS requires all independently available base UI lanes, real Preview, completed save and Export evidence.
SHORTFORM_LIVE_E2E remains separate and may stay VERIFY_REQUIRED solely for missing approved upstream Contract/assets.

## Protection
No UI redesign, no SSOT modification, no fabricated media/approval/Contract, no main merge, Production deploy, force push, credential exposure, destructive cleanup, or new model scouting.
