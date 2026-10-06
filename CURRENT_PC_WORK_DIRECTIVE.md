# MINDLE MEDIA AI — CURRENT PC WORK DIRECTIVE

STATUS: ACTIVE — WINDOWS SANDBOX ACL RECOVERY ONLY
DATE: 2026-10-06
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-WINDOWS-SANDBOX-ACL-RECOVERY-V1.1
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## SINGLE ACTIVE DIRECTIVE
docs/commander/MINDLE_MEDIA_AI_PC_WORK_WINDOWS_SANDBOX_ACL_STATE_RECOVERY_DIRECTIVE_v1.1_20261006.md

## SINGLE ACTIVE EVIDENCE CONTRACT
docs/commander/MINDLE_MEDIA_AI_PC_WORK_WINDOWS_SANDBOX_ACL_STATE_RECOVERY_EVIDENCE_CONTRACT_v1.1_20261006.json

## CONFIRMED FAILURE
The repeated failure occurs before normal command execution:
`helper_unknown_error: apply deny-read ACLs`

Blind session restarts are no longer the recovery plan.

## CURRENT RECOVERY TARGET
Classify persisted Windows sandbox ACL state first.
Only apply backup-and-regenerate recovery to the exact malformed 22-byte all-NUL state signature.
Then verify with an environment-neutral exec probe.

## RULE
- do not modify product files
- do not build employee package
- do not reset repository ACLs
- do not create repo copies/worktrees
- do not broadly delete .codex
- employee package directive is SUSPENDED / REFERENCE_ONLY

## REQUIRED RESULT
RECOVERY_PASS
or one exact diagnostic result from the active directive.

Only after RECOVERY_PASS may employee-package work be explicitly reactivated.
