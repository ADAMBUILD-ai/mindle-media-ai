# MINDLE MEDIA AI

Canonical development branch: `feature/ad-shortform-bridge-p0-20260926` · PR #23: **Draft / HOLD / DO NOT MERGE**.

## Current scope — 2026-10-25 KST

Local Qwen generative planning, Supertonic Korean neural narration, FFmpeg media processing, durable execution, project persistence and product evidence are implemented. Text-to-new-video and semantic scene generation are **not implemented**.

Latest source review and remaining acceptance:
[Commander core closeout](docs/evidence/media-ai-commander-closeout-20261025/RESULT_KO.md) · [Machine validation](docs/evidence/media-ai-commander-closeout-20261025/SOURCE_VALIDATION.json).

- Source regression: 280 Python PASS, 6 SKIP; 30 UI JavaScript PASS.
- This revision: actual local FFmpeg/HTTP/file-evidence tests; **Qwen/Supertonic inference not rerun**.
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
