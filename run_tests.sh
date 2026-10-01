#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TEST_PYTHON="${MINDLE_TEST_PYTHON:-${PYTHON:-python}}"

cd "$ROOT_DIR"
PYTHONPATH=src "$TEST_PYTHON" -m pytest -q
"$TEST_PYTHON" model_scout/validate_evidence_sync.py
node --test ui/interaction.test.js ui/ssot_structure.test.js
"$TEST_PYTHON" model_scout/validate_package_manifest.py --source
