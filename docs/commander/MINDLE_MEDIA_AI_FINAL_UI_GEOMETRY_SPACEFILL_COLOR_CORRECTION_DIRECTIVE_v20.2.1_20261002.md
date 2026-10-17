# MINDLE MEDIA AI — FINAL UI GEOMETRY / SPACE-FILL / COLOR COMPLIANCE CORRECTION DIRECTIVE v20.2.1

Date: 2026-10-02
Status: ACTIVE — UI_CORRECTION_REQUIRED
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.1

## 0. Commander ruling

The current Windows live UI is NOT accepted as the final fixed UI.

Representative-provided Windows photos show material mismatch against the approved visual direction.

Do NOT begin the icon phase.

The representative has specifically rejected the current UI because:
- central VIDEO area leaves unnecessary empty lower space
- VIDEO right panel leaves unnecessary empty lower space
- PHOTO center leaves a large empty lower/middle area
- PHOTO right panel leaves a large empty lower area
- overall content density is lower than the approved fixed UI
- panel proportions differ
- visual colors / neon accents / contrast differ from the approved fixed UI
- the UI looks compressed rather than proportionally filled

Status:
UI_CORRECTION_REQUIRED

## 1. Final fixed UI authority

Final fixed UI =

A. F27E base visual/layout authority:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

PLUS

B. Shortform Addendum:
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

Required VIDEO action order:

영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

The F27E image fixes the overall geometry, visual density, panel proportions, color hierarchy and working-area balance.
The Shortform Addendum adds the separate 광고 숏폼 button without redesigning the base layout.

## 2. Proven CSS root causes — MUST CORRECT

Current file:
ui/approved_visual.css

The following current rules are directly implicated:

### A. Aggressive compact breakpoints

At max-width 1400 and max-width 1100:

[data-layout="left-center-right"] min-height is reduced to about 300px
PHOTO layout min-height is reduced to about 286px

At the same time:

VIDEO Preview min-height is reduced to about 116px
PHOTO Preview min-height is reduced to about 155px

This leaves panel height that is not being meaningfully occupied by working content.

### B. PHOTO center forced empty middle

Current PHOTO center uses:

display: flex
justify-content: space-between

The Preview has a small fixed/min height.
The transport is pushed toward the bottom.

Result:
large empty middle zone.

### C. Right panels do not vertically distribute their content

VIDEO/PHOTO right panels stretch to the full row height, but controls remain compressed near the top.
This produces unused lower vertical space.

### D. Duplicate/nested responsive compression

The max-width 1400 and max-width 1100 rules substantially duplicate the same compact geometry and force the application into an over-compressed state when the Windows screen is split.

This must be replaced with a proportional fill strategy.

### E. Color hierarchy mismatch

The current live UI is visually darker/flatter and less saturated than the approved F27E visual identity.

Do not eyeball new colors.

Use the F27E reference as the visual source for:
- navy background levels
- blue/cyan borders
- violet VIDEO AI accents
- pink/magenta PHOTO accents
- selected tabs
- button contrast
- panel separation
- slider accent hierarchy

## 3. Canonical full-screen geometry — MUST MATCH FIRST

The representative must judge the product in a maximized/full usable browser window.

The Windows worker must NOT use a narrow side-by-side browser pane as the final geometry judgment.

Side-by-side mode is only for reference comparison.

After comparison:
MAXIMIZE the MEDIA AI browser/app.

At canonical full window:
- VIDEO and PHOTO work areas must fill the available width
- central Preview/work area must visually dominate the center column
- right editor panel must be fully populated vertically
- no large unexplained dead zones
- lower PHOTO section must feel as dense/complete as the approved F27E reference

## 4. Responsive rule — split screen must also remain filled

Even when the representative compares the reference and live UI side-by-side:

DO NOT shrink the live editor into a tiny compressed mockup.

At widths below 1400:
- scale controls proportionally
- reduce margins/gaps first
- reduce sidebar width
- reduce text size moderately
- DO NOT collapse Preview height to 116/155px while retaining 286/300px panel rows
- DO NOT create large dead zones

