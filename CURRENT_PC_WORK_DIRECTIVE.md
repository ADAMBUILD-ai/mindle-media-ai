# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
DATE: 2026-10-01
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## THIS FILE IS THE ONLY STARTING POINT FOR THE PC WORKER

Before doing ANY work:

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. pull/reconcile to the current remote branch HEAD
4. verify this file exists from the updated working tree
5. read the Rule Registry below
6. confirm which rules are ACTIVE / REFERENCE_ONLY / HISTORY_ONLY
7. read the ACTIVE directive
8. read the machine-readable Evidence Path Contract
9. execute only the ACTIVE cycle
10. publish Evidence to the exact required paths
11. commit, push, and remote-verify before stopping

## RULE REGISTRY — MUST READ BEFORE ANY OLD DOCUMENT

Human-readable:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md

Machine-readable:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json

DEFAULT RULE:
Any old PC Work directive/review/evidence NOT explicitly classified ACTIVE or REFERENCE_ONLY by the Rule Registry is HISTORY_ONLY and MUST NOT be executed.

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_ENFORCEMENT_NONCOMPLIANCE_CORRECTION_DIRECTIVE_v13.1_20261001.md

Technical execution scope inherited from:

docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_DIRECTIVE_v13.0_20261001.md

Machine-readable Evidence path contract:

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v1.0_20261001.json

## EXACT REQUIRED OUTPUT PATHS

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_EVIDENCE_v13_0_20261001.json

Detailed Evidence:
evidence/pc_remote/pc-work-current-pc-four-lane-v13-20261001/

## HARD STOP RULE

If the worker is about to:
- execute an old directive not marked ACTIVE
- create a file name not listed in the ACTIVE directive or Evidence Path Contract
- continue from remembered/cached instructions before syncing remote HEAD

STOP THAT ACTION.

Invalid examples:
- MINDLE_MEDIA_AI_EVIDENCE_CYCLE_01_20261001.md
- MINDLE_MEDIA_AI_PC_RUNTIME_RESTORE_v16_20261001.json
- any other invented Evidence filename
- local-only Evidence
- chat-only Evidence
- old v1-v11 PC Work directives as current execution instructions

These do not advance the cycle.

## STALE CONTEXT GATE

If current remote HEAD was not synced and the Rule Registry was not read:

STATUS = STALE_CONTEXT_BLOCKED

The worker must not continue using remembered or cached rules.

## COMPLETION CONDITION

The cycle is complete only when:
- current remote HEAD was synced first
- Rule Registry was read
- only ACTIVE directives were executed
- exact review path exists on remote
- exact Evidence JSON path exists on remote
- exact detail directory exists on remote
- all required 12 detail files exist on remote
- commit is pushed
- remote readback is verified

The representative is not responsible for reconciling rule versions or Evidence paths.

FINAL RULE:
SYNC FIRST → READ CURRENT ENTRYPOINT → READ RULE REGISTRY → EXECUTE ONLY ACTIVE DIRECTIVE → SAVE ONLY TO EXACT PATHS → PUSH → REMOTE VERIFY.
