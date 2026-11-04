# MINDLE MEDIA AI — GOOGLE DRIVE F27E HANDOFF + FINAL UI IMPLEMENTATION CONTINUATION DIRECTIVE v18.1

Date: 2026-10-01
Status: ACTIVE — RESUME v18 FROM VERIFIED EXTERNAL HANDOFF
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v18

v18 result is accepted as:
ASSET_HANDOFF_REQUIRED

The worker correctly did not implement the visual UI because the exact F27E handoff file was absent from:
incoming/commander/MINDLE_MEDIA_AI_APPROVED_UI_F27E_20260913.png

The blocker has now been resolved by the commander.

The exact approved source has been uploaded to the user's connected Google Drive.

Handoff receipt:
docs/commander/MINDLE_MEDIA_AI_APPROVED_UI_GOOGLE_DRIVE_HANDOFF_RECEIPT_v1.0_20261001.json

Google Drive path:
/Google Drive/MINDLE_MEDIA_AI_HANDOFF/MINDLE_MEDIA_AI_APPROVED_UI_F27E_20260913.png

Google Drive file ID:
1hyZJpzsDecHgUFwYq463K30JlEJ4jgHA

Expected:
- PNG
- 1536 × 1024
- 1,737,365 bytes
- SHA-256:
  f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

THEREFORE:
DO NOT SEARCH LOCAL DISK FOR THE APPROVED SOURCE.
DO NOT CREATE A ZERO-BYTE PLACEHOLDER.
DO NOT STOP AT ASSET_HANDOFF_REQUIRED BEFORE ATTEMPTING THE EXACT GOOGLE DRIVE HANDOFF.

## 1. Mandatory start order

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_DIRECTIVE.md
5. read CURRENT_PC_WORK_STATE.json
6. read Rule Registry
7. read this v18.1 directive
8. read:
   docs/commander/MINDLE_MEDIA_AI_APPROVED_UI_GOOGLE_DRIVE_HANDOFF_RECEIPT_v1.0_20261001.json
9. retrieve the exact Google Drive file
10. continue through final UI implementation and Evidence publication without stopping after retrieval

## 2. Exact Google Drive retrieval

Use the connected Google Drive source first.

Locate by exact file ID:
1hyZJpzsDecHgUFwYq463K30JlEJ4jgHA

or exact path/name:
/Google Drive/MINDLE_MEDIA_AI_HANDOFF/MINDLE_MEDIA_AI_APPROVED_UI_F27E_20260913.png

Retrieve/download/materialize the raw PNG bytes into:

incoming/commander/MINDLE_MEDIA_AI_APPROVED_UI_F27E_20260913.png

After retrieval, verify ALL:
- file exists
- non-zero
- MIME/decoding is PNG
- dimensions = 1536 × 1024
- bytes = 1,737,365
- SHA-256 = f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

If Google Drive access itself fails:
- record the exact connector/browser/auth failure
- do not fall back to random local search
- do not ask the representative for the asset
- status may be DRIVE_HANDOFF_ACCESS_BLOCKED only after the exact file ID/path was attempted

## 3. Placeholder prohibition

v18 used zero-byte marker files to document the blocked state. That is accepted only as historical blocked evidence.

From v18.1 forward:
- zero-byte APPROVED_SSOT files are FORBIDDEN
- a required PNG counts as present only if it decodes and hash/size/dimensions are verified
- binary Evidence files must be actual bytes
- "path exists" is not enough

Any zero-byte required binary:
EVIDENCE_INVALID = YES
CYCLE_COMPLETE = NO

## 4. Preserve old invalid candidate

Before canonical replacement, preserve the current invalid 9AAF bytes:

evidence/pc_remote/pc-work-approved-ui-final-v18_1-20261001/LEGACY_INVALID_SSOT_9AAF.bin

Verify:
SHA-256 =
9aaf05be17a3b851717a8bcdbeaf9c589812cb02f4807e3e2c9d10e75709ad3d

Do not use it as visual authority.

## 5. Install the exact approved SSOT

Copy the verified handoff source to:

ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Re-verify canonical target:
- PNG decode PASS
- 1536 × 1024
- 1,737,365 bytes
- SHA-256 = f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

Then update SSOT metadata truthfully:

ui/ssot_manifest.json
- status = APPROVED_PINNED
- approved_ui_asset = assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- asset_sha256 = exact F27E value
- approved_at = 2026-09-13

docs/01_UI_SSOT_FINAL.md
- remove obsolete blocked-source wording
- record exact path/hash/date
- preserve approved structure and behavior rules

## 6. Final real DOM/CSS implementation

Implement the live canonical UI against the exact F27E approved source.

The approved source is visual authority.
Existing live DOM/function contract is behavior authority.

