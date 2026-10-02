# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.9

Date: 2026-10-02
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.5

## ACTIVE

Exactly one executable cycle:
- docs/commander/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_FINAL_CORRECTION_DIRECTIVE_v20.2.5_20261002.md

Evidence contract:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.5_20261002.json

## FROZEN

Do not change:
- Windows launcher
- desktop shortcut
- branded app icon
- favicon
- current colors
- Shortform action row
- runtime/model/Marketing integration

## CURRENT UI DEFECT

VIDEO:
- video-right is correct reference
- video-left and video-center must match its top/bottom/height

PHOTO:
- photo-center is correct reference
- photo-left and photo-right must match its top/bottom/height

Page bottom:
- full PHOTO row must be visible when scrolled to the document bottom

## HARD NUMERIC GATE

All VIDEO top/bottom/height max deltas <= 2px.
All PHOTO top/bottom/height max deltas <= 2px.
No required panel scrollHeight may exceed clientHeight by more than 2px if overflow would hide controls.
page_bottom_visible = true.

## EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_REVIEW_v20.2.5_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_EVIDENCE_v20_2_5_20261002.json

Detail:
evidence/pc_remote/media-ai-row-height-v20_2_5-20261002/

Required files: 20

## REFERENCE_ONLY

All prior directives through v20.2.4 are reference only.

## FINAL RULE

CONSOLIDATE HEIGHT CSS → MATCH REFERENCE PANELS → PROVE DOM GEOMETRY → PROVE BOTTOM VISIBILITY → REPRESENTATIVE CHECK.
