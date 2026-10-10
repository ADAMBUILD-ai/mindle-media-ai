# MINDLE MEDIA AI — PC WORK FINAL UI ACTIVATION & SHORTFORM E2E DIRECTIVE v1.0
Date: 2026-09-30
Status: PC WORK — EXECUTE TO COMPLETION
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23
Base: 6f813a0a444a5f2be6db4632caab69aa8624fa1a

## 0. Objective
Use the real Windows PC to finish the remaining product-level work. Do not redesign or reinterpret the approved UI. Activate the already-developed functions in the approved UI and complete real local E2E evidence.

## 1. Immutable UI SSOT
Use the approved pinned UI and Shortform UI SSOT Addendum. Preserve all layout, colors, panel geometry, VIDEO/PHOTO hierarchy, natural-language cards, Preview, Timeline, project save and export.
Only the already-approved 광고 숏폼 entry is additive.
UI_SSOT_CHANGED:NO.

## 2. Existing MEDIA AI functions — activate in UI
Verify and activate through the actual UI:
- file import / native chooser
- PHOTO segmentation
- PHOTO 4x upscale
- VIDEO tracking
- Korean STT
- Preview
- project save
- export
Do not substitute backend/API evidence for the final UI replay.

## 3. Shortform Contract v1
Consume the Marketing AI-approved SHORTFORM BRIDGE Contract v1 handoff when available.
Do not hard-code or require any one product. Treat Contract v1 as product/service-agnostic.
Do not duplicate Marketing AI planning logic inside MEDIA AI.

## 4. Shortform real E2E
Through the approved 광고 숏폼 UI:
Contract ingest -> approved asset validation -> actual cut edit -> 9:16 -> subtitles -> voice/voiceover -> BGM -> transitions -> brand ending -> Preview -> representative approval -> MP4 Export.
If an approved Contract/asset handoff is not yet available, keep this lane VERIFY_REQUIRED and finish every independent MEDIA AI UI activation item first. Never fabricate an asset or approval.

## 5. Representative approval
Export must remain fail-closed before representative approval.
Surface the approval step in the existing UI flow without redesign.
After actual approval, record evidence and unlock MP4 export.

## 6. MP4 verification
Verify final file duration, 9:16 dimensions/aspect, decodability, audio track, bytes, SHA-256, reopen/playback and Preview-vs-Export consistency.

## 7. Time discipline
No passive wait loops. If one technical attempt shows no measurable progress within 10 minutes, capture evidence, change route and continue. Do not redo already-PASS model acquisition/runtime work unless regression proves breakage.

## 8. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_FINAL_UI_ACTIVATION_SHORTFORM_E2E_REVIEW_20260930.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_FINAL_UI_ACTIVATION_SHORTFORM_E2E_EVIDENCE_20260930.json
Record actual PC paths/hashes, UI screenshots, native chooser replay, each function result, shortform Contract identity, assets, timeline, Preview, approval, MP4, regressions and blockers.

## 9. Verdict discipline
PASS only evidence-backed actual PC/UI execution.
Keep already-PASS backend/runtime lanes frozen.
Failed/incomplete lane = REWORK and rerun only that lane and downstream dependents.

## 10. Completion
MEDIA_AI_PC_UI_FINAL:PASS requires existing MEDIA AI UI functions + Preview/save/export actual PC replay.
SHORTFORM_LIVE_E2E:PASS additionally requires real Contract v1, approved assets, full shortform render, representative approval and verified MP4.
If shortform upstream handoff is unavailable, do not falsely block the MEDIA AI base UI closeout; report SHORTFORM as scoped VERIFY_REQUIRED.

## Protection
No UI redesign, independent shortform app, hard-coded single-product dependency, automatic publishing, ad-spend action, main merge, Production deploy, force push, GPU/paid compute without approval, credential exposure, or Evidence overwrite.
