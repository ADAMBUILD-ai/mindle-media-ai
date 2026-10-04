# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261003-V21.0
DATE: 2026-10-03
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## ACTIVE DIRECTIVE
docs/commander/MINDLE_MEDIA_AI_FULL_PRODUCT_REAL_USE_REAUDIT_AND_IMPROVEMENT_DIRECTIVE_v21.0_20261003.md

## ACTIVE EVIDENCE CONTRACT
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v21.0_20261003.json

## PURPOSE
Full real-use re-audit and improvement.

## RULES
- Real Windows execution overrides metadata-only PASS.
- One workspace / one runtime / one desktop launch path.
- Re-test desktop shortcut 2/2.
- Re-test VIDEO, PHOTO, Shortform, Save/Reopen, Export.
- Detect stale/duplicate servers and UI sources.
- Keep MEDIA AI user guide:
  docs/manual/MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md

## EXACT OUTPUTS
Review: docs/commander/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_REVIEW_v21.0_20261003.md
Evidence: evidence/pc_remote/MINDLE_MEDIA_AI_FULL_REAL_USE_REAUDIT_EVIDENCE_v21_0_20261003.json
Detail: evidence/pc_remote/media-ai-full-reaudit-v21_0-20261003/

## FINAL RULE
NO PASS WITHOUT REAL RUNTIME EVIDENCE.


## TWO-WORKER COORDINATION — MANDATORY

Before any write:
1. read CURRENT_WORKER_COORDINATION_LOCK.json
2. confirm your assigned lane
3. if another lane owns the target file, STOP with LANE_OWNERSHIP_CONFLICT
4. Worker A owns product/runtime files for active v21.0
5. Worker B owns Master/repository governance only
6. no simultaneous product-file writes by two workers

Current Master:
docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_v2.0_20261005.md

Repository map:
docs/commander/MINDLE_MEDIA_AI_REPOSITORY_CONSOLIDATION_SSOT_v1.0_20261005.md
