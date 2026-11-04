# Reproduction and handoff

Source: `3a889d9af5e0e91b4efc8132eb86e11251f1ced5`. Fresh Linux development data directory required. Never overwrite c37 payload.

1. Obtain official pinned Qwen GGUF and llama.cpp archive from QWEN15_MODEL.json / LLAMA_RELEASE_IDENTITY.json. Verify upstream LFS/GitHub SHA256 before extraction; preserve all runtime shared libraries. GGUF/engine binary hashes and runtime tree hashes must match VERIFIED_RUNTIME_ENGINES.json.
2. Install pinned `sherpa-onnx==1.13.8`; exact observed Python dependency versions are in PROVENANCE.json. Download Supertonic archive from SUPERTONIC_ASSET.json, require its exact GitHub SHA256 before extraction. Model terms are in SUPERTONIC_LICENSE; upstream code license does not replace model license. No external provider/API key.
3. Write data-dir/runtime-engines.json with verified local paths and hashes (example is this development manifest). Keep model binaries outside git. No auto-acceptance of changed identity.
4. Prepare the same development FFmpeg, test font and Chromium fixtures as the prior runtime evidence. Run `WORKFLOW_REPO_ROOT=/absolute/product WORKFLOW_DATA_DIR=/absolute/fresh-data /absolute/venv/bin/python docs/evidence/media-ai-local-engines-closeout-20261018/run_runtime.py`. This harness performs real model inference, synth, product HTTP/browser work and own-server restart. Never run another filesystem exec against a live harness; preserve one orchestrator and its polling session.
5. browser_reopen.cjs is the additional existing-project restore/audio decode check. Supply URL, OUT, PROJECT_ID, Chromium paths and development FONTCONFIG_FILE. It must not be counted as Windows EXE acceptance or human hearing.

Tests: selected affected pytest suite in PYTEST.txt; Node UI suite in NODE.txt. New tests validate rejection boundaries, not substitute engine inference. Actual outputs/provenance are separate.

Accepted planner cases are bounded evidence. The neural voice has not been human-rated. Source changed files are workflow_planner.py, workflow_worker.py and test_local_planner_scope.py; UI source and PHOTO model pipeline are unchanged.

Windows worker must wait for a separately authorized new candidate whose source/manifest/EXE/ZIP identities include this change and all prior pending repairs. Native Windows dependencies must be prepared and hashed first. Do not use Linux binaries, c37, validator exit 0 or source browser evidence as Windows acceptance. Preserve package_build_allowed=false until authorized. No final employee package or merge.
