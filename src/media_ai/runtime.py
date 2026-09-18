import json
import shutil
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from .contracts import MediaJob, JobState
from .evidence import blocked_evidence, execution_evidence
from .job_pipeline import BlockedInputError, BlockedModelError, validate_job
from .photo import process_photo
from .video import process_video

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()

class MediaRuntime:
    def __init__(self, root: Path):
        self.root = root; self.jobs: dict[str, MediaJob] = {}
        for name in ("originals", "outputs", "logs"): (root / name).mkdir(parents=True, exist_ok=True)

    def submit(self, job: MediaJob, retries: int = 1) -> MediaJob:
        self.jobs[job.id] = job
        job.error = None
        job.transition(JobState.VALIDATING)
        try:
            boundary = validate_job(job)
        except BlockedInputError as error:
            job.error = str(error)
            job.transition(JobState.BLOCKED_INPUT)
            job.evidence = blocked_evidence(job, "BLOCKED_INPUT", job.error)
            self._write_log(job)
            return job
        except BlockedModelError as error:
            job.error = str(error)
            job.transition(JobState.BLOCKED_MODEL)
            job.evidence = blocked_evidence(job, "BLOCKED_MODEL", job.error)
            self._write_log(job)
            return job

        job.transition(JobState.READY)
        stamped = f"{job.id}_{job.input_path.name}"
        preserved = self.root / "originals" / stamped
        shutil.copy2(job.input_path, preserved)
        target = job.output_target or self.root / "outputs" / f"{job.id}_{job.input_path.stem}_result{job.input_path.suffix}"
        for attempt in range(retries + 1):
            job.transition(JobState.RUNNING)
            job.attempts += 1
            started = datetime.now(timezone.utc).isoformat(); tick = time.perf_counter()
            try:
                detail = process_photo(preserved, target, job.options) if job.media_type.value == "photo" else process_video(preserved, target, job.options)
                actual = Path(detail.pop("actual_output", target))
                job.output_path = actual
                job.transition(JobState.SUCCEEDED)
                job.evidence = execution_evidence(job, boundary, preserved, actual, digest(preserved), digest(actual), started, round((time.perf_counter()-tick)*1000, 2), detail)
                break
            except BlockedInputError as error:
                job.error = str(error)
                job.transition(JobState.BLOCKED_INPUT)
                job.evidence = blocked_evidence(job, "BLOCKED_INPUT", job.error)
                break
            except BlockedModelError as error:
                job.error = str(error)
                job.transition(JobState.BLOCKED_MODEL)
                job.evidence = blocked_evidence(job, "BLOCKED_MODEL", job.error)
                break
            except Exception as error:
                job.error = str(error)
                if attempt < retries:
                    job.transition(JobState.READY)
                    continue
                job.transition(JobState.FAILED)
                job.evidence = {
                    **blocked_evidence(job, "VERIFY_REQUIRED", job.error),
                    "input_sha256": digest(preserved),
                    "attempts": job.attempts,
                }
        self._write_log(job)
        return job

    def retry(self, job_id: str, retries: int = 1) -> MediaJob:
        return self.submit(self.jobs[job_id], retries)

    def _write_log(self, job: MediaJob) -> None:
        (self.root / "logs" / f"{job.id}.json").write_text(
            json.dumps({"id": job.id, "state": job.state, "state_history": job.state_history, "error": job.error, "evidence": job.evidence}, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )

    def submit_batch(self, jobs: list[MediaJob]) -> list[MediaJob]:
        return [self.submit(job) for job in jobs]
