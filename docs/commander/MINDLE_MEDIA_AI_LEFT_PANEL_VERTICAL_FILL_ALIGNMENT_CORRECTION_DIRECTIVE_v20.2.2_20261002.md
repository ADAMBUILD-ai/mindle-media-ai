# MINDLE MEDIA AI — LEFT PANEL VERTICAL FILL / ALIGNMENT FINAL CORRECTION DIRECTIVE v20.2.2

Date: 2026-10-02
Status: ACTIVE — LEFT PANEL ONLY CORRECTION
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.2

## 0. Commander ruling

v20.2.1 center/right correction is accepted as the current baseline.

Representative review of the latest Windows UI found one remaining visual defect:

- VIDEO left panel content remains compressed toward the top
- PHOTO left panel content remains compressed toward the top
- the outer left panel reaches the row bottom, but its functional content does not use the full height
- the natural-language / reference / chip area should extend downward and visually align with the center working area
- left panel visual weight is weaker than the center panel

Therefore:

STATUS = LEFT_PANEL_CORRECTION_REQUIRED

This cycle is LEFT PANEL ONLY.

## 1. HARD FREEZE — DO NOT CHANGE

The following areas from v20.2.1 are now frozen:

- VIDEO center Preview
- VIDEO transport
- VIDEO Timeline
- VIDEO right editor panel
- PHOTO center Preview
- PHOTO transport
- PHOTO right editor panel
- overall F27E color hierarchy
- top bar
- sidebar
- VIDEO header
- PHOTO header
- Shortform button identity/order
- Marketing/MP4/runtime/model functionality

Do not modify their geometry unless a left-panel change directly breaks them.

Required VIDEO header order remains:

영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

## 2. Root cause to fix

Current left panels are not full-height flex layouts.

They contain:

panel tabs
→ asset grid
→ command card

but the internal blocks keep their natural compact height.

Result:
- outer panel reaches the row bottom
- content stays at the top
- empty lower navy area remains
- left panel looks unfinished compared with the center

Fix the content distribution, not the outer row height.

## 3. VIDEO left panel — required final structure

Target:
VIDEO left panel bottom edge must align with VIDEO center/timeline bottom edge.

Use the existing functions only:

1. panel tabs
2. media asset grid
3. natural-language command area
4. reference image control
5. reference list/status
6. command chips
7. send button

Recommended implementation:

[data-panel="video-left"] {
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
}

Asset grid:
- keep near the top
- approximately 38–44% of usable content height
- thumbnails must remain visible and usable
- do not stretch thumbnails grotesquely

Command card:
- flex: 1
- use remaining height
- natural-language area becomes the dominant lower block
- do not leave an empty navy block beneath it

Inside command card:
- display:flex
- flex-direction:column
- input/label at top
- reference button/list in middle
- command chips/send control anchored near the bottom
- vertical spacing distributed naturally

The command card bottom should sit close to the left panel bottom.

## 4. PHOTO left panel — required final structure

Target:
PHOTO left panel bottom edge and internal content should visually align with PHOTO center bottom controls.

Use only existing functions:

1. panel tabs
2. photo asset grid
3. natural-language command area
4. reference image control
5. reference list/status
6. command chips
7. send button

Required:

[data-panel="photo-left"] {
  display:flex;
  flex-direction:column;
  min-height:0;
  height:100%;
}

Photo asset grid:
- top area approximately 30–38%
- preserve 3-column approved structure

Photo command card:
- flex:1
- fills the remaining lower area
- grows downward
- chips/send stay near the lower edge
- no unexplained blank block under the command area

## 5. Natural-language area importance

The natural-language command field is a primary MEDIA AI interaction surface.

It must not look like a tiny secondary widget.

For VIDEO and PHOTO:
- increase the visual height/presence of the command area
- preserve readable text
- preserve reference upload
- preserve chips
- preserve send button
- do not add new features simply to fill space

The remaining height must be used by the existing command workflow.

## 6. Left / center bottom-line alignment

At the representative's maximized Windows view:

VIDEO:
left panel bottom ≈ center timeline bottom ≈ right panel bottom

PHOTO:
left panel bottom ≈ center transport bottom ≈ right panel bottom

Target tolerance:
within approximately 6 px visual alignment where browser rendering allows.

Do not enforce alignment by adding meaningless padding.
Use real flex distribution.

## 7. Split-screen behavior

At the representative split-screen comparison width:

- left panel must still fill the full row height
- command area must not collapse back to a tiny card
- font and chips must remain readable
- no overflow clipping
- no hidden reference controls
- no new lower dead space

Responsive changes may reduce:
- gaps
- padding
- thumbnail height moderately

Responsive changes must NOT collapse:
- command workflow
- input field
- reference control
- chip row
- send button

