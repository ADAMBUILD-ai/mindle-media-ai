from __future__ import annotations
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
golden = subprocess.check_output(['git', 'show', '97900cc6c784e74b4224333fa2cc84d29c611f87:ui/approved_visual.css'])
current = (ROOT / 'ui/approved_visual.css').read_bytes()
golden_blob = subprocess.check_output(['git', 'rev-parse', '97900cc6c784e74b4224333fa2cc84d29c611f87:ui/approved_visual.css'], text=True).strip()
current_blob = subprocess.check_output(['git', 'hash-object', 'ui/approved_visual.css'], text=True).strip()
assert current.replace(b'\r\n', b'\n') == golden, 'approved_visual.css is not the 97900cc golden content'
assert current_blob == golden_blob, 'approved_visual.css git blob does not match the golden baseline'
css = current.decode('utf-8')
assert 'v20.2.5 canonical row-height system' not in css
assert 'max-height: 100%' not in css
launcher = (ROOT / 'scripts/launch_media_ai_windows.ps1').read_text(encoding='utf-8')
assert '$RepoRoot' in launcher and 'ui_refresh' not in launcher and 'copy' not in launcher.lower()
print('WORKSPACE_MIRROR_PASS')
print('GOLDEN_CSS_SHA256=' + hashlib.sha256(golden).hexdigest())
print('CURRENT_CSS_SHA256=' + hashlib.sha256(current).hexdigest())
print('GIT_BLOB_MATCH=PASS')
