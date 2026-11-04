"""Copy selected PC R9 originals and launcher logs with byte hashes; no product mutation.

Run from the existing PC development Python, not inside the product payload.
Browser geometry JSON is collected separately with pc_r9_geometry.js.
"""
import argparse
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

R9_FILES = ('RESUMED_RESULT_KO.txt', 'RESUMED_BUTTON_60.csv', 'SSOT_VS_ACTUAL_CHROME.png')
LOG_FILES = ('bootstrap.log', 'server.log')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def collect(r9, data, output):
    r9, data, output = r9.resolve(), data.resolve(), output.resolve()
    if any(output == source or output.is_relative_to(source) or source.is_relative_to(output)
           for source in (r9, data)):
        raise ValueError('Evidence destination must be separate from R9 and product data')
    output.mkdir(parents=True, exist_ok=False)
    entries, missing = [], []
    for group, root, names in (('r9', r9, R9_FILES), ('launcher', data / 'logs', LOG_FILES)):
        for name in names:
            source = root / name
            if not source.is_file():
                missing.append(group + '/' + name)
                continue
            if source.is_symlink():
                raise ValueError('Refusing symlink evidence: ' + name)
            target = output / group / name
            target.parent.mkdir(exist_ok=True)
            before = sha(source)
            shutil.copyfile(source, target)
            after = sha(source)
            copied = sha(target)
            entries.append({'path': target.relative_to(output).as_posix(), 'bytes': target.stat().st_size,
                            'sha256': copied, 'source_sha256_before': before,
                            'source_sha256_after': after, 'stable_snapshot': before == after == copied})
    lock = data / 'launch.lock'
    lock_state = {'exists': lock.exists()}
    if lock.is_file():
        stat = lock.stat()
        lock_state.update(bytes=stat.st_size, mtime_ns=stat.st_mtime_ns)
    receipt = {'scope': 'PC_R9_ORIGINALS_AND_LOG_SNAPSHOT_ONLY',
               'collected_utc': datetime.now(timezone.utc).isoformat(), 'files': entries,
               'missing': missing, 'launch_lock_metadata': lock_state,
               'lock_owner_verified': False, 'owner_pc_pass': False, 'full_product_pass': False,
               'notes': ['Live logs may change; unstable snapshots require a second capture.',
                         'No process was stopped, no lock deleted, no model invoked.',
                         'Review logs for secrets before external handoff.']}
    (output / 'MANIFEST.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    archive = output / 'PC_R9_DIAGNOSTICS.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(output.rglob('*')):
            if path.is_file() and path != archive:
                z.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('Collected ZIP CRC failure')
    delivery = {'zip': archive.name, 'bytes': archive.stat().st_size, 'sha256': sha(archive),
                'crc': 'PASS', 'missing': missing,
                'unstable': [e['path'] for e in entries if not e['stable_snapshot']],
                'runtime_pass': False}
    (output / 'DELIVERY.json').write_text(json.dumps(delivery, indent=2)+'\n', encoding='utf-8')
    return delivery


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--r9-root', type=Path, required=True)
    ap.add_argument('--data-root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = collect(args.r9_root, args.data_root, args.output)
    print(json.dumps(result, indent=2))
    return 1 if result['missing'] or result['unstable'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
