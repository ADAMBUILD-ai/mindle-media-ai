# MINDLE MEDIA AI v29.0 Next Directive

## Objective

Complete the PC-side closeout using the verified v28.1 runtime package. Do not acquire models again unless a file digest fails.

## Required sequence

1. Download artifact parts 00, 01, and 02 from workflow run 35973861998.
2. Reassemble in order and verify the unsplit package SHA-256:
   `93da2189fc37bb42cc60e8335131d2e533440a96c7c6c7e2535dea90834c8a4c`.
3. Extract and verify every manifest file.
4. Install/use free CPU OpenVINO; preserve OpenCV video decode path.
5. Fix and rerun PHOTO adapter mapping, mask selection, overlay transform, and output quality.
6. Fix and rerun UPSCALE adapter dtype/layout/range/channel/PNG path; require non-black true 4x output.
7. Rerun local VIDEO tracking and local Korean STT.
8. Exercise UI flow: input → natural-language instruction/reference image → run → visible status → Preview → original/result compare → save → export → undo/redo.
9. Record before/after outputs, dimensions, file hashes, quality checks, and regression results.

## Protection

UI_SSOT_CHANGED:NO. No redesign, main merge, Production deployment, force push, GPU, paid compute, secret exposure, or overwrite of prior Evidence. If package transfer or a local quality gate fails, record cause → fix → rerun and keep the failure evidence.

## Completion

Publish a v29.0 Evidence JSON and review on the branch, then open/update a Draft PR. Do not claim PC PASS until all local gates pass.
