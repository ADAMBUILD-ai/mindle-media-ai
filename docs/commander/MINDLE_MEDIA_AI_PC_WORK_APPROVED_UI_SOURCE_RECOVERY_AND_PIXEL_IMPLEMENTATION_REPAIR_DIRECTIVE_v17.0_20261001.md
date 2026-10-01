# MINDLE MEDIA AI — APPROVED UI SOURCE RECOVERY + PIXEL IMPLEMENTATION REPAIR DIRECTIVE v17.0

Date: 2026-10-01
Status: ACTIVE — VISUAL IMPLEMENTATION REPAIR
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander verdict on v16

v16 is accepted as a diagnostic PASS with result:

VISUAL_IMPLEMENTATION_GAP

Verified facts:
- canonical live UI was served from the current canonical worktree
- live screenshot was captured and remotely published
- structural UI controls are present
- Python regression: 51 passed
- Node UI structure/interaction: 2/2 passed
- v14 product/runtime PASS remains preserved
- dark-navy approved visual treatment is NOT present in the live canonical UI
- only interaction.css is loaded; no approved visual stylesheet is present
- wrong static root is NOT the cause
- screenshot timing is NOT the cause
- current repository "SSOT_CANDIDATE_9AAF.png" bytes cannot be decoded as a valid PNG by the worker
- therefore the current repository candidate cannot be trusted as a usable pixel reference even though it has a stable hash

This means final closeout cannot be achieved by changing manifest metadata alone.

## 1. Non-negotiable protection

DO NOT:
- alter model identities
- rerun model scouting
- rework PHOTO/VIDEO/STT/Save/Export
- change product backend contracts
- invent a new UI design
- use the corrupt/non-decodable 9AAF candidate as a pixel reference
- update manifest hash merely to match 9AAF
- claim UI PASS from structural tests alone

Preserve all v14 runtime PASS evidence.

## 2. Primary objective

Recover the authentic user-approved MEDIA AI UI visual source or the strongest verifiable historical visual reference, then implement ONLY the missing visual layer so the canonical live UI matches the approved design without changing the already-fixed structure and behavior.

The approved design identity remains:
- dark navy
- upper VIDEO
- lower PHOTO
- left media / natural-language zone
- center Preview/work area
- right editing panel
- VIDEO Timeline
- independent natural-language controls
- reference upload
- Project Save
- Export
- additive 광고 숏폼 only
- no independent shortform app
- no layout redesign

## 3. Phase A — recover an authentic visual reference

Search in this order:

A. Existing local MEDIA AI historical assets
- preserved stale worktree
- known 2026-09-13 / 09-15 / 09-21 / 09-25 / 09-30 MEDIA AI worktrees
- prior screenshots/output packages
- historical UI implementation packages
- Downloads/Documents paths specifically tied to MEDIA AI
- any local screenshot/evidence files referenced by historical directives

B. Repository history
- old branches/tags/commits containing UI screenshots or visual CSS
- old CSS/HTML implementation before/after SSOT pin
- evidence screenshots in historical commits

C. Existing accessible project/library material
- use only existing user-owned MEDIA AI material available to the worker/environment
- do not generate a replacement design

For each candidate:
- path/source
- date/commit if known
- file type
- decodable YES/NO
- dimensions
- SHA-256
- why it is or is not authentic
- visual relation to the approved design contract

## 4. Phase B — inspect historical visual CSS/source

Search Git/local history for any previous visual implementation containing:
- dark navy background
- panel/card styling
- VIDEO/PHOTO two-stack layout
- muted teal/accent usage if historically present
- preview/timeline panel styles
- button/input visual hierarchy

If authentic historical CSS exists:
- recover selectively
- do NOT wholesale merge old branches
- map selectors to current DOM
- document exact source commit/path

If no authentic CSS exists but a decodable approved historical screenshot/reference exists:
- implement the visual layer strictly from that reference and fixed contract
- no new features
- no layout changes beyond making the existing structure visually conform

If neither authentic CSS nor authentic visual reference can be recovered:
- status = APPROVED_VISUAL_SOURCE_REQUIRED
- publish all recovery evidence
- do not guess or redesign
- do not ask representative to approve the white/basic UI

## 5. Phase C — repair visual implementation only when grounded

Allowed code scope ONLY after authentic grounding:
- visual CSS
- CSS variables/tokens
- class hooks strictly required to attach visual CSS without changing behavior
- static visual assets proven authentic

