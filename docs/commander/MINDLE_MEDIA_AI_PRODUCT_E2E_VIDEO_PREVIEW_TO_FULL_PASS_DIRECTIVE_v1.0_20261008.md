# MINDLE MEDIA AI — PRODUCT E2E VIDEO PREVIEW TO FULL PASS DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — PRODUCT E2E RECOVERY AND FULL PASS
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-PRODUCT-E2E-VIDEO-PREVIEW-TO-FULL-PASS-R1

## 0. COMMANDER VERDICT / STARTING POINT

Do NOT restart already-passed work.

Frozen PASS / reuse from the verified 2026-10-08 retest:
- PHOTO segment real model TESTED_PASS + browser image decode
- PHOTO 4x upscale real model TESTED_PASS + browser image decode
- upscale 480x270 -> 1920x1080
- segment output SHA == upscale input SHA continuity verified
- VIDEO tracking backend TESTED_PASS
- tracking API POST 201 and preview GET 200
- baseline CI: Python 64 PASS / UI 2 PASS
- current approved UI visual/layout preserved
- PR #23 remains HOLD / DO NOT MERGE
- main/prod unchanged

Current failing gate:
FULL PRODUCT E2E FAILS AT VIDEO BROWSER PREVIEW.

Observed tracking preview:
- codec_name=mpeg4
- codec_tag_string=mp4v
- 512x292
- yuv420p
- backend success and exact tracking operation/jobId are present in DOM
- browser media readiness does not complete
- MediaError code was not captured, therefore codec incompatibility is LIKELY but NOT YET PROVEN

## 1. PURPOSE

Close the product runtime E2E in this exact order:

VIDEO browser preview diagnosis/repair
-> VIDEO tracking preview decode
-> Korean STT
-> project Save
-> full close/reopen restoration
-> Export
-> Marketing HTTP
-> approved AVORA asset
-> 광고 숏폼 9:16 Preview
-> approved MP4 export
-> final full-product E2E Evidence and remote readback

The employee Windows distribution package is NOT rebuilt in this cycle.
After full product E2E PASS, the commander may reactivate the one-click employee package cycle.

## 2. UI / SSOT LOCK

This lane is runtime/function recovery, not a visual redesign lane.

Rules:
- Preserve the currently approved MINDLE MEDIA AI layout, colors, action order, and owner-approved VIDEO/PHOTO workspace.
- Do not reintroduce clipping or fixed-height overflow-hidden defects.
- Do not remove 광고 숏폼.
- Do not move or redesign controls merely to make E2E easier.
- UI changes are allowed only when strictly required to expose a runtime state/error without changing approved visual geometry.
- Any unavoidable UI-visible change requires explicit Evidence and commander review.

## 3. VIDEO BROWSER DIAGNOSTIC — FIRST GATE

Before changing codec behavior, capture the actual browser failure.

For the exact tracking preview element record:
- jobId
- operation
- currentSrc
- readyState
- networkState
- videoWidth
- videoHeight
- duration when available
- MediaError.code
- MediaError.message when available
- canPlayType results for the produced MIME/codec candidates
- HTTP status and Content-Type for the preview GET
- first relevant browser console/media error
- ffprobe codec_name / codec_tag_string / pix_fmt / width / height / duration

Write:
docs/evidence/media-ai-product-e2e-full-pass-20261008/VIDEO_BROWSER_DIAGNOSTICS.json

Do not claim codec root cause until these diagnostics are captured.

## 4. H.264 PREVIEW CLOSURE

If the diagnostics confirm or remain consistent with mp4v browser incompatibility, use the EXISTING FFmpeg path to create a browser preview derivative.

Requirements:
- preserve original tracking result, mask, tracking JSON, job Evidence, and hashes
- preview video encoding: H.264
- pixel format: yuv420p
- MP4 faststart enabled
- no GPU requirement
- no paid compute requirement
- no silent fallback to another unverified codec
- record exact ffmpeg command line, ffmpeg version, encoder availability, input/output SHA-256, ffprobe result

The browser must then prove:
- HTTP preview GET 200
- expected tracking jobId and operation match
- videoWidth > 0
- videoHeight > 0
- readyState reaches browser-decodable state
- no MediaError
- actual playback can start
- screenshot/DOM Evidence is stored after decode

Do not solve by merely increasing the 300-second timeout.

## 5. STT — MUST BE REACHED AFTER VIDEO PASS

After tracking preview browser decode passes:
- execute Korean STT through the verified model/runtime
- prove TESTED_PASS
- record input SHA
- record transcript output/hash
- prove the transcript is visible in the approved UI
- preserve VIDEO preview and tracking state

A backend-only STT result is insufficient.

## 6. SAVE / CLOSE / REOPEN

