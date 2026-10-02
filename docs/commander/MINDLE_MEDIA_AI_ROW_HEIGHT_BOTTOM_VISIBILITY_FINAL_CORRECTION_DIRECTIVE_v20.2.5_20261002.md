# MINDLE MEDIA AI — ROW HEIGHT CONVERGENCE + BOTTOM VISIBILITY FINAL UI CORRECTION DIRECTIVE v20.2.5

Date: 2026-10-02
Status: ACTIVE — FINAL GEOMETRY CORRECTION
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.5

## 0. Representative ruling

The branded icon / launcher work is accepted as the current launcher baseline.

The remaining UI defect is geometry only.

Representative-provided Windows photos show:

### VIDEO
- right panel height appears correct
- left and center content still appears clipped / vertically mismatched
- therefore VIDEO RIGHT is the visual height reference

### PHOTO
- center panel height appears correct
- left and right appear to extend lower than the center
- even at the document scroll bottom, lower content is not fully visible
- therefore PHOTO CENTER is the visual height reference

Status:
ROW_HEIGHT_CONVERGENCE_REQUIRED

## 1. HARD FREEZE

Do NOT change:
- desktop branded icon
- canonical Windows launcher
- favicon
- top bar / sidebar
- color hierarchy
- Shortform button/order
- VIDEO right visual content hierarchy
- PHOTO center visual content hierarchy
- Marketing / MP4 / model/runtime functionality

This cycle changes ONLY vertical row geometry and internal vertical fitting.

## 2. Current CSS root cause

ui/approved_visual.css contains multiple historical generations of:

- row min-height
- row fixed height
- preview min-height
- timeline min-height
- panel min-height
- responsive overrides at <=1400 and <=1100
- v20.2.1 correction overrides
- v20.2.2 left-panel correction overrides

The current effective geometry can still conflict.

Important examples in the current file:

- VIDEO row height about 350px at <=1400
- VIDEO preview min-height about 165px
- VIDEO timeline min-height about 150px
- transport also consumes height

This can force VIDEO center content to exceed the row height.

PHOTO has similar independent panel content sizing, and global panel overflow clipping can hide the excess.

Do NOT add another blind CSS patch over all previous conflicting declarations.

## 3. Mandatory CSS consolidation

Refactor the geometry declarations for these selectors into ONE canonical final section:

- [data-layout="left-center-right"]
- VIDEO row
- PHOTO row
- video-left
- video-center
- video-right
- photo-left
- photo-center
- photo-right
- video preview
- video timeline
- photo preview
- photo transport

Remove / neutralize obsolete conflicting min-height / height rules that fight the final geometry.

Goal:
one unambiguous row-height system.

Do not rewrite unrelated visual styling.

## 4. Runtime measurement before editing

On the actual icon-launched Windows UI at 100% browser zoom, capture via browser JS:

For each of:
- video-left
- video-center
- video-right
- photo-left
- photo-center
- photo-right

Record:
- top
- bottom
- height
- clientHeight
- scrollHeight
- overflowY

Also record:
- window.innerWidth
- window.innerHeight
- document.documentElement.scrollHeight
- window.scrollY
- devicePixelRatio

Evidence:
GEOMETRY_BEFORE.json

## 5. VIDEO reference rule

VIDEO RIGHT is the reference height.

After correction:

video-left.top
video-center.top
video-right.top

must match within 2px.

video-left.bottom
video-center.bottom
video-right.bottom

must match within 2px.

All three outer heights must match within 2px.

Do NOT increase the VIDEO row just to fit left/center.

Instead fit left/center internal content into the right-reference row.

## 6. VIDEO center fitting

Use a strict internal layout that cannot overflow the row.

Preferred structure:

video-center:
display:grid
grid-template-rows:
  minmax(0, 46%)
  auto
  minmax(0, 1fr)
height:100%
min-height:0

Children:
1. Preview
2. Transport
3. Timeline

