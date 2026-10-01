# MINDLE MEDIA AI — SHORTFORM ADDITIVE UI SSOT REGRESSION CORRECTION DIRECTIVE v18.2

Date: 2026-10-01
Status: ACTIVE — NARROW CORRECTION ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v18.1

v18.1 is accepted for:
- exact Google Drive F27E source retrieval
- exact F27E hash / dimensions / PNG decode
- canonical SSOT replacement
- dark navy approved visual implementation
- screenshot-cheat gate PASS
- Python 51 PASS
- UI tests 2 PASS
- v14 product runtime PASS preserved
- remote Evidence publication 17/17

However v18.1 is NOT accepted as final product closeout because the current ui/index.html violates the approved Shortform UI SSOT Addendum.

Approved rule:
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

It requires:
- keep existing AI 자동 편집
- add exactly one new entry labeled 광고 숏폼
- place 광고 숏폼 between AI 자동 편집 and 프로젝트 저장
- additive implementation only

Current source has only one button:
- visible label: AI 자동 편집
- data-action: shortform-mode

Therefore current implementation has collapsed/replaced the two intended entries into one and is NONCOMPLIANT.

## 1. Scope lock

This cycle corrects ONLY the upper VIDEO action-row shortform additive regression.

DO NOT:
- redesign the F27E visual implementation
- alter dark navy theme
- change PHOTO area
- modify model/runtime code
- rerun long model E2E
- change Save/Export behavior
- change natural-language panels
- change Preview or Timeline placement
- change F27E canonical SSOT
- change approved model identities

All v18.1 PASS items remain frozen.

## 2. Required VIDEO action row

The upper VIDEO action row must contain, in this order:

1. 영상 불러오기
2. AI 자동 편집
3. 광고 숏폼
4. 프로젝트 저장
5. 내보내기

The exact new approved entry is:

Label:
광고 숏폼

Role:
enter advertising short-form mode

Placement:
between AI 자동 편집 and 프로젝트 저장

Visual:
same existing MINDLE MEDIA AI control family
NEW badge permitted

## 3. Functional action identity

The advertising shortform button MUST own:
data-action="shortform-mode"

The existing AI 자동 편집 control MUST NOT masquerade as shortform-mode.

Before changing code:
- inspect ui/interaction.js
- inspect ui/product_integration.js
- inspect current tests
- identify whether AI 자동 편집 already has a canonical action hook

Rules:
- if a canonical existing AI auto-edit action hook exists, restore/use it
- if UI-only visual control existed without a live backend hook, preserve it as a distinct real DOM button without falsely mapping it to shortform-mode
- do not invent backend behavior
- do not map both buttons to shortform-mode
- do not remove either button

## 4. Required regression tests

Add/strengthen tests so they fail if this regression returns.

Must assert:
- visible AI 자동 편집 control exists
- visible 광고 숏폼 control exists
- two controls are distinct DOM elements
- 광고 숏폼 has data-action="shortform-mode"
- 광고 숏폼 appears after AI 자동 편집
- 광고 숏폼 appears before 프로젝트 저장
- Project Save and Export remain present
- PHOTO action row unchanged
- exactly one advertising shortform entry exists
- no independent shortform app/page was created

## 5. Live UI verification

Launch canonical product server after correction.

Verify visually:
- F27E dark navy implementation remains
- AI 자동 편집 and 광고 숏폼 are both visible
- order is correct
- no header overflow/broken alignment at canonical capture width
- Save/Export remain visible
- no screenshot/background cheat introduced

Capture focused evidence of the VIDEO action row and full-page live UI.

## 6. Regression protection

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Run any new shortform-specific UI test added by this cycle.

Preserve:
- F27E canonical SSOT SHA-256:
  f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541
- PHOTO segmentation PASS
- PHOTO 4x PASS
- VIDEO tracking PASS
- Korean STT PASS
- Project Save/Export/Reopen PASS
- model identities unchanged
- backend unchanged unless an already-existing UI hook must be reconnected

## 7. Exact v18.2 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_SHORTFORM_ADDITIVE_SSOT_REGRESSION_REVIEW_v18.2_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_SHORTFORM_ADDITIVE_SSOT_REGRESSION_EVIDENCE_v18_2_20261001.json

Detailed Evidence directory:
evidence/pc_remote/pc-work-shortform-additive-v18_2-20261001/

Required detail files:
1. MANIFEST.json
2. BEFORE_VIDEO_ACTION_ROW.html
3. AFTER_VIDEO_ACTION_ROW.html
4. SHORTFORM_ACTION_IDENTITY.json
5. SHORTFORM_ORDER_ASSERTION.json
6. LIVE_UI_FULLPAGE.png
7. LIVE_VIDEO_ACTION_ROW.png
8. UI_SSOT_PRESERVATION.json
9. V18_1_PASS_PRESERVATION.json
10. REGRESSION_TEST_RESULTS.txt
11. OUTPUT_HASHES.sha256
12. REMOTE_PUSH_VERIFY.txt

All 12 must exist remotely.
PNG files must be real non-zero images.

## 8. Completion result

TESTED_PASS:
- AI 자동 편집 exists
- 광고 숏폼 exists
- distinct DOM elements
- 광고 숏폼 alone owns shortform-mode
- correct order
- F27E UI preserved
- tests PASS
- v18.1 PASS preserved
- all Evidence published and remotely verified

FAIL:
- additive rule remains broken
- shortform-mode identity ambiguous
- visual regression
- test regression
- evidence incomplete

## 9. End-of-cycle response

RESULT:
Repository:
Branch:
HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
AI 자동 편집 present: YES/NO
광고 숏폼 present: YES/NO
Distinct controls: YES/NO
광고 숏폼 data-action:
Order correct: YES/NO
F27E SSOT preserved: YES/NO
UI tests:
Python tests:
V18.1 PASS preserved: YES/NO
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

DO NOT TOUCH THE RECOVERED PRODUCT OR APPROVED F27E VISUAL SYSTEM. FIX ONLY THE ADDITIVE SHORTFORM UI CONTRACT: AI 자동 편집 MUST REMAIN, 광고 숏폼 MUST BE A SEPARATE ENTRY BETWEEN IT AND 프로젝트 저장, AND ONLY 광고 숏폼 MAY OWN shortform-mode.
