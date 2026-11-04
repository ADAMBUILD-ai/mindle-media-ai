# AI Adapter Contracts

## Common adapter contract

Every adapter accepts a typed request, records immutable model identity and returns an artifact reference. It must expose a fallback without altering the user interface.

| Field | Requirement |
|---|---|
| `adapter_id` | stable internal identifier |
| `repo_id` and `revision` | required before model activation |
| `license_status` | explicit verified, pending, rejected, or blocked |
| `input_artifacts` | input, mask, reference and source metadata where applicable |
| `output_artifacts` | output file, metrics, duration, hash and preview |
| `fallback` | deterministic local route and reason |
| `quality_gate` | technical, benchmark, real-fixture, or production status |

No adapter may enable `trust_remote_code`, download unpinned weights, or silently substitute a provider.

## Natural-language and reference-image ingress

The fixed UI may submit at most five reference images with each natural-language
command. The browser state and the Python bridge apply the same contract: only
JPG, PNG, WEBP, and TIFF filenames are accepted; path components are removed;
and a filename may occur once only, case-insensitively. Invalid references fail
before routing or adapter selection, while the command draft remains available
for retry. This code-level contract does not change the approved UI SSOT.

## Job execution boundary and evidence hook

The bridge preserves the command text, routed media type, source asset, normalized
reference filenames, requested operation, project identifier, and optional output
target in one `MediaJob`. The runtime follows `QUEUED → VALIDATING → READY →
RUNNING` before reaching `SUCCEEDED`, `FAILED`, `BLOCKED_INPUT`, or
`BLOCKED_MODEL`. Failed and blocked jobs keep their original command and reference
selection so a retry does not require rebuilding the UI state.

Each operation resolves to a stable photo or video adapter boundary before execution.
The boundary records the model or program identifier, pinned revision when applicable,
and license/source status. A request that explicitly requires a verified model becomes
`BLOCKED_MODEL` until a verified adapter is available; it never treats an unverified
cache or fallback as model success. Missing source input becomes `BLOCKED_INPUT`.

Execution evidence captures source and output hashes, adapter identity, revision,
license/source, runtime environment, latency, project identifier, requested operation,
and reference filenames. Local deterministic execution is marked `VERIFY_REQUIRED`;
it does not claim `TESTED_PASS` or `DELIVERED` before real MEDIA input and Runtime
E2E evidence are available.

Every job also carries a stable job identifier, evidence identifier, and source
provenance record. Empty sources and absent or mismatched provenance fail closed as
`BLOCKED_INPUT`. Re-submitting a completed or in-flight job with the same identifier
returns the existing result instead of creating duplicate execution or evidence.
Retry attempts preserve both identifiers and record their attempt number in evidence.

## Queue and output contract

The common Job Queue deduplicates equivalent submissions by a stable idempotency
key, permits cancellation only while a job is queued, and permits retry only after
a failure. Photo and video lanes share this queue contract but retain independent
adapter boundaries. Successful local execution records an output artifact path,
type, size, hash, and availability status. The runtime rejects a successful result
whose required provenance, adapter, hash, retry, or output evidence is incomplete.

## Runtime orchestration readiness

Runtime orchestration is a separate, fail-closed path that preserves the approved
UI contract. It validates source presence, extension, size, provenance, SHA-256,
adapter identity, pinned revision, license source, backend, and device requirement
before dispatch. `PHOTO`, `VIDEO`, and `KOREAN_AUDIO` lanes preflight independently:
missing input in one lane records `BLOCKED_INPUT` and never holds another lane.

The orchestration state sequence is `PREFLIGHT_READY → DISPATCHED → RUNNING →
OUTPUT_VALIDATING → SUCCEEDED/FAILED/BLOCKED`. Dispatch builds an immutable context
containing the job and evidence IDs, source hash, natural-language instruction,
reference-image names, retry provenance, and adapter identity. A cancelled job cannot
become successful; retries are limited to failed jobs. Output completion requires a
nonempty artifact of the expected type, SHA-256, size, and a parseability check before
success is recorded.

The adapter registry explicitly records availability. An unavailable model or program
returns `MODEL_UNAVAILABLE`/`BLOCKED_MODEL`; it does not substitute a mock result.
Korean-audio Runtime remains unavailable until a verified adapter and real Korean audio
are supplied. Model Scout callback receipts must match both job and evidence IDs and
are evidence-only: callback status never promotes a job to a runtime success.

## Model Scout integration gate

Model Scout handoffs require request and issue IDs, lane and operation, model/program
source and exact revision, license evidence, artifact filename/size/SHA-256, backend,
device requirement, adapter ID/version, verification status, and issue time. Only a
locally materialized `VERIFIED` handoff with matching filename, size, and SHA-256 enters
the adapter registry. Registry readiness rechecks the artifact before preflight.

