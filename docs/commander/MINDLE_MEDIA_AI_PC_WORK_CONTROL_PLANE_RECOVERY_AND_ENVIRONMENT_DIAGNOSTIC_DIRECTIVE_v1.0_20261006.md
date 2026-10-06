# MINDLE MEDIA AI — PC WORK CONTROL PLANE RECOVERY & ENVIRONMENT DIAGNOSTIC DIRECTIVE v1.0

Date: 2026-10-06
Status: ACTIVE — RECOVERY ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0

## 0. Purpose

Recover one unambiguous PC Work authority chain and diagnose the repeated Windows Work execution failure:

`helper_unknown_error: apply deny-read ACLs`

This cycle is NOT product development.
This cycle is NOT employee package construction.
This cycle is NOT UI repair.

No product file may be modified until this recovery cycle passes.

## 1. Single authority chain

Read ONLY in this order:

1. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
2. CURRENT_PC_WORK_DIRECTIVE.md
3. CURRENT_PC_WORK_STATE.json
4. docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
5. scripts/validate_pc_work_control_plane.py
6. this directive
7. active recovery evidence contract

Do NOT execute any historical/preflight/parent/technical-base directive unless this recovery directive explicitly names it.

## 2. Historical directive rule

All prior product directives, including v13, v21.0, v21.0A, v21.0A-R1 and employee-package v1.0, are REFERENCE_ONLY during this recovery cycle.

Specifically DO NOT execute:
- branch-rebind v1.0 from 2026-10-01
- v13 evidence cycle
- v21.0 full real-use audit
- v21.0A launcher/UI repair
- employee distribution package build

The employee distribution package directive remains preserved and becomes executable only after RECOVERY_PASS and a new explicit activation.

## 3. Phase A — environment-neutral exec probe

Before touching Git or the repository, test the Work execution environment itself.

Use neutral folder:
`C:\MINDLE_WORK_TEST`

Attempt:
1. determine whether the folder exists
2. create it if allowed
3. create `acl_probe.txt` with exact content:
   `MINDLE_PC_WORK_ACL_PROBE_PASS`
4. read it back
5. record elapsed time and exact result

If ANY command fails before process creation with:
`apply deny-read ACLs`

then:
- status = `WORK_ENVIRONMENT_ACL_HELPER_BLOCKED`
- STOP
- do not touch repository
- do not change Windows ACL manually
- do not create another repo/worktree
- report exact error text

## 4. Phase B — read-only canonical repository probe

Only if Phase A passes.

Read-only checks:
- repository root
- current branch
- remote URL
- current HEAD
- origin canonical branch HEAD
- existence/readability of CURRENT authority files

Do not switch/reset/rebase/stash/checkout during recovery.

Required:
- repo = ADAMBUILD-ai/mindle-media-ai
- branch = feature/ad-shortform-bridge-p0-20260926

If current local checkout differs:
report `LOCAL_BINDING_MISMATCH` and STOP.
Do not run the old branch-rebind directive.

## 5. Phase C — authority consistency validator

Run:
`python scripts/validate_pc_work_control_plane.py`

Required:
`CONTROL_PLANE_PASS`

Then verify semantically:
- one epoch only
- one active directive only
- one active evidence contract only
- no ACTIVE v13/v21/package directive elsewhere in CURRENT/README/Master/Registry
- no lane collision
- no stale preflight required

## 6. Forbidden actions

During this cycle:
- no ui/** changes
- no src/** changes
- no tests/** product changes
- no launcher changes
- no package build
- no model copying
- no branch switching
- no reset/rebase/stash
- no Windows ACL mutation
- no admin permission changes
- no new worktree/repository copy

## 7. Evidence

Review:
`docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_REVIEW_v1.0_20261006.md`

Machine Evidence:
`evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_v1_0_20261006.json`

Detail:
`evidence/pc_remote/media-ai-control-plane-recovery-v1_0-20261006/`

Minimum detail:
- ENV_NEUTRAL_EXEC_PROBE.txt
- CANONICAL_REPO_READONLY_PROBE.txt
- CONTROL_PLANE_VALIDATOR.txt
- AUTHORITY_CONSISTENCY_AUDIT.json
- EXACT_FAILURE.txt (only if blocked)

## 8. Result vocabulary

PASS only:
`RECOVERY_PASS`

Blocked:
`WORK_ENVIRONMENT_ACL_HELPER_BLOCKED`

Other:
`LOCAL_BINDING_MISMATCH`
`CONTROL_PLANE_MISMATCH_BLOCKED`
`FAIL`

## 9. Next cycle

Only after RECOVERY_PASS may the commander explicitly reactivate:
`MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_FULL_WINDOWS_PACKAGE_DIRECTIVE_v1.0_20261006.md`

No automatic continuation.

## Final rule

ONE ACTIVE EPOCH. ONE ACTIVE DIRECTIVE. ONE ACTIVE CONTRACT. NO HISTORICAL PREFLIGHT EXECUTION. DIAGNOSE THE EXEC ENVIRONMENT BEFORE PRODUCT WORK.
