# MINDLE MEDIA AI PC Torch Recovery / Final Local E2E Review v32.0

Date: 2026-09-25  
Repository: `ADAMBUILD-ai/mindle-media-ai`  
PR: `#22`  
Branch: `work/v28-1-remote-runtime-package-20260924`  
Verified source fix head: `95be3ee184b0277d9e03f4a667515cb67a6a2d50`

## Decision

**PASS for the requested local CPU runtime and product backend closeout.**

The frozen PASS lanes remain unchanged: remote package/license/canonical gates, remote approved UI E2E, exact PC materialization of SAM 2.1 / whisper-small / Intel SISR OpenVINO, PHOTO target selection, and the non-black 4x output. The remaining rework from v32 was executed against the actual restored PHOTO, VIDEO, and Korean audio inputs.

## Evidence summary

- Torch import recovery: `outputs/mindle-media-v30-runtime/torch-import-v32.json`; torch `2.14.0+cu126` loaded on Python `3.11.9` in `29.158997297286987s`. The earlier “crash” was a wrapper timeout, not a torch import failure.
- PHOTO segmentation: job `92d190cc-c747-4e3a-bf62-b57d1c85fbda`, evidence `725260a0-f8b5-49b4-90a3-433433250c1c`, `TESTED_PASS`; SAM 2.1 CPU; prompt point `[125,146]`; overlay output validated.
- PHOTO 4x SISR: job `44b04f92-ac92-417a-b987-41fe457854f1`, evidence `84be1dcd-d394-4b61-b58a-c303ba39223a`, `TESTED_PASS`; `1920x1080`, `1,920,451` bytes, SHA-256 `4806a7ab40db3cf8dabec2451ee58015c70e662834643389ae8b6d4684c9d35f`.
- VIDEO tracking: job `bdeb31cd-f47d-453a-9e77-815bc3680704`, evidence `62277a17-efe7-401d-9f48-c05ac23dcd1f`, `TESTED_PASS`; four non-empty mask/overlay samples and validated MP4 output. The Windows validator now uses OpenCV when `ffprobe` is unavailable.
- Korean STT: job `924746ee-4c03-48c3-9141-c7e09518698b`, evidence `0e55ada2-77ae-42be-a382-a65d7291d21f`, `TESTED_PASS`; exact pinned whisper-small on CPU; 16 kHz / 12.48 s; transcript emitted; WER `0.35714285714285715`.
- Project save: project `f1434a9a-e76a-4ff6-8a35-0e57ec6eae03`, SHA-256 `5643a63530fcfa73b89c4018e6ec373d829df09839822b60bfe72d7dfe3bf962`.
- Project export: `f1434a9a-e76a-4ff6-8a35-0e57ec6eae03_export.zip`, `2,798,557` bytes, SHA-256 `cbda249c11c1a52e1c63277d1628fbae361e812dff9f23bdeedd15603a0947c3`.

Full machine-readable evidence is in `evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json`.

## Source fixes applied and verified

- `c2505411f9f066bc56f5475fa08ebf07267d3af9`: validate Windows VIDEO outputs through OpenCV instead of requiring `ffprobe`.
- `95be3ee184b0277d9e03f4a667515cb67a6a2d50`: make the Korean STT adapter read pinned float32 PCM WAV input with the standard library and calculate WER internally, removing the undeclared `soundfile`/`jiwer` runtime dependency.

Remote verification after the fixes is green: Canonical `36093824185`, License Gate `36093824166`, Product E2E `36093824149`, Remote Package `36093824228`, and Windows OpenVINO supplement `36093824242` all completed successfully. Unrelated heavyweight lanes were intentionally skipped.

## Scope boundary / next work

The local product API path performed the real model work and completed save/export. The browser-native file chooser could not be driven by this desktop automation surface, so a separate browser-only Preview → Save → Export replay is not asserted as PASS. No UI/SSOT files were changed. The next directive records only this narrow remaining replay item.

