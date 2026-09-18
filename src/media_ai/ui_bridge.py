"""Bridge fixed UI command state to the existing media job contract."""
from pathlib import Path, PureWindowsPath

from .contracts import MediaJob
from .router import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS, route
from .ui_contract import normalize_reference_files


def command_to_job(
    command: str,
    input_path: Path,
    reference_files: list[str] | None = None,
    project_id: str | None = None,
    output_target: Path | None = None,
    requested_operation: str | None = None,
) -> MediaJob:
    """Create a routed job without exposing model choices in the UI contract."""
    cleaned = command.strip()
    if not cleaned:
        raise ValueError("A natural-language command is required")
    source = Path(input_path)
    if not source.is_file():
        raise ValueError(f"Source asset is unavailable: {source}")
    if source.suffix.lower() not in PHOTO_EXTENSIONS | VIDEO_EXTENSIONS:
        raise ValueError(f"Unsupported source asset: {source.name}")
    for reference in reference_files or []:
        supplied_path = Path(reference)
        if (supplied_path.is_absolute() or PureWindowsPath(str(reference)).is_absolute()) and not supplied_path.is_file():
            raise ValueError(f"Reference asset is unavailable: {reference}")
    references = normalize_reference_files(reference_files)
    return MediaJob(
        request=cleaned,
        input_path=source,
        media_type=route(cleaned, source),
        options={"reference_files": references},
        project_id=project_id,
        output_target=output_target,
        requested_operation=requested_operation,
        reference_files=references,
    )
