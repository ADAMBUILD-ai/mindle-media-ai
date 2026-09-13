from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from uuid import uuid4

class MediaType(StrEnum):
    PHOTO = "photo"
    VIDEO = "video"

class JobState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RETRY = "retry"

@dataclass
class MediaJob:
    request: str
    input_path: Path
    media_type: MediaType
    options: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    state: JobState = JobState.QUEUED
    output_path: Path | None = None
    error: str | None = None
    evidence: dict = field(default_factory=dict)
    attempts: int = 0
