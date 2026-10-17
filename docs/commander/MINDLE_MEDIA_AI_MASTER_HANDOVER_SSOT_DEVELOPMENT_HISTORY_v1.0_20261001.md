# MINDLE MEDIA AI — MASTER HANDOVER / SSOT / DEVELOPMENT HISTORY v1.0
Date: 2026-10-01
Status: MASTER HANDOVER — NEW WORKER MUST READ FIRST
Repository: ADAMBUILD-ai/mindle-media-ai
Active branch: feature/ad-shortform-bridge-p0-20260926
Prepared at HEAD: 5e6ca5e9456685df30e8369d543bd08d603f4ca9

# 0. Purpose
This document is the consolidated handover for MINDLE MEDIA AI. It collects the authoritative UI SSOT, approved model/runtime baseline, proven E2E history, shortform SSOT, PC Work operating rules, recent rework history, current route correction, and exact next-worker start procedure.

Do not infer missing facts from old partial reviews. Where documents conflict, use the precedence rules below.

# 1. Precedence / authority
1. User-approved UI source asset + ui/ssot_manifest.json + docs/01_UI_SSOT_FINAL.md
2. Approved SSOT addenda under docs/ssot/
3. Final adopted model/runtime manifest and final closeout evidence
4. Latest commander route-correction directives
5. Current-cycle Evidence
6. Older historical directives/reviews only as diagnostic history

A later REWORK caused by local materialization/automation limitations does NOT erase a prior evidence-backed PASS unless regression proves the prior PASS invalid.

# 2. UI SSOT — immutable
Authoritative files:
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json
- ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- ui/assets/ssot/README.md

Approved UI asset:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
Approval date: 2026-09-13
Manifest status: APPROVED_PINNED

Fixed structure:
- dark navy
- upper VIDEO editing / lower PHOTO editing
- both use left media + AI/natural-language instruction, center Preview/work area, right editing panel
- VIDEO includes Timeline
- VIDEO and PHOTO command fields are independent
- each command field includes reference upload / plus control
- project save and export preserved
- layout, colors, panel placement, proportions must not be inferred/redesigned
- product integration may add behavior only
- UI_SSOT_CHANGED must remain NO unless user explicitly approves a new UI SSOT

# 3. Approved Shortform UI SSOT
Authoritative:
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

Approved additive change:
- add 광고 숏폼 to upper VIDEO action row
- placement: between AI 자동 편집 and 프로젝트 저장
- existing UI otherwise unchanged

Architecture:
A. Marketing AI -> SHORTFORM BRIDGE -> MEDIA AI
B. MEDIA AI 광고 숏폼 -> Marketing AI request -> SHORTFORM BRIDGE -> MEDIA AI
Marketing plans; MEDIA AI produces.
Do not duplicate Marketing planning logic inside MEDIA AI.
Do not build an independent shortform app.

Shortform production target:
Contract -> actual cuts -> 9:16 -> subtitles -> voice -> BGM -> transitions -> brand ending -> Preview -> representative approval -> MP4 Export.

Important current product direction:
Shortform/Bridge must be product/service-agnostic, not hard-coded to one product. Architecture products are baseline content sources, but future lifestyle/commerce/content services must be connectable through the same generic contract.

# 4. Adopted model/runtime SSOT
Authoritative:
evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json
evidence/model_scout/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_V13.json

Adopted:
SAM 2.1 Hiera Base Plus
- revision b7320756a13354e7530a63935656d35b2f91a290
- model.safetensors
- 323476296 bytes
- SHA-256 2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780
- Apache-2.0
- PERPETUAL_USE_GATE_PASS

Whisper-small
- source openai/whisper-small
- revision 973afd24965f72e36ca33b3055d56a652f456b4d
- model.safetensors
- 966995080 bytes
- SHA-256 1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b
- Apache-2.0
- PERPETUAL_USE_GATE_PASS

Intel single-image-super-resolution-1032
- source openvinotoolkit/open_model_zoo
- revision a6946b6d6ce42cbf4278df20275fab199655fc7d
- XML SHA-384 4f355965e070341e1f1df5b954213e0ecca5d43faf8a0c9770efdf04c7442c88fb0aaeb825fc8091b30f0a674c808446
- BIN SHA-384 ec5a759c2d43eebf679040638ad765bc6ce5c16253421ddeb8acafd1ab6c8cb406f9f85b274771d9f670efc3d824e926
- Apache-2.0
- PERPETUAL_USE_GATE_PASS

Legacy/unadopted immutable:
- Whisper Large v3 Turbo
- Qualcomm RealESRGAN x4plus ONNX
Do not silently substitute these for adopted runtime.

Private frozen reference:
MINDLE1846/MINDLE-MEDIA-AI-MODELS
revision 9202e5744a191fa77562b0c0ffe6af8053f8e3d9
path VERIFIED_MODEL_CACHE/perpetual-use-alternatives/

# 5. Proven completed product history — critical
Authoritative final closeout:
evidence/model_scout/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_V13.json
This records:
MINDLE_MEDIA_AI_FINAL_CLOSEOUT: PASS
RELEASE_CANDIDATE_PASS: true
COMMERCIAL_RELEASE_BLOCKED: false
UI_SSOT_CHANGED: NO
Product owner manually confirmed actual PHOTO segmentation / VIDEO tracking / 4x upscale / Korean STT results, Preview, project save and export.

Critical later local E2E proof:
docs/commander/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_REVIEW_v32.0_20260925.md
evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json

v32 proven local results:
- PHOTO segmentation TESTED_PASS, SAM 2.1 CPU
- PHOTO 4x SISR TESTED_PASS; 1920x1080; 1,920,451 bytes; SHA-256 4806a7ab40db3cf8dabec2451ee58015c70e662834643389ae8b6d4684c9d35f
- VIDEO tracking TESTED_PASS with validated MP4
- Korean STT TESTED_PASS; exact pinned whisper-small CPU; 16kHz / 12.48s; WER 0.35714285714285715
- Project save PASS; project f1434a9a-e76a-4ff6-8a35-0e57ec6eae03; SHA-256 5643a63530fcfa73b89c4018e6ec373d829df09839822b60bfe72d7dfe3bf962
- Project export PASS; f1434a9a-e76a-4ff6-8a35-0e57ec6eae03_export.zip; 2,798,557 bytes; SHA-256 cbda249c11c1a52e1c63277d1628fbae361e812dff9f23bdeedd15603a0947c3

Source fixes proven:
- c2505411f9f066bc56f5475fa08ebf07267d3af9 — Windows VIDEO validation through OpenCV when ffprobe unavailable
- 95be3ee184b0277d9e03f4a667515cb67a6a2d50 — Korean STT standard-library WAV + internal WER, removing undeclared soundfile/jiwer dependency

v32 boundary:
backend/local product API real work/save/export PASS.
Browser-native file chooser could not be driven by desktop automation, so separate browser-only Preview/Save/Export replay was not asserted there.
This is a narrow automation boundary, NOT proof that the underlying product functions were never completed.

# 6. Historical remote packaging
Relevant history:
docs/commander/MINDLE_MEDIA_AI_COMPLETED_WORK_VERIFICATION_REVIEW_v30.1_20250925.md
and v28-v32 package/evidence files.

Remote package was verified with exact pinned SAM, Whisper-small, Intel SISR and free CPU OpenVINO. Some later PC Work cycles became over-focused on reconstructing old split artifacts and a missing exact part-01.

IMPORTANT:
Historical artifact reconstruction is NOT the product objective and must NOT be treated as the universal prerequisite if verified current local runtime/assets can execute the product.

# 7. Recent PC Work rework history
Recent chain:
v1 final UI activation -> v2 local service recovery -> v3 runtime/input recovery -> v4 verified runtime artifact recovery -> v5 transfer/reassembly -> v6 exact part-01 -> v7 human/auth gate -> v8 gate check -> v9 long-run -> v10 broad closeout -> v11 human gate.

These reviews accurately record their local observations, but the chain became over-dependent on historical Artifact ID 10797756522 and repeated GitHub authentication/download attempts.

Do not continue that loop as the primary strategy.

# 8. Current route correction — highest current commander instruction
Authoritative current directives:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FIRST_PRODUCT_RECOVERY_DIRECTIVE_v12.0_20261001.md
docs/commander/MINDLE_MEDIA_AI_PC_WORK_COMMANDER_ROUTE_CORRECTION_NO_GITHUB_LOGIN_LOOP_DIRECTIVE_v12.1_20261001.md

Mandatory:
- stop repeated Connect to GitHub / Sign in loops
- do not ask user to sign in as the first recovery action
- do not install/authenticate gh as first action
- do not make Artifact 10797756522 a universal prerequisite
- current Windows PC runtime/model/cache inventory FIRST
- four independent lanes: PHOTO segmentation / PHOTO 4x / VIDEO tracking / Korean STT
- run every lane currently runnable
- one blocked lane must not block others
- identify exact missing item per failed lane
- selective recovery only after proof
- historical artifact = last-resort source for a specific missing item
- actual product E2E, not artifact reconstruction, is the goal

# 9. New worker bootstrap
Authoritative:
docs/commander/MINDLE_MEDIA_AI_NEW_PC_WORKER_BOOTSTRAP_ROUTE_CORRECTION_HANDOFF_v1.0_20261001.md

New worker read order:
1. v12.1 route correction
2. v12.0 current-PC-first
3. Evidence location/commit/push operating rule
4. this MASTER handover
5. UI SSOT + shortform addendum + adopted model manifest + v32 proven local E2E
6. old v7-v11 only if diagnostic history is needed

First worker actions:
- dismiss leftover MEDIA AI GitHub auth dialogs safely
- no new auth flow
- confirm GITHUB_AUTH_LOOP_STOPPED
- inventory current PC
- create four-lane runtime matrix
- execute runnable lanes

# 10. PC Work Evidence operating rule
Authoritative:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

Current repo:
ADAMBUILD-ai/mindle-media-ai
Current branch:
feature/ad-shortform-bridge-p0-20260926

Cycle:
ACTUAL WORK -> SELF VERIFY -> Review MD + Evidence JSON + Manifest -> COMMIT -> PUSH -> REMOTE VERIFY -> ONE BROAD NEXT DIRECTIVE -> COMMIT/PUSH -> CONTINUE

Do not confuse local save with GitHub submission.
Do not ask “commit?” or “where save?” when directive already authorizes it.
Do not force push/main merge/Production deploy.

# 11. Evidence locations
Human reviews:
docs/commander/

Machine evidence:
evidence/pc_remote/

Cycle manifests/log/output references:
evidence/pc_remote/<cycle-name>/

Model Scout/adopted model evidence:
evidence/model_scout/

UI SSOT:
docs/01_UI_SSOT_FINAL.md
ui/ssot_manifest.json
ui/assets/ssot/

Shortform SSOT:
docs/ssot/

# 12. Product UI/runtime files
Key UI:
ui/index.html
ui/interaction.css
ui/interaction.js
ui/interaction.test.js
ui/product_integration.js
ui/ssot_structure.test.js

Approved UI image:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Current product server referenced by recent work:
src/media_ai/product_server.py

# 13. Shortform current state
P0 wiring implemented on PR #23:
- 광고 숏폼 mode entry
- existing natural-language input reuse
- MEDIA AI -> Marketing request hook
- Contract v1 reader
- 9:16 scene/timeline planning
- approved asset validation
- representative approval export gate
Unit/interaction tests passed in P0.
Live Shortform E2E remains VERIFY_REQUIRED until approved Marketing Contract v1 + approved assets are actually available.
Do not fabricate Contract/assets.
Do not let Shortform block base MEDIA AI.

# 14. UI behavior still to respect
From UI SSOT:
- Video AI command states: collapsed / expanded / executing; Enter submits and collapses
- Photo AI command same independent behavior
- reference upload states: idle / selected / uploading / ready / failed
- Save states: clean / dirty / saving / saved / failed
- Export states: ready / exporting / complete / failed
- responsive changes may reduce density but never exchange panel order or remove command/reference controls

# 15. Known mistakes to avoid
- generating substitute UI instead of using approved SSOT image
- treating old artifact reconstruction as the goal
- repeated GitHub auth dialogs
- blocking all lanes because one runtime is missing
- confusing input fixture filename with adopted inference model
- repeating already-PASS model scouting
- claiming PASS without real output
- claiming Evidence submitted before remote push verification
- micro-slicing every hash/model check into a new cycle
- asking user unnecessary technical questions already covered by directive
- using legacy/unadopted models as silent substitutes

# 16. Current next execution objective
New PC worker must:
1. stop auth loop
2. inventory current PC runtime/models/caches
3. reconcile against proven v32 runtime/evidence
4. build four-lane runtime matrix
5. execute every runnable base lane through real product E2E
6. recover only exact missing items selectively
7. preserve UI SSOT
8. keep Shortform independent
9. produce consolidated Evidence and one broad continuation directive

# 17. Handover closeout
The repository contains extensive historical directives and evidence. Do not replay them chronologically. Use this master as the map, then open only the authoritative/current files named above.

Final governing sentence:
PRODUCT FUNCTIONALITY IS THE GOAL. APPROVED UI/SSOT AND VERIFIED MODEL IDENTITIES ARE FIXED. HISTORICAL ARTIFACT RECOVERY IS A FALLBACK, NOT THE PRODUCT.
