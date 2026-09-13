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
