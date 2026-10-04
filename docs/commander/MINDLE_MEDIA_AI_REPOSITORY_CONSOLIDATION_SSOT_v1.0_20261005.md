# MINDLE MEDIA AI — REPOSITORY CONSOLIDATION SSOT v1.0

Date: 2026-10-05
Status: GOVERNING REPOSITORY MAP
Repository: ADAMBUILD-ai/mindle-media-ai

## 1. Canonical product line

The only ACTIVE product-development branch is:

feature/ad-shortform-bridge-p0-20260926

Current active product cycle:
MEDIA-AI-20261003-V21.0

Current entrypoint:
CURRENT_PC_WORK_DIRECTIVE.md

Current state:
CURRENT_PC_WORK_STATE.json

Current control-plane lock:
CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json

No worker may infer "current" from branch date, PR number, filename version, or default branch.

## 2. Main branch status

main is NOT the current product SSOT.

Comparison at consolidation time:
- active branch is 452 commits ahead of main
- active branch is 1 commit behind main
- branches are diverged
- merge base: 067fa55484a8cd9e381200b1a799855def2eef6b

Therefore:
- do not merge main into active blindly
- do not reset active to main
- do not treat default branch as latest product
- any future main integration requires an explicit reconciliation cycle

## 3. Branch classification

### ACTIVE
- feature/ad-shortform-bridge-p0-20260926

### REFERENCE_ONLY / BASELINE
- main
- integration

These branches may be read for history but are not execution targets.

### ARCHIVE_CANDIDATE / NO NEW WORK
- automation/model-scout-route-media-50
- every branch matching work/* currently present in the repository

Examples include:
- work/track-a-full-project-handoff-20260913
- work/pc-runtime-e2e-evidence-20260915
- work/job-idempotency-provenance-remote-reconstruction-20260918
- work/job-queue-evidence-remote-reconstruction-20260918
- work/photo-video-job-pipeline-remote-reconstruction-20260918
- work/runtime-orchestration-ready-remote-reconstruction-20260918
- work/model-scout-adapter-gate-remote-reconstruction-20260918
- work/media-direct-acquisition-20260919
- work/pc-local-v14-ui-review-20260924
- work/pc-runtime-v15-closeout-20260924
- work/pc-runtime-v17-auth-input-gate-20260924
- work/pc-v19-execution-review-20260924
- work/pc-v20-1-true-manual-gate-20260924
- work/pc-v22-verified-asset-restore-20260924
- work/v23-1-materialization-review-20260924
- work/v24-1-pc-e2e-review-20260924
- work/v25-1-artifact-recovery-review-20260924
- work/v26-1-real-pc-e2e-review-20260924
- work/v27-1-quality-recovery-review-20260924
- work/v28-1-remote-runtime-package-20260924

ARCHIVE_CANDIDATE means:
- preserve history
- do not delete without owner approval
- do not commit new product work
- do not use as PC Work checkout
- do not use as merge target for current work

## 4. Pull request classification

### PR #23
Title:
P0: Add bidirectional MINDLE ADA ad shortform bridge

Head:
feature/ad-shortform-bridge-p0-20260926

Base:
work/v28-1-remote-runtime-package-20260924

The active branch is 290 commits ahead of this PR base.

Status:
HOLD / DO NOT MERGE

Reason:
The PR base is a historical work branch, not the current integration target.
PR #23 may remain as historical context until a clean main-integration strategy is explicitly approved.

### PR #22 through historical open PRs
Treat as:
REFERENCE_ONLY / ARCHIVE_CANDIDATE

Do not merge or continue them as current work.

## 5. File authority

Highest current authority:
1. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
2. CURRENT_WORKER_COORDINATION_LOCK.json
3. scripts/validate_pc_work_control_plane.py
4. CURRENT_PC_WORK_DIRECTIVE.md
5. CURRENT_PC_WORK_STATE.json
6. Rule Registry MD/JSON
7. MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_v2.0_20261005.md
8. active v21.0 directive + evidence contract
9. approved UI / model / Shortform SSOT
10. older directives/reviews as reference/history only

## 6. Historical directive policy

docs/commander contains a large historical chain.

Rule:
- ACTIVE means explicitly named by CURRENT_PC_WORK_DIRECTIVE / STATE
- REFERENCE_ONLY means useful evidence/history
- HISTORY_ONLY means do not execute
- an old file with a higher-looking version number does not become current automatically

## 7. Evidence policy

Current real-use audit remains v21.0.

Prior PASS evidence remains historical evidence, but representative real-use failures reopen the affected area.

No worker may:
- overwrite older evidence
- rename evidence to appear current
- reuse old evidence as current runtime proof without explicit cross-reference

## 8. Cleanup policy

No destructive cleanup is authorized by this document.

For now:
- preserve all branches
- preserve all PRs
- preserve all historical evidence
- stop new work on archive candidates
- consolidate navigation and write ownership only

Branch deletion / PR closure / default-branch change requires separate owner approval.

## Final rule

ONE ACTIVE PRODUCT BRANCH. ONE ACTIVE CONTROL PLANE. OLD BRANCHES AND PRS ARE HISTORY, NOT EXECUTION ROUTES.
