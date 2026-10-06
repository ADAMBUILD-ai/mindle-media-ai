# MINDLE MEDIA AI — PC WORK CONTROL PLANE RECOVERY & ENVIRONMENT DIAGNOSTIC DIRECTIVE v1.0

Date: 2026-10-06
Status: ACTIVE — RECOVERY ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-CONTROL-PLANE-RECOVERY-V1.0

## 0. Purpose

Recover one unambiguous PC Work authority chain and diagnose the repeated Windows Work execution failure:
`helper_unknown_error: apply deny-read ACLs`

This cycle is NOT product development, package construction, UI repair, branch repair, or historical directive replay.

## 1. Single authority chain

Read ONLY in this order:

1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
3. CURRENT_PC_WORK_STATE.json
4. CURRENT_WORKER_COORDINATION_LOCK.json
5. scripts/validate_pc_work_control_plane.py
6. this directive
7. docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_CONTRACT_v1.0_20261006.json

Do not use the old Rule Registry, README, Master, preflight, parent directive, or technical-base directive as execution authority during this recovery cycle.

## 2. Historical directive rule

All prior product directives are REFERENCE_ONLY during recovery, including:
- branch-rebind v1.0
- v13 evidence cycle
- v21.0 full real-use audit
- v21.0A / v21.0A-R1
- employee distribution package v1.0

Do not execute any of them automatically.

## 3. Phase A — environment-neutral exec probe

Before touching Git or the repository, use only:
`C:\MINDLE_WORK_TEST`

Attempt:
1. check whether the folder exists
2. create it if allowed
3. create `acl_probe.txt` with exact content `MINDLE_PC_WORK_ACL_PROBE_PASS`
4. read it back
5. record exact result

If process creation fails with the known ACL helper error:
- result = `WORK_ENVIRONMENT_ACL_HELPER_BLOCKED`
- STOP
- do not touch repository
- do not change Windows ACL manually
- do not create another repo/worktree

## 4. Phase B — read-only canonical repository probe

Only if Phase A passes.

Read-only checks:
- repository root
- current branch
- remote URL
- current HEAD
- origin canonical branch HEAD
- readability of the CURRENT authority files

Do not switch/reset/rebase/stash/checkout.

Required:
- repo = ADAMBUILD-ai/mindle-media-ai
- branch = feature/ad-shortform-bridge-p0-20260926

If local binding differs:
`LOCAL_BINDING_MISMATCH` and STOP.

## 5. Phase C — current authority validator

Run:
`python scripts/validate_pc_work_control_plane.py`

Required:
`CONTROL_PLANE_PASS`

The recovery validator intentionally checks only CURRENT/LOCK/STATE/WORKER-LOCK.
Historical registry content is not execution authority during recovery.

## 6. Forbidden actions

- no ui/src/tests product changes
- no package build
- no model copying
- no branch switching/reset/rebase/stash
- no manual Windows ACL mutation
- no admin permission changes
- no new worktree/repository copy

## 7. Evidence

Review:
`docs/commander/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_REVIEW_v1.0_20261006.md`

Machine Evidence:
`evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CONTROL_PLANE_RECOVERY_EVIDENCE_v1_0_20261006.json`

Detail:
`evidence/pc_remote/media-ai-control-plane-recovery-v1_0-20261006/`

## 8. Results

PASS only:
`RECOVERY_PASS`

Blocked:
`WORK_ENVIRONMENT_ACL_HELPER_BLOCKED`

Other:
`LOCAL_BINDING_MISMATCH`
`CONTROL_PLANE_MISMATCH_BLOCKED`
`FAIL`

## 9. Next cycle

Only after RECOVERY_PASS may the commander explicitly reactivate employee package construction.

## Final rule

ONE ACTIVE EPOCH. ONE ACTIVE DIRECTIVE. ONE ACTIVE CONTRACT. NO HISTORICAL EXECUTION CHAIN.