Required visual identity:
- dark navy / near-black professional editor
- cyan/blue neon separators and highlights
- violet/pink accent hierarchy where present
- upper VIDEO editor, lower PHOTO editor
- left / center / right panel hierarchy
- large Preview areas
- VIDEO Timeline
- natural-language command panels
- reference upload
- Project Save
- Export
- additive 광고 숏폼 only
- dense professional editing-tool visual hierarchy

Keep all controls real DOM elements.

Forbidden:
- screenshot as background
- full-page image overlay pretending to be UI
- replacing interactive controls with raster image
- model/backend changes
- unrelated redesign
- invented feature expansion

## 7. Live verification

After implementation:

1. launch the product from canonical current worktree
2. verify branch/HEAD/static root
3. confirm visual CSS actually loads
4. capture actual full-page live UI
5. copy exact approved F27E source into Evidence
6. create side-by-side comparison
7. create annotated delta
8. run screenshot-cheat gate
9. verify all controls remain interactive DOM
10. run tests

## 8. Visual compliance hard gate

Required classification:
MATCH / ACCEPTABLE_IMPLEMENTATION_VARIANCE / FAIL

Check:
- dark navy theme
- global top identity/navigation
- upper VIDEO / lower PHOTO
- video left panel
- video Preview
- Timeline
- video right controls
- video natural-language field
- photo left panel
- photo Preview
- photo right controls
- photo natural-language field
- reference upload
- Save
- Export
- 광고 숏폼 placement
- panel proportions
- spacing/alignment
- typography
- borders/backgrounds
- neon accent hierarchy

Hard FAIL:
- white/basic browser styling remains
- approved image used as background/overlay
- major panel hierarchy differs
- Preview/Timeline placement materially differs
- natural-language areas omitted
- Save/Export missing

## 9. Regression protection

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve:
- v14 PHOTO segmentation PASS
- PHOTO 4x PASS
- VIDEO tracking PASS
- Korean STT PASS
- Project Save/Export/Reopen PASS
- model identities unchanged
- backend behavior unchanged

Do not rerun long model E2E unless actual regression is detected.

## 10. Exact v18.1 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_GOOGLE_DRIVE_HANDOFF_FINAL_UI_REVIEW_v18.1_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_GOOGLE_DRIVE_HANDOFF_FINAL_UI_EVIDENCE_v18_1_20261001.json

Detail directory:
evidence/pc_remote/pc-work-approved-ui-final-v18_1-20261001/

Required files:
1. MANIFEST.json
2. DRIVE_HANDOFF_RECEIPT.json
3. COMMANDER_HANDOFF_HASH_VERIFY.json
4. LEGACY_INVALID_SSOT_9AAF.bin
5. APPROVED_SSOT_F27E.png
6. LIVE_UI_AFTER.png
7. LIVE_VS_APPROVED.png
8. VISUAL_DELTA_ANNOTATED.png
9. VISUAL_COMPLIANCE_MATRIX.json
10. SCREENSHOT_CHEAT_GATE.json
11. CSS_IMPLEMENTATION_RESULT.json
12. LIVE_SOURCE_IDENTITY.json
13. SSOT_MANIFEST_VERIFY.json
14. V14_PASS_PRESERVATION.json
15. REGRESSION_TEST_RESULTS.txt
16. OUTPUT_HASHES.sha256
17. REMOTE_PUSH_VERIFY.txt

All 17 files must exist remotely.
All binary image evidence required to be actual non-zero decodable files.

## 11. Completion results

TESTED_PASS:
- exact Google Drive F27E source retrieved
- hash/size/dimensions/decode verified
- canonical SSOT exact F27E
- manifest/docs corrected
- live UI visually implemented
- dark navy present
- screenshot-cheat gate PASS
- UI/Python regression PASS
- v14 product PASS preserved
- all 17 Evidence files remotely readable

DRIVE_HANDOFF_ACCESS_BLOCKED:
- only if exact Google Drive file ID/path was actually attempted and inaccessible
- exact access error recorded
- no substitute used

ASSET_HANDOFF_HASH_FAIL:
- Drive file retrieved but identity does not match expected F27E

FAIL:
- implementation/regression/evidence failure

## 12. End-of-cycle response

RESULT:
Repository:
Branch:
HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Drive file ID:
Drive handoff retrieved: YES/NO
Handoff bytes:
Handoff dimensions:
Handoff SHA-256:
Canonical SSOT SHA-256:
Manifest SHA-256:
Dark navy implemented: YES/NO
Visual compliance:
Screenshot cheat gate:
UI tests:
Python tests:
V14 PASS preserved:
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE EXACT APPROVED UI SOURCE HAS NOW BEEN DELIVERED TO GOOGLE DRIVE. RETRIEVE THAT FILE BY ITS EXACT ID/PATH, VERIFY F27E, INSTALL IT AS CANONICAL SSOT, IMPLEMENT THE REAL LIVE UI, AND COMPLETE THE VISUAL CLOSEOUT IN THE SAME CYCLE.
