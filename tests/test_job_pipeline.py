from pathlib import Path

from PIL import Image

from media_ai.contracts import JobState, MediaJob, MediaType
from media_ai.job_pipeline import validate_job
from media_ai.runtime import MediaRuntime
from media_ai.ui_bridge import command_to_job


def test_photo_job_preserves_common_command_contract_and_evidence_hook(tmp_path: Path):
    source = tmp_path / "facade.jpg"
    reference = tmp_path / "style.png"
    output = tmp_path / "result.jpg"
    Image.new("RGB", (16, 12), "gray").save(source)
    Image.new("RGB", (16, 12), "gray").save(reference)

    job = command_to_job(
        "사진을 밝게 보정해줘",
        source,
        [str(reference)],
        project_id="project-17",
        output_target=output,
    )
    result = MediaRuntime(tmp_path / "workspace").submit(job)

    assert result.state is JobState.SUCCEEDED
    assert result.state_history == [JobState.QUEUED, JobState.VALIDATING, JobState.READY, JobState.RUNNING, JobState.SUCCEEDED]
    assert result.requested_operation == "photo_adjust"
    assert result.reference_files == ["style.png"]
    assert result.output_path == output
    assert result.evidence["project_id"] == "project-17"
    assert result.evidence["evidence_status"] == "VERIFY_REQUIRED"
    assert result.evidence["model_or_program_id"] == "Pillow OpenCV"
    assert result.evidence["input_sha256"] and result.evidence["output_sha256"]
    assert "TESTED_PASS" not in result.evidence.values()


def test_missing_input_is_blocked_without_discarding_command_or_references(tmp_path: Path):
    job = MediaJob(
        "객체를 지워줘",
        tmp_path / "missing.jpg",
        MediaType.PHOTO,
        {"reference_files": ["style.png"]},
    )
    result = MediaRuntime(tmp_path / "workspace").submit(job)

    assert result.state is JobState.BLOCKED_INPUT
    assert result.request == "객체를 지워줘"
    assert result.requested_operation == "object_removal"
    assert result.reference_files == ["style.png"]
    assert result.evidence["evidence_status"] == "BLOCKED_INPUT"


def test_unverified_model_request_is_blocked_without_a_false_success(tmp_path: Path):
    source = tmp_path / "facade.jpg"
    Image.new("RGB", (16, 12), "gray").save(source)
    job = MediaJob(
        "객체 제거",
        source,
        MediaType.PHOTO,
        {"object_remove": True, "requires_verified_model": True},
    )
    result = MediaRuntime(tmp_path / "workspace").submit(job)

    assert result.state is JobState.BLOCKED_MODEL
    assert result.evidence["runtime_status"] == "BLOCKED_MODEL"
    assert result.output_path is None


def test_video_fixture_validates_contract_and_records_a_failure_path(tmp_path: Path):
    source = tmp_path / "fixture.mp4"
    source.write_bytes(b"deterministic-invalid-video-fixture")
    job = command_to_job("대상을 추적해줘", source, requested_operation="tracking")

    boundary = validate_job(job)
    result = MediaRuntime(tmp_path / "workspace").submit(job, retries=0)

    assert boundary.adapter_id == "video_tracking_boundary"
    assert result.state is JobState.FAILED
    assert result.state_history == [JobState.QUEUED, JobState.VALIDATING, JobState.READY, JobState.RUNNING, JobState.FAILED]
    assert result.evidence["evidence_status"] == "VERIFY_REQUIRED"
    assert (tmp_path / "workspace" / "logs" / f"{job.id}.json").exists()


def test_retry_preserves_command_and_reference_selection(tmp_path: Path):
    source = tmp_path / "fixture.mp4"
    source.write_bytes(b"deterministic-invalid-video-fixture")
    job = MediaJob("영상을 안정화해줘", source, MediaType.VIDEO, {"reference_files": ["style.png"]})
    runtime = MediaRuntime(tmp_path / "workspace")
    evidence_id = job.evidence_id

    failed = runtime.submit(job, retries=0)
    retried = runtime.retry(job.id, retries=0)

    assert failed.state is JobState.FAILED
    assert retried.state is JobState.FAILED
    assert retried.request == "영상을 안정화해줘"
    assert retried.reference_files == ["style.png"]
    assert retried.attempts == 2
    assert retried.evidence_id == evidence_id
    assert retried.evidence["retry_provenance"] == {"job_id": job.id, "evidence_id": evidence_id, "attempt": 2}


def test_duplicate_successful_submission_reuses_job_and_evidence(tmp_path: Path):
    source = tmp_path / "facade.jpg"
    Image.new("RGB", (16, 12), "gray").save(source)
    job = command_to_job("사진을 밝게 보정해줘", source)
    runtime = MediaRuntime(tmp_path / "workspace")

    first = runtime.submit(job)
    second = runtime.submit(job)

    assert first is second
    assert second.state is JobState.SUCCEEDED
    assert second.attempts == 1
    assert second.evidence["job_id"] == job.id
    assert second.evidence["evidence_id"] == job.evidence_id


def test_empty_source_or_missing_provenance_is_blocked(tmp_path: Path):
    empty = tmp_path / "empty.jpg"
    empty.write_bytes(b"")
    empty_result = MediaRuntime(tmp_path / "empty-workspace").submit(MediaJob("밝게 보정해줘", empty, MediaType.PHOTO))
    assert empty_result.state is JobState.BLOCKED_INPUT
    assert "empty" in empty_result.error

    source = tmp_path / "facade.jpg"
    Image.new("RGB", (16, 12), "gray").save(source)
    missing_provenance = MediaJob("밝게 보정해줘", source, MediaType.PHOTO, source_provenance={})
    provenance_result = MediaRuntime(tmp_path / "provenance-workspace").submit(missing_provenance)
    assert provenance_result.state is JobState.BLOCKED_INPUT
    assert "provenance" in provenance_result.error
