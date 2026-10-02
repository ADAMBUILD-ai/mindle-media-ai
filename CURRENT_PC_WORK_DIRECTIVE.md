# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261002-V20.2.6
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
7. read CURRENT_PC_WORK_STATE.json and Rule Registry
8. execute ONLY v20.2.6
9. restore WORKSPACE ui/approved_visual.css exactly from golden commit 97900cc6c784e74b4224333fa2cc84d29c611f87
10. verify PHOTO CENTER returns to the previous accepted workspace appearance
11. verify VIDEO stays in the previous accepted workspace appearance
12. preserve later icon/favicon/no-cache/launcher improvements
13. lock the corrected WORKSPACE UI
14. desktop shortcut must launch ONLY that same workspace
15. no copied desktop UI, no desktop-only CSS, no old worktree
16. compare workspace direct launch vs desktop launch at same viewport/zoom
17. publish exact v20.2.6 Evidence
18. push and remote-readback

## ACTIVE DIRECTIVE

docs/commander/MINDLE_MEDIA_AI_WORKSPACE_GOLDEN_TO_DESKTOP_EXACT_MIRROR_FINAL_DIRECTIVE_v20.2.6_20261002.md

## ACTIVE EVIDENCE CONTRACT

docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_v20.2.6_20261002.json

## SINGLE SOURCE OF TRUTH

WORKSPACE UI ONLY.

Golden geometry commit:
97900cc6c784e74b4224333fa2cc84d29c611f87

Rejected clipping commit:
2ab174e03dc786c53f38ba956dea95f8e1ccd5a7

## HARD RULE

The desktop is NOT a second UI build.

Desktop shortcut:
→ repository-owned launcher
→ current repository root
→ same ui/ files

No desktop-specific UI modifications are allowed.

## EXACT OUTPUTS

Review:
docs/commander/MINDLE_MEDIA_AI_WORKSPACE_GOLDEN_TO_DESKTOP_MIRROR_FINAL_REVIEW_v20.2.6_20261002.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_WORKSPACE_GOLDEN_TO_DESKTOP_MIRROR_FINAL_EVIDENCE_v20_2_6_20261002.json

Detail:
evidence/pc_remote/media-ai-workspace-mirror-v20_2_6-20261002/

Required files:
26

## FINAL RULE

RESTORE WORKSPACE GOLDEN UI → LOCK WORKSPACE → DESKTOP LAUNCHES SAME WORKSPACE → COMPARE → PASS ONLY IF IDENTICAL.
