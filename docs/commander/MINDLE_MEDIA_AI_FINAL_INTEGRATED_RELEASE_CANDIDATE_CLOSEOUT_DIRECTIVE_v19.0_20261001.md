# MINDLE MEDIA AI — FINAL INTEGRATED RELEASE CANDIDATE CLOSEOUT DIRECTIVE v19.0

Date: 2026-10-01
Status: ACTIVE — FINAL CLOSEOUT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander acceptance of v18.1

v18.1 is ACCEPTED as TESTED_PASS.

Frozen PASS — DO NOT REWORK WITHOUT REGRESSION EVIDENCE:
- exact approved UI source F27E recovered and installed
- canonical SSOT PNG = f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
- ui/ssot_manifest.json matches canonical SSOT
- docs/01_UI_SSOT_FINAL.md synchronized
- real DOM/CSS visual implementation complete
- dark navy editor visual identity present
- upper VIDEO / lower PHOTO hierarchy preserved
- Preview / Timeline / command fields / reference upload / Save / Export preserved
- screenshot-cheat gate PASS
- Python regression 51 PASS
- UI tests 2 PASS
- PHOTO segmentation TESTED_PASS
- PHOTO 4x TESTED_PASS
- VIDEO tracking TESTED_PASS
- Korean STT TESTED_PASS
- Project Save / Export / Reopen TESTED_PASS
- adopted model identities preserved
- backend behavior preserved

Implementation commit:
c3d36c8cfffc56e8b087475e56c9263d056b5410

Remote verification commit:
f8c509175395caec50c623a41506fcd280cd919b

This directive MUST NOT reopen already-PASS model/UI recovery work.

## 1. Purpose

Create the final integrated MEDIA AI release-candidate closeout package and determine the precise status of the additive Advertising Shortform integration without allowing that external integration boundary to erase the proven base-product PASS.

This is a CLOSEOUT/INTEGRITY cycle, not a redesign cycle.

## 2. Mandatory read order

1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_STATE.json
3. Rule Registry
4. this v19 directive
5. MASTER handover
6. v14 final base-product runtime Evidence
7. v18.1 final UI Evidence
8. ui/ssot_manifest.json
9. docs/01_UI_SSOT_FINAL.md
10. FINAL_ADOPTED_MODEL_MANIFEST_V13.json
11. Shortform UI SSOT addendum
12. current shortform bridge tests / PR #23 implementation state

Do not execute old directives.

## 3. Base product final integrity audit

Verify without repeating long model E2E:

- canonical branch/head is current
- canonical F27E SSOT exists and hash matches
- approved_visual.css is loaded by live UI
- no white/basic fallback regression
- manifest/docs/asset agree
- v14 runtime Evidence remains present and internally consistent
- v18.1 UI Evidence remains present and internally consistent
- current Python regression PASS
- current UI tests PASS
- Save/Export code path remains intact
- no model substitution
- no backend regression
- no screenshot cheat
- no unexpected production/main changes

If an actual regression is detected:
- reproduce
- fix
- rerun only the affected area
- record before/after Evidence

Do NOT rerun long model inference merely to reproduce already-proven PASS.

## 4. Advertising Shortform boundary audit

The approved additive architecture remains:

Marketing AI
→ SHORTFORM BRIDGE
→ MINDLE MEDIA AI

and:

MINDLE MEDIA AI 광고 숏폼
→ Marketing AI request
→ SHORTFORM BRIDGE
→ MINDLE MEDIA AI

Rules:
- Marketing plans
- MEDIA AI produces
- no independent shortform app
- no duplicated Marketing planning logic inside MEDIA AI
- additive 광고 숏폼 only; base UI remains intact

Verify current code/tests for:
- shortform mode state
- bridge contract handling
- request/response validation
- service/product agnostic behavior
- no hard-coding to a single product
- UI additive action placement
- failure isolation: Shortform failure must not break base MEDIA AI

## 5. Live Shortform E2E gate

Attempt live Shortform E2E ONLY if the current environment already has the required approved external prerequisites.

Possible prerequisites include:
- reachable Marketing AI endpoint/contract
- approved asset/package input
- required bridge configuration
- permitted local runtime

Do not:
- invent an endpoint
- hard-code credentials
- ask the representative to provide secrets
- alter Marketing AI
- use unrelated sample assets as proof of live integration

If prerequisites exist:
run:
Contract → cuts → 9:16 → subtitles → voice → BGM → transitions → brand ending → Preview → approval-ready result → MP4 Export

