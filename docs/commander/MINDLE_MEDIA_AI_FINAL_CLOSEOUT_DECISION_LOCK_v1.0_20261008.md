# MINDLE MEDIA AI — FINAL CLOSEOUT DECISION LOCK v1.0

Date: 2026-10-08
Status: OWNER DECISION LOCKED
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926

## 1. FINAL CLOSEOUT SEQUENCE — LOCKED

The final sequence is fixed as follows:

1. General Work performs one complete self-audit of all work completed to date.
2. Any missing, partial, dead, disconnected, mocked, stale, or non-runtime function found during the audit is fixed in General Work.
3. General Work publishes Evidence and receives:
   PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK
4. Only after that PASS may PC Work begin.
5. PC Work creates and validates a ONE-CLICK RUNTIME PACKAGE.
6. Final employee experience is double-click once -> runtime starts -> browser opens -> MINDLE MEDIA AI is usable.

No PC Work packaging may begin before General Work PASS.

## 2. EXTERNAL INTEGRATION POLICY — DEFERRED

Marketing AI / AVORA / external Shortform live integration is deliberately deferred.

Existing requests and Evidence are preserved, but they are NOT an active blocker for General Work self-audit or the subsequent local one-click runtime package.

Deferred items:
- MARKETING_SHORTFORM_BASE_URL
- MARKETING_SHORTFORM_BRIDGE_TOKEN
- real Marketing HTTP
- approved AVORA asset
- 9:16 Shortform live Preview
- Representative Approval
- approved advertisement MP4 live export

The 광고 숏폼 UI entry and existing bridge code must remain present and non-destructive.
Do not delete or falsely mark the external integration PASS.

## 3. OWNER-APPROVED UI LOCK

The General Work audit must treat the latest owner-approved UI decision as authoritative.

Locked principles:
- Product title: MINDLE MEDIA AI
- Do not show the word SSOT as the product title.
- VIDEO side remains the approved structure; do not redesign it.
- PHOTO is landscape-first for the main Preview.
- PHOTO and VIDEO must read as one clean paired product.
- Original aspect ratio is preserved for both VIDEO and PHOTO.
- No forced stretching.
- Landscape PHOTO should use the Preview efficiently.
- Portrait PHOTO uses Auto Fit / centered placement with natural side margins.
- PHOTO basic correction functions must remain available, including brightness, contrast, highlights, shadows, saturation, color temperature, and sharpness.
- Crop/rotate and the approved PHOTO AI tools remain available.
- 광고 숏폼 remains visible in VIDEO.
- Existing approved dark-navy / blue-cyan VIDEO / purple-magenta PHOTO identity is preserved.
- No broad visual redesign during final audit.

If repository implementation does not match these locked points, it is a General Work gap and must be corrected before PASS.

## 4. PACKAGE STRATEGY — LOCKED

Do NOT return to the previous complex employee installer-package strategy as the primary closeout target.

PC Work target is:
ONE-CLICK RUNTIME PACKAGE

Required employee experience:
- receive package
- double-click one launcher/icon
- local runtime starts automatically
- browser opens automatically
- MINDLE MEDIA AI opens directly
- no Git
- no repository clone
- no Python installation by the employee
- no pip
- no terminal commands
- no HF_TOKEN entry
- no manual model download
- no developer profile/worktree dependency

Formal installer/MSI/EXE distribution may be considered later only after runtime use is stable.

## 5. EVIDENCE RULE

No PASS without actual Evidence.
Document existence is not PASS.
UI appearance alone is not PASS.
Unit tests alone are not PASS.
A button that is present but not connected is FAIL.
A runtime path that depends on developer-only state is FAIL.

## 6. MERGE / PROTECTION

- main/default branch merge forbidden
- force push forbidden
- new repo/worktree forbidden
- PR #23 remains HOLD / DO NOT MERGE
- historical Evidence must not be deleted
- frozen valid PASS Evidence may be reused if the audited component was not changed

This document is the final owner decision lock for the General Work -> PC Work closeout order.