Using the same product session/project:
- save project
- record project ID and project file/hash
- fully close the product/server session as appropriate for this product E2E
- reopen
- restore exact VIDEO, PHOTO, tracking, STT, and processed PHOTO state
- verify job IDs / artifact hashes or immutable references match the saved project

Do not substitute a source-tree unit test for this gate.

## 7. EXPORT

Perform actual product Export after reopen.

Evidence must include:
- exported file name/path
- byte size
- SHA-256
- ZIP/MP4 structure check as applicable
- CRC/integrity where applicable
- expected project/media outputs present

## 8. MARKETING / AVORA / SHORTFORM INTEGRATION

After base product E2E passes, verify the existing Shortform Addendum integration.

Required:
1. actual Marketing AI HTTP call using the approved SHORTFORM BRIDGE Contract
2. approved AVORA asset/reference ingestion
3. request/response status and identifiers
4. 9:16 shortform scene/timeline transformation
5. actual browser Preview
6. Representative Approval gate behavior
7. actual approved MP4 export
8. exported MP4 ffprobe + SHA-256
9. no automatic publishing or ad-spend execution

If an external endpoint, credential, or approved AVORA asset is genuinely unavailable, stop with:
BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION
and record the exact missing dependency.
Do not convert a mock/stub response into PASS.

## 9. TEST / REGRESSION REQUIREMENTS

At minimum:
- existing Python baseline: 64 PASS or greater
- existing UI baseline: 2 PASS or greater
- targeted regression for browser diagnostics
- targeted regression that import cannot pass as segment
- targeted regression that explicit backend/UI failure exits promptly
- PHOTO segment regression
- PHOTO 4x regression
- VIDEO tracking backend regression
- H.264 browser preview regression
- STT regression
- Save/Reopen regression
- Export regression
- Shortform integration regression when external dependencies are available

Any dependency version conflict shown by pip/CI must be explicitly resolved or documented as a blocker; do not ignore resolver warnings that contradict project requirements.

## 10. REQUIRED EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_PRODUCT_E2E_VIDEO_PREVIEW_TO_FULL_PASS_REVIEW_v1.0_20261008.md

Machine Evidence:
docs/evidence/media-ai-product-e2e-full-pass-20261008/EVIDENCE.json

Evidence root:
docs/evidence/media-ai-product-e2e-full-pass-20261008/

Required files:
- VIDEO_BROWSER_DIAGNOSTICS.json
- VIDEO_TRACKING_ARTIFACTS_MANIFEST.json
- H264_PREVIEW_PROBE.json
- VIDEO_BROWSER_DECODE_RESULT.json
- KOREAN_STT_RESULT.json
- SAVE_REOPEN_RESULT.json
- EXPORT_RESULT.json
- SHORTFORM_INTEGRATION_RESULT.json
- BASELINE_CI_PASS.log
- PRODUCT_E2E_RUN_RECEIPT.json
- REMOTE_READBACK.txt

Retain the existing targeted evidence under:
docs/evidence/media-ai-product-e2e-timeout-20261008/

Do not overwrite or delete historical Evidence.

## 11. PASS / FAIL VOCABULARY

Only when base product E2E AND Shortform integration all pass:
PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED

If VIDEO backend passes but browser decode fails:
FAIL_VIDEO_BROWSER_PREVIEW

If VIDEO passes but STT fails:
FAIL_KOREAN_STT_UI_E2E

If Save/Reopen fails:
FAIL_SAVE_REOPEN_E2E

If Export fails:
FAIL_EXPORT_E2E

If external Shortform dependencies are genuinely unavailable:
BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION

If Marketing/AVORA/Shortform is not actually tested:
FULL_PRODUCT_E2E_PASS_FORBIDDEN

## 12. REPOSITORY / MERGE RULES

- canonical branch only
- no force push
- no new repo
- no new worktree
- no main/default merge
- PR #23 remains HOLD / DO NOT MERGE
- do not use PR #23 as the current merge route
- no Production deploy
- no historical Evidence deletion
- no Evidence-less PASS

## FINAL COMMAND

START FROM THE VERIFIED PHOTO PASS / VIDEO PREVIEW FAIL CHECKPOINT.

DO NOT REBUILD PASSED PHOTO WORK.
DO NOT EXPAND TIMEOUT AS THE FIX.
CAPTURE THE REAL BROWSER MEDIA ERROR FIRST.
CLOSE VIDEO H.264 BROWSER DECODE.
THEN RUN STT -> SAVE/REOPEN -> EXPORT.
THEN VERIFY REAL MARKETING HTTP -> APPROVED AVORA ASSET -> SHORTFORM PREVIEW -> APPROVED MP4.
PUBLISH THE REQUIRED REVIEW/EVIDENCE AND REMOTE READBACK.
