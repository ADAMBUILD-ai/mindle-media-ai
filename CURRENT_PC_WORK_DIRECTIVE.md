# MINDLE MEDIA AI — CURRENT PC WORK DIRECTIVE

STATUS: ACTIVE — RECOVERY ONLY
DATE: 2026-10-06
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## SINGLE ACTIVE DIRECTIVE
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_AND_ENVIRONMENT_DIAGNOSTIC_DIRECTIVE_v1.0_20261006.md

## SINGLE ACTIVE EVIDENCE CONTRACT
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261006.json

## PURPOSE
Recover one clean PC Work authority chain and diagnose the repeated Windows Work error:
`helper_unknown_error: apply deny-read ACLs`

## START RULE
Read only:
1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
3. CURRENT_PC_WORK_STATE.json
4. scripts/validate_pc_work_control_plane.py
5. the SINGLE ACTIVE DIRECTIVE
6. the SINGLE ACTIVE EVIDENCE CONTRACT

Do not execute any historical preflight, parent, technical-base, v13, v21, v21.0A, v21.0A-R1, or employee-package directive during this recovery cycle.

## REQUIRED OUTPUTS
Review: docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_REVIEW_v1.0_20261006.md
Machine Evidence: evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_v1_0_20261006.json
Detail: evidence/pc_remote/media-ai-control-plane-recovery-v1_0-20261006/

## HARD STOP
If a neutral execution probe fails before process creation with `apply deny-read ACLs`:
result = WORK_ENVIRONMENT_ACL_HELPER_BLOCKED
Stop. Do not touch the repository or Windows ACL manually.

## PASS
RECOVERY_PASS

Only after RECOVERY_PASS may the commander explicitly reactivate employee-package work.