For compact widths:
- Preview min-height must be 0
- Timeline min-height must be 0
- remove obsolete hard min-heights that force overflow
- tracks distribute inside timeline
- no track may push the timeline outside its grid row

Hard gate:

video-center.scrollHeight <= video-center.clientHeight + 2

No required control may be clipped.

## 7. VIDEO left fitting

VIDEO left must match VIDEO right height.

Use:
height:100%
min-height:0
display:flex
flex-direction:column

Asset grid:
- top block
- can shrink moderately

Command card:
- flex:1
- min-height:0
- existing natural-language / reference / chips retained

Hard gate:

video-left.scrollHeight <= video-left.clientHeight + 2

If content does not fit:
- reduce internal gaps/padding moderately
- reduce thumbnail height moderately
- do NOT hide controls
- do NOT shrink typography to unreadable size

## 8. PHOTO reference rule

PHOTO CENTER is the reference height.

After correction:

photo-left.top
photo-center.top
photo-right.top

must match within 2px.

photo-left.bottom
photo-center.bottom
photo-right.bottom

must match within 2px.

All three outer heights must match within 2px.

Do NOT increase PHOTO center to follow oversized left/right panels.

Fit left/right content into the center-reference height.

## 9. PHOTO left fitting

Use:
height:100%
min-height:0
display:flex
flex-direction:column

Asset grid:
flex:0 1 auto

Command card:
flex:1
min-height:0

Preserve:
- natural-language field
- reference image
- chips
- send

Hard gate:

photo-left.scrollHeight <= photo-left.clientHeight + 2

No hidden lower chip/send row.

## 10. PHOTO right fitting

PHOTO right must fit exactly into PHOTO center height.

Use existing groups only:
- tabs
- basic edit tools
- color adjustment
- actions

Fit by:
- removing obsolete min-height constraints
- modestly reducing vertical gaps/margins
- distributing rows with flex/grid

Do not delete tools.

Hard gate:

photo-right.scrollHeight <= photo-right.clientHeight + 2

The reset/apply controls must remain fully visible.

## 11. Page-bottom visibility gate

At document scroll bottom:

window.scrollTo(0, document.documentElement.scrollHeight)

Then measure PHOTO row in viewport coordinates.

Required:

photo-row bottom <= window.innerHeight - 4px
AND
photo-row bottom >= window.innerHeight - 40px

Meaning:
the full PHOTO row bottom must be visible near the viewport bottom when fully scrolled down.

If not:
- inspect body/main/editor bottom margin/padding
- remove any parent clipping
- add a small intentional bottom breathing space if required

Do NOT solve by shrinking the entire UI again.

## 12. Outer row hard constraints

At the representative's current icon-launched viewport:

VIDEO:
use one explicit row height driven by the current responsive breakpoint.

PHOTO:
use one explicit row height driven by the current responsive breakpoint.

Every direct child panel:
height:100%
min-height:0
max-height:100%

No direct child may be taller than the row.

## 13. Overflow policy

Outer panels:
overflow:hidden is allowed ONLY if all required child content fits.

Hard FAIL if:
scrollHeight > clientHeight + 2
and required controls are hidden.

No silent clipping.

No hidden overflow used to make geometry appear aligned.

## 14. Preserve launcher/icon

Do not change:
- scripts/launch_media_ai_windows.ps1
- desktop shortcut
- final branded ICO
- favicon assets

Use the branded desktop icon to launch the corrected UI for all final visual checks.

## 15. Functional regression check

Verify after geometry consolidation:

VIDEO:
- load
- AI auto edit
- 광고 숏폼
- natural-language
- reference image
- Preview
- Timeline
- Save
- Export

PHOTO:
- load
- natural-language
- reference image
- Preview
- AI 보정
- Save
- Export

Geometry changes must not affect behavior.

## 16. Required Windows captures

Capture actual icon-launched Windows screen:

