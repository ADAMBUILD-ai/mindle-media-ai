"""Native Windows source helper tests; no packaged EXE or owner-PC acceptance."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(os.name=='nt','native Windows file locking required')
class NativeLockTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('employee_launcher',Path(__file__).parents[1]/'scripts/employee_package_launcher.py')
        self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.lock=Path(self.tmp.name)/'launch.lock'

    def competing_process(self):
        code='''import msvcrt,sys
with open(sys.argv[1],'a+b') as f:
 f.seek(0)
 try:
  msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
 except OSError:
  print('BUSY')
 else:
  msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
  print('ACQUIRED')
'''
        return subprocess.check_output([sys.executable,'-c',code,str(self.lock)],text=True,timeout=10).strip()

    def test_second_process_blocked_only_while_request_holds_lock(self):
        with self.module.launch_request_lock(self.lock):self.assertEqual(self.competing_process(),'BUSY')
        self.assertEqual(self.competing_process(),'ACQUIRED')

    def test_preparation_failure_releases_native_lock(self):
        with self.assertRaisesRegex(RuntimeError,'preparation'):
            with self.module.launch_request_lock(self.lock):raise RuntimeError('preparation')
        self.assertEqual(self.competing_process(),'ACQUIRED')

    def test_repeated_requests_leave_lock_file_and_allow_reentry(self):
        for _ in range(3):
            with self.module.launch_request_lock(self.lock):pass
        self.assertTrue(self.lock.is_file())
        self.assertEqual(self.competing_process(),'ACQUIRED')


if __name__=='__main__':unittest.main()
