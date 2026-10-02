# MINDLE MEDIA AI — PC WORK RULE REGISTRY v1.7

Date: 2026-10-02
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Status: GOVERNING
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.3

## 0. Governing rule

Exactly ONE cycle is executable:

- docs/commander/MINDLE_MEDIA_AI_WINDOWS_DESKTOP_LAUNCHER_CACHE_VIEWPORT_PARITY_CORRECTION_DIRECTIVE_v20.2.3_20261002.md

Evidence contract:

- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.3_20261002.json

Any mismatch:
CONTROL_PLANE_MISMATCH_BLOCKED

## 1. ACTIVE — the only executable set

### Control plane
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_STATE.json
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_RULE_REGISTRY_ACTIVE_SUPERSEDED_v1.0_20261001.json
- scripts/validate_pc_work_control_plane.py

### Execution
- docs/commander/MINDLE_MEDIA_AI_WINDOWS_DESKTOP_LAUNCHER_CACHE_VIEWPORT_PARITY_CORRECTION_DIRECTIVE_v20.2.3_20261002.md
- docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.3_20261002.json

## 2. Frozen UI baseline

v20.2.2 current worker-opened UI is frozen.

Do NOT redesign any UI region in v20.2.3.

The only task is to make the desktop icon launch exactly the same current UI.

## 3. Current defect

WINDOWS_DESKTOP_LAUNCHER_PARITY_DEFECT

Verify:
- shortcut target/arguments/working directory
- URL/query
- server root/HEAD/process
- CSS/JS cache identity
- browser window/viewport/zoom state

## 4. Required repair

Create/verify one repository-owned canonical Windows launcher.
Desktop shortcut must point to that launcher, not an old localhost URL.

Desktop icon launch and worker launch must resolve to:
- same repository
- same branch
- same HEAD
- same port/server identity
- same current UI assets
- fresh cache state
- equivalent maximized viewport

## 5. Icon design phase

BLOCKED_PENDING_UI_AND_LAUNCHER_APPROVAL

Existing desktop icon is only the launcher test.

## 6. Exact Evidence

Review:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_REVIEW_v20.2.3_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_EVIDENCE_v20_2_3_20261002.json

Detail:
evidence/pc_remote/media-ai-launcher-parity-v20_2_3-20261002/

Required files:
20

## Final rule

SYNC → VALIDATE → LAUNCHER FORENSICS → CACHE/VIEWPORT PARITY FIX → DESKTOP ICON REOPEN → REPRESENTATIVE CONFIRMATION.
