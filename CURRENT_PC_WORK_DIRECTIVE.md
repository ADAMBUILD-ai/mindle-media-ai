# MINDLE MEDIA AI — CURRENT PC WORK DIRECTIVE

STATUS: ACTIVE — CANONICAL LOCAL REBIND ONLY
DATE: 2026-10-06
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-CANONICAL-LOCAL-REBIND-V1.2
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## SINGLE ACTIVE DIRECTIVE
docs/commander/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_AND_RECOVERY_DIRECTIVE_v1.2_20261006.md

## SINGLE ACTIVE EVIDENCE CONTRACT
docs/commander/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_EVIDENCE_CONTRACT_v1.2_20261006.json

## CONFIRMED STATE
- Windows sandbox ACL neutral exec probe PASS
- local remote URL correct
- local branch name correct
- local HEAD 093d15f33b99e04794532367046219367e811441 is not present in GitHub remote history
- local worktree has two modified v20.2.7 evidence files and untracked work-data/
- remote canonical branch is newer

## RULE
Do not build employee package.
Do not delete local-only information.
First create an external recovery backup/bundle, then fetch/classify, then rebind tracked files to origin, leaving work-data intact.

## REQUIRED RESULT
LOCAL_CANONICAL_REBIND_PASS
then RECOVERY_PASS

Only after RECOVERY_PASS may employee-package work be explicitly reactivated.
