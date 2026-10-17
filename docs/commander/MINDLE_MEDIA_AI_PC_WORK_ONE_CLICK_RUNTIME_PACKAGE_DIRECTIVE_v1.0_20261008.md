# MINDLE MEDIA AI — WINDOWS PC WORK ONE-CLICK RUNTIME PACKAGE DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — WINDOWS PC WORK FINAL RUNTIME DELIVERY
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-PACKAGE-R1
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
General Work baseline: 9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb

## 0. AUTHORIZATION / START POINT

General Work has passed:
PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK

PC Work is now authorized.

Do NOT return to the previous manual employee installer flow.
Do NOT require the owner/employee to run PowerShell/CMD commands, choose folders, answer TEST/YES prompts, install Python, run pip, clone Git, set HF_TOKEN, or manually download models.

External Marketing / AVORA live integration remains DEFERRED_EXTERNAL and does not block this Windows runtime closeout.

## 1. FINAL EMPLOYEE EXPERIENCE

The target is a ONE-CLICK RUNTIME PACKAGE.

The only normal user action allowed to start the product is:

DOUBLE-CLICK MINDLE MEDIA AI

From that action the runtime must automatically:
1. validate/materialize its own local runtime payload
2. start exactly one local product server
3. wait for health readiness
4. open the approved MINDLE MEDIA AI web UI automatically
5. remain usable without developer tooling

No manual ZIP extraction step is allowed in the employee flow.
If internal extraction/materialization is needed, the launcher performs it automatically.

Preferred visible artifact:
MINDLE_MEDIA_AI_RUN.exe

Equivalent single-click launcher form is allowed only if it produces the same no-terminal/no-manual-step experience.

## 2. ARCHITECTURE — PORTABLE RUNTIME, NOT COMPLEX INSTALLER

Implement a portable/self-contained runtime delivery.

Preferred structure:
- one employee-visible launcher
- versioned internal runtime under a controlled local directory such as %LOCALAPPDATA%\MINDLE_MEDIA_AI\runtime\<version>
- persistent user/project data stored separately under %LOCALAPPDATA%\MINDLE_MEDIA_AI\data or the existing safe persistent location
- runtime replacement must not delete user data
- no registry dependence unless strictly necessary
- no administrator/UAC requirement unless technically unavoidable and evidenced

The launcher may self-extract or materialize a bundled payload on first run.
Subsequent launches should reuse the validated runtime instead of unpacking everything again.

## 3. REUSE EXISTING WINDOWS WORK — DO NOT RESTART FROM SCRATCH

Inspect and reuse only useful parts of the existing Windows/package code, including where applicable:
- scripts/launch_media_ai_windows.ps1
- scripts/employee_package_launcher.py
- scripts/build_employee_distribution_package.py
- scripts/employee_installed_function_gate.py
- scripts/FINAL_EMPLOYEE_PACKAGE_HOST_GATE.ps1

However:
- the old multi-step employee installer UX is rejected
- install_employee_package.ps1 must not be the normal employee path
- FINAL_EMPLOYEE_PACKAGE_HOST_GATE must be adapted/replaced for one-click runtime behavior
- old manual VC runtime repair steps must not be exposed to the employee

Delete nothing historical. Mark obsolete packaging paths as legacy/not-user-facing where necessary.

## 4. BUNDLED RUNTIME DEPENDENCIES

The one-click runtime must not depend on:
- system Python
- system pip
- Git
- repository checkout
- VS Code
- HF_TOKEN for normal base-product use
- manual Hugging Face/model downloads
- developer worktree
- developer environment variables

PC Work must inventory and resolve all runtime dependencies needed by the passed base product:
- Python runtime / packaged executable runtime
- required Python packages
- FFmpeg / ffprobe
- OpenCV / NumPy / OpenVINO and other runtime libraries
- fonts needed for Korean/CJK subtitle rendering
- browser-opening mechanism
- required verified model weights/cache
- VC runtime / native DLL requirements
- any transitive DLLs

For every bundled third-party binary/model:
- verify redistribution/license status
- include required notices/licenses
- record SHA-256
- do not silently include a dependency without entitlement

