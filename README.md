# MINDLE MEDIA AI

Canonical development branch: `feature/ad-shortform-bridge-p0-20260926` · PR #23: **Draft / HOLD / DO NOT MERGE**.

## Current scope — 2026-10-25 KST

Local Qwen generative planning, Supertonic Korean neural narration, FFmpeg media processing, durable execution, project persistence and product evidence are implemented. Text-to-new-video and semantic scene generation are **not implemented**.

Latest AI core and behavior review: [Actual inference failures, isolated 7B proof and completion gates](docs/evidence/media-ai-core-behavior-audit-20261025/RESULT_KO.md). The AI auto-edit button now requires real input-bound Qwen decisions and technical output checks; no deterministic fallback. The tested 1.5B configuration failed automatic exposure judgment. A separate 7B evaluation passed two synthetic cases; it has not replaced installed models. Whole-product acceptance remains pending.

Earlier source review and remaining acceptance:
[Commander core closeout](docs/evidence/media-ai-commander-closeout-20261025/RESULT_KO.md) · [Machine validation](docs/evidence/media-ai-commander-closeout-20261025/SOURCE_VALIDATION.json).

- Latest source regression: 329 Python PASS, 5 SKIP remotely; 31 UI JavaScript PASS locally.
- This review: actual pinned Qwen automatic-edit probes and FFmpeg/HTTP/file-evidence tests. **Supertonic and the complete latest Windows promotional-video chain were not rerun**.
- Prior R3: [remote Windows candidate evidence](docs/evidence/windows-ai-successor-20261024-r3/RESULT_KO.md), source `9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6`. That EXE does not contain today's changes.
- Office PC acceptance, human listening and approved visual comparison remain pending.
- Package Build Gate=false; no new candidate, final release or merge authorized by this source closeout.

## Worker entry

Read the current directive and machine state before executing PC or package work:

1. `CURRENT_PC_WORK_DIRECTIVE.md`
2. `CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json`
3. `CURRENT_PC_WORK_STATE.json`
4. `CURRENT_WORKER_COORDINATION_LOCK.json`
5. `scripts/validate_pc_work_control_plane.py`
6. The active directive and its Evidence contract.

The October 6 recovery-only notice previously displayed here is historical. This README is a status index, not a replacement for execution locks or build approval. Never reuse consumed build authorization or treat source tests as Windows product acceptance.
