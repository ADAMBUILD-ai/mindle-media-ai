# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.3

Date: 2026-10-01
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20.1

## 0. Governing rule

Exactly ONE cycle is executable:

- docs/commander/MINDLE_MEDIA_AI_LOCAL_MARKETING_RUNTIME_BOOTSTRAP_AUTH_MP4_E2E_DIRECTIVE_v20.1_20261001.md

Evidence contract:

- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.1_20261001.json

Authoritative lock:
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json

Validator:
- scripts/validate_pc_work_control_plane.py

Any mismatch:
CONTROL_PLANE_MISMATCH_BLOCKED

## 1. Mandatory start order

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read lock
5. run validator
6. require CONTROL_PLANE_PASS
7. read Current/State/Registry
8. execute only v20.1
9. publish exact v20.1 Evidence
10. push and remote-readback

## 2. ACTIVE — the only executable set

### Control plane
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
- scripts/validate_pc_work_control_plane.py

### Execution
- docs/commander/MINDLE_MEDIA_AI_LOCAL_MARKETING_RUNTIME_BOOTSTRAP_AUTH_MP4_E2E_DIRECTIVE_v20.1_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.1_20261001.json

### Branch preflight
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_BRANCH_REBIND_AND_STALE_WORKTREE_RECOVERY_DIRECTIVE_v1.0_20261001.md

### Reference SSOT
- docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json
- docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md
- evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json

## 3. FROZEN PASS

- v14 base runtime TESTED_PASS
- v18.1 F27E UI TESTED_PASS
- v18.2 Shortform additive UI TESTED_PASS
- v19 integrated base product closeout accepted
- v20 gateway/adapter implementation accepted; cycle result MARKETING_AUTH_ENV_REQUIRED

## 4. v20.1 purpose

Resolve only the live runtime blockers:
- Marketing local checkout/runtime
- ephemeral in-memory auth
- ffmpeg runtime
- actual Contract/assets retrieval
- actual MP4 render/Preview/export
- truthful voiceover audio status

Do not reopen frozen base product/UI work.

## 5. REFERENCE_ONLY

All prior directives through v20 are CLOSED / REFERENCE_ONLY.

Do not execute:
- v19
- v20
- v18.2
or any older cycle as current work.

## 6. Exact v20.1 Evidence

Review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_REVIEW_v20.1_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_EVIDENCE_v20_1_20261001.json

Detail:
evidence/pc_remote/media-ai-marketing-live-shortform-v20_1-20261001/

Required files:
18

## Final rule

ONE EPOCH. ONE ACTIVE DIRECTIVE. ONE EVIDENCE CONTRACT.

SYNC → VALIDATE → START VERIFIED MARKETING LOCAL RUNTIME → EPHEMERAL AUTH → FFMPEG → REAL MP4 → EXACT EVIDENCE → PUSH → READBACK.
