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
