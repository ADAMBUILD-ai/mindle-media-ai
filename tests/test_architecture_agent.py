import base64
import hashlib
import shutil
import subprocess
import time
from pathlib import Path
import io
import json

import pytest

from media_ai.architecture_agent import ArchitectureAgentRuntime, apply_explicit_duration_guardrail, validate_generated_architecture_plan
from media_ai.architectural_video_pipeline import ProductionCancelled
from media_ai.product_runtime import ProductJobService


def _catalog():
    return [
        {"source_id":"input-01","duration_seconds":2,"filename":"arrival.mp4","width":320,"height":180},
        {"source_id":"input-02","duration_seconds":3,"filename":"lobby.mp4","width":180,"height":320},
    ]


def test_generated_architecture_plan_binds_every_source_and_explicit_contract():
    parsed={"aspect":"16:9","scenes":[
        {"source_id":"input-02","duration_seconds":2},
        {"source_id":"input-01","duration_seconds":1},
    ]}
    result=validate_generated_architecture_plan("두 영상으로 3초 16:9 건축 홍보 영상",parsed,_catalog())
    assert [x["source_id"] for x in result["scenes"]]==["input-02","input-01"]
    assert result["total_duration_seconds"]==3


def test_model_prompt_contains_machine_readable_exact_contract(monkeypatch,tmp_path):
    from media_ai import architecture_agent
    captured={}
    raw='{"aspect":"16:9","scenes":[{"source_id":"input-01","duration_seconds":1},{"source_id":"input-02","duration_seconds":1}]}\n'
    settings={"model_id":"fixture-qwen","model_sha256":"a"*64,"revision":"b"*40,"license":"Apache-2.0",
              "executable_sha256":"c"*64,"runtime_sha256":"d"*64}
    def invoke(_root,prompt,_schema,**_kwargs):
        captured["prompt"]=prompt
        return json.loads(raw),raw,settings
    monkeypatch.setattr(architecture_agent,"invoke_local_json_plan",invoke)
    monkeypatch.setattr(architecture_agent,"_add_measured_ranges",lambda plan,_catalog,_provider=None:plan)
    catalog=[{**item,"orientation":"landscape","visual_profile":{"mean_motion":0.0}} for item in _catalog()]
    value=architecture_agent.make_architecture_plan(tmp_path,"두 영상으로 2초 16:9 건축 홍보 영상",catalog,"00000000-0000-0000-0000-000000000001")
    assert value["total_duration_seconds"]==2
    exact=captured["prompt"].split("EXACT_CONTRACT=",1)[1].split("\n",1)[0]
    assert json.loads(exact)=={"required_source_ids":["input-01","input-02"],"duration_seconds":2.0,"aspect":"16:9"}
    response=tmp_path/"architecture-agent/plans"/(value["plan_id"]+".response.txt")
    assert response.read_bytes()==raw.encode("utf-8")
    assert hashlib.sha256(response.read_bytes()).hexdigest()==value["raw_response_sha256"]


@pytest.mark.parametrize("parsed,error",[
    ({"aspect":"16:9","scenes":[{"source_id":"invented","duration_seconds":1},{"source_id":"input-02","duration_seconds":2}]},"SOURCE_MISMATCH"),
    ({"aspect":"16:9","scenes":[{"source_id":"input-01","duration_seconds":3},{"source_id":"input-02","duration_seconds":1}]},"DURATION_EXCEEDS"),
    ({"aspect":"9:16","scenes":[{"source_id":"input-01","duration_seconds":1},{"source_id":"input-02","duration_seconds":2}]},"ASPECT_MISMATCH"),
    ({"aspect":"16:9","scenes":[{"source_id":"input-01","duration_seconds":1},{"source_id":"input-02","duration_seconds":1}]},"TOTAL_DURATION_MISMATCH"),
    ({"aspect":"16:9","scenes":[{"source_id":"input-01","duration_seconds":1}]},"INCOMPLETE"),
])
def test_generated_architecture_plan_rejects_model_drift(parsed,error):
    with pytest.raises(ValueError,match=error):
        validate_generated_architecture_plan("3초 16:9 건축 홍보 영상",parsed,_catalog())


