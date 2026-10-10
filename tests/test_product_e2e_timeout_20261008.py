import ast
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]

def function(path, name, globals_):
    tree = ast.parse(path.read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), globals_)
    return globals_[name]

class WorkerTests(unittest.TestCase):
    def run_worker(self, local):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); package = root / 'media_ai'; package.mkdir()
            (package / '__init__.py').write_text('')
            (package / 'product_runtime.py').write_text('''import os,sys
class ProductJobService:
 def __init__(self, root, token): self.token=token
 def execute(self, request):
  try: sys.audit('socket.connect', None, ('127.0.0.1', 1)); allowed=True
  except PermissionError: allowed=False
  return {'job_id':'regression-job','network_allowed':allowed,'token_available':bool(self.token),'offline':os.environ.get('HF_HUB_OFFLINE'),'request':request}
''')
            fn = function(ROOT/'src/media_ai/product_runtime.py', 'execute_isolated',
                          {'Path':Path,'sys':sys,'os':os,'json':json,'uuid4':uuid4,'__file__':str(package/'product_runtime.py')})
            data = root/'data'; jobs = data/'jobs'; jobs.mkdir(parents=True)
            service = SimpleNamespace(root=data,jobs=jobs,records={},vault=SimpleNamespace(local_root=root if local else None,token='test-only-credential'))
            env = {'HF_TOKEN':'test-only-credential','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
            if local: env['MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT']=str(root)
            with patch.dict(os.environ, env):
                if not local:
                    with patch.dict(os.environ):
                        os.environ.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
                        result=fn(service, {'operation':'upscale'})
                else: result=fn(service, {'operation':'upscale'})
            self.assertEqual(service.records[result['job_id']], result)
            self.assertEqual(list(jobs.glob('worker-result-*')), [])
            return result
    def test_remote_vault_can_read_pinned_private_cache(self):
        r=self.run_worker(False)
        self.assertTrue(r['network_allowed']); self.assertTrue(r['token_available']); self.assertIsNone(r['offline'])
    def test_employee_package_stays_offline_and_token_free(self):
        r=self.run_worker(True)
        self.assertFalse(r['network_allowed']); self.assertFalse(r['token_available']); self.assertEqual(r['offline'],'1')

class PreviewTests(unittest.TestCase):
    def wait(self, operation, image_loaded=True, error=False):
        attrs={'data-preview-status':'actual-output','data-job-id':'job','data-operation':operation}
        element=SimpleNamespace(tag_name='img',text='',get_attribute=lambda key: {'data-job-id':'job','data-output-sha256':'digest'}.get(key))
        host=SimpleNamespace(get_attribute=attrs.get,find_element=lambda *args:element)
        msg=SimpleNamespace(text='model failed',get_attribute=lambda key:'error' if error else 'ok')
        editor=SimpleNamespace(find_element=lambda by,selector:msg if selector=='[data-command-error]' else host)
        driver=SimpleNamespace(execute_script=lambda *args:image_loaded)
        class Wait:
            def __init__(self,*args): pass
            def until(self,condition): return condition(None)
        fn=function(ROOT/'model_scout/run_product_e2e.py','wait_preview', {'By':SimpleNamespace(CSS_SELECTOR='css'),'WebDriverWait':Wait})
        return fn(driver,editor,'img',expected_operation='segment')
    def test_import_cannot_pass_as_segment(self): self.assertFalse(self.wait('import'))
    def test_unloaded_image_cannot_pass(self): self.assertFalse(self.wait('segment',False))
    def test_exact_operation_and_decoded_image_pass(self): self.assertEqual(self.wait('segment')['operation'],'segment')
    def test_failure_exits_without_300_second_wait(self):
        with self.assertRaisesRegex(RuntimeError,'model failed'): self.wait('segment',error=True)

if __name__=='__main__': unittest.main(verbosity=2)
