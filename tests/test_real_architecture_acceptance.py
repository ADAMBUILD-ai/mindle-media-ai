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
