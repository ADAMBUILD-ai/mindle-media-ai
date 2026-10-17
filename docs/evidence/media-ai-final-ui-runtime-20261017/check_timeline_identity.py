import ast, hashlib, json, os, subprocess, tempfile, textwrap
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

root=Path(__file__).parent
module=ast.parse((root/'src/media_ai/product_server.py').read_text())
method=next(n for c in module.body if isinstance(c,ast.ClassDef) and c.name=='ProductHttpServer' for n in c.body if isinstance(n,ast.FunctionDef) and n.name=='_runtime_identity')
ns={'os':os,'Path':Path,'json':json,'hashlib':hashlib,'subprocess':subprocess}
exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),'product_server.py','exec'),ns)
with tempfile.TemporaryDirectory() as tmp:
 base=Path(tmp)
 names=['index.html','approved_visual.css','interaction.css','interaction.js','product_integration.js','photo_workspace.js','video_workspace.js','workspace_shell.js','timeline_preview.js','assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico']
 for name in names:
  file=base/'ui'/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(b'fixture')
 obj=SimpleNamespace(root=base,data_dir=base/'data')
 with patch.dict(os.environ,{'MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT':''}),patch('subprocess.check_output',side_effect=subprocess.CalledProcessError(128,'git')):
  first=ns['_runtime_identity'](obj)
  (base/'ui/timeline_preview.js').write_bytes(b'changed timeline')
  second=ns['_runtime_identity'](obj)
 assert first['workspace_ui_fingerprint']!=second['workspace_ui_fingerprint']
 assert 'ui/timeline_preview.js' in second['file_hashes']
 for script in ['scripts/build_one_click_runtime_layout.py','scripts/build_employee_distribution_package.py']:
  ast.parse((root/script).read_text());assert 'timeline_preview.js' in (root/script).read_text()
 print(json.dumps({'status':'PASS','scope':'extracted production fingerprint method; timeline byte change changes identity; builders syntax/list inclusion only, no build execution','before':first['workspace_ui_fingerprint'],'after':second['workspace_ui_fingerprint']}))
