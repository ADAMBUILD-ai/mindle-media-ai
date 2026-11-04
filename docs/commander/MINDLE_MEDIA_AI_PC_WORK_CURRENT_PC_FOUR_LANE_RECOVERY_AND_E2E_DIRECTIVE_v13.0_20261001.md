# MINDLE MEDIA AI — PC WORK CURRENT-PC FOUR-LANE RECOVERY + REAL E2E + EVIDENCE PUBLICATION DIRECTIVE v13.0

Date: 2026-10-01
Status: EXECUTE NOW — DO NOT STOP AT PLAN/REPORT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Commander baseline HEAD before this directive: 08851dc988cca446ef65b568eaea69d3cd0fa943

## 0. Why this directive exists

The replacement PC worker was called, but as of commander remote verification there is no new worker Evidence commit after MASTER commit 08851dc988cca446ef65b568eaea69d3cd0fa943 on the active branch.

Therefore the current worker state is:

- RESULT: UNVERIFIED
- REASON: current-cycle Evidence is not present on the remote repository
- DO NOT claim PASS/COMPLETE based on local-only files or chat text
- DO NOT ask the representative where to save Evidence; all locations are fixed below

This directive starts the mandatory commander → worker → Evidence → commander review cycle.

## 1. Mandatory read order

Read these files before execution, in this order:

1. docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
2. docs/commander/MINDLE_MEDIA_AI_PC_WORK_COMMANDER_ROUTE_CORRECTION_NO_GITHUB_LOGIN_LOOP_DIRECTIVE_v12.1_20261001.md
3. docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FIRST_PRODUCT_RECOVERY_DIRECTIVE_v12.0_20261001.md
4. docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md
5. docs/commander/MINDLE_MEDIA_AI_COMMANDER_PC_WORKER_REPOSITORY_CIRCULATION_PROTOCOL_v1.0_20261001.md
6. docs/01_UI_SSOT_FINAL.md
7. ui/ssot_manifest.json
8. evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json
9. evidence/model_scout/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_V13.json
10. docs/commander/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_REVIEW_v32.0_20260925.md
11. evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json

Old v7-v11 artifact/auth cycles are diagnostic history only. Do not replay them chronologically.

## 2. Fixed worker behavior rules

The worker MUST:

- execute actual work, not only describe a plan
- never stop after analysis when the next executable action is available
- not expand or shrink the directive scope arbitrarily
- preserve approved UI SSOT
- preserve adopted model identities
- compare current PC state against proven v32 Evidence before declaring anything missing
- treat the four product lanes independently
- execute every runnable lane even if another lane is blocked
- fix reproducible local defects and rerun before reporting
- record exact command/result/output/hash/error evidence
- save Evidence to the exact repository paths below
- COMMIT and PUSH the Evidence
- verify the remote branch contains the Evidence after push
- never claim PASS/COMPLETE without remote Evidence

The worker MUST NOT:

- restart the GitHub login loop
- ask the representative to sign in as the first action
- make historical Artifact 10797756522 a universal prerequisite
- rebuild an independent shortform app
- redesign MEDIA AI UI
- silently substitute legacy/unadopted models
- report “model missing” until current PC/cache/runtime inventory and v32 comparison are complete
- stop because one lane is blocked

## 3. Fixed product/model baselines

UI SSOT:
- ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- SHA-256: f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
- UI_SSOT_CHANGED must remain NO

Adopted models:
- SAM 2.1 Hiera Base Plus
- Whisper-small
- Intel single-image-super-resolution-1032

Use exact revision/hash/license values from evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json.

Historical proven v32 local capabilities that must be used as comparison baseline:
- PHOTO segmentation: TESTED_PASS
- PHOTO 4x SISR: TESTED_PASS
- VIDEO tracking: TESTED_PASS
- Korean STT: TESTED_PASS
- Project Save: PASS
- Export: PASS

A current failure is a regression/recovery problem unless evidence proves otherwise.

## 4. Execution scope

### G1 — Current Windows PC inventory

Inventory current runtime and resources FIRST.

At minimum record:
- repository working copy path
- checked-out branch and HEAD
- Python executable/version
- relevant virtual environment
- torch version and CPU availability
- OpenCV availability
- OpenVINO availability
- ffmpeg/ffprobe availability
- current model/cache locations
- exact presence/size/hash for adopted SAM asset
- exact presence/size/hash for adopted Whisper-small asset
- exact presence/size/hash for Intel SISR XML/BIN
- product server/runtime entrypoint presence
- known fixture/input files currently present
- any stale auth dialogs/processes relevant to previous loop

Do not alter unrelated PC configuration.

### G2 — v32 reconciliation

Build a current-vs-v32 matrix for:
1. PHOTO segmentation
2. PHOTO 4x
3. VIDEO tracking
4. Korean STT
5. Project Save
6. Export

For each row record:
- v32 status
- current required runtime
- current asset found YES/NO
- current runnable YES/NO
- exact blocker if NO
- recovery action
- rerun result

### G3 — Four independent real execution lanes

Run all runnable lanes through the real current product/backend path.

#### Lane A — PHOTO Segmentation
Required:
- adopted SAM 2.1 Hiera Base Plus identity verified
- real input used
- real segmentation executed
- output created
- output dimensions/size/hash recorded
- product/API success recorded

#### Lane B — PHOTO 4x
Required:
- adopted Intel SISR 1032 identity verified
- real image input used
- actual 4x execution
- output dimensions/size/hash recorded
- product/API success recorded

#### Lane C — VIDEO Tracking
Required:
- adopted SAM 2.1 path used
- real MP4 input used
- actual tracking executed
- output MP4 validated
- OpenCV fallback may be used where the already-proven implementation uses it
- output duration/dimensions/size/hash recorded

