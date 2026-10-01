"""SHORTFORM BRIDGE Contract v1 reader for the approved MEDIA AI pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PRODUCTS = {"ADAM", "AVORA", "AURA", "ARCOS", "AXIOM", "ADRAW", "ASPEC", "MARKETING_EXTERNAL"}
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


def normalize_marketing_contract(payload: dict[str, Any]) -> dict[str, Any]:
    """Map the Marketing handoff shape without mutating or relabeling its raw identity."""
    _require(isinstance(payload, dict), "Marketing contract must be an object")
    mission = payload.get("mission", {})
    brief = payload.get("brief", {})
    resolved_assets = payload.get("resolved_assets", [])
    scenes = payload.get("scenes", [])
    normalized = dict(payload)
    normalized["product"] = "MARKETING_EXTERNAL"
    normalized["project_id"] = payload.get("project_id", mission.get("project_id"))
    normalized["campaign_id"] = payload.get("campaign_id", brief.get("campaign_id", normalized["project_id"]))
    normalized["target"] = payload.get("target", mission.get("target", brief.get("target")))
    normalized["campaign_goal"] = payload.get("campaign_goal", mission.get("campaign_goal", brief.get("objective")))
    normalized["duration"] = payload.get("duration", mission.get("duration", brief.get("duration")))
    normalized["hook"] = payload.get("hook", brief.get("hook", ""))
    normalized["cta"] = payload.get("cta", brief.get("cta", ""))
    normalized["evidence_refs"] = payload.get("evidence_refs", mission.get("evidence", []))
    normalized["assumptions"] = payload.get("assumptions", mission.get("assumptions", []))
    normalized["traceability"] = payload.get("traceability", {"generator": "marketing-shortform"})
    normalized["brand_outro"] = payload.get("brand_outro", {})
    normalized["media_assets"] = [
        {"asset_id": item.get("asset_id", item.get("id")), "approval_state": "approved"}
        for item in resolved_assets
    ]
    normalized["scenes"] = [
        {**scene, "id": scene.get("scene_id", scene.get("id")), "media_asset_id": scene.get("media_asset_id", scene.get("asset_id"))}
        for scene in scenes
    ]
    normalized["platform"] = "other" if payload.get("platform") == "generic" else payload.get("platform")
    if payload.get("approval_state") == "handoff_ready" and payload.get("representative_approval", {}).get("decision") == "approve":
        normalized["approval_state"] = "representative_approved"
    normalized["contract_version"] = "1.0"
    normalized["aspect_ratio"] = payload.get("aspect_ratio", "9:16")
    return normalized

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
