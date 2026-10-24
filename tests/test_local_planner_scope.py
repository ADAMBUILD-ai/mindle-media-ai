"""Boundary tests for generated plans; real model receipts live in evidence."""
import pytest
from media_ai.workflow_planner import validate_plan_scope

def test_generated_requested_scope():
    steps=[{'operation':'video_edit','options':{'brightness':10}},{'operation':'narrate','text':'안녕하세요'},{'operation':'mix_narration'}]
    assert validate_plan_scope('밝기를 10 높이고 "안녕하세요" 나레이션을 넣어 주세요.',steps)==steps

@pytest.mark.parametrize('command,steps',[
    ('파일을 삭제해 줘.',[{'operation':'video_edit','options':{'brightness':10}}]),
    ('대비를 7 높여 줘.',[{'operation':'video_edit','options':{'brightness':7}}]),
    ('대비를 7 높여 줘.',[{'operation':'transcribe'}]),
    ('대비를 7 높여 줘.',[{'operation':'mix_narration'}]),
    ('"요청 원고" 나레이션',[{'operation':'narrate','text':'발명한 원고'}]),
])
def test_generated_invented_actions_are_rejected(command,steps):
    with pytest.raises(ValueError,match='PLANNER_'):validate_plan_scope(command,steps)

def test_neural_model_identity_checked_before_construction(tmp_path):
    pytest.importorskip('sherpa_onnx')
    from media_ai.workflow_worker import narrate_neural
    with pytest.raises(ValueError,match='TTS_ENGINE_IDENTITY_MISMATCH'):
        narrate_neural(None,'안녕하세요',{'data_path':str(tmp_path),'data_sha256':'incorrect'})

def test_engine_tree_digest_has_case_sensitive_portable_order(tmp_path):
    import hashlib
    from media_ai.workflow_worker import tree_sha
    for name,content in [('a.txt',b'lower'),('Z.txt',b'upper'),('A.txt',b'first')]:
        (tmp_path/name).write_bytes(content)
    rows=[name+':'+hashlib.sha256(content).hexdigest() for name,content in [('A.txt',b'first'),('Z.txt',b'upper'),('a.txt',b'lower')]]
    assert tree_sha(tmp_path)==hashlib.sha256('\n'.join(rows).encode()).hexdigest()

def test_local_planner_decodes_korean_as_utf8(tmp_path,monkeypatch):
    import hashlib,json
    from media_ai import workflow_planner as planner
    executable=tmp_path/'executor.exe';executable.write_bytes(b'fixture-not-executed')
    model=tmp_path/'model.gguf';model.write_bytes(b'fixture-not-a-model')
    settings={'executable':str(executable),'executable_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'model_path':str(model),'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'license':'fixture','revision':'a'*40}
    monkeypatch.setattr(planner,'engines_config',lambda root:{'planner':settings})
    def output(args,**kwargs):
        assert kwargs['encoding']=='utf-8'
        return json.dumps({'steps':[{'operation':'narrate','text':'한국어 원고'},{'operation':'mix_narration','length_policy':'reject'}]},ensure_ascii=False)
    monkeypatch.setattr(planner.subprocess,'check_output',output)
    result=planner.make_plan(tmp_path,{'command':'"한국어 원고" 나레이션 추가'})
    assert result['steps'][0]['text']=='한국어 원고'

@pytest.mark.parametrize('command,steps',[
 ('밝기 5와 대비 9를 높여 줘.',[{'operation':'video_edit','options':{'brightness':5}}]),
 ('밝기 5와 "안녕" 나레이션 넣어 줘.',[{'operation':'video_edit','options':{'brightness':5}}]),
 ('자막을 넣어 줘.',[{'operation':'transcribe'}]),
])
def test_generated_partial_plan_is_not_success(command,steps):
    with pytest.raises(ValueError,match='PLANNER_INCOMPLETE_PLAN'):
        validate_plan_scope(command,steps)

@pytest.mark.parametrize('command,value',[
 ('밝기를 3 높여 줘',3),('밝기를 3 낮춰 줘',-3),
 ('밝기를 2.5 줄여 줘',-2.5),('밝기 0 높여 줘',0),
])
def test_exact_numeric_direction(command,value):
    steps=[{'operation':'video_edit','options':{'brightness':value}}]
    assert validate_plan_scope(command,steps)==steps

@pytest.mark.parametrize('command,value',[
 ('밝기를 3 높여 줘',30),('밝기를 3 낮춰 줘',3),
 ('밝기를 3으로 설정해',3),('밝기를 3% 높여 줘',3),
 ('밝기를 높여 줘',3),('밝기 3 높이고 밝기 3 높여',3),
 ('밝기를 바꾸지 마',3),('밝기 -3 낮춰 줘',-3),
 ('밝기 3 높여 줘',True),('밝기 3 높여 줘',float('nan')),
])
def test_unsafe_numeric_plan_rejected(command,value):
    with pytest.raises(ValueError,match='PLANNER_'):
        validate_plan_scope(command,[{'operation':'video_edit','options':{'brightness':value}}])

