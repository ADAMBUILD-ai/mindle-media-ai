# Hugging Face Model Gate

| Capability | Candidate | Current decision | Required next gate | Fallback |
|---|---|---|---|---|
| Object mask and tracking | SAM 2.1 Hiera Base Plus | VERIFY_REQUIRED | Safe `model.safetensors` selected at revision `b7320756a13354e7530a63935656d35b2f91a290`; obtain locally, hash, load, then run isolated inference | OpenCV GrabCut |
| Object removal | LaMa ONNX | GATE_PASS | Local ONNX weight hash, CPU load, and actual inpaint output are recorded in `HF_MODEL_RUNTIME_RESULTS.json` | OpenCV TELEA |
| Korean subtitles | Whisper Large v3 Turbo | VERIFY_REQUIRED | MIT safe `model.safetensors` selected at revision `41f01f3fe87f28c78e2fbf8b568835947dd65ed9`; obtain locally, hash, load, and use three licensed Korean recordings | Manual subtitles / FFmpeg path |
| Super resolution | Qualcomm Real-ESRGAN x4plus ONNX | VERIFY_REQUIRED | BSD-3-Clause source and exact revision verified; resolve the upstream release asset, then hash, load, infer, and review | OpenCV Lanczos4 |
| Background separation | BiRefNet | REJECT | Do not execute; `Xenova/modnet` is scouting-only because its license is unverified. Keep GrabCut until a safe replacement completes all gates | OpenCV GrabCut |

No candidate is promoted to `adapter_enabled=true` by this document. Hub access is
is blocked with `WinError 10013` even though the signed-in browser can reach the Hub.
Browser authentication does not provision the CLI/runtime with a credential or restore its
blocked outbound socket path.
