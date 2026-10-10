# MINDLE MEDIA AI — UI SSOT PROVENANCE FINAL ADJUDICATION + RELEASE CLOSEOUT DIRECTIVE v15.0

Date: 2026-10-01
Status: ACTIVE — FINAL UI SSOT GATE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v14

v14 is accepted as:

PARTIAL_PASS_UI_SSOT_BLOCKED

The following are VERIFIED PASS and MUST NOT be reworked unless regression evidence appears:
- SAM 2.1 exact asset recovered and hash-verified
- Whisper-small exact asset recovered and hash-verified
- Intel SISR 1032 exact asset recovered and hash-verified
- v32 PHOTO input recovered
- v32 VIDEO input recovered
- v32 Korean AUDIO input recovered
- PHOTO segmentation TESTED_PASS
- PHOTO 4x TESTED_PASS
- VIDEO tracking TESTED_PASS
- Korean STT TESTED_PASS
- Project Save / Export / Reopen TESTED_PASS
- remote Evidence push/readback PASS

The only remaining blocker is the approved UI SSOT binary hash.

## 1. Confirmed UI lineage facts

Current manifest expects:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

Current repository PNG measures:
9aaf05be17a3b851717a8bcdbeaf9c589812cb02f4807e3e2c9d10e75709ad3d

Git history shows:
- the PNG path and APPROVED_PINNED manifest were introduced together at commit:
  39b313bd9bfc60194609910c25a639c325a9b2ca
- the PNG Git blob at that commit is the same Git blob as current:
  293cc4d1a218b62442189e3c6f88ec81bb6ff38c
- therefore the current PNG was not later replaced in Git history after the pin commit
- the mismatch between manifest SHA-256 and actual PNG existed from the first repository pin event
- the exact f27e... binary has not been recovered from targeted local lineage search

This means the remaining problem is provenance adjudication, not product runtime failure.

## 2. Mandatory protection

Do NOT:
- regenerate a UI image
- alter the current PNG to force a hash
- change layout/color/panel geometry
- overwrite the manifest hash without evidence or representative approval
- re-run completed model scouting
- re-run the already-PASS v14 product lanes unless needed only for final smoke confirmation
- merge stale branches wholesale

## 3. Phase A — repository provenance proof

Produce a concise immutable provenance report proving:

1. commit where ui/ssot_manifest.json first became APPROVED_PINNED
2. commit where ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png first appeared
3. Git blob SHA of that original committed PNG
4. current Git blob SHA
5. whether the blob changed after first pin
6. manifest expected SHA-256
7. current observed PNG SHA-256
8. conclusion:
   - MANIFEST_HASH_MISMATCH_AT_INITIAL_PIN
   OR
   - LATER_BINARY_REPLACEMENT
   OR
   - OTHER, with proof

Do not infer. Use Git history evidence.

## 4. Phase B — final exact-original recovery sweep

Perform one final targeted search for the exact expected SHA-256 f27e... in:

- preserved stale local branch/worktree
- all known MEDIA AI Codex worktrees
- prior v13/v14 worktrees
- v30/v32 output/package locations
- local Git object database reachable from the repository
- user-local exported UI/source directories already referenced in project history
- local Downloads/Desktop/Documents only where MEDIA AI-related names/path lineage justify the search
- existing conversation/library material that is already locally materialized and accessible to the worker, if any

Do NOT perform broad uncontrolled disk crawling.

For each candidate:
- path
- bytes
- SHA-256
- match yes/no
- provenance

If exact f27e... is found:
- restore it to the SSOT path
- verify exact SHA-256
- run UI structure/interaction/screenshot regression
- continue to TESTED_PASS closeout

If exact f27e... is NOT found:
- do not change the expected manifest hash
- status becomes USER_VISUAL_CONFIRMATION_REQUIRED
- continue to Phase C

## 5. Phase C — visual confirmation package when exact original is absent

If f27e... remains unavailable, prepare a user-facing confirmation package containing:

