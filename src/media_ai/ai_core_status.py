"""Truthful product-level status for the local AI execution chain."""
from __future__ import annotations


def _actual_neural_voice(records: list[dict]) -> bool:
    return any(
        record.get("operation") == "narration"
        and record.get("status") == "TESTED_PASS"
        and record.get("runtime_result", {}).get("model_inference") is True
        for record in records
    )


def _completed_operation(records: list[dict], operation: str) -> bool:
    return any(
        record.get("status") == "TESTED_PASS"
        and record.get("operation") == operation
        and bool(record.get("model") or record.get("runtime_result", {}).get("model_inference"))
        for record in records
    )


def summarize_ai_core(
    capabilities: dict,
    workflows: list[dict],
    productions: list[dict],
    records: list[dict],
    model_readiness: dict | None = None,
) -> dict:
    """Separate configured engines, completed inference and unimplemented generation."""
    planner_configured = capabilities.get("generative_planner") not in {None, "LOCAL_GENERATIVE_MODEL_UNAVAILABLE"}
    tts_configured = capabilities.get("tts") not in {None, "TTS_ENGINE_UNAVAILABLE"}
    planner_runs = [
        task for task in workflows
        if task.get("state") == "SUCCEEDED"
        and task.get("plan_receipt", {}).get("plan_source") == "LOCAL_GENERATIVE_INFERENCE"
    ]
    architecture_runs = [
        task for task in productions
        if task.get("state") == "SUCCEEDED"
        and task.get("receipt", {}).get("planner_model_inference") is True
    ]
    workflow_records = [record for task in workflows for record in task.get("records", [])]
    all_records = [*records, *workflow_records]
    neural_voice = _actual_neural_voice(all_records)
    actual_tools = {
        "sam_photo_segmentation": _completed_operation(all_records, "segment"),
        "sam_video_tracking": _completed_operation(all_records, "tracking"),
        "whisper_korean_stt": _completed_operation(all_records, "transcribe"),
        "photo_upscale_4x": _completed_operation(all_records, "upscale"),
    }
    mp4_output = any(
        record.get("status") == "TESTED_PASS"
        and record.get("lane") == "video"
        and str(record.get("primary_output", {}).get("path", "")).lower().endswith(".mp4")
        for record in all_records
    )
    actual_planner = bool(planner_runs or architecture_runs)
    actual_chain = actual_planner and neural_voice and mp4_output
    if actual_chain:
        state = "AI_RUNTIME_ACTUAL_CHAIN_VERIFIED"
    elif planner_configured and tts_configured:
        state = "AI_ENGINES_READY_INFERENCE_REQUIRED"
    else:
        state = "AI_RUNTIME_INCOMPLETE"
    return {
        "state": state,
        "shell_only": not (planner_configured or tts_configured or actual_planner or neural_voice),
        "configured": {
            "local_generative_planner": planner_configured,
            "neural_korean_tts": tts_configured,
            "durable_queue": capabilities.get("durable_queue") is True,
            "verified_media_model_files": (model_readiness or {}).get("status") not in {
                None, "NOT_VERIFIED", "BLOCKED_MODEL_FILES"
            },
        },
        "actual_evidence": {
            "qwen_or_architecture_plan": actual_planner,
            "neural_korean_voice": neural_voice,
            "mp4_output": mp4_output,
            "completed_generative_workflows": len(planner_runs),
            "completed_architecture_productions": len(architecture_runs),
            **actual_tools,
        },
        "limitations": {
            "semantic_vision_generation": False,
            "text_to_video_generation": False,
            "external_provider_connected": False,
        },
    }
