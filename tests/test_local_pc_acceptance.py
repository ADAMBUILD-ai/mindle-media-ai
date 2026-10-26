import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("validator", Path(__file__).parents[1] / "scripts/validate_local_pc_acceptance.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        data = b"SYNTHETIC TEST ONLY; NOT PC EXECUTION EVIDENCE"
        (self.root / "fixture.txt").write_bytes(data)
        self.proof = {"path": "fixture.txt", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        self.receipt = {
            "scope": "OFFICE_PC_NEW_EXECUTION", "source_sha": validator.SOURCE,
            "zip_sha256": validator.ZIP_SHA, "runtime_id": validator.RUNTIME,
            "full_product_pass": False, "execution_id": "TEST", "started_at": "TEST",
            "finished_at": "TEST", "browser_version": "TEST",
            "runtime_identity": self.proof, "environment": self.proof, "approved_ui_screenshot": self.proof,
            "inputs": [{"id": str(i), "file": self.proof, "result": self.proof} for i in range(8)],
            "buttons": [{"id": str(i), "selector": "TEST", "reason": "TEST", "disposition": "active",
                         "result": "FAIL", "evidence": self.proof} for i in range(60)],
            "model_jobs": [{"operation": op, "execution_id": "TEST", "request_id": op, "job_id": op,
                            "receipt": self.proof, "output": self.proof} for op in validator.OPERATIONS],
            "media": {"MediaError_code": 4, "readyState": 0, "videoWidth": 0, "currentSrc": "TEST",
                      "before_time": 0, "after_time": 0, "evidence": self.proof},
            "lifecycle": {key: self.proof for key in ("single_instance", "save", "cold_close", "reopen",
                           "export_zip", "export_mp4", "play_seek_audio")}}

    def test_complete_failed_run_is_reviewable_not_runtime_pass(self):
        self.assertEqual(validator.validate(self.receipt, self.root), [])

    def test_missing_controls_and_inputs_rejected(self):
        self.receipt["buttons"].pop()
        self.receipt["inputs"].pop()
        self.assertEqual(len(validator.validate(self.receipt, self.root)), 2)

    def test_old_candidate_and_foreign_execution_rejected(self):
        self.receipt["source_sha"] = "old"
        self.receipt["model_jobs"][0]["execution_id"] = "old"
        self.assertEqual(len(validator.validate(self.receipt, self.root)), 2)

    def test_tampered_file_rejected(self):
        (self.root / "fixture.txt").write_bytes(b"tampered")
        self.assertTrue(validator.validate(self.receipt, self.root))

    def test_absolute_traversal_and_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / "external.txt"
            outside.write_text("external")
            (self.root / "link").symlink_to(outside)
            for path in (str(outside), "../external.txt", "link"):
                self.receipt["runtime_identity"] = {**self.proof, "path": path}
                self.assertTrue(validator.validate(self.receipt, self.root), path)

    def test_global_pass_and_missing_media_fields_rejected(self):
        self.receipt["full_product_pass"] = True
        del self.receipt["media"]["MediaError_code"]
        self.assertEqual(len(validator.validate(self.receipt, self.root)), 2)


if __name__ == "__main__":
    unittest.main()
