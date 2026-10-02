# MINDLE MEDIA AI — LIVE UI VISUAL EVIDENCE MATERIALIZATION + SSOT COMPLIANCE DIAGNOSIS DIRECTIVE v16.0

Date: 2026-10-01
Status: ACTIVE — FINAL VISUAL EVIDENCE GATE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v15

v15 Evidence publication is accepted, but final UI adjudication is NOT complete.

Accepted:
- all exact v15 Evidence paths exist
- all 12 detail files exist
- remote push/readback verified
- Git lineage proves the current PNG blob was present at the initial APPROVED_PINNED commit
- exact f27e... binary was not recovered
- v14 product/runtime PASS remains preserved
- Python 51 PASS
- UI structure/interaction tests PASS

Unresolved and now mandatory:
1. the live UI screenshot itself was NOT published as a visual artifact; only a text reference was published
2. the worker recorded that dark-navy visual styling was NOT observed in the live UI
3. therefore representative visual confirmation cannot yet be requested responsibly
4. the live UI may be structurally compliant but visually non-compliant with the approved SSOT

This cycle materializes actual visual evidence and diagnoses whether the live implementation matches the approved UI candidate.

## 1. Protection

DO NOT:
- change the manifest hash yet
- redesign the UI
- add guessed colors/geometry
- modify layout to "look closer"
- rework models/runtime
- rerun long model E2E
- merge stale branches
- ask representative for approval before actual comparison images are published

The purpose of v16 is EVIDENCE + DIAGNOSIS first.

## 2. Inputs to compare

### Candidate approved SSOT PNG currently in repository
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Current SHA-256:
9aaf05be17a3b851717a8bcdbeaf9c589812cb02f4807e3e2c9d10e75709ad3d

Manifest historical expected SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

### Live canonical UI
http://127.0.0.1:8765/

Use the canonical branch and current product server only.

## 3. Phase A — publish actual visual artifacts

Create and save these EXACT files:

1. Current live UI full-page screenshot:
evidence/pc_remote/pc-work-live-ui-visual-v16-20261001/LIVE_UI_FULLPAGE.png

2. Current repository SSOT candidate copy:
evidence/pc_remote/pc-work-live-ui-visual-v16-20261001/SSOT_CANDIDATE_9AAF.png

The SSOT candidate copy must be byte-for-byte identical to:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Verify identical SHA-256.

3. Side-by-side comparison board:
evidence/pc_remote/pc-work-live-ui-visual-v16-20261001/LIVE_VS_SSOT_COMPARISON.png

The comparison board may only:
- place SSOT candidate and live screenshot side by side
- add labels
- add non-destructive annotation boxes/arrows
- must NOT edit either source image content

## 4. Phase B — visual compliance diagnosis

Compare the live UI against the candidate SSOT for:

- dark navy overall theme
- upper VIDEO / lower PHOTO stacking
- left media/input zone
- center Preview/work area
- right editing panel
- VIDEO Timeline
- independent VIDEO/PHOTO natural-language fields
- reference upload control
- Project Save
- Export
- additive 광고 숏폼 placement
- panel proportions
- spacing/alignment hierarchy
- visible typography hierarchy
- visual density
- borders/panels/backgrounds
- any missing major visual treatment

Classify each:
- MATCH
- STRUCTURAL_MATCH_VISUAL_MISMATCH
- MISSING
- NOT_COMPARABLE

Do not use subjective "close enough" language.

## 5. Phase C — CSS/source diagnosis

Inspect:
- ui/index.html
- ui/interaction.css
- ui/interaction.js
- ui/product_integration.js
- any linked CSS/assets used by the live page

Determine exactly why dark navy styling is not observed.

Record:
- which stylesheet(s) load
- whether a visual stylesheet is missing
- whether class names expected by CSS mismatch DOM
- whether only behavior CSS exists
- whether approved visual CSS was never implemented
- whether a stale server/root served the wrong UI
- whether the live screenshot was taken before styles loaded

No code changes in this phase unless needed only to fix an obvious wrong-server/wrong-static-root execution mistake.
If a true implementation gap exists, record it for the next implementation directive.

## 6. Phase D — live-source identity verification

Prove that the screenshot came from the canonical current worktree:

Record:
- repository root
- branch
- HEAD
- product server command
- served static root
- index.html absolute path
- CSS absolute paths
- timestamp
- screenshot SHA-256

If the server is serving any stale/other worktree:
- stop visual adjudication
- relaunch from canonical root
- recapture all visual artifacts

## 7. Result classification

VISUAL_MATCH_READY_FOR_REPRESENTATIVE:
- canonical live UI captured
- candidate SSOT captured
- major visual/structural elements match
- only hash provenance remains
- comparison package ready for representative

VISUAL_IMPLEMENTATION_GAP:
- canonical live UI is structurally present but materially differs from candidate SSOT
- exact missing visual implementation is diagnosed
- no unauthorized redesign performed

WRONG_RUNTIME_ROOT_FIXED:
- initial mismatch was from stale/wrong server root
- canonical relaunch resolves mismatch
- new screenshots prove it

FAIL:
- visual evidence cannot be captured or source identity cannot be proven

## 8. Exact v16 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_LIVE_UI_VISUAL_SSOT_DIAGNOSIS_REVIEW_v16.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_LIVE_UI_VISUAL_SSOT_DIAGNOSIS_EVIDENCE_v16_0_20261001.json

Detailed Evidence directory:
evidence/pc_remote/pc-work-live-ui-visual-v16-20261001/

Required files:
1. MANIFEST.json
2. LIVE_UI_FULLPAGE.png
3. SSOT_CANDIDATE_9AAF.png
4. LIVE_VS_SSOT_COMPARISON.png
5. VISUAL_COMPLIANCE_MATRIX.json
6. CSS_SOURCE_DIAGNOSIS.json
7. LIVE_SOURCE_IDENTITY.json
8. V15_PROVENANCE_PRESERVATION.json
9. REGRESSION_TEST_RESULTS.txt
10. OUTPUT_HASHES.sha256
11. REMOTE_PUSH_VERIFY.txt

No alternate filenames.

## 9. Completion gate

The worker may stop only after:
- all 11 files exist
- the three PNG artifacts exist and are non-zero
- SSOT_CANDIDATE_9AAF.png hash equals the source PNG hash
- live screenshot is from canonical current worktree
- visual diagnosis is explicit
- remote push/readback is verified

Do NOT request representative confirmation inside the worker response.
The commander will inspect the actual visual package first and then decide whether representative confirmation is needed.

## 10. End-of-cycle response

RESULT:
Repository:
Branch:
HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Live screenshot path:
SSOT candidate path:
Comparison image path:
Live source canonical: YES/NO
Dark navy observed: YES/NO
Overall visual result:
Implementation gap:
V14 product PASS preserved: YES/NO
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

DO NOT ASK THE REPRESENTATIVE TO CONFIRM AN IMAGE THAT HAS NOT BEEN MATERIALIZED. PUBLISH THE ACTUAL LIVE UI, THE CURRENT SSOT CANDIDATE, AND A SIDE-BY-SIDE COMPARISON FIRST; THEN THE COMMANDER WILL INSPECT THE VISUAL EVIDENCE.
