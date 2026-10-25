#!/usr/bin/env python3
"""Reuse a pinned successful engine job only when its complete inputs are unchanged."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import urllib.request

BASE = '93a5e80ae214365043e91622920ce8e9f1ac0e9d'
PRIOR_RUN = 40186056871
ROOT = Path(__file__).resolve().parents[1]
CONTROL_ONLY = {
    '.github/workflows/runtime-recovery.yml', 'CURRENT_GENERAL_WORK_DIRECTIVE.md',
    '.github/workflows/pc-one-click-windows-build.yml',
    '.github/workflows/windows-openvino-runtime.yml',
    '.github/workflows/remote-verified-runtime-package.yml',
    'tests/test_r2_package_gate.py',
    '.github/workflows/pc-one-click-windows-fallback.yml','tests/test_exact_checkout_bytes.py',
    'scripts/validate_general_work_control_plane.py', 'scripts/select_runtime_recovery_checks.py',
    'tests/test_general_work_control_plane.py', 'tests/test_runtime_recovery_selection.py',
    'model_scout/run_runtime_recovery_browser.py',
    # Source/PC acceptance tooling is not imported by the engine workflow.
    'src/media_ai/source_e2e.py','src/media_ai/e2e_intake.py','scripts/run_real_architecture_acceptance.py',
    'tests/test_e2e_intake.py',
    'tests/test_source_e2e.py','tests/test_real_architecture_acceptance.py',
    'scripts/media_work_status.py','tests/test_media_work_status.py',
    'scripts/validate_pc_work_control_plane.py','CURRENT_PC_WORK_DIRECTIVE.md',
    'CURRENT_MEDIA_WORK_STATUS.json','CURRENT_GENERAL_WORK_STATE.json',
    'CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json','CURRENT_PC_WORK_STATE.json',
    'CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json','CURRENT_WORKER_COORDINATION_LOCK.json',
}


def control_only(paths):
    return bool(paths) and all(path in CONTROL_ONLY or path.startswith(('docs/evidence/media-ai-control-plane-recovery-20261025/',
        'docs/evidence/media-ai-core-e2e-r2-20261025/','docs/handoff/media-ai-core-e2e-r2-20261025/',
        'docs/evidence/media-ai-r2-work-status-20261025/','docs/commander/MINDLE_MEDIA_AI_R2_CURRENT_WORK_20261025.md')) for path in paths)


def engine_job_body(source):
    # The selector may add a dependency/condition, but never reuse changed engine steps.
    section = source.split('  adopted-real-engines:\n', 1)[1]
    return '\n'.join(line for line in section.splitlines() if not line.startswith(('    needs:', '    if:')))


def select(paths, before, after):
    return control_only(paths) and engine_job_body(before) == engine_job_body(after)


def main():
    paths = subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=ROOT,text=True).splitlines()
    before = subprocess.check_output(['git','show',BASE+':.github/workflows/runtime-recovery.yml'],cwd=ROOT,text=True)
    reuse = select(paths,before,(ROOT/'.github/workflows/runtime-recovery.yml').read_text())
    prior = None
    if reuse:
        headers = {'Accept':'application/vnd.github+json','Authorization':'Bearer '+os.environ['GH_TOKEN']}
        api = os.environ.get('GITHUB_API_URL','https://api.github.com')
        repo = os.environ['GITHUB_REPOSITORY']
        def get(path):
            with urllib.request.urlopen(urllib.request.Request(api+'/repos/'+repo+path,headers=headers),timeout=30) as response:
                return json.load(response)
        run = get(f'/actions/runs/{PRIOR_RUN}')
        jobs = get(f'/actions/runs/{PRIOR_RUN}/jobs?per_page=100')['jobs']
        successes = [job for job in jobs if job['name']=='adopted-real-engines' and job['conclusion']=='success']
        if run['head_sha'] != BASE or len(successes) != 1:
            raise ValueError('PRIOR_ENGINE_REUSE_EVIDENCE_MISMATCH')
        prior = {'run_id':PRIOR_RUN,'source':BASE,'job_id':successes[0]['id'],'conclusion':'success'}
    receipt = {'source':os.environ.get('GITHUB_SHA'),'changed_paths':paths,'engine_inputs_unchanged':reuse,
               'run_engines':not reuse,'reused_engine_job':prior,'full_product_pass':False}
    output = ROOT/'runtime_recovery_selection.json'
    output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
    with open(os.environ['GITHUB_OUTPUT'],'a') as stream:
        stream.write('run_engines='+str(not reuse).lower()+'\n')


if __name__ == '__main__':
    main()