Responsive state must remain a usable editor, not a miniature layout.

## 5. VIDEO center correction

The VIDEO center column must occupy the full panel height.

Required proportions:
- Preview: approximately 45–52% of center usable height
- transport: compact fixed band
- Timeline: all remaining height

Implementation principle:
- [data-panel="video-center"] flex: column
- [data-preview="video"] flex-grow / proportional basis
- [data-timeline="video"] flex: 1
- timeline tracks must visibly consume the timeline area
- avoid a dark empty block below the last track
- if the timeline grows, distribute row/track height or provide visible timeline workspace grid

At representative target size, the center must look filled vertically.

## 6. VIDEO right panel correction

The VIDEO right editor panel must visually fill its height.

Do not leave all controls packed at top with a blank lower half.

Use the existing approved functional groups only:
- tabs
- basic edit tools
- screen settings
- stabilization
- noise reduction

Allowed:
- increase vertical spacing proportionally
- increase tool tile height
- increase range row height
- place toggle group toward lower section
- use internal flex/grid distribution

Forbidden:
- invent unrelated controls just to fill space
- stretch empty decorative blocks
- redesign the approved tool hierarchy

## 7. PHOTO center correction

The PHOTO center currently has the most obvious empty-space defect.

Remove the geometry that creates a large middle void.

Current problematic pattern:
justify-content: space-between
+
small Preview
+
bottom transport

Required:
- PHOTO Preview must flex-grow and occupy the center area
- image must scale/crop within the approved preview frame
- transport sits directly below Preview
- no large empty block between Preview and transport
- Preview should visually dominate the center column similarly to F27E

Use:
display:flex
flex-direction:column

Preview:
flex:1

Transport:
fixed/auto natural height

Do NOT use space-between to manufacture distance.

## 8. PHOTO right panel correction

The PHOTO right panel must be vertically balanced.

Required groups:
- tabs
- basic edit tools
- color adjustment
- reset/apply actions

The color controls and bottom actions should use the full available height in a visually intentional way.

No large blank lower/middle area.

Use proportional row spacing/flex distribution only.
Do not invent tools.

## 9. Left panels

VIDEO and PHOTO left media/natural-language panels should also use their full available height.

Preserve:
- asset thumbnails
- natural-language input
- reference image
- chips
- send control

The command panel must remain visually strong and similar in size/prominence to the approved F27E reference.

Do not make the natural-language area tiny.

## 10. Column proportions

Current compact mode uses approximately:
28% / flexible / 25%

Re-tune against the F27E approved visual.

Target visual relationship:
- left: approximately 27–30%
- center: largest working zone
- right: approximately 25–27%

Do not let the center become narrow merely to preserve side-by-side comparison.

At canonical full-screen, use the approved visual proportions first.

## 11. Color compliance

Create a CSS token audit based on F27E.

Compare:
- body/navy background
- panel navy
- panel border
- selected tab cyan
- primary blue
- VIDEO violet
- PHOTO pink/magenta
- muted text
- white text
- slider blue / cyan / green / yellow accents

Required output:
COLOR_TOKEN_COMPARISON.json

For each token:
- current CSS value
- corrected CSS value
- reference role
- reason

Do not use arbitrary new brand colors.

## 12. Required before/after capture sizes

Capture at least TWO runtime widths.

### A. Canonical maximized
Use the actual maximized Windows browser/app.
Record viewport width/height.

### B. Split comparison
Use the side-by-side comparison state.
Record viewport width/height.

Both must:
- have no large unexplained empty panel zones
- preserve controls
- preserve Shortform button
- preserve full editor usability

## 13. Representative visual comparison

On Windows:

1. open the approved F27E base reference
2. make the Shortform Addendum requirement visible
3. open the corrected live UI
4. first show side-by-side
5. then maximize corrected live UI
6. leave it open

Required question:

"신작가님, 지금 수정된 실제 MEDIA AI 화면이 기본 F27E 구조와 색상·밀도·패널 비율을 유지하면서 광고 숏폼까지 포함한 최종 UI로 맞습니까?"

