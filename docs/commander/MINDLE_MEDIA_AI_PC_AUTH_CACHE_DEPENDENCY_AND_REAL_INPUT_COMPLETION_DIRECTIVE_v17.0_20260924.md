# MINDLE MEDIA AI — PC AUTH CACHE DEPENDENCY & REAL INPUT COMPLETION DIRECTIVE v17.0
Date: 2026-09-24
Status: EXECUTE
Base: PR #12 head 82ed36a1ebcbdd725c431eabe8a970f7ce2caf99
Verified source: v15 report + evidence + v16 directive

## 1. Commander verdict
v15 is accepted as an honest REWORK / PC_MANUAL_INPUT_REQUIRED result.
Do not repeat readiness review.
The product runtime/server restoration is PASS; blockers are now credential/cache materialization, approved local dependencies, and two owned real inputs.

## 2. Preserve completed work
- v13 FINAL CLOSEOUT Evidence remains immutable.
- v14 UI/UX review remains PASS.
- v15 restored product runtime files and server health PASS remain baseline.
- Python regression 46 PASS and UI structure/interaction PASS must not regress.
- UI_SSOT_CHANGED:NO.

## 3. Immediate execution

### STEP 1 — Secure HF credential path
Use the already approved Hugging Face credential/Secret path. Never paste the token into chat, source, logs, PR, or Evidence.
If the PC-local process cannot access the existing credential, open only the approved secure credential/secret injection UI and request the minimum user action needed.
Do not create a new broad token if the existing scoped token can be reused.

### STEP 2 — Materialize frozen adopted cache
Fetch/materialize the v13 adopted immutable Private HF cache into the PC runtime using the approved credential.
Verify every adopted artifact against the frozen manifest before use:
- SAM 2.1
- whisper-small
- Intel single-image-super-resolution-1032
Record exact revision, filename, bytes and hash.
Any mismatch => fail closed; no legacy fallback.

### STEP 3 — Approved local dependencies
Install/expose only free/local dependencies required for the existing runtime:
- OpenVINO CPU
- ffmpeg
- Selenium + compatible Chrome/Chromedriver only if required for actual UI automation
- PyArrow only if required by the selected approved input path
Pin/version-record each dependency.
Do not use GPU or paid compute.
After installation, rerun health/preflight.

### STEP 4 — Search owned inputs before asking user
Search the MEDIA project/work folders, assets, demo, evidence, tests, prior approved artifacts and other explicitly approved local project folders for:
- one real moving-subject video
- one real spoken-Korean audio recording
Do not use silent audio as STT evidence.
Do not use unrelated/private material without approval.
Record every searched location and result.

### STEP 5 — Minimal manual input gate
Only if STEP 4 finds no valid owned input, stop only the affected lane and present one precise request:
- VIDEO: one owned/approved video file
- KOREAN_AUDIO: one owned/approved spoken-Korean audio file
Continue PHOTO and 4x UPSCALE while waiting.
Never stop the whole workflow for two missing inputs.

### STEP 6 — PHOTO lane
With verified SAM cache and existing architecture photo:
UI upload -> SAM CPU segmentation -> output validation -> Preview -> save -> export.
Record input/output bytes/SHA/runtime/model identity and visual usability.

### STEP 7 — 4x UPSCALE lane
With verified Intel SISR cache and approved photo:
UI upload -> Intel CPU inference -> 4x output -> reopen/dimension/hash validation -> Preview -> save -> export.
Record quality/artifact notes.

### STEP 8 — VIDEO lane
When approved video exists:
UI upload -> SAM tracking -> output video -> decode/continuity validation -> Preview -> save -> export.
Record ffmpeg/runtime/model/input/output evidence.

### STEP 9 — Korean STT lane
When approved spoken Korean exists:
UI upload -> whisper-small CPU STT -> transcript -> Preview -> save/export evidence.
Record transcript, obvious error notes, hashes and runtime.

### STEP 10 — Full local product E2E
After four lanes pass, verify Preview/project save/export as an integrated user workflow.
Do not substitute GitHub-hosted E2E for PC-local evidence.

### STEP 11 — Regression and preservation
Run Python/UI/Evidence/package regressions.
Preserve all v13-v15 Evidence.
Commit only evidence/minimal permitted fixes to non-main branch.

## 4. Final Gate
PC_LOCAL_FINAL_E2E_PASS requires actual PC-local evidence for:
PHOTO segmentation / VIDEO tracking / 4x upscale / Korean STT / Preview / project save / export / regression.
No lane may be inferred from remote evidence.

## 5. Mandatory evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_LOCAL_REAL_E2E_FINAL_REVIEW_v17.0_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_LOCAL_REAL_E2E_v17_20260924.json
Include credential status without secret value, cache revisions/hashes, dependency versions, searched input locations, input/output hashes, lane verdicts, Preview/save/export, regression, changed files, commit/PR/Actions.

## 6. Automatic next-directive rule
Immediately after verification:
1. verdict PASS/REWORK/BLOCKED from Evidence;
2. create next directive;
3. commit it under docs/commander/;
4. report exact path + commit SHA.
No verification cycle is complete without the next directive committed.

## 7. Protection
No UI redesign; UI_SSOT_CHANGED:NO.
No main merge, Production deploy, force push, GPU, paid compute, or secret exposure.
Do not overwrite adopted models or v13 immutable Evidence.
