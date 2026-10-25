from media_ai.durable_workflows import validate_steps
from media_ai.planner_constraints import validate_edit_values, validate_media_tool_values


def video_step(options):
    return [{"operation": "video_edit", "options": options}]


def assert_rejected(code, command, steps):
    try:
        validate_media_tool_values(command, steps)
    except ValueError as error:
        assert code in str(error)
    else:
        raise AssertionError(f"expected {code}")


def test_trim_speed_values_are_bound_to_the_korean_request():
    command = "5초부터 12초까지 자르고 속도를 1.25배로 해 주세요."
    steps = video_step({"start": 5, "duration": 7, "speed": 1.25})
    assert validate_media_tool_values(command, steps) == {"speed": 1.25, "start": 5.0, "duration": 7.0}
    assert validate_edit_values(command, steps) == {}


def test_model_cannot_change_requested_trim_or_speed():
    for options in (
        {"start": 5, "duration": 8, "speed": 1.25},
        {"start": 5, "duration": 7, "speed": 1.5},
    ):
        assert_rejected(
            "PLANNER_TOOL_VALUE_MISMATCH",
            "5초부터 12초까지 자르고 속도를 1.25배로",
            video_step(options),
        )


def test_aspect_fade_and_bgm_are_explicit_and_bgm_has_a_visible_default():
    command = "9:16 비율로 페이드 전환하고 배경음악을 넣어 주세요."
    options = {"aspect": "9:16", "fade": True, "backgroundVolume": .35}
    assert validate_media_tool_values(command, video_step(options)) == options
    assert validate_media_tool_values(
        "16:9 비율로 BGM 20%를 넣어 주세요.",
        video_step({"aspect": "16:9", "backgroundVolume": .2}),
    )["backgroundVolume"] == .2


def test_missing_or_invented_media_tool_is_rejected():
    assert_rejected("PLANNER_INCOMPLETE_PLAN", "속도를 1.2배로", video_step({}))
    assert_rejected("PLANNER_SCOPE_MISMATCH", "밝기를 3 높여 주세요.", video_step({"speed": 1.2}))


def test_durable_contract_accepts_bounded_bgm_volume_option():
    steps = validate_steps(video_step({"backgroundVolume": .35}))
    assert steps[0]["options"]["backgroundVolume"] == .35


def test_durable_contract_rejects_unsafe_tool_ranges():
    for options in ({"speed": 4}, {"start": -1}, {"duration": 0}, {"backgroundVolume": 2}, {"fade": "yes"}):
        try:
            validate_steps(video_step(options))
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe options accepted: {options}")
