from pathlib import Path

import pytest

from media_ai.contracts import JobState, MediaJob, MediaType
from media_ai.job_queue import JobQueue


def test_queue_deduplicates_and_cancels_before_execution():
    queue = JobQueue()
    first = MediaJob("밝게 보정해줘", Path("source.jpg"), MediaType.PHOTO)
    duplicate = MediaJob("밝게 보정해줘", Path("source.jpg"), MediaType.PHOTO)

    assert queue.enqueue(first) is first
    assert queue.enqueue(duplicate) is first
    assert queue.dequeue() is first
    assert queue.cancel_before_run(first).state is JobState.CANCELLED
    assert queue.dequeue() is None


def test_queue_rejects_late_cancellation_and_limits_retry_to_failures():
    queue = JobQueue()
    job = MediaJob("밝게 보정해줘", Path("source.jpg"), MediaType.PHOTO)
    job.transition(JobState.VALIDATING)

    with pytest.raises(ValueError, match="Only queued"):
        queue.cancel_before_run(job)

    job.transition(JobState.FAILED)
    assert queue.retry_eligible(job)
    job = MediaJob("밝게 보정해줘", Path("source.jpg"), MediaType.PHOTO)
    job.transition(JobState.CANCELLED)
    assert not queue.retry_eligible(job)
