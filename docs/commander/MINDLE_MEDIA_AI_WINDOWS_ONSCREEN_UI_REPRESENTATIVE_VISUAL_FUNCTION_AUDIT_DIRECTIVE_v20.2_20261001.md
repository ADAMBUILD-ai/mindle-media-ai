# MINDLE MEDIA AI — WINDOWS ON-SCREEN UI REPRESENTATIVE VISUAL + FUNCTION ACTIVATION AUDIT DIRECTIVE v20.2

Date: 2026-10-01
Status: NEXT_PENDING — ACTIVATE ONLY AFTER v20.1 CLOSEOUT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Planned Epoch: MEDIA-AI-20261001-V20.2

## 0. Purpose

Before any final MEDIA AI closeout, the representative must personally see the actual running Windows UI.

This is NOT a screenshot-only audit.
This is NOT a code-only audit.
This is NOT an automated visual PASS.

The Windows worker must physically open the canonical live MEDIA AI UI on the representative's Windows screen and leave it visible for direct inspection.

Final closeout is forbidden until the representative has seen:
1. the originally approved fixed UI reference
2. the current live UI
3. the current live controls responding on screen

## 1. Activation timing

This directive is NEXT_PENDING.

Do not execute it while v20.1 is still ACTIVE.

Activate v20.2 only after:
- v20.1 Review/Evidence is published and commander-reviewed
- v20.1 result is recorded
- control plane is advanced to MEDIA-AI-20261001-V20.2

When activated, the control-plane validator must be updated to v20.2 before execution.

## 2. Final fixed UI authority — BASE + ADDITIVE SHORTFORM

IMPORTANT CORRECTION:

The F27E PNG alone is NOT the complete final fixed UI because it predates the approved 광고 숏폼 additive change.

The final fixed UI is defined by TWO authoritative layers together:

### A. Base visual/layout authority
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Expected SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

This fixes:
- overall dark navy visual identity
- upper VIDEO / lower PHOTO structure
- left / center / right panel geometry
- Preview / Timeline / editing panel placement
- typography / spacing / accent hierarchy
- natural-language command panel placement
- Save / Export visual family

### B. Final additive Shortform authority
docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md

This later approved addendum modifies the VIDEO action row ONLY by adding:
광고 숏폼

Required final VIDEO action order:
영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

Therefore:
- the uploaded/F27E baseline without 광고 숏폼 is NOT the final complete UI
- final comparison must evaluate the F27E visual/layout baseline PLUS the Shortform Addendum
- a live UI identical to F27E but missing 광고 숏폼 is NONCOMPLIANT

Do NOT:
- redesign the base F27E structure
- omit 광고 숏폼
- replace AI 자동 편집 with 광고 숏폼
- merge the two controls
- generate a lookalike
- treat automated PASS as representative visual approval

## 3. Representative on-screen visual gate — MANDATORY

The Windows worker must:

1. launch the canonical MEDIA AI product server from the current canonical worktree
2. open the live UI in the Windows foreground browser
3. open the exact approved F27E UI source in a second visible window/tab
4. arrange the approved reference and live UI so the representative can compare them visually
5. preferably use side-by-side Windows snap layout:
   - LEFT: approved F27E source
   - RIGHT: live MEDIA AI
6. maximize readability; do not show tiny thumbnails
7. after side-by-side review, bring the live MEDIA AI to the foreground at full usable size
8. leave the browser/app OPEN on the Windows screen

The worker must NOT close the live UI after Evidence publication.

End state of this cycle must be:

UI_ON_SCREEN_AWAITING_REPRESENTATIVE

unless the representative has already explicitly approved or identified corrections during the same session.

## 4. What the representative must be able to see

The live UI must visibly show:

### Global
- MINDLE MEDIA AI identity
- dark navy / near-black editor theme
- cyan / blue / violet accent hierarchy
- no white/basic-browser fallback UI

### VIDEO — upper area
- 영상 편집
- 영상 불러오기
- AI 자동 편집
- 광고 숏폼
- 프로젝트 저장
- 내보내기
- left media/library area
- natural-language VIDEO command input
- reference upload
- central VIDEO Preview
- VIDEO Timeline
- right editing controls

### PHOTO — lower area
- 사진 편집
- 사진 불러오기
- Project Save / 저장
- Export / 내보내기
- left media/library area
- natural-language PHOTO command input
- reference upload
- central PHOTO Preview
- right editing controls

Required visible order in VIDEO header:
영상 불러오기
→ AI 자동 편집
→ 광고 숏폼
→ 프로젝트 저장
→ 내보내기

## 5. Final fixed UI comparison checklist — F27E BASE + SHORTFORM ADDENDUM

Compare the live UI against the exact F27E reference for:

