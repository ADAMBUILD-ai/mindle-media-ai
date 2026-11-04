"""Packaging invariants only. No native execution is claimed by these tests."""
import importlib.util,json,tempfile,unittest,zipfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('candidate',Path(__file__).parents[1]/'scripts/build_ai_windows_candidate.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
class PackagePolicy(unittest.TestCase):
 def test_cache_and_copy_staging_excluded_but_legitimate_numpy_preserved(self):
  for name in ['runtime/site-packages/PIL/__pycache__/ExifTags.cpython-311.pyc','app/src/model.pyc','.rsync-tmp/x','models/.weight-copy.abc']:
   self.assertFalse(build.stable(Path(name)),name)
  for name in ['runtime/site-packages/PIL/ExifTags.py','runtime/site-packages/numpy/f2py/.f2py_f2cmap','models/model.gguf','tools/llama/llama.dll']:
   self.assertTrue(build.stable(Path(name)),name)
 def test_archive_traversal_is_rejected(self):
  for name in ['../outside','/outside','C:/outside','a\\..\\outside']:
   with self.assertRaises(ValueError):build.safe_name(name)
 def test_seal_refuses_modified_pinned_result(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'candidate';payload=root/'_payload';payload.mkdir(parents=True)
   code=payload/'code.py';code.write_text('original')
   build.write(payload/'PACKAGE_MANIFEST.json',{'files':[build.record(payload,code)],'build_commit':'a'*40})
   code.write_text('changed')
   args=type('Args',(),{'output':str(root),'evidence':str(Path(d)/'evidence')})()
   with self.assertRaisesRegex(RuntimeError,'payload changed'):build.seal(args)
 def test_seal_refuses_generated_unlisted_cache(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'candidate';payload=root/'_payload';payload.mkdir(parents=True)
   build.write(payload/'PACKAGE_MANIFEST.json',{'files':[],'build_commit':'a'*40})
   (payload/'generated.pyc').write_bytes(b'new bytecode')
   args=type('Args',(),{'output':str(root),'evidence':str(Path(d)/'evidence')})()
   with self.assertRaisesRegex(RuntimeError,'bytecode'):build.seal(args)
if __name__=='__main__':unittest.main()

class SealedDelivery(unittest.TestCase):
 def test_happy_seal_outputs_starter_and_exact_parts(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/build.NAME;payload=root/'_payload';payload.mkdir(parents=True)
   (root/'MINDLE_MEDIA_AI_RUN.exe').write_bytes(b'fixture-not-executed')
   code=payload/'code.py';code.write_text('VALUE=1')
   build.write(payload/'PACKAGE_MANIFEST.json',{'files':[build.record(payload,code)],'build_commit':'a'*40})
   evidence=Path(d)/'evidence'
   args=type('Args',(),{'output':str(root),'evidence':str(evidence)})()
   build.seal(args)
   receipt=json.loads((evidence/'DELIVERY.json').read_text())
   self.assertEqual(receipt['sha256'],build.sha(root.with_suffix('.zip')))
   with zipfile.ZipFile(Path(d)/'MINDLE_MEDIA_AI_START_20261024_R1.zip') as z:
    cmd=z.read('START_MINDLE_MEDIA_AI.cmd').decode('ascii')
    self.assertIn('$env:MINDLE_INSTALLER_DIR',cmd)
    self.assertNotIn('ExecutionPolicy',cmd)
    self.assertLess(max(map(len,cmd.splitlines())),8191)
    self.assertIn(receipt['sha256'],z.read('INSTALL_COMMAND.txt').decode('utf-8-sig'))