If a required component cannot legally or technically be bundled:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY
with exact component/evidence.
Do not push manual repair instructions onto the employee as PASS.

## 5. MODEL / OFFLINE BEHAVIOR

Normal employee use must not require manually fetching models.

For the passed base features:
- PHOTO segmentation
- PHOTO 4x upscale
- VIDEO tracking
- Korean STT

the package must either bundle the verified model assets or automatically materialize them from an approved local payload without employee intervention.

A first-run network download is not accepted as the default PASS path unless the owner explicitly approves it later.

Model identity/revision/hash must match the verified General Work lineage or an explicitly revalidated equivalent.

## 6. SINGLE-INSTANCE / PORT / RELAUNCH

Implement robust local runtime lifecycle:

- double-click #1 starts one runtime
- double-click #2 while already running must NOT create another server
- second launch should open/focus the existing UI
- use a PID/lock/health strategy robust to stale locks
- port collision must be handled deterministically
- do not kill unrelated processes
- orphaned prior MINDLE MEDIA AI runtime must be detected and recovered safely
- relaunch after browser close must work
- relaunch after runtime shutdown must work
- Windows reboot/logoff must not corrupt project data

Record process IDs, selected port, health URL, and single-instance Evidence.

## 7. BROWSER AUTO-OPEN

After server health is READY:
- open the product automatically
- use a Windows-available browser path/default-browser mechanism that does not require Chrome installation
- MINDLE MEDIA AI title and approved UI must appear
- do not expose a developer terminal as the normal UX
- do not open multiple tabs/windows for one launch

If application/window mode is used, it must preserve all required browser media behavior and downloads.

## 8. OWNER-APPROVED UI / PRODUCT LOCK

Packaging work must not redesign the UI.

Preserve:
- title MINDLE MEDIA AI
- VIDEO approved structure
- PHOTO landscape-first Preview
- portrait Auto Fit centered
- original aspect ratio
- PHOTO brightness / contrast / highlights / shadows / saturation / temperature / sharpness
- 광고 숏폼 entry
- dark navy + VIDEO blue/cyan + PHOTO purple/magenta identity
- disabled/NOT_IMPLEMENTED controls exactly as General Work classified them unless PC Work specifically implements an OS/runtime lifecycle control

External Shortform remains graceful DEFERRED_EXTERNAL.
Do not require Marketing/AVORA for base product startup.

## 9. WINDOWS CLEAN-PROFILE E2E — REQUIRED

The final PASS requires actual Windows execution from an ordinary user profile.

Test from a default/clean employee-style Windows profile that does not rely on:
- repository clone
- system Python
- pip environment
- Git
- developer terminal state
- pre-set HF_TOKEN
- pre-running product server

Required scenario:

1. place the delivery artifact as an employee would receive it
2. do not manually extract with a separate utility
3. double-click the single launcher
4. prove first-run internal materialization if used
5. prove exactly one runtime starts
6. prove browser/UI auto-opens
7. record time-to-ready
8. load a landscape PHOTO
9. load a portrait PHOTO and verify Auto Fit
10. exercise at least one basic PHOTO correction
11. run PHOTO segmentation using bundled runtime/model
12. run PHOTO 4x upscale
13. import VIDEO and verify H.264 browser playback
14. run VIDEO tracking
15. run Korean STT and verify UI visibility
16. Save project
17. shut down product/runtime safely
18. relaunch by double-click only
19. reopen saved project
20. Export through UI
21. verify exported ZIP/media hashes and CRC
22. double-click again while runtime is already active and prove no duplicate server
23. reboot/logoff or equivalent cold-process reset, relaunch, and prove project data remains
24. verify no manual Marketing/AVORA setup was required

## 10. NEGATIVE / FAILURE TESTS

Prove:
- missing/corrupt runtime payload produces a clear actionable error, not a blank black window
- no 300-second blind wait after fatal startup error
- occupied port is handled without killing unrelated service
- stale lock/PID recovers
- missing browser association has a clear fallback/error
- malformed input does not corrupt existing project
- package does not use source-tree-relative paths
- package does not write into the repository
- package does not depend on current working directory
- Korean/space-containing Windows paths work

## 11. WINDOWS PATH / CJK / CODEC

