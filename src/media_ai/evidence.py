"""Evidence records for execution attempts without claiming unverified model runtime."""
import platform
from datetime import datetime, timezone
from pathlib import Path

from .contracts import MediaJob
from .job_pipeline import ExecutionBoundary


def runtime_environment() -> dict[str, str]:
    return {
        "platform": platform.platform(),
        "hardware": platform.processor() or "unreported",
    }


def blocked_evidence(job: MediaJob, status: str, reason: str) -> dict:
    return {
        "job_id": job.id,
        "evidence_id": job.evidence_id,
        "evidence_status": status,
        "runtime_status": status,
        "terminal_state": job.state,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "project_id": job.project_id,
        "requested_operation": job.requested_operation,
        "source_provenance": dict(job.source_provenance or {}),
        "reference_files": list(job.reference_files),
        "retry_provenance": {"job_id": job.id, "evidence_id": job.evidence_id, "attempt": job.attempts},
        "reason": reason,
        "runtime": runtime_environment(),
    }


def execution_evidence(
    job: MediaJob,
    boundary: ExecutionBoundary,
    source: Path,
    output: Path,
    input_sha256: str,
    output_sha256: str,
    started_at: str,
    duration_ms: float,
    detail: dict,
) -> dict:
    return {
        "job_id": job.id,
        "evidence_id": job.evidence_id,
        "evidence_status": "VERIFY_REQUIRED",
        "runtime_status": "LOCAL_EXECUTION",
        "terminal_state": job.state,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "duration_ms": duration_ms,
        "project_id": job.project_id,
        "requested_operation": boundary.operation,
        "source_provenance": dict(job.source_provenance or {}),
        "adapter_id": boundary.adapter_id,
        "model_or_program_id": boundary.model_or_program_id,
        "revision": boundary.revision,
        "license_source": boundary.license_source,
        "input_sha256": input_sha256,
        "output_sha256": output_sha256,
        "output_artifact": {
            "path": str(output),
            "type": output.suffix.lower(),
            "sha256": output_sha256,
            "size_bytes": output.stat().st_size,
            "status": "available",
        },
        "source": str(source),
        "output": str(output),
        "reference_files": list(job.reference_files),
        "retry_provenance": {"job_id": job.id, "evidence_id": job.evidence_id, "attempt": job.attempts},
        "runtime": runtime_environment(),
        **detail,
    }


def missing_execution_evidence_fields(evidence: dict) -> set[str]:
    required = {
        "job_id", "evidence_id", "evidence_status", "runtime_status", "terminal_state",
        "source_provenance", "input_sha256", "output_sha256", "output_artifact",
        "adapter_id", "model_or_program_id", "runtime", "retry_provenance",
    }
    return {field for field in required if not evidence.get(field)}
