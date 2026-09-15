# Offline Model Staging

`model_scout/stage_verified_model.py` accepts a complete model snapshot that was
acquired through an approved local transfer path. It performs no download and never
uses credentials. It rejects SAM pickle `.pt` weights, verifies the supplied SHA-256,
and writes a staging manifest before any revalidation is run.

| Model | Fixed revision | Required input | Target |
|---|---|---|---|
| SAM 2.1 Hiera Base Plus | `b7320756a13354e7530a63935656d35b2f91a290` | Snapshot directory with safe `model.safetensors` and required JSON files | `model_scout/artifacts/sam21` |
| Whisper Large v3 Turbo | `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` | Snapshot directory with safe `model.safetensors` and required JSON files | `model_scout/artifacts/whisper_turbo` |
| Qualcomm Real-ESRGAN x4plus | `4022efb8b74eb88900724d9e05a468ac3673df4a` | Qualcomm's fixed ONNX float release ZIP | `model_scout/artifacts/realesrgan_qualcomm/real_esrgan_x4plus-onnx-float` |

After staging, execute the corresponding existing revalidation script. Those scripts
are local-only and fail closed if a required safe snapshot file is absent. Their
output artifacts remain the evidence source for SHA-256, load, inference, runtime,
and output evidence. `UI_SSOT_CHANGED: NO` applies to every staging and validation
change.
