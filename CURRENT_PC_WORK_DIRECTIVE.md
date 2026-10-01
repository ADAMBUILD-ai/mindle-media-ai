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
5. read and complete the ACTIVE branch-rebind preflight below
6. read the Rule Registry below
7. confirm which rules are ACTIVE / REFERENCE_ONLY / HISTORY_ONLY
8. read the ACTIVE directive
9. read the machine-readable Evidence Path Contract
10. execute only the ACTIVE cycle
11. publish Evidence to the exact required paths
12. commit, push, and remote-verify before stopping

## ACTIVE BRANCH-REBIND PREFLIGHT — MUST COMPLETE FIRST

docs/commander/MINDLE_MEDIA_AI_PC_WORK_BRANCH_REBIND_AND_STALE_WORKTREE_RECOVERY_DIRECTIVE_v1.0_20261001.md

The PC worker must not continue from any already-open local branch without completing this preflight.

## RULE REGISTRY — MUST READ BEFORE ANY OLD DOCUMENT

Human-readable:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md

Machine-readable:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json

DEFAULT RULE:
Any old PC Work directive/review/evidence NOT explicitly classified ACTIVE or REFERENCE_ONLY by the Rule Registry is HISTORY_ONLY and MUST NOT be executed.

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_PC_WORK_LIVE_UI_VISUAL_EVIDENCE_MATERIALIZATION_AND_SSOT_COMPLIANCE_DIAGNOSIS_DIRECTIVE_v16.0_20261001.md

Previous accepted cycle:

docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md

Machine-readable Evidence path contract remains governing for exact-path behavior:

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v16.0_20261001.json

## EXACT REQUIRED OUTPUT PATHS

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_LIVE_UI_VISUAL_SSOT_DIAGNOSIS_REVIEW_v16.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_LIVE_UI_VISUAL_SSOT_DIAGNOSIS_EVIDENCE_v16_0_20261001.json

Detailed Evidence:
evidence/pc_remote/pc-work-live-ui-visual-v16-20261001/

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
- old v1-v13 PC Work directives as current execution instructions unless explicitly referenced by v14

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
- all required 11 detail files exist on remote
- commit is pushed
- remote readback is verified

The representative is not responsible for reconciling rule versions or Evidence paths.

FINAL RULE:
SYNC FIRST → READ CURRENT ENTRYPOINT → READ RULE REGISTRY → EXECUTE ONLY ACTIVE DIRECTIVE → SAVE ONLY TO EXACT PATHS → PUSH → REMOTE VERIFY.