Input intake creates a per-lane manifest with provenance, size, and SHA-256; one ready
lane is `PARTIAL_INPUT_READY` without waiting for other media types. A real runtime may
start only when both the intake manifest and registered adapter are ready. A Model Scout
`TESTED_PASS` callback must match request/issue/job/evidence IDs, lane, revision,
artifact hash, adapter version, backend, device, input hash, output identity/hash, and
elapsed time. On success it records `DELIVERED`; these contracts validate receipts only
and do not execute or claim local model inference.

## Track A feature-flag contracts

All entries below are integration-ready only. `adapter_enabled` stays `false`
until the applicable benchmark and human-quality gate are complete; a KEEP
recommendation never turns on production automatically.

| Capability | Pinned candidate | Input -> output | Timeout / UI evidence | Fallback |
|---|---|---|---|---|
| Object selection and tracking | SAM 2.1 Hiera Base Plus, `facebook/sam2.1-hiera-base-plus` at `b7320756a13354e7530a63935656d35b2f91a290` | image or video frame plus prompt -> mask artifact | timeout, VRAM failure, `fallback_used`, `VERIFY_REQUIRED` | existing mask or manual selection / GrabCut |
| Object removal | LaMa ONNX, `opencv/inpainting_lama` at `aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f` | image plus mask -> inpainted image artifact | timeout, output hash, fallback evidence | OpenCV TELEA |
| Subtitles | Whisper Large v3 Turbo, `openai/whisper-large-v3-turbo` at `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` | audio -> text and timestamp segments | Korean benchmark is blocked; show `VERIFY_REQUIRED` | manual subtitle or FFmpeg subtitle path |
| High resolution | Qualcomm Real-ESRGAN x4plus ONNX, `qualcomm/Real-ESRGAN-x4plus` at `4022efb8b74eb88900724d9e05a468ac3673df4a` | image -> 4x image artifact | human review is required; output hash and fallback evidence | OpenCV Lanczos4 |
| Background separation | no approved model | image -> mask or alpha artifact | safe-model scout is blocked; show `VERIFY_REQUIRED` | OpenCV GrabCut |

The UI uses capability names, not model names. Any execution error, timeout,
or memory shortage must surface the selected fallback and preserve the command
text for retry; it must not appear as a successful model result.

## Owned external production asset boundary

Blender, ComfyUI, and local video-generation models enter MEDIA through the
registry in `external_assets/media-production/ASSET_REGISTRY.json`. A registry
entry is evidence of identity and policy only. It cannot become enabled unless
its state is `RUNTIME_READY` or `PRODUCT_RUNTIME_VERIFIED`; model and program
downloads remain a separate, reviewed materialization step.

Blender receives only a structured request through the hash-pinned MEDIA camera
render driver. User text cannot select another Python script or a Python/shell
expression. The driver selects an existing camera, applies bounded frame and
resolution values, renders, and hashes its output receipt.

ComfyUI must listen on an explicit loopback address and isolated MEDIA-owned
port. Its API workflow bytes are hash-pinned and only named node inputs may be
overridden. Because ComfyUI's interrupt endpoint affects global execution, the
adapter rejects cancellation unless MEDIA owns that isolated process and the
prompt identifier. Output paths must resolve inside the owned output root.

Wan activation additionally requires pinned model bytes, an official exported
API workflow, target-PC hardware evidence, a real generated clip, and human
quality review. LTX Desktop remains hardware-deferred. None of these pending
assets may replace the existing FFmpeg edit/export path or appear as successful
AI generation in the UI.

Architecture-video production plans contain one to twelve ordered scenes. Each
scene fixes its engine (`existing_clip`, `blender`, or `wan22`), source SHA-256,
bounded duration, and engine-specific camera or prompt. The output must remain
an MP4 under the owned job root. Preflight returns `BLOCKED_INPUT` for an invalid
or changed source and `BLOCKED_ASSET` when any exact runtime is disabled.

Only a ready plan may enter delivery. The delivery adapter rechecks pinned
FFmpeg and FFprobe executable hashes, source hash stability, and output path
containment; it invokes a fixed argument vector without a shell. Published MP4
must decode as H.264/yuv420p, use AAC when an audio stream exists, and place the
`moov` atom before `mdat` for browser preview. This technical receipt does not
certify generated-scene quality or human hearing.

Multi-scene delivery normalizes ordered clips to a bounded even resolution and
24 fps, preserves aspect ratio with centered padding, supplies silence for a
clip without audio, and concatenates paired video/audio streams in plan order.
The output cannot reuse any source path. Its receipt includes the ordered scene
IDs and every source hash, and the measured duration must match the planned sum.

The architecture-production ledger persists request fingerprint, plan, asset
requirements, state, and final receipt in SQLite with full synchronous writes.
Identical request keys replay the same record; a different plan under the same
key is rejected. A process restart converts `RUNNING` and `CANCEL_REQUESTED` to
`INTERRUPTED`, never success. Completion is allowed only from `RUNNING` after
the published output path, size, and SHA-256 match the delivery receipt.
