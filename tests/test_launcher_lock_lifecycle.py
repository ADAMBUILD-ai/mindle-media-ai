"""Fault injection for launcher resource lifecycle; not native Windows locking."""
import ast
from contextlib import contextmanager
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock


class Handle(io.BytesIO):
    def fileno(self): return 42


class LockLifecycleTests(unittest.TestCase):
    def helper(self, effects=None, clock=None, handle=None):
        source=Path(__file__).parents[1]/'scripts/employee_package_launcher.py'
        fn=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='launch_request_lock')
        handle=handle or Handle()
        crt=Mock(LK_NBLCK=1,LK_UNLCK=2)
        if effects is not None:crt.locking.side_effect=effects
        timer=Mock();timer.monotonic.side_effect=clock or [0]
        env={'contextmanager':contextmanager,'open':Mock(return_value=handle),'msvcrt':crt,'time':timer,'sys':sys}
        exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),'exec'),env)
        return env['launch_request_lock'],handle,crt,timer

    def test_first_and_subsequent_requests_release_and_close(self):
        for _ in range(2):
            lock,h,crt,_=self.helper()
            with lock('test.lock'):self.assertFalse(h.closed)
            self.assertTrue(h.closed)
            self.assertEqual([c.args[1] for c in crt.locking.call_args_list],[1,2])

    def test_contended_request_retries_then_releases(self):
        lock,h,crt,timer=self.helper([OSError('busy'),None,None],[0,1])
        with lock('test.lock'):pass
        self.assertTrue(h.closed);timer.sleep.assert_called_once_with(.25)
        self.assertEqual([c.args[1] for c in crt.locking.call_args_list],[1,1,2])

    def test_acquisition_timeout_closes_without_unlocking(self):
        lock,h,crt,_=self.helper([OSError('busy')],[0,91])
        with self.assertRaises(RuntimeError):
            with lock('test.lock'):self.fail('must not enter')
        self.assertTrue(h.closed)
        self.assertEqual([c.args[1] for c in crt.locking.call_args_list],[1])

    def test_server_preparation_error_releases_and_preserves_error(self):
        lock,h,crt,_=self.helper()
        error=RuntimeError('server exited')
        with self.assertRaises(RuntimeError) as caught:
            with lock('test.lock'):raise error
        self.assertIs(caught.exception,error);self.assertTrue(h.closed)
        self.assertEqual(crt.locking.call_args_list[-1].args[1],2)

    def test_unlock_failure_does_not_hide_startup_failure(self):
        lock,h,_,_=self.helper([None,OSError('unlock')])
        error=RuntimeError('startup failed')
        with self.assertRaises(RuntimeError) as caught:
            with lock('test.lock'):raise error
        self.assertIs(caught.exception,error);self.assertTrue(h.closed)
        self.assertIn('unlock',error.__notes__[0])

    def test_unlock_failure_remains_visible_and_handle_closes(self):
        lock,h,_,_=self.helper([None,OSError('unlock')])
        with self.assertRaisesRegex(OSError,'unlock'):
            with lock('test.lock'):pass
        self.assertTrue(h.closed)


if __name__=='__main__':unittest.main()
