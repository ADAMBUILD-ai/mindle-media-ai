# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.2

Date: 2026-10-01
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20

## 0. Governing rule

Exactly ONE cycle is executable:

- docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_COMPLETION_DIRECTIVE_v20.0_20261001.md

Evidence contract:

- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.0_20261001.json

Authoritative lock:

- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json

Validator:

- scripts/validate_pc_work_control_plane.py

If Lock / Current Directive / State / Registry MD / Registry JSON disagree:
CONTROL_PLANE_MISMATCH_BLOCKED

Do not execute an older cycle on mismatch.

## 1. Mandatory start order

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run python scripts/validate_pc_work_control_plane.py
6. required result: CONTROL_PLANE_PASS
7. read CURRENT_PC_WORK_DIRECTIVE.md
8. read CURRENT_PC_WORK_STATE.json
9. execute only v20
10. publish only to v20 exact Evidence paths
11. commit, push, remote-readback

## 2. ACTIVE — the only executable set

### Control plane
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
- scripts/validate_pc_work_control_plane.py

### Execution
- docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_COMPLETION_DIRECTIVE_v20.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.0_20261001.json

### Branch preflight
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_BRANCH_REBIND_AND_STALE_WORKTREE_RECOVERY_DIRECTIVE_v1.0_20261001.md

### Reference SSOT used by v20
- docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json
- docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md
- evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json

## 3. FROZEN PASS — read only

### Base product
v14 runtime remains TESTED_PASS.

### Approved UI
v18.1 F27E UI remains TESTED_PASS.

Approved UI SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

### Shortform additive UI
v18.2 remains TESTED_PASS.

Preserved:
- AI 자동 편집 distinct
- 광고 숏폼 distinct
- 광고 숏폼 alone owns shortform-mode
- required action order PASS
- no independent shortform page

### Integrated closeout
v19 result:
BASE_PRODUCT_TESTED_PASS_SHORTFORM_EXTERNAL_DEPENDENCY

The v19 external dependency is now supplied by Marketing AI.
v19 is CLOSED / REFERENCE_ONLY.

## 4. VERIFIED MARKETING PROVIDER FOR v20

Repository:
ADAMBUILD-ai/mindle-marketing-department

PR:
#4

Branch:
feature/shortform-bridge-p0-20260926

Commit:
3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a

Workflow run:
36852551111

Workflow:
SUCCESS

Base URL:
http://127.0.0.1:4318

Secret ENV:
MARKETING_SHORTFORM_BRIDGE_TOKEN

Do not persist secret values.

## 5. REFERENCE_ONLY

All prior MEDIA AI directives through v19 are closed historical/reference cycles and MUST NOT be executed as current work.

This includes:
- v12–v13 recovery
- v14 runtime recovery
- v15–v18 UI recovery/implementation
- v18.2 Shortform UI correction
- v19 final integrated base-product closeout

Physical presence in the repository does not make them executable.

## 6. Exact v20 Evidence paths

Review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_REVIEW_v20.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_EVIDENCE_v20_0_20261001.json

Detail:
evidence/pc_remote/media-ai-marketing-live-shortform-v20-20261001/

Required files:
16

Any alternate current-cycle output is NONCOMPLIANT.

## 7. Final rule

ONE EPOCH. ONE ACTIVE DIRECTIVE. ONE EVIDENCE CONTRACT.

SYNC → VALIDATE → EXECUTE v20 → REAL MARKETING HTTP → REAL MP4 → EXACT EVIDENCE → PUSH → REMOTE READBACK.
