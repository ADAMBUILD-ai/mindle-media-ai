"""Non-visual interaction contract for the fixed MINDLE MEDIA AI UI."""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


MAX_REFERENCE_IMAGES = 5
IMAGE_REFERENCE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def normalize_reference_files(reference_files: list[str] | None) -> list[str]:
    """Return safe, supported reference-image filenames for a command payload."""
    references = list(reference_files or [])
    if len(references) > MAX_REFERENCE_IMAGES:
        raise ValueError(f"A maximum of {MAX_REFERENCE_IMAGES} reference images is allowed")

    normalized: list[str] = []
    seen: set[str] = set()
    for reference in references:
        filename = str(reference).strip().replace("\\", "/").rsplit("/", 1)[-1]
        if not filename:
            raise ValueError("A reference image filename is required")
        if Path(filename).suffix.lower() not in IMAGE_REFERENCE_SUFFIXES:
            raise ValueError("Reference files must be JPG, PNG, WEBP, or TIFF images")
        identity = filename.casefold()
        if identity in seen:
            raise ValueError("Each reference image may be attached only once")
        seen.add(identity)
        normalized.append(filename)
    return normalized


class CommandPhase(str, Enum):
    COLLAPSED = "collapsed"
    EXPANDED = "expanded"
    EXECUTING = "executing"


@dataclass
class CommandState:
    phase: CommandPhase = CommandPhase.COLLAPSED
    text: str = ""
    reference_files: list[str] = field(default_factory=list)
    max_references: int = MAX_REFERENCE_IMAGES

    def focus(self) -> None:
        if self.phase != CommandPhase.EXECUTING:
            self.phase = CommandPhase.EXPANDED

    def attach_reference(self, filename: str) -> None:
        self.focus()
        if len(self.reference_files) >= self.max_references:
            raise ValueError(f"A maximum of {self.max_references} reference images is allowed")
        if self.max_references != MAX_REFERENCE_IMAGES:
            candidate = [*self.reference_files, filename]
            if len(candidate) > self.max_references:
                raise ValueError(f"A maximum of {self.max_references} reference images is allowed")
            self.reference_files = normalize_reference_files(candidate)
            return
        self.reference_files = normalize_reference_files([*self.reference_files, filename])

    def submit(self) -> dict:
        if not self.text.strip():
            raise ValueError("A natural-language command is required before submission")
        self.phase = CommandPhase.EXECUTING
        return {"command": self.text.strip(), "references": list(self.reference_files)}

    def complete(self) -> None:
        self.phase = CommandPhase.COLLAPSED
        self.text = ""
        self.reference_files.clear()

    def fail(self) -> None:
        self.phase = CommandPhase.EXPANDED


@dataclass
class MediaUiContract:
    """Video and photo command states must stay independent."""
    video_command: CommandState = field(default_factory=CommandState)
    photo_command: CommandState = field(default_factory=CommandState)
