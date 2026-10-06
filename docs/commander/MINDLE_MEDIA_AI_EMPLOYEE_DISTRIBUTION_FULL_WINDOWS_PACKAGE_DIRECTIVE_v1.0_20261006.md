# MINDLE MEDIA AI — EMPLOYEE DISTRIBUTION FULL WINDOWS PACKAGE DIRECTIVE v1.0

Date: 2026-10-06
Status: ACTIVE — BUILD AND TEST ACTUAL DISTRIBUTION PACKAGE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-EMPLOYEE-PACKAGE-V1.0

## 0. Owner intent

Build a COMPLETE Windows employee distribution package.

This is NOT a desktop shortcut export.
This is NOT a source-code ZIP.
This is NOT a developer package.

The recipient employee must be able to receive the package by file transfer, install/extract it, double-click the MINDLE MEDIA AI icon, and use the product without:

- GitHub
- git
- Python installed separately
- pip
- VS Code
- PowerShell commands typed manually
- Hugging Face login
- HF_TOKEN
- model downloads
- repository checkout
- developer knowledge

The package must contain all runtime components required for the approved local/offline product functions.

## 1. Deliverables

Produce BOTH:

### A. Complete offline portable package
`dist/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0/`

and archive:

`dist/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip`

### B. Transfer-friendly split package

Split the complete ZIP into numbered binary parts suitable for ordinary file transfer.

Example:
- `MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip.001`
- `...002`
- etc.

Default target part size:
300 MiB

Also provide:
- `REASSEMBLE_AND_INSTALL.cmd`
- `REASSEMBLE_AND_INSTALL.ps1`

The script must:
1. verify all expected part hashes
2. concatenate parts in exact order
3. verify final ZIP SHA-256
4. extract
5. invoke installer
6. show PASS/FAIL clearly

If a transfer service has a smaller file limit, the splitter must support a configurable smaller part size.

## 2. Installation experience

The employee should perform only:

1. Receive package/files
2. Double-click `INSTALL_MINDLE_MEDIA_AI.cmd`
3. Wait for installation
4. Double-click desktop icon `MINDLE MEDIA AI`

No terminal typing.

Install location:

`%LOCALAPPDATA%\MINDLE\MEDIA_AI\`

User data location:

`%LOCALAPPDATA%\MINDLE\MEDIA_AI_DATA\`

Never write employee data into the app installation folder.

Installer must:
- install app files
- install bundled runtime
- install bundled model cache
- install bundled FFmpeg tools
- create data folder
- create one branded desktop shortcut
- create Start Menu shortcut
- preserve existing user data on upgrade
- support reinstall
- support uninstall without deleting user data unless explicitly chosen
- write install receipt/version manifest

No administrator rights should be required unless technically unavoidable.
Prefer per-user install.

## 3. Package architecture

Required package layout:

```
MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0/
  INSTALL_MINDLE_MEDIA_AI.cmd
  INSTALL_MINDLE_MEDIA_AI.ps1
  UNINSTALL_MINDLE_MEDIA_AI.cmd
  README_FIRST_KO.txt
  PACKAGE_MANIFEST.json
  PACKAGE_SHA256SUMS.txt
  LICENSES/
  docs/
    MINDLE_MEDIA_AI_USER_GUIDE_KO.pdf-or-html
    MINDLE_MEDIA_AI_USER_GUIDE_v1.0_20261003.md
  app/
    ui/
    src/
    launcher/
  runtime/
    python/
    site-packages/
  models/
    sam21/
    whisper-small/
  omz/
    intel/
      single-image-super-resolution-1032/
        FP32/
  tools/
    ffmpeg/
      ffmpeg.exe
      ffprobe.exe
  assets/
    brand/
  tests/
    employee_smoke_test.ps1
  uninstall/