1. current SSOT PNG copy/reference
2. current live UI screenshot at the canonical app state
3. fixed UI contract checklist:
   - dark navy
   - upper VIDEO / lower PHOTO
   - left media + natural language
   - center Preview/work area
   - right editing panel
   - VIDEO Timeline
   - independent PHOTO/VIDEO command fields
   - reference upload control
   - Project Save
   - Export
   - additive 광고 숏폼 only
4. current PNG SHA-256 = 9aaf...
5. expected manifest SHA-256 = f27e...
6. Git provenance statement that the current PNG blob is the same blob present at the repository pin commit
7. explicit question for representative:
   "현재 저장소의 9aaf... PNG가 최종 승인 UI 원본과 시각적으로 동일한가?"

Do not update manifest until representative confirmation.

## 6. Phase D — post-confirmation rule

Only after explicit representative confirmation that the current 9aaf... PNG is the approved final UI:

- update ui/ssot_manifest.json asset_sha256 to the actual verified 9aaf... value
- update docs/01_UI_SSOT_FINAL.md to remove stale BLOCKED wording and record the same actual path/hash/date
- record that the old f27e... manifest value was an initial pin metadata mismatch
- run UI tests/regression
- produce final TESTED_PASS closeout Evidence

If representative says the current PNG is NOT the approved UI:
- keep UI gate BLOCKED
- do not redesign
- request/provide recovery of the exact approved source asset only
- base product runtime PASS remains preserved

## 7. Final product smoke protection

Before final closeout, run only a light non-destructive smoke confirmation:
- current branch correct
- UI tests PASS
- Python regression PASS
- model identities unchanged
- v14 Evidence still valid
- no UI geometry/layout change
- no model substitution
- no product feature regression

Do not redo long expensive model E2E unless regression evidence requires it.

## 8. Exact v15 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_UI_SSOT_PROVENANCE_FINAL_REVIEW_v15.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_UI_SSOT_PROVENANCE_FINAL_EVIDENCE_v15_0_20261001.json

Detailed Evidence directory:
evidence/pc_remote/pc-work-ui-ssot-provenance-v15-20261001/

Required detail files:
1. MANIFEST.json
2. GIT_UI_LINEAGE.json
3. EXACT_HASH_RECOVERY_SEARCH.txt
4. UI_SSOT_HASH_COMPARISON.json
5. CURRENT_UI_VISUAL_CONFIRMATION_PACKAGE.json
6. CURRENT_UI_SCREENSHOT_REFERENCE.txt
7. UI_CONTRACT_CHECKLIST.json
8. REGRESSION_TEST_RESULTS.txt
9. V14_PASS_PRESERVATION_CHECK.json
10. REPRESENTATIVE_CONFIRMATION_GATE.json
11. OUTPUT_HASHES.sha256
12. REMOTE_PUSH_VERIFY.txt

No alternate filenames.

## 9. Completion results

TESTED_PASS:
- exact approved UI SSOT resolved
- manifest/docs consistent with actual approved asset
- UI regression PASS
- v14 product PASS preserved
- remote Evidence published

USER_VISUAL_CONFIRMATION_REQUIRED:
- exact f27e... original not recoverable
- repository lineage proves initial manifest/binary mismatch
- current UI visual package prepared
- no unauthorized manifest change
- remote Evidence published

FAIL:
- provenance could not be established or regression discovered
- exact failure Evidence published

## 10. End-of-cycle response format

RESULT:
Repository:
Branch:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
First pin commit:
Original pin blob SHA:
Current blob SHA:
Expected manifest SHA-256:
Current PNG SHA-256:
Exact f27e asset recovered: YES/NO
Current UI screenshot prepared: YES/NO
V14 PASS preserved: YES/NO
Representative confirmation required: YES/NO
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE BASE PRODUCT IS FUNCTIONALLY RECOVERED. DO NOT REWORK PASSING RUNTIME. RESOLVE ONLY THE UI SSOT PROVENANCE, AND NEVER SILENTLY CHANGE THE APPROVED UI IDENTITY WITHOUT EVIDENCE OR REPRESENTATIVE CONFIRMATION.