def test_negated_edit_with_another_requested_edit():
    steps=[{'operation':'video_edit','options':{'contrast':4}}]
    assert validate_plan_scope('밝기는 그대로 두고 대비를 4 높여 줘',steps)==steps

def test_script_edit_words_do_not_become_instructions():
    steps=[{'operation':'narrate','text':'밝기 30 대비 20'},{'operation':'mix_narration'}]
    assert validate_plan_scope('"밝기 30 대비 20" 나레이션 넣어 줘',steps)==steps

def test_duplicate_model_edits_rejected():
    with pytest.raises(ValueError,match='PLANNER_DUPLICATE_EDIT'):
        validate_plan_scope('밝기 3 높여 줘',[{'operation':'video_edit','options':{'brightness':3}}]*2)

@pytest.mark.parametrize('model_value,accepted',[(3,True),(30,False),(-3,False)])
def test_plan_api_rejects_wrong_model_values_before_persistence(tmp_path,monkeypatch,model_value,accepted):
    """Actual product HTTP boundary, synthetic model reply; no model inference."""
    import hashlib,json,threading
    from urllib.request import Request,urlopen
    from urllib.error import HTTPError
    from media_ai import workflow_planner as planner
    from media_ai.product_server import create_server
    executable=tmp_path/'executor';executable.write_bytes(b'not-executed')
    model=tmp_path/'model';model.write_bytes(b'not-a-model')
    settings={'executable':str(executable),'executable_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'model_path':str(model),'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'license':'fixture','revision':'a'*40}
    monkeypatch.setattr(planner,'engines_config',lambda root:{'planner':settings})
    monkeypatch.setattr(planner.subprocess,'check_output',lambda *args,**kw:json.dumps({'steps':[{'operation':'video_edit','options':{'brightness':model_value}}]}))
    from pathlib import Path
    data=tmp_path/'data'
    server=create_server(Path(__file__).resolve().parents[1],data,'')
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    request=Request('http://127.0.0.1:'+str(server.server_port)+'/api/workflows/plan',data=json.dumps({'command':'밝기를 3 높여 줘'}).encode(),headers={'Content-Type':'application/json'})
    try:
        if accepted:
            with urlopen(request,timeout=10) as response:result=json.load(response)
            assert result['validated_edit_values']=={'brightness':3}
            assert list((data/'workflows/plans').glob('*.json'))
        else:
            with pytest.raises(HTTPError) as error:urlopen(request,timeout=10)
            assert error.value.code==422
            assert 'PLANNER_VALUE_MISMATCH' in json.load(error.value)['error']
            assert not list((data/'workflows/plans').glob('*.json'))
    finally:
        server.shutdown();server.server_close();thread.join(timeout=3)

@pytest.mark.parametrize('command', ['밝기 3초 높여 줘','밝기 3e1 높여 줘','밝기 3배 높여 줘','밝기 3 높이고 낮춰 줘'])
def test_unsupported_units_and_conflicting_directions(command):
    with pytest.raises(ValueError,match='PLANNER_'):
        validate_plan_scope(command,[{'operation':'video_edit','options':{'brightness':3}}])

@pytest.mark.parametrize('command,steps',[
 ('자막을 넣지 마',[{'operation':'transcribe'},{'operation':'apply_subtitles'}]),
 ('"안녕" 나레이션 하지 마',[{'operation':'narrate','text':'안녕'},{'operation':'mix_narration'}]),
])
def test_negated_audio_subtitle_commands_do_not_execute(command,steps):
    with pytest.raises(ValueError,match='PLANNER_AMBIGUOUS_NEGATION'):
        validate_plan_scope(command,steps)

def test_independent_compound_values_preserve_plan():
    steps=[{'operation':'video_edit','options':{'brightness':-3,'contrast':4,'saturation':2.5}}]
    assert validate_plan_scope('밝기 3 낮추고 대비 4 높이고 채도 2.5 높여 줘',steps)==steps

@pytest.mark.parametrize('command', ['자막 없이 해 줘', '자막은, 넣지 마', "do not add subtitles"])
def test_other_negated_subtitle_forms_fail_closed(command):
    with pytest.raises(ValueError,match='PLANNER_AMBIGUOUS_NEGATION'):
        validate_plan_scope(command,[{'operation':'transcribe'},{'operation':'apply_subtitles'}])

def test_korean_additive_particle_is_not_a_degree_unit():
    steps=[{'operation':'video_edit','options':{'brightness':3}},{'operation':'transcribe'},{'operation':'apply_subtitles'}]
    assert validate_plan_scope('밝기 3 높이고 자막도 넣어 줘',steps)==steps
