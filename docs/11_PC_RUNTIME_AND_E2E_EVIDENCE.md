# PC Runtime and E2E Evidence

## Canonical baseline — 2026-09-15

On branch `work/pc-runtime-e2e-evidence-20260915`, based on recovery commit
`3cf99a6488817836bc46e683ddc506c05bc667b3`:

| Check | Result | Evidence command |
|---|---|---|
| Python regression | `11 passed` | `python -m pytest -q` |
| Evidence sync | PASS | `python model_scout/validate_evidence_sync.py` |
| UI structure and interaction | `2 passed` | `node --test ui/interaction.test.js ui/ssot_structure.test.js` |
| Package completeness | PASS | `python model_scout/validate_package_manifest.py --source` |

`run_tests.sh` cannot be used by this Windows runtime because no compatible Bash
service is available. The four explicit canonical commands above are the
equivalent, passing baseline.

## Runtime capture

Run the following before any PC-only test session:

```powershell
python model_scout/capture_pc_runtime.py --output evidence/pc_remote/runtime/runtime_inventory.json
```

The capture is informational only. It does not download, load, or enable a
model adapter.

## Current blockers

- UI SSOT source image/source is absent. Keep `ui/ssot_manifest.json` blocked;
  do not infer geometry or pin a substitute.
- No owned/licensed PHOTO F1–F6, VIDEO 5+, or Korean speech recordings and
  reference transcripts were supplied. No human review or production E2E result
  may be fabricated.
- FFmpeg is not on this PC's PATH. VIDEO import, timeline edit, subtitle,
  reframe, audio, and export E2E remain blocked until an approved FFmpeg install
  is available.
- BiRefNet remains rejected; only the existing GrabCut fallback is available.

## Evidence destinations after inputs are supplied

- `evidence/pc_remote/photo/` — source license record, input/output hashes,
  reviewer decision for PHOTO F1–F6.
- `evidence/pc_remote/video/` — five project files, edit logs, exports, and
  natural-language/reference-image verification.
- `evidence/pc_remote/whisper_ko/` — recording consent/license, reference
  transcript, timestamps, error review, and KEEP/REPLACE decision.
- `evidence/pc_remote/browser/` — approved asset SHA-256, approval date,
  screenshot regression, and geometry assertion.