## 8. Visual balance

The left panel must carry similar visual weight to the approved F27E UI.

Check:
- tab height
- thumbnail size
- command-card height
- input height
- reference button size
- chip size
- send-button size
- internal vertical spacing

Do not make the left panel visually heavier than the center.
Do not make it visibly weaker either.

## 9. Scope protection

Allowed files:
- ui/approved_visual.css
- ui/index.html ONLY if a wrapper/class is strictly necessary for flex distribution
- UI regression tests if required

Forbidden:
- center panel redesign
- right panel redesign
- color palette redesign
- Shortform behavior changes
- product runtime changes
- Marketing integration changes
- model changes
- icon work

## 10. Required Windows visual check

After correction:

1. reload the canonical MEDIA AI on Windows
2. show VIDEO full row
3. show PHOTO full row
4. capture maximized UI
5. capture VIDEO left-panel close view
6. capture PHOTO left-panel close view
7. capture split-screen comparison
8. leave the corrected UI open for representative inspection

Required representative-facing question:

"신작가님, 중앙은 유지한 상태에서 VIDEO/PHOTO 좌측 패널이 아래까지 자연스럽게 채워지고 중앙 하단선과 맞게 정리된 것이 맞습니까?"

Do not claim approval before the representative answers.

## 11. Functional protection

Re-test only the affected left-panel interactions:

VIDEO:
- media load
- natural-language input
- reference image
- chips
- send control

PHOTO:
- photo load
- natural-language input
- reference image
- chips
- send control

Also verify frozen functions remain unchanged:
- VIDEO Preview/Timeline
- PHOTO Preview
- Save/Export
- 광고 숏폼

## 12. Exact Evidence

Human Review:
docs/commander/MINDLE_MEDIA_AI_LEFT_PANEL_VERTICAL_FILL_ALIGNMENT_REVIEW_v20.2.2_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_LEFT_PANEL_VERTICAL_FILL_ALIGNMENT_EVIDENCE_v20_2_2_20261002.json

Detail directory:
evidence/pc_remote/media-ai-left-panel-v20_2_2-20261002/

Required files:
1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. V20_2_1_BASELINE_PRESERVATION.json
4. LEFT_PANEL_ROOT_CAUSE.json
5. BEFORE_VIDEO_LEFT.png
6. AFTER_VIDEO_LEFT.png
7. BEFORE_PHOTO_LEFT.png
8. AFTER_PHOTO_LEFT.png
9. AFTER_MAXIMIZED_FULL_UI.png
10. AFTER_SPLIT_FULL_UI.png
11. LEFT_CENTER_BOTTOM_ALIGNMENT.json
12. VIDEO_LEFT_FILL_AUDIT.json
13. PHOTO_LEFT_FILL_AUDIT.json
14. LEFT_PANEL_FUNCTION_ACTIVATION.json
15. FROZEN_CENTER_RIGHT_REGRESSION.json
16. SHORTFORM_PRESERVATION.json
17. REPRESENTATIVE_SCREEN_GATE.json
18. REGRESSION_TEST_RESULTS.txt
19. OUTPUT_HASHES.sha256
20. REMOTE_PUSH_VERIFY.txt

All PNG files must be actual non-zero Windows captures.

## 13. Result vocabulary

LEFT_PANEL_READY_FOR_REPRESENTATIVE:
- VIDEO left fills row height
- PHOTO left fills row height
- command areas extend downward naturally
- bottom lines align with center
- split-screen remains usable
- center/right remain unchanged
- functionality preserved
- UI left open on Windows

LEFT_PANEL_CORRECTION_REQUIRED:
- left dead space remains
- command area still compressed
- bottom alignment remains visibly off
- center/right were unintentionally changed
- functional regression exists

REPRESENTATIVE_UI_APPROVED:
Only after the representative explicitly approves the corrected full UI.

## 14. Icon gate

ICON PHASE = BLOCKED_PENDING_UI_APPROVAL

Do not create icon candidates in this cycle.

Only after representative says UI OK may the existing v20.2 icon phase resume.

## Final governing sentence

PRESERVE THE NOW-CORRECT CENTER AND RIGHT PANELS. FIX ONLY THE VIDEO/PHOTO LEFT PANELS SO THEIR EXISTING CONTENT USES THE FULL AVAILABLE HEIGHT, THE NATURAL-LANGUAGE/REFERENCE AREA EXTENDS DOWNWARD, THE BOTTOM EDGE ALIGNS WITH THE CENTER, AND NO EMPTY LOWER NAVY BLOCK REMAINS. THEN LEAVE THE REAL WINDOWS UI OPEN FOR REPRESENTATIVE REVIEW.
