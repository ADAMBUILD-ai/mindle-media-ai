# MINDLE MEDIA AI v30.0 Next Directive — Resume After Artifact Materialization

## Objective

Resume the v29.0 PC closeout only after parts 00, 01, and 02 exist as complete local files.

## Required handoff

1. Materialize the three GitHub Actions artifacts from run 35974551384 into `work/v29_0_transfer`.
2. Verify exact artifact sizes and digests:
   - part-00: 419251237 bytes, sha256:b930e521bb627f02134984ded6e7eb8ace20e15c2e56d9b9632c4759aaa62224
   - part-01: 418706393 bytes, sha256:8bc5a6df3759a48b50efce8c5984c65057ec57ea4270935a2c11359f5835b128
   - part-02: 78665503 bytes, sha256:c2ad3507f48c1b5ee54f1063af868ef85be3d2f19b689efdf3f2df6ec0272b4e
3. Reassemble/extract the verified package and inventory the exact model/runtime files.
4. Run local OpenVINO CPU health/load checks.
5. Execute PHOTO, UPSCALE, VIDEO tracking, and Korean STT locally on the recovered inputs.
6. Verify Preview, original/result compare, project save, export, and regression tests.
7. Publish v30 Evidence and review with actual local paths/hashes and only then claim PC_LOCAL_FINAL_E2E_PASS.

## Protection

UI_SSOT_CHANGED:NO. Do not repeat model shopping or remote packaging. Do not use GPU, paid compute, main merge, Production deployment, force push, credential exposure, or stale partial files. Preserve the v29 transfer-failure Evidence.
