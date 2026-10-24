# MINDLE MEDIA AI — PC WORK HUMAN/AUTH TRANSFER GATE RESUME DIRECTIVE v7.0
Date: 2026-10-01
Status: EXECUTE / RESUME AUTOMATICALLY AFTER GATE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## Permanent cycle rule
Inherit:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

This directive exists so the cycle never ends at review. After every review, the next directive must already be committed/pushed.

## Accepted v6 evidence
Accepted evidence commit: 5fe05edc6061cc900af5d42cd9710e0d51b66ea3.
Freeze all v6 verified facts.

## Gate
Required exact GitHub Actions artifact:
- Artifact ID: 10797756522
- v29 part-01
- bytes: 418706393
- SHA-256: 8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128

The existing local part-01 is rejected and must never be used.

## 1. Attempt authenticated transfer first
Use any already-authorized GitHub session available to PC Work without exposing credentials.
If an authenticated transfer action is available, download artifact ID 10797756522 directly to a dedicated staging folder and verify bytes/hash.

## 2. Human gate behavior
If Work cannot perform the authenticated transfer itself, surface the exact GitHub artifact download page/control and request ONLY this single human action:
“Artifact ID 10797756522 v29 part-01 다운로드를 완료해 주세요.”
Do not ask the user to choose filenames, hashes, folders, models, or other technical decisions.

After the download appears in Windows Downloads, Work must resume automatically without needing a new directive or user instruction.

## 3. Automatic file detection
Monitor the Downloads folder for a completed non-.crdownload candidate.
For every candidate verify:
- bytes exactly 418706393
- SHA-256 exactly 8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128
Reject mismatches and keep the exact gate open.

## 4. Reassemble immediately after PASS
Use verified v29 part-00 + exact part-01 + verified v29 part-02 only.
Reassemble with the accepted recipe.
Required v29 package target SHA-256:
93da2189fc37bb42cc60e8335131d2e533440a96c7c6c7e2535dea90834c8a4c
Do not extract unless target hash passes.

## 5. Runtime extraction and verification
Extract and verify packaged SAM 2.1, Intel SISR/OpenVINO, and Whisper-small identities/hashes against accepted evidence.
Configure local runtime to use verified local payloads without direct HF download.

## 6. Product E2E continuation
Run PHOTO segmentation and PHOTO 4x with traceable approved inputs.
Then:
Preview -> project save -> Export -> reopen -> bytes/hash -> visual quality.
Freeze PASS lanes.

Recover/run VIDEO tracking and Korean STT independently if traceable approved inputs are recoverable.

Shortform remains VERIFY_REQUIRED unless approved Contract v1/assets exist.

## 7. Exact v7 evidence paths
Always create/push, including if still at human gate:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_HUMAN_AUTH_TRANSFER_GATE_RESUME_REVIEW_v7.0_20261001.md

evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_HUMAN_AUTH_TRANSFER_GATE_RESUME_EVIDENCE_v7_0_20261001.json

evidence/pc_remote/pc-work-human-auth-transfer-v7-20261001/manifest.json

## 8. Mandatory cycle closeout
At every v7 execution:
save evidence -> commit -> push -> remote verify -> create next directive -> commit/push it.
If human gate remains, next directive must preserve the exact gate and resume instructions.
If gate clears, next directive must carry only remaining failed lanes.

## 9. Stop condition
Do not stop the commander cycle merely because a human action is needed. Save the gate Evidence and next resume directive first.
The technical execution may pause only after those remote artifacts exist.

## Protection
No mixed generations, direct HF retry, fabricated files/results/approval, UI SSOT changes, main merge, Production deploy, force push, credential disclosure, or destructive cleanup.
