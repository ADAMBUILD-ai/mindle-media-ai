from pathlib import Path

import pytest

from media_ai.contracts import MediaType
from media_ai.ui_bridge import command_to_job


def test_photo_command_routes_without_exposing_model_name(tmp_path: Path):
    source = tmp_path / "facade.jpg"
    reference = tmp_path / "style.png"
    source.write_bytes(b"photo-fixture")
    reference.write_bytes(b"reference-fixture")
    job = command_to_job("수직을 바로잡고 유리 반사를 줄여줘", source, [str(reference)])
    assert job.media_type is MediaType.PHOTO
    assert job.options["reference_files"] == ["style.png"]


def test_video_command_routes_from_video_instruction_without_file_extension(tmp_path: Path):
    source = tmp_path / "clip.mp4"
    source.write_bytes(b"video-fixture")
    job = command_to_job("영상의 앞부분을 잘라줘", source)
    assert job.media_type is MediaType.VIDEO


def test_command_bridge_rejects_blank_command(tmp_path: Path):
    source = tmp_path / "facade.jpg"
    source.write_bytes(b"photo-fixture")
    with pytest.raises(ValueError):
        command_to_job("  ", source)


@pytest.mark.parametrize("references", [["animation.gif"], ["reference.png", "REFERENCE.PNG"], ["a.png"] * 6])
def test_command_bridge_rejects_invalid_reference_payloads(tmp_path: Path, references):
    source = tmp_path / "facade.jpg"
    source.write_bytes(b"photo-fixture")
    with pytest.raises(ValueError):
        command_to_job("반사를 줄여줘", source, references)


def test_command_bridge_rejects_missing_or_unsupported_source_assets(tmp_path: Path):
    with pytest.raises(ValueError, match="unavailable"):
        command_to_job("밝게 보정해줘", tmp_path / "missing.jpg")

    source = tmp_path / "facade.gif"
    source.write_bytes(b"unsupported-fixture")
    with pytest.raises(ValueError, match="Unsupported"):
        command_to_job("밝게 보정해줘", source)

    valid_source = tmp_path / "facade.jpg"
    valid_source.write_bytes(b"photo-fixture")
    with pytest.raises(ValueError, match="Reference asset is unavailable"):
        command_to_job("밝게 보정해줘", valid_source, [str(tmp_path / "missing.png")])
