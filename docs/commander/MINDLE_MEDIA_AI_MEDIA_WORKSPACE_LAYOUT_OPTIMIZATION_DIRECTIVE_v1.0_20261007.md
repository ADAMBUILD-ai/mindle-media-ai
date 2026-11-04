# MINDLE MEDIA AI — MEDIA WORKSPACE LAYOUT OPTIMIZATION DIRECTIVE v1.0

DATE: 2026-10-07
STATUS: QUEUED_NEXT — DO NOT EXECUTE UNTIL FINAL CLOSEOUT R2 IS CLOSED
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
CANONICAL_BRANCH: feature/ad-shortform-bridge-p0-20260926
NEXT_EPOCH: MEDIA-AI-20261007-MEDIA-WORKSPACE-LAYOUT-OPTIMIZATION-V1
OWNER: 신작가님
COMMANDER: MINDLE MEDIA AI 사령관

## 0. ACTIVATION CONDITION

This directive is the NEXT UI work item.

Do NOT execute while the current active epoch
MEDIA-AI-20261007-EMPLOYEE-PACKAGE-FINAL-CLOSEOUT-R2
is still ACTIVE.

Activation is allowed only after:
1. Final Closeout R2 publishes its required Review/Evidence,
2. the Commander reviews that Evidence,
3. R2 is closed by Commander decision,
4. CURRENT_PC_WORK_DIRECTIVE.md and the Control Plane are explicitly advanced to this epoch.

Do not mix package/runtime closeout changes and this UI layout work in one execution cycle.

## 1. OWNER-APPROVED UI PRINCIPLE

The governing Owner direction is:

“사진·영상의 본래 비율은 유지하고, Preview 아래 남는 공간에 필요한 기능들을 내려 배치해서 화면 낭비와 하단 기능 잘림을 동시에 없앤다.”

The purpose is not to fill the screen for appearance.
The purpose is to make the actual media workspace easier to use.

Design order is fixed:

MEDIA SIZE / ASPECT RATIO
→ REMAINING SPACE CALCULATION
→ FUNCTION RELOCATION

## 2. UI SSOT TO PRESERVE

Base approved UI:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Approved asset SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

Shortform Addendum:
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

Final visual definition remains:
F27E BASE + SHORTFORM ADDENDUM

Stable workspace geometry reference:
97900cc6c784e74b4224333fa2cc84d29c611f87

Known bad clipping commit that must not be reintroduced:
2ab174e03dc786c53f38ba956dea95f8e1ccd5a7

## 3. HARD PROHIBITIONS

Do not:
- stretch VIDEO or PHOTO vertically to fill unused space,
- distort source aspect ratio,
- solve layout by fixed-height clipping,
- hide required controls with overflow:hidden,
- allow bottom controls to disappear on smaller windows,
- remove or hide the 광고 숏폼 action,
- redesign the whole product UI,
- change unrelated runtime/backend behavior,
- regress previously working media functions.

## 4. COMMON VIDEO / PHOTO LAYOUT RULE

Use the same workspace language for VIDEO and PHOTO.

Upper area:
- media Preview,
- aspect ratio preserved,
- centered and proportionally fit,
- no unnecessary enlargement.

Lower area:
- use remaining Preview-bottom space as an active work area,
- place relevant controls based on available space and workflow priority,
- all important functions must remain reachable.

If all controls do not fit:
- use responsive reflow,
- use legitimate scrolling where appropriate,
- use collapsible low-frequency sections if necessary,
- never solve it by making functions inaccessible.

## 5. VIDEO REQUIREMENTS

Preserve original video ratio.

Review and relocate, where useful, into the available lower workspace:
- Timeline,
- transport/playback controls,
- current position,
- tracking state,
- AI execution state,
- result status,
- related VIDEO controls,
- project save,
- export.

Required VIDEO action order remains:

영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

광고 숏폼 must remain visible and accessible.

## 6. PHOTO REQUIREMENTS

Preserve original photo ratio for landscape, portrait, and other aspect ratios.

Use remaining workspace for:
- SAM segmentation,
- AI editing actions,
- Intel 4× upscale,
- job status,
- result / before-after inspection,
- project save,
- export,
- related PHOTO controls.

VIDEO and PHOTO may use different functional contents, but alignment, spacing, sizing logic, and interaction language must remain coherent.

## 7. RESPONSIVE TEST MATRIX

Required viewport tests:

A. 1920 × 1080
B. 1600 × 900
C. 1366 × 768

