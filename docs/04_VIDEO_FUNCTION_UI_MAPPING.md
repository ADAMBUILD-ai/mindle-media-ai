# VIDEO Function UI Mapping

| Capability | Fixed UI location | Interaction contract | Evidence |
|---|---|---|---|
| Preview and clip selection | center preview and timeline | select one clip without losing timeline context | selection state test |
| Split, trim and delete | clip context toolbar | split at playhead; delete before, after or selection | timeline manifest |
| Multi-track | timeline | video, audio, subtitle and overlay tracks stay independently addressable | track state test |
| Mask and background | right panel | mask selected clip or region | mask artifact |
| Keyframe and transform | right panel and timeline | transform state is keyframeable | keyframe contract test |
| Subtitle, audio, reframe and export | right panel | changes remain previewable before export | E2E output manifest |

Adopt these workflows without copying any reference app's visual design, subscription flow, advertising, or sales UI.
