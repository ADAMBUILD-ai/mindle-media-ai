# MINDLE MEDIA AI — COMMANDER QUALITY RECOVERY / DIRECT ACQUISITION FALLBACK v27.1
Date: 2026-09-24
Status: REWORK — EXECUTE TO QUALITY PASS
Base: PR #20 head da444a0735ed50a789b7219ff99fe300f7742774

## Commander verdict
v26.1 made major progress. PASS and freeze:
- artifact local materialization
- exact ZIP size/hash verification
- extraction of 30 files
- real PHOTO/VIDEO/Korean speech recovery
- video local decode PASS
- Korean audio metadata PASS
- UI_SSOT_CHANGED:NO and prior Evidence preservation

REWORK:
- adopted SAM/whisper-small/Intel SISR payloads not restored locally
- OpenVINO missing
- PHOTO recovered overlay quality FAIL
- 4x recovered output quality FAIL (black)
- VIDEO/STT not locally rerun
- Preview/save/export not locally proven

The two quality failures prove that remote execution-success alone is insufficient. Do not preserve bad outputs as release-quality results.

## 1. Restore exact adopted models first
Use v22/v13 verified identities. Attempt in order:
A. approved Private HF frozen cache restore;
B. authenticated remote workflow packages exact verified files for transfer;
C. official upstream direct acquisition of the SAME exact model/revision if licensing/provenance matches the frozen manifest.
After acquisition, verify exact bytes/hash/revision before load.
If exact adopted payload cannot be restored after A/B/C, then and only then open a replacement-model track under the same perpetual-use license gate.

## 2. Direct shopping fallback — only if exact restore truly fails
Do not wait for MODEL SCOUT.
Work itself must search official Hugging Face/GitHub/vendor distribution for a replacement suited to the failed function.
Candidate must satisfy:
- official source
- pinned exact revision
- actual artifact download
- bytes/hash
- model/weight license evidence
- perpetual-use gate
- CPU-compatible runtime
- actual quality test on the recovered input
Only a replacement that beats the failed output quality may be adopted.
Do not change UI/SSOT; keep adapter boundary.

## 3. PHOTO quality recovery
The existing recovered overlay is REJECTED as quality evidence because the region misses the intended central subject.
Rerun with real SAM 2.1 first.
Check prompt/point/box selection and preprocessing/coordinate transforms before blaming the model.
Generate multiple deterministic candidate masks only when needed and choose by documented subject criterion, not arbitrary appearance.
PASS requires the mask to correspond to the intended subject with practically usable boundaries.
If exact SAM runtime is correct but quality still fails, tune adapter/prompt logic; only after adapter correction fails may a replacement segmentation model be shopped.

## 4. UPSCALE quality recovery
The recovered 1920x1080 black output is REJECTED.
Rerun exact Intel SISR with verified OpenVINO CPU first.
Inspect input normalization, tensor layout, model input/output names, output range, channel order, postprocessing/clipping and image encoding.
PASS requires:
- true expected dimensions
- non-black/non-empty content
- reopen success
- visible detail preservation/improvement without severe artifacts
If exact model/runtime remains unsuitable after adapter correction, directly shop an official CPU-compatible super-resolution replacement under the same license gate.

## 5. OpenVINO and ffmpeg recovery
Do not rely on public pip.
Search/download through approved official or authenticated routes and package for local transfer.
Prefer official Intel/OpenVINO distribution for OpenVINO and an approved trusted ffmpeg distribution/portable package.
Verify package provenance/version/hash where available.
No GPU/paid compute.

## 6. VIDEO local rerun
The recovered source video is valid and locally decodable. No new user video is required.
Once SAM runtime is restored:
run actual tracking locally -> validate continuity/decodability -> Preview -> save -> export.
If ffmpeg CLI is unavailable but OpenCV can complete the existing verified video path safely, use the existing supported path rather than blocking solely on PATH.

## 7. Korean STT local rerun
The recovered 16 kHz / 12.48 s Korean speech is valid. No new user audio is required.
Once whisper-small is restored:
run actual local STT -> compare transcript with expected/reference evidence and listen/inspect obvious errors -> Preview -> save/export.
If exact whisper-small cannot be restored after official direct acquisition attempt, shop an official CPU-compatible Korean STT replacement under the same license gate.

## 8. Product UI integration
For every corrected lane:
actual recovered input -> local CPU runtime -> actual output -> Preview -> project save -> export.
Do not use recovered remote outputs as the new PC-local output.

## 9. Regression
Run Python/UI/server/evidence/package regressions after fixes. Existing UI/SSOT remains locked.

## 10. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_QUALITY_RECOVERY_AND_LOCAL_E2E_REVIEW_v27.1_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_QUALITY_RECOVERY_AND_LOCAL_E2E_EVIDENCE_v27_1_20260924.json
Include every restore/direct-acquisition attempt, model identity/license/hash, adapter fixes, input/output hashes, quality evidence, Preview/save/export and regressions.

## 11. PASS discipline
PASS: artifact/input recovery already proven.
REWORK: every model/runtime/quality lane until actual local quality evidence exists.
Do not call a black image or wrong mask PASS because dimensions or process exit succeeded.

## 12. Stop condition
Do not stop at “model unavailable”, “OpenVINO unavailable”, or “network blocked”.
Attempt exact restore -> authenticated packaging -> official direct acquisition -> adapter correction -> qualified replacement shopping.
Only after all permitted paths fail may a precise human action be requested.

## 13. Automatic next directive
After review, immediately create and commit the next directive. Do not wait for the user.

## Protection
UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, unverified third-party model, or overwrite of prior Evidence.