Explicitly validate:
- Windows paths with spaces
- Korean Windows user/profile path where practical
- UTF-8 project/file names
- CJK subtitle font availability from the bundled/approved runtime path
- FFmpeg H.264/yuv420p/faststart Preview
- ffprobe availability from packaged runtime
- browser Range/206 seek behavior

## 12. PACKAGE INTEGRITY

Publish:
- final delivery artifact name
- bytes
- SHA-256
- internal manifest/hash list
- license/notice manifest
- exact General Work baseline commit
- exact PC Work implementation commit
- no source-tree dependency
- no employee manual install steps

If a single-file launcher materializes a runtime payload, also record:
- embedded payload hash
- materialized runtime manifest hash
- first-run and second-run behavior

## 13. REGRESSION

PC packaging changes must preserve:
- General Work Python 77 baseline or greater
- UI tests 2 or greater
- General Work actual browser smoke on unchanged product behavior
- pip/runtime dependency consistency
- Control Plane validator
- approved UI hash/invariant checks

Do not re-run expensive model inference in CI merely for packaging if actual Windows E2E already proves the bundled model runtime; however final Windows E2E must execute the required real base functions.

## 14. REQUIRED EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_PC_WORK_ONE_CLICK_RUNTIME_PACKAGE_REVIEW_v1.0_20261008.md

Machine Evidence:
docs/evidence/media-ai-pc-work-one-click-runtime-20261008/EVIDENCE.json

Evidence root:
docs/evidence/media-ai-pc-work-one-click-runtime-20261008/

Required files:
- PACKAGE_MANIFEST.json
- LICENSE_AND_REDISTRIBUTION_AUDIT.json
- WINDOWS_HOST_PROFILE.json
- FIRST_DOUBLE_CLICK_RESULT.json
- SECOND_DOUBLE_CLICK_SINGLE_INSTANCE_RESULT.json
- BROWSER_AUTO_OPEN_RESULT.json
- WINDOWS_RUNTIME_FUNCTION_E2E.json
- SAVE_REOPEN_COLD_RELAUNCH_RESULT.json
- EXPORT_INTEGRITY_RESULT.json
- NEGATIVE_STARTUP_TESTS.json
- PROCESS_PORT_LIFECYCLE.json
- REGRESSION_RESULT.json
- DELIVERY_ARTIFACT_SHA256.txt
- REMOTE_READBACK.txt

## 15. PASS / FAIL VOCABULARY

Only when the ordinary-user Windows flow passes end to end:
PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E

If packaging artifact exists but clean/default Windows E2E has not run:
PACKAGE_BUILT_WINDOWS_E2E_NOT_PROVEN

If employee must manually install/fix dependencies:
FAIL_ONE_CLICK_RUNTIME_USER_FRICTION

If duplicate server/process occurs:
FAIL_SINGLE_INSTANCE_RUNTIME

If legal/redistribution evidence blocks bundling:
BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY

External Marketing/AVORA remains:
DEFERRED_EXTERNAL
and does not prevent this local runtime PASS.

## 16. REPOSITORY RULES

- canonical branch only
- no force push
- no main/default merge
- no new repo/worktree/branch
- PR #23 remains HOLD / DO NOT MERGE
- preserve historical Evidence
- do not claim external Shortform live PASS
- do not restore the rejected complex employee installer UX

## FINAL COMMAND

START FROM GENERAL WORK PASS HEAD 9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb.

BUILD THE SIMPLE ONE-CLICK WINDOWS RUNTIME EXPERIENCE.
DOUBLE-CLICK MUST BE THE ONLY NORMAL START ACTION.
NO MANUAL EXTRACTION, PYTHON, PIP, GIT, TERMINAL, TOKEN, MODEL DOWNLOAD, OR DEPENDENCY REPAIR BY THE EMPLOYEE.

RUN IT ON THE ACTUAL WINDOWS PC/DEFAULT EMPLOYEE-STYLE PROFILE.
PROVE FIRST RUN, SECOND RUN, SINGLE INSTANCE, PHOTO, VIDEO, STT, SAVE/REOPEN, EXPORT, COLD RELAUNCH, AND DATA PRESERVATION.
PUBLISH EVIDENCE AND REMOTE READBACK.
