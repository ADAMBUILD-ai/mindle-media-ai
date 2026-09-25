# MINDLE MEDIA AI UI SSOT Final

## Fixed structure

The screen stays dark navy and has two vertically stacked work areas: `영상 편집` above `사진 편집`. Each area preserves left media and AI instruction, center preview or timeline work area, and right editing panel in the approved alignment and proportions.

Both areas use `프로젝트 저장` and `내보내기`. No layout, color, panel placement, or proportion may be inferred or redesigned from this specification.

## Source asset gate

The current source-asset manifest is `../ui/ssot_manifest.json`. It is intentionally `BLOCKED_SOURCE_ASSET_NOT_PRESENT` because neither the official remote nor the supplied package contains the user-approved UI image or source. Pixel-level implementation and screenshot regression start only after the asset is placed in `../ui/assets/ssot/` and its SHA-256 and approval date are recorded.

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
