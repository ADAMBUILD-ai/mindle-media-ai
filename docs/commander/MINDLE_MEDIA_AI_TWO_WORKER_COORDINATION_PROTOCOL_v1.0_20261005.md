# MINDLE MEDIA AI — TWO-WORKER COORDINATION PROTOCOL v1.0

Date: 2026-10-05
Status: GOVERNING

## 1. Purpose

Two workers may operate around MEDIA AI, but they must not both behave as product writers.

The repository uses two lanes.

## 2. Worker A — PRODUCT / WINDOWS REAL-USE EXECUTOR

Primary role:
- execute active v21.0 product audit
- Windows runtime
- desktop shortcut / launcher runtime checks
- VIDEO / PHOTO / Shortform real function tests
- Save/Reopen/Export
- fix product defects only when required by active directive
- publish current-cycle Review/Evidence

Write ownership while v21.0 is ACTIVE:
- ui/**
- src/**
- scripts/** except commander-only governance files
- tests/**
- current-cycle docs/evidence explicitly required by v21.0

Worker A may update product code only within active directive scope.

## 3. Worker B — MASTER / REPOSITORY GOVERNANCE AUDITOR

Primary role:
- Master consolidation
- branch/PR map
- evidence completeness review
- documentation cleanup
- conflict detection
- handover/status reporting

Write ownership:
- repository governance docs
- Master handover docs
- repository consolidation docs
- audit/review docs explicitly assigned to Worker B

Worker B MUST NOT modify while Worker A is active:
- ui/**
- src/**
- runtime launcher behavior
- tests/**
- CURRENT control-plane files
unless the commander explicitly transfers ownership.

If Worker B finds a product defect:
- document it
- produce a proposed directive/review
- do not patch product files directly

## 4. No overlapping writes

The same file may not be edited by both workers in the same cycle.

Before writing, each worker must inspect:
CURRENT_WORKER_COORDINATION_LOCK.json

If another lane owns the file:
STOP and report LANE_OWNERSHIP_CONFLICT.

## 5. Git behavior

Both workers use:
feature/ad-shortform-bridge-p0-20260926

Rules:
- fetch before work
- read remote HEAD
- no force push
- no main merge
- no checkout of historical work/* as current
- if remote HEAD moved after local work started, reconcile before push
- never overwrite another worker's new commit by using stale SHA blindly

## 6. Commit labels

Worker A commit prefix:
product:
runtime:
fix:
test:
evidence:

Worker B commit prefix:
master:
repo:
governance:
review:

This is for human traceability only; Control Plane remains authoritative.

## 7. Handoff sequence

Worker A:
ACTUAL RUN → FIX → RETEST → EVIDENCE → PUSH

Worker B:
READ REMOTE → INSPECT → CLASSIFY → MASTER/REPO DOC UPDATE → PUSH

Worker B must not run a repo reorganization commit in the middle of Worker A's unpushed file edits.

## 8. Final authority

Representative/user approval > current commander Control Plane > lane lock > worker local assumptions.

## Final rule

TWO WORKERS MAY EXIST, BUT ONLY ONE PRODUCT WRITER MAY OWN PRODUCT FILES AT A TIME.
