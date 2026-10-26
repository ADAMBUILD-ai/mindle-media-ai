"""Truthful product-level status for the local AI execution chain."""
from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path
import re


@lru_cache(maxsize=256)
def _artifact_digest(path: Path, identity: tuple) -> str | None:
    # Cache only unchanged filesystem identities, never a prior PASS verdict.
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return digest if _file_identity(path) == identity else None


def _file_identity(path: Path) -> tuple:
    info = path.stat()
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _verified_artifact(item: dict, root: Path | None) -> bool:
    """Recheck evidence bytes in the product data directory; missing data fails closed."""
    if root is None or not isinstance(item, dict):
        return False
    try:
        path = Path(item["path"]).resolve()
        if root.resolve() not in path.parents or not path.is_file():
            return False
        if type(item.get("bytes")) is not int or path.stat().st_size != item["bytes"] or item["bytes"] <= 0:
            return False
        return _artifact_digest(path, _file_identity(path)) == item.get("sha256")
    except (OSError, KeyError, TypeError, ValueError):
        return False


def _verified_record(record: dict, root: Path | None) -> bool:
    return record.get("status") == "TESTED_PASS" and _verified_artifact(record.get("primary_output"), root)


def _verified_plan(plan: dict, root: Path | None, architecture=False) -> bool:
    if root is None or plan.get("plan_source") != "LOCAL_GENERATIVE_INFERENCE":
        return False
    if not all(re.fullmatch(r"[0-9a-f]{64}", str(plan.get(key, "")))
               for key in ("model_sha256", "raw_response_sha256")):
        return False
    identifier = str(plan.get("plan_id", ""))
    if not re.fullmatch(r"[0-9a-f-]{36}", identifier):
        return False
    path = root / ("architecture-agent/plans" if architecture else "workflows/plans") / (identifier + ".response.txt")
    try:
        return _verified_artifact({"path": str(path), "bytes": path.stat().st_size,
                                   "sha256": plan["raw_response_sha256"]}, root)
    except OSError:
        return False


def _connected_chain(task: dict, root: Path | None) -> bool:
    """Only one successful inferred workflow can prove its own voice-to-final-MP4 link."""
    if task.get("state") != "SUCCEEDED" or not _verified_plan(task.get("plan_receipt", {}), root):
        return False
    records = task.get("records", [])
    result = task.get("result", {})
    identifier = task.get("workflow_id")
    if not identifier or not _verified_record(result, root):
        return False
    final = next((r for r in records if r.get("job_id") == result.get("job_id")), None)
    if not final or not _verified_record(final, root) or final.get("primary_output") != result.get("primary_output") or final.get("workflow_id") != identifier:
        return False
    runtime = final.get("runtime_result", {})
    if final.get("lane") != "video" or final.get("operation") != "video_edit":
        return False
    if not str(final.get("primary_output", {}).get("path", "")).lower().endswith(".mp4"):
        return False
    if runtime.get("video_codec") != "h264" or runtime.get("audio_codec") != "aac":
        return False
    voice_id = runtime.get("options", {}).get("narration_job_id")
    for voice in records:
        if (voice_id and voice.get("job_id") == voice_id and voice.get("workflow_id") == identifier
                and _actual_neural_voice([voice]) and _verified_record(voice, root)):
            # Sealing changes paths, so bind the copied mix input by content identity.
            source = voice["primary_output"]
            return any(item.get("sha256") == source["sha256"] and item.get("bytes") == source["bytes"]
                       and _verified_artifact(item, root) for item in final.get("outputs", []))
    return False


def _verified_auto_edit(task, root):
    plan = task.get("plan_receipt", {})
    if task.get("state") != "SUCCEEDED" or plan.get("task_kind") != "MEASURED_GENERATIVE_AUTO_EDIT":
        return False
    result = task.get("result", {})
    quality = task.get("technical_quality", {})
    if not _verified_plan(plan, root) or not _verified_record(result, root):
        return False
    source = task.get("input_record", {})
    artifact = source.get("preview_output", source.get("primary_output", {}))
    if not _verified_artifact(artifact, root):
        return False
    if (quality.get("status") != "PASS_TECHNICAL_ONLY" or quality.get("output_sha256") != result["primary_output"]["sha256"]
            or source.get("job_id") != plan.get("input_job_id") or artifact.get("sha256") != plan.get("input_sha256")):
        return False
    try:
        from .generative_auto_edit import validate_auto_binding
        validate_auto_binding(root, plan, source, artifact)
    except (OSError, ValueError, KeyError, TypeError):
        return False
    return result.get("runtime_result", {}).get("options") == plan["steps"][0]["options"]


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
    data_root: Path | None = None,
) -> dict:
    """Separate configured engines, completed inference and unimplemented generation."""
    planner_configured = capabilities.get("generative_planner") not in {None, "LOCAL_GENERATIVE_MODEL_UNAVAILABLE"}
    tts_configured = capabilities.get("neural_korean_tts") is True
    planner_runs = [
        task for task in workflows
        if task.get("state") == "SUCCEEDED"
        and _verified_plan(task.get("plan_receipt", {}), data_root)
    ]
    architecture_runs = [
        task for task in productions
        if task.get("state") == "SUCCEEDED"
        and task.get("receipt", {}).get("planner_model_inference") is True
        and _verified_plan(task.get("planner_receipt", {}), data_root, architecture=True)
        and _verified_artifact(task.get("receipt", {}).get("output"), data_root)
    ]
    workflow_records = [record for task in workflows for record in task.get("records", [])]
    all_records = [record for record in [*records, *workflow_records] if _verified_record(record, data_root)]
    neural_voice = _actual_neural_voice(all_records)
    actual_tools = {
        "sam_photo_segmentation": _completed_operation(all_records, "segment"),
        "sam_video_tracking": _completed_operation(all_records, "tracking"),
        "whisper_korean_stt": _completed_operation(all_records, "transcribe"),
        "photo_upscale_4x": _completed_operation(all_records, "upscale"),
    }
    mp4_output = any(
        record.get("status") == "TESTED_PASS"
        and record.get("operation") != "import"
        and record.get("lane") == "video"
        and str(record.get("primary_output", {}).get("path", "")).lower().endswith(".mp4")
        for record in all_records
    )
    actual_planner = bool(planner_runs or architecture_runs)
    connected = [task["workflow_id"] for task in planner_runs if _connected_chain(task, data_root)]
    auto_edits = [task["workflow_id"] for task in planner_runs if _verified_auto_edit(task, data_root)]
    actual_chain = bool(connected)
    if actual_chain:
        state = "AI_RUNTIME_ACTUAL_CHAIN_VERIFIED"
    elif auto_edits:
        state = "AI_EDIT_EXECUTION_VERIFIED"
    elif planner_configured and tts_configured:
        state = "AI_ENGINES_READY_INFERENCE_REQUIRED"
    else:
        state = "AI_RUNTIME_INCOMPLETE"
    return {
        "state": state,
        "chain_evidence": {"workflow_ids": connected, "scope": "SAME_WORKFLOW_VERIFIED_ARTIFACTS",
                           "full_product_pass": False, "human_hearing": "NOT_VERIFIED"},
        "auto_edit_evidence": {"workflow_ids": auto_edits, "semantic_understanding": False,
                               "human_visual_approval": "REQUIRED", "full_product_pass": False},
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
