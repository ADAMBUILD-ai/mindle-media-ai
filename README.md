# MINDLE MEDIA AI

## CURRENT STATUS

Canonical branch:
`feature/ad-shortform-bridge-p0-20260926`

Current PC Work cycle:
`MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0`

Status:
**RECOVERY ONLY — PRODUCT AND EMPLOYEE PACKAGE WORK PAUSED**

Single active directive:
`docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_AND_ENVIRONMENT_DIAGNOSTIC_DIRECTIVE_v1.0_20261006.md`

Single active Evidence contract:
`docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261006.json`

The current recovery cycle exists to diagnose the repeated Windows Work process-creation failure and to remove stale directive-chain ambiguity.

Historical v13, v21, v21.0A, v21.0A-R1, branch-rebind, and employee-package directives are not executable during recovery.

Worker start order:
1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
3. CURRENT_PC_WORK_STATE.json
4. CURRENT_WORKER_COORDINATION_LOCK.json
5. scripts/validate_pc_work_control_plane.py
6. active recovery directive
7. active recovery Evidence contract

Recovery PASS:
`RECOVERY_PASS`

Blocked status:
`WORK_ENVIRONMENT_ACL_HELPER_BLOCKED`

Only after RECOVERY_PASS may employee package work be explicitly reactivated.
