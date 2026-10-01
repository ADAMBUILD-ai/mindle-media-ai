import pytest

from media_ai.ui_contract import CommandPhase, MediaUiContract


def test_video_and_photo_command_states_are_independent():
    ui = MediaUiContract()
    ui.video_command.focus()
    ui.video_command.text = "split at the playhead"
    ui.video_command.attach_reference("cut-reference.png")
    payload = ui.video_command.submit()

    assert payload == {"command": "split at the playhead", "references": ["cut-reference.png"]}
    assert ui.video_command.phase is CommandPhase.EXECUTING
    assert ui.photo_command.phase is CommandPhase.COLLAPSED

    ui.video_command.complete()
    assert ui.video_command.phase is CommandPhase.COLLAPSED
    assert ui.video_command.reference_files == []


def test_enter_submission_requires_a_nonempty_command():
    ui = MediaUiContract()
    ui.photo_command.focus()
    with pytest.raises(ValueError):
        ui.photo_command.submit()


def test_reference_limit_and_failed_command_preserve_the_draft():
    ui = MediaUiContract()
    ui.photo_command.text = "유리 반사를 줄여줘"
    for index in range(5):
        ui.photo_command.attach_reference(f"reference-{index}.png")

    with pytest.raises(ValueError, match="maximum of 5"):
        ui.photo_command.attach_reference("reference-5.png")

    ui.photo_command.submit()
    ui.photo_command.fail()
    assert ui.photo_command.phase is CommandPhase.EXPANDED
    assert ui.photo_command.text == "유리 반사를 줄여줘"
    assert len(ui.photo_command.reference_files) == 5


def test_reference_images_are_unique_supported_filenames_without_paths():
    ui = MediaUiContract()
    ui.photo_command.attach_reference(r"C:\\uploads\\Facade.PNG")

    assert ui.photo_command.reference_files == ["Facade.PNG"]

    with pytest.raises(ValueError, match="only once"):
        ui.photo_command.attach_reference("facade.png")
    with pytest.raises(ValueError, match="JPG, PNG, WEBP, or TIFF"):
        ui.photo_command.attach_reference("animation.gif")
