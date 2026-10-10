"""External-only runner verification; preserve frozen base PASS and fail closed."""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/evidence/media-ai-shortform-external-integration-closeout-20261008"
EPOCH="MEDIA-AI-20261008-SHORTFORM-EXTERNAL-INTEGRATION-CLOSEOUT-R1"

def write(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validator=subprocess.run(["python","scripts/validate_pc_work_control_plane.py"],cwd=ROOT,capture_output=True,text=True)
    (OUT/"CONTROL_PLANE.log").write_text(validator.stdout+validator.stderr,encoding="utf-8")
    if validator.returncode:raise RuntimeError("CONTROL_PLANE_MISMATCH_BLOCKED")
    state=json.loads((ROOT/"CURRENT_PC_WORK_STATE.json").read_text())
    if state["control_plane_epoch"]!=EPOCH:raise RuntimeError("wrong external epoch")
    base=os.environ.get("MARKETING_SHORTFORM_BASE_URL","").strip().rstrip("/")
    token_present=bool(os.environ.get("MARKETING_SHORTFORM_BRIDGE_TOKEN","").strip())
    provider={"configured":bool(base),"token_present":token_present,"actual_runner":True,
              "default_localhost_substituted":False,"network_attempted":False,
              "captured_at":datetime.now(timezone.utc).isoformat(),"mock_used":False}
    blockers=[]
    if not base:
        provider.update(status="BLOCKED_MARKETING_PROVIDER_UNREACHABLE",reason="MARKETING_SHORTFORM_BASE_URL_MISSING")
        blockers.append("MARKETING_SHORTFORM_BASE_URL repository variable is empty in the actual runner")
    else:
        parsed=urlsplit(base)
        if parsed.scheme not in {"http","https"} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            provider.update(status="BLOCKED_MARKETING_PROVIDER_UNREACHABLE",reason="INVALID_PROVIDER_BASE_URL")
            blockers.append("actual provider URL must be a valid credential-free HTTP(S) base URL")
        else:
            path=os.environ.get("MARKETING_SHORTFORM_HEALTH_PATH","").strip() or "/v1/shortform/health"
            if not path.startswith("/") or "?" in path or "#" in path:raise ValueError("invalid provider health path")
            provider.update(base_url=base,health_path=path,method="GET",request_headers={"Accept":"application/json"},network_attempted=True)
            try:
                with urlopen(Request(base+path,headers={"Accept":"application/json"}),timeout=10) as response:
                    body=response.read(1024*1024+1)
                    provider.update(http_status=response.status,response_sha256=hashlib.sha256(body).hexdigest(),reachable=True)
                    provider["status"]="PASS" if response.status==200 else "BLOCKED_MARKETING_PROVIDER_UNREACHABLE"
            except HTTPError as error:
                provider.update(http_status=error.code,reachable=True,status="BLOCKED_MARKETING_PROVIDER_UNREACHABLE",reason="PROVIDER_HEALTH_HTTP_NOT_SUCCESS")
            except (URLError,TimeoutError,OSError):
                provider.update(reachable=False,status="BLOCKED_MARKETING_PROVIDER_UNREACHABLE",reason="PROVIDER_CONNECTION_FAILED")
            if provider["status"]!="PASS":blockers.append("actual provider health/reachability gate failed")
    if not token_present:blockers.append("MARKETING_SHORTFORM_BRIDGE_TOKEN Actions secret is absent in the actual runner")
    write("PROVIDER_REACHABILITY.json",provider)
    marketing={"status":"NOT_REACHED","token_present":token_present,"authentication_tested":False,
               "reason":provider["status"] if provider["status"]!="PASS" else ("BLOCKED_MARKETING_BRIDGE_TOKEN_MISSING" if not token_present else "LIVE_CONTRACT_RUNTIME_VERIFY_REQUIRED"),
               "request_sent":False,"secret_values_recorded":False}
    write("MARKETING_HTTP_RESULT.json",marketing)
    for name in ("AVORA_APPROVED_ASSET_RESULT.json","SHORTFORM_9X16_BROWSER_PREVIEW.json","REPRESENTATIVE_APPROVAL_RESULT.json","APPROVED_MP4_EXPORT_RESULT.json"):
        write(name,{"status":"NOT_REACHED","blocked_by":marketing["reason"],"mock_used":False,"fabricated_approval":False})
    write("REGRESSION_RESULT.json",{"status":"FROZEN_BASE_PASS_REUSED","product_runtime_UI_changed":False,
        "base_gates_rerun":False,"photo_models_rerun":False,"source_run":37738880868,
        "source_commit":"99a9cd4fcdced32a728db06f0692a394c9a4dfd2","previous_python_pass":66,"previous_UI_pass":2,
        "control_plane":"PASS","new_epoch_routing_only":True})
    status="BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION" if blockers else "FULL_PRODUCT_E2E_PASS_FORBIDDEN"
    evidence={"status":status,"epoch":EPOCH,"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "run_id":os.environ.get("GITHUB_RUN_ID"),"missing_dependencies":blockers,
        "provider_gate":provider["status"],"marketing_gate":marketing["status"],"full_product_pass":False,
        "base_product_pass_frozen":True,"main_changed":False,"pr23":"HOLD / DO NOT MERGE",
        "employee_package_rebuilt":False,"mock_used":False,"auto_publish":False,"ad_spend":False}
    write("EVIDENCE.json",evidence)
    print(status)
    print("provider_configured="+str(bool(base)).lower()+" token_present="+str(token_present).lower())
    if not blockers:print("External inputs available; real contract/asset/approval/MP4 runtime verification remains required.")
    raise SystemExit(3)

if __name__=="__main__":main()
