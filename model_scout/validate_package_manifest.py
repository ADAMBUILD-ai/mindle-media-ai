"""Fail a deliverable archive if it cannot reproduce the project test surface."""
from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile

REQUIRED_PREFIXES = (
    "mindle-media-ai/src/",
    "mindle-media-ai/tests/",
    "mindle-media-ai/docs/",
    "mindle-media-ai/evidence/",
    "mindle-media-ai/ui/",
    "mindle-media-ai/model_scout/",
)
REQUIRED_FILES = (
    "mindle-media-ai/pyproject.toml",
    "mindle-media-ai/run_tests.sh",
    "mindle-media-ai/model_scout/validate_evidence_sync.py",
    "mindle-media-ai/model_scout/validate_package_manifest.py",
)


def validate(archive: Path) -> None:
    if not archive.is_file():
        raise SystemExit(f"package missing: {archive}")
    with ZipFile(archive) as package:
        names = set(package.namelist())
    missing_prefixes = [prefix for prefix in REQUIRED_PREFIXES if not any(name.startswith(prefix) for name in names)]
    missing_files = [filename for filename in REQUIRED_FILES if filename not in names]
    if missing_prefixes or missing_files:
        raise SystemExit(f"package incomplete: prefixes={missing_prefixes}; files={missing_files}")
    print("package completeness pass")


def validate_source_tree(root: Path) -> None:
    missing_prefixes = [prefix for prefix in REQUIRED_PREFIXES if not (root / prefix.split("/", 2)[1]).is_dir()]
    missing_files = [filename for filename in REQUIRED_FILES if not (root / filename.removeprefix("mindle-media-ai/")).is_file()]
    if missing_prefixes or missing_files:
        raise SystemExit(f"source tree incomplete: prefixes={missing_prefixes}; files={missing_files}")
    print("source tree completeness pass")


if __name__ == "__main__":
    if sys.argv[1:] == ["--source"]:
        validate_source_tree(Path(__file__).parents[1])
    elif len(sys.argv) == 2:
        validate(Path(sys.argv[1]))
    else:
        raise SystemExit("usage: validate_package_manifest.py PACKAGE.zip | --source")
