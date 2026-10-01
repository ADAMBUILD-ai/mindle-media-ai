# MINDLE MEDIA AI — COMMANDER ↔ PC WORKER REPOSITORY CIRCULATION PROTOCOL v1.0
Date: 2026-10-01
Status: PERMANENT SSOT OPERATING RULE
Repository: ADAMBUILD-ai/mindle-media-ai
Working branch: feature/ad-shortform-bridge-p0-20260926

## 1. Single shared coordination surface
Commander and PC Worker communicate execution state through THIS GitHub repository/branch.
Do not rely on chat-only statements, Desktop notes, temporary files, or memory as the authoritative handoff.
The repository is the circulation bus for:
DIRECTIVE -> WORK -> EVIDENCE -> COMMANDER REVIEW -> NEXT DIRECTIVE.

## 2. Exact locations
Commander directives / human-readable reviews:
docs/commander/

PC Worker machine-readable evidence:
evidence/pc_remote/

Per-cycle screenshots/log refs/manifests/output inventories:
evidence/pc_remote/<cycle-name>/

Permanent worker bootstrap:
docs/commander/MINDLE_MEDIA_AI_NEW_PC_WORKER_BOOTSTRAP_ROUTE_CORRECTION_HANDOFF_v1.0_20261001.md

Route correction:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_COMMANDER_ROUTE_CORRECTION_NO_GITHUB_LOGIN_LOOP_DIRECTIVE_v12.1_20261001.md

## 3. Mandatory circulation
A. Commander:
- inspect latest remote Evidence
- verify facts
- freeze PASS lanes
- write next executable directive to docs/commander/
- commit/push directive

B. PC Worker:
- fetch/pull the working branch
- read latest directive
- execute actual Windows work
- self-verify
- write Review MD + Evidence JSON + Manifest to exact repository locations
- commit/push
- verify remote files exist
- report exact remote commit SHA

C. Commander:
- inspect those remote files, not chat claims
- immediately create/push the next directive
- repeat

No cycle is complete without remote GitHub persistence.

## 4. No waiting for redundant approval
If the directive authorizes code/test/evidence/branch commit/push, Worker does not ask:
- where to save
- whether to commit
- whether to push
Commander does not wait for user to remind it to issue the next directive after evidence review.

## 5. Worker replacement
A replacement Worker starts by:
1. fetch/pull working branch
2. read this circulation protocol
3. read NEW_PC_WORKER_BOOTSTRAP
4. read latest commander directive
5. inspect latest Evidence/Review
6. execute only remaining lanes
Previous worker browser/auth state is not inherited as SSOT.

## 6. Current route protection
GitHub artifact-download authentication is NOT the general work path.
Do not create repeated GitHub sign-in windows.
Existing repository commit/push path remains separate.
Current product-first rule: inspect current PC runtime/models first, run independent PHOTO/4x/VIDEO/STT lanes, selectively recover only exact missing items.

## 7. Evidence naming
Every meaningful cycle must contain:
- Review MD in docs/commander/
- Evidence JSON in evidence/pc_remote/
- Manifest in evidence/pc_remote/<cycle-name>/
All must identify directive path/commit, starting HEAD, actual Windows actions, lane verdicts, outputs/hashes, exact blockers, UI_SSOT_CHANGED, final remote commit SHA.

## 8. Commander review discipline
Commander must not accept “done/saved/sent” without remote verification.
Review order:
commit history -> Review MD -> Evidence JSON -> Manifest -> outputs/log refs -> verdict -> next directive.

## 9. Granularity
Do not micro-slice ordinary technical steps.
One directive should carry all executable downstream work until meaningful completion or a true human/external gate.
One blocked lane must not stop independent runnable lanes.

## 10. Current immediate objective
MINDLE MEDIA AI Windows product E2E:
current-PC inventory -> four-lane runtime matrix -> run available PHOTO segmentation / PHOTO 4x / VIDEO tracking / Korean STT -> Preview -> Save -> Export -> regression.
Shortform is separate and remains VERIFY_REQUIRED without approved Contract v1/assets.

## 11. Protection
No UI SSOT redesign, fabricated results, credential exposure, main merge, Production deploy, force push, destructive cleanup, unnecessary GitHub authentication, or unverified model substitution.
