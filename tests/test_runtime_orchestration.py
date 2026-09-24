from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from PIL import Image

from media_ai.contracts import JobState, MediaJob, MediaType
from media_ai.runtime_orchestration import PreflightStatus, RuntimeOrchestrator, validate_output


def make_photo(path: Path) -> Path:
    Image.new("RGB", (12, 8), "gray").save(path)
    return path


def test_preflight_keeps_each_missing_lane_blocked_independently(tmp_path: Path):
    orchestrator = RuntimeOrchestrator()
    jobs = [
        MediaJob("사진 보정", tmp_path / "missing.jpg", MediaType.PHOTO),
        MediaJob("영상 편집", tmp_path / "missing.mp4", MediaType.VIDEO),
        MediaJob("한국어 받아쓰기", tmp_path / "missing.wav", MediaType.KOREAN_AUDIO),
    ]

    receipts = orchestrator.preflight_many(jobs)

    assert [receipt.status for receipt in receipts] == [PreflightStatus.BLOCKED_INPUT] * 3
    assert [job.state for job in jobs] == [JobState.BLOCKED_INPUT] * 3
    assert all(job.evidence["missing_requirements"] == ["source artifact"] for job in jobs)


def test_partial_input_photo_reaches_preflight_without_waiting_for_other_lanes(tmp_path: Path):
    photo = MediaJob("사진 보정", make_photo(tmp_path / "photo.jpg"), MediaType.PHOTO)
    video = MediaJob("영상 편집", tmp_path / "missing.mp4", MediaType.VIDEO)
    audio = MediaJob("한국어 받아쓰기", tmp_path / "missing.wav", MediaType.KOREAN_AUDIO)

    receipts = RuntimeOrchestrator().preflight_many([photo, video, audio])

    assert receipts[0].status is PreflightStatus.PREFLIGHT_READY
    assert photo.state is JobState.PREFLIGHT_READY
    assert {video.state, audio.state} == {JobState.BLOCKED_INPUT}


def test_unavailable_korean_adapter_is_not_reported_as_runtime_success(tmp_path: Path):
    source = tmp_path / "voice.wav"
    source.write_bytes(b"RIFF-not-a-runtime-result")
    job = MediaJob("한국어 받아쓰기", source, MediaType.KOREAN_AUDIO)

    receipt = RuntimeOrchestrator().preflight(job)

    assert receipt.status is PreflightStatus.MODEL_UNAVAILABLE
    assert job.state is JobState.BLOCKED_MODEL
    assert job.evidence["runtime_status"] == "MODEL_UNAVAILABLE"
    assert job.evidence["evidence_status"] == "VERIFY_REQUIRED"


def test_dispatch_builds_immutable_context_with_ids_hash_and_instruction(tmp_path: Path):
    job = MediaJob("사진 보정", make_photo(tmp_path / "photo.jpg"), MediaType.PHOTO, {"reference_files": ["style.png"]})
    orchestrator = RuntimeOrchestrator()

    orchestrator.preflight(job)
    context = orchestrator.dispatch(job)

    assert job.state is JobState.DISPATCHED
    assert context.job_id == job.id and context.evidence_id == job.evidence_id
    assert context.source_hashes["source"]
    assert context.nl_instruction == "사진 보정"
    with pytest.raises(FrozenInstanceError):
        context.nl_instruction = "mutated"


def test_runtime_state_machine_rejects_illegal_dispatch_transition(tmp_path: Path):
    job = MediaJob("사진 보정", make_photo(tmp_path / "photo.jpg"), MediaType.PHOTO)

    with pytest.raises(ValueError, match="Invalid job transition"):
        job.transition(JobState.DISPATCHED)


def test_cancelled_job_never_transitions_to_success(tmp_path: Path):
    source = make_photo(tmp_path / "photo.jpg")
    output = make_photo(tmp_path / "output.jpg")
    job = MediaJob("사진 보정", source, MediaType.PHOTO)
    orchestrator = RuntimeOrchestrator()
    orchestrator.preflight(job)
    orchestrator.dispatch(job)
    orchestrator.start(job)
    orchestrator.cancel(job)

    with pytest.raises(ValueError, match="running job"):
        orchestrator.complete(job, output)
    assert job.state is JobState.CANCELLED
    assert JobState.SUCCEEDED not in job.state_history


def test_timeout_can_retry_once_but_cancelled_jobs_are_not_retry_eligible(tmp_path: Path):
    job = MediaJob("사진 보정", make_photo(tmp_path / "photo.jpg"), MediaType.PHOTO)
    orchestrator = RuntimeOrchestrator(max_retries=2)
    orchestrator.preflight(job)
    orchestrator.dispatch(job)
    orchestrator.start(job)
    orchestrator.timeout(job, timeout_seconds=5)

    assert job.state is JobState.FAILED
    assert orchestrator.retry(job).status is PreflightStatus.PREFLIGHT_READY
    orchestrator.cancel(job)
    with pytest.raises(ValueError, match="Only failed"):
        orchestrator.retry(job)


def test_output_validation_records_parseable_artifact_and_callback_correlation(tmp_path: Path):
    source = make_photo(tmp_path / "photo.jpg")
    output = make_photo(tmp_path / "output.jpg")
    job = MediaJob("사진 보정", source, MediaType.PHOTO)
    orchestrator = RuntimeOrchestrator()
    orchestrator.preflight(job)
    orchestrator.dispatch(job)
    orchestrator.start(job)

    receipt = orchestrator.complete(job, output)
    callback = orchestrator.accept_model_scout_callback(job, {"job_id": job.id, "evidence_id": job.evidence_id, "status": "TESTED_FAIL"})

    assert receipt.valid
    assert job.state is JobState.SUCCEEDED
    assert job.evidence["output_artifact"]["sha256"]
    assert callback["status"] == "TESTED_FAIL"
    assert job.evidence["evidence_status"] == "VERIFY_REQUIRED"
    with pytest.raises(ValueError, match="does not correlate"):
        orchestrator.accept_model_scout_callback(job, {"job_id": "other", "evidence_id": job.evidence_id, "status": "TESTED_FAIL"})


def test_invalid_output_fails_closed_without_success(tmp_path: Path):
    source = make_photo(tmp_path / "photo.jpg")
    invalid_output = tmp_path / "empty.jpg"
    invalid_output.write_bytes(b"")
    job = MediaJob("사진 보정", source, MediaType.PHOTO)
    orchestrator = RuntimeOrchestrator()
    orchestrator.preflight(job)
    orchestrator.dispatch(job)
    orchestrator.start(job)

    receipt = orchestrator.complete(job, invalid_output)

    assert not receipt.valid
    assert job.state is JobState.FAILED
    assert JobState.SUCCEEDED not in job.state_history
    assert not validate_output(invalid_output, MediaType.PHOTO).valid
