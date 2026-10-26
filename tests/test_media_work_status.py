"""Current status is derived from real source/input; never a production approval."""
import importlib.util
import json
from pathlib import Path
import shutil
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('current_work',ROOT/'scripts/media_work_status.py')
status=importlib.util.module_from_spec(spec);spec.loader.exec_module(status)


@pytest.fixture
def tree(tmp_path):
    names=set(status.CONTROLS)|{status.STATUS_FILE,status.MANIFEST,status.BASELINE,status.FOUNDATION,status.DIRECTIVE}
    baseline=status.read(ROOT,status.BASELINE);foundation=status.read(ROOT,status.FOUNDATION)
    names.update(foundation['source_file_sha256'])
    names.update(name for name in baseline['code_file_sha256'] if name.startswith('src/media_ai/'))
    names.update(baseline['source_ui_identity']['file_hashes'])
    for name in names:
        target=tmp_path/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    return tmp_path


def change(root,name,key,value):
    body=status.read(root,name);body[key]=value;status.write(root/name,body)


def test_current_status_separates_preparation_production_and_pc_observation(tree):
    value=status.check(tree)
    assert value['general_status']=='R2_GENERAL_PREPARATION_COMPLETE'
    assert value['production_eligibility']=='BLOCKED_ASSET_INTAKE'
    assert value['local_pc_process_status']=='NOT_OBSERVED'
    assert value['production_execution_allowed'] is False
    assert value['background_execution_claimed'] is False
    for name in status.CONTROLS:
        assert status.read(tree,name)['current_work']['work_id']==status.WORK_ID


def test_source_change_cannot_be_hidden_by_a_ready_status(tree):
    target=tree/'src/media_ai/workflow_worker.py';target.write_bytes(target.read_bytes()+b'\n# injected source drift\n')
    with pytest.raises(ValueError,match='SNAPSHOT_STALE_OR_FORGED'):status.check(tree)
    value=status.refresh(tree)
    assert value['production_eligibility']=='BLOCKED_SOURCE_REVALIDATION'
    assert 'src/media_ai/workflow_worker.py' in value['runtime_baseline']['changed_paths']
    assert value['general_status']=='R2_SOURCE_REVALIDATION_REQUIRED'


def test_reviewed_acceptance_tool_patch_still_rejects_further_drift(tree):
    path=status.ACCEPTANCE_TOOL_PATCH['path']
    assert status.runtime_baseline(tree)['acceptance_tool_patch']['sha256']==status.digest(tree/path)
    target=tree/path;target.write_bytes(target.read_bytes()+b'\n# unverified drift\n')
    value=status.refresh(tree)
    assert value['production_eligibility']=='BLOCKED_SOURCE_REVALIDATION'
    assert path in value['runtime_baseline']['changed_paths']


def test_missing_or_added_runtime_module_requires_revalidation(tree):
    p=tree/'src/media_ai/new_unverified_runtime.py';p.write_text('# fixture',encoding='utf-8')
    value=status.refresh(tree)
    assert value['production_eligibility']=='BLOCKED_SOURCE_REVALIDATION'
    p.unlink();(tree/'ui/ai_core_status.js').unlink()
    assert status.refresh(tree)['production_eligibility']=='BLOCKED_SOURCE_REVALIDATION'


def test_input_change_invalidates_snapshot_even_if_still_blocked(tree):
    change(tree,status.MANIFEST,'narration_script','fixture, not an approved owner script')
    with pytest.raises(ValueError,match='SNAPSHOT_STALE_OR_FORGED'):status.check(tree)
    value=status.refresh(tree)
    assert value['production_eligibility']=='BLOCKED_ASSET_INTAKE'
    assert value['input_manifest_sha256']==status.digest(tree/status.MANIFEST)


def test_claimed_pass_cannot_replace_real_intake_or_approve_execution(tree):
    change(tree,status.STATUS_FILE,'production_execution_allowed',True)
    with pytest.raises(ValueError,match='SNAPSHOT_STALE_OR_FORGED'):status.check(tree)


@pytest.mark.parametrize('name',status.CONTROLS)
def test_lane_disagreement_is_rejected(tree,name):
    body=status.read(tree,name);body['current_work']['work_id']='STALE';status.write(tree/name,body)
    with pytest.raises(ValueError,match='REFERENCE_MISMATCH'):status.check(tree)


def test_refresh_refuses_open_gate_without_closing_it_or_granting_approval(tree):
    change(tree,'CURRENT_PC_WORK_STATE.json','package_build_allowed',True)
    before=(tree/status.STATUS_FILE).read_bytes()
    with pytest.raises(ValueError,match='EXISTING_BUILD_GATE_NOT_CLOSED'):status.refresh(tree)
    assert status.read(tree,'CURRENT_PC_WORK_STATE.json')['package_build_allowed'] is True
    assert (tree/status.STATUS_FILE).read_bytes()==before


def test_evidence_expectations_cannot_be_rewritten_to_make_source_pass(tree):
    authority=tree/status.BASELINE;authority.write_bytes(authority.read_bytes()+b'\n')
    value=status.refresh(tree)
    assert value['runtime_baseline']['status']=='BLOCKED_EVIDENCE_AUTHORITY_CHANGED'
    assert value['production_execution_allowed'] is False


def test_consumed_r3_identity_and_epoch_are_preserved(tree):
    before={name:status.read(tree,name) for name in status.CONTROLS[:4]}
    status.refresh(tree)
    for name,old in before.items():
        new=status.read(tree,name)
        for key in ('control_plane_epoch','phase','owner_windows_ai_successor_20261024','active_directive','evidence_contract'):
            assert new.get(key)==old.get(key)
        assert new['package_build_allowed'] is False


def test_ready_intake_advances_general_to_engine_preflight_without_windows_approval_gate(tree,monkeypatch):
    monkeypatch.setattr(status,'intake_result',lambda path:{'errors':[],'manifest_sha256':status.digest(path),'status':'PASS_INTAKE_TECHNICAL_ONLY'})
    value=status.derive(tree)
    assert value['production_eligibility']=='ENGINE_PREFLIGHT_REQUIRED'
    assert value['next_action']=='RUN_GENERAL_SOURCE_ENGINE_PREFLIGHT'
    assert value['pc_status']=='R2_WINDOWS_ENGINE_AND_APPROVAL_PREFLIGHT_REQUIRED'
    assert value['production_execution_allowed'] is False  # Status tool never verifies/runs engines.
