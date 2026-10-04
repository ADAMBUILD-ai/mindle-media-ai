# MINDLE MEDIA AI

## CURRENT STATUS — READ THIS FIRST

Canonical product branch:

`feature/ad-shortform-bridge-p0-20260926`

Current active cycle:

`MEDIA-AI-20261003-V21.0`

Current directive:

`docs/commander/MINDLE_MEDIA_AI_FULL_PRODUCT_REAL_USE_REAUDIT_AND_IMPROVEMENT_DIRECTIVE_v21.0_20261003.md`

Current Master:

`docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_v2.0_20261005.md`

Repository map:

`docs/commander/MINDLE_MEDIA_AI_REPOSITORY_CONSOLIDATION_SSOT_v1.0_20261005.md`

Two-worker protocol:

`docs/commander/MINDLE_MEDIA_AI_TWO_WORKER_COORDINATION_PROTOCOL_v1.0_20261005.md`

Worker lane lock:

`CURRENT_WORKER_COORDINATION_LOCK.json`

User guide:

`docs/manual/MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md`

## Important

`main` is NOT the current product branch.

At the 2026-10-05 consolidation point, the active product branch is 452 commits ahead of `main`, 1 commit behind it, and diverged.

Do not:
- treat main as latest product
- merge main blindly
- execute historical work/* branches
- merge historical PRs as current product
- run two workers as simultaneous product writers

PR #23 is HOLD / DO NOT MERGE because its base is historical `work/v28-1-remote-runtime-package-20260924`.

## Worker start order

1. `CURRENT_WORKER_COORDINATION_LOCK.json`
2. `CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json`
3. `CURRENT_PC_WORK_DIRECTIVE.md`
4. `CURRENT_PC_WORK_STATE.json`
5. Control-plane validator
6. Current Master v2
7. Active directive

## Product

MINDLE MEDIA AI provides VIDEO and PHOTO editing with:
- natural-language editing
- reference images
- Preview
- VIDEO Timeline
- Save / Export
- PHOTO segmentation / upscale
- VIDEO tracking / Korean STT
- Marketing AI linked Shortform workflow

Current closeout standard is real Windows use, not metadata-only PASS.

See:
`docs/manual/MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md`
