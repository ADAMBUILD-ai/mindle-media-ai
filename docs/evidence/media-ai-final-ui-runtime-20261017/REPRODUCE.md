# Browser harness reproduction

The receipt was generated with the harness copied to the materialized repository root. Copy check_final_ui.cjs and check_timeline_identity.py from this folder to that root before running. Install Playwright in the development environment and set CODEX_PRIMARY_RUNTIME_NODE_MODULES to its parent node_modules. The browser executable defaults to ../browser-runtime/extracted/chromium and LD_LIBRARY_PATH to its lib directory; adapt only these harness paths for your development environment.

Create fixture.png as a plain480x960 PNG. Generate six-second timeline_fixture.mp4 with FFmpeg testsrc2 320x180/12fps and sine440Hz/22050Hz, encode libx264/yuv420p + AAC and +faststart. Create timeline_silent.mp4 with -an -c:v copy from that file. These generated fixtures are test input, not adopted AI outputs. Optional fonts/NotoSansCJKkr-Regular.otf is injected only by the browser harness.

Run node check_final_ui.cjs, node --test ui/*.test.js, python check_timeline_identity.py. The browser harness runs its HTTP server and browser together, supports HTTP Range, and uses fixture assets/latest API responses. It does not start the product backend or validate Windows/Save/Export. The identity harness executes the extracted production fingerprint method without importing model dependencies. It checks builder syntax/list inclusion only.
