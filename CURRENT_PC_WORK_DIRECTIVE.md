# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V19
DATE: 2026-10-01
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## THIS FILE IS THE ONLY HUMAN-READABLE STARTING POINT

Before ANY work:

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile local HEAD to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. read CURRENT_PC_WORK_STATE.json
6. read Rule Registry
7. verify ALL THREE declare CONTROL_PLANE_EPOCH = MEDIA-AI-20261001-V19
8. verify all three point to the SAME active directive and Evidence contract
9. if any mismatch: STOP with CONTROL_PLANE_MISMATCH_BLOCKED
10. only then read and execute the active directive
11. publish Evidence to exact required paths
12. commit, push, and remote-readback before stopping

## AUTHORITATIVE CONTROL-PLANE LOCK

CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json

The lock is authoritative for active-cycle identity.
This file, CURRENT_PC_WORK_STATE.json, and Rule Registry MUST agree with it.

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_DIRECTIVE_v19.0_20261001.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v19.0_20261001.json

## PREVIOUS CYCLE — FROZEN PASS

v18.2 Shortform additive UI correction:
- TESTED_PASS
- code commit: 175e509da5cef1415d66fa527ce69711892819d7
- evidence finalization: 10563ab3c2e3ef3bbec6d23708975b94896edacd
- remote readback: 737cded9f09a568513a118abc0330e997a7865b3

Preserved:
- AI 자동 편집 remains distinct
- 광고 숏폼 is a separate control
- 광고 숏폼 alone owns data-action="shortform-mode"
- order: 영상 불러오기 → AI 자동 편집 → 광고 숏폼 → 프로젝트 저장 → 내보내기
- F27E UI SSOT preserved
- v18.1 PASS preserved

Do NOT execute v18.2 again.

## EXACT REQUIRED v19 OUTPUT PATHS

Human review:
docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_REVIEW_v19.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_EVIDENCE_v19_0_20261001.json

Detailed Evidence:
evidence/pc_remote/media-ai-final-integrated-closeout-v19-20261001/

Required detail files: 11

## HARD STOP RULE

STOP if:
- control-plane epoch differs anywhere
- active directive differs anywhere
- Evidence contract differs anywhere
- local branch is not canonical
- worker is using remembered/cached instructions
- worker is about to execute v18.2 or any older directive as current work

On mismatch:
STATUS = CONTROL_PLANE_MISMATCH_BLOCKED

The representative is not responsible for reconciling versions.

## FINAL RULE

SYNC → LOCK → STATE → REGISTRY → ACTIVE v19 → EXACT EVIDENCE → PUSH → REMOTE READBACK.
