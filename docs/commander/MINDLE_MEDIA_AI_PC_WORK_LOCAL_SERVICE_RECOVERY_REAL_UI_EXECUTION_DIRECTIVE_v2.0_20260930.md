# MINDLE MEDIA AI — PC WORK LOCAL SERVICE RECOVERY / REAL UI EXECUTION DIRECTIVE v2.0
Date: 2026-09-30
Status: REWORK — EXECUTE, VERIFY, SAVE EVIDENCE, CONTINUE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23
Base review head: 4f80c24974f46f470896d86bd7a1b049df6e92a0

## Commander review
PASS/FROZEN:
- Approved UI shell/hierarchy
- Korean natural-language instruction entry
- approved 광고 숏폼 entry
- UI_SSOT_CHANGED:NO

REWORK:
- native chooser/import
- PHOTO segmentation
- PHOTO 4x
- VIDEO tracking
- Korean STT
- Preview
- project save
- export

SHORTFORM remains VERIFY_REQUIRED until an approved Contract v1 + approved asset handoff actually exists. Do not fabricate it.

## 1. Root cause first: static preview is not the product runtime
The previous replay used a Windows browser static UI preview and produced Failed to fetch.
Do not repeat the same static-file replay and call it a new attempt.
Find and launch the repository's actual local product service using the documented/canonical startup path and existing project environment.
Verify:
- bound host/port
- health endpoint or equivalent product response
- browser UI is served from/reaches that local service
- API base URL used by the UI matches the running service
- no stale static preview/file:// origin is being used

If the expected port is occupied, identify the owning process and either reuse the correct existing service or launch on the documented alternate port and update only runtime configuration, not UI SSOT.

## 2. Diagnose Failed to fetch with evidence
Capture browser/network or equivalent request evidence:
- request URL
- method
- status/error
- origin
- service-side log
Fix the actual integration cause: service not running, wrong API base, CORS/origin, stale config, or route mismatch.
Do not hide the error with a fake success state.

## 3. Native file chooser
After the real product service is reachable, click the existing 영상/사진 불러오기 controls.
Use actual approved local test media already present in the project/evidence workspace where possible.
If browser automation cannot inject the native chooser, surface the chooser and require only the one human file-selection action; then continue automatically.
Do not redesign the UI or add a bypass button.

## 4. Execute real UI lanes
Through the actual approved UI, not backend-only calls:
- PHOTO segmentation
- PHOTO 4x upscale
- VIDEO tracking
- Korean STT
For each lane record real input identity/hash, UI action, backend job/result, visible Preview/result and output hash/path.
Reuse already-verified model/runtime assets; do not rescout/repackage unless regression proves corruption.

## 5. Preview / Save / Export
After actual results exist:
- verify Preview is rendered/playable
- click 프로젝트 저장 and verify persisted project state/ID
- click 내보내기 and verify actual exported file
For video/export verify decode/playback, bytes/hash and Preview-vs-export consistency.

## 6. Shortform
If Marketing AI-approved SHORTFORM BRIDGE Contract v1 and approved advertising assets become available during this cycle, continue through the already-defined shortform E2E.
If not, keep SHORTFORM_LIVE_E2E=VERIFY_REQUIRED without blocking MEDIA_AI_PC_UI_FINAL.

## 7. 10-minute rule
Do not passively wait on one route for more than 10 minutes without measurable progress.
Capture blocker evidence, switch to the next permitted recovery route, and continue.
Do not stop after merely identifying Failed to fetch.

## 8. Mandatory evidence-save cycle
EVERY PC Work execution cycle must end by committing fresh evidence to GitHub, whether PASS, REWORK, BLOCKED or VERIFY_REQUIRED.
Mandatory outputs:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_LOCAL_SERVICE_REAL_UI_REVIEW_v2.0_20260930.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_LOCAL_SERVICE_REAL_UI_EVIDENCE_v2_0_20260930.json
Include actual Windows service/process/port evidence, request diagnostics, UI actions, lane results, screenshots/paths/hashes, Preview/save/export, regressions and exact remaining blocker.

Evidence is not optional. Work must not end, timeout, hand off, or claim completion without committing the current cycle's evidence.

## 9. Automatic commander continuation packet
At the end of the cycle, also create the next executable directive under docs/commander based strictly on the new evidence.
Successful lanes are frozen PASS; only failed/incomplete lanes are carried forward.
Report exact Evidence paths + next-directive path + commit SHA.

## 10. Completion
MEDIA_AI_PC_UI_FINAL:PASS only after actual local product service + real UI execution + Preview + save + export pass.
SHORTFORM_LIVE_E2E remains a separate gate.

## Protection
No UI redesign, independent shortform app, fabricated success/approval/asset, hard-coded single-product dependency, main merge, Production deploy, force push, GPU/paid compute without approval, credential exposure, or prior Evidence overwrite.
