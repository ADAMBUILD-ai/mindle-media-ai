# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.4

Date: 2026-10-02
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20.2

## 0. Governing rule

Exactly ONE cycle is executable:

- docs/commander/MINDLE_MEDIA_AI_WINDOWS_ONSCREEN_UI_REPRESENTATIVE_VISUAL_FUNCTION_AUDIT_DIRECTIVE_v20.2_20261001.md

Evidence contract:

- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2_20261001.json

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
8. execute only v20.2
9. show the actual Windows UI and approved reference
10. exercise live controls visibly
11. leave UI open for representative
12. publish exact v20.2 Evidence
13. push and remote-readback

## 2. ACTIVE — the only executable set

### Control plane
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
- scripts/validate_pc_work_control_plane.py

### Execution
- docs/commander/MINDLE_MEDIA_AI_WINDOWS_ONSCREEN_UI_REPRESENTATIVE_VISUAL_FUNCTION_AUDIT_DIRECTIVE_v20.2_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2_20261001.json

### Reference SSOT
- ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json

## 3. FROZEN PASS

- v14 base runtime TESTED_PASS
- v18.1 F27E UI TESTED_PASS
- v18.2 Shortform additive UI TESTED_PASS
- v19 integrated base-product closeout accepted
- v20 Marketing gateway/adapter implementation accepted
- v20.1 live Marketing E2E MP4 PASS with voiceover audio dependency explicit

v20.1 MP4:
- 15 sec
- 1080x1920
- h264/aac
- BGM present
- subtitles present
- transitions present
- brand outro present
- SHA-256 641fc1323667168eb293cac8b3ec1a5d07c4d3a8d4818fa363dcb537e0faece4

Voiceover audio remains VERIFY_REQUIRED because no approved TTS runtime exists.

## 4. FINAL FIXED UI DEFINITION

Final fixed UI is:

F27E base visual/layout
PLUS
Shortform Addendum

Required VIDEO action order:

영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

F27E alone without 광고 숏폼 is incomplete.

## 5. REFERENCE_ONLY

All prior directives through v20.1 are CLOSED / REFERENCE_ONLY.

Do not execute v20.1, v20, v19, v18.2, or older cycles as current work.

## 6. Exact v20.2 Evidence

Review:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_UI_REPRESENTATIVE_VISUAL_FUNCTION_REVIEW_v20.2_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_UI_REPRESENTATIVE_VISUAL_FUNCTION_EVIDENCE_v20_2_20261001.json

Detail:
evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/

Required files:
20

## 7. Representative gate

The worker must leave the actual MEDIA AI UI open on the Windows screen.

Without explicit representative visual decision:
REPRESENTATIVE_VISUAL_REVIEW_REQUIRED

Final closeout remains blocked.

## Final rule

ONE EPOCH. ONE ACTIVE DIRECTIVE. ONE EVIDENCE CONTRACT.

SYNC → VALIDATE → SHOW REAL UI → COMPARE F27E + SHORTFORM ADDENDUM → EXERCISE CONTROLS → LEAVE UI OPEN → REPRESENTATIVE DECISION → EVIDENCE → PUSH → READBACK.
