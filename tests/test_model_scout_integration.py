from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest
from PIL import Image

from media_ai.contracts import MediaJob, MediaType
from media_ai.model_scout_integration import (
    HandoffValidationError, InputArtifactIntake, IntegrationStatus, ModelScoutAdapterRegistry,
    ModelScoutHandoff, RuntimeIntegrationGate,
)
from media_ai.runtime_orchestration import RuntimeOrchestrator, artifact_sha256


def photo(path: Path) -> Path:
    Image.new("RGB", (8, 8), "gray").save(path)
    return path


def handoff(tmp_path: Path, lane: MediaType = MediaType.PHOTO, operation: str = "photo_adjust") -> ModelScoutHandoff:
    artifact = tmp_path / "adapter.bin"
    artifact.write_bytes(b"verified-adapter-artifact")
    return ModelScoutHandoff("scout-request-1", "issue-1", lane, operation, "vendor/model", "https://example.invalid/model", "rev-1", "Apache-2.0", artifact, artifact.name, artifact.stat().st_size, artifact_sha256(artifact), "onnx", "cpu", "scout_photo_adapter", "1.0.0", "VERIFIED", datetime.now(timezone.utc).isoformat())


@pytest.mark.parametrize("field,value", [("revision", ""), ("license_evidence", ""), ("artifact_size_bytes", 1), ("artifact_sha256", "0" * 64), ("verification_status", "DOWNLOADED")])
def test_invalid_handoffs_never_enter_verified_registry(tmp_path: Path, field: str, value: str | int):
    registry = ModelScoutAdapterRegistry()
    with pytest.raises(HandoffValidationError):
        registry.ingest(replace(handoff(tmp_path), **{field: value}))
    assert registry.get(MediaType.PHOTO, "photo_adjust") is None


def test_verified_handoff_registers_and_readiness_is_rechecked_before_preflight(tmp_path: Path):
    registry = ModelScoutAdapterRegistry()
    registered = registry.ingest(handoff(tmp_path))
    assert registry.readiness(MediaType.PHOTO, "photo_adjust") is IntegrationStatus.RUNTIME_READY
    job = MediaJob("사진 보정", photo(tmp_path / "input.jpg"), MediaType.PHOTO)
    assert RuntimeOrchestrator(registry.runtime_registry).preflight(job).status.value == "PREFLIGHT_READY"
    registered.handoff.artifact_path.unlink()
    blocked = MediaJob("사진 보정", photo(tmp_path / "next.jpg"), MediaType.PHOTO)
    assert RuntimeOrchestrator(registry.runtime_registry).preflight(blocked).status.value == "MODEL_UNAVAILABLE"


def test_partial_input_intake_and_gate_do_not_wait_for_other_lanes(tmp_path: Path):
    registry = ModelScoutAdapterRegistry(); intake = InputArtifactIntake()
    registry.ingest(handoff(tmp_path))
    source = photo(tmp_path / "input.jpg")
    manifest = intake.ingest(MediaType.PHOTO, source)
    job = MediaJob("사진 보정", source, MediaType.PHOTO, requested_operation="photo_adjust")
    gate = RuntimeIntegrationGate(registry, intake)
    assert manifest.status == "PARTIAL_INPUT_READY"
    assert gate.readiness(job) is IntegrationStatus.RUNTIME_READY
    assert intake.get(MediaType.VIDEO) is None and intake.get(MediaType.KOREAN_AUDIO) is None


def test_callback_rejects_wrong_lane_stale_revision_and_hash(tmp_path: Path):
    registry = ModelScoutAdapterRegistry(); intake = InputArtifactIntake(); entry = handoff(tmp_path)
    registry.ingest(entry)
    source = photo(tmp_path / "input.jpg"); manifest = intake.ingest(MediaType.PHOTO, source)
    job = MediaJob("사진 보정", source, MediaType.PHOTO, requested_operation="photo_adjust")
    callback = {"request_id": entry.request_id, "issue_id": entry.issue_id, "callback_id": "callback-1", "job_id": job.id, "evidence_id": job.evidence_id, "lane": MediaType.PHOTO, "revision": entry.revision, "artifact_sha256": entry.artifact_sha256, "adapter_id": entry.adapter_id, "adapter_version": entry.adapter_version, "status": "TESTED_PASS", "input_sha256": manifest.sha256, "output_sha256": "a" * 64, "output_path": "external://result.png", "elapsed_ms": 1, "runtime_backend": entry.runtime_backend, "device_requirement": entry.device_requirement, "sent_at": entry.issued_at}
    gate = RuntimeIntegrationGate(registry, intake)
    for key, value in [("lane", MediaType.VIDEO), ("revision", "old"), ("artifact_sha256", "b" * 64), ("sent_at", "2000-01-01T00:00:00+00:00")]:
        with pytest.raises(HandoffValidationError):
            gate.accept_callback(job, {**callback, key: value})
    assert gate.accept_callback(job, callback) is IntegrationStatus.DELIVERED
    assert job.evidence["model_scout_delivery"]["status"] is IntegrationStatus.DELIVERED


def test_tested_pass_gate_requires_real_input_identity_and_output_evidence(tmp_path: Path):
    registry = ModelScoutAdapterRegistry(); intake = InputArtifactIntake(); entry = handoff(tmp_path)
    registry.ingest(entry)
    source = photo(tmp_path / "input.jpg"); intake.ingest(MediaType.PHOTO, source)
    job = MediaJob("사진 보정", source, MediaType.PHOTO, requested_operation="photo_adjust")
    callback = {"request_id": entry.request_id, "issue_id": entry.issue_id, "callback_id": "callback-1", "job_id": job.id, "evidence_id": job.evidence_id, "lane": MediaType.PHOTO, "revision": entry.revision, "artifact_sha256": entry.artifact_sha256, "adapter_id": entry.adapter_id, "adapter_version": entry.adapter_version, "status": "TESTED_PASS", "input_sha256": "wrong", "output_sha256": "", "output_path": "", "elapsed_ms": 1, "runtime_backend": entry.runtime_backend, "device_requirement": entry.device_requirement, "sent_at": entry.issued_at}
    with pytest.raises(HandoffValidationError, match="incomplete"):
        RuntimeIntegrationGate(registry, intake).accept_callback(job, callback)
