# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.5
DATE: 2026-10-02
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## START ORDER

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run python scripts/validate_pc_work_control_plane.py
6. require CONTROL_PLANE_PASS
7. read CURRENT_PC_WORK_STATE.json and Rule Registry
8. execute only v20.2.5
9. DO NOT change launcher/icon
10. consolidate conflicting row-height CSS
11. VIDEO: use right panel as height reference
12. PHOTO: use center panel as height reference
13. prove top/bottom/height delta <= 2px
14. prove full PHOTO row visible at document bottom
15. leave corrected icon-launched UI open
16. publish exact Evidence
17. push and remote-readback

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_FINAL_CORRECTION_DIRECTIVE_v20.2.5_20261002.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.5_20261002.json

## REPRESENTATIVE RULING

Launcher and branded icon are now frozen.

Remaining UI problem:
- VIDEO right is correct; left + center must match its exact row height
- PHOTO center is correct; left + right must match its exact row height
- at full page scroll bottom, all PHOTO lower controls must be completely visible

## HARD FREEZE

DO NOT CHANGE:
- desktop shortcut
- branded icon
- favicon
- launcher
- color hierarchy
- Shortform header/order
- runtime/model/Marketing functionality

## EXACT OUTPUTS

Review:
docs/commander/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_REVIEW_v20.2.5_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_EVIDENCE_v20_2_5_20261002.json

Detail:
evidence/pc_remote/media-ai-row-height-v20_2_5-20261002/

Required files:
20

## FINAL RULE

SYNC → VALIDATE → CONSOLIDATE HEIGHT RULES → VIDEO RIGHT REFERENCE → PHOTO CENTER REFERENCE → DOM GEOMETRY <=2PX → PAGE BOTTOM FULLY VISIBLE → REPRESENTATIVE CHECK.
