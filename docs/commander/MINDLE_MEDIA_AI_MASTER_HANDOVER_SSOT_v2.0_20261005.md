# MINDLE MEDIA AI — MASTER HANDOVER SSOT v2.0

Date: 2026-10-05
Status: CURRENT MASTER / READ FIRST
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926

## 0. Current truth

This file supersedes the 2026-10-01 Master as the CURRENT navigation map.
The older Master remains historical/reference evidence.

Current product branch:
feature/ad-shortform-bridge-p0-20260926

Current active cycle:
MEDIA-AI-20261003-V21.0

Current product directive:
docs/commander/MINDLE_MEDIA_AI_FULL_PRODUCT_REAL_USE_REAUDIT_AND_IMPROVEMENT_DIRECTIVE_v21.0_20261003.md

Current Evidence contract:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v21.0_20261003.json

Current worker coordination:
CURRENT_WORKER_COORDINATION_LOCK.json

Repository consolidation map:
docs/commander/MINDLE_MEDIA_AI_REPOSITORY_CONSOLIDATION_SSOT_v1.0_20261005.md

Two-worker protocol:
docs/commander/MINDLE_MEDIA_AI_TWO_WORKER_COORDINATION_PROTOCOL_v1.0_20261005.md

User guide:
docs/manual/MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md

## 1. Why v2 exists

The repository has accumulated:
- many historical work branches
- many still-open historical PRs
- long PC Work directive history
- two workers that may operate concurrently
- a stale default main branch
- representative real-use findings that overruled metadata-only PASS claims

The purpose of v2 is to make the current product path impossible to confuse with historical paths.

## 2. Branch authority

ACTIVE:
- feature/ad-shortform-bridge-p0-20260926

REFERENCE_ONLY:
- main
- integration

ARCHIVE_CANDIDATE / READ ONLY:
- automation/model-scout-route-media-50
- all work/* branches currently present

Do not delete historical branches without owner approval.

Do not perform new product work on archive candidates.

## 3. Main branch warning

At consolidation time:
- active branch is 452 commits ahead of main
- active branch is 1 commit behind main
- status: diverged
- merge base: 067fa55484a8cd9e381200b1a799855def2eef6b

Therefore main is NOT current product SSOT.
No blind merge/reset/rebase against main.

## 4. PR warning

PR #23:
- head = current active branch
- base = work/v28-1-remote-runtime-package-20260924
- active branch is 290 commits ahead of that base

Therefore PR #23 is HOLD / DO NOT MERGE.

Historical PRs #1-#22:
REFERENCE_ONLY / ARCHIVE_CANDIDATE unless explicitly reopened by commander.

## 5. Current product objective

v21.0 performs full real-use re-audit.

Representative real-use findings override metadata-only PASS.

Mandatory current checks:
- desktop shortcut launches 2/2
- no stale/duplicate product server
- workspace and desktop launch same product identity
- VIDEO actual functions
- PHOTO actual functions
- Shortform actual functions
- Save/Reopen persistence
- Export
- icon/favicon
- error recovery

No final PASS without real Windows runtime evidence.

## 6. UI authority

Final visual authority:
F27E base:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

PLUS:
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

VIDEO action order:
영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

Known accepted workspace geometry recovery point:
97900cc6c784e74b4224333fa2cc84d29c611f87

Known rejected clipping approach:
2ab174e03dc786c53f38ba956dea95f8e1ccd5a7

Do not reintroduce fixed-height/overflow tricks that visually cut controls.

## 7. Proven runtime baseline

Adopted models remain:
- SAM 2.1 Hiera Base Plus
- Whisper-small
- Intel single-image-super-resolution-1032

Legacy/unadopted substitutions remain prohibited.

Historical v32 proves base PHOTO/VIDEO/STT/Save/Export runtime.
v20.1 proves real Shortform MP4 E2E with documented voice-audio dependency.

These remain evidence, but any representative-observed regression in the current product must be re-tested.

## 8. Worker lanes

### Worker A — Product/Windows Real-Use
Owns:
- ui/**
- src/**
- scripts/**
- tests/**
- current v21.0 runtime Evidence

### Worker B — Master/Repository
Owns:
- Master
- repo consolidation map
- two-worker governance
- branch/PR classification
- documentation navigation

Worker B may not patch product files while Worker A owns them.

If Worker B finds a defect:
document it and route it to Worker A.

## 9. Collision prevention

Every worker must:
1. git fetch origin
2. read remote HEAD
3. read CURRENT_WORKER_COORDINATION_LOCK.json
4. confirm lane ownership
5. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
6. run control-plane validator
7. only then write

If owned by another lane:
LANE_OWNERSHIP_CONFLICT
and stop.

No force push.

## 10. Current read order

New worker read order:

1. README.md
2. CURRENT_WORKER_COORDINATION_LOCK.json
3. CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
4. CURRENT_PC_WORK_DIRECTIVE.md
5. CURRENT_PC_WORK_STATE.json
6. Rule Registry JSON/MD
7. this Master v2
8. Repository Consolidation SSOT
9. Two-Worker Coordination Protocol
10. active v21.0 directive + evidence contract
11. older files only when explicitly referenced

## 11. Historical files

Do not replay docs/commander chronologically.

The repository intentionally retains historical evidence.
Filename version alone does not grant authority.

Use CURRENT files and this Master v2 as navigation.

## 12. Cleanup policy

Current cleanup is NON-DESTRUCTIVE.

Done:
- one active branch identified
- old branches classified
- old PRs classified
- two-worker lane ownership established
- Master v2 created
- README current navigation refreshed

Not done without owner approval:
- branch deletion
- PR closure
- default-branch change
- main merge

## Final governing sentence

ONE ACTIVE PRODUCT BRANCH, ONE ACTIVE CONTROL PLANE, ONE PRODUCT WRITER AT A TIME. MASTER/REPO WORK MUST NEVER SILENTLY MODIFY PRODUCT FILES.