#### Lane D — Korean STT
Required:
- exact adopted Whisper-small identity verified
- Korean WAV/audio real execution
- transcript saved
- sample rate/duration recorded
- transcript quality metric or deterministic comparison recorded if available
- output/transcript hash recorded

A blocked lane MUST NOT block the others.

### G4 — Project Save and Export regression check

Because v32 proved Save and Export, current execution must also verify:
- create/update a test project through the current product path
- save succeeds
- export ZIP succeeds
- project ID recorded
- saved artifact hash recorded
- export filename/size/hash recorded

If browser-native file chooser automation remains a boundary, distinguish:
- underlying product/backend E2E result
- browser-only automation boundary

Do not convert an automation limitation into a false product failure.

### G5 — Defect fix and rerun rule

If any failure is caused by current code/config/runtime and can be fixed within this repository/current PC without violating SSOT:
1. reproduce
2. identify root cause
3. fix
4. run targeted test
5. rerun affected E2E lane
6. record before/after evidence

Do not merely list a fix suggestion.

### G6 — UI SSOT regression check

Verify that current product UI still preserves:
- dark navy
- upper VIDEO / lower PHOTO
- natural-language command areas
- Preview
- VIDEO Timeline
- Save
- Export
- additive 광고 숏폼 placement only
- no independent shortform app
- no unapproved layout/color/panel redesign

Set UI_SSOT_CHANGED=NO unless the user explicitly approved a different UI.

Shortform live E2E is not allowed to block the base product four-lane closeout when approved Marketing Contract/assets are unavailable.

## 5. Exact Evidence publication locations

### Human-readable review file — REQUIRED

Save exactly:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md

### Machine-readable Evidence file — REQUIRED

Save exactly:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_EVIDENCE_v13_0_20261001.json

### Detailed Evidence directory — REQUIRED

Save all detailed cycle files under exactly:
evidence/pc_remote/pc-work-current-pc-four-lane-v13-20261001/

Required files in that directory:

1. MANIFEST.json
2. CURRENT_PC_INVENTORY.txt
3. CURRENT_VS_V32_MATRIX.json
4. PHOTO_SEGMENTATION_RUN.json
5. PHOTO_4X_RUN.json
6. VIDEO_TRACKING_RUN.json
7. KOREAN_STT_RUN.json
8. PROJECT_SAVE_EXPORT_RUN.json
9. UI_SSOT_REGRESSION_CHECK.json
10. TEST_RESULTS.txt
11. OUTPUT_HASHES.sha256
12. REMOTE_PUSH_VERIFY.txt

If a lane is blocked, its required JSON file must still exist and contain:
- status: BLOCKED or FAIL
- exact command/action attempted
- exact missing item or error
- why other lanes were still executable
- next selective recovery target

## 6. Mandatory JSON top-level fields

The machine Evidence JSON must include at minimum:

- directive_version
- repository
- branch
- starting_head
- ending_head
- timestamp
- master_handover_commit
- github_auth_loop_stopped
- ui_ssot_changed
- current_pc_inventory_complete
- v32_reconciliation_complete
- photo_segmentation_status
- photo_4x_status
- video_tracking_status
- korean_stt_status
- project_save_status
- export_status
- shortform_live_e2e_status
- blockers
- code_changes
- tests
- output_hashes
- evidence_files
- remote_push_verified
- overall_result

Allowed overall_result:
- TESTED_PASS
- PARTIAL_PASS
- FAIL

Do not use TESTED_PASS unless every required base-product lane plus Save/Export has evidence-backed success.

## 7. Required review conclusion

The human-readable review must clearly state:

- what was actually executed
- what changed
- what passed
- what failed or is blocked
- exact model identity used per applicable lane
- exact output paths and hashes
- whether UI SSOT changed
- whether the prior GitHub auth/artifact loop was avoided
- whether remote push was verified
- exact next blocker, if any

No vague wording such as “appears okay”, “likely PASS”, “should work”.

## 8. Commit / push / remote verification

After the actual work and Evidence files are complete:

1. git status
2. review changed files
3. commit all authorized code/test/Evidence changes
4. push to:
   feature/ad-shortform-bridge-p0-20260926
5. verify the remote branch HEAD
6. verify all 14 required Evidence/review files are readable remotely
7. write the pushed commit SHA and remote verification result into REMOTE_PUSH_VERIFY.txt and the review/Evidence JSON
8. if adding the final commit SHA requires one metadata-only follow-up commit, do it once and push once; do not create a micro-commit loop

## 9. Completion gate

The worker may stop only when ONE of these is true:

### A. TESTED_PASS
All four lanes + Save + Export executed successfully with remote Evidence.

### B. PARTIAL_PASS
All currently runnable lanes were executed and passed, every blocked lane has a precise proven blocker and selective recovery target, and all Evidence is remotely committed/pushed.

### C. FAIL
A reproducible repository/runtime defect remains after attempted fix/rerun, with exact failure Evidence remotely committed/pushed.

Local-only Evidence, chat-only reports, screenshots without repository publication, or “waiting for commander” before push are NOT valid completion states.

## 10. Final worker handoff message format

Return only after remote publication is verified:

- RESULT: TESTED_PASS / PARTIAL_PASS / FAIL
- Repository:
- Branch:
- Evidence commit:
- Review path:
- Evidence JSON path:
- Detailed Evidence directory:
- Four-lane statuses:
- Save/Export statuses:
- UI_SSOT_CHANGED:
- Blocker:
- REMOTE_PUSH_VERIFIED: YES

Then stop and wait for commander review.

---

Commander intent:
The representative should observe progress, not mediate between worker and commander. The worker executes and publishes Evidence; the commander reviews that Evidence and immediately publishes the next directive. Do not return responsibility to the representative.
