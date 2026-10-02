# MINDLE MEDIA AI — V32 PROVEN ASSET RECOVERY + UI SSOT RECONCILIATION + REAL E2E DIRECTIVE v14.0

Date: 2026-10-01
Status: ACTIVE — EXECUTE AFTER v13 PARTIAL_PASS
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 0. Commander review of v13

v13 is accepted only as an infrastructure/repository recovery PARTIAL_PASS.

Verified:
- stale local branch preserved
- canonical branch rebind PASS
- exact Evidence path compliance PASS
- all required v13 Evidence files published
- remote push/readback verified
- Python/UI/static validators passed

Not accepted as product closeout:
- PHOTO segmentation BLOCKED
- PHOTO 4x BLOCKED
- VIDEO tracking BLOCKED
- Korean STT BLOCKED
- Save/Export BLOCKED
- UI SSOT hash mismatch unresolved

Therefore this cycle MUST recover the previously proven v32 runtime/assets before any new product redesign or model scouting.

## 1. Mandatory read order

1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_STATE.json
3. docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
4. docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
5. evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json
6. docs/commander/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_REVIEW_v32.0_20260925.md
7. evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json
8. ui/ssot_manifest.json
9. docs/01_UI_SSOT_FINAL.md
10. v13 review/evidence package

Do not execute old v14-v32 directives as current instructions. They are evidence/history only unless explicitly referenced by this directive.

## 2. Governing principle

V32 already proved on Windows local:
- PHOTO segmentation TESTED_PASS
- PHOTO 4x TESTED_PASS
- VIDEO tracking TESTED_PASS
- Korean STT TESTED_PASS
- Project Save PASS
- Export PASS

Therefore current missing assets are a RECOVERY/LINEAGE problem, not proof that the product never worked.

Do not:
- restart model scouting
- silently swap models
- recreate UI
- restart GitHub login loops
- ask the representative for files before completing targeted local recovery
- claim permanent loss without hash-based local search evidence

## 3. Canonical identities to recover

### SAM 2.1 Hiera Base Plus
Revision:
b7320756a13354e7530a63935656d35b2f91a290
Expected SHA-256:
2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780

### Whisper-small
Revision:
973afd24965f72e36ca33b3055d56a652f456b4d
Expected SHA-256:
1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b

### Intel SISR 1032
Revision:
a6946b6d6ce42cbf4278df20275fab199655fc7d
Use exact XML/BIN hashes from:
evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json

### Proven v32 real inputs
PHOTO SHA-256:
8ecec108e674b51d36d5323dc2f99240a55913b87003aeb754307da8553edb6f

VIDEO SHA-256:
4e28622467284da93f7575189c84f0e762b170bb7cf19667ca52929f93dcc238

AUDIO SHA-256:
e6bc095e55046de927d7c937f036f96ebb506570648ad9ae7c6576febfc4746a

### Approved UI SSOT
Path:
ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png

Expected SHA-256:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

Current v13 observed SHA-256:
9AAF05BE17A3B851717A8BCDBEAF9C589812CB02F4807E3E2C9D10E75709AD3D

The mismatch must be explained and reconciled. Do not overwrite blindly.

## 4. Phase A — local lineage recovery before network/auth

Search targeted local locations first.

Mandatory search roots:
- current canonical worktree
- backup/media-ai-stale-pc-work-20261001 worktree/history
- prior MEDIA AI worktrees under the known Codex/Documents path
- prior v32/v30 output/package directories
- repository outputs/ and evidence-related local directories
- user-local Hugging Face cache locations
- Python/package caches relevant to OpenVINO/model runtime
- any previous MEDIA AI verified-runtime staging/cache directories referenced by old evidence/manifests

Use filename + size + SHA-256 verification.

For every candidate:
- record full path
- bytes
- SHA-256
- source/lineage
- MATCH / NO_MATCH

Do not copy a candidate into canonical runtime until hash identity is verified.

## 5. Phase B — stale branch/history inspection

Inspect the preserved backup branch:

backup/media-ai-stale-pc-work-20261001

Do NOT merge it.

Use it only to locate:
- exact model/cache paths
- prior runtime configuration
- prior real input paths
- prior approved UI binary or source
- prior output/package staging paths

If a file is recovered from stale history:
- copy only the exact required artifact
- verify hash after copy
- document provenance

No whole-branch merge/cherry-pick.

## 6. Phase C — UI SSOT hash reconciliation

The current binary hash differs from the manifest/Master approved hash.

Determine:
1. when the current 9AAF... binary entered the worktree
2. whether the exact f27e... approved binary exists in:
   - backup stale branch/worktree
   - local old worktrees
   - previous package/output directories
   - repository history/local object database
3. whether docs/01_UI_SSOT_FINAL.md is stale/internally inconsistent with the current APPROVED_PINNED manifest

Rules:
- manifest/Master approved hash f27e... is the acceptance hash
- do not declare UI PASS on 9AAF...
- do not generate a replacement image
- do not edit the image to force a hash
- restore only an authentic exact f27e... binary if found
- if exact binary is not found after targeted lineage search, status = UI_SSOT_ASSET_RECOVERY_BLOCKED and record exhaustive evidence

