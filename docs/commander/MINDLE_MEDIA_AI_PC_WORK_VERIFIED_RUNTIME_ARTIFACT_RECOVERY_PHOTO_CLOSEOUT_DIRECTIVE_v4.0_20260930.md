# MINDLE MEDIA AI — PC WORK VERIFIED RUNTIME ARTIFACT RECOVERY & PHOTO CLOSEOUT DIRECTIVE v4.0
Date: 2026-09-30
Status: EXECUTE — DO NOT REPEAT FAILED NETWORK ROUTE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## Mandatory rule
First read:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

## Commander review of v3 evidence
Remote v3 evidence is accepted. Evidence commit: 46fd8babec9d3deed3c38c514aa8c6db87a043c1.

FREEZE PASS:
- local product server http://127.0.0.1:8765/
- approved UI shell
- project-save fail-closed gate
- shortform entry and explicit 503 VERIFY_REQUIRED
- traceable PHOTO input identities/hashes
- UI_SSOT_CHANGED:NO

DO NOT repeat the blocked direct HF network request that produced WinError 10013.

## 1. Correct the v3.1 weakness: recover from already-proven runtime artifacts first
Before any network/auth attempt, inspect prior successful runtime package/materialization evidence from v28-v32 and the local artifact/cache paths recorded there.
The project previously verified packaged model/runtime assets. Reuse those exact verified artifacts/revisions when present.
Check prior evidence for:
- runtime package artifact IDs/parts and local extraction paths
- SAM 2.1 pinned payload/revision used by the prior PASS
- Intel SISR/OpenVINO or other final adopted perpetual-use 4x payload/revision used by prior PASS
- whisper-small pinned payload for later STT

Do not substitute RealESRGAN/other legacy payload merely because a benchmark input exists. The input fixture and the adopted inference model are different things.

## 2. SAM recovery order
A. Search the actual Windows local project/cache for the exact previously verified SAM payload/revision.
B. Search prior downloaded runtime-package extraction directories recorded in evidence.
C. If absent locally, re-materialize the already-proven GitHub runtime artifact package/parts from the prior successful remote packaging evidence.
D. Verify bytes/hash/revision against prior evidence before loading.
E. Only if A-D genuinely fail may the lane report the exact missing payload and authentication boundary.
Do not retry blocked Hugging Face direct network as the primary route.

## 3. 4x recovery order
The v3 result “perpetual-use alternative cache revision is required” is not enough to stop.
Identify the exact final adopted perpetual-use 4x model/runtime from prior evidence and restore that exact revision from:
A. local cache/extraction,
B. prior runtime package,
C. proven GitHub artifact materialization.
Verify revision/hash before use.
Do not infer the adopted model from the current input fixture filename.

## 4. Execute PHOTO lanes immediately after recovery
Use the already verified inputs:
Segmentation:
model_scout/artifacts/public_architecture_fixtures/01_42756291.jpg
SHA-256 473107c3388f26b2ffe3cc920fb6931f1446c8d59b61f6986fcc24a135821d75

4x input:
model_scout/artifacts/realesrgan_qualcomm/benchmark/01_input_128.png
SHA-256 112d9ed220e4a990bc86efaafef8a2575548c65be39b432a67ac95471a73bcd2

Run through the real product service/UI pipeline.
For each lane require:
actual completed job -> visible result/Preview -> output file -> SHA-256 -> quality check.

## 5. Native chooser
Attempt the approved UI native chooser once using the actual Windows interactive surface.
If automation cannot populate it, leave it surfaced and record HUMAN_FILE_SELECTION_REQUIRED with the exact file path to select.
Do not create a bypass UI.
Do not let chooser automation block backend/runtime recovery and job completion evidence.

## 6. Save/export closeout
For each completed PHOTO job:
- verify Preview
- project save must return persisted state/ID
- Export must create real file
- reopen output
- record bytes/hash and visible quality
If both PHOTO lanes complete, freeze them PASS permanently unless regression later proves breakage.

## 7. VIDEO/STT
Do not fabricate inputs.
However, before saying inputs are unavailable, inspect prior v15-v32 evidence for exact previously recovered owned video and spoken-Korean WAV paths/hashes and any artifact/materialization route.
If recoverable, materialize and execute independently in this same cycle.
If not recoverable, leave only those lanes VERIFY_REQUIRED with exact missing artifact identity.

## 8. Shortform
Do not spend this cycle on upstream shortform discovery. Keep 503 VERIFY_REQUIRED unless an approved Contract v1/asset handoff is already present.

## 9. Exact v4 evidence paths
Create and PUSH:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_VERIFIED_RUNTIME_ARTIFACT_RECOVERY_PHOTO_CLOSEOUT_REVIEW_v4.0_20260930.md

evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_VERIFIED_RUNTIME_ARTIFACT_RECOVERY_PHOTO_CLOSEOUT_EVIDENCE_v4_0_20260930.json

evidence/pc_remote/pc-work-verified-runtime-photo-v4-20260930/manifest.json

Save screenshot/log/output references inside:
evidence/pc_remote/pc-work-verified-runtime-photo-v4-20260930/

## 10. Mandatory remote closeout
Work is NOT complete at local save.
Commit authorized changes/evidence -> push origin feature/ad-shortform-bridge-p0-20260926 -> verify remote HEAD -> verify all three v4 evidence paths remotely -> create next directive -> commit/push next directive.
Do not ask permission.

## 11. 10-minute route discipline
No single recovery route may consume more than 10 minutes without measurable progress. Switch route according to the ordered recovery paths above.

## 12. Final reporting
Report per lane:
PASS / REWORK / VERIFY_REQUIRED
with actual evidence, not generalized blockers.
Include exact final remote commit SHA and next-directive path.

## Protection
No UI SSOT redesign, no fabricated input/output/approval, no new Model Scout, no main merge, no Production deploy, no force push, no credential disclosure, no destructive cleanup.
