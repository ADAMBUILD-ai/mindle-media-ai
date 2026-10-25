from media_ai.ai_core_status import summarize_ai_core


READY = {"generative_planner": "CONFIGURED_NOT_INFERENCE_VERIFIED", "tts": "CONFIGURED_NOT_SYNTHESIS_VERIFIED", "durable_queue": True}


def test_configured_engines_are_not_misreported_as_actual_ai_work():
    value = summarize_ai_core(READY, [], [], [])
    assert value["state"] == "AI_ENGINES_READY_INFERENCE_REQUIRED"
    assert value["shell_only"] is False
    assert not any(value["actual_evidence"][key] for key in ("qwen_or_architecture_plan", "neural_korean_voice", "mp4_output"))


def test_actual_qwen_neural_voice_and_mp4_close_the_chain():
    voice = {"status": "TESTED_PASS", "operation": "narration", "runtime_result": {"model_inference": True}}
    video = {"status": "TESTED_PASS", "lane": "video", "primary_output": {"path": "C:/data/final.mp4"}}
    workflow = {"state": "SUCCEEDED", "plan_receipt": {"plan_source": "LOCAL_GENERATIVE_INFERENCE"}, "records": [voice, video]}
    value = summarize_ai_core(READY, [workflow], [], [])
    assert value["state"] == "AI_RUNTIME_ACTUAL_CHAIN_VERIFIED"
    assert value["actual_evidence"] == {
        "qwen_or_architecture_plan": True,
        "neural_korean_voice": True,
        "mp4_output": True,
        "completed_generative_workflows": 1,
        "completed_architecture_productions": 0,
        "sam_photo_segmentation": False,
        "sam_video_tracking": False,
        "whisper_korean_stt": False,
        "photo_upscale_4x": False,
    }


def test_static_shell_is_exposed_and_generation_limits_stay_explicit():
    value = summarize_ai_core({}, [], [], [])
    assert value["state"] == "AI_RUNTIME_INCOMPLETE"
    assert value["shell_only"] is True
    assert value["limitations"]["text_to_video_generation"] is False


def test_media_ai_models_require_successful_inference_records():
    records = [
        {"status": "TESTED_PASS", "operation": "segment", "model": {"repo_id": "facebook/sam2"}},
        {"status": "TESTED_PASS", "operation": "tracking", "model": {"repo_id": "facebook/sam2"}},
        {"status": "TESTED_PASS", "operation": "transcribe", "model": {"repo_id": "openai/whisper-small"}},
        {"status": "TESTED_PASS", "operation": "upscale", "model": {"repo_id": "Intel/4x"}},
        {"status": "FAILED", "operation": "upscale", "model": {"repo_id": "ignored"}},
    ]
    actual = summarize_ai_core(READY, [], [], records)["actual_evidence"]
    assert actual["sam_photo_segmentation"] is True
    assert actual["sam_video_tracking"] is True
    assert actual["whisper_korean_stt"] is True
    assert actual["photo_upscale_4x"] is True
