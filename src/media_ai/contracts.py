from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from uuid import uuid4

class MediaType(StrEnum):
    PHOTO = "photo"
    VIDEO = "video"

class JobState(StrEnum):
    QUEUED = "queued"
    VALIDATING = "validating"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED_INPUT = "blocked_input"
    BLOCKED_MODEL = "blocked_model"

@dataclass
class MediaJob:
    request: str
    input_path: Path
    media_type: MediaType
    options: dict = field(default_factory=dict)
    project_id: str | None = None
    output_target: Path | None = None
    requested_operation: str | None = None
    reference_files: list[str] = field(default_factory=list)
    source_provenance: dict | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    evidence_id: str = field(default_factory=lambda: str(uuid4()))
    state: JobState = JobState.QUEUED
    state_history: list[JobState] = field(default_factory=lambda: [JobState.QUEUED])
    output_path: Path | None = None
    error: str | None = None
    evidence: dict = field(default_factory=dict)
    attempts: int = 0

    def __post_init__(self) -> None:
        self.input_path = Path(self.input_path)
        if self.output_target is not None:
            self.output_target = Path(self.output_target)
        if self.source_provenance is None:
            self.source_provenance = {"source_path": str(self.input_path)}
        else:
            self.source_provenance = dict(self.source_provenance)
        if not self.reference_files:
            self.reference_files = list(self.options.get("reference_files", []))
        self.options = {**self.options, "reference_files": list(self.reference_files)}

    def transition(self, state: JobState) -> None:
        allowed = {
            JobState.QUEUED: {JobState.VALIDATING},
            JobState.VALIDATING: {JobState.READY, JobState.BLOCKED_INPUT, JobState.BLOCKED_MODEL, JobState.FAILED},
            JobState.READY: {JobState.RUNNING},
            JobState.RUNNING: {JobState.READY, JobState.SUCCEEDED, JobState.FAILED, JobState.BLOCKED_INPUT, JobState.BLOCKED_MODEL},
            JobState.SUCCEEDED: set(),
            JobState.FAILED: {JobState.VALIDATING},
            JobState.BLOCKED_INPUT: {JobState.VALIDATING},
            JobState.BLOCKED_MODEL: {JobState.VALIDATING},
        }
        if state not in allowed[self.state]:
            raise ValueError(f"Invalid job transition: {self.state} -> {state}")
        self.state = state
        self.state_history.append(state)