- overall dark navy identity
- upper VIDEO / lower PHOTO hierarchy
- left / center / right panel organization
- VIDEO Preview placement
- VIDEO Timeline placement
- right control panel placement
- PHOTO Preview placement
- natural-language panels
- reference upload controls
- Save / Export placement
- visual density
- panel proportions
- margins / spacing / alignment
- typography hierarchy
- neon accent hierarchy
- borders / cards / separators
- Shortform additive button placement
- AI 자동 편집 remains present as a separate control
- 광고 숏폼 is present as a separate control
- 광고 숏폼 appears between AI 자동 편집 and 프로젝트 저장
- exactly one 광고 숏폼 entry exists

Classify each:

MATCH
ACCEPTABLE_RUNTIME_VARIANCE
MISMATCH
MISSING

Do NOT automatically convert MISMATCH into PASS.

## 6. Representative decision gate

The worker may perform automated comparison and functional checks, but ONLY the representative decides whether the live UI is the UI that was originally fixed/approved.

Required final human-facing question shown while UI is still open:

"신작가님, 지금 오른쪽 실제 실행 UI가 왼쪽의 F27E 기본 UI 구조를 유지하면서, 최종 승인된 광고 숏폼 버튼까지 포함한 최종 고정 UI가 맞습니까?"

Allowed representative responses:
- APPROVED_AS_FIXED_UI
- CORRECTION_REQUIRED

If no representative response is available during the worker session:

status =
REPRESENTATIVE_VISUAL_REVIEW_REQUIRED

Do not mark final UI release approval.

## 7. Functional activation audit — real live controls

After the initial side-by-side visual inspection is prepared, verify that visible controls are not decorative only.

### VIDEO controls

Test:
- 영상 불러오기 button responds
- VIDEO file input can receive an approved local test file
- AI 자동 편집 button is clickable and distinct
- 광고 숏폼 button is clickable and enters shortform mode
- VIDEO natural-language command field accepts text
- VIDEO reference upload control opens/accepts input
- Preview surface updates when a valid output exists
- Timeline is live DOM and reflects current VIDEO/shortform state
- 프로젝트 저장 executes actual save route
- 내보내기 executes actual export route

### PHOTO controls

Test:
- 사진 불러오기 responds
- PHOTO file input accepts an approved test image
- PHOTO natural-language command accepts text
- PHOTO reference upload responds
- Preview is live
- segmentation/upscale command routing remains available
- 프로젝트 저장 works
- 내보내기 works

### Shortform controls

If v20.1 completed live MP4:
- 광고 숏폼 mode enters correctly
- live Marketing bridge status is visible/usable
- rendered MP4 appears in Preview
- Timeline reflects shortform scenes
- exported MP4 can be invoked from the UI

If v20.1 remains partially blocked:
- verify UI shortform control activation and error/status presentation
- do NOT fabricate successful MP4 state

## 8. Interaction visibility requirement

The Windows worker must perform the functional checks while the actual app is open.

The representative must be able to see at least:
- button pressed state or resulting message
- command input accepting text
- reference/upload interaction
- Preview area
- Timeline state
- Save result
- Export result/status
- 광고 숏폼 mode state

Automated DOM tests alone are insufficient.

## 9. Do not hide failures

If a visible button:
- does nothing
- opens the wrong function
- is mislabeled
- is disabled unexpectedly
- produces an error
- changes another unrelated part of the UI
- causes layout breakage

record it as a UI_FUNCTION_DEFECT.

Do not immediately redesign.
First capture Evidence and exact reproduction steps.

## 10. One-change isolation check

Because MEDIA AI must behave predictably:

When one UI action is triggered, unrelated UI areas must not unexpectedly change.

Check especially:
- entering 광고 숏폼 does not alter PHOTO layout
- saving does not reset Preview/Timeline unexpectedly
- reference upload does not replace primary input
- VIDEO operation does not alter PHOTO command state
- PHOTO operation does not alter VIDEO command state

## 11. Windows foreground requirement

At the end of automated checks:

- live MEDIA AI browser/app must remain open in foreground
- server process must remain alive
- approved F27E reference must remain easily accessible in adjacent window/tab
- do not minimize everything
- do not close the app
- do not terminate the local server
- do not leave only a text report

The representative should be able to look at the Windows screen immediately.

## 12. Evidence requirements

Human Review:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_UI_REPRESENTATIVE_VISUAL_FUNCTION_REVIEW_v20.2_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_UI_REPRESENTATIVE_VISUAL_FUNCTION_EVIDENCE_v20_2_20261001.json

Detail directory:
evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/

Required files:

