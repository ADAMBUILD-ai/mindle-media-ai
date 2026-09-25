# MINDLE MEDIA AI — COMMANDER MANDATORY ARTIFACT RECOVERY & EXECUTION v25.1
Date: 2026-09-24
Status: REWORK — EXECUTE, DO NOT RESTATE
Base: PR #18 head 08ab3439b430c22e18fb149355f5a6f47477e55c

## Commander verdict
v24.1 is REWORK. The Work report is not accepted as completion.
PASS only: UI/SSOT preservation, prior Evidence preservation, exact artifact identity, and honest non-fabrication.
REWORK: artifact local transfer, digest verification, extraction, adopted runtime restoration, dependency restoration, and every PC-local lane.

## 1. Stop repeating the same blocker
Do not produce another report that merely says the ZIP is absent.
The next report must contain either:
A. locally materialized artifact bytes with verified digest and execution progress; or
B. evidence that the exact user-facing Download control/file-save handoff was actually opened and is awaiting the user's one action.
Anything less is REWORK.

## 2. Force the concrete artifact handoff
Target is fixed:
run 35596903385 / artifact 10636679053
size 228,710,107 bytes
SHA-256 aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5

Use the authenticated GitHub Actions artifact route already proven accessible.
Surface/open the actual artifact Download action for the user.
Target local staging folder: work/v23_1_transfer.
If the platform cannot programmatically save the bytes, stop ONLY after the actual download/file-save UI is presented. Do not substitute prose instructions for the actionable UI when the UI can be opened.

## 3. Immediate continuation after ZIP selection
Once the ZIP is present:
- verify exact size and SHA-256 before extraction;
- extract to a new staging directory;
- inventory every source input/output/evidence/model payload;
- record path/bytes/hash/provenance;
- preserve prior Evidence.

## 4. Recover verified assets, not replacements
Use the v13/v22 manifests to restore exact adopted:
SAM 2.1 / whisper-small / Intel SISR 1032.
No new shopping, no MODEL SCOUT wait, no legacy fallback.
If payloads are absent from the ZIP, use the verified manifests and approved authenticated Private HF path to restore them.

## 5. Dependencies — exhaust approved alternatives
For OpenVINO CPU and ffmpeg:
- search installed locations outside PATH;
- search project/cache/download/wheel/portable locations;
- use approved offline/portable package if present;
- use approved authenticated remote packaging/transfer if supported;
- only then request one precise human installer/file action.
Do not repeat a failed public pip network call as the only attempt.

## 6. Execute without waiting
PHOTO and UPSCALE run first as soon as model/runtime prerequisites exist.
Then VIDEO and Korean STT using recovered approved source inputs where available; otherwise open the local picker for only the missing source.
Each lane must reach real output -> Preview -> save -> export.

## 7. Quality and regression
Do not PASS on process exit alone.
Review segmentation boundary, tracking continuity, true 4x dimensions/artifacts, Korean transcript errors, Preview/export consistency.
Run Python/UI/server/evidence/package regressions.

## 8. Evidence required
Create a new review + JSON containing:
- actual artifact handoff state
- local ZIP path/size/hash
- extraction inventory
- model restore identities
- dependency restore attempts/results
- lane input/output hashes and quality
- Preview/save/export
- regression
- exact human action if one remains

## 9. PASS/REWORK discipline
PASS only evidence-backed completed items.
REWORK every uncompleted item.
Never convert remote PASS into PC-local PASS.

## 10. Automatic next directive
Immediately after review, create and commit the next directive. Do not wait for the user.

## Protection
UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or Evidence overwrite.
