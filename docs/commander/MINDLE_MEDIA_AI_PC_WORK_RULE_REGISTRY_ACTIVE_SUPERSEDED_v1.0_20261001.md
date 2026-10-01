# MINDLE MEDIA AI — PC WORK RULE REGISTRY / ACTIVE vs SUPERSEDED v1.0

Date: 2026-10-01
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING RULE REGISTRY

## 0. Purpose

This registry prevents a PC worker from accidentally executing an old directive, old evidence rule, old auth loop, or historical recovery cycle.

The repository intentionally retains historical documents for audit/evidence. Their physical presence does NOT make them executable.

## 1. Precedence — mandatory

When documents conflict, use this order:

1. CURRENT_PC_WORK_DIRECTIVE.md
2. CURRENT_PC_WORK_STATE.json
3. this Rule Registry
4. current ACTIVE directive
5. current machine-readable Evidence Path Contract
6. current technical-scope directive
7. MASTER handover / immutable SSOT / adopted model manifest
8. REFERENCE_ONLY documents
9. HISTORY_ONLY / SUPERSEDED documents

A lower item can never override a higher item.

## 2. ACTIVE — worker MUST read/use

### Single worker entrypoint
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json

### Governing registry
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json

### Active branch-rebind preflight
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_BRANCH_REBIND_AND_STALE_WORKTREE_RECOVERY_DIRECTIVE_v1.0_20261001.md

### Active execution directive
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_V32_ASSET_RECOVERY_UI_SSOT_AND_REAL_E2E_DIRECTIVE_v14.0_20261001.md

### Active technical scope
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_DIRECTIVE_v13.0_20261001.md

### Active Evidence path contract
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v1.0_20261001.json

### Active commander-worker circulation protocol
- docs/commander/MINDLE_MEDIA_AI_COMMANDER_PC_WORKER_REPOSITORY_CIRCULATION_PROTOCOL_v1.0_20261001.md

### MASTER / SSOT
- docs/commander/MINDLE_MEDIA_AI_MASTER_HANDOVER_SSOT_DEVELOPMENT_HISTORY_v1.0_20261001.md
- docs/01_UI_SSOT_FINAL.md
- ui/ssot_manifest.json
- evidence/model_scout/FINAL_ADOPTED_MODEL_MANIFEST_V13.json
- evidence/model_scout/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_V13.json
- docs/commander/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_REVIEW_v32.0_20260925.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json

## 3. REFERENCE_ONLY — may be read for context, MUST NOT be executed as current work

- docs/commander/MINDLE_MEDIA_AI_NEW_PC_WORKER_BOOTSTRAP_ROUTE_CORRECTION_HANDOFF_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_COMMANDER_ROUTE_CORRECTION_NO_GITHUB_LOGIN_LOOP_DIRECTIVE_v12.1_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FIRST_PRODUCT_RECOVERY_DIRECTIVE_v12.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_MANDATORY_EVIDENCE_SAVE_CONTINUATION_RULE_v1.0_20260930.md

These can explain why the current rules exist, but they are not independent executable cycles.

## 4. SUPERSEDED / HISTORY_ONLY — NEVER execute as current work

The following PC Work chains are closed historical records. They remain for audit only.

### Old UI/service/runtime recovery
- MINDLE_MEDIA_AI_PC_WORK_FINAL_UI_ACTIVATION_SHORTFORM_E2E_DIRECTIVE_v1.0_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_LOCAL_SERVICE_RECOVERY_REAL_UI_EXECUTION_DIRECTIVE_v2.0_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_RUNTIME_INPUT_RECOVERY_REAL_UI_EXECUTION_DIRECTIVE_v3.0_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_RUNTIME_INPUT_RECOVERY_NEXT_DIRECTIVE_v3.1_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_VERIFIED_RUNTIME_ARTIFACT_RECOVERY_PHOTO_CLOSEOUT_DIRECTIVE_v4.0_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_VERIFIED_RUNTIME_ARTIFACT_RECOVERY_NEXT_DIRECTIVE_v4.1_20260930.md

### Old artifact transfer / reassembly path
- MINDLE_MEDIA_AI_PC_WORK_GITHUB_ARTIFACT_TRANSFER_RECOVERY_RUNTIME_REASSEMBLY_DIRECTIVE_v5.0_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_GITHUB_ARTIFACT_TRANSFER_RUNTIME_REASSEMBLY_NEXT_DIRECTIVE_v5.1_20260930.md
- MINDLE_MEDIA_AI_PC_WORK_EXACT_PART01_V29_REASSEMBLY_PHOTO_CLOSEOUT_DIRECTIVE_v6.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_EXACT_PART01_V29_REASSEMBLY_NEXT_DIRECTIVE_v6.1_20261001.md

