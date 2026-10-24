# MINDLE MEDIA AI — GENERAL WORK → PC WORK ONE-CLICK HANDOFF v1.0

Date: 2026-10-08
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
General Work final HEAD: 9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb

## General Work final result

PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK

Verified:
- actual Chrome checks: 75 PASS
- Python: 77 PASS
- UI tests: 2 PASS
- pip check / compile / General Work validator: PASS
- findings: 20 total
  - 18 fixed
  - 2 explicitly disabled / NOT_IMPLEMENTED
- open active base-product gaps: 0
- actual Export ZIP / media SHA / CRC verified
- owner-approved UI preserved
- PHOTO / VIDEO base runtime PASS preserved
- external Marketing / AVORA: DEFERRED_EXTERNAL
- main unchanged
- PR #23 HOLD / DO NOT MERGE

General Work Review:
docs/commander/MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_REVIEW_v1.0_20261008.md

General Work Evidence:
docs/evidence/media-ai-general-work-final-self-audit-20261008/EVIDENCE.json

## Frozen product baseline for PC Work

PC Work must not redesign or re-implement the product.

Use commit 9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb as the handoff baseline and preserve:
- MINDLE MEDIA AI approved UI
- VIDEO approved structure and playback/runtime
- PHOTO landscape-first Preview
- portrait Auto Fit / centered margins
- PHOTO 7 basic correction controls
- segmentation / 4x upscale
- Korean STT
- Save / full close / reopen behavior
- base Export
- 광고 숏폼 entry with graceful external-unavailable behavior

## PC Work objective

Replace the old complex employee installer workflow with a ONE-CLICK RUNTIME PACKAGE.

Employee-visible flow:
1. receive the runtime artifact/package
2. double-click one MINDLE MEDIA AI launcher
3. local runtime starts automatically
4. browser opens automatically
5. MINDLE MEDIA AI is ready to use

The employee must not perform Git clone, Python/pip installation, terminal commands, manual model acquisition, repository selection, script selection, environment-variable entry, or manual dependency repair.