def test_explicit_duration_guardrail_preserves_model_order_and_fits_total():
    parsed={"aspect":"16:9","scenes":[
        {"source_id":"input-02","duration_seconds":3},
        {"source_id":"input-01","duration_seconds":2},
    ]}
    adjusted,receipt=apply_explicit_duration_guardrail("두 영상으로 2초 16:9 건축 홍보 영상",parsed,_catalog())
    assert [x["source_id"] for x in adjusted["scenes"]]==["input-02","input-01"]
    assert sum(x["duration_seconds"] for x in adjusted["scenes"])==2
    assert receipt==[{"field":"scene.duration_seconds","reason":"EXPLICIT_TOTAL_DURATION",
                      "model_total_seconds":5.0,"applied_total_seconds":2.0,
                      "method":"PROPORTIONAL_WITH_SOURCE_CAPS"}]


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"),reason="FFmpeg unavailable")
def test_local_model_plan_to_durable_mp4_and_project(monkeypatch,tmp_path):
    service=ProductJobService(tmp_path/"data","")
    jobs=[]
    for color in ("blue","red"):
        path=tmp_path/(color+".mp4")
        subprocess.run([shutil.which("ffmpeg"),"-v","error","-f","lavfi","-i",f"color=c={color}:s=160x90:r=12",
                        "-t","0.6","-c:v","libx264","-pix_fmt","yuv420p","-y",str(path)],check=True,timeout=30)
        jobs.append(service.import_media({"kind":"video","filename":path.name,
                    "content_base64":base64.b64encode(path.read_bytes()).decode()}))
    from PIL import Image
    photo=io.BytesIO();Image.new("RGB",(32,48),"white").save(photo,"PNG")
    photo_job=service.import_media({"kind":"photo","filename":"reference.png",
                                    "content_base64":base64.b64encode(photo.getvalue()).decode()})
    from media_ai import architecture_agent
    settings={"model_id":"fixture-qwen","model_sha256":"a"*64,"revision":"b"*40,"license":"Apache-2.0",
              "executable_sha256":"c"*64,"runtime_sha256":"d"*64}
    raw='{"aspect":"16:9","scenes":[{"source_id":"input-02","duration_seconds":0.5},{"source_id":"input-01","duration_seconds":0.5}]}'
    monkeypatch.setattr(architecture_agent,"invoke_local_json_plan",lambda *args,**kw:(__import__("json").loads(raw),raw,settings))
    real_analyze=architecture_agent.analyze_video;analysis_calls=[]
    monkeypatch.setattr(architecture_agent,"analyze_video",lambda source,duration:(analysis_calls.append((str(source),duration)) or real_analyze(source,duration)))
    runtime=ArchitectureAgentRuntime(service,Path(__file__).resolve().parents[1])
    try:
        context_ids=[photo_job["job_id"],*[x["job_id"] for x in jobs]]
        plan=runtime.plan({"command":"두 영상으로 1초 16:9 건축 홍보 영상","job_ids":context_ids})
        assert plan["plan_source"]=="LOCAL_GENERATIVE_INFERENCE"
        assert [x["source_id"] for x in plan["scenes"]]==["input-02","input-01"]
        assert all(x["selection"]["model_inference"] is False for x in plan["scenes"])
        assert all(x["start_seconds"]>=0 for x in plan["scenes"])
        assert all(x["visual_profile"]["semantic_understanding"] is False for x in plan["catalog"])
        task=runtime.submit({"request_id":"architecture-real-assembly","plan_id":plan["plan_id"]})
        assert runtime.submit({"request_id":"browser-retry-new-id","plan_id":plan["plan_id"]})["production_id"]==task["production_id"]
        assert len(analysis_calls)==4
        end=time.monotonic()+30
        while time.monotonic()<end:
            task=runtime.get(task["production_id"])
            if task["state"] in {"SUCCEEDED","FAILED","CANCELLED","INTERRUPTED"}:break
            time.sleep(.05)
        assert task["state"]=="SUCCEEDED",task
        output=Path(task["receipt"]["output"]["path"])
        assert output.is_file() and hashlib.sha256(output.read_bytes()).hexdigest()==task["receipt"]["output"]["sha256"]
        assert task["receipt"]["scene_order"]==["scene-01","scene-02"]
        project=service.projects/(task["receipt"]["project_id"]+".json")
        assert project.is_file()
        assert set(json.loads(project.read_text())["job_ids"])==set([*context_ids,task["receipt"]["job_id"]])
        record=service.records[task["receipt"]["job_id"]]
        assert record["runtime_result"]["model_inference"] is True
        assert record["runtime_result"]["assembly_model_inference"] is False
    finally:runtime.close()
    assert len(list((service.root/"architecture-agent/analysis").glob("*.json")))==2
    reopened_service=ProductJobService(service.root,"");reopened=ArchitectureAgentRuntime(reopened_service,Path(__file__).resolve().parents[1])
    try:
        reopened.catalog([x["job_id"] for x in jobs])
        assert len(analysis_calls)==4
    finally:reopened.close()


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"),reason="FFmpeg unavailable")
def test_running_architecture_cancel_never_publishes_output(monkeypatch,tmp_path):
    service=ProductJobService(tmp_path/"data","")
    source=tmp_path/"source.mp4"
    subprocess.run([shutil.which("ffmpeg"),"-v","error","-f","lavfi","-i","color=c=blue:s=160x90:r=12",
                    "-t","0.6","-c:v","libx264","-pix_fmt","yuv420p","-y",str(source)],check=True,timeout=30)
    job=service.import_media({"kind":"video","filename":source.name,
                              "content_base64":base64.b64encode(source.read_bytes()).decode()})
    from media_ai import architecture_agent
    settings={"model_id":"fixture-qwen","model_sha256":"a"*64,"revision":"b"*40,"license":"Apache-2.0",
              "executable_sha256":"c"*64,"runtime_sha256":"d"*64}
    raw='{"aspect":"16:9","scenes":[{"source_id":"input-01","duration_seconds":0.5}]}'
    monkeypatch.setattr(architecture_agent,"invoke_local_json_plan",lambda *args,**kw:(json.loads(raw),raw,settings))
    started=__import__("threading").Event()
    def held_assembly(_adapter,_scenes,output,_aspect,_width,_height,timeout=900,cancel_check=None):
        started.set()
        end=time.monotonic()+5
        while time.monotonic()<end:
            if cancel_check and cancel_check():raise ProductionCancelled("test cancellation")
            time.sleep(.01)
        raise AssertionError("cancel did not reach the owned worker")
    monkeypatch.setattr(architecture_agent.FFmpegDeliveryAdapter,"assemble_existing_clips",held_assembly)
    runtime=ArchitectureAgentRuntime(service,Path(__file__).resolve().parents[1]);before=set(service.records)
    try:
        plan=runtime.plan({"command":"0.5초 16:9 건축 홍보 영상","job_ids":[job["job_id"]]})
        task=runtime.submit({"request_id":"cancel-running","plan_id":plan["plan_id"]})
        assert started.wait(3)
        runtime.cancel(task["production_id"])
        end=time.monotonic()+5
        while time.monotonic()<end:
            task=runtime.get(task["production_id"])
            if task["state"]=="CANCELLED":break
            time.sleep(.02)
        assert task["state"]=="CANCELLED"
        assert set(service.records)==before
        assert not Path(task["plan"]["output"]).exists()
        assert not list(service.projects.glob("*.json"))
    finally:runtime.close()
