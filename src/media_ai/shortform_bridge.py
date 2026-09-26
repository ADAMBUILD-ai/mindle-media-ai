"""SHORTFORM BRIDGE Contract v1 reader for the approved MEDIA AI pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PRODUCTS = {"ADAM", "AVORA", "AURA", "ARCOS", "AXIOM", "ADRAW", "ASPEC"}
DURATIONS = {15, 30, 60}
PLATFORMS = {"youtube_shorts", "instagram_reels", "tiktok", "other"}
APPROVAL_STATES = {"draft", "preview_ready", "representative_approved", "exported"}
REQUIRED_FIELDS = {
    "contract_version", "project_id", "campaign_id", "product", "target",
    "campaign_goal", "duration", "platform", "hook", "scenes",
    "media_assets", "cta", "brand_outro", "approval_state",
    "evidence_refs", "assumptions", "traceability",
}

@dataclass(frozen=True)
class ShortformScene:
    scene_id: str
    start_sec: float
    end_sec: float
    subtitle: str
    voiceover: str
    media_asset_id: str

@dataclass(frozen=True)
class ShortformProductionPlan:
    campaign_id: str
    project_id: str
    product: str
    duration: int
    platform: str
    aspect_ratio: str
    scenes: tuple[ShortformScene, ...]
    approval_state: str
    export_authorized: bool = False

class ShortformContractError(ValueError):
    pass

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ShortformContractError(message)

def read_shortform_contract(payload: dict[str, Any]) -> ShortformProductionPlan:
    _require(isinstance(payload, dict), "contract must be an object")
    missing = sorted(REQUIRED_FIELDS - payload.keys())
    _require(not missing, f"missing fields: {', '.join(missing)}")
    _require(payload["contract_version"] == "1.0", "unsupported contract_version")
    _require(payload["product"] in PRODUCTS, "unsupported product")
    _require(payload["duration"] in DURATIONS, "unsupported duration")
    _require(payload["platform"] in PLATFORMS, "unsupported platform")
    _require(payload["approval_state"] in APPROVAL_STATES, "invalid approval_state")
    _require(payload.get("aspect_ratio") == "9:16", "shortform aspect_ratio must be 9:16")
    _require(isinstance(payload["scenes"], list) and payload["scenes"], "scenes are required")
    _require(isinstance(payload["media_assets"], list), "media_assets must be a list")
    approved_assets = {
        item.get("asset_id") for item in payload["media_assets"]
        if item.get("approval_state") == "approved"
    }
    scenes: list[ShortformScene] = []
    cursor = 0.0
    for raw in payload["scenes"]:
        start, end = float(raw["start_sec"]), float(raw["end_sec"])
        _require(start == cursor and end > start, "scene timeline must be continuous")
        asset_id = raw.get("media_asset_id")
        _require(asset_id in approved_assets, f"scene references unapproved asset: {asset_id}")
        scenes.append(ShortformScene(
            scene_id=str(raw["id"]), start_sec=start, end_sec=end,
            subtitle=str(raw.get("subtitle", "")), voiceover=str(raw.get("voiceover", "")),
            media_asset_id=str(asset_id),
        ))
        cursor = end
    _require(cursor == float(payload["duration"]), "scene timeline must equal duration")
    return ShortformProductionPlan(
        campaign_id=str(payload["campaign_id"]), project_id=str(payload["project_id"]),
        product=str(payload["product"]), duration=int(payload["duration"]),
        platform=str(payload["platform"]), aspect_ratio="9:16", scenes=tuple(scenes),
        approval_state=str(payload["approval_state"]), export_authorized=False,
    )

def authorize_export(plan: ShortformProductionPlan) -> ShortformProductionPlan:
    _require(plan.approval_state == "representative_approved", "representative approval required")
    return ShortformProductionPlan(**{**plan.__dict__, "export_authorized": True})