Forbidden:
- backend changes
- model changes
- command behavior changes
- Save/Export behavior changes
- layout restructuring
- independent shortform UI
- speculative feature additions

## 6. Phase D — live visual verification

After repair, launch canonical product server and capture:

1. LIVE_UI_AFTER_REPAIR.png
2. APPROVED_REFERENCE_USED.png
3. LIVE_VS_APPROVED_AFTER_REPAIR.png

The approved reference copy must be decodable.

Verify:
- dark navy visible
- upper VIDEO/lower PHOTO
- panel hierarchy
- left/center/right alignment
- Preview
- Timeline
- command fields
- reference upload
- Save
- Export
- shortform additive only
- no behavior regression

## 7. Phase E — regression

Mandatory:
- pytest -q
- node --test ui/ssot_structure.test.js ui/interaction.test.js
- live product server load
- visual screenshot capture
- v14 product PASS preservation check
- no model identity changes
- no backend changes

Do not rerun expensive model inference unless a regression is detected.

## 8. SSOT metadata rule

Do not change ui/ssot_manifest.json in this cycle unless:
- a decodable authentic approved source is recovered,
- its provenance is established,
- its SHA-256 is verified,
- and it is actually used as the visual reference.

If an authentic approved source is recovered, update manifest/docs only to that proven source/hash and record why the prior metadata/candidate was invalid.

If authenticity is still uncertain, keep metadata unresolved and report APPROVED_VISUAL_SOURCE_REQUIRED.

## 9. Exact v17 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_APPROVED_UI_RECOVERY_PIXEL_REPAIR_REVIEW_v17.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_APPROVED_UI_RECOVERY_PIXEL_REPAIR_EVIDENCE_v17_0_20261001.json

Detailed Evidence directory:
evidence/pc_remote/pc-work-approved-ui-recovery-v17-20261001/

Required files:
1. MANIFEST.json
2. APPROVED_VISUAL_SOURCE_SEARCH.txt
3. HISTORICAL_VISUAL_SOURCE_MATRIX.json
4. HISTORICAL_CSS_SOURCE_MATRIX.json
5. APPROVED_REFERENCE_PROVENANCE.json
6. VISUAL_IMPLEMENTATION_CHANGESET.json
7. LIVE_UI_AFTER_REPAIR.png
8. APPROVED_REFERENCE_USED.png
9. LIVE_VS_APPROVED_AFTER_REPAIR.png
10. VISUAL_COMPLIANCE_AFTER_REPAIR.json
11. REGRESSION_TEST_RESULTS.txt
12. V14_PASS_PRESERVATION_CHECK.json
13. SSOT_METADATA_DECISION.json
14. OUTPUT_HASHES.sha256
15. REMOTE_PUSH_VERIFY.txt

No alternate filenames.

If no authentic reference is recovered, PNG items 7-9 may document the current live state/reference-search blocker only as specified in MANIFEST, but no fake approved reference may be created.

## 10. Result classification

TESTED_PASS:
- authentic approved visual reference recovered
- canonical live UI visually implemented from it
- visual compliance PASS
- regression PASS
- SSOT metadata consistent
- remote Evidence verified

VISUAL_REPAIR_PASS_METADATA_PENDING:
- authentic visual reference recovered and live UI repaired
- visual compliance/regression PASS
- only legacy manifest provenance remains unresolved
- no silent metadata rewrite

APPROVED_VISUAL_SOURCE_REQUIRED:
- authentic decodable approved visual reference cannot be recovered
- current 9AAF candidate remains unusable as pixel reference
- no speculative redesign performed
- all search/provenance evidence remotely published

FAIL:
- grounded repair attempted but regression or visual mismatch remains

## 11. Worker completion response

RESULT:
Repository:
Branch:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Authentic approved reference recovered: YES/NO
Reference source:
Reference SHA-256:
Historical visual CSS recovered: YES/NO
Live dark navy after repair: YES/NO
Visual compliance:
Python regression:
Node regression:
V14 product PASS preserved:
SSOT metadata changed: YES/NO
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE LIVE UI IS CURRENTLY A REAL VISUAL IMPLEMENTATION GAP. DO NOT MASK IT WITH A MANIFEST HASH CHANGE. RECOVER AN AUTHENTIC APPROVED VISUAL SOURCE OR HISTORICAL VISUAL CSS FIRST, THEN REPAIR ONLY THE VISUAL LAYER AND PROVE THE RESULT WITH ACTUAL SCREENSHOTS.
