import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec=importlib.util.spec_from_file_location('collector',Path(__file__).parents[1]/'scripts/collect_pc_r9_diagnostics.py')
collector=importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.r9=self.root/'r9';self.r9.mkdir()
        self.data=self.root/'data';(self.data/'logs').mkdir(parents=True)
        for name in collector.R9_FILES:(self.r9/name).write_bytes(b'SYNTHETIC_TEST_ONLY')
        for name in collector.LOG_FILES:(self.data/'logs'/name).write_bytes(b'SYNTHETIC_LOG')
        (self.data/'launch.lock').write_bytes(b'0')

    def test_snapshot_crc_hash_and_originals_unchanged(self):
        result=collector.collect(self.r9,self.data,self.root/'out')
        self.assertEqual(result['missing'],[]);self.assertEqual(result['unstable'],[])
        self.assertFalse(result['runtime_pass'])
        receipt=json.loads((self.root/'out/MANIFEST.json').read_text())
        self.assertEqual(len(receipt['files']),5)
        self.assertTrue(all(x['stable_snapshot'] for x in receipt['files']))
        self.assertEqual((self.data/'launch.lock').read_bytes(),b'0')
        with zipfile.ZipFile(self.root/'out/PC_R9_DIAGNOSTICS.zip') as z:self.assertIsNone(z.testzip())

    def test_missing_original_is_reported(self):
        (self.r9/collector.R9_FILES[0]).unlink()
        result=collector.collect(self.r9,self.data,self.root/'out')
        self.assertIn('r9/'+collector.R9_FILES[0],result['missing'])

    def test_output_cannot_overwrite_source_or_existing_evidence(self):
        with self.assertRaises(ValueError):collector.collect(self.r9,self.data,self.r9/'out')
        collector.collect(self.r9,self.data,self.root/'out')
        with self.assertRaises(FileExistsError):collector.collect(self.r9,self.data,self.root/'out')


if __name__=='__main__':unittest.main()
