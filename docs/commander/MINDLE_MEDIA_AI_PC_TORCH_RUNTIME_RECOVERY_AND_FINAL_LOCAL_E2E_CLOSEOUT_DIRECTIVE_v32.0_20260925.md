# MINDLE MEDIA AI — PC TORCH RUNTIME RECOVERY & FINAL LOCAL E2E CLOSEOUT DIRECTIVE v32.0
Date: 2026-09-25
Status: REWORK — EXECUTE ONLY REMAINING LOCAL GATES
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: work/v28-1-remote-runtime-package-20260924

## Commander verification
The latest v30 Evidence is accepted as the authoritative state. The older v31 transfer-incomplete narrative is superseded where it conflicts with v30.

FREEZE AS PASS — DO NOT REDO:
- Remote runtime packaging / exact model verification / license / canonical.
- Approved remote UI Product E2E FINAL_PASS.
- PC materialization of SAM 2.1, whisper-small, Intel SISR and Windows OpenVINO CPU.
- PC PHOTO segmentation quality PASS: intended person selected at [125,145].
- PC Intel SISR 4x quality PASS: 1920x1080, non-black, SHA-256 4806a7ab40db3cf8dabec2451ee58015c70e662834643389ae8b6d4684c9d35f.
- UI_SSOT_CHANGED:NO.

REWORK ONLY:
1. Fresh PC Python process terminates during import torch after numpy-loaded.
2. VIDEO tracking local CPU rerun.
3. Korean STT local CPU rerun.
4. Latest approved-UI local Preview -> Save -> Export replay.
5. Final local regression/closeout.

## 1. Diagnose torch import crash — bounded, evidence-driven
Do not reinstall everything blindly and do not rerun already-PASS model acquisition.
Capture:
- exact python executable/version/architecture
- torch version/build and installation path
- Windows exit code / Event Viewer or process error where accessible
- VC runtime / DLL dependency state
- CPU instruction compatibility
- PATH/DLL search conflicts
- whether the previously successful PHOTO process used the same interpreter/environment
Run minimal probes in isolated order: python only -> numpy -> torch.
If current environment is corrupted, create a clean project-local CPU venv from the already verified/approved package sources and install only the pinned compatible dependencies required by SAM/Whisper. Preserve the working OpenVINO environment separately if safer.
Do not spend more than 10 minutes without measurable progress on one approach; after that switch to the next permitted route.

## 2. Recovery routes — mandatory sequence
A. Repair current project-local Python/torch environment from existing verified local caches/packages.
B. Reuse the exact interpreter/environment that successfully executed the PC PHOTO SAM run, if identifiable.
C. Build a clean CPU-only project venv from approved cached/offline packages.
D. If local torch binaries remain broken, package the exact compatible CPU torch/runtime remotely through the already-proven GitHub Artifact transfer route, then materialize and verify it locally.
E. Only if A-D fail, use official CPU-only PyTorch distribution/package via an approved outbound-capable remote environment and transfer it as an artifact.
Do not stop at “torch import failed”.

## 3. VIDEO local tracking
Recovered source video is already valid: 125 frames / 24 fps / 672x384.
Once torch/SAM is healthy:
- run actual local SAM tracking;
- use OpenCV path if sufficient; ffmpeg absence alone is not a blocker;
- verify continuity and decodability;
- produce actual local output hash;
- Preview -> project save -> export.
Quality FAIL => correct adapter/runtime and rerun VIDEO only.

## 4. Korean STT local execution
Recovered Korean WAV is already valid: 16 kHz / 12.48 s.
Once torch/whisper-small is healthy:
- run actual local STT;
- record transcript and output hash;
- compare for obvious Korean recognition errors against preserved reference evidence;
- Preview -> project save/export.
Quality FAIL => correct adapter/runtime and rerun STT only.

## 5. Approved UI local replay
Using latest approved UI and actual LOCAL outputs:
PHOTO PASS output + UPSCALE PASS output + new VIDEO output + new STT transcript.
Verify actual Preview, project save and export.
Remote UI E2E is preserved as PASS but cannot substitute for this local replay.

## 6. Regression
Run Python/UI/server/evidence/package regressions after torch recovery and local E2E.
Do not reopen frozen PHOTO/UPSCALE quality work unless regression proves breakage.

## 7. Final Evidence
Create:
- docs/commander/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_REVIEW_v32.0_20260925.md
- evidence/pc_remote/MINDLE_MEDIA_AI_PC_TORCH_RECOVERY_FINAL_LOCAL_E2E_EVIDENCE_v32_20260925.json
Include torch crash root cause, recovery route, interpreter/runtime identity, VIDEO/STT input/output hashes and quality, local UI Preview/save/export, regressions, changed files, commit/PR/Actions.

## 8. Final Gate
Declare:
PC_LOCAL_FINAL_E2E_PASS: PASS
MINDLE_MEDIA_AI_PC_FINAL_QUALITY_CLOSEOUT: PASS
only when VIDEO + Korean STT + local Preview/save/export + regression pass while frozen PHOTO/UPSCALE remain valid.

## 9. Automatic next directive
Immediately after verification, inspect actual Evidence and commit the next directive under docs/commander. Do not wait for user instruction.

## Protection
No UI redesign, main merge, Production deploy, force push, GPU, paid compute, credential exposure, legacy fallback, or prior Evidence overwrite.
