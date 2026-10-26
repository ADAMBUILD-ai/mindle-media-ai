"""Execution tooling/fault fixtures only; no real architecture or model PASS."""
import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
import pytest
from media_ai import source_e2e as runner
from media_ai.e2e_intake import intake_result

ROOT=Path(__file__).resolve().parents[1]


def test_missing_assets_stop_before_process_or_inference(tmp_path,monkeypatch):
    manifest=tmp_path/'INPUT_MANIFEST.json';manifest.write_text('{}',encoding='utf-8')
    out=tmp_path/'evidence'
    monkeypatch.setattr(sys,'argv',['source_e2e','--manifest',str(manifest),'--output',str(out),'--execute'])
    monkeypatch.setattr(runner.SourceSession,'start',lambda *a:pytest.fail('blocked assets must not launch'))
    monkeypatch.setattr(runner,'verify_engines',lambda *a:pytest.fail('blocked assets must not inspect/run engines'))
    assert runner.main()==2
    receipt=json.loads((out/'RUN_RECEIPT.json').read_text(encoding='utf-8'))
    assert receipt['status']=='BLOCKED' and receipt['error']=='BLOCKED_ASSET_INTAKE'
    assert receipt['stages']['cold_restart']['status']=='NOT_EXECUTED'
    assert receipt['full_product_pass'] is False
    a=json.loads((out/'ASSET_INTAKE.json').read_text(encoding='utf-8'))
    b=json.loads((out/'INTAKE_RESULT.json').read_text(encoding='utf-8'))
    assert a==b and a['manifest_sha256']==hashlib.sha256(manifest.read_bytes()).hexdigest()
    assert not (out/'isolated-product-data').exists()


def manifest():return {'narration_script':'확정 시험 원고','volumes':{'narration':.8,'original':.2,'bgm':.15},'voice_length_policy':'reject'}


@pytest.mark.parametrize('fault',['script','volume','length','extra_step','missing_bgm'])
def test_audio_finish_cannot_change_exact_contract(fault):
    m=manifest();steps=[{'operation':'narrate','text':m['narration_script']},
                       {'operation':'mix_narration','volume':.8,'original_volume':.2,'background_volume':.15,'length_policy':'reject'}]
    if fault=='script':steps[0]['text']='다른 원고'
    elif fault=='volume':steps[1]['volume']=.9
    elif fault=='length':steps[1]['length_policy']='extend_video'
    elif fault=='extra_step':steps.insert(0,{'operation':'video_edit','options':{'aspect':'16:9'}})
    elif fault=='missing_bgm':del steps[1]['background_volume']
    with pytest.raises(ValueError):runner.validate_audio_plan(m,{'plan_source':'LOCAL_GENERATIVE_INFERENCE','steps':steps})


def test_audio_command_is_product_compatible_and_exact():
    m=manifest();steps=[{'operation':'narrate','text':m['narration_script']},
                       {'operation':'mix_narration','volume':.8,'original_volume':.2,'background_volume':.15,'length_policy':'reject'}]
    runner.validate_audio_plan(m,{'plan_source':'LOCAL_GENERATIVE_INFERENCE','steps':steps})


def test_timeout_cancels_only_the_owned_task(tmp_path):
    class Session:
        calls=[]
        def call(self,path,body=None):self.calls.append((path,body))
    s=Session()
    with pytest.raises(TimeoutError,match='CANCEL_REQUESTED'):runner.wait_task(s,'/api/workflows','owned-id',tmp_path/'task.json',timeout=0)
    assert s.calls==[('/api/workflows/owned-id/cancel',{})]


