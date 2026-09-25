# MINDLE MEDIA AI — COMMANDER BREAKTHROUGH EXECUTION: AUTHENTICATED PACKAGING / DIRECT SHOPPING / QUALITY FIX v28.1
Date: 2026-09-24
Status: REWORK — DO NOT STOP UNTIL ALL PERMITTED ROUTES EXHAUSTED
Base: PR #21 head 4a267db442934709cdd0ec929ed5240a5c4e6e0d

## Commander verdict
v27.1 is PARTIAL PASS + REWORK.

FREEZE AS PASS:
- local verified artifact ZIP and extraction
- recovered PHOTO/VIDEO/Korean speech inputs
- VIDEO local decode
- Korean audio metadata
- UI/SSOT preservation
- honest rejection of bad PHOTO overlay and black UPSCALE output

REWORK:
- exact adopted model payload restore
- OpenVINO/ffmpeg runtime restore
- PHOTO adapter/quality
- UPSCALE adapter/quality
- local VIDEO tracking
- local Korean STT
- Preview/save/export

Work has now proven that public outbound HTTPS from the PC is blocked. Repeating the same PC download is prohibited.

## 1. Change the acquisition topology
Do not download from Hugging Face directly on the blocked PC again.
Use an environment that already has authenticated outbound access (approved remote workflow / Work cloud environment / existing authenticated project path) to acquire and package the exact required files, then transfer the package to the PC through the GitHub artifact route that is already proven to work.

This is now the PRIMARY path, not an optional suggestion.

## 2. Exact model package — build remotely
Acquire exact pinned official artifacts:
- SAM 2.1 Hiera Base Plus at the frozen verified revision
- whisper-small at the frozen verified revision
- Intel SISR 1032 exact XML/BIN revision
For every file verify source, revision, bytes, hash and license/provenance against the frozen manifest.
Package only verified files plus manifest/checksums into a transfer archive.
Upload as a GitHub Actions artifact or another already-approved authenticated project artifact.
No secret values inside package/evidence.

## 3. Runtime dependency package — build remotely or source officially
Prepare free CPU runtime packages required by the existing adapters:
- OpenVINO CPU runtime compatible with the project
- ffmpeg only if the existing VIDEO path actually needs it; if OpenCV path is sufficient, do not block on ffmpeg
Use official/approved distributions. Record version/source/hash.
Package for PC transfer using the same proven artifact route.

## 4. Transfer and verify on PC
Download the model/runtime package through the proven GitHub artifact UI.
Verify package digest locally before extraction.
Verify every model/runtime file again after extraction.
Only verified exact assets enter the PC runtime cache.

## 5. Fix PHOTO before replacement shopping
Once exact SAM is local:
- reproduce the wrong-mask issue
- inspect image resize/letterbox, coordinate scaling, prompt point/box mapping, mask index selection and overlay transform
- correct adapter logic
- rerun on recovered PHOTO
PASS only when intended subject is segmented with usable boundary.
Do not replace SAM merely because the previous remote overlay was wrong if adapter logic is the cause.

## 6. Fix UPSCALE before replacement shopping
Once exact Intel SISR/OpenVINO is local:
- reproduce black output
- inspect dtype, normalization, NCHW/NHWC, input/output tensor names, output range, channel order, resize path, clipping and PNG encoding
- correct adapter/postprocess
- rerun recovered PHOTO
PASS requires true 4x, non-black output, reopen success and useful detail.

## 7. Direct shopping fallback — mandatory if exact model remains unusable
If an exact adopted model cannot be packaged/restored OR still fails quality after verified adapter correction:
Work itself must directly shop official alternatives. Do NOT wait for MODEL SCOUT.
Use official HF/GitHub/vendor sources from the outbound-capable environment.
For each candidate:
official source -> exact pinned revision -> actual artifact -> bytes/hash -> model/weight license -> perpetual-use evidence -> CPU runtime -> same recovered input -> quality comparison.
Select only an evidence-backed candidate that meets or exceeds the required quality.
Keep UI/SSOT unchanged; replace only adapter/model binding.

## 8. VIDEO
Recovered video is already valid.
As soon as SAM runtime is fixed, execute local tracking using the existing supported decode/encode path.
Do not block solely because ffmpeg is absent if OpenCV safely supports the path.
Validate continuity, output decode, Preview, save, export.

## 9. Korean STT
Recovered real Korean audio is already valid.
As soon as whisper-small is local, execute STT and compare actual transcript quality.
If exact Whisper cannot be restored after remote packaging, direct-shop an official CPU-compatible Korean STT alternative under the same license gate.
Preview/save/export required.

## 10. Parallelize
Run remote exact-model packaging and runtime-dependency packaging in parallel.
In parallel, inspect/fix adapter code paths that caused wrong mask and black upscale using the recovered inputs and manifests.
Do not serialize independent work.

## 11. Evidence
Record:
- remote package acquisition source/revision/hash/license
- package artifact ID/digest
- PC transfer/digest
- adapter code fixes
- before/after output hashes and images
- quality verdict
- VIDEO/STT local results
- Preview/save/export
- regression
- Commit/PR/Actions

## 12. PASS discipline
Artifact/input recovery remains PASS and must not be redone.
Bad overlay and black upscale remain FAIL until corrected.
A successful process exit is not a quality PASS.
Remote evidence is not PC-local execution.

## 13. Stop condition
Do not stop on public-network denial.
Do not stop on missing local cache.
Do not stop on missing ffmpeg if supported OpenCV path exists.
Allowed sequence is:
remote exact packaging -> PC transfer -> adapter correction -> local quality rerun -> direct official replacement shopping if needed.
Only after these routes fail may a precise human action be requested.

## 14. Automatic next directive
After review, immediately create and commit the next directive under docs/commander. Do not wait for user request.

## Protection
UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, secret exposure, unverified third-party model, or overwrite of prior Evidence.
