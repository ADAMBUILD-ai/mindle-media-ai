"""Real import/relaunch integrity reproduction on host Python; not Windows EXE."""
import ast
import hashlib
from pathlib import Path
import py_compile
import subprocess
import sys

ROOT=Path(__file__).parents[1]

def test_writable_bytecode_breaks_seal_but_B_preserves_it(tmp_path):
    module=tmp_path/'sample.py'; module.write_text('VALUE=42\n')
    cache=Path(py_compile.compile(str(module),doraise=True))
    # Emulate a cache carried from a different build path/version/mtime.
    original=cache.read_bytes(); stale=bytearray(original); stale[8:12]=b'\0\0\0\0';cache.write_bytes(stale)
    sealed=hashlib.sha256(cache.read_bytes()).hexdigest()
    subprocess.run([sys.executable,'-B','-c','import sample; assert sample.VALUE==42'],cwd=tmp_path,check=True)
    assert hashlib.sha256(cache.read_bytes()).hexdigest()==sealed
    subprocess.run([sys.executable,'-c','import sample; assert sample.VALUE==42'],cwd=tmp_path,check=True)
    assert hashlib.sha256(cache.read_bytes()).hexdigest()!=sealed

def test_bootstrap_and_server_children_disable_bytecode():
    for filename,needle in [('one_click_bootstrap.py','command = [str(executable), "-B", str(launcher)]'),('employee_package_launcher.py','[sys.executable, "-B", str(Path(__file__))')]:
        text=(ROOT/'scripts'/filename).read_text()
        ast.parse(text)
        assert needle in text
    tree=ast.parse((ROOT/'scripts/employee_package_launcher.py').read_text())
    assignment=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr=='dont_write_bytecode' for t in n.targets))
    assert assignment < next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Import) and any(a.name=='argparse' for a in n.names))


def test_workflow_child_disables_bytecode():
    text=(ROOT/'src/media_ai/durable_workflows.py').read_text()
    assert "[sys.executable,'-B','-X','utf8'" in text
