from dataclasses import dataclass
from .contracts import MediaType

@dataclass(frozen=True)
class Step:
    name: str
    provider: str = "local_default_provider"

def plan(media_type: MediaType, request: str, options: dict) -> list[Step]:
    text = request.lower()
    if media_type == MediaType.PHOTO:
        steps = [Step("preserve_original"), Step("photo_adjust")]
        if options.get("width"): steps.append(Step("resize"))
        return steps + [Step("write_result"), Step("write_evidence")]
    steps = [Step("preserve_original")]
    if options.get("clips"): steps.append(Step("concat_clips"))
    if options.get("start") or options.get("duration"): steps.append(Step("cut_segment"))
    if options.get("subtitle"): steps.append(Step("render_subtitle"))
    if options.get("mute"): steps.append(Step("mute_audio"))
    elif options.get("volume") is not None: steps.append(Step("adjust_volume"))
    if "쇼츠" in text or options.get("aspect"): steps.append(Step("reframe"))
    return steps + [Step("encode_h264_aac"), Step("write_evidence")]
