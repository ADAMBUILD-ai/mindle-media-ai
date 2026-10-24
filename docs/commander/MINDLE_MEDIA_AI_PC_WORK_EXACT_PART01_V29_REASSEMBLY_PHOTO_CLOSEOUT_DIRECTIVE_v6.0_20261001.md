# MINDLE MEDIA AI — PC WORK EXACT PART-01 ACQUISITION / V29 REASSEMBLY / PHOTO CLOSEOUT DIRECTIVE v6.0
Date: 2026-10-01
Status: EXECUTE IMMEDIATELY
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## Mandatory continuous cycle
Inherit:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

Do not wait for another user/commander prompt after this cycle. Execute -> verify -> evidence -> commit/push -> remote verify -> next directive -> continue.

## Commander review of v5
Accepted evidence commit: 5b3251a927d10daa70d9c46845788a6c190283c9.

Freeze PASS:
- v29 part-00 exact local file/hash
- v29 part-02 exact local file/hash
- local product server/UI shell and UI SSOT protection
- shortform fail-closed behavior
- direct HF is excluded

Single runtime package blocker:
EXACT v29 part-01 is missing.
Expected:
- bytes: 418706393
- SHA-256: 8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128

Do not spend time rehashing already-verified v29 part-00/02 except once immediately before reassembly.

## 1. Acquire exact v29 part-01 — ordered routes
Use the prior GitHub Actions run/artifact evidence to identify the exact v29 part-01 artifact ID and artifact name. Do not guess from filenames.

Route A — GitHub API using existing authorized browser/repository session or available connector-safe credential mechanism on PC. Download artifact ZIP directly to a dedicated staging path.
Route B — install/use GitHub CLI only if installation can be completed non-destructively and authentication can reuse an existing authorized session without exposing credentials. Then download the exact artifact by ID.
Route C — GitHub Actions artifact web download with explicit completion monitoring. If browser is used, wait only while bytes are increasing; once complete, rename/move from browser temp to staging.
Route D — if the original artifact has expired/unavailable, rerun/reproduce ONLY the already-approved v29 runtime packaging workflow at the same pinned revisions and package recipe to regenerate the exact required generation. Verify that the regenerated part identities/package target match the accepted manifest before use.

Never use direct Hugging Face as a shortcut. Never accept the current wrong part-01.

## 2. Download completion criteria
The candidate part-01 is accepted only when:
- normal file, not .crdownload
- actual bytes = 418706393
- SHA-256 = 8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128

If mismatch, reject and move to next route. Do not reassemble.

## 3. Reassemble v29 only
Use exactly:
- verified v29 part-00
- newly verified v29 part-01
- verified v29 part-02

Follow the accepted original package order/recipe.
Verify final package target hash from the corresponding v29 evidence BEFORE extraction.
Do not use the v30 target hash for a v29 generation. Read the exact v29 target from prior accepted evidence and record it in v6 Evidence.

## 4. Extract and payload verification
After package target PASS, extract to a controlled runtime directory.
Verify the exact packaged payload identities against the v29 manifest/evidence:
- SAM 2.1
- Intel SISR/OpenVINO 4x runtime
- Whisper-small
Record exact revision/hash and local path.
No legacy substitution.

## 5. PHOTO real closeout
Immediately rerun through actual local product pipeline:
A. PHOTO segmentation using the already-approved architecture fixture.
B. PHOTO 4x using the already-approved 4x fixture.

For each require:
completed job -> visible Preview -> project save persisted ID/state -> Export -> reopen -> bytes/SHA-256 -> visual quality check.
If PASS, freeze lane.

## 6. Native chooser
Use actual Windows UI. If chooser needs one human click/file selection, surface it with the exact approved file path and wait only for that human action. After selection continue automatically.
Do not add bypass UI.

## 7. VIDEO/STT
After runtime extraction, recover traceable prior inputs if available and execute independently. Do not block PHOTO closeout on them and do not fabricate inputs.

## 8. Shortform
Keep VERIFY_REQUIRED unless approved Marketing Contract v1/assets are actually present.

## 9. Exact v6 evidence paths
Create and PUSH:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EXACT_PART01_V29_REASSEMBLY_PHOTO_CLOSEOUT_REVIEW_v6.0_20261001.md

evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_EXACT_PART01_V29_REASSEMBLY_PHOTO_CLOSEOUT_EVIDENCE_v6_0_20261001.json

evidence/pc_remote/pc-work-v29-part01-reassembly-v6-20261001/manifest.json

Put transfer/hash/reassembly/extraction/output references under:
evidence/pc_remote/pc-work-v29-part01-reassembly-v6-20261001/

## 10. Mandatory Git closeout
Local files are not submission.
Commit -> push -> verify remote branch HEAD -> verify Review+JSON+Manifest remotely -> create next directive -> commit/push next directive.
Do not ask permission.

## 11. 10-minute rule
If a route has no measurable progress for 10 minutes, record it and switch to the next route. A growing download is measurable progress and may continue beyond 10 minutes.

## 12. Completion
Do not call MEDIA_AI_PC_UI_FINAL PASS until real jobs + Preview + Save + Export are evidenced.
Shortform remains separate.

## Protection
No UI SSOT changes, no mixed-generation package, no fabricated payload/media/output/approval, no main merge, Production deploy, force push, credential disclosure, destructive cleanup, or new Model Scout cycle.
