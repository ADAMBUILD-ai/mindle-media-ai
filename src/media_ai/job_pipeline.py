"""Non-visual job validation and adapter-boundary selection."""
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath

from .contracts import MediaJob, MediaType
from .router import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS
from .ui_contract import normalize_reference_files


class BlockedInputError(ValueError):
    """Raised when a job cannot start until a real input asset is available."""


class BlockedModelError(RuntimeError):
    """Raised when a requested model-backed operation lacks a verified adapter."""


@dataclass(frozen=True)
class ExecutionBoundary:
    operation: str
    adapter_id: str
    model_or_program_id: str
    revision: str | None
    license_source: str


PHOTO_BOUNDARIES = {
    "object_removal": ExecutionBoundary("object_removal", "photo_inpaint_boundary", "opencv/inpainting_lama", "aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f", "pending runtime verification"),
    "restore_upscale": ExecutionBoundary("restore_upscale", "photo_upscale_boundary", "qualcomm/Real-ESRGAN-x4plus", "4022efb8b74eb88900724d9e05a468ac3673df4a", "pending runtime verification"),
    "photo_adjust": ExecutionBoundary("photo_adjust", "pillow_opencv_boundary", "Pillow OpenCV", None, "local program dependency"),
}
VIDEO_BOUNDARIES = {
    "tracking": ExecutionBoundary("tracking", "video_tracking_boundary", "facebook/sam2.1-hiera-base-plus", "b7320756a13354e7530a63935656d35b2f91a290", "pending runtime verification"),
    "mask": ExecutionBoundary("mask", "video_mask_boundary", "facebook/sam2.1-hiera-base-plus", "b7320756a13354e7530a63935656d35b2f91a290", "pending runtime verification"),
    "interpolation": ExecutionBoundary("interpolation", "video_interpolation_boundary", "ffmpeg", None, "local program dependency"),
    "stabilization": ExecutionBoundary("stabilization", "video_stabilization_boundary", "ffmpeg", None, "local program dependency"),
    "video_edit": ExecutionBoundary("video_edit", "ffmpeg_video_boundary", "ffmpeg", None, "local program dependency"),
}


def requested_operation(job: MediaJob) -> str:
    if job.requested_operation:
        return job.requested_operation
    text = job.request.lower()
    if job.media_type is MediaType.PHOTO:
        if job.options.get("object_remove") or any(token in text for token in ("object removal", "remove object", "객체 제거", "객체를", "지워")):
            return "object_removal"
        if job.options.get("upscale") or any(token in text for token in ("upscale", "restore", "복원", "업스케일")):
            return "restore_upscale"
        return "photo_adjust"
    if job.options.get("tracking") or any(token in text for token in ("tracking", "track", "트래킹", "추적")):
        return "tracking"
    if job.options.get("mask") or any(token in text for token in ("mask", "마스크")):
        return "mask"
    if job.options.get("interpolation") or any(token in text for token in ("interpolation", "보간")):
        return "interpolation"
    if job.options.get("stabilization") or any(token in text for token in ("stabilization", "stabilize", "안정화")):
        return "stabilization"
    return "video_edit"


def validate_job(job: MediaJob) -> ExecutionBoundary:
    if not job.request.strip():
        raise BlockedInputError("A natural-language command is required")
    operation = requested_operation(job)
    job.requested_operation = operation
    if not job.input_path.is_file():
        raise BlockedInputError(f"Source asset is unavailable: {job.input_path}")
    if job.input_path.stat().st_size == 0:
        raise BlockedInputError(f"Source asset is empty: {job.input_path}")
    if not job.source_provenance or job.source_provenance.get("source_path") != str(job.input_path):
        raise BlockedInputError("Source provenance is required and must match the source asset")

    allowed_extensions = PHOTO_EXTENSIONS if job.media_type is MediaType.PHOTO else VIDEO_EXTENSIONS
    if job.input_path.suffix.lower() not in allowed_extensions:
        raise BlockedInputError(f"Unsupported {job.media_type.value} source asset: {job.input_path.name}")

    for reference in job.reference_files:
        supplied_path = Path(reference)
        if (supplied_path.is_absolute() or PureWindowsPath(str(reference)).is_absolute()) and not supplied_path.is_file():
            raise BlockedInputError(f"Reference asset is unavailable: {reference}")
    job.reference_files = normalize_reference_files(job.reference_files)
    job.options["reference_files"] = list(job.reference_files)
    boundaries = PHOTO_BOUNDARIES if job.media_type is MediaType.PHOTO else VIDEO_BOUNDARIES
    if operation not in boundaries:
        raise BlockedInputError(f"Unsupported {job.media_type.value} operation: {operation}")
    boundary = boundaries[operation]
    if job.options.get("requires_verified_model") and boundary.revision and not job.options.get("verified_model"):
        raise BlockedModelError(f"Verified model is required for {operation}: {boundary.model_or_program_id}")
    return boundary