### Old human-auth/gate chain
- MINDLE_MEDIA_AI_PC_WORK_HUMAN_AUTH_TRANSFER_GATE_RESUME_DIRECTIVE_v7.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_HUMAN_AUTH_TRANSFER_GATE_RESUME_NEXT_DIRECTIVE_v7.1_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_V7_GATE_COMPLETION_AUTO_RESUME_DIRECTIVE_v8.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_V7_GATE_COMPLETION_AUTO_RESUME_NEXT_DIRECTIVE_v8.1_20261001.md

### Old long-run closeout chain
- MINDLE_MEDIA_AI_PC_WORK_LONG_RUN_INTEGRATED_CLOSEOUT_DIRECTIVE_v9.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_LONG_RUN_INTEGRATED_CLOSEOUT_NEXT_DIRECTIVE_v9.1_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_LONG_RUN_FULL_BASE_PRODUCT_CLOSEOUT_DIRECTIVE_v10.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_LONG_RUN_FULL_BASE_PRODUCT_CLOSEOUT_NEXT_DIRECTIVE_v10.1_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_HUMAN_GATE_RESUME_FULL_CLOSEOUT_DIRECTIVE_v11.0_20261001.md
- MINDLE_MEDIA_AI_PC_WORK_HUMAN_GATE_RESUME_FULL_CLOSEOUT_NEXT_DIRECTIVE_v11.1_20261001.md

### Historical reviews/evidence associated with old cycles
Every REVIEW/EVIDENCE file tied to v1-v11 above is HISTORY_ONLY unless explicitly referenced by the current ACTIVE directive for comparison.

## 5. Default rule for unlisted old documents

Any PC Work directive/review/evidence document NOT explicitly listed as ACTIVE or REFERENCE_ONLY above is automatically:

HISTORY_ONLY

The worker must not execute it unless a new ACTIVE directive explicitly references it by exact path.

## 6. Anti-stale-worker bootstrap

Before every work cycle, the worker MUST:

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile/pull to current remote HEAD
4. open CURRENT_PC_WORK_DIRECTIVE.md from the updated working tree
5. open this Rule Registry
6. confirm the active directive path and Evidence paths
7. only then execute

If the worker cannot prove it read the current remote HEAD, the cycle status is:
STALE_CONTEXT_BLOCKED

It must not continue using remembered or cached directive names.

## 7. Evidence naming rule

The worker must never invent an Evidence filename.

Only the exact paths from the ACTIVE directive/contract are permitted.

If the worker creates:
- MINDLE_MEDIA_AI_EVIDENCE_CYCLE_01_20261001.md
- MINDLE_MEDIA_AI_PC_RUNTIME_RESTORE_v16_20261001.json
- or any other unlisted Evidence file

that file is NONCOMPLIANT and does not advance the cycle.

## 8. Commander responsibility

Before issuing work, the commander must:
- update CURRENT_PC_WORK_DIRECTIVE.md
- update CURRENT_PC_WORK_STATE.json
- update this registry if rule status changed
- name exact Evidence output paths
- verify the worker is on current remote HEAD

The representative is not responsible for reconciling rules, versions, or Evidence paths.

## 9. Final governing rule

HISTORICAL DOCUMENTS STAY FOR AUDIT, BUT ONLY ACTIVE DOCUMENTS CAN DRIVE WORK.

SYNC FIRST → READ CURRENT ENTRYPOINT → CHECK RULE REGISTRY → EXECUTE ONLY ACTIVE DIRECTIVE → SAVE TO EXACT ACTIVE PATHS → PUSH → REMOTE VERIFY.


## 10. v13 cycle status update

The v13 cycle is now closed as:
PARTIAL_PASS — repository/branch/evidence recovery only.

The following are no longer active execution directives:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_ENFORCEMENT_NONCOMPLIANCE_CORRECTION_DIRECTIVE_v13.1_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FOUR_LANE_RECOVERY_AND_E2E_DIRECTIVE_v13.0_20261001.md

They are now REFERENCE_ONLY for the v14 recovery lineage.

Current ACTIVE product-recovery directive:
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_V32_ASSET_RECOVERY_UI_SSOT_AND_REAL_E2E_DIRECTIVE_v14.0_20261001.md
