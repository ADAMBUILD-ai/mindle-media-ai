# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.3
DATE: 2026-10-02
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## START ORDER

1. git fetch origin
2. checkout feature/ad-shortform-bridge-p0-20260926
3. reconcile to current remote HEAD
4. read CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
5. run python scripts/validate_pc_work_control_plane.py
6. require CONTROL_PLANE_PASS
7. read CURRENT_PC_WORK_STATE.json
8. read Rule Registry MD + JSON
9. execute only v20.2.3
10. DO NOT redesign the current good UI
11. inspect the actual Windows desktop MEDIA AI shortcut
12. compare desktop-icon launch with worker-opened good launch
13. repair launcher/cache/window parity
14. replace/update desktop shortcut to canonical launcher
15. close/reopen using ONLY the desktop icon
16. prove the same current UI opens without bottom clipping
17. leave desktop icon and reopened UI available for representative click test
18. publish exact v20.2.3 Evidence
19. commit, push, remote-readback

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_WINDOWS_DESKTOP_LAUNCHER_CACHE_VIEWPORT_PARITY_CORRECTION_DIRECTIVE_v20.2.3_20261002.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.3_20261002.json

## REPRESENTATIVE OBSERVATION

Current worker-opened v20.2.2 UI:
GOOD / visually acceptable for the present correction stage.

Existing desktop-icon launch:
DIFFERENT / lower UI clipping or stale geometry appears.

This cycle diagnoses launch-path parity only.

## LIKELY CAUSES TO VERIFY

- desktop shortcut still points to old URL/query
- desktop shortcut points to stale worktree/server process
- browser cache serves old approved_visual.css
- product server does not send no-store for UI static assets
- desktop shortcut opens a restored/smaller browser window instead of maximized current view

Do not assume; verify actual Windows shortcut Target/Arguments/WorkingDirectory first.

## HARD FREEZE

DO NOT CHANGE:
- VIDEO/PHOTO UI geometry from current v20.2.2
- color hierarchy
- Shortform button/order
- runtime/model/Marketing behavior

## ICON DESIGN PHASE

BLOCKED_PENDING_UI_AND_LAUNCHER_APPROVAL

The existing desktop icon is only the launcher under test.
It is NOT yet the final approved icon design.

## EXACT OUTPUTS

Review:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_REVIEW_v20.2.3_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_LAUNCHER_PARITY_EVIDENCE_v20_2_3_20261002.json

Detail:
evidence/pc_remote/media-ai-launcher-parity-v20_2_3-20261002/

Required files:
20

## FINAL RULE

SYNC → VALIDATE → FORENSIC DESKTOP SHORTCUT → SAME CURRENT SERVER/HEAD/CSS → FRESH CACHE → MAXIMIZED VIEWPORT → DESKTOP ICON REOPEN TEST → REPRESENTATIVE CONFIRMATION.
