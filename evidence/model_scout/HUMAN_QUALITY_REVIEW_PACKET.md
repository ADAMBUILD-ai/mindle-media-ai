# MINDLE MEDIA AI Human Quality Review Packet

## Purpose and decision rule

This packet supports a human reviewer in deciding whether the technically verified
model outputs are suitable for a KEEP recommendation. It records no automated
or inferred human decision. Until every required review row is completed, all
model adapters remain disabled.

Use `PASS`, `FAIL`, or `REVIEW_REQUIRED` for each row. A final KEEP decision
requires five completed fixture reviews with no repeated structural distortion
or fabricated detail and a documented improvement over the named baseline.

## Super resolution review

Compare each input, `Lanczos4 4x`, and `Real ESRGAN 4x` image side by side in
`model_scout/artifacts/realesrgan_qualcomm/benchmark/`.

| Fixture | Required comparison files | Review status | Defect type | Reviewer note |
| --- | --- | --- | --- | --- |
| 01 | `01_input_128.png`, `01_lanczos4_4x.png`, `01_realesrgan_4x.png` | REVIEW_REQUIRED |  |  |
| 02 | `02_input_128.png`, `02_lanczos4_4x.png`, `02_realesrgan_4x.png` | REVIEW_REQUIRED |  |  |
| 03 | `03_input_128.png`, `03_lanczos4_4x.png`, `03_realesrgan_4x.png` | REVIEW_REQUIRED |  |  |
| 04 | `04_input_128.png`, `04_lanczos4_4x.png`, `04_realesrgan_4x.png` | REVIEW_REQUIRED |  |  |
| 05 | `05_input_128.png`, `05_lanczos4_4x.png`, `05_realesrgan_4x.png` | REVIEW_REQUIRED |  |  |

Check window frames, railings, columns, straight vertical and horizontal lines,
signage or lettering, stone, timber, glass, grass texture, halo or ringing,
over-sharpening, and hallucinated detail. Current technical state:
`ACTUAL_WEIGHT_INFERENCE_FIVE_FIXTURES_COMPLETE` and `HUMAN_REVIEW_REQUIRED`.

## Segment anything review

Review the five masks in `model_scout/artifacts/sam21_live/` against their
fixture sources recorded in `result.json`. For each fixture, record object
selection, boundary omission or spill, and impact on architectural structure.
Final recommendation: `KEEP` or `REPLACE` only after all five rows are filled.

| Fixture | Mask | Review status | Defect type | Reviewer note |
| --- | --- | --- | --- | --- |
| 01 | `01_42756291_mask.png` | REVIEW_REQUIRED |  |  |
| 02 | `02_39871464_mask.png` | REVIEW_REQUIRED |  |  |
| 03 | `03_33975416_mask.png` | REVIEW_REQUIRED |  |  |
| 04 | `04_44272315_mask.png` | REVIEW_REQUIRED |  |  |
| 05 | `05_46280980_mask.png` | REVIEW_REQUIRED |  |  |

## Inpainting review

Compare each LaMa output with its TELEA baseline in
`model_scout/artifacts/lama_live/`. Check architectural lines, joints, windows,
colour artefacts, and texture continuity.

| Fixture | Required comparison files | Review status | Defect type | Reviewer note |
| --- | --- | --- | --- | --- |
| 01 | `01_input.png`, `01_mask.png`, `01_lama.png`, `01_telea.png` | REVIEW_REQUIRED |  |  |
| 02 | `02_input.png`, `02_mask.png`, `02_lama.png`, `02_telea.png` | REVIEW_REQUIRED |  |  |
| 03 | `03_input.png`, `03_mask.png`, `03_lama.png`, `03_telea.png` | REVIEW_REQUIRED |  |  |
| 04 | `04_input.png`, `04_mask.png`, `04_lama.png`, `04_telea.png` | REVIEW_REQUIRED |  |  |
| 05 | `05_input.png`, `05_mask.png`, `05_lama.png`, `05_telea.png` | REVIEW_REQUIRED |  |  |

## Remaining closure inputs

- Whisper needs at least three licensed Korean speech recordings, transcripts
  where available, and human timestamp/omission/error review. The silent-input
  smoke test is not a speech-quality result.
- Matting remains `SOURCE_REVIEW_REJECT` for BiRefNet. A safe, commercially
  usable replacement candidate needs provenance review before any actual smoke
  inference; otherwise retain GrabCut as a non-production fallback.
- The UI SSOT stays `BLOCKED_SOURCE_ASSET_NOT_PRESENT` until the approved
  original asset is supplied. Do not substitute regenerated imagery.
