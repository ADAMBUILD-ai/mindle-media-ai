"""Generative, asset-bound architecture edit planning and durable MP4 assembly."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time
from typing import Any
from uuid import UUID, uuid4

from .architectural_video_pipeline import (
    ArchitectureProductionLedger,
    ArchitectureScene,
    ArchitectureVideoPlan,
    FFmpegDeliveryAdapter,
    preflight_production,
)
from .external_media_assets import file_sha256, load_asset_registry
from .product_runtime import file_record
from .workflow_planner import invoke_local_json_plan
from .video_analysis import analyze_video


def _programs() -> tuple[Path, Path]:
    package = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT", "").strip()
    ffmpeg = Path(package) / "tools/ffmpeg/ffmpeg.exe" if package else Path(shutil.which("ffmpeg") or "")
    ffprobe = Path(package) / "tools/ffmpeg/ffprobe.exe" if package else Path(shutil.which("ffprobe") or "")
    if not ffmpeg.is_file() or not ffprobe.is_file():
        raise ValueError("ARCHITECTURE_FFMPEG_UNAVAILABLE: 검증 가능한 FFmpeg와 FFprobe가 필요합니다.")
    return ffmpeg.resolve(), ffprobe.resolve()


def _probe(ffprobe: Path, source: Path) -> dict[str, Any]:
    return json.loads(subprocess.check_output([
        str(ffprobe), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(source)
    ], text=True, encoding="utf-8", timeout=30))


def _requested_contract(command: str) -> dict[str, Any]:
    text = command.casefold()
    durations = re.findall(r"(?<![\d.])(\d+(?:\.\d+)?)\s*초", text)
    if len(durations) > 1:
        raise ValueError("ARCHITECTURE_AMBIGUOUS_DURATION: 전체 영상 길이는 한 번만 지정하세요.")
    duration = float(durations[0]) if durations else None
    if duration is not None and not .25 <= duration <= 180:
        raise ValueError("ARCHITECTURE_UNSUPPORTED_DURATION: 전체 영상 길이는 0.25~180초입니다.")
    ratios = set(re.findall(r"(?:16\s*:\s*9|9\s*:\s*16)", text))
    if len(ratios) > 1:
        raise ValueError("ARCHITECTURE_AMBIGUOUS_ASPECT: 출력 비율을 하나만 지정하세요.")
    aspect = next(iter(ratios), None)
    if aspect:aspect = aspect.replace(" ", "")
    elif "원본 비율" in text or "원본비율" in text:aspect = "original"
    return {"duration_seconds": duration, "aspect": aspect}


def _visual_profile(source: Path, duration: float) -> dict[str, Any]:
    """Summarize decoded pixels for the planner without claiming semantic vision."""
    measured=analyze_video(source,min(3.0,duration))
    samples=measured["samples"]
    usable=[item for item in samples if item["usable"]]
    selected=usable or samples
    mean=lambda key:round(sum(float(item[key]) for item in selected)/len(selected),4)
    return {
        "method":measured["method"],"model_inference":False,"semantic_understanding":False,
        "sample_count":measured["sample_count"],"usable_ratio":round(len(usable)/len(samples),4),
        "mean_exposure":mean("exposure"),"mean_motion":mean("motion"),
        "mean_sharpness":mean("sharpness"),"measured_best_start":round(float(measured["start"]),3),
        "measured_window_seconds":round(float(measured["duration"]),3),
    }


def _measured_range(source: Path, duration: float) -> dict[str, Any]:
    measured=analyze_video(source,duration)
    start=round(float(measured["start"]),3)
    selected=[x for x in measured["samples"] if start<=float(x["second"])<start+duration]
    return {"start_seconds":start,"selection":{
        "method":measured["method"],"model_inference":False,"semantic_understanding":False,
        "sample_count":measured["sample_count"],"selected_sample_count":len(selected),
        "mean_score":round(sum(float(x["score"]) for x in selected)/len(selected),4) if selected else 0.0,
        "reason":measured["reason"],
    }}


def _add_measured_ranges(plan: dict[str, Any], catalog: list[dict[str, Any]], provider=None) -> dict[str, Any]:
    sources={item["source_id"]:item for item in catalog};provider=provider or (lambda source,duration,_sha:_measured_range(source,duration))
    enriched=[]
    for scene in plan["scenes"]:
        source=sources[scene["source_id"]]
        measured=provider(Path(source["path"]),scene["duration_seconds"],source["sha256"])
        start=float(measured["start_seconds"])
        if not math.isfinite(start) or start<0 or start+scene["duration_seconds"]>float(source["duration_seconds"])+.05:
            raise ValueError("ARCHITECTURE_MEASURED_RANGE_INVALID")
        enriched.append({**scene,**measured})
    return {**plan,"scenes":enriched}


def validate_generated_architecture_plan(command: str, parsed: dict[str, Any], catalog: list[dict[str, Any]]) -> dict[str, Any]:
    """Reject invented sources, omitted inputs, and altered explicit constraints."""
    if parsed.get("error"):
        raise ValueError("ARCHITECTURE_PLANNER_UNSUPPORTED: " + str(parsed["error"]))
    if set(parsed) - {"aspect", "scenes", "error"}:
        raise ValueError("ARCHITECTURE_PLAN_UNKNOWN_FIELD")
    if parsed.get("aspect") not in {"original", "16:9", "9:16"}:
        raise ValueError("ARCHITECTURE_PLAN_INVALID_ASPECT")
    scenes = parsed.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 12:
        raise ValueError("ARCHITECTURE_PLAN_SCENE_COUNT")
    sources = {item["source_id"]: item for item in catalog}
    used: list[str] = []
    normalized = []
    for index, scene in enumerate(scenes, 1):
        if not isinstance(scene, dict) or set(scene) != {"source_id", "duration_seconds"}:
            raise ValueError("ARCHITECTURE_PLAN_SCENE_SHAPE")
        source_id = str(scene["source_id"])
        if source_id not in sources or source_id in used:
            raise ValueError("ARCHITECTURE_PLAN_SOURCE_MISMATCH")
        try:duration = float(scene["duration_seconds"])
        except (TypeError, ValueError):raise ValueError("ARCHITECTURE_PLAN_INVALID_DURATION")
        available = float(sources[source_id]["duration_seconds"])
        if not .25 <= duration <= min(30, available + .01):
            raise ValueError("ARCHITECTURE_PLAN_DURATION_EXCEEDS_SOURCE")
        used.append(source_id)
        normalized.append({"scene_id": f"scene-{index:02d}", "source_id": source_id, "duration_seconds": duration})
    if set(used) != set(sources):
        raise ValueError("ARCHITECTURE_PLAN_INCOMPLETE: 선택한 모든 영상 자료를 한 번씩 사용해야 합니다.")
    requested = _requested_contract(command)
    if requested["aspect"] and parsed["aspect"] != requested["aspect"]:
        raise ValueError("ARCHITECTURE_PLAN_ASPECT_MISMATCH")
    total = sum(item["duration_seconds"] for item in normalized)
    if requested["duration_seconds"] is not None and abs(total - requested["duration_seconds"]) > .05:
        raise ValueError("ARCHITECTURE_PLAN_TOTAL_DURATION_MISMATCH")
    return {"aspect": parsed["aspect"], "scenes": normalized, "total_duration_seconds": total,
            "validated_request": requested}


def apply_explicit_duration_guardrail(command: str, parsed: dict[str, Any], catalog: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Fit model-proposed scene weights to an explicit total without inventing sources or order."""
    requested=_requested_contract(command);target=requested["duration_seconds"]
    if target is None or not isinstance(parsed.get("scenes"),list):return parsed,[]
    sources={item["source_id"]:item for item in catalog};scenes=parsed["scenes"]
    if (not scenes or any(not isinstance(x,dict) or set(x)!={"source_id","duration_seconds"} for x in scenes)
            or len({str(x["source_id"]) for x in scenes})!=len(scenes)
            or {str(x["source_id"]) for x in scenes}!=set(sources)):
        return parsed,[]
    try:weights=[float(x["duration_seconds"]) for x in scenes]
    except (TypeError,ValueError):return parsed,[]
    if any(not math.isfinite(x) or x<=0 for x in weights):return parsed,[]
    if abs(sum(weights)-target)<=.05:return parsed,[]
    minimum=.25;caps=[min(30.0,float(sources[str(x["source_id"])]["duration_seconds"])+.01) for x in scenes]
    if target < minimum*len(scenes)-.001 or target > sum(caps)+.001:return parsed,[]
    allocated=[minimum]*len(scenes);remaining=target-sum(allocated);active=set(range(len(scenes)))
    while remaining>1e-9 and active:
        weight=sum(weights[i] for i in active);progress=0.0
        for i in list(active):
            share=remaining*(weights[i]/weight) if weight else remaining/len(active)
            add=min(share,caps[i]-allocated[i]);allocated[i]+=add;progress+=add
            if caps[i]-allocated[i]<=1e-9:active.remove(i)
        remaining-=progress
        if progress<=1e-9:break
    if abs(sum(allocated)-target)>.001:return parsed,[]
    allocated[-1]+=target-sum(allocated)
    adjusted={**parsed,"scenes":[{**scene,"duration_seconds":round(allocated[i],6)} for i,scene in enumerate(scenes)]}
    return adjusted,[{"field":"scene.duration_seconds","reason":"EXPLICIT_TOTAL_DURATION",
                      "model_total_seconds":sum(weights),"applied_total_seconds":target,
                      "method":"PROPORTIONAL_WITH_SOURCE_CAPS"}]


