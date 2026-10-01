# MINDLE MEDIA AI — PC NEXT EXECUTION DIRECTIVE v21.0

Date: 2026-09-24
Status: WAIT_FOR_TRUE_MANUAL_INPUT
Base: v20.1 execution review and evidence

## Verdict

v20.1 executed the available non-sensitive checks. The remaining gate is genuinely manual and must not be simulated.

## Required user actions

1. Use the approved secure local credential UI to expose the existing scoped HF credential to the PC-local process. Do not paste it into chat, terminal history, source, logs, PR, or Evidence.
2. Select one owned/approved moving-subject video through the local file picker.
3. Select or record one owned/approved spoken-Korean audio sample through the local file picker.

## Next execution

After those actions, immediately:
- verify only the boolean authentication result;
- materialize and hash-verify SAM 2.1, whisper-small, and Intel SISR adopted caches;
- install/expose only free local dependencies required by the runtime;
- run PHOTO, UPSCALE, VIDEO, and Korean STT through the approved UI/runtime;
- validate real output hashes, dimensions/continuity, transcript, Preview, save, export, and quality;
- run Python/UI/server/evidence regressions;
- record PASS/REWORK and create the next directive.

## Protection

UI_SSOT_CHANGED:NO. No UI redesign, main merge, Production deploy, force push, GPU, paid compute, legacy fallback, secret exposure, or prior Evidence overwrite.
