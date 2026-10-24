# MINDLE MEDIA AI — EMPLOYEE PACKAGE FINAL CLOSEOUT R2 DIRECTIVE v1.0

Date: 2026-10-07
Status: ACTIVE — FINAL CLOSEOUT ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261007-EMPLOYEE-PACKAGE-FINAL-CLOSEOUT-R2

## 0. Current verified checkpoint

Do NOT restart from scratch. Reuse all already-passed work.

Frozen PASS / reuse:
- Windows sandbox ACL recovery PASS
- canonical local rebind PASS
- control plane PASS
- source regression suite: 56 PASS
- package runtime import under isolated temporary profile PASS
- Intel 4x actual CPU execution PASS
- Korean Whisper actual CPU execution PASS
- SAM PHOTO segmentation PASS
- SAM VIDEO tracking PASS
- UI VIDEO tracking/decoded preview observed
- UI PHOTO 1920x1080 upscale preview observed
- Save -> Close -> Reopen observed in copied install
- Export ZIP observed
- Shortform unavailable-path graceful continuation observed
- uninstall/reinstall temporary-profile PASS
- preserved data: 17/17 hashes matched
- extraction verification: 21,182 files
- candidate archive and 5 split parts were produced and reconstruction verified during the latest worker run

Do not invalidate these passes unless a later change touches the relevant component.

## 1. Current final blockers

Final result is NOT PASS.

Current blocker class:
RUNTIME_DEPENDENCY_LEAK

Known package-local missing native runtime files:
- msvcp140.dll
- msvcp140_atomic_wait.dll
- vcruntime140_threads.dll

Other remaining gates:
- actual default Windows profile install/write test
- desktop shortcut cold launch 2/2
- installed-package Korean STT
- installed-package PHOTO SAM
- final package self-containment audit
- final redistribution notices/license audit
- refresh stale Evidence files
- final package/split hashes after the last dependency fix
- final remote readback

## 2. Microsoft Visual C++ redistribution rule

Microsoft's official documentation states that redistribution of the Visual C++ Runtime Redistributable package, merge modules, or individual binaries is limited to licensed Visual Studio users and is subject to the applicable Microsoft Software License Terms.

Authoritative references:
- https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files
- https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist/
- https://visualstudio.microsoft.com/license-terms/

Therefore:
- DO NOT infer redistribution entitlement.
- DO NOT copy loose Microsoft runtime DLLs into the final package merely because they are Microsoft-signed.
- DO NOT claim OFFLINE_FULL_PACKAGE legal PASS until redistribution entitlement is supported by owner/license evidence.

## 3. VC runtime closure paths

### Path A — owner/license entitlement confirmed

If a qualifying Visual Studio redistribution entitlement is confirmed:

Preferred implementation:
1. Use the official, unmodified Microsoft x64 Visual C++ Redistributable package rather than manually copying loose DLLs.
2. Record:
   - source URL
   - file version
   - SHA-256
   - Authenticode status
   - publisher
   - applicable license reference
3. Bundle the unmodified redistributable into the installer package.
4. Installer must detect whether a sufficiently new v14 runtime already exists.
5. If missing/outdated, install the bundled official redistributable silently.
6. Re-run package self-containment and clean install E2E.

Do not package debug_nonredist binaries.

### Path B — redistribution entitlement NOT confirmed

Do not bundle Microsoft redistributable binaries.

Implement only a separate online-bootstrap fallback that downloads the official Microsoft x64 redistributable from:
https://aka.ms/vc14/vc_redist.x64.exe

Requirements:
- download only from Microsoft official permalink
- verify Microsoft Authenticode signature
- record SHA-256 and file version
- user-visible consent before prerequisite installation
- no third-party mirror
- no loose DLL copying

This path may be tested, but it MUST NOT be labeled:
EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS
for the requested complete offline package.

Use:
OFFLINE_FULL_PACKAGE_LICENSE_GATE_BLOCKED
until Path A entitlement is confirmed.

## 4. Default Windows profile host gate

The Work sandbox's refusal to grant default profile write access is NOT itself a product failure.

Create:
- scripts/FINAL_EMPLOYEE_PACKAGE_HOST_GATE.ps1
- scripts/FINAL_EMPLOYEE_PACKAGE_HOST_GATE.cmd

This host gate is designed to run in ordinary Windows PowerShell outside the Work sandbox.

It must perform, with no developer commands typed manually beyond launching the gate:

