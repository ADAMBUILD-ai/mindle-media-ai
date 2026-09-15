# Hugging Face Model Gate

| Capability | Candidate | Current decision | Required next gate | Fallback |
|---|---|---|---|---|
| Object mask and tracking | SAM 2.1 Hiera Base Plus | VERIFY_REQUIRED | Restore the pinned weight, verify source/license, then run isolated inference | OpenCV GrabCut |
| Object removal | LaMa ONNX | VERIFY_REQUIRED | Run offline local smoke; remote revision/license still needs verification | OpenCV TELEA |
| Korean subtitles | Whisper Large v3 Turbo | VERIFY_REQUIRED | Restore pinned weight and use three licensed Korean recordings | Manual subtitles / FFmpeg path |
| Super resolution | Qualcomm Real-ESRGAN x4plus ONNX | VERIFY_REQUIRED | Restore pinned weight, verify license, run isolated inference and human review | OpenCV Lanczos4 |
| Background separation | BiRefNet | REJECT | Do not execute; restart safe-loader scouting when Hub access is restored | OpenCV GrabCut |

No candidate is promoted to `adapter_enabled=true` by this document. Hub access is
currently blocked with `WinError 10013`; authentication is also not active.
