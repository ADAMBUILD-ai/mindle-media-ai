from pathlib import Path
from .contracts import MediaType

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}

def route(request: str, input_path: Path) -> MediaType:
    ext = input_path.suffix.lower()
    if ext in PHOTO_EXTENSIONS: return MediaType.PHOTO
    if ext in VIDEO_EXTENSIONS: return MediaType.VIDEO
    lowered = request.lower()
    if any(word in lowered for word in ("영상", "쇼츠", "자막", "컷", "video")): return MediaType.VIDEO
    return MediaType.PHOTO
