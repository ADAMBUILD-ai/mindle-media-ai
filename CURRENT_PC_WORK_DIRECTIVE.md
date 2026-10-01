# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20
DATE: 2026-10-01
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## THIS FILE IS THE ONLY HUMAN-READABLE STARTING POINT

Before ANY work:

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile local HEAD to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run: python scripts/validate_pc_work_control_plane.py
6. read CURRENT_PC_WORK_STATE.json
7. read Rule Registry MD + JSON
8. validator MUST return CONTROL_PLANE_PASS
9. only then execute v20
10. publish Evidence to exact v20 paths
11. commit, push, remote-readback before stopping

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_COMPLETION_DIRECTIVE_v20.0_20261001.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.0_20261001.json

## VERIFIED MARKETING LIVE PROVIDER

Repository:
ADAMBUILD-ai/mindle-marketing-department

PR:
#4

Branch:
feature/shortform-bridge-p0-20260926

Commit:
3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a

Workflow:
36852551111 — SUCCESS

Local Base URL:
http://127.0.0.1:4318

Secret ENV:
MARKETING_SHORTFORM_BRIDGE_TOKEN

Never print or persist the token.

## PREVIOUS CYCLE — FROZEN

v19:
BASE_PRODUCT_TESTED_PASS_SHORTFORM_EXTERNAL_DEPENDENCY

The external dependency is now supplied by Marketing AI, so v19 is REFERENCE_ONLY.
Do not execute v19 again.

Frozen base PASS remains:
- v14 runtime
- v18.1 F27E UI
- v18.2 Shortform additive action identity/order
- v19 integrated base-product closeout

## EXACT REQUIRED v20 OUTPUTS

Review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_REVIEW_v20.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_EVIDENCE_v20_0_20261001.json

Detail directory:
evidence/pc_remote/media-ai-marketing-live-shortform-v20-20261001/

Required files:
16

## HARD STOP

If Lock / Current / State / Registry MD / Registry JSON / validator disagree:
CONTROL_PLANE_MISMATCH_BLOCKED

Do not select an older directive.
Do not run v19 or v18.2 as current work.

FINAL:
SYNC → VALIDATE → EXECUTE v20 → REAL MARKETING HTTP → REAL MP4 → EXACT EVIDENCE → PUSH → REMOTE READBACK.
