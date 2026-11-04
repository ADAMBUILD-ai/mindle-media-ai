# MINDLE MEDIA AI — NEW PC WORKER BOOTSTRAP / ROUTE CORRECTION HANDOFF v1.0
Date: 2026-10-01
Status: NEW WORKER START HERE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926

## 1. Worker replacement
The previous PC Work execution is terminated/replaced.
New worker must NOT inherit the previous worker's active browser/authentication state or assumptions.
Start from repository evidence and this handoff.

## 2. Read order
Read in this exact order:
1. docs/commander/MINDLE_MEDIA_AI_PC_WORK_COMMANDER_ROUTE_CORRECTION_NO_GITHUB_LOGIN_LOOP_DIRECTIVE_v12.1_20261001.md
2. docs/commander/MINDLE_MEDIA_AI_PC_WORK_CURRENT_PC_FIRST_PRODUCT_RECOVERY_DIRECTIVE_v12.0_20261001.md
3. docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_LOCATION_COMMIT_PUSH_OPERATING_RULE_v2.0_20260930.md
4. latest v11 Review/Evidence only as historical blocker context.

v12.1 overrides the old interpretation that historical Artifact 10797756522 or GitHub login is a universal prerequisite.

## 3. First actions after new worker starts
A. Close/dismiss any leftover Connect to GitHub / Sign in dialogs created by the previous MEDIA AI worker, if safe.
B. Do not click Sign in with browser/code.
C. Do not create a new GitHub auth flow.
D. Confirm GITHUB_AUTH_LOOP_STOPPED.
E. Begin CURRENT-PC runtime/model inventory immediately.

## 4. Product-first objective
Goal: actual MEDIA AI Windows product E2E.
Not goal: historical artifact reconstruction.

Inventory current PC first, then build independent runtime matrix for:
- PHOTO segmentation
- PHOTO 4x
- VIDEO tracking
- Korean STT

Run every lane that is currently runnable.
One blocked lane must not block the others.

## 5. Actual execution standard
For each runnable lane:
real approved input -> actual UI/product action -> job/result -> Preview -> quality -> project save -> Export where applicable -> reopen/hash.
Backend-only success is insufficient.

## 6. Selective recovery
Only after inventory proves an exact required model/file/revision is absent may it be recovered.
Historical GitHub Artifact 10797756522 is last-resort selective recovery only, never the first action.
No repeated GitHub login windows.

## 7. Shortform
Separate gate. No approved Contract v1/assets = VERIFY_REQUIRED without blocking base MEDIA AI.

## 8. Evidence cycle
At meaningful completion:
Review MD + Evidence JSON + Manifest -> commit -> push -> remote verify -> one broad next directive -> commit/push.
Do not ask user where to save or whether to commit.

## 9. Immediate PASS gate for route correction
Before proceeding far, evidence must show:
- GITHUB_AUTH_LOOP_STOPPED: PASS
- duplicate auth dialogs remaining: 0
- current-PC inventory started/completed
- four-lane runtime matrix created
- UI_SSOT_CHANGED:NO

## Protection
No UI redesign, no credential exposure, no main merge, Production deploy, force push, fabricated results, unverified model substitution, destructive cleanup, or unnecessary GitHub authentication.
