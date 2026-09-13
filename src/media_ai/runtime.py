import json
import shutil
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from .contracts import MediaJob, JobState
from .photo import process_photo
from .video import process_video
from .planner import plan

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
        self.jobs[job.id] = job; job.state = JobState.RUNNING; job.attempts += 1
        stamped = f"{job.id}_{job.input_path.name}"
        preserved = self.root / "originals" / stamped
        shutil.copy2(job.input_path, preserved)
        target = self.root / "outputs" / f"{job.id}_{job.input_path.stem}_result{job.input_path.suffix}"
        started = datetime.now(timezone.utc).isoformat(); tick = time.perf_counter()
        try:
            detail = process_photo(preserved, target, job.options) if job.media_type.value == "photo" else process_video(preserved, target, job.options)
            actual = Path(detail.pop("actual_output", target)); job.output_path = actual; job.state = JobState.SUCCEEDED
            job.evidence = {"started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(), "duration_ms": round((time.perf_counter()-tick)*1000,2), "input_sha256": digest(preserved), "output_sha256": digest(actual), "tool_version": detail["engine"], "provider": "local_default_provider", "plan": [s.name for s in plan(job.media_type, job.request, job.options)], "source": str(preserved), "output": str(actual), **detail}
        except Exception as exc:
            job.error = str(exc)
            if job.attempts <= retries:
                job.state = JobState.RETRY
                return self.submit(job, retries)
            job.state = JobState.FAILED; job.evidence = {"started_at": started, "failed_at": datetime.now(timezone.utc).isoformat(), "input_sha256": digest(preserved), "error": job.error, "attempts": job.attempts}
        (self.root / "logs" / f"{job.id}.json").write_text(json.dumps({"id":job.id,"state":job.state,"error":job.error,"evidence":job.evidence}, ensure_ascii=False, indent=2), encoding="utf-8")
        return job

    def submit_batch(self, jobs: list[MediaJob]) -> list[MediaJob]:
        return [self.submit(job) for job in jobs]