def test_export_internal_tamper_is_rejected_even_with_valid_zip_crc_and_outer_hash(tmp_path):
    path=tmp_path/'export.zip';payload=b'original';changed=b'changed'
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('project.json',json.dumps({'project_id':'project'}))
        z.writestr('BUNDLE_MANIFEST.json',json.dumps({'project_id':'project','files':[{'archive_path':'clip','bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}]}))
        z.writestr('clip',changed)
    with pytest.raises(ValueError,match='EXPORT_INTERNAL_IDENTITY_FAILED'):
        runner.verify_export(path,hashlib.sha256(path.read_bytes()).hexdigest(),'project')


def test_owned_real_product_process_cold_restart_reopen_and_export(tmp_path):
    # One-second synthetic import/save tests the lifecycle tool, not the 30s AI E2E.
    data=tmp_path/'data';data.mkdir();evidence=tmp_path/'evidence';evidence.mkdir()
    source=tmp_path/'test.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=32x18:r=4','-t','1','-c:v','libx264',str(source)],check=True)
    session=runner.SourceSession(ROOT,data,evidence)
    try:
        first=session.start('first')
        imported=session.call('/api/media/import',{'kind':'video','filename':'test.mp4','content_base64':base64.b64encode(source.read_bytes()).decode()})
        runner.verify_imported_input(imported,runner.file_record(source))
        saved=session.call('/api/projects/save',{'job_ids':[imported['job_id']]})
        before=session.call('/api/projects/'+saved['project_id'])['project'];session.stop()
        second=session.start('second')
        assert first['server_pid']!=second['server_pid']
        assert first['server_instance_id']!=second['server_instance_id']
        reopened=session.call('/api/projects/'+saved['project_id'])['project']
        runner.verify_reopened_project(before,reopened)
        assert reopened['jobs'][0]['primary_output']['sha256']==imported['primary_output']['sha256']
        exported=session.call('/api/projects/'+saved['project_id']+'/export',{})
        result=runner.verify_export(exported['export']['path'],exported['export']['sha256'],saved['project_id'],reopened['jobs'])
        assert result['status']=='PASS'
        session.stop()
    finally:session.cleanup()


def test_fixed_30_second_quality_does_not_accept_short_video(tmp_path):
    source=tmp_path/'short.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=160x90:r=4','-f','lavfi','-i','sine=duration=1',
                    '-t','1','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(source)],check=True)
    with pytest.raises(ValueError,match='OUTPUT_NOT_EXACT_30_SECONDS'):runner.quality(source,manifest())


def test_export_cannot_hide_changed_job_metadata_behind_transport_url_normalization(tmp_path):
    path=tmp_path/'export.zip';payload=b'media'
    job={'job_id':'job','runtime_result':{'text':'original'},'preview_url':'/files/old'}
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('project.json',json.dumps({'project_id':'project','jobs':[job]}))
        z.writestr('BUNDLE_MANIFEST.json',json.dumps({'project_id':'project','files':[{'archive_path':'clip','bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}]}))
        z.writestr('clip',payload)
    changed={**job,'preview_url':'/files/new','runtime_result':{'text':'changed'}}
    with pytest.raises(ValueError,match='EXPORT_REOPEN_JOB_IDENTITY_FAILED'):
        runner.verify_export(path,hashlib.sha256(path.read_bytes()).hexdigest(),'project',[changed])


@pytest.mark.parametrize('fault',[None,'input','preview'])
def test_original_input_and_transcoded_preview_have_separate_identities(tmp_path,fault):
    original=tmp_path/'original.mp4';original.write_bytes(b'owner original bytes')
    preview=tmp_path/'preview.mp4';preview.write_bytes(b'different transcoded preview bytes')
    source=runner.file_record(original)
    job={'status':'TESTED_PASS','operation':'import','input':source.copy(),'primary_output':runner.file_record(preview)}
    assert source['sha256']!=job['primary_output']['sha256']
    if fault=='input':job['input']['sha256']='a'*64
    elif fault=='preview':preview.write_bytes(b'changed preview')
    if fault:
        with pytest.raises(ValueError,match='IMPORTED_(SOURCE|PREVIEW)_IDENTITY_FAILED'):runner.verify_imported_input(job,source)
    else:runner.verify_imported_input(job,source)


@pytest.mark.parametrize('video_seconds,audio_seconds,accepted',[(1,30,False),(30,1,False),(30,30,True)])
def test_quality_checks_both_actual_stream_lengths(tmp_path,video_seconds,audio_seconds,accepted):
    # Fault fixtures exercise the acceptance gate; never owner production assets.
    path=tmp_path/'timing.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'color=s=160x90:r=4:d={video_seconds}',
                    '-f','lavfi','-i',f'anullsrc=r=16000:cl=mono:d={audio_seconds}',
                    '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(path)],check=True)
    if accepted:
        result=runner.quality(path,{})
        assert result['stream_timelines']['video']['duration_seconds']==30
        assert result['human_review']=='NOT_EXECUTED'
    else:
        with pytest.raises(ValueError,match='OUTPUT_STREAM_NOT_EXACT_30_SECONDS'):
            runner.quality(path,{})


@pytest.mark.parametrize('fault',['missing','nan','infinity','offset','opposite_ends'])
def test_invalid_or_skewed_stream_timing_cannot_reach_decode(monkeypatch,fault):
    info={'format':{'duration':'30'},'streams':[
        {'codec_type':'video','codec_name':'h264','pix_fmt':'yuv420p','width':160,'height':90,'duration':'30','start_time':'0'},
        {'codec_type':'audio','codec_name':'aac','duration':'30','start_time':'0'}]}
    if fault=='missing':del info['streams'][0]['duration']
    elif fault=='nan':info['streams'][0]['duration']='nan'
    elif fault=='infinity':info['streams'][1]['start_time']='inf'
    elif fault=='offset':info['streams'][1]['start_time']='1'
    else:
        info['streams'][0]['duration']='29.86';info['streams'][1]['duration']='30.14'
    monkeypatch.setattr(runner,'probe',lambda path:info)
    monkeypatch.setattr(runner.subprocess,'run',lambda *a,**kw:pytest.fail('invalid timing must block decode'))
    with pytest.raises(ValueError,match='OUTPUT_(STREAM|AUDIO_VIDEO)'):
        runner.quality(Path('unused.mp4'),{})


def test_quality_from_probe_can_use_the_approved_package_decoder(monkeypatch):
    info={'format':{'duration':'30'},'streams':[{'codec_type':'video','codec_name':'h264','pix_fmt':'yuv420p','width':160,'height':90,'duration':'30','start_time':'0'},
        {'codec_type':'audio','codec_name':'aac','duration':'30','start_time':'0'}]}
    called=[]
    monkeypatch.setattr(runner.subprocess,'run',lambda command,**kwargs:called.append(command))
    result=runner.quality_from_probe(Path('approved.mp4'),info,'C:/approved/ffmpeg.exe')
    assert result['decoded_video_and_audio'] is True
    assert called[0][0]=='C:/approved/ffmpeg.exe'


@pytest.mark.parametrize('fault',['script','volume','workspace','input','reference',None])
def test_reopen_preserves_full_project_and_original_reference_bytes(tmp_path,fault):
    original=tmp_path/'original';original.write_bytes(b'original')
    reference=tmp_path/'reference';reference.write_bytes(b'reference')
    output=tmp_path/'output';output.write_bytes(b'output')
    job={'job_id':'job','outputs':[runner.file_record(output)],'input':runner.file_record(original),
         'reference_artifacts':[runner.file_record(reference)],'preview_url':'/old',
         'runtime_result':{'text':'exact script','options':{'volume':.8}}}
    saved={'project_id':'p','jobs':[job],'workspace':{'label':'approved'}}
    reopened=deepcopy(saved);reopened['jobs'][0]['preview_url']='/new'
    if fault=='script':reopened['jobs'][0]['runtime_result']['text']='changed'
    elif fault=='volume':reopened['jobs'][0]['runtime_result']['options']['volume']=.9
    elif fault=='workspace':reopened['workspace']['label']='changed'
    elif fault=='input':original.write_bytes(b'altered')
    elif fault=='reference':reference.write_bytes(b'altered')
    if fault:
        with pytest.raises(ValueError,match='REOPEN_(PROJECT_METADATA_CHANGED|FILE_IDENTITY_FAILED)'):
            runner.verify_reopened_project(saved,reopened)
    else:runner.verify_reopened_project(saved,reopened)
