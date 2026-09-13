from pathlib import Path

import pytest

from media_ai.contracts import MediaType
from media_ai.ui_bridge import command_to_job


def test_photo_command_routes_without_exposing_model_name():
    job = command_to_job("수직을 바로잡고 유리 반사를 줄여줘", Path("facade.jpg"), ["style.png"])
    assert job.media_type is MediaType.PHOTO
    assert job.options["reference_files"] == ["style.png"]


def test_video_command_routes_from_video_instruction_without_file_extension():
    job = command_to_job("영상의 앞부분을 잘라줘", Path("unknown.asset"))
    assert job.media_type is MediaType.VIDEO


def test_command_bridge_rejects_blank_command():
    with pytest.raises(ValueError):
        command_to_job("  ", Path("facade.jpg"))
