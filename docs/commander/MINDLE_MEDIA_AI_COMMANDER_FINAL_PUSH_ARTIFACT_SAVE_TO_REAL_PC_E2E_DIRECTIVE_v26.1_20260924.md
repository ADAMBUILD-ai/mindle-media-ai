# MINDLE MEDIA AI — COMMANDER FINAL PUSH: ARTIFACT SAVE GATE TO REAL PC E2E v26.1
Date: 2026-09-24
Status: EXECUTE TO SUCCESS
Base: PR #19 head c18ef755d946fb2f33e41a627f04ff21ab8bcbfd

## Commander judgment
v25.1 is PARTIAL PASS / REWORK.
PASS: Work opened the real GitHub artifact page, verified the visible Download control and expected digest, preserved UI/SSOT and prior Evidence.
REWORK: no local save event occurred; ZIP bytes, extraction, runtime restoration and all PC-local lanes remain incomplete.

This cycle must not return another prose-only “save pending” report.

## 1. Drive the user action to completion
Keep/surface the actual artifact Download UI for:
run 35596903385 / artifact 10636679053.
The required human action is only: complete the browser download/save of the ZIP.
After download, immediately locate the downloaded ZIP using approved local download/project folders and file-selection UI.
If the browser saves to Downloads rather than work/v23_1_transfer, accept that location, verify the file, then copy/move it into the approved project staging folder.
Do not require the user to type a path if Work can locate/select the file.

## 2. Verify local bytes immediately
Expected:
size 228,710,107 bytes
SHA-256 aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5
Calculate locally.
Mismatch = REWORK and re-download. Match = PASS and continue automatically.

## 3. Extract and recover everything useful
Extract into a fresh staging directory.
Inventory recursively.
Recover approved source PHOTO, VIDEO, Korean speech, output evidence, manifests and any model/cache payloads.
Record paths, bytes, hashes, provenance.
Do not overwrite immutable prior Evidence.

## 4. Restore exact adopted models
Use recovered payloads or the approved frozen Private HF route guided by the manifest:
SAM 2.1 / whisper-small / Intel SISR 1032.
Verify exact identity before load.
No MODEL SCOUT waiting, no new shopping, no legacy fallback.

## 5. Resolve runtime dependencies aggressively but safely
Do not stop at PATH/import checks.
Search local Downloads, package caches, project tools, Python environments and approved portable locations for ffmpeg/OpenVINO.
If absent, use an approved free offline/portable package route or authenticated transfer route.
If one unavoidable installer click remains, surface that exact action.
No GPU/paid compute.

## 6. Run lanes as prerequisites become ready
PHOTO first; UPSCALE second; do not wait for VIDEO/STT.
Then VIDEO and Korean STT using recovered approved sources. If a source is truly absent, open a file picker for only that source.
Each lane: real input -> real CPU model -> real output -> Preview -> save -> export.

## 7. Quality gate
PHOTO boundary quality.
VIDEO continuity/decodability.
UPSCALE true 4x dimensions and artifact/detail review.
STT actual Korean transcript/error review.
Preview/export consistency.
Poor quality = REWORK, not PASS.

## 8. Regression
Run Python/UI/server/evidence/package regressions after runtime execution.

## 9. Evidence
Create final review + JSON with:
local ZIP path/size/hash; extraction inventory; model identity; dependencies; all input/output hashes; quality; Preview/save/export; regression; remaining blocker if any.

## 10. Success discipline
The objective is PC_LOCAL_FINAL_E2E_PASS.
Do not stop at an intermediate status when another permitted action exists.
A blocker is accepted only after the exact alternative paths above were attempted and evidence is recorded.

## 11. Automatic next directive
After review, immediately create/commit the next directive. Do not wait for user instruction.

## Protection
UI_SSOT_CHANGED:NO. No redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.