For both VIDEO and PHOTO confirm:
- Preview aspect ratio preserved,
- no media distortion,
- no bottom clipping,
- Timeline reachable where applicable,
- major AI actions reachable,
- project save reachable,
- export reachable,
- Shortform reachable in VIDEO,
- required controls do not disappear,
- any necessary scrolling behaves normally,
- left/right panels do not crush the central work area.

## 8. IMPLEMENTATION ORDER

1. Measure current viewport and workspace geometry.
2. Measure actual Preview width/height and media ratio.
3. Calculate remaining vertical space.
4. Identify controls currently pushed outside useful view.
5. Reflow only the necessary controls into the lower work area.
6. Remove clipping-causing layout constraints.
7. Preserve existing events/state/function bindings.
8. Test VIDEO.
9. Test PHOTO.
10. Run regression.
11. Capture actual screenshots and measurements.
12. Publish Evidence for Commander review.

Do not rebuild the approved UI from scratch.

## 9. REGRESSION REQUIREMENTS

After layout changes, verify at minimum:

- VIDEO Import
- VIDEO Playback
- SAM VIDEO Tracking
- Korean STT
- PHOTO Import
- SAM PHOTO Segmentation
- Intel 4× Upscale
- Preview
- Project Save
- Project Reopen
- Export
- Shortform unavailable graceful handling
- Desktop launch

Existing function bindings must not be broken merely because controls were relocated.

## 10. REQUIRED SCREENSHOT EVIDENCE

VIDEO:
- VIDEO_1920x1080.png
- VIDEO_1600x900.png
- VIDEO_1366x768.png

PHOTO:
- PHOTO_1920x1080.png
- PHOTO_1600x900.png
- PHOTO_1366x768.png

Screenshots must show:
- complete Preview,
- preserved source ratio,
- lower work area,
- primary actions,
- save/export,
- VIDEO 광고 숏폼,
- no clipped bottom controls.

## 11. REQUIRED MACHINE EVIDENCE

Save final outputs at:

Review:
docs/commander/MINDLE_MEDIA_AI_MEDIA_WORKSPACE_LAYOUT_OPTIMIZATION_REVIEW_v1.0_20261007.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MEDIA_WORKSPACE_LAYOUT_OPTIMIZATION_EVIDENCE_v1_0_20261007.json

Detail directory:
evidence/pc_remote/media-ai-media-workspace-layout-optimization-v1_0-20261007/

Required detail files:
- VIDEO_1920x1080.png
- VIDEO_1600x900.png
- VIDEO_1366x768.png
- PHOTO_1920x1080.png
- PHOTO_1600x900.png
- PHOTO_1366x768.png
- LAYOUT_MEASUREMENT.json
- REGRESSION_TEST_RESULT.json
- REMOTE_READBACK.txt

## 12. REVIEW STATUS VOCABULARY

Each required criterion must be one of:
PASS
FAIL
PARTIAL
BLOCKED

Evidence-free PASS is forbidden.

## 13. COMPLETION GATES

PASS requires all of the following:

- VIDEO source aspect ratio preserved
- PHOTO source aspect ratio preserved
- Preview bottom unused area actively utilized
- no important lower-function clipping
- all primary controls reachable
- VIDEO/PHOTO layout language aligned
- F27E identity preserved
- Shortform Addendum preserved
- 1920×1080 actual-screen PASS
- 1600×900 actual-screen PASS
- 1366×768 actual-screen PASS
- regression PASS
- final remote readback PASS
- required Review/Evidence present on canonical branch

Worker completion result:

PASS_MEDIA_WORKSPACE_LAYOUT_OPTIMIZATION_OWNER_REVIEW_READY

This result means ready for Owner review only.
It does not mean final Owner UI lock.

## 14. GIT / EXECUTION RULES

Canonical branch only:
feature/ad-shortform-bridge-p0-20260926

Forbidden:
- main merge
- force push
- new repository
- arbitrary worktree
- reuse of old work/* branch
- deletion of historical Evidence
- PASS without runtime/screenshot Evidence

After execution:
Commit
→ push canonical branch without force
→ remote readback
→ record commit SHA and Evidence paths.

## FINAL EXECUTION ORDER

Preserve media aspect ratio first.
Calculate remaining space second.
Relocate required functions third.

Do not stretch media to consume empty space.
Do not leave useful Preview-bottom space idle when it can carry required work controls.
Do not hide lower controls to make the layout appear to fit.

Actual VIDEO/PHOTO runtime screenshots and Evidence are mandatory before completion.