1. install to %LOCALAPPDATA%\MINDLE\MEDIA_AI
2. use %LOCALAPPDATA%\MINDLE\MEDIA_AI_DATA
3. create Start Menu shortcut
4. create Desktop shortcut
5. launch from Desktop shortcut — cold launch #1
6. close fully
7. launch from Desktop shortcut — cold launch #2
8. verify exactly one product server
9. verify package runtime identity = LOCAL_OFFLINE_PACKAGE
10. VIDEO import + tracking + decoded preview
11. Korean STT
12. PHOTO import + SAM segmentation
13. Intel 4x upscale
14. project save
15. close
16. reopen from Desktop shortcut
17. saved project restoration
18. export ZIP
19. Shortform unavailable-path graceful behavior
20. uninstall
21. verify application removed
22. verify user data preserved
23. reinstall
24. verify the 17 preserved files and hashes
25. verify no dependency on Git, system Python, pip, HF token, repo path, developer profile, or external model cache

Output:
- FINAL_HOST_GATE_RESULT.json
- FINAL_HOST_GATE_LOG.txt

Required:
DEFAULT_PROFILE_HOST_GATE_PASS

The host gate must be safe to rerun and must not delete user data.

## 5. Installed-package tests still required

Even though component tests already passed, the following must be run from the installed distribution package itself:

- Korean STT
- PHOTO SAM segmentation
- VIDEO SAM tracking
- Intel 4x
- Save/Reopen
- Export
- Shortform unavailable-path

Do not count source-tree or component-only tests as installed-package PASS.

## 6. Refresh stale Evidence

The following repository Evidence files are stale and MUST be rewritten from the final actual run:

- PACKAGE_BUILD_MANIFEST.json
- PACKAGE_SELF_CONTAINMENT_AUDIT.json
- DESKTOP_SHORTCUT_TEST.json
- INSTALLER_TEST.json
- SAVE_REOPEN_TEST.json
- EXPORT_TEST.json
- SHORTFORM_OFFLINE_BEHAVIOR.json
- UNINSTALL_REINSTALL_TEST.json
- PACKAGE_SHA256SUMS.txt
- SPLIT_PARTS_MANIFEST.json
- REMOTE_PUSH_VERIFY.txt

Do not leave NOT_RUN/BLOCKED placeholders after the actual test has passed.

## 7. Candidate archive rule

Previous candidate archive/hash is reference-only after any runtime dependency change.

After VC runtime closure:
- rebuild complete ZIP
- rebuild 300 MiB split parts
- reconstruct ZIP from split parts
- verify reconstructed SHA-256 equals final ZIP
- verify exact extracted file count
- verify package manifest
- verify final package has no missing native dependencies

No earlier archive hash may be reused as final after package contents change.

## 8. Redistribution notices audit

Before final PASS, generate/update:
- LICENSES/THIRD_PARTY_NOTICES.txt
- LICENSES/MODEL_LICENSE_MANIFEST.json
- LICENSES/RUNTIME_REDISTRIBUTION_MANIFEST.json

The runtime manifest must identify:
- Python
- PyTorch
- Torchvision
- Transformers
- OpenVINO
- NumPy
- OpenCV
- FFmpeg/ffprobe
- Visual C++ runtime handling
- all bundled redistributable native binaries/installers

For each:
- origin
- version
- license/notice source
- bundled/not bundled
- redistribution basis
- SHA-256 where applicable

## 9. Final output paths

Final package:
dist/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip

Split package:
dist/transfer_parts/

Final Review:
docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_REVIEW_v1.0_20261007.md

Final Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_EVIDENCE_v1_0_20261007.json

Detail:
evidence/pc_remote/media-ai-employee-package-final-closeout-r2-v1_0-20261007/

## 10. Final result vocabulary

PASS only when ALL required gates pass:
EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS

If only Microsoft redistribution entitlement remains:
OFFLINE_FULL_PACKAGE_LICENSE_GATE_BLOCKED

If package still depends on machine-installed Visual C++ runtime:
RUNTIME_DEPENDENCY_LEAK

If default-profile host gate has not been run:
DEFAULT_PROFILE_HOST_GATE_PENDING

If any installed-package function fails:
CLEAN_WINDOWS_TEST_FAILED

## 11. Remote publication

After final evidence generation:
- commit to canonical branch
- no force push
- no main merge
- remote readback every final Review/Evidence/manifest
- record final commit SHA
- record final ZIP SHA-256
- record split part SHA-256 values

## Final command

DO NOT REBUILD ALREADY-PASSED WORK FROM SCRATCH.
CLOSE ONLY THE REMAINING DISTRIBUTION GATES:
VISUAL C++ RUNTIME ENTITLEMENT/DEPLOYMENT,
DEFAULT WINDOWS PROFILE HOST GATE,
INSTALLED-PACKAGE FUNCTION RETEST,
FINAL SELF-CONTAINMENT,
LICENSE/NOTICE AUDIT,
FINAL ZIP/SPLIT HASHES,
REMOTE READBACK.
