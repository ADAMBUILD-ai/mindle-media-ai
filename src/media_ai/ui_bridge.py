"""Bridge fixed UI command state to the existing media job contract."""
from pathlib import Path

from .contracts import MediaJob
from .router import route


def command_to_job(command: str, input_path: Path, reference_files: list[str] | None = None) -> MediaJob:
    """Create a routed job without exposing model choices in the UI contract."""
    cleaned = command.strip()
    if not cleaned:
        raise ValueError("A natural-language command is required")
    return MediaJob(
        request=cleaned,
        input_path=input_path,
        media_type=route(cleaned, input_path),
        options={"reference_files": list(reference_files or [])},
    )
