# MINDLE MEDIA AI — EVIDENCE PATH ENFORCEMENT / NONCOMPLIANCE CORRECTION DIRECTIVE v13.1

Date: 2026-10-01
Status: MANDATORY IMMEDIATE CORRECTION
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Supersedes only the Evidence-publication handling portion of v13.0. All technical execution scope in v13.0 remains active.

## 0. Commander finding

The worker reported an Evidence file named:

MINDLE_MEDIA_AI_EVIDENCE_CYCLE_01_20261001.md

This filename/path was NOT authorized by v13.0.

The approved v13.0 Evidence destinations were explicitly fixed. Therefore any work saved only to an arbitrary local filename, chat attachment, or non-specified repository path is NOT accepted as cycle completion.

Current status:
- EVIDENCE_PATH_COMPLIANCE: FAIL
- REMOTE_EVIDENCE_PUBLICATION: NOT VERIFIED
- CYCLE_COMPLETE: NO

## 1. Non-negotiable rule

The worker MUST NOT invent:
- Evidence filenames
- Evidence folders
- Review filenames
- alternate save locations
- local-only handoff files

If the directive specifies an exact path, that exact path is part of the acceptance criteria.

Any mismatch between required path and actual path = FAIL.

## 2. Exact required repository paths

### A. Human review — EXACT PATH

docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md

### B. Machine Evidence JSON — EXACT PATH

evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_EVIDENCE_v13_0_20261001.json

### C. Detailed Evidence directory — EXACT PATH

evidence/pc_remote/pc-work-current-pc-four-lane-v13-20261001/

Required files inside that exact directory:

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

No substitute filenames are allowed.

## 3. Immediate correction action

The worker must now:

1. Locate the locally generated arbitrary Evidence file(s), including MINDLE_MEDIA_AI_EVIDENCE_CYCLE_01_20261001.md if present.
2. Extract all valid factual execution evidence from them.
3. Do NOT treat the arbitrary file itself as the final Evidence artifact.
4. Populate the exact required Review/JSON/detailed Evidence files listed in Section 2.
5. If required fields are missing, continue actual execution and collect them.
6. Commit all required files to:
   feature/ad-shortform-bridge-p0-20260926
7. Push.
8. Verify the exact remote paths are readable from GitHub.
9. Record the final remote commit SHA in REMOTE_PUSH_VERIFY.txt.
10. Only then report completion.

## 4. Mandatory path compliance gate

Before the worker is allowed to stop, verify all of the following:

- REVIEW_EXACT_PATH_EXISTS_REMOTE = YES
- EVIDENCE_JSON_EXACT_PATH_EXISTS_REMOTE = YES
- DETAIL_DIRECTORY_EXACT_PATH_EXISTS_REMOTE = YES
- ALL_12_DETAIL_FILES_EXIST_REMOTE = YES
- REMOTE_PUSH_VERIFIED = YES

If any value is NO:
- CYCLE_COMPLETE = NO
- worker must continue
- worker must not ask the representative whether to proceed
- worker must not report PASS/COMPLETE

## 5. Worker response format

After successful remote verification, report only:

RESULT: TESTED_PASS / PARTIAL_PASS / FAIL
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Evidence commit: <sha>
Review exact path: docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md
Evidence JSON exact path: evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_EVIDENCE_v13_0_20261001.json
Detail directory exact path: evidence/pc_remote/pc-work-current-pc-four-lane-v13-20261001/
ALL_12_DETAIL_FILES_EXIST_REMOTE: YES
REMOTE_PUSH_VERIFIED: YES

No other path is accepted as completion evidence.

## 6. Commander-worker circulation rule

The representative is not the file router.

The fixed cycle is:

COMMANDER WRITES EXACT DIRECTIVE PATH
→ WORKER READS DIRECTIVE
→ WORKER EXECUTES
→ WORKER SAVES EVIDENCE TO EXACT SPECIFIED PATHS
→ WORKER COMMITS/PUSHES
→ WORKER VERIFIES REMOTE
→ COMMANDER READS EXACT PATHS
→ COMMANDER ISSUES NEXT DIRECTIVE

If the worker saves Evidence somewhere else, the cycle has not advanced.

## 7. Final governing sentence

EXACT EVIDENCE PATH COMPLIANCE IS A HARD GATE. ARBITRARY FILENAMES OR LOCAL-ONLY EVIDENCE ARE NOT ACCEPTED AND DO NOT COUNT AS COMPLETION.
