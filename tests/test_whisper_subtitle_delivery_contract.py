"""Contract tests for binding real Whisper evidence to a subtitle MP4."""
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from media_ai.product_runtime import ProductJobService, file_record


def test_verified_whisper_receipt_is_required_for_subtitle_render(tmp_path):
    service = ProductJobService.__new__(ProductJobService)
    service.records = {}
    with pytest.raises(ValueError, match="VERIFIED_TRANSCRIPTION_REQUIRED"):
        service.render_transcribed_subtitles("missing")


def test_subtitle_render_keeps_the_transcription_and_source_identities(tmp_path, monkeypatch):
    video = tmp_path / "source.mp4"; video.write_bytes(b"approved source video")
    srt = tmp_path / "korean_transcript.srt"; srt.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\n안녕하세요 MINDLE MEDIA\n", encoding="utf-8")
    transcript = tmp_path / "korean_transcript.json"; transcript.write_text("{}", encoding="utf-8")
    font = tmp_path / "malgun.ttf"; font.write_bytes(b"font fixture")
    service = ProductJobService.__new__(ProductJobService)
    service.jobs = tmp_path / "jobs"; service.jobs.mkdir()
    service.records = {
        "stt-job": {
            "status": "TESTED_PASS", "job_id": "stt-job", "operation": "transcribe",
            "primary_output": file_record(transcript),
            "outputs": [file_record(transcript), file_record(srt)],
            "runtime_result": {
                "source_media": file_record(video),
                "segments": [{"start_seconds": 0.0, "end_seconds": 2.0, "text": "안녕하세요 MINDLE MEDIA"}],
            },
        }
    }
    monkeypatch.setenv("MINDLE_SUBTITLE_FONT", str(font))
    monkeypatch.delenv("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", raising=False)

    def fake_run(command, **_kwargs):
        if command[:2] == ["ffmpeg", "-y"]:
            Path(command[-1]).write_bytes(b"subtitle mp4")
        return None

    probe = json.dumps({"format": {"duration": "2.0"}, "streams": [
        {"codec_type": "video", "codec_name": "h264"},
        {"codec_type": "audio", "codec_name": "aac"},
    ]})
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(
        subprocess, "check_output",
        lambda _command, text=False: probe if text else probe.encode("utf-8"),
    )
    rendered = service.render_transcribed_subtitles("stt-job")
    assert rendered["status"] == "TESTED_PASS"
    assert rendered["runtime_result"]["transcription_job_id"] == "stt-job"
    assert rendered["runtime_result"]["source_media_sha256"] == hashlib.sha256(video.read_bytes()).hexdigest()
    assert rendered["runtime_result"]["timed_srt_sha256"] == hashlib.sha256(srt.read_bytes()).hexdigest()
    assert Path(rendered["primary_output"]["path"]).is_file()
