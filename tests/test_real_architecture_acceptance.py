import importlib.util
import json
from pathlib import Path


def _runner():
    path=Path(__file__).resolve().parents[1]/'scripts/run_real_architecture_acceptance.py'
    spec=importlib.util.spec_from_file_location('real_architecture_acceptance',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_missing_intake_stops_before_product_or_model_calls(tmp_path,monkeypatch):
    manifest=tmp_path/'INPUT_MANIFEST.json'
    manifest.write_text(json.dumps({'duration_seconds':30,'aspect':'16:9','narration_script':None,
        'voice_length_policy':'reject','volumes':{'narration':None,'original':None,'bgm':None},
        'clips':[],'bgm':None}),encoding='utf-8')
    output=tmp_path/'evidence';module=_runner()
    monkeypatch.setattr(module,'execute',lambda *args,**kwargs:(_ for _ in ()).throw(AssertionError('must not execute')))
    monkeypatch.setattr('sys.argv',['runner',str(manifest),'--evidence-root',str(output)])
    assert module.main()==2
    result=json.loads((output/'RESULT.json').read_text(encoding='utf-8'))
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert result['execution_id'] and result['started_at'] and result['ended_at']
    assert result['first_blocking_gate']=='INPUT_MANIFEST'
    assert 'Qwen' in result['not_executed'] and 'Supertonic' in result['not_executed']


def test_bgm_product_limit_is_shared_by_intake_and_execution(tmp_path):
    from media_ai.e2e_intake import validate_intake
    manifest={'duration_seconds':30,'aspect':'16:9','narration_script':'확정 원고','voice_length_policy':'reject',
              'volumes':{'narration':1,'original':1,'bgm':1.01},'clips':[],'bgm':None}
    result=validate_intake(manifest,tmp_path)
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert 'explicit bgm volume required (0..1)' in result['errors']


def test_approved_exe_is_mandatory_for_cold_restart(tmp_path,monkeypatch):
    manifest=tmp_path/'INPUT_MANIFEST.json';manifest.write_text('{}',encoding='utf-8')
    output=tmp_path/'evidence';module=_runner()
    monkeypatch.setattr(module,'validate_intake',lambda *_args:{'status':'PASS_INTAKE_TECHNICAL_ONLY'})
    monkeypatch.setattr(module,'execute',lambda *_args,**_kwargs:(_ for _ in ()).throw(AssertionError('must not execute')))
    monkeypatch.setattr('sys.argv',['runner',str(manifest),'--evidence-root',str(output),
                                   '--expected-source','a'*40,'--base-url','http://127.0.0.1:18768'])
    try:module.main()
    except ValueError as error:assert str(error)=='approved source and EXE are required after intake passes'
    else:raise AssertionError('missing EXE must block the acceptance run')



def test_candidate_approval_blocks_before_any_server_call(tmp_path,monkeypatch):
    from types import SimpleNamespace
    import pytest
    module=_runner();approval=tmp_path/'approval.json';approval.write_text(json.dumps({'approved':False}),encoding='utf-8')
    args=SimpleNamespace(approval_file=approval,expected_source='a'*40)
    monkeypatch.setattr(module,'call',lambda *a,**k:pytest.fail('unapproved candidate must not be called'))
    with pytest.raises(RuntimeError,match='BLOCKED_CANDIDATE_APPROVAL_BINDING'):
        module.execute(args,{}, {'manifest_sha256':'b'*64},tmp_path)


def test_candidate_probe_rejects_wrong_aspect_before_decode(monkeypatch):
    import pytest
    module=_runner()
    probe={'format':{'duration':'30'},'streams':[{'codec_type':'video','codec_name':'h264','pix_fmt':'yuv420p','width':720,'height':1280},{'codec_type':'audio','codec_name':'aac'}]}
    monkeypatch.setattr(module.subprocess,'check_output',lambda *a,**k:json.dumps(probe))
    with pytest.raises(RuntimeError,match='FINAL_MEDIA_ASPECT_GATE_FAILED'):
        module.technical_probe(Path('ffprobe.exe'),Path('video.mp4'))


def test_pid_exit_requires_actual_process_exit():
    import os,subprocess,sys
    module=_runner();assert not module.pid_exited(os.getpid())
    child=subprocess.Popen([sys.executable,'-c','pass']);child.wait(timeout=10)
    assert module.pid_exited(child.pid)
