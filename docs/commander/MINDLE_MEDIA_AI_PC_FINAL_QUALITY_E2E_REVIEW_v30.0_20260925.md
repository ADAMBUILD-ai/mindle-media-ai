# MINDLE MEDIA AI PC Final Quality E2E Review v30.0

- Decision: **REWORK — remote product quality PASS; final PC-local VIDEO/STT/UI re-run remains incomplete.**
- Source head reviewed: `c5b559793ffaea5e5fc1fb8eaa4c63a7c123fbd2`
- UI SSOT changed: **NO**. Production, merge, force-push, GPU, and paid compute: **NOT USED**.

## Frozen PASS evidence

| Gate | Result | Evidence |
|---|---|---|
| Canonical baseline / licence | PASS | runs `36089930054`, `36089930079` |
| Exact remote runtime package | PASS | run `36089930051`; part-00 `10845890220` / `sha256:5d0fb6ba466b9ad77a6ebaac0e15eb730994f1968def25405f1a535643114ee4`, part-01 `10845890248` / `sha256:14f282cef0360c8c13edb7416f4b1a78053a95408199771ddd20680d25fda8e1`, part-02 `10845670524` / `sha256:6a89ff6e18268c7ca6fb96e3c6c7f61113ccd85e3b0176d3b84628ddeffb83c0` |
| Windows OpenVINO supplement | PASS | run `36089930047` |
| Photo subject selection | PASS | Source now passes the approved command-derived point to SAM; actual PC overlay selects the person at `[125,145]`, not the wall/sign. |
| Intel SISR 4× | PASS | Adapter now composes the Open Model Zoo residual with bicubic input. Actual PC 1920×1080 output is non-black; SHA-256 `4806a7ab40db3cf8dabec2451ee58015c70e662834643389ae8b6d4684c9d35f`. |
| Approved UI remote E2E | PASS | run `36089930046`; evidence artifact `10845352093`, digest `sha256:070339b42d06b6ba0b9818e996e8976f3322b1199cf8f63c2990c927e18aae7f`. All four actual CPU jobs, Preview, Save, and Export passed. |

## PC-local evidence

The retained PC materialization verified the former package's three archive digests, reassembled package SHA-256 `f80ca743a482f4ad3636f5ed73ba66a32d1d43e649a882154d980334b9965ea2`, exact SAM 2.1, Whisper-small, Intel SISR XML/BIN, and a Windows OpenVINO 2025.1 CPU runtime. Intel SISR compiled on CPU and produced the reviewed non-black photo.

After that successful photo run, a newly spawned PC Python process reproducibly ended during `import torch` (diagnostic reached `numpy-loaded`, not `torch-loaded`). Video tracking and Korean STT were therefore not falsely promoted from process status or remote evidence. The PC-local approved-UI Preview→Save→Export replay at the latest source is likewise outstanding.

See `evidence/pc_remote/MINDLE_MEDIA_AI_PC_FINAL_QUALITY_E2E_EVIDENCE_v30_20260925.json` and the next directive for the bounded recovery sequence.
