"""Execute real workflow preflight blocks without starting any build job."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap
import pytest

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('workflow',['pc-one-click-windows-build.yml','windows-openvino-runtime.yml','remote-verified-runtime-package.yml'])
@pytest.mark.parametrize('pc_gate',[False,True])
def test_r2_current_work_never_implicitly_releases_generic_build(tmp_path,workflow,pc_gate):
    source=(ROOT/'.github/workflows'/workflow).read_text(encoding='utf-8')
    code=textwrap.dedent(re.search(r'        run: \|\n((?:          .*\n|\n)+)',source).group(1))
    (tmp_path/'CURRENT_PC_WORK_STATE.json').write_text(json.dumps({'package_build_allowed':pc_gate}),encoding='utf-8')
    (tmp_path/'CURRENT_GENERAL_WORK_STATE.json').write_text(json.dumps({'status':'R2_GENERAL_PREPARATION_COMPLETE','current_work':{'work_id':'MEDIA-AI-CORE-E2E-R2-20261025'}}),encoding='utf-8')
    result_file=tmp_path/'output.txt'
    completed=subprocess.run([sys.executable,'-c',code],cwd=tmp_path,env={**os.environ,'GITHUB_OUTPUT':str(result_file)},capture_output=True,text=True)
    assert completed.returncode==0,completed.stderr
    assert result_file.read_text(encoding='utf-8').strip()=='allowed=false'