1. BEFORE_VIDEO_ROW.png
2. AFTER_VIDEO_ROW.png
3. BEFORE_PHOTO_ROW_BOTTOM.png
4. AFTER_PHOTO_ROW_BOTTOM.png
5. AFTER_FULL_UI_TOP.png
6. AFTER_FULL_UI_BOTTOM.png

The AFTER_FULL_UI_BOTTOM screenshot must be taken with the page scrolled fully to the bottom.

It must visibly show:
- full PHOTO left bottom
- full PHOTO center bottom
- full PHOTO right bottom
- aligned bottom line
- no clipped controls

## 17. Required numeric Evidence

GEOMETRY_AFTER.json must include for all 6 panels:
- top
- bottom
- height
- clientHeight
- scrollHeight

Plus computed deltas:

video_top_max_delta_px
video_bottom_max_delta_px
video_height_max_delta_px
photo_top_max_delta_px
photo_bottom_max_delta_px
photo_height_max_delta_px

Pass threshold:
<= 2px for each delta.

Also include:
- page_bottom_visible = true
- required_controls_clipped = false

## 18. Exact Evidence paths

Human Review:
docs/commander/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_REVIEW_v20.2.5_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_ROW_HEIGHT_BOTTOM_VISIBILITY_EVIDENCE_v20_2_5_20261002.json

Detail directory:
evidence/pc_remote/media-ai-row-height-v20_2_5-20261002/

Required files:

1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. CSS_CONFLICT_CLEANUP.json
4. GEOMETRY_BEFORE.json
5. GEOMETRY_AFTER.json
6. VIDEO_REFERENCE_RIGHT_AUDIT.json
7. PHOTO_REFERENCE_CENTER_AUDIT.json
8. PANEL_OVERFLOW_AUDIT.json
9. PAGE_BOTTOM_VISIBILITY_AUDIT.json
10. BEFORE_VIDEO_ROW.png
11. AFTER_VIDEO_ROW.png
12. BEFORE_PHOTO_ROW_BOTTOM.png
13. AFTER_PHOTO_ROW_BOTTOM.png
14. AFTER_FULL_UI_TOP.png
15. AFTER_FULL_UI_BOTTOM.png
16. LAUNCHER_ICON_PRESERVATION.json
17. FUNCTION_REGRESSION_AUDIT.json
18. REGRESSION_TEST_RESULTS.txt
19. OUTPUT_HASHES.sha256
20. REMOTE_PUSH_VERIFY.txt

## 19. Result vocabulary

ROW_HEIGHT_READY_FOR_REPRESENTATIVE:
- VIDEO 3 panel top/bottom/height deltas <=2px
- PHOTO 3 panel top/bottom/height deltas <=2px
- VIDEO left/center no clipping
- PHOTO left/right no clipping
- page-bottom PHOTO row fully visible
- current launcher/icon preserved
- functionality preserved
- corrected icon-launched UI left open

ROW_HEIGHT_CORRECTION_REQUIRED:
- any panel delta >2px
- any required control clipped
- page bottom still hides PHOTO lower controls
- current good launcher/icon regresses

## 20. Representative final visual gate

Leave the corrected UI open.

Ask:

"신작가님, 영상 편집은 우측 높이에 좌·중앙이 맞고, 사진 편집은 중앙 높이에 좌·우가 맞아서 스크롤 끝에서도 세 칼럼 하단이 모두 완전히 보입니까?"

Do not close out before representative confirmation.

## Final governing sentence

STOP PATCHING INDIVIDUAL PANELS INDEPENDENTLY. CONSOLIDATE THE HEIGHT RULES. VIDEO RIGHT IS THE HEIGHT REFERENCE FOR ALL THREE VIDEO COLUMNS. PHOTO CENTER IS THE HEIGHT REFERENCE FOR ALL THREE PHOTO COLUMNS. FIT CHILD CONTENT INSIDE THOSE ROWS, PROVE TOP/BOTTOM/HEIGHT PARITY WITH RUNTIME DOM MEASUREMENTS, AND PROVE THE COMPLETE PHOTO ROW IS VISIBLE AT THE PAGE BOTTOM.
