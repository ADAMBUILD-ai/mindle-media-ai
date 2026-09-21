# PC Remote Final Checklist

This is the only remaining PC-side scope. Work-side contracts, placeholder
evidence schemas, UI state behaviour, and regression checks are already in the
repository. Do not replace them with local copies.

| Task | Input location and command | Expected output and PASS condition | Evidence location | Failure diagnosis |
|---|---|---|---|---|
| Establish baseline | checkout `integration`, run `./run_tests.sh` from the workspace root | all Python, evidence-sync, and Node checks pass; record `git rev-parse HEAD` | `evidence/pc_remote/baseline/` | test failure = return code issue to Work; checkout/path mismatch = PC setup issue |
| Licensed PHOTO F1-F6 | add six owned/licensed architecture images with source and use metadata | before/after outputs exist and reviewer records SR, mask, inpaint and matting quality | `evidence/pc_remote/photo/` | bad output = model/adapter review; unreadable input = fixture issue |
| Licensed Korean audio | add at least three recordings, source/license and reference transcripts | transcript, timestamps, runtime, WER or human omission/substitution/drift review; three editing commands checked | `evidence/pc_remote/whisper_ko/` | model quality/result issue returns to Work; missing consent/license is fixture blocker |
| Video E2E | five or more owned/licensed clips; exercise timeline, split, range delete, subtitles, reframe, audio, export | each project opens, edits, saves and exports a real file | `evidence/pc_remote/video/` | UI interaction issue returns to Work; codec/device issue = PC environment |
| Local runtime | run local GPU/CPU, FFmpeg, ONNX Runtime and PyTorch checks | version, resource, latency, failure and fallback route captured | `evidence/pc_remote/runtime/` | missing driver/library = PC environment; fallback not shown = Work code issue |
| Browser UI | open `ui/index.html` using the approved original SSOT asset | approved geometry/colors/panel ratio; natural language focus/Enter/error/reference/remove/save/export verified | `evidence/pc_remote/browser/` | asset mismatch = source asset blocker; interaction failure = Work code issue |
| Real file actions | use both video and photo editors | project save and export create different real artifacts | `evidence/pc_remote/files/` | no file or same action result = Work code issue |

Before final reporting, keep the UI asset unpinned unless the approved original
file is present. Record its path, SHA-256 and approval date only after the
original is supplied. Do not merge `main` or deploy production.
