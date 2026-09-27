# MINDLE MEDIA AI — SHORTFORM CONTRACT v1 LIVE E2E COMPLETION DIRECTIVE v1.0
Date: 2026-09-28
Status: EXECUTE TO REAL E2E COMPLETION
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23
Base head: ef1ff5a0b3e79d357c5d5b9e2923ee8c4f373766

## 0. Commander order
Complete the advertising shortform feature against the Marketing AI-approved and pinned SHORTFORM BRIDGE Contract v1 handoff.
Do not stop at schema/unit-test/P0 wiring.
The exit condition is a real E2E-produced MP4 after representative approval.

## 1. Immutable UI protection
Keep the approved MINDLE MEDIA AI UI/SSOT unchanged.
The already-approved incremental 광고 숏폼 entry is the only shortform UI addition.
Do not redesign layout, colors, panel geometry, natural-language cards, Preview, Timeline, PHOTO area, Save or Export.
UI_SSOT_CHANGED:NO is mandatory.

## 2. Contract v1 is the single source of truth
Consume the Marketing AI handoff exactly through SHORTFORM BRIDGE Contract v1.
Do not duplicate Marketing AI planning logic inside MEDIA AI.
Do not hard-code any specific product name or architectural-only field.
The implementation must remain product/service-agnostic so approved assets from architecture, lifestyle, commerce, content and future MINDLE services can use the same bridge.

Required generic concepts include:
product/service identity, target, campaign goal, duration, platform, hook, scenes/timing, approved asset references, subtitles, voiceover, music/BGM instruction, transitions, CTA, brand outro and representative-approval state.

## 3. Bidirectional entry
Both paths must converge on the same Contract v1 pipeline:
A. Marketing AI -> Contract v1 -> MEDIA AI 광고 숏폼
B. MEDIA AI 광고 숏폼 natural-language request -> Marketing AI request hook -> Contract v1 return -> same MEDIA AI pipeline
No duplicate production pipeline.

## 4. Activate shortform UI
Activate the approved 광고 숏폼 mode in the existing VIDEO workspace.
Reuse existing natural-language input, media/reference handling, Preview, Timeline, project save and Export.
Show Contract ingest/validation status and fail closed on missing/unapproved assets.
Do not fabricate placeholder approval.

## 5. Real production pipeline
Using one source-verifiable, explicitly advertising-approved Contract v1 handoff, execute:
Contract ingest -> asset validation/materialization -> scene/timeline build -> actual cut editing -> 9:16 composition/reframe -> subtitles -> voice/voiceover -> BGM -> transitions -> brand ending -> Preview.

Each stage must create inspectable Evidence. A generated plan alone is not execution.

## 6. 9:16 and cut-edit quality
Build the real 9:16 output at the Contract duration.
Preserve important visual subject/architecture/product regions when reframing.
Validate scene order, timing, cut boundaries, subtitle readability, audio balance, transition timing and brand-ending duration.
Do not call technical render success a quality PASS.

## 7. Subtitle / voice / BGM / transition / brand outro
Render each requested Contract element into the actual media output.
Record source/asset identity and output evidence.
Voice/BGM must not clip or drown speech.
Brand ending must use the Contract/brand asset and CTA supplied through the approved handoff; MEDIA AI must not invent campaign claims.

## 8. Preview and representative approval gate
Generate a real Preview from the assembled shortform.
Export remains fail-closed before representative approval.
Surface the representative approval action in the existing approved UI.
After approval, persist approval evidence and unlock MP4 Export.
Do not simulate approval.

## 9. MP4 export
After representative approval:
- export actual MP4;
- verify duration, 9:16 dimensions/aspect, decodability, audio track, file bytes and SHA-256;
- reopen/play the exported file;
- verify Preview vs Export consistency.
No auto-publish and no ad-spend action.

## 10. Regression
Preserve ordinary VIDEO/PHOTO editing behavior.
Run shortform Contract tests, UI interaction tests, full feasible repository regression and product server health.
Any regression = REWORK.

## 11. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_SHORTFORM_CONTRACT_V1_LIVE_E2E_FINAL_REVIEW_20260928.md
- docs/evidence/MINDLE_MEDIA_AI_SHORTFORM_CONTRACT_V1_LIVE_E2E_EVIDENCE_20260928.json

Evidence must include:
Contract version/hash or immutable identity; approved asset refs/hashes; bidirectional path tested; scene/timeline; cut-edit output; 9:16 dimensions; subtitle/voice/BGM/transition/brand-outro evidence; Preview; representative approval; final MP4 path/bytes/hash/duration/decode; regressions; changed files; commit/PR/Actions.

## 12. PASS discipline
Keep existing P0 wiring/tests PASS where still valid.
Do not promote VERIFY_REQUIRED to PASS without real evidence.
If any stage fails, fix and rerun only that stage and downstream dependents.
Do not stop on a generic blocker while a permitted alternative exists.

## 13. Final verdict
Declare SHORTFORM_LIVE_E2E:PASS only when:
- approved Contract v1 ingested
- approved assets materialized
- actual cut editing complete
- actual 9:16 render complete
- subtitles/voice/BGM/transitions/brand ending rendered
- Preview verified
- representative approval recorded
- final MP4 exported, decoded and hash-verified
- regression PASS
- UI_SSOT_CHANGED:NO

## 14. Automatic next directive
Immediately after verification, issue PASS/REWORK and commit the next directive under docs/commander. Do not wait for the user to request it.

## Protection
No independent shortform app. No UI redesign. No Marketing planning duplication. No hard-coded single-product dependency. No automatic publishing. No ad-spend execution. No main merge, Production deployment, force push, GPU/paid compute unless separately approved, credential exposure, or prior Evidence overwrite.
