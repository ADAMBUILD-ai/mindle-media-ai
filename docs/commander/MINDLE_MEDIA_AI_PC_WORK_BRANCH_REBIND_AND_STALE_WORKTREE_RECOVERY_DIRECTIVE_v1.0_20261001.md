# MINDLE MEDIA AI — PC WORK BRANCH REBIND / STALE WORKTREE RECOVERY DIRECTIVE v1.0

Date: 2026-10-01
Status: ACTIVE PREFLIGHT — MUST COMPLETE BEFORE v13 EXECUTION
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical PC Work branch: feature/ad-shortform-bridge-p0-20260926

## 0. Root cause confirmed

The PC worker has been operating from a stale/local branch:

work/ui-final-pc-work-20260924

That branch is NOT present in the current GitHub remote branch set.

The worker also reported local commit:

f10875b

That commit cannot be resolved from the current GitHub remote repository.

Therefore the worker's local checkout is not a trustworthy source of current commander directives.

Additional repository condition:
- default branch main is stale relative to current development
- feature/ad-shortform-bridge-p0-20260926 is the canonical current development/commander branch
- main and feature branch are diverged
- current work must NOT use main as the source of truth

## 1. Safety first — preserve stale local state before rebinding

Before switching branches, the PC worker MUST preserve any local-only state.

Run and record:
- git status --short
- git rev-parse --show-toplevel
- git remote -v
- git branch --show-current
- git rev-parse HEAD

Create a local backup pointer to the current stale HEAD BEFORE any reset/switch that could overwrite it:

git branch backup/media-ai-stale-pc-work-20261001 HEAD

If the worktree is dirty, stash tracked + untracked files:

git stash push -u -m "media-ai-stale-pc-work-before-rebind-20261001"

Do NOT delete the stale branch.
Do NOT merge the stale branch into canonical.
Do NOT cherry-pick stale commits unless a later commander directive explicitly requests a specific commit after inspection.

## 2. Rebind to canonical remote branch

Execute:

git fetch --prune origin

Verify this remote branch exists:

origin/feature/ad-shortform-bridge-p0-20260926

Then bind the local worktree to the canonical branch:

git switch -C feature/ad-shortform-bridge-p0-20260926 --track origin/feature/ad-shortform-bridge-p0-20260926

Then verify:

git branch --show-current
git rev-parse HEAD
git rev-parse origin/feature/ad-shortform-bridge-p0-20260926

Required:
- current branch = feature/ad-shortform-bridge-p0-20260926
- local HEAD = origin/feature/ad-shortform-bridge-p0-20260926

If these are not equal, status = BRANCH_REBIND_FAIL and do not execute product work yet.

## 3. Mandatory current-entrypoint readback

After successful rebind, read in this order:

1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_STATE.json
3. docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
4. docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
5. docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_ENFORCEMENT_NONCOMPLIANCE_CORRECTION_DIRECTIVE_v13.1_20261001.md
6. docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_DIRECTIVE_v13.0_20261001.md
7. docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v1.0_20261001.json

Do not search for "latest directive" by filename/date after rebind.
The entrypoint and registry define what is current.

## 4. Old local branch treatment

The following is now explicitly STALE_LOCAL_HISTORY:

work/ui-final-pc-work-20260924

Do not execute directives based on that branch's local snapshot.

Historical file:
docs/commander/MINDLE_MEDIA_AI_PC_RUNTIME_RESTORE_NEXT_DIRECTIVE_v16.0_20260924.md

is HISTORY_ONLY under the current Rule Registry and MUST NOT drive current work.

## 5. Continue the existing v13 Evidence cycle

After branch rebind succeeds, do NOT create a new Evidence naming scheme.

Continue the existing exact v13 outputs:

Review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_REVIEW_v13.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_EVIDENCE_v13_0_20261001.json

Detail directory:
evidence/pc_remote/pc-work-current-pc-four-lane-v13-20261001/

Record branch-rebind facts inside:
- CURRENT_PC_INVENTORY.txt
- MANIFEST.json
- REMOTE_PUSH_VERIFY.txt

Do not invent a separate rebind Evidence filename.

## 6. Hard gates

Before product execution:
- STALE_LOCAL_BRANCH_BACKED_UP = YES
- REMOTE_FETCH_COMPLETED = YES
- CANONICAL_BRANCH_EXISTS = YES
- CURRENT_BRANCH_CANONICAL = YES
- LOCAL_HEAD_EQUALS_REMOTE_HEAD = YES
- CURRENT_PC_WORK_DIRECTIVE_READ = YES
- RULE_REGISTRY_READ = YES

Before cycle completion:
- all v13 exact Evidence paths exist remotely
- all required 12 detail files exist remotely
- remote push readback verified

## 7. Commander rule going forward

No MEDIA AI PC worker may begin work merely from "whatever branch is already open".

Every cycle begins with:
REMOTE FETCH → CANONICAL BRANCH ASSERTION → CURRENT ENTRYPOINT READ → RULE REGISTRY READ → ACTIVE DIRECTIVE EXECUTION.

If the worktree is on any other branch:
status = STALE_CONTEXT_BLOCKED
until safely rebound.

## Final rule

THE ROOT PROBLEM IS BRANCH BINDING, NOT JUST DOCUMENT SELECTION.

PRESERVE STALE LOCAL STATE → FETCH REMOTE → REBIND TO CANONICAL FEATURE BRANCH → READ CURRENT ENTRYPOINT → EXECUTE ACTIVE v13 CYCLE.
