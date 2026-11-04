"""Verify actual codec derivative and original artifact preservation."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from media_ai.browser_preview import create_preview, digest, faststart


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class BrowserPreviewTests(unittest.TestCase):
    def test_mpeg4_derivative_is_h264_yuv420p_faststart_without_changing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'model.mp4'
            destination = Path(directory) / 'browser.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                            'color=c=blue:s=64x48:r=10', '-t', '0.3',
                            '-c:v', 'mpeg4', str(source)], check=True)
            original = digest(source)
            result = create_preview(source, original, destination)
            self.assertEqual(digest(source), original)
            self.assertEqual(result['ffprobe']['streams'][0]['codec_name'], 'h264')
            self.assertEqual(result['ffprobe']['streams'][0]['pix_fmt'], 'yuv420p')
            self.assertTrue(faststart(destination))
            self.assertEqual(result['output']['sha256'], digest(destination))
            with self.assertRaises(ValueError):
                create_preview(source, original, source)
            with self.assertRaises(ValueError):
                create_preview(source, '0' * 64, destination)

    def test_corrupt_mp4_is_not_marked_faststart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'corrupt.mp4'
            path.write_bytes(b'\x00\x00\x00\x01moov\x00')
            self.assertFalse(faststart(path))
