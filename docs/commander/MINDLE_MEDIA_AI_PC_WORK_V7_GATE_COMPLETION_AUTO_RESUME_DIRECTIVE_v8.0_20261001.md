# MINDLE MEDIA AI — PC WORK V7 GATE COMPLETION CHECK & AUTO-RESUME DIRECTIVE v8.0
Date: 2026-10-01
Status: EXECUTE NOW
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## Permanent cycle
Inherit docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md.
Every cycle: execute -> verify -> MD+JSON+Manifest -> commit/push -> remote verify -> next directive commit/push -> continue.

## Commander verification
Latest remote evidence remains v7:
- evidence commit 1d00b40b76d38cfe955b787b3e630357f2caae7f
- metadata finalization 363b2ce12d3c3d33a417879cb2372c7fb91c4ae4
No newer remote execution evidence was visible at commander inspection time.

## 1. First action: detect whether human download gate already changed
Inspect Windows Downloads/staging NOW for Artifact ID 10797756522 / v29 part-01 candidate.
Do not rely on filename alone.
Accept only:
- bytes 418706393
- SHA-256 8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128

If exact file exists, immediately proceed to section 2.
If it does not exist, surface the exact GitHub Actions artifact download control for run 35974551384 and request only the single human download action. Before pausing, save/push v8 gate evidence and the next resume directive.

## 2. Reassemble v29
Use only verified v29 part-00 + exact part-01 + verified v29 part-02.
Reassemble using accepted recipe.
Required package SHA-256:
93da2189fc37bb42cc60e8335131d2e533440a96c7c6c7e2535dea90834c8a4c
Hash must PASS before extraction.

## 3. Extract and verify runtime
Extract to controlled local runtime directory.
Verify SAM 2.1, Intel SISR/OpenVINO, Whisper-small against accepted package manifest/revisions/hashes.
Configure product server to local verified payloads; no direct HF.

## 4. PHOTO closeout
Run real PHOTO segmentation and PHOTO 4x with previously approved traceable fixtures.
Each lane must produce:
completed job -> visible Preview -> persisted project save -> Export -> reopen -> bytes/hash -> visual quality verdict.
Freeze PASS lanes.

## 5. VIDEO/STT
Recover traceable approved prior inputs if materializable and run independently. Do not fabricate.

## 6. Shortform
Keep separate VERIFY_REQUIRED unless approved Marketing Contract v1/assets actually exist.

## 7. Exact v8 evidence paths
Create/push:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_V7_GATE_COMPLETION_AUTO_RESUME_REVIEW_v8.0_20261001.md
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_V7_GATE_COMPLETION_AUTO_RESUME_EVIDENCE_v8_0_20261001.json
evidence/pc_remote/pc-work-v7-gate-auto-resume-v8-20261001/manifest.json

## 8. Mandatory next directive
Regardless of PASS/REWORK/HUMAN_ACTION_REQUIRED, create and push the next directive in the same cycle before stopping.
Do not wait for the user to request it.

## 9. Report
Report exact remote commit SHA, evidence paths, per-lane verdicts, and next-directive path.

## Protection
No mixed generation, fabricated output/approval, UI SSOT changes, direct HF retry, main merge, Production deploy, force push, credential disclosure, destructive cleanup.