If exact f27e... binary is recovered:
- restore to ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png
- re-hash
- run UI structure/interaction tests
- do not alter layout/code beyond necessary binary restoration

## 7. Phase D — runtime dependency recovery

Before installing anything, determine whether previous local runtime already contains:
- OpenVINO
- ffmpeg/ffprobe
- required model runtime packages

If missing and the dependency is a free approved local dependency already required by historical MEDIA AI runtime:
- install/expose only the minimum required dependency
- record version/source/command
- do not enable paid compute
- do not change production
- do not use GPU merely because CUDA is present unless existing approved runtime explicitly requires it; default to prior CPU-proven path

VIDEO validation may use the already-proven OpenCV fallback where applicable.

## 8. Phase E — selective artifact acquisition only after local proof

Only if an exact adopted artifact is not recoverable locally:

1. identify the exact missing artifact
2. prove local targeted search failed
3. use the already-approved frozen source/reference for that artifact if accessible
4. avoid general GitHub/authentication loops
5. do not substitute legacy/unadopted model
6. verify revision/hash/license after acquisition

If access requires a human credential gate that cannot be completed autonomously:
- isolate that single artifact as AUTH_REQUIRED
- continue every other recoverable lane
- do not stop the whole cycle

## 9. Phase F — real v32-equivalent E2E rerun

After exact assets/runtime are recovered, rerun independently:

### Lane A — PHOTO segmentation
- exact SAM identity
- recovered approved/proven input or another already-approved owned input only if v32 input truly cannot be recovered
- real product/API execution
- output hash and dimensions

### Lane B — PHOTO 4x
- exact Intel SISR identity
- OpenVINO CPU path
- real 4x execution
- output dimensions/bytes/hash

### Lane C — VIDEO tracking
- exact SAM identity
- recovered proven/approved MP4
- real tracking
- output MP4 validation
- OpenCV fallback permitted where existing product code supports it

### Lane D — Korean STT
- exact Whisper-small identity
- recovered proven/approved Korean WAV
- real transcription
- sample rate/duration
- transcript + WER/deterministic quality metric
- output hash

One blocked lane must not block others.

## 10. Phase G — Save / Export

After at least one real TESTED_PASS job and product flow permit it:
- create/use current test project
- save
- export
- record project ID
- saved project hash
- export filename/bytes/hash

Goal is to restore the v32-proven Save/Export behavior on the current canonical branch.

## 11. Exact v14 Evidence paths

### Human review
docs/commander/MINDLE_MEDIA_AI_PC_WORK_V32_ASSET_RECOVERY_UI_SSOT_AND_REAL_E2E_REVIEW_v14.0_20261001.md

### Machine Evidence
evidence/pc_remote/MINDLE_MEDIA_AI_PC_WORK_V32_ASSET_RECOVERY_UI_SSOT_AND_REAL_E2E_EVIDENCE_v14_0_20261001.json

### Detailed Evidence directory
evidence/pc_remote/pc-work-v32-asset-recovery-ui-ssot-v14-20261001/

Required files:
1. MANIFEST.json
2. LOCAL_LINEAGE_SEARCH.txt
3. MODEL_ASSET_RECOVERY.json
4. V32_INPUT_RECOVERY.json
5. UI_SSOT_LINEAGE_AND_HASH_RECOVERY.json
6. RUNTIME_DEPENDENCY_RECOVERY.json
7. PHOTO_SEGMENTATION_RUN.json
8. PHOTO_4X_RUN.json
9. VIDEO_TRACKING_RUN.json
10. KOREAN_STT_RUN.json
11. PROJECT_SAVE_EXPORT_RUN.json
12. TEST_RESULTS.txt
13. OUTPUT_HASHES.sha256
14. REMOTE_PUSH_VERIFY.txt

No alternate filenames.

## 12. Acceptance result

TESTED_PASS:
- exact adopted model identities verified
- four lanes real execution PASS
- Save/Export PASS
- UI SSOT exact f27e... hash restored/verified
- exact v14 Evidence remotely published

PARTIAL_PASS:
- all recoverable lanes executed
- every remaining blocker has exact artifact/path/auth proof
- UI lineage fully investigated
- exact v14 Evidence remotely published

FAIL:
- reproducible defect remains after permitted recovery/fix/rerun
- exact failure Evidence remotely published

## 13. Mandatory end-of-cycle response

RESULT:
Repository:
Branch:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
SAM recovery:
Whisper recovery:
Intel SISR recovery:
v32 PHOTO input recovery:
v32 VIDEO input recovery:
v32 AUDIO input recovery:
UI SSOT hash:
PHOTO segmentation:
PHOTO 4x:
VIDEO tracking:
Korean STT:
Save:
Export:
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

DO NOT REDESIGN OR RE-SCOUT WHAT V32 ALREADY PROVED. RECOVER THE EXACT PROVEN ASSETS, RECONCILE THE APPROVED UI HASH, THEN RERUN THE REAL PRODUCT E2E ON THE CANONICAL BRANCH.
