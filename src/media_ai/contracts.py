from dataclasses import dataclass, field
from enum import StrEnum
import hashlib
import json
from pathlib import Path
from uuid import uuid4

class MediaType(StrEnum):
    PHOTO = "photo"
    VIDEO = "video"
    KOREAN_AUDIO = "korean_audio"

class JobState(StrEnum):
    QUEUED = "queued"
    VALIDATING = "validating"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED_INPUT = "blocked_input"
    BLOCKED_MODEL = "blocked_model"
    CANCELLED = "cancelled"
    PREFLIGHT_READY = "preflight_ready"
    DISPATCHED = "dispatched"
    OUTPUT_VALIDATING = "output_validating"

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
    idempotency_key: str | None = None
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
        if self.idempotency_key is None:
            payload = {
                "request": self.request,
                "input_path": str(self.input_path),
                "media_type": self.media_type,
                "project_id": self.project_id,
                "output_target": str(self.output_target) if self.output_target else None,
                "reference_files": self.reference_files,
                "source_provenance": self.source_provenance,
            }
            self.idempotency_key = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    def transition(self, state: JobState) -> None:
        allowed = {
            JobState.QUEUED: {JobState.VALIDATING, JobState.CANCELLED},
            JobState.VALIDATING: {JobState.READY, JobState.PREFLIGHT_READY, JobState.BLOCKED_INPUT, JobState.BLOCKED_MODEL, JobState.FAILED, JobState.CANCELLED},
            JobState.READY: {JobState.RUNNING, JobState.CANCELLED},
            JobState.PREFLIGHT_READY: {JobState.DISPATCHED, JobState.CANCELLED},
            JobState.DISPATCHED: {JobState.RUNNING, JobState.CANCELLED},
            JobState.RUNNING: {JobState.READY, JobState.OUTPUT_VALIDATING, JobState.SUCCEEDED, JobState.FAILED, JobState.BLOCKED_INPUT, JobState.BLOCKED_MODEL, JobState.CANCELLED},
            JobState.OUTPUT_VALIDATING: {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED},
            JobState.SUCCEEDED: set(),
            JobState.FAILED: {JobState.VALIDATING},
            JobState.BLOCKED_INPUT: {JobState.VALIDATING},
            JobState.BLOCKED_MODEL: {JobState.VALIDATING},
            JobState.CANCELLED: set(),
        }
        if state not in allowed[self.state]:
            raise ValueError(f"Invalid job transition: {self.state} -> {state}")
        self.state = state
        self.state_history.append(state)
