# MINDLE MEDIA AI — PC WORK MANDATORY EVIDENCE SAVE & CONTINUATION RULE v1.0
Date: 2026-09-30
Status: PERMANENT PC WORK OPERATING RULE

## Mandatory rule
Every PC Work directive execution MUST save and commit inspection evidence to the GitHub repository before the work cycle ends.

This applies to every outcome:
- PASS
- REWORK
- FAIL
- BLOCKED
- VERIFY_REQUIRED
- timeout/recovery
- partial completion

## Required cycle
DIRECTIVE -> ACTUAL EXECUTION -> SELF-VERIFY -> EVIDENCE MD/JSON -> GITHUB COMMIT -> NEXT DIRECTIVE/HANDOFF

No evidence commit = work cycle NOT COMPLETE.

## Required evidence
At minimum record:
- directive path/commit
- branch/head
- actual Windows actions performed
- changed files
- commands/process/service/port where relevant
- actual UI/runtime results
- PASS/REWORK per lane
- screenshots/output paths/hashes where available
- exact blocker/root cause
- regression result
- remaining work
- commit SHA

Evidence must be stored under docs/commander and/or evidence/pc_remote according to the active directive. Never overwrite prior evidence.

## No unnecessary approval pause
If the active directive already authorizes code fixes, tests, evidence creation and branch commits, do not stop to ask whether to commit. Commit the authorized work, verify it, save evidence and continue.

## Automatic continuation
After evidence is committed, create or update the next executable directive/handoff based strictly on the evidence. Freeze successful lanes; carry forward only failed/incomplete lanes.

## Protection
This rule does not authorize main merge, Production deployment, force push, credential exposure, UI SSOT redesign, GPU/paid compute or other actions outside the active directive.
