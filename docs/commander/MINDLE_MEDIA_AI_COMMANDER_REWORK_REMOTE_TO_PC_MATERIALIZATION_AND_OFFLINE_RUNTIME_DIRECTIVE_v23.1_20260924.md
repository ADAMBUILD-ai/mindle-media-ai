# MINDLE MEDIA AI — COMMANDER REWORK: REMOTE-TO-PC MATERIALIZATION & OFFLINE RUNTIME v23.1
Date: 2026-09-24
Status: EXECUTE
Base: PR #16 head 18512739c12a1f81ce97229307977278c925aaf4

## Commander review
v22 receives PARTIAL PASS + REWORK.

PASS:
- Work finally reconciled the verified remote baseline correctly.
- Adopted model identities/revisions/hashes are now documented.
- Real restore/install attempts were made.
- No legacy fallback or fabricated PC PASS occurred.
- UI/SSOT and prior evidence were preserved.

REWORK:
- A downloadable prior E2E artifact reference was obtained but Work stopped at “local extraction unavailable”.
- Dependency installation tried only the blocked pip-network route.
- The report still ends before exhausting remote-to-local/offline materialization routes.
Therefore PC local E2E is NOT PASS and work must continue.

## 1. Use the verified remote artifact as a transfer source
Artifact 10636679053 is already verified in v22:
- size 228,710,107 bytes
- SHA-256 aac9492699c28ca9c6e640994cc99d25e5fe5e3e13c42a8326ef48d9cded1fe5

Do not reclassify it as unavailable merely because the current process cannot inject it automatically.
Use the approved GitHub authenticated path to download/materialize the artifact into a permitted project-local staging location.
If Work cannot write directly to the PC filesystem, prepare the artifact in the supported transfer/materialization mechanism and surface the exact one-click/user transfer action. Do not return a generic blocker.

After transfer, verify the ZIP digest before extraction.

## 2. Recover reusable prior inputs/evidence
Inspect the verified E2E artifact contents for the previously approved photo/video/Korean speech inputs and their output evidence.
Where provenance allows reuse, stage them for PC-local reproduction.
Record exact paths/bytes/hashes.
If the artifact contains evidence but not source video, state that precisely and request only the missing video via file picker.

## 3. Restore adopted models
Use the approved Private HF path or a verified cache package produced by an authenticated remote workflow.
Materialize only:
- SAM 2.1
- whisper-small
- Intel SISR 1032
Verify against v22 identities before load.
No rescouting and no legacy fallback.

## 4. Offline dependency route
The failed pip network attempt is not the end.
Search in this order:
1. already-installed executable/module locations outside PATH;
2. project/NAS/cache/download/wheel/package directories already approved;
3. portable/free package already present in the environment;
4. authenticated remote workflow that can package the required free runtime dependency for approved transfer;
5. only then surface a precise manual installer/file-selection action.
Required minimum: OpenVINO CPU and ffmpeg.
Selenium/Chrome/PyArrow only if the selected path needs them.
Record each search/attempt.

## 5. Execute lanes as soon as prerequisites exist
Do not wait for all lanes.

PHOTO:
verified SAM + existing approved photo -> actual CPU segmentation -> Preview -> save -> export.

UPSCALE:
verified Intel SISR + approved photo -> actual CPU 4x -> reopen/dimension/hash -> Preview -> save -> export.

VIDEO:
reuse prior approved input if actually recovered; otherwise file picker -> SAM tracking -> decode/continuity -> Preview -> save -> export.

Korean STT:
reuse recovered approved 16 kHz Korean speech if source audio is present and provenance intact; otherwise picker/record -> whisper-small -> transcript -> Preview -> save/export.

## 6. Quality review
Each lane is PASS only after actual output and practical quality review.
Failed quality => REWORK and rerun.

## 7. Regression
Maintain Python 46+ baseline, UI structure/interaction, server health, evidence/package checks.

## 8. Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_REMOTE_TO_PC_MATERIALIZATION_REVIEW_v23.1_20260924.md
- evidence/pc_remote/MINDLE_MEDIA_AI_REMOTE_TO_PC_MATERIALIZATION_EVIDENCE_v23_1_20260924.json
Include transfer attempts, artifact digest verification, recovered files, dependency search/install attempts, model cache verification, lane outputs, quality, Preview/save/export, regression.

## 9. Verdict discipline
Do not PASS the PC-local lane from remote evidence alone.
Do not stop at “network blocked” or “extraction unavailable” until offline/transfer alternatives above are attempted.
If a human action remains, present exactly the one concrete action required.

## 10. Automatic next directive
Immediately after review, create and commit the next directive under docs/commander with exact path/SHA. Do not wait for the user.

## Protection
UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.
