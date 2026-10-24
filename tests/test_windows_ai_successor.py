import json
from pathlib import Path

from scripts import build_ai_windows_successor as successor


ROOT=Path(__file__).resolve().parents[1]


def test_successor_reuses_test_r2_without_engine_download_or_rebuild():
    policy=json.loads((ROOT/'docs/commander/MINDLE_MEDIA_AI_TEST_R2_REUSE_AND_REBUILD_GATE_20261024.json').read_text())
    authorization=json.loads((ROOT/'docs/commander/WINDOWS_AI_SUCCESSOR_20261024_AUTHORIZATION.json').read_text())
    source=(ROOT/'scripts/build_ai_windows_successor.py').read_text()
    assert successor.BASE_SHA256==policy['candidate']['zip_sha256']==authorization['reuse_base_zip_sha256']
    assert authorization['engine_download_allowed'] is False and authorization['engine_rebuild_allowed'] is False
    assert 'urllib' not in source and 'pip install' not in source and 'llama.cpp/releases' not in source


def test_successor_gate_is_one_attempt_and_bound_to_all_control_planes():
    authorization=json.loads((ROOT/'docs/commander/WINDOWS_AI_SUCCESSOR_20261024_AUTHORIZATION.json').read_text())
    assert authorization['attempts_allowed']==1
    for name in ('CURRENT_PC_WORK_STATE.json','CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json',
                 'CURRENT_GENERAL_WORK_STATE.json','CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json'):
        control=json.loads((ROOT/name).read_text())
        assert control['package_build_allowed'] is True
        assert control['owner_windows_ai_successor_20261024']['authorization']==authorization['id']
        assert control['owner_windows_ai_successor_20261024']['engine_bytes']=='REUSE_VERIFIED_NO_DOWNLOAD_NO_REBUILD'


def test_windows_acceptance_requires_real_architecture_qwen_and_restart_export():
    source=(ROOT/'scripts/accept_ai_windows_successor.py').read_text()
    for required in ('/api/architecture-agent/plan','/api/architecture-agent/productions',
                     "planner_model_inference'] is True",'/api/runtime/shutdown',
                     'ARCHITECTURE_AFTER_RESTART_EXPORT.zip'):
        assert required in source
