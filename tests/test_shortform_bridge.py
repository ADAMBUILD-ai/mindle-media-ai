from dataclasses import replace
import pytest

from media_ai.marketing_shortform_gateway import build_marketing_shortform_request
from media_ai.shortform_bridge import ShortformContractError, authorize_export, read_shortform_contract

def contract():
    assets = [
        {"asset_id": "plan-01", "approval_state": "approved"},
        {"asset_id": "process-01", "approval_state": "approved"},
        {"asset_id": "model-01", "approval_state": "approved"},
    ]
    scenes = [
        {"id":"scene_01","start_sec":0,"end_sec":3,"media_asset_id":"plan-01","subtitle":"Hook","voiceover":"Hook"},
        {"id":"scene_02","start_sec":3,"end_sec":6,"media_asset_id":"plan-01","subtitle":"Problem","voiceover":"Problem"},
        {"id":"scene_03","start_sec":6,"end_sec":11,"media_asset_id":"process-01","subtitle":"Solution","voiceover":"Solution"},
        {"id":"scene_04","start_sec":11,"end_sec":13,"media_asset_id":"model-01","subtitle":"Result","voiceover":"Result"},
        {"id":"scene_05","start_sec":13,"end_sec":15,"media_asset_id":"model-01","subtitle":"CTA","voiceover":"CTA"},
    ]
    return {
        "contract_version":"1.0","project_id":"avora-01","campaign_id":"cmp-01","product":"AVORA",
        "target":"architects","campaign_goal":"product_intro","duration":15,"platform":"youtube_shorts",
        "aspect_ratio":"9:16","hook":"Hook","scenes":scenes,"media_assets":assets,"cta":"CTA",
        "brand_outro":{"brand":"MINDLE ADA"},"approval_state":"draft","evidence_refs":["ev-01"],
        "assumptions":[],"traceability":{"generator":"marketing-ai"},
    }

def test_reads_marketing_contract_into_media_plan():
    plan = read_shortform_contract(contract())
    assert plan.duration == 15
    assert plan.aspect_ratio == "9:16"
    assert len(plan.scenes) == 5
    assert plan.export_authorized is False

def test_rejects_unapproved_or_missing_scene_asset():
    payload = contract()
    payload["media_assets"][1]["approval_state"] = "pending"
    with pytest.raises(ShortformContractError, match="unapproved asset"):
        read_shortform_contract(payload)

def test_rejects_timeline_gap():
    payload = contract()
    payload["scenes"][1]["start_sec"] = 4
    with pytest.raises(ShortformContractError, match="continuous"):
        read_shortform_contract(payload)

def test_export_requires_representative_approval():
    plan = read_shortform_contract(contract())
    with pytest.raises(ShortformContractError, match="approval required"):
        authorize_export(plan)
    approved = authorize_export(replace(plan, approval_state="representative_approved"))
    assert approved.export_authorized is True

def test_media_entry_builds_fail_closed_marketing_request():
    request = build_marketing_shortform_request("AVORA를 건축사 대상으로 15초 광고로 만들어", project_id="avora-01")
    assert request["entrypoint"] == "media_ai"
    assert request["requested_output"] == "shortform_bridge_contract"
    assert request["allow_publish"] is False
    assert request["allow_ad_spend"] is False
