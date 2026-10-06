# MINDLE MEDIA AI — CURRENT PC WORK ACTIVE DIRECTIVE

STATUS: ACTIVE
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-EMPLOYEE-PACKAGE-V1.0
DATE: 2026-10-06
REPOSITORY: ADAMBUILD-ai/mindle-media-ai
BRANCH: feature/ad-shortform-bridge-p0-20260926

## ACTIVE DIRECTIVE
docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_FULL_WINDOWS_PACKAGE_DIRECTIVE_v1.0_20261006.md

## ACTIVE EVIDENCE CONTRACT
docs/commander/MINDLE_MEDIA_AI_PC_WORK_EVIDENCE_PATH_CONTRACT_EMPLOYEE_PACKAGE_v1.0_20261006.json

## PURPOSE
Build and validate a complete employee-transferable Windows x64 distribution package.

## PRODUCT REQUIREMENT
The employee must be able to install and run MINDLE MEDIA AI without GitHub, git, system Python, pip, HF_TOKEN, model downloads, or developer setup.

## REQUIRED OUTPUTS
Review:
docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_REVIEW_v1.0_20261006.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_EVIDENCE_v1_0_20261006.json

Detail:
evidence/pc_remote/media-ai-employee-package-v1_0-20261006/

Distribution:
dist/MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip
dist/transfer_parts/

## EXECUTION ORDER
1. Read CURRENT_WORKER_COORDINATION_LOCK.json
2. Confirm Worker A / product-runtime lane
3. Validate control plane
4. Capture actual proven Windows runtime versions
5. Build package-local Python/runtime environment
6. Bundle adopted model snapshots and verify hashes
7. Bundle ffmpeg/ffprobe
8. Implement LOCAL_OFFLINE_PACKAGE runtime mode with no HF_TOKEN
9. Build installer/uninstaller and branded shortcuts
10. Build full ZIP
11. Build 300 MiB transfer parts + reassembly installer
12. Test install from package only, without repo/system Python/Git/HF token
13. Run PHOTO/VIDEO/STT/upscale/save/reopen/export E2E
14. Test Shortform unavailable-path gracefully
15. Uninstall/reinstall test
16. Publish evidence, commit, push, remote-readback

## HARD RULES
- no secrets in package
- no silent model substitution
- no dependency on Git checkout
- no dependency on developer profile
- no metadata-only PASS
- no package PASS until clean-package E2E passes

## FINAL PASS
EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS
