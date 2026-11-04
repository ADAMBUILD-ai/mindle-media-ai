# MINDLE MEDIA AI — COMMANDER APPROVED UI ASSET HANDOFF + PIXEL IMPLEMENTATION FINAL CLOSEOUT DIRECTIVE v18.0

Date: 2026-10-01
Status: ACTIVE — FINAL UI IMPLEMENTATION CYCLE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v17.1

v17.1 result is accepted as:
ASSET_HANDOFF_REQUIRED

This was the correct worker behavior because the exact approved source was not accessible inside the PC Work environment.

However, the commander has now independently recovered and verified the exact approved source from ChatGPT Library.

Verified commander source:
- Library filename: 네온 다크 테마 AI 미디어 편집기.png
- Type: PNG
- Dimensions: 1536 × 1024
- Bytes: 1,737,365
- SHA-256: f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
- Decode: PASS
- Visual inspection: PASS

Therefore:
DO NOT SEARCH FOR THE APPROVED UI AGAIN.
DO NOT USE THE 9AAF CANDIDATE AS VISUAL AUTHORITY.
THE ONLY REMAINING GATE IS ONE-TIME COMMANDER→PC ASSET HANDOFF, THEN IMPLEMENTATION.

Read:
docs/commander/MINDLE_MEDIA_AI_APPROVED_UI_ASSET_HANDOFF_MANIFEST_v1.0_20261001.json

## 1. Existing PASS items are frozen

The following are already PASS and MUST NOT be reworked without regression evidence:
- PHOTO segmentation
- PHOTO 4x
- VIDEO tracking
- Korean STT
- Project Save / Export / Reopen
- adopted model identities
- v14 runtime assets
- canonical branch binding
- Evidence circulation protocol

No model scouting.
No runtime rebuild.
No auth loop.
No product-backend redesign.

## 2. Exact handoff file location

The worker must receive the commander-verified exact PNG at:

incoming/commander/MINDLE_MEDIA_AI_APPROVED_UI_F27E_20260913.png

Before doing any visual implementation, run:

- file/decode validation
- dimensions validation = 1536 × 1024
- SHA-256 validation = f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

If the file is absent:
RESULT = ASSET_HANDOFF_REQUIRED
Do not search elsewhere.
Do not continue visual implementation.
Do not invent another source.

If the hash does not match:
RESULT = ASSET_HANDOFF_HASH_FAIL
Do not proceed.

## 3. Preserve the invalid legacy candidate before replacement

Current canonical path contains the historically mismatched/non-decodable 9AAF candidate.

Before replacement:
1. copy/archive the current file to:
   evidence/pc_remote/pc-work-approved-ui-final-v18-20261001/LEGACY_INVALID_SSOT_9AAF.bin
2. record its SHA-256:
   9aaf05be17a3b851717a8bcdbeaf9c589812cb02f4807e3e2c9d10e75709ad3d
3. do not treat it as an approved image

Then copy the exact verified F27E source to:

ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Re-verify:
SHA-256 MUST equal:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

## 4. SSOT metadata correction

Only after the exact F27E source is physically present and verified:

Update ui/ssot_manifest.json so it truthfully records:
- status: APPROVED_PINNED
- approved_ui_asset: assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- asset_sha256: f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
- approved_at: 2026-09-13

Update docs/01_UI_SSOT_FINAL.md:
- remove stale BLOCKED_SOURCE_ASSET_NOT_PRESENT wording
- record the exact approved F27E source
- preserve the fixed structure contract

Do not alter the identity/hash.

## 5. Approved visual identity to implement

The exact approved screenshot is now the sole visual authority.

Implement the canonical live UI to match it materially:

### Global
- dark navy / near-black editor background
- blue/cyan edge highlights and dividers
- MINDLE MEDIA AI top identity
- dense professional desktop editor layout
- rounded dark panels
- high-contrast white/gray typography
- neon blue + violet accents
- no white/basic browser-default page

### Upper VIDEO editor
- upper half of the product
- left source/library panel
- central large video preview
- lower video timeline directly under preview
- right edit controls panel
- natural-language command panel integrated on the left/lower-left
- reference image control
- Project Save and Export
- approved blue/violet hierarchy

### Lower PHOTO editor
- lower half of the product
- left image library + natural-language command
- large central image preview
- right photo edit controls
- Project Save and Export
- magenta/violet accent hierarchy where shown by approved UI

### Existing product contract
Preserve:
- upper VIDEO / lower PHOTO
- independent natural-language fields
- Preview
- Timeline
- reference upload
- Save
- Export
- additive 광고 숏폼 only
- existing runtime/backend behavior

The approved source image is VISUAL AUTHORITY.
Existing functional DOM contract is BEHAVIOR AUTHORITY.

## 6. Implementation rules

Allowed:
- CSS visual implementation
- DOM classes/wrappers needed only to accurately express approved layout
- non-functional icons/placeholders where existing product behavior already defines the function
- responsive safeguards that do not change hierarchy

Forbidden:
- screenshot-as-background cheat
- placing the approved UI image behind the app and calling it implementation
- flattening the application into one image
- removing live controls
- changing business/product behavior
- adding new unrelated features
- redesigning approved layout
- using 9AAF candidate as authority

All visible controls must remain real DOM/UI controls.

## 7. Required live verification

After implementation:

1. launch canonical product server from current worktree
2. verify served root and branch/HEAD
3. load the live editor
4. verify CSS/assets are actually loaded
5. capture full-page live screenshot
6. capture approved F27E source copy
7. produce side-by-side comparison
8. produce annotated visual delta
9. confirm no screenshot/background cheat
10. verify functional controls remain live

## 8. Required visual compliance matrix

Score each as:
MATCH / ACCEPTABLE_IMPLEMENTATION_VARIANCE / FAIL

Required:
- dark navy overall theme
- top identity/nav
- video upper / photo lower hierarchy
- left video library
- video preview
- timeline
- video right controls
- video natural-language panel
- lower photo library
- photo preview
- photo right controls
- photo natural-language panel
- Project Save
- Export
- reference upload
- neon blue/violet/pink hierarchy
- border/panel treatment
- spacing/alignment
- typography hierarchy

FAIL in dark navy theme, editor hierarchy, preview/timeline placement, natural-language panels, Save/Export, or screenshot-cheat gate means:
OVERALL = FAIL

## 9. Regression protection

Run:
- pytest -q
- node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve:
- v14 product PASS
- model identities unchanged
- Save/Export behavior
- no backend regression

Do not rerun long model E2E unless a regression appears.

## 10. Exact v18 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_APPROVED_UI_FINAL_IMPLEMENTATION_REVIEW_v18.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_APPROVED_UI_FINAL_IMPLEMENTATION_EVIDENCE_v18_0_20261001.json

Detailed Evidence directory:
evidence/pc_remote/pc-work-approved-ui-final-v18-20261001/

Required detail files:
1. MANIFEST.json
2. COMMANDER_HANDOFF_HASH_VERIFY.json
3. LEGACY_INVALID_SSOT_9AAF.bin
4. APPROVED_SSOT_F27E.png
5. LIVE_UI_AFTER.png
6. LIVE_VS_APPROVED.png
7. VISUAL_DELTA_ANNOTATED.png
8. VISUAL_COMPLIANCE_MATRIX.json
9. SCREENSHOT_CHEAT_GATE.json
10. CSS_IMPLEMENTATION_RESULT.json
11. LIVE_SOURCE_IDENTITY.json
12. SSOT_MANIFEST_VERIFY.json
13. V14_PASS_PRESERVATION.json
14. REGRESSION_TEST_RESULTS.txt
15. OUTPUT_HASHES.sha256
16. REMOTE_PUSH_VERIFY.txt

All 16 files must exist remotely.

## 11. Completion results

TESTED_PASS:
- exact handoff F27E asset verified
- canonical SSOT replaced with exact F27E source
- manifest/docs truthful
- live UI materially matches approved visual identity
- no screenshot cheat
- UI tests PASS
- Python tests PASS
- v14 product PASS preserved
- all Evidence remotely published

ASSET_HANDOFF_REQUIRED:
- only if the exact commander handoff file is not physically present at the specified PC path

ASSET_HANDOFF_HASH_FAIL:
- handoff file exists but exact SHA does not match

FAIL:
- visual implementation materially misses approved UI
- regression occurs
- screenshot cheat used
- evidence incomplete

## 12. End-of-cycle response

RESULT:
Repository:
Branch:
HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Commander handoff file present: YES/NO
Commander handoff SHA-256:
Canonical SSOT SHA-256:
Manifest SHA-256:
Dark navy implemented: YES/NO
Video editor visual match:
Photo editor visual match:
Screenshot cheat gate:
UI tests:
Python tests:
V14 product PASS preserved:
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE APPROVED F27E SOURCE HAS BEEN RECOVERED BY THE COMMANDER. STOP SEARCHING. ACCEPT ONLY THE EXACT HANDOFF FILE, VERIFY ITS HASH, INSTALL IT AS THE CANONICAL SSOT, IMPLEMENT THE LIVE UI AGAINST THAT SOURCE, AND CLOSE THE VISUAL GAP WITHOUT TOUCHING THE ALREADY-PASSING PRODUCT RUNTIME.
