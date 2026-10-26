"""Candidate data isolation contract; native EXE acceptance remains separate."""
import ast,os,re
from pathlib import Path
import pytest

def helper():
    source=Path(__file__).parents[1]/'scripts/employee_package_launcher.py'
    node=next(n for n in ast.parse(source.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='package_data_root')
    env={'Path':Path,'os':os,'re':re}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),env)
    return env['package_data_root']

def test_candidate_does_not_share_legacy_data(tmp_path,monkeypatch):
    monkeypatch.setenv('LOCALAPPDATA',str(tmp_path));resolve=helper()
    old=resolve({});new=resolve({'data_directory_name':'MEDIA_AI_CANDIDATE_20261018_R1'})
    assert old==tmp_path/'MINDLE/MEDIA_AI_DATA'
    assert new==tmp_path/'MINDLE/MEDIA_AI_CANDIDATE_20261018_R1'
    assert old!=new
    assert resolve({},new)==new

@pytest.mark.parametrize('name',['../MEDIA_AI_DATA','C:\\existing','', 'a/b'])
def test_candidate_profile_cannot_escape(tmp_path,monkeypatch,name):
    monkeypatch.setenv('LOCALAPPDATA',str(tmp_path))
    with pytest.raises(RuntimeError):helper()({'data_directory_name':name})
