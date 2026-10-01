"""In-memory queue contract for non-visual media job orchestration."""
from collections import deque

from .contracts import JobState, MediaJob


class JobQueue:
    def __init__(self) -> None:
        self._jobs_by_key: dict[str, MediaJob] = {}
        self._pending: deque[str] = deque()

    def enqueue(self, job: MediaJob) -> MediaJob:
        existing = self._jobs_by_key.get(job.idempotency_key)
        if existing is not None:
            return existing
        self._jobs_by_key[job.idempotency_key] = job
        self._pending.append(job.idempotency_key)
        return job

    def dequeue(self) -> MediaJob | None:
        while self._pending:
            key = self._pending.popleft()
            job = self._jobs_by_key[key]
            if job.state is JobState.QUEUED:
                return job
        return None

    def cancel_before_run(self, job: MediaJob) -> MediaJob:
        if job.state is not JobState.QUEUED:
            raise ValueError("Only queued jobs may be cancelled")
        job.transition(JobState.CANCELLED)
        return job

    @staticmethod
    def retry_eligible(job: MediaJob) -> bool:
        return job.state is JobState.FAILED