Do not claim approval before the representative answers.

## 14. Functional activation protection

After layout correction, recheck:
- VIDEO load
- AI 자동 편집
- 광고 숏폼
- VIDEO natural-language input
- VIDEO reference upload
- VIDEO Preview
- Timeline
- VIDEO Save
- VIDEO Export
- PHOTO load
- PHOTO natural-language input
- PHOTO reference upload
- PHOTO Preview
- PHOTO Save
- PHOTO Export

No layout correction may break functionality.

## 15. One-change isolation

Confirm:
- VIDEO changes do not shift PHOTO unexpectedly
- PHOTO changes do not alter VIDEO state
- Shortform mode does not distort PHOTO layout
- Save/Export do not collapse panels
- Preview content does not change unrelated panel sizes

## 16. Icon phase remains blocked

DO NOT generate icon candidates in this correction cycle.

Icon phase remains:
PENDING_UI_APPROVAL

Only after representative explicitly says UI OK may the icon phase in v20.2 continue.

## 17. Exact Evidence

Human Review:
docs/commander/MINDLE_MEDIA_AI_FINAL_UI_GEOMETRY_COLOR_CORRECTION_REVIEW_v20.2.1_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_FINAL_UI_GEOMETRY_COLOR_CORRECTION_EVIDENCE_v20_2_1_20261002.json

Detail:
evidence/pc_remote/media-ai-ui-geometry-color-v20_2_1-20261002/

Required files:
1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. CSS_ROOT_CAUSE_ANALYSIS.json
4. APPROVED_REFERENCE_IDENTITY.json
5. BEFORE_MAXIMIZED.png
6. BEFORE_SPLIT.png
7. AFTER_MAXIMIZED.png
8. AFTER_SPLIT.png
9. SIDE_BY_SIDE_AFTER.png
10. PANEL_GEOMETRY_MATRIX.json
11. COLOR_TOKEN_COMPARISON.json
12. VIDEO_CENTER_FILL_AUDIT.json
13. VIDEO_RIGHT_FILL_AUDIT.json
14. PHOTO_CENTER_FILL_AUDIT.json
15. PHOTO_RIGHT_FILL_AUDIT.json
16. SHORTFORM_HEADER_AUDIT.json
17. FUNCTION_ACTIVATION_AUDIT.json
18. ONE_CHANGE_ISOLATION_AUDIT.json
19. REPRESENTATIVE_SCREEN_GATE.json
20. REGRESSION_TEST_RESULTS.txt
21. OUTPUT_HASHES.sha256
22. REMOTE_PUSH_VERIFY.txt

All screenshots must be actual non-zero Windows captures.

## 18. Pass conditions

UI_CORRECTION_READY_FOR_REPRESENTATIVE:
- canonical maximized UI materially matches F27E geometry/density/color hierarchy
- Shortform additive button present
- center areas fill vertical space
- right panels fill vertical space
- PHOTO large empty area eliminated
- responsive split mode remains usable without dead zones
- functional activation PASS
- regression PASS
- live corrected UI left open on Windows

UI_CORRECTION_REQUIRED:
- material mismatch remains
- unexplained blank areas remain
- color hierarchy remains materially different
- function regression exists

REPRESENTATIVE_UI_APPROVED:
Only after representative explicitly approves the corrected live UI.

## Final governing sentence

FIX THE REAL CAUSE, NOT THE SCREENSHOT. REMOVE THE RESPONSIVE GEOMETRY THAT CREATES DEAD SPACE, MAKE VIDEO/PHOTO CENTER AND RIGHT PANELS PROPORTIONALLY FILL THEIR AVAILABLE HEIGHT, RESTORE THE F27E COLOR/DENSITY HIERARCHY, PRESERVE THE SHORTFORM ADDITIVE BUTTON, SHOW BOTH SPLIT AND MAXIMIZED WINDOWS STATES, AND DO NOT ENTER THE ICON PHASE UNTIL THE REPRESENTATIVE APPROVES THE CORRECTED UI.
