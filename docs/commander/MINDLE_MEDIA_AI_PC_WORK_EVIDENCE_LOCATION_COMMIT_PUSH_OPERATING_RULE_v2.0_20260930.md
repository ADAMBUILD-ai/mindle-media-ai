# MINDLE MEDIA AI — PC WORK EVIDENCE LOCATION / COMMIT / PUSH OPERATING RULE v2.0
Date: 2026-09-30
Status: PERMANENT — ALL PC WORK DIRECTIVES MUST INHERIT
Repository: ADAMBUILD-ai/mindle-media-ai
Active branch: feature/ad-shortform-bridge-p0-20260926

## 1. Purpose
Remove ambiguity. PC Work must never ask where to save evidence or whether to commit/push when the active directive already authorizes the work.

## 2. Exact repository and branch
All current MEDIA AI PC Work evidence is written to:
- Repository: ADAMBUILD-ai/mindle-media-ai
- Branch: feature/ad-shortform-bridge-p0-20260926
Do not save only to Desktop/Documents/temp/local notes.

Before work:
1. cd to the local clone of ADAMBUILD-ai/mindle-media-ai
2. git fetch origin
3. verify current branch is feature/ad-shortform-bridge-p0-20260926
4. verify git status and current HEAD
5. do not switch to main

## 3. Exact evidence locations
For EVERY execution cycle create BOTH files:

A. Human-readable review:
docs/commander/<DIRECTIVE_BASENAME>_REVIEW_<YYYYMMDD>.md

B. Machine-readable evidence:
evidence/pc_remote/<DIRECTIVE_BASENAME>_EVIDENCE_<YYYYMMDD>.json

If the active directive already specifies exact evidence filenames, those exact filenames override the template above.

Screenshots/logs/output manifests:
evidence/pc_remote/<cycle_name>/
Create the cycle folder when needed. Do not overwrite prior cycle folders/files.

## 4. What must be inside
MD and JSON must record:
- repository / branch / starting HEAD
- directive exact path and directive commit
- Windows machine execution surface
- files changed
- commands/processes/service host+port
- request URL/status/server log for integration errors
- each lane PASS/REWORK/FAIL/VERIFY_REQUIRED
- actual input/output path + SHA-256 where applicable
- UI screenshot evidence paths
- Preview / project save / Export result
- regression result
- exact blocker/root cause
- remaining work
- UI_SSOT_CHANGED
- final commit SHA after commit/push

## 5. Mandatory commit and push
Creating local MD/JSON is NOT evidence completion.
After self-verification:
1. git status
2. git add ONLY authorized changed source + current-cycle evidence + next directive/handoff
3. git diff --cached --check
4. git diff --cached --stat
5. git commit with a clear cycle message
6. git push origin feature/ad-shortform-bridge-p0-20260926
7. git rev-parse HEAD
8. verify remote branch HEAD equals local HEAD
9. verify BOTH evidence files are visible from the remote branch

Only after steps 1-9 may Work say EVIDENCE_COMMITTED_AND_PUSHED: PASS.

## 6. No approval pause
Do NOT ask whether to commit, where to save, or whether to push when the active directive already authorizes branch commit/push.
Execute commit+push automatically. This rule does NOT authorize main merge or Production deploy.

## 7. If push fails
Do not stop after local save.
Capture exact push error in evidence and attempt permitted recovery:
- fetch/rebase only when non-destructive and safe
- resolve only Work's own branch changes
- never force-push
If still blocked, keep local commit intact and report REMOTE_PUSH_BLOCKED with exact error.

## 8. Automatic continuation
After remote evidence verification:
- freeze successful lanes as PASS
- carry only failed/incomplete lanes
- create next directive under docs/commander/
- include this rule by reference: MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md
- commit and push the next directive in the SAME cycle.

## 9. Completion definition
A PC Work cycle is complete only when:
ACTUAL WORK -> SELF VERIFY -> MD+JSON -> COMMIT -> PUSH -> REMOTE FILE VERIFY -> NEXT DIRECTIVE COMMITTED/PUSHED.

Anything less is an incomplete cycle.

## 10. Protection
No main merge, Production deployment, force push, UI SSOT redesign, credential exposure, destructive cleanup, GPU/paid compute without separate authorization, or overwrite of prior Evidence.
