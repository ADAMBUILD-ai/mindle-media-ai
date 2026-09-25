# MINDLE MEDIA AI — SHORTFORM UI SSOT ADDENDUM v1.0
Date: 2026-09-26
Status: APPROVED / PINNED

## Approved baseline
The user-approved MINDLE MEDIA AI UI remains the immutable base SSOT:
- two-tier dark navy layout
- upper VIDEO EDITING / lower PHOTO EDITING
- existing media, natural-language command cards, reference-image upload, previews, timeline, editing panels, project save and export remain unchanged.

## Approved incremental UI change
Add exactly one new entry to the upper VIDEO EDITING action row:
- label: 광고 숏폼
- role: enter advertising short-form mode
- placement: between AI 자동 편집 and 프로젝트 저장
- visual treatment: same existing MINDLE MEDIA AI control family; NEW badge permitted as shown in approved mockup.

No other layout, panel, size, alignment, color system, natural-language card, PHOTO area, Preview, Timeline, Save or Export control is redesigned by this approval.

## Functional architecture fixed
Bidirectional entry is approved:
1. Marketing AI -> SHORTFORM BRIDGE -> MINDLE MEDIA AI
2. MINDLE MEDIA AI 광고 숏폼 -> Marketing AI request -> 7-product asset collection/planning -> SHORTFORM BRIDGE -> MINDLE MEDIA AI production

Roles:
- MINDLE ADA 7 products: source content providers
- Marketing AI: campaign planning, asset selection, scenario/script/subtitle/voiceover/music/CTA planning
- SHORTFORM BRIDGE: shared structured production instruction
- MINDLE MEDIA AI: actual short-form assembly/edit/preview/save/export

## Development sequence
Phase 1: finish/lock current MEDIA AI UI activation and existing local E2E.
Phase 2: activate the approved 광고 숏폼 UI entry and bidirectional Marketing AI connection point.
Phase 3: incrementally add automated asset retrieval, scenario generation, 9:16 production, subtitle/voice/BGM/brand outro and natural-language re-editing.

Rule: additive implementation only. Existing approved MEDIA AI UI/SSOT must not be redesigned.
