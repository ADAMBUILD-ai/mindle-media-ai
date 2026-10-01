# PHOTO Function UI Mapping

| Core capability | UI entry point | Right panel control | Natural-language command | Evidence |
|---|---|---|---|---|
| Vertical and perspective correction | photo preview | Geometry | straighten facade and verticals | before and after image |
| Lens correction | photo preview | Lens | correct wide-angle distortion | parameter log |
| Denoise and upscale | photo preview | Enhance | reduce noise and improve resolution | output and rollback |
| Inpaint | photo preview and reference image | Repair | remove selected object and restore background | mask, input, output |
| Background and masking | photo preview | Mask and background | select subject or replace background | mask and output |
| Batch and before-after | photo list | Batch | apply the same approved adjustment | batch manifest and preview |

All model calls route through internal adapters. User-visible UI must describe the action, not a model name.
