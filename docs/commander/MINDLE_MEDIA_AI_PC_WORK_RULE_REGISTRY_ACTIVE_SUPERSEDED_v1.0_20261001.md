# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.1

Date: 2026-10-01
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V19

## 0. Governing rule

There is exactly ONE current executable cycle.

Authoritative lock:
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json

Current executable cycle:
- docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_DIRECTIVE_v19.0_20261001.md

Current Evidence contract:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v19.0_20261001.json

If Lock / Current Directive / Current State / Registry JSON / this Registry disagree:
- STATUS = CONTROL_PLANE_MISMATCH_BLOCKED
- NO work may execute
- NO older directive may be selected by precedence or memory

## 1. Mandatory start order

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run: python scripts/validate_pc_work_control_plane.py
6. read CURRENT_PC_WORK_DIRECTIVE.md
7. read CURRENT_PC_WORK_STATE.json
8. read this Registry and its JSON twin
9. execute only the v19 directive
10. publish only to the v19 exact Evidence paths
11. commit / push / remote-readback

## 2. ACTIVE — the only executable set

### Control plane
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
- scripts/validate_pc_work_control_plane.py

### Execution
- docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_DIRECTIVE_v19.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v19.0_20261001.json

### Branch preflight
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_BRANCH_REBIND_AND_STALE_WORKTREE_RECOVERY_DIRECTIVE_v1.0_20261001.md

### Immutable/reference SSOT used by v19
- docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json
- docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md
- evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json
- evidence/model_scout/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_V13.json

## 3. FROZEN PASS — read-only evidence, not executable work

### v14 base product runtime
Preserved TESTED_PASS:
- PHOTO segmentation
- PHOTO 4x
- VIDEO tracking
- Korean STT
- Project Save / Export / Reopen
- adopted model identity

### v18.1 approved final UI
Preserved TESTED_PASS:
- exact F27E UI asset
- dark navy real DOM/CSS implementation
- screenshot-cheat gate PASS
- Python 51 PASS
- UI 2 PASS

Approved UI SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

### v18.2 additive Shortform UI correction
Preserved TESTED_PASS:
- AI 자동 편집 remains a distinct control
- 광고 숏폼 is a separate control
- 광고 숏폼 alone owns data-action="shortform-mode"
- order is 영상 불러오기 → AI 자동 편집 → 광고 숏폼 → 프로젝트 저장 → 내보내기
- no independent shortform editor
- F27E UI preserved

Code commit:
175e509da5cef1415d66fa527ce69711892819d7

Evidence finalization:
10563ab3c2e3ef3bbec6d23708975b94896edacd

Remote readback:
737cded9f09a568513a118abc0330e997a7865b3

## 4. REFERENCE_ONLY — never execute as current work

All prior recovery/correction directives through v18.2 are historical reference only, including:
- v12 / v12.1 route correction
- v13 / v13.1 Evidence-path recovery
- v14 asset/runtime recovery
- v15 UI provenance adjudication
- v16 visual diagnosis
- v17.0 / v17.1 UI source recovery
- v18.0 / v18.1 UI handoff and implementation
- v18.2 Shortform additive correction

Specific v18.2 directive:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_SHORTFORM_ADDITIVE_UI_SSOT_REGRESSION_CORRECTION_DIRECTIVE_v18.2_20261001.md

It is CLOSED / REFERENCE_ONLY.
It must not be executed again.

## 5. HISTORY_ONLY

PC Work v1-v11 chains and any unlisted old PC Work directive/review/evidence are HISTORY_ONLY unless the v19 directive explicitly references an exact file for evidence comparison.

Physical presence in the repository does not make a document executable.

## 6. Evidence path rule

Only the current v19 paths are valid completion outputs:

Review:
docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_REVIEW_v19.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_EVIDENCE_v19_0_20261001.json

Detailed directory:
evidence/pc_remote/media-ai-final-integrated-closeout-v19-20261001/

Required detail file count:
11

Any alternate current-cycle path is NONCOMPLIANT.

## 7. Control-plane invariant

All of the following MUST identify MEDIA-AI-20261001-V19 and the same v19 directive/contract:
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- this Registry
- machine Registry JSON

The validator must PASS before worker execution:
python scripts/validate_pc_work_control_plane.py

If it fails:
CONTROL_PLANE_MISMATCH_BLOCKED

Do not choose one conflicting source and continue.

## 8. Commander responsibility

Before every new cycle the commander must update, as one coherent control plane:
1. Lock
2. Current Directive
3. Current State
4. Registry MD
5. Registry JSON
6. Evidence Contract/path references

The representative is never responsible for reconciling these.

## Final rule

ONE EPOCH. ONE ACTIVE DIRECTIVE. ONE EVIDENCE CONTRACT. ALL PRIOR CYCLES ARE READ-ONLY.

SYNC → VALIDATE CONTROL PLANE → EXECUTE v19 → EXACT EVIDENCE → PUSH → REMOTE READBACK.
