import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('selection',ROOT/'scripts/select_runtime_recovery_checks.py')
selection=importlib.util.module_from_spec(spec)
spec.loader.exec_module(selection)


@pytest.mark.parametrize('path', ['src/media_ai/ai_core_status.py','ui/workflow_execution.js','pyproject.toml','model_scout/run_live_agent_engines.py','unknown-model-input.json'])
def test_runtime_or_unknown_input_change_invalidates_engine_reuse(path):
    assert selection.control_only(['scripts/validate_general_work_control_plane.py',path]) is False


def test_control_only_changes_can_reuse_unchanged_engine_job():
    before='  adopted-real-engines:\n    runs-on: ubuntu-latest\n    steps:\n      - run: verify-engine\n'
    after=before.replace('    runs-on:', "    needs: select-checks\n    if: needs.select-checks.outputs.run_engines == 'true'\n    runs-on:")
    assert selection.select(['scripts/validate_general_work_control_plane.py'],before,after)
    assert not selection.select(['scripts/validate_general_work_control_plane.py'],before,after.replace('verify-engine','different-engine'))


def test_empty_delta_does_not_silently_claim_new_reuse():
    assert selection.control_only([]) is False


@pytest.mark.parametrize('path',['src/media_ai/source_e2e.py','scripts/run_real_architecture_acceptance.py','tests/test_source_e2e.py'])
def test_acceptance_tooling_can_reuse_verified_engine_job_but_runtime_cannot(path):
    before='  adopted-real-engines:\n    runs-on: ubuntu-latest\n    steps:\n      - run: verify-engine\n'
    assert selection.select([path],before,before)
    assert not selection.select([path,'src/media_ai/workflow_planner.py'],before,before)
    assert not selection.select([path],before,before.replace('verify-engine','changed-engine'))
