# MINDLE MEDIA AI UI SSOT Final

## Current Owner direction — 2026-10-10, reconciled 2026-10-17

The later Owner instruction takes precedence over the September reference image:
desktop VIDEO stays on the left and PHOTO on the right. PHOTO is landscape-first;
portrait media uses Auto Fit, center placement and its original aspect ratio.
Keep both natural-language input areas reachable, seven PHOTO corrections,
the right editing panels, Shortform, title, colors and existing approved controls.
This reconciliation does not authorize a redesign or claim final visual approval.

See `commander/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_EXECUTION_20261017.md` and
`evidence/media-ai-final-closeout-20261017/UI_AUTHORITY_RECONCILIATION.json`.

## Historical F27E structure

The screen stays dark navy and has two vertically stacked work areas: `영상 편집` above `사진 편집`. Each area preserves left media and AI instruction, center preview or timeline work area, and right editing panel in the approved alignment and proportions.

Both areas use `프로젝트 저장` and `내보내기`. No layout, color, panel placement, or proportion may be inferred or redesigned from this specification.

## Source asset

The historical source-asset manifest is `../ui/ssot_manifest.json`. The exact approved PNG is present at `../ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png`, verified as 1536 × 1024 with SHA-256 `f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541`, approved 2026-09-13. Preserve it as the original reference and provenance. Its stacked geometry does not override the later Owner desktop direction above. It must never be used as a page background or UI overlay.

## Component and state contract

| Component | Required state | Required event | Result |
|---|---|---|---|
| Video AI command | collapsed, expanded, executing | click/input, Enter | expand while editing; submit then collapse |
| Photo AI command | collapsed, expanded, executing | click/input, Enter | expand while editing; submit then collapse |
| Reference upload | idle, selected, uploading, ready, failed | plus button and file selection | preserves selected reference for the command |
| Save | clean, dirty, saving, saved, failed | 프로젝트 저장 | records project state only |
| Export | ready, exporting, complete, failed | 내보내기 | emits a file only after final runtime validation |

The video and photo command fields are independent. Each field must expose `+` and `참고 이미지 추가`.

## Responsive rule

Responsive behavior may reduce density and stack controls only when needed for viewport safety. It must not exchange panel order, replace the two-track hierarchy, or remove either command or reference-upload control.
