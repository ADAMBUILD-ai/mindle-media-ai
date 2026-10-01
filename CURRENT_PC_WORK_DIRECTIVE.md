# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20.1
DATE: 2026-10-01
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## START ORDER

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run python scripts/validate_pc_work_control_plane.py
6. require CONTROL_PLANE_PASS
7. read CURRENT_PC_WORK_STATE.json
8. read Rule Registry MD + JSON
9. execute only v20.1
10. publish exact v20.1 Evidence
11. commit, push, remote-readback

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_LOCAL_MARKETING_RUNTIME_BOOTSTRAP_AUTH_MP4_E2E_DIRECTIVE_v20.1_20261001.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.1_20261001.json

## PREVIOUS CYCLE

v20 = MARKETING_AUTH_ENV_REQUIRED

Accepted from v20:
- fail-closed Marketing HTTP client implemented
- request/contract adapter static PASS
- Python 52 PASS
- UI 2 PASS
- base product frozen PASS

v20 is now REFERENCE_ONLY.

## EXACT v20.1 OUTPUTS

Review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_REVIEW_v20.1_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_EVIDENCE_v20_1_20261001.json

Detail:
evidence/pc_remote/media-ai-marketing-live-shortform-v20_1-20261001/

Required files:
18

## HARD RULE

Do not ask representative for token.
Use ephemeral in-memory E2E token only.
Do not execute v20 or any older cycle as current work.

SYNC → VALIDATE → RUN MARKETING → AUTHENTICATED CONTRACT/ASSETS → FFMPEG → REAL MP4 → EXACT EVIDENCE → PUSH → READBACK.