def make_architecture_plan(data_root: Path, command: str, catalog: list[dict[str, Any]], project_id: str,
                           range_provider=None) -> dict[str, Any]:
    command = str(command).strip()
    if not 1 <= len(command) <= 4000:
        raise ValueError("건축 영상 지시는 1~4000자입니다.")
    UUID(project_id)
    if not 1 <= len(catalog) <= 12:
        raise ValueError("건축 영상 계획에는 1~12개 영상 자료가 필요합니다.")
    requested = _requested_contract(command)
    if requested["duration_seconds"] and requested["duration_seconds"] > sum(float(x["duration_seconds"]) for x in catalog) + .05:
        raise ValueError("ARCHITECTURE_SOURCE_TOO_SHORT: 요청 길이보다 실제 원본 영상이 짧습니다.")
    schema={"type":"object","properties":{
        "aspect":{"enum":["original","16:9","9:16"]},
        "scenes":{"type":"array","minItems":1,"maxItems":12,"items":{"type":"object","properties":{
            "source_id":{"type":"string"},"duration_seconds":{"type":"number"}},
            "required":["source_id","duration_seconds"],"additionalProperties":False}},
        "error":{"type":"string"}},"required":["aspect","scenes"],"additionalProperties":False}
    catalog_prompt=[{"source_id":x["source_id"],"filename":x["filename"],"duration_seconds":x["duration_seconds"],
                     "width":x["width"],"height":x["height"],"orientation":x["orientation"],
                     "visual_profile":x["visual_profile"]} for x in catalog]
    instructions=("You are the local MINDLE architecture video planner. Return JSON only. "
      "Arrange every supplied source exactly once into a concise architecture promotion. "
      "Use only source_id values in the catalog. Never emit paths, tools, shell commands, prompts, or new media. "
      "Each duration must be 0.25 to 30 seconds and cannot exceed that source duration. "
      "Honor an explicit total duration and aspect exactly. If no aspect is explicit choose 16:9. "
      "Use the measured visual_profile to choose a deliberate order; it is numeric evidence, not semantic recognition. "
      "This plan edits existing clips only; it does not claim image/video generation. "
      "Unsupported or contradictory requests should use error.")
    exact_contract={"required_source_ids":[x["source_id"] for x in catalog],**requested}
    prompt=("<|im_start|>system\n"+instructions+"<|im_end|>\n<|im_start|>user\nCATALOG="+
            json.dumps(catalog_prompt,ensure_ascii=False)+"\nEXACT_CONTRACT="+
            json.dumps(exact_contract,ensure_ascii=False)+
            "\nEvery required_source_id must appear exactly once. When duration_seconds is set, "
            "the scene duration_seconds values must sum to it exactly.\nREQUEST="+command+
            "<|im_end|>\n<|im_start|>assistant\n")
    parsed, raw, settings = invoke_local_json_plan(data_root, prompt, schema, max_tokens=1024, timeout=120)
    parsed,adjustments=apply_explicit_duration_guardrail(command,parsed,catalog)
    validated = _add_measured_ranges(validate_generated_architecture_plan(command, parsed, catalog),catalog,range_provider)
    plan_id=str(uuid4());folder=Path(data_root)/"architecture-agent/plans";folder.mkdir(parents=True,exist_ok=True)
    receipt={"plan_id":plan_id,"project_id":project_id,"plan_source":"LOCAL_GENERATIVE_INFERENCE",
             "command_sha256":hashlib.sha256(command.encode()).hexdigest(),"model_id":settings.get("model_id"),
             "model_sha256":settings["model_sha256"],"revision":settings["revision"],"license":settings["license"],
             "executable_sha256":settings["executable_sha256"],"runtime_sha256":settings.get("runtime_sha256"),
             "raw_response_sha256":hashlib.sha256(raw.encode()).hexdigest(),"catalog":catalog,
             "constraint_adjustments":adjustments,**validated}
    (folder/(plan_id+".json")).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (folder/(plan_id+".response.txt")).write_text(raw,encoding="utf-8")
    return receipt


