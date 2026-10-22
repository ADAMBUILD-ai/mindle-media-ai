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
