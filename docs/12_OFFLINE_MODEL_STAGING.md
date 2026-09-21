# Offline Model Staging

`model_scout/stage_verified_model.py` accepts a complete model snapshot that was
acquired through an approved local transfer path. It performs no download and never
uses credentials. It rejects SAM pickle `.pt` weights and promotes a model only after
the fixed repo, revision, required filename, supplied byte size, and SHA-256 agree.

| Model | Fixed revision | Required input | Target |
|---|---|---|---|
| SAM 2.1 Hiera Base Plus | `facebook/sam2.1-hiera-base-plus` | `b7320756a13354e7530a63935656d35b2f91a290` | `model.safetensors` (safe; Hub display: 323 MB) plus `config.json`, `preprocessor_config.json`, `processor_config.json` | `model_scout/artifacts/sam21` |
| Whisper Large v3 Turbo | `openai/whisper-large-v3-turbo` | `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` | `model.safetensors` (safe; Hub display: 1.62 GB) plus `config.json`, `generation_config.json`, `preprocessor_config.json`, `tokenizer.json`, `tokenizer_config.json` | `model_scout/artifacts/whisper_turbo` |
| Qualcomm Real-ESRGAN x4plus | `qualcomm/Real-ESRGAN-x4plus` | `4022efb8b74eb88900724d9e05a468ac3673df4a` | `real_esrgan_x4plus-onnx-float.zip` from the pinned Qualcomm release-assets URL | `model_scout/artifacts/realesrgan_qualcomm/real_esrgan_x4plus-onnx-float` |

After staging, execute the corresponding existing revalidation script. Those scripts
are local-only and fail closed if a required safe snapshot file is absent. Their
output artifacts remain the evidence source for SHA-256, load, inference, runtime,
and output evidence. `UI_SSOT_CHANGED: NO` applies to every staging and validation
change. The transfer record must supply exact byte size and SHA-256 from the source;
rounded Hub display sizes are identifiers only and are not accepted as verification
values. A successful staging record is the only path to `VERIFIED_MODEL_CACHE`.