class ArchitectureAgentRuntime:
    """Owns the persistent queue and publishes only validated existing-clip assemblies."""
    def __init__(self, product_service, repo_root: Path):
        self.service=product_service;self.repo_root=Path(repo_root).resolve()
        self.root=(self.service.root/"architecture-agent").resolve();self.root.mkdir(parents=True,exist_ok=True)
        self.registry=load_asset_registry(self.repo_root/"external_assets/media-production/ASSET_REGISTRY.json")
        self.ledger=ArchitectureProductionLedger(self.root)
        self.analysis_lock=threading.RLock();self.wake=threading.Event();self.closed=False
        self.thread=threading.Thread(target=self._loop,name="mindle-architecture-agent",daemon=True);self.thread.start()

    def _analysis_cache(self, digest: str) -> tuple[Path, dict[str, Any]]:
        folder=self.root/"analysis";folder.mkdir(exist_ok=True);path=folder/(digest+".json")
        value={"schema":"MINDLE_ARCHITECTURE_MEASURED_ANALYSIS_V1","source_sha256":digest,"profile":None,"ranges":{}}
        if path.is_file():
            try:
                loaded=json.loads(path.read_text(encoding="utf-8"))
                if loaded.get("schema")==value["schema"] and loaded.get("source_sha256")==digest and isinstance(loaded.get("ranges"),dict):value=loaded
            except (OSError,ValueError,TypeError):pass
        return path,value

    @staticmethod
    def _write_analysis_cache(path: Path, value: dict[str, Any]) -> None:
        pending=path.with_suffix("."+str(uuid4())+".tmp")
        try:pending.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");os.replace(pending,path)
        finally:pending.unlink(missing_ok=True)

    def _cached_profile(self, source: Path, duration: float, digest: str) -> dict[str, Any]:
        with self.analysis_lock:
            path,value=self._analysis_cache(digest)
            if not isinstance(value.get("profile"),dict):
                value["profile"]=_visual_profile(source,duration);self._write_analysis_cache(path,value)
            return value["profile"]

    def _cached_range(self, source: Path, duration: float, digest: str) -> dict[str, Any]:
        key=f"{float(duration):.6f}"
        with self.analysis_lock:
            path,value=self._analysis_cache(digest)
            if not isinstance(value["ranges"].get(key),dict):
                value["ranges"][key]=_measured_range(source,duration);self._write_analysis_cache(path,value)
            return value["ranges"][key]

    def catalog(self, job_ids: list[str]) -> list[dict[str, Any]]:
        if not isinstance(job_ids,list) or not job_ids or len(job_ids)>100 or len(set(job_ids)) != len(job_ids):
            raise ValueError("서로 다른 완료 작업 목록이 필요합니다.")
        _,ffprobe=_programs();result=[]
        for identifier in job_ids:
            record=self.service.records.get(str(identifier))
            if not record or record.get("status")!="TESTED_PASS":
                raise ValueError("완료된 작업만 건축 영상 자료로 사용할 수 있습니다.")
            if record.get("lane")!="video" or record.get("operation") in {"transcribe","narration"}:continue
            artifact=record.get("preview_output",record.get("primary_output",{}));source=Path(artifact.get("path","")).resolve()
            if not source.is_file() or not source.is_relative_to(self.service.root.resolve()) or file_sha256(source)!=artifact.get("sha256"):
                raise ValueError("건축 영상 자료 무결성 확인에 실패했습니다.")
            info=_probe(ffprobe,source);video=next((x for x in info.get("streams",[]) if x.get("codec_type")=="video"),None)
            duration=float(info.get("format",{}).get("duration",0))
            if not video or duration < .25:raise ValueError("유효한 영상 스트림과 길이가 필요합니다.")
            result.append({"source_id":f"input-{len(result)+1:02d}","job_id":record["job_id"],"filename":source.name,
                           "path":str(source),"sha256":artifact["sha256"],"duration_seconds":duration,
                           "width":int(video["width"]),"height":int(video["height"]),
                           "orientation":"landscape" if int(video["width"])>int(video["height"]) else "portrait" if int(video["height"])>int(video["width"]) else "square",
                           "visual_profile":self._cached_profile(source,duration,artifact["sha256"])})
        if not 1 <= len(result) <= 12:raise ValueError("1~12개의 완료 영상이 필요합니다.")
        return result

    def plan(self, body: dict[str, Any]) -> dict[str, Any]:
        project_id=str(body.get("project_id") or uuid4());UUID(project_id)
        job_ids=list(dict.fromkeys(body.get("job_ids",[])))
        receipt=make_architecture_plan(self.service.root,str(body.get("command","")),self.catalog(job_ids),project_id,self._cached_range)
        receipt["project_job_ids"]=job_ids
        path=self.root/"plans"/(receipt["plan_id"]+".json")
        path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return receipt

    def submit(self, body: dict[str, Any]) -> dict[str, Any]:
        plan_id=str(UUID(str(body.get("plan_id",""))))
        path=self.root/"plans"/(plan_id+".json")
        if not path.is_file():raise ValueError("검증된 건축 영상 계획을 찾을 수 없습니다.")
        receipt=json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("plan_id")!=plan_id or receipt.get("plan_source")!="LOCAL_GENERATIVE_INFERENCE":
            raise ValueError("건축 영상 계획 identity가 일치하지 않습니다.")
        for key,size in (("model_sha256",64),("executable_sha256",64),("raw_response_sha256",64),("revision",40)):
            if not re.fullmatch(f"[0-9a-f]{{{size}}}",str(receipt.get(key,""))):raise ValueError("건축 영상 계획 provenance가 유효하지 않습니다.")
        response=self.root/"plans"/(plan_id+".response.txt")
        if not response.is_file() or hashlib.sha256(response.read_bytes()).hexdigest()!=receipt["raw_response_sha256"]:
            raise ValueError("건축 영상 계획 원문 무결성 확인에 실패했습니다.")
        current=self.catalog([x["job_id"] for x in receipt.get("catalog",[])])
        catalog={x["source_id"]:x for x in current}
        if any(current[index] != saved for index,saved in enumerate(receipt.get("catalog",[]))):
            raise ValueError("건축 영상 자료가 계획 이후 변경됐습니다.")
        checked=_add_measured_ranges(validate_generated_architecture_plan("",{"aspect":receipt.get("aspect"),"scenes":[
            {"source_id":x.get("source_id"),"duration_seconds":x.get("duration_seconds")} for x in receipt.get("scenes",[])]},current),current,self._cached_range)
        if checked["scenes"]!=receipt.get("scenes") or abs(checked["total_duration_seconds"]-receipt.get("total_duration_seconds",-1))>.001:
            raise ValueError("저장된 건축 영상 계획 의미 계약이 일치하지 않습니다.")
        if any(job_id not in self.service.records for job_id in receipt.get("project_job_ids",[])):
            raise ValueError("건축 영상 프로젝트 자료가 누락됐습니다.")
        scenes=tuple(ArchitectureScene(item["scene_id"],"existing_clip",Path(catalog[item["source_id"]]["path"]),
                    item["duration_seconds"],catalog[item["source_id"]]["sha256"],start_seconds=item["start_seconds"]) for item in receipt["scenes"])
        output=self.root/"outputs"/(plan_id+".mp4")
        plan=ArchitectureVideoPlan(receipt["project_id"],receipt["aspect"],scenes,output)
        preflight=preflight_production(plan,self.registry,self.root.parent)
        # A verified plan is single-use/idempotent even if the browser retries with
        # another transport request ID.
        task=self.ledger.submit("architecture-plan:"+plan_id,plan,preflight)
        task["plan_id"]=plan_id;task["planner_receipt"]=receipt
        self.ledger._put(task)
        if task["state"]=="QUEUED":self.wake.set()
        return task

    def get(self,identifier: str)->dict[str,Any]:return self.ledger.get(identifier)
    def list(self)->list[dict[str,Any]]:return self.ledger.list()
    def cancel(self,identifier: str)->dict[str,Any]:
        value=self.ledger.cancel(identifier);self.wake.set();return value

    def _loop(self):
        while not self.closed:
            queued=next((x for x in reversed(self.ledger.list()) if x["state"]=="QUEUED"),None)
            if not queued:self.wake.wait(.5);self.wake.clear();continue
            self._execute(queued["production_id"])

    def _execute(self,identifier: str):
        record_added=None;record_folder=None;project_path=None;previous_project=None
        try:
            value=self.ledger.start(identifier);plan_value=value["plan"]
            scenes=tuple(ArchitectureScene(x["scene_id"],x["engine"],Path(x["source"]),x["duration_seconds"],
                        x["source_sha256"],x.get("prompt"),x.get("camera"),x.get("start_seconds",0)) for x in plan_value["scenes"])
            ffmpeg,ffprobe=_programs();adapter=FFmpegDeliveryAdapter(ffmpeg,ffprobe,self.service.root,file_sha256(ffmpeg),file_sha256(ffprobe))
            aspect=plan_value["aspect"]
            if aspect=="9:16":width,height=720,1280
            elif aspect=="original":
                info=_probe(ffprobe,scenes[0].source);video=next(x for x in info["streams"] if x["codec_type"]=="video")
                width,height=int(video["width"])//2*2,int(video["height"])//2*2
            else:width,height=1280,720
            delivery=adapter.assemble_existing_clips(
                scenes,Path(plan_value["output"]),aspect,width,height,
                cancel_check=lambda:self.closed or self.ledger.get(identifier)["state"]=="CANCEL_REQUESTED")
            if self.ledger.get(identifier)["state"]=="CANCEL_REQUESTED":self.ledger.finish_cancel(identifier);return
            planner=value["planner_receipt"];job_id=str(uuid4());output=Path(delivery["output"]["path"])
            planner_inference=planner.get("plan_source")=="LOCAL_GENERATIVE_INFERENCE"
            record={"status":"TESTED_PASS","job_id":job_id,"lane":"video","operation":"architecture_ai_assembly",
                    "command":"로컬 생성형 건축 영상 장면 계획과 조립","input":file_record(scenes[0].source),
                    "primary_output":file_record(output),"outputs":[file_record(output)],
                    "runtime_result":{"planning_engine":planner.get("model_id"),"model_inference":planner_inference,
                        "planner_model_sha256":planner["model_sha256"],"planner_raw_response_sha256":planner["raw_response_sha256"],
                        "scene_order":delivery["scene_order"],"total_duration_seconds":planner["total_duration_seconds"],
                        "assembly_engine":"FFmpeg","assembly_model_inference":False,"delivery":delivery}}
            folder=self.service.jobs/job_id;folder.mkdir();(folder/"JOB_EVIDENCE.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            record_folder=folder;record_added=job_id;self.service.records[job_id]=record
            project_path=self.service.projects/(planner["project_id"]+".json")
            previous_project=project_path.read_bytes() if project_path.is_file() else None
            saved=self.service.save_project({"project_id":planner["project_id"],
                                             "job_ids":[*planner.get("project_job_ids",[x["job_id"] for x in planner["catalog"]]),job_id]})
            self.ledger.complete(identifier,{**delivery,"job_id":job_id,"project_id":saved["project_id"],
                                            "planner_model_inference":planner_inference,"planner_plan_id":planner["plan_id"]})
        except Exception as error:
            if record_added:
                self.service.records.pop(record_added,None)
                if record_folder:shutil.rmtree(record_folder,ignore_errors=True)
            if project_path:
                if previous_project is None:project_path.unlink(missing_ok=True)
                else:
                    pending=project_path.with_suffix(".architecture-rollback.tmp");pending.write_bytes(previous_project);os.replace(pending,project_path)
            try:
                current=self.ledger.get(identifier)
                if current["state"]=="CANCEL_REQUESTED":self.ledger.finish_cancel(identifier)
                elif current["state"]=="RUNNING":self.ledger.fail(identifier,str(error))
            except Exception:pass

    def busy(self)->bool:return any(x["state"] in ArchitectureProductionLedger.ACTIVE for x in self.ledger.list())
    def close(self):
        self.closed=True;self.wake.set();self.thread.join(timeout=3);self.ledger.close()
