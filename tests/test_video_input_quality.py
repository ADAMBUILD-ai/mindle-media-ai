import json

import cv2
import numpy as np

from media_ai.video_input_quality import assess_video_input


def test_low_bits_per_pixel_video_requires_visual_review(tmp_path, monkeypatch):
    source = tmp_path / "architectural.mp4"
    writer = cv2.VideoWriter(str(source), cv2.VideoWriter_fourcc(*"mp4v"), 30, (64, 48))
    for index in range(12):
        frame = np.full((48, 64, 3), index * 10, dtype=np.uint8)
        frame[:, 16::16] = 255
        writer.write(frame)
    writer.release()
    assert source.is_file()

    monkeypatch.setattr(
        "media_ai.video_input_quality._ffprobe",
        lambda _ffprobe, _source: {
            "streams": [{"codec_name": "h264", "width": 64, "height": 48,
                         "avg_frame_rate": "30/1", "bit_rate": "4000"}],
            "format": {"bit_rate": "4000"},
        },
    )

    evidence = tmp_path / "INPUT_QUALITY.json"
    result = assess_video_input(source, evidence, "unused-ffprobe")

    assert result["status"] == "INPUT_QUALITY_REVIEW_REQUIRED"
    assert "LOW_BITS_PER_PIXEL_PER_FRAME" in result["risk_signals"]
    assert result["promotion_eligible_without_restoration"] is False
    assert json.loads(evidence.read_text(encoding="utf-8"))["source"]["sha256"] == result["source"]["sha256"]
