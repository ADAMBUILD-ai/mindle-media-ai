"""Fail-closed request contract for MEDIA AI -> Marketing AI shortform planning."""
from __future__ import annotations
from typing import Any

def build_marketing_shortform_request(
    command: str, *, project_id: str | None = None, request_id: str | None = None
) -> dict[str, Any]:
    cleaned = command.strip()
    if not cleaned:
        raise ValueError("A natural-language shortform command is required")
    return {
        "contract_version": "1.0",
        "entrypoint": "media_ai",
        "request_id": request_id,
        "project_id": project_id,
        "command": cleaned,
        "requested_output": "shortform_bridge_contract",
        "approval_policy": "representative_required_before_export",
        "allow_publish": False,
        "allow_ad_spend": False,
    }