1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. LIVE_SOURCE_IDENTITY.json
4. APPROVED_SSOT_IDENTITY.json
5. APPROVED_REFERENCE_VIEW.png
6. LIVE_UI_INITIAL_FULL.png
7. SIDE_BY_SIDE_REFERENCE_VS_LIVE.png
8. VISUAL_COMPLIANCE_MATRIX.json
9. VIDEO_FUNCTION_ACTIVATION.json
10. VIDEO_FUNCTION_SCREEN.png
11. PHOTO_FUNCTION_ACTIVATION.json
12. PHOTO_FUNCTION_SCREEN.png
13. SHORTFORM_FUNCTION_ACTIVATION.json
14. SHORTFORM_FUNCTION_SCREEN.png
15. SAVE_EXPORT_ACTIVATION.json
16. ONE_CHANGE_ISOLATION_AUDIT.json
17. UI_FUNCTION_DEFECT_LIST.json
18. REPRESENTATIVE_SCREEN_GATE.json
19. REGRESSION_TEST_RESULTS.txt
20. REMOTE_PUSH_VERIFY.txt

All screenshot files must be real non-zero screen captures.

## 13. Representative screen gate Evidence

REPRESENTATIVE_SCREEN_GATE.json must include:

- live_ui_left_open_or_foreground: true/false
- approved_reference_open: true/false
- side_by_side_shown: true/false
- live_ui_left_running_after_checks: true/false
- representative_visual_decision:
  APPROVED_AS_FIXED_UI | CORRECTION_REQUIRED | PENDING
- representative_notes: string or null

Do not invent representative approval.

If no approval was explicitly given:
representative_visual_decision = PENDING

## 14. Regression checks

Run:
python scripts/validate_pc_work_control_plane.py

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve:
- F27E SHA
- base runtime PASS
- v18.2 Shortform action identity/order
- any v20.1 verified MP4 work
- model identities

## 15. Completion results

### REPRESENTATIVE_UI_APPROVED
Only if:
- actual Windows UI was displayed
- exact F27E base reference displayed
- Shortform Addendum requirement displayed and verified
- side-by-side comparison completed
- functional activation audit completed
- no blocking UI function defects
- representative explicitly says the live UI matches the fixed approved UI

### REPRESENTATIVE_VISUAL_REVIEW_REQUIRED
Use if:
- automated visual/function audit is complete
- live app remains open on Windows
- representative has not yet given the decision

### UI_CORRECTION_REQUIRED
Use if:
- representative says UI differs from fixed approval
OR
- blocking visual/function defect exists

### FAIL
Use only for inability to launch/capture/operate the canonical UI or Evidence failure.

## 16. Final prohibition

MEDIA AI final closeout MUST NOT occur merely because:
- screenshot tests passed
- CSS tests passed
- F27E hash matches
- worker says MATCH

Representative visual inspection on the real Windows screen is mandatory.

## Final governing sentence

BEFORE FINAL CLOSEOUT, PUT THE REAL MEDIA AI UI ON THE REPRESENTATIVE'S WINDOWS SCREEN, SHOW THE EXACT F27E APPROVED REFERENCE BESIDE IT, EXERCISE THE REAL CONTROLS ON SCREEN, LEAVE THE APP OPEN, AND WAIT FOR THE REPRESENTATIVE'S VISUAL DECISION. AUTOMATED PASS IS NOT A SUBSTITUTE FOR THAT HUMAN VISUAL GATE.


## 17. Conditional app icon phase — execute ONLY after UI OK

This icon phase is conditional.

It MUST NOT begin until the representative explicitly gives:

APPROVED_AS_FIXED_UI

If the representative says CORRECTION_REQUIRED:
- stop icon work
- keep UI open
- record the UI correction request
- do not spend time producing production icon assets for an unapproved UI

Once UI is approved, continue in the same v20.2 cycle.

## 18. Icon design authority

There is currently no separately approved MEDIA AI application icon asset in the repository.

Therefore the worker MUST NOT arbitrarily declare a self-created icon final.

Use only the approved MEDIA AI visual language already visible in the approved UI:

- dark navy / near-black base
- electric blue / cyan accents
- violet / magenta accents
- clean professional B2B editing-product identity
- MINDLE MEDIA AI identity
- no unrelated cartoon mascot
- no stock icon
- no copied third-party logo
- no generic Windows application symbol
- no visual style that conflicts with the approved UI

The icon should communicate MEDIA / PHOTO / VIDEO / AI in a compact professional mark.

Do not alter the approved UI itself while designing the icon.

## 19. Required icon candidate workflow

After UI approval:

1. create exactly THREE icon candidates
2. each candidate must be original to MINDLE MEDIA AI
3. keep the same approved color/world identity
4. render each at 1024×1024
5. create one comparison sheet showing all three candidates
6. show the comparison sheet on the Windows screen
7. leave it visible for representative selection

Candidate Evidence paths:

evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/ICON_CANDIDATE_A_1024.png
evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/ICON_CANDIDATE_B_1024.png
evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/ICON_CANDIDATE_C_1024.png
evidence/pc_remote/media-ai-windows-ui-representative-v20_2-20261001/ICON_CANDIDATE_COMPARISON.png

Do not choose the winner on behalf of the representative.

Required visible question:

"신작가님, UI는 승인된 상태입니다. 지금 보이는 MEDIA AI 아이콘 3안 중 최종 사용할 아이콘을 선택해 주세요."

Allowed icon decision:

ICON_A_APPROVED
ICON_B_APPROVED
ICON_C_APPROVED
ICON_CORRECTION_REQUIRED
PENDING

If no icon decision is available:
RESULT = ICON_REPRESENTATIVE_REVIEW_REQUIRED

## 20. Final icon production after representative selection

Only after one candidate is explicitly selected:

Create final production assets:

ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_1024.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_512.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_256.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_128.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_64.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_48.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_32.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON_16.png
ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico

ICO must contain the normal Windows icon size set, including:
16 / 32 / 48 / 64 / 128 / 256 where supported.

Also apply the approved icon to:
- the browser favicon / local product tab if the current architecture supports it
- the Windows desktop shortcut ONLY if an approved MEDIA AI launcher/shortcut path exists or can be created without inventing a fake executable

Do NOT create a fake EXE merely to display an icon.

If the product remains a local web app:
- use the real local launch command
- create a Windows shortcut only to that real launcher/start path
- assign the final .ico
- prove that clicking the shortcut opens the canonical MEDIA AI UI

## 21. Icon application verification

The Windows worker must visibly show:

1. final icon PNG
2. final ICO
3. icon as favicon/tab icon where applicable
4. Windows shortcut icon where applicable
5. clicking/opening from the shortcut or normal launcher reaches the canonical live MEDIA AI UI

Capture:

ICON_FINAL_ASSET_VERIFY.json
ICON_FINAL_PREVIEW.png
ICON_WINDOWS_APPLICATION_SCREEN.png
ICON_LAUNCH_VERIFY.json

Do not claim icon application PASS from files alone.

## 22. Expanded v20.2 Evidence after UI approval

The original 20 UI files remain required.

After UI approval, add these 10 icon files:

21. ICON_BRAND_SOURCE_AUDIT.json
22. ICON_CANDIDATE_A_1024.png
23. ICON_CANDIDATE_B_1024.png
24. ICON_CANDIDATE_C_1024.png
25. ICON_CANDIDATE_COMPARISON.png
26. ICON_REPRESENTATIVE_DECISION.json
27. ICON_FINAL_ASSET_VERIFY.json
28. ICON_FINAL_PREVIEW.png
29. ICON_WINDOWS_APPLICATION_SCREEN.png
30. ICON_LAUNCH_VERIFY.json

Final icon production assets under ui/assets/brand/ are product outputs and must also be committed after representative selection.

No production icon asset may be committed before representative selection.

## 23. Final result vocabulary — revised

### REPRESENTATIVE_VISUAL_REVIEW_REQUIRED
UI/function audit complete, UI remains open, representative UI decision pending.

### UI_CORRECTION_REQUIRED
Representative rejects the live UI or a blocking UI/function defect exists.
Do not begin icon phase.

### ICON_REPRESENTATIVE_REVIEW_REQUIRED
Representative approved the UI.
Three icon candidates are displayed.
Final icon selection is pending.

### ICON_CORRECTION_REQUIRED
Representative rejects all icon candidates or requests revision.

### REPRESENTATIVE_UI_AND_ICON_APPROVED
Only if:
- representative approved the live UI
- representative selected an icon
- final icon assets were generated from the selected candidate
- icon was applied to actual product surfaces where applicable
- launch/icon verification passed
- UI and app remain consistent with the approved MEDIA AI visual identity
- all required Evidence and product icon assets are remotely readable

## 24. Final closeout prohibition — revised

MEDIA AI final closeout is forbidden until BOTH are complete:

1. REPRESENTATIVE UI APPROVAL
2. REPRESENTATIVE ICON APPROVAL + APPLICATION

Final closeout must not occur after UI approval alone.

## Final governing sentence — revised

SHOW THE REAL UI FIRST. ONLY AFTER THE REPRESENTATIVE SAYS THE UI IS OK, CREATE THREE MEDIA AI ICON CANDIDATES, SHOW THEM ON THE WINDOWS SCREEN, LET THE REPRESENTATIVE SELECT ONE, PACKAGE THAT SELECTED ICON FOR THE REAL PRODUCT, VERIFY IT OPENS/APPEARS CORRECTLY, AND ONLY THEN ALLOW FINAL CLOSEOUT.