```

Exact runtime structure may be adjusted if needed, but all required components must remain package-local.

## 4. Adopted models — include exact verified identities only

### SAM 2.1 Hiera Base Plus
Revision:
`b7320756a13354e7530a63935656d35b2f91a290`

model.safetensors:
- bytes: 323476296
- SHA-256: `2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780`
- license: Apache-2.0

Package snapshot must include all files required by the adapter, including:
- config.json
- model.safetensors
- preprocessor_config.json
- processor_config.json

### Whisper-small
Revision:
`973afd24965f72e36ca33b3055d56a652f456b4d`

model.safetensors:
- bytes: 966995080
- SHA-256: `1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b`
- license: Apache-2.0

Package snapshot must include:
- config.json
- generation_config.json
- model.safetensors
- preprocessor_config.json
- tokenizer.json
- tokenizer_config.json
- all additional local files proven required by AutoProcessor / AutoModelForSpeechSeq2Seq

### Intel single-image-super-resolution-1032
Revision:
`a6946b6d6ce42cbf4278df20275fab199655fc7d`

Include exact:
- `single-image-super-resolution-1032.xml`
- `single-image-super-resolution-1032.bin`

Verify the existing SHA-384 identities from the adopted model SSOT.

### Forbidden
Do NOT package as active substitutes:
- Whisper Large v3 Turbo
- Qualcomm RealESRGAN x4plus ONNX

## 5. No secrets in employee package

ABSOLUTELY FORBIDDEN:
- HF_TOKEN
- GitHub token
- private repository credentials
- passwords
- API secrets
- personal paths
- developer account data

The employee package must run the adopted base local models without any Hugging Face authentication.

## 6. Required runtime code change — local package mode

Current development runtime requires `HF_TOKEN` at product_server startup.

That is unacceptable for employee distribution.

Implement explicit package-local mode.

Required environment/launch behavior:

`MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT=<installed package runtime root>`

When this local verified root is present and complete:
- SAM must use local snapshot only
- Whisper-small must use local snapshot only
- Intel SISR must use local package only
- NO Hugging Face network call
- NO HF_TOKEN requirement
- NO private repo lookup
- fail closed on missing/hash-mismatched model files

Modify `src/media_ai/product_server.py` and/or `ProductModelVault` minimally so:
- local package mode accepts no token
- network model acquisition is disabled for employee package mode
- local model hash verification remains mandatory

Do not weaken model identity checks.

## 7. Bundle exact runtime dependencies

Do NOT rely only on current pyproject.toml because actual verified runtime imports more packages.

From the proven Windows environment, capture exact working versions of at least:

- Python 3.11 x64 runtime
- torch CPU
- transformers
- safetensors
- huggingface_hub if still needed internally
- numpy
- Pillow
- OpenCV
- OpenVINO
- tokenizers
- required transitive runtime dependencies

Also bundle:
- ffmpeg.exe
- ffprobe.exe

Use the ACTUAL proven PC runtime versions.
Generate:

`RUNTIME_LOCK_EMPLOYEE_WIN_X64.txt`

with exact versions and hashes where practical.

Do not silently upgrade packages during packaging.

## 8. Browser / UI launch behavior

Employee must see an app, not a developer console.

Final desktop shortcut:
`MINDLE MEDIA AI`

It must invoke a package-local launcher.

The launcher must:
- discover installed package root from its own location
- not depend on Git repository or Git branch
- not execute `git rev-parse`
- compute package version / UI fingerprint from PACKAGE_MANIFEST.json
- start exactly one product server
- use a package-local fixed port strategy
- if preferred port is occupied by unrelated software, choose an approved fallback local port rather than kill unrelated processes
- wait for health/runtime identity
- open Edge/Chrome in app-style or stable new-window mode
- never open an old development repo
- never use historical worktree paths

No Git identity is required in employee mode.

## 9. Package runtime identity

Add package runtime identity endpoint fields:

- product = MINDLE MEDIA AI
- distribution = EMPLOYEE_WIN_X64
- package_version = 1.0
- build_commit
- package_manifest_sha256
- ui_fingerprint
- model_manifest_hash
- install_root
- data_root
- runtime_mode = LOCAL_OFFLINE_PACKAGE

Do not expose secrets.

## 10. Marketing / Shortform behavior in employee package

Base PHOTO / VIDEO local editing must work offline.

Advertising Shortform has an external Marketing AI dependency.

Employee package behavior:
- base product must not fail if Marketing AI bridge is unavailable
- Shortform button remains
- if Marketing AI service is unavailable, show a clear Korean message such as:
  `마케팅 AI 연결이 필요합니다. 기본 사진/영상 편집은 계속 사용할 수 있습니다.`
- no crash
- no hidden failure

If an approved internal Marketing endpoint can be configured separately, support it through a user-local configuration file, NOT hardcoded credentials.

Do not embed tokens.

## 11. Installer requirements

Create repository-owned installer scripts:

- `scripts/build_employee_distribution_package.ps1`
- `scripts/install_employee_package.ps1`
- `scripts/uninstall_employee_package.ps1`
- `scripts/split_employee_package.ps1`
- `scripts/reassemble_employee_package.ps1`

Installer must:
- be idempotent
- create branded icon
- create desktop shortcut
- create Start Menu shortcut
- register package version locally
- create logs under:
  `%LOCALAPPDATA%\MINDLE\MEDIA_AI_DATA\logs\`
- verify package manifest and model hashes before first launch

If package verification fails:
STOP and show a Korean error.
Never partially launch.

## 12. Full employee smoke test

Test on a CLEAN Windows user profile or a Windows environment that does NOT depend on the development repository.

Forbidden test:
running from the Git checkout and calling it an employee package test.

Required test:

1. Remove/rename access to development repo for test process
2. Install from package only
3. Confirm no system Python dependency
4. Confirm no Git dependency
5. Confirm no HF token
6. Launch from desktop icon
7. Verify exactly one product server
8. VIDEO import
9. VIDEO tracking
10. Korean STT with approved fixture
11. PHOTO import
12. SAM segmentation
13. Intel 4x upscale
14. Preview
15. Project save
16. Close
17. Reopen from desktop icon
18. Saved project reopen/persistence
19. Export
20. Shortform unavailable-path graceful behavior
21. Re-launch 2/2
22. Uninstall
23. Reinstall
24. Confirm user data preservation

Required result:
`EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS`

## 13. Package self-containment audit

Run a dependency audit and prove that the installed package has no runtime dependency on:

- repository path
- Git
- GitHub
- user developer profile
- Python installed on PATH
- pip
- private HF cache outside package
- environment secrets
- temporary build folder

Evidence:
`PACKAGE_SELF_CONTAINMENT_AUDIT.json`

## 14. Licenses and redistribution

Create:
`LICENSES/THIRD_PARTY_NOTICES.txt`
`LICENSES/MODEL_LICENSE_MANIFEST.json`

Include licenses/notices required for bundled:
- Python
- PyTorch and dependencies
- Transformers and dependencies
- OpenVINO
- FFmpeg build
- SAM model
- Whisper-small
- Intel SISR model
- other redistributed runtime libraries

Do not omit redistribution notices.

## 15. Output package and hashes

Required outputs:

`dist/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip`

`dist/transfer_parts/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip.001...`

`dist/transfer_parts/REASSEMBLE_AND_INSTALL.cmd`

`dist/transfer_parts/REASSEMBLE_AND_INSTALL.ps1`

Generate:
- SHA-256 for full ZIP
- SHA-256 for every split part
- exact byte sizes
- package manifest
- build commit
- UI fingerprint
- model manifest

## 16. User guide

Include a simple Korean guide:

`README_FIRST_KO.txt`

It should say, in simple terms:

1. 파일을 한 폴더에 모은다.
2. 분할본이면 REASSEMBLE_AND_INSTALL.cmd를 더블클릭한다.
3. 단일 ZIP이면 압축을 풀고 INSTALL_MINDLE_MEDIA_AI.cmd를 더블클릭한다.
4. 설치가 끝나면 바탕화면의 MINDLE MEDIA AI 아이콘을 더블클릭한다.
5. 사진/영상 파일을 불러와 사용한다.
6. 오류가 나면 설치 폴더를 지우지 말고 logs 폴더를 전달한다.

No developer instructions in employee guide.

## 17. Evidence

Human Review:
`docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_REVIEW_v1.0_20261006.md`

Machine Evidence:
`evidence/pc_remote/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_EVIDENCE_v1_0_20261006.json`

Detail:
`evidence/pc_remote/media-ai-employee-package-v1_0-20261006/`

Required detail evidence:
- PACKAGE_BUILD_MANIFEST.json
- RUNTIME_LOCK_EMPLOYEE_WIN_X64.txt
- MODEL_HASH_VERIFICATION.json
- FFmpeg identity
- PACKAGE_SELF_CONTAINMENT_AUDIT.json
- INSTALLER_TEST.json
- DESKTOP_SHORTCUT_TEST.json
- CLEAN_WINDOWS_ENVIRONMENT.json
- CLEAN_WINDOWS_FUNCTION_AUDIT.json
- SAVE_REOPEN_TEST.json
- EXPORT_TEST.json
- SHORTFORM_OFFLINE_BEHAVIOR.json
- UNINSTALL_REINSTALL_TEST.json
- PACKAGE_SHA256SUMS.txt
- SPLIT_PARTS_MANIFEST.json
- REMOTE_PUSH_VERIFY.txt

## 18. PASS vocabulary

PASS only:
`EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS`

Anything else:
- PACKAGE_BUILD_PARTIAL
- CLEAN_WINDOWS_TEST_FAILED
- MODEL_BUNDLE_MISMATCH
- RUNTIME_DEPENDENCY_LEAK
- BLOCKED
- FAIL

## 19. Final delivery gate

Do not call the package complete because a ZIP exists.

Complete only when:
- package built
- hashes verified
- split transfer set built
- install from package tested
- clean Windows-style E2E passed
- desktop icon worked
- models ran locally
- save/reopen/export worked
- no external dev dependency
- package evidence pushed
- remote readback passed

## Final command

BUILD A COMPLETE EMPLOYEE-TRANSFERABLE WINDOWS PACKAGE. THE RECIPIENT MUST BE ABLE TO INSTALL AND RUN MINDLE MEDIA AI WITHOUT GITHUB, PYTHON, TOKENS, MODEL DOWNLOADS, OR DEVELOPER SETUP.