If prerequisites do not exist:
status =
SHORTFORM_EXTERNAL_DEPENDENCY_VERIFY_REQUIRED

Record exact missing dependency and prove:
- base MEDIA AI remains TESTED_PASS
- shortform bridge/static contract tests pass
- missing external prerequisite is isolated
- no false FULL PASS is claimed

## 6. Final status vocabulary

Allowed final integrated results:

### FULL_TESTED_PASS
Use only if:
- base product remains PASS
- final UI remains PASS
- Shortform live E2E executes successfully
- final MP4/export evidence exists

### BASE_PRODUCT_TESTED_PASS_SHORTFORM_EXTERNAL_DEPENDENCY
Use if:
- base product remains fully TESTED_PASS
- final UI remains TESTED_PASS
- shortform bridge/code/tests pass
- live shortform is blocked only by missing approved external prerequisite

### FAIL
Use only if:
- base product regression exists
- UI regression exists
- shortform implementation itself is defective rather than externally blocked
- required Evidence is incomplete

Do not downgrade the proven base product to FAIL solely because Marketing AI or another external dependency is unavailable.

## 7. Final release-candidate summary

Produce one final consolidated machine-readable and human-readable summary containing:

- repository
- branch
- final HEAD
- base product status
- UI SSOT status
- approved UI SHA-256
- adopted model identities
- PHOTO segmentation status
- PHOTO 4x status
- VIDEO tracking status
- Korean STT status
- Save status
- Export status
- Reopen status
- Python regression
- UI regression
- screenshot-cheat gate
- shortform bridge static status
- shortform live E2E status
- shortform blocker if any
- commercial/release blocker distinction
- remaining VERIFY_REQUIRED items
- exact Evidence chain references
- remote push verification

## 8. Final Evidence chain integrity

Confirm these prior Evidence packages remain remotely readable:

- v14 runtime recovery package
- v15 provenance package
- v16 visual diagnosis package
- v17.1 handoff-blocked package
- v18 handoff-blocked package
- v18.1 final UI TESTED_PASS package

Do not regenerate them.
Reference them.

## 9. Exact v19 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_REVIEW_v19.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FINAL_INTEGRATED_RELEASE_CANDIDATE_CLOSEOUT_EVIDENCE_v19_0_20261001.json

Detailed directory:
evidence/pc_remote/media-ai-final-integrated-closeout-v19-20261001/

Required detail files:
1. MANIFEST.json
2. BASE_PRODUCT_INTEGRITY_AUDIT.json
3. UI_SSOT_FINAL_AUDIT.json
4. MODEL_IDENTITY_FINAL_AUDIT.json
5. REGRESSION_TEST_RESULTS.txt
6. SHORTFORM_BRIDGE_AUDIT.json
7. SHORTFORM_LIVE_E2E_RESULT.json
8. PRIOR_EVIDENCE_CHAIN_READBACK.json
9. FINAL_RELEASE_CANDIDATE_STATUS.json
10. OUTPUT_HASHES.sha256
11. REMOTE_PUSH_VERIFY.txt

All 11 required files must exist remotely.

## 10. No-change protection

Unless a real regression is found:
- no model changes
- no UI redesign
- no SSOT replacement
- no backend redesign
- no main merge
- no production deployment
- no paid/GPU expansion
- no new feature scope

This is closeout, not feature expansion.

## 11. Completion

Before stopping:
- commit authorized code fixes only if a real regression required them
- commit all v19 Evidence
- push to feature/ad-shortform-bridge-p0-20260926
- verify remote HEAD
- verify Review + machine Evidence + 11 detail files from remote
- record commit SHA and remote readback

## 12. End-of-cycle response

RESULT:
Repository:
Branch:
Final HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Base product:
UI SSOT:
Approved UI SHA-256:
PHOTO segmentation:
PHOTO 4x:
VIDEO tracking:
Korean STT:
Save:
Export:
Reopen:
Python regression:
UI regression:
Shortform bridge:
Shortform live E2E:
Shortform blocker:
Remaining VERIFY_REQUIRED:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE BASE MEDIA AI PRODUCT AND APPROVED UI ARE NOW PROVEN TESTED_PASS. FREEZE THEM. THIS FINAL CYCLE ONLY CONSOLIDATES RELEASE-CANDIDATE INTEGRITY AND DETERMINES WHETHER ADVERTISING SHORTFORM IS LIVE-TESTED OR CLEANLY ISOLATED BEHIND AN EXTERNAL DEPENDENCY.
