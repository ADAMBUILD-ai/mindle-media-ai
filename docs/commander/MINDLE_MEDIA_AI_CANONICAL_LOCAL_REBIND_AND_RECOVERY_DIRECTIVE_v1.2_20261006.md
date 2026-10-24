# MINDLE MEDIA AI — CANONICAL LOCAL REBIND & RECOVERY DIRECTIVE v1.2

Date: 2026-10-06
Status: ACTIVE — LOCAL REBIND ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-CANONICAL-LOCAL-REBIND-V1.2

## Confirmed facts

Host sandbox ACL recovery passed:
- neutral probe: C:\MINDLE_WORK_TEST\acl_probe.txt
- readback: MINDLE_PC_WORK_ACL_PROBE_PASS

Current local checkout reported:
- repo: C:\Users\PC\Documents\Codex\2026-09-30\referenced-chatgpt-conversation-this-is-an-2\work\mindle-media-ai
- remote: https://github.com/ADAMBUILD-ai/mindle-media-ai.git
- branch: feature/ad-shortform-bridge-p0-20260926
- local HEAD: 093d15f33b99e04794532367046219367e811441
- remote canonical HEAD observed by commander: 8610cbe486398c4490b2cc444d0c760d400831ff
- local HEAD 093d15f... is not present in GitHub remote history
- dirty tracked:
  - docs/commander/MINDLE_MEDIA_AI_DESKTOP_SHORTCUT_REACTIVATION_REVIEW_v20.2.7_20261002.md
  - evidence/pc_remote/MINDLE_MEDIA_AI_DESKTOP_SHORTCUT_REACTIVATION_EVIDENCE_v20_2_7_20261002.json
- untracked: work-data/

## Objective

Safely preserve ALL local-only history and dirty evidence, then rebind the local canonical branch to origin without losing recoverable information.

## Forbidden

- no repo deletion
- no new clone/worktree
- no git clean
- no deletion of work-data/
- no force push
- no merge/rebase
- no package build
- no product/UI modification

## Phase A — immutable backup outside repository

Create:
C:\MINDLE_RECOVERY_BACKUP\media-ai-20261006\

Capture:
1. full local HEAD bundle:
   mindle-media-ai-local-093d.bundle
2. git status:
   STATUS_BEFORE.txt
3. local log:
   LOG_BEFORE.txt
4. binary diff:
   DIRTY_TRACKED_CHANGES.patch
5. exact copies of the two modified v20.2.7 Review/Evidence files
6. work-data inventory only (path/size/hash where practical), without deleting or moving work-data

Required backup verification:
- bundle verify PASS
- backup files exist and are readable

## Phase B — fetch and classify

Run:
git fetch origin feature/ad-shortform-bridge-p0-20260926

Record:
- HEAD
- origin/feature/ad-shortform-bridge-p0-20260926
- git rev-list --left-right --count HEAD...origin/feature/ad-shortform-bridge-p0-20260926
- git merge-base HEAD origin/feature/ad-shortform-bridge-p0-20260926

If fetch fails: STOP.

## Phase C — canonical rebind

Only after Phase A backup PASS.

Reset tracked repository state to:
origin/feature/ad-shortform-bridge-p0-20260926

Use:
git reset --hard origin/feature/ad-shortform-bridge-p0-20260926

DO NOT run git clean.
DO NOT remove work-data/.

Then verify:
- remote URL exact
- branch exact
- HEAD == origin/feature/ad-shortform-bridge-p0-20260926
- only allowed untracked work-data remains
- CURRENT authority files readable

## Phase D — validator

Run:
python scripts/validate_pc_work_control_plane.py

Required:
CONTROL_PLANE_PASS

## Phase E — local evidence reconciliation

Do NOT automatically restore the backed-up v20.2.7 files.

Compare backups against canonical versions.
Preserve local richer fields as a separate reconciliation evidence artifact.
Commander decides whether to merge those fields later.

## Required outputs

Review:
docs/commander/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_REVIEW_v1.2_20261006.md

Machine evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_EVIDENCE_v1_2_20261006.json

Detail:
evidence/pc_remote/media-ai-canonical-local-rebind-v1_2-20261006/

Required detail:
- STATUS_BEFORE.txt
- LOG_BEFORE.txt
- BUNDLE_VERIFY.txt
- DIRTY_TRACKED_CHANGES.patch.sha256
- FETCH_CLASSIFICATION.txt
- STATUS_AFTER.txt
- CANONICAL_REPO_READONLY_PROBE.txt
- CONTROL_PLANE_VALIDATOR.txt
- V20_2_7_LOCAL_RECONCILIATION.txt

## PASS

LOCAL_CANONICAL_REBIND_PASS
then RECOVERY_PASS

Employee package remains suspended until commander explicitly reactivates it.
