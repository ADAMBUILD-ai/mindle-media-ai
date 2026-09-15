"""Non-visual interaction contract for the fixed MINDLE MEDIA AI UI."""
from dataclasses import dataclass, field
from enum import Enum


class CommandPhase(str, Enum):
    COLLAPSED = "collapsed"
    EXPANDED = "expanded"
    EXECUTING = "executing"


@dataclass
class CommandState:
    phase: CommandPhase = CommandPhase.COLLAPSED
    text: str = ""
    reference_files: list[str] = field(default_factory=list)
    max_references: int = 5

    def focus(self) -> None:
        if self.phase != CommandPhase.EXECUTING:
            self.phase = CommandPhase.EXPANDED

    def attach_reference(self, filename: str) -> None:
        self.focus()
        if len(self.reference_files) >= self.max_references:
            raise ValueError(f"A maximum of {self.max_references} reference images is allowed")
        self.reference_files.append(filename)

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
