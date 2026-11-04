# MINDLE MEDIA AI — PC WORK GITHUB ARTIFACT TRANSFER RECOVERY & RUNTIME REASSEMBLY DIRECTIVE v5.0
Date: 2026-09-30
Status: EXECUTE IMMEDIATELY — CONTINUE UNTIL NEXT EVIDENCE COMMIT
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
PR: #23

## 0. Mandatory operating cycle
Read and obey:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md

From this directive onward, do NOT wait for a separate commander prompt after evidence is produced.
Every cycle is:
EXECUTE -> VERIFY -> SAVE MD+JSON+MANIFEST -> COMMIT -> PUSH -> REMOTE VERIFY -> CREATE NEXT DIRECTIVE -> COMMIT/PUSH NEXT DIRECTIVE -> CONTINUE.
Repeat automatically until the current PC closeout gates are PASS or a genuine external/human-only gate is reached.

## 1. Accepted v4 evidence
Accepted remote evidence commit:
b75be81fdbe32c4d335e27a8b1198ad5db288bb8

Freeze:
- local product server and approved UI shell
- UI SSOT unchanged
- exact adopted model identities/revisions/hashes
- direct HF network is not the recovery route
- shortform missing-contract 503 fail-closed behavior

Current technical blocker:
browser download of runtime artifact part-00 stalled as a 15,380-byte .crdownload.

## 2. Do NOT repeat browser download as primary route
Use a programmatic/authenticated GitHub artifact transfer route on the Windows PC.
Preferred order:
A. Existing authenticated GitHub CLI/session on PC: use gh run / gh api artifact download for run 36089930051 or the exact artifact IDs.
B. Existing authorized repository credential/session through a non-browser GitHub API download route.
C. If A/B unavailable, use the repository's already-proven artifact transfer mechanism/scripts from prior v28-v30 evidence.
D. Browser download is last fallback only.

Never print/store credentials in evidence.

## 3. Recover ALL runtime package parts
From the prior successful runtime package evidence, enumerate the exact three artifact IDs/part names/digests for the same package generation.
Download all three parts into one staging directory.
For each:
- record artifact ID/name
- expected bytes/digest
- actual bytes
- actual SHA-256/digest
- PASS/FAIL
A partial .crdownload is never accepted.

If any part fails, retry only that part using the next permitted transfer route.

## 4. Reassemble and verify
Follow the original package manifest/order exactly.
Reassemble to the recorded package target.
Verify the reassembled package SHA-256 against the prior accepted target:
f80ca743a482f4ad3636f5ed73ba66a32d1d43e649a882154d980334b9965ea2
Do not extract if this hash fails.

## 5. Extract and verify adopted payloads
After package hash PASS, extract to a project-controlled runtime directory.
Verify exact identities:
- SAM 2.1 revision b7320756a13354e7530a63935656d35b2f91a290; model SHA-256 2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780
- Whisper-small revision 973afd24965f72e36ca33b3055d56a652f456b4d; model SHA-256 1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b
- Intel SISR 1032 revision a6946b6d6ce42cbf4278df20275fab199655fc7d; verify XML/BIN hashes from accepted v28 evidence
- packaged Windows OpenVINO runtime manifest/wheel identity
No legacy substitution.

## 6. Runtime load
Configure the local product runtime to load these verified local payloads without direct HF network access.
Verify each model/runtime loads.
Do not expose tokens.
Do not use GPU/paid compute unless separately authorized.

## 7. Execute PHOTO lanes
Immediately rerun:
A. PHOTO segmentation with the already-verified approved architecture photo.
B. PHOTO 4x with the already-verified input.

Require actual completed job, visible Preview, output path/hash and visual quality PASS.

## 8. Save/export
For completed PHOTO jobs:
Preview -> project save -> Export -> reopen -> bytes/hash -> quality check.
Freeze successful lanes PASS.

## 9. VIDEO/STT
Once SAM/Whisper payloads are restored, recover the exact previously evidenced video/Korean spoken-audio inputs from prior v15-v32 materialization records if possible.
Run each independently.
Do not fabricate missing input.
If a human-only file selection is genuinely necessary, surface the native chooser and state the exact traceable file to select, then continue after selection.

## 10. Shortform
Keep separate. If no approved Marketing Contract v1/assets are present, SHORTFORM_LIVE_E2E remains VERIFY_REQUIRED and does not block base MEDIA AI closeout.

## 11. Exact v5 evidence paths
Create and PUSH:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_GITHUB_ARTIFACT_TRANSFER_RUNTIME_REASSEMBLY_REVIEW_v5.0_20260930.md

evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_GITHUB_ARTIFACT_TRANSFER_RUNTIME_REASSEMBLY_EVIDENCE_v5_0_20260930.json

evidence/pc_remote/pc-work-artifact-transfer-runtime-v5-20260930/manifest.json

Store transfer logs/hash manifests/output references under:
evidence/pc_remote/pc-work-artifact-transfer-runtime-v5-20260930/

## 12. Automatic next directive — REQUIRED
After v5 evidence is pushed and remotely verified, Work MUST immediately create the next directive under docs/commander, commit/push it, and continue executing it without waiting for the user or commander to say “next”.
Successful lanes are frozen; only remaining lanes continue.
The automatic chain stops only at:
- MEDIA_AI_PC_UI_FINAL:PASS with required evidence, or
- a true human/external approval/input gate that cannot be performed by Work.

## 13. Time rule
Maximum 10 minutes without measurable progress on one transfer/recovery route. Then switch to the next ordered route.

## Protection
No UI redesign/SSOT change, no fabricated asset/output/approval, no Model Scout restart, no main merge, no Production deploy, no force push, no credential disclosure, no destructive cleanup.
