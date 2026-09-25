# Model Scout Validation Matrix

`evidence/model_scout/registry.json` is the status SSOT. No adapter is enabled before the production quality gate.

| Capability | Candidate and pinned revision | Current evidence | Decision | Remaining gate |
|---|---|---|---|---|
| Mask and tracking | SAM 2.1 Hiera Base Plus `facebook/sam2.1-hiera-base-plus` `b7320756a13354e7530a63935656d35b2f91a290` | Five CC/PD architecture fixtures, input/mask SHA-256 and CPU latency in `model_scout/artifacts/sam21_live/result.json` | `LIVE_FUNCTIONAL_BENCHMARK_COMPLETE`; adapter disabled; GrabCut fallback | Human review of object selection and edge defects, then KEEP or REPLACE |
| Inpaint | LaMa ONNX `opencv/inpainting_lama` `aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f` | Five CC/PD architecture fixtures, pinned model hash, LaMa/TELEA A/B outputs and latency in `model_scout/artifacts/lama_live/result.json` | `LIVE_FUNCTIONAL_BENCHMARK_COMPLETE`; adapter disabled; TELEA fallback | Human review of lines, texture and color artifacts, then KEEP or REPLACE |
| Korean subtitles | Whisper Large v3 Turbo `openai/whisper-large-v3-turbo` `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` | Weight-load/generation technical smoke on a silent 10-second WAV | `TECHNICAL_SMOKE_PASS`; adapter disabled; FFmpeg path only | Three or more licensed Korean utterances with transcript, timestamps and accuracy review |
| Super resolution | Qualcomm Real-ESRGAN x4plus `qualcomm/Real-ESRGAN-x4plus` `4022efb8b74eb88900724d9e05a468ac3673df4a` | ONNX weight/data SHA-256, actual inference and Lanczos4 4x A/B outputs for five public architecture fixtures in `model_scout/artifacts/realesrgan_qualcomm/benchmark/result.json` | `ACTUAL_WEIGHT_INFERENCE_FIVE_FIXTURES_COMPLETE`; `HUMAN_REVIEW_REQUIRED`; adapter disabled; Lanczos4 fallback | Human review of straight lines, text, texture and hallucinated detail for all five fixtures before KEEP |
| Matting | BiRefNet `ZhengPeng7/BiRefNet` `e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4` | Source review documents dynamic `eval`, `torch.load` and a network-capable handler | `SOURCE_REVIEW_REJECT`; adapter disabled; GrabCut fallback | Scout three safe-loader alternatives and smoke at least one alpha-edge candidate |

All published artifact results retain `VERIFY_REQUIRED` until a human review and the full production approval gate are completed.
