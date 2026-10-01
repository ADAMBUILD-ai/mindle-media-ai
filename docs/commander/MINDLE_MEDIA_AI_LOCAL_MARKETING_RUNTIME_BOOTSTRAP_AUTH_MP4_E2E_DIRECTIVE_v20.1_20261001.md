# MINDLE MEDIA AI — LOCAL MARKETING RUNTIME BOOTSTRAP + AUTHENTICATED SHORTFORM MP4 E2E DIRECTIVE v20.1

Date: 2026-10-01
Status: ACTIVE — RESUME FINAL LIVE E2E
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20.1

## 0. Commander review of v20

v20 result is ACCEPTED as:
MARKETING_AUTH_ENV_REQUIRED

Accepted PASS:
- MEDIA 503 stub removed
- fail-closed Marketing HTTP client implemented
- request adapter implemented
- Marketing contract compatibility adapter implemented
- no credential logging/hardcoding
- Python regression: 52 PASS
- UI regression: 2 PASS
- v14/v18.1/v18.2/v19 frozen PASS preserved
- exact v20 Evidence 16/16 published
- remote readback verified

Remaining blockers proven by v20:
1. Marketing local provider at 127.0.0.1:4318 was not running
2. MARKETING_SHORTFORM_BRIDGE_TOKEN was absent
3. local ffmpeg was not available
4. no approved voiceover audio/TTS capability exists yet

Do NOT rework already-PASS gateway/adapter code unless live execution reveals a reproducible defect.

## 1. Purpose

Complete the live E2E on the SAME Windows PC without requiring the representative to manually provide a token.

Sequence:
Marketing exact checkout
→ ephemeral in-memory E2E token
→ start Marketing runtime
→ health PASS
→ authenticated approved Contract GET
→ six asset HTTP/hash PASS
→ ffmpeg ready
→ MEDIA live gateway PASS
→ real 15 sec 1080×1920 MP4
→ Preview
→ MP4 Export
→ truthful voiceover result
→ Evidence

## 2. Exact Marketing source

Repository:
ADAMBUILD-ai/mindle-marketing-department

Branch:
feature/shortform-bridge-p0-20260926

Commit:
3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a

PR:
#4

Workflow:
36852551111 SUCCESS

Do not modify Marketing source.

## 3. Local Marketing checkout

First search only known development roots for an existing:
mindle-marketing-department

If exact checkout exists:
- git fetch origin
- checkout feature/shortform-bridge-p0-20260926
- verify HEAD = 3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a
- do not alter source

If absent:
- clone/fetch the exact private repository using the PC's EXISTING Git credential/session
- no browser auth loop
- no token printed
- one authenticated attempt only
- checkout exact branch/commit

If repository cannot be obtained with existing credentials:
RESULT = MARKETING_SOURCE_CHECKOUT_BLOCKED
Record exact failure and stop only live-provider work; base MEDIA PASS stays frozen.

## 4. Ephemeral local E2E authentication — NO USER ACTION REQUIRED

The Marketing runtime accepts its Bearer secret from:
MARKETING_SHORTFORM_BRIDGE_TOKEN

For E2E_TEST_ONLY, generate a cryptographically random ephemeral token locally in memory.

Requirements:
- at least 256 bits random
- set it in the parent PowerShell/process environment
- launch BOTH Marketing runtime and MEDIA runtime from child processes inheriting that environment
- never echo/token-print it
- never write it to disk
- never commit it
- never include it in Evidence
- Evidence records only:
  token_present = true
  token_length_class >= 32 bytes
  token_persisted = false
  token_logged = false

This is an E2E_TEST_ONLY local secret, not a production credential.

Do not ask the representative to supply a token.

## 5. Start Marketing live provider

Set:
MARKETING_SHORTFORM_HOST=127.0.0.1
MARKETING_SHORTFORM_PORT=4318
MARKETING_SHORTFORM_ENV=local
MARKETING_SHORTFORM_BASE_URL=http://127.0.0.1:4318
MARKETING_SHORTFORM_BRIDGE_TOKEN=<ephemeral in-memory value>

From exact Marketing checkout:
npm run start:shortform

Keep the process alive.

Poll:
GET http://127.0.0.1:4318/v1/shortform/health

Expected:
HTTP 200
status = READY
service = MINDLE_MARKETING_SHORTFORM_BRIDGE
contract_version = 1.0

Do not continue to Contract retrieval until health PASS.

## 6. Authenticated Contract and assets

With the same ephemeral token:

GET:
/v1/shortform/e2e/approved-contract

Expected:
HTTP 200
status = handoff_ready

Save the raw response/contract exactly.

Then retrieve all six assets with Bearer auth:
- e2e-source-image
- e2e-before
- e2e-process
- e2e-completed-result
- e2e-brand-outro
- e2e-bgm

Verify expected SHA-256 values from v20 directive.

Any mismatch = FAIL.
No substitution.

## 7. ffmpeg runtime recovery

v20 proved ffmpeg was not available.

Before rendering:
1. search known approved local runtime locations / prior MEDIA or AVORA staging for ffmpeg.exe and ffprobe.exe
2. if exact local ffmpeg is found, record version/path/hash and use it
3. if absent, install/expose a free local ffmpeg runtime through the machine's existing approved package-management route
4. no paid service
5. no GPU requirement
6. record installation/source/version/path
7. verify:
   ffmpeg -version
   ffprobe -version

Do not finish with "ffmpeg absent" without attempting the permitted local recovery.

If installation/recovery itself is impossible:
RESULT = FFMPEG_RUNTIME_BLOCKED

## 8. MEDIA runtime environment

Set:
MARKETING_SHORTFORM_BASE_URL=http://127.0.0.1:4318
MARKETING_SHORTFORM_CONTRACT_PATH=/v1/shortform/contracts
MARKETING_SHORTFORM_E2E_CONTRACT_PATH=/v1/shortform/e2e/approved-contract
MARKETING_SHORTFORM_BRIDGE_TOKEN=<same inherited ephemeral token>

Launch canonical MEDIA product server from current worktree.

Do not expose the token in command logs/Evidence.

## 9. MEDIA live gateway

Exercise the actual MEDIA route:
POST /api/integrations/marketing/shortform

Use explicit E2E context:
- product_or_project = MINDLE ADA
- target = architects
- campaign_goal = brand_awareness
- duration = 15
- platform = generic
- publish disabled
- ad spend disabled

Expected:
- no 503 stub
- Marketing live HTTP request occurs
- valid contract result returned
- fail-closed behavior preserved

Record request fields excluding secrets and response identity.

## 10. Approved Contract compatibility

Use the existing v20 normalization layer.

Verify actual raw Marketing Contract against normalized internal plan:
- raw preserved unchanged
- product_or_project retained in raw Evidence
- internal product identity = MARKETING_EXTERNAL
- resolved_assets mapped to approved asset set
- scene_id mapped safely
- generic mapped to internal other
- handoff_ready + representative approve mapped to E2E representative_approved
- E2E_TEST_ONLY cannot authorize publication/ad spend

Run actual normalized reader on the live Contract.
Not static-only.

## 11. Real MP4 renderer

If no renderer exists, implement the minimum product-owned shortform renderer inside MEDIA AI.

Input:
- live approved Contract
- live verified six assets
- ffmpeg runtime

Output:
- 1080×1920
- approximately 15 sec
- H.264 MP4
- five scene timing windows
- subtitles burned into video
- BGM audio
- cut / soft_cut transitions where technically supported by approved local path
- brand outro in final scene
- no external publishing

SVG source handling:
- use ffmpeg SVG decode if supported
- otherwise use an already-available local rendering route
- if a conversion dependency is required, use only free local tooling and record it
- do not replace the approved SVGs with other imagery

## 12. Voiceover gate

The Contract supplies voiceover TEXT only.
The delivered WAV is BGM, not narration.

Current approved MEDIA model manifest contains no TTS model.

Therefore:
- do not silently install a TTS model
- do not synthesize narration with an unapproved online service
- do not claim voiceover PASS from text alone

If an already-approved local voice synthesis capability is documented and available, record it and use it.

Otherwise:
Voiceover audio = VERIFY_REQUIRED

This does NOT block producing the real visual/subtitle/BGM MP4.

Expected likely cycle result:
LIVE_E2E_PASS_VOICE_AUDIO_DEPENDENCY

## 13. Preview and MP4 verification

The produced MP4 must be loaded in MEDIA Preview and validated.

Record:
- actual filename
- bytes
- SHA-256
- duration
- 1080×1920
- video codec
- audio codec
- audio stream present
- BGM audible/present
- subtitles visible
- transitions present
- brand outro present
- voiceover audio present/absent

Actual MP4 file must be preserved in Evidence:
evidence/pc_remote/media-ai-marketing-live-shortform-v20_1-20261001/SHORTFORM_FINAL_15S_9X16.mp4

No ZIP substitution.

## 14. Regression

Run:
python scripts/validate_pc_work_control_plane.py

Expected:
CONTROL_PLANE_PASS

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Base product/UI/model PASS remains frozen unless a reproducible regression appears.

## 15. Exact v20.1 Evidence

Human Review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_REVIEW_v20.1_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_EVIDENCE_v20_1_20261001.json

Detail:
evidence/pc_remote/media-ai-marketing-live-shortform-v20_1-20261001/

Required files:
1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. MARKETING_LOCAL_CHECKOUT.json
4. EPHEMERAL_TOKEN_BOOTSTRAP.json
5. MARKETING_RUNTIME_HEALTH.json
6. AUTHENTICATED_CONTRACT_GET.json
7. APPROVED_CONTRACT_RAW.json
8. ASSET_HTTP_HASH_VERIFY.json
9. FFMPEG_RUNTIME_RECOVERY.json
10. MEDIA_GATEWAY_LIVE_RESULT.json
11. SHORTFORM_RENDER_RESULT.json
12. VOICEOVER_DEPENDENCY_AUDIT.json
13. PREVIEW_VERIFY.json
14. MP4_EXPORT_VERIFY.json
15. SHORTFORM_FINAL_15S_9X16.mp4
16. REGRESSION_TEST_RESULTS.txt
17. OUTPUT_HASHES.sha256
18. REMOTE_PUSH_VERIFY.txt

All 18 required files must exist remotely.
MP4 must be non-zero and decodable.
No secret may appear in any Evidence.

## 16. Allowed results

FULL_TESTED_PASS:
Only if audible approved voiceover also exists and passes.

LIVE_E2E_PASS_VOICE_AUDIO_DEPENDENCY:
- Marketing health PASS
- auth PASS
- Contract PASS
- six asset hashes PASS
- MEDIA gateway PASS
- Contract adapter live PASS
- actual MP4 PASS
- Preview PASS
- subtitles/BGM/transitions/brand outro PASS
- only voiceover audio remains VERIFY_REQUIRED

MARKETING_SOURCE_CHECKOUT_BLOCKED:
Only if exact private Marketing source cannot be checked out with existing credentials.

FFMPEG_RUNTIME_BLOCKED:
Only after permitted recovery/install was attempted and proven impossible.

FAIL:
Actual code/render/hash/regression/Evidence defect.

## 17. Final response

RESULT:
Marketing checkout:
Marketing HEAD:
Ephemeral auth:
Marketing health:
Authenticated Contract:
Asset 6/6:
ffmpeg:
MEDIA gateway:
Contract adapter:
MP4:
MP4 bytes:
MP4 SHA-256:
Duration:
Resolution:
Video codec:
Audio codec:
BGM:
Subtitles:
Transitions:
Brand outro:
Voiceover audio:
Preview:
Python:
UI:
Base product preserved:
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

DO NOT ASK THE REPRESENTATIVE FOR A TOKEN. CREATE A LOCAL EPHEMERAL E2E SECRET IN MEMORY, START BOTH VERIFIED LOCAL SERVICES WITH IT, RECOVER FFMPEG, RETRIEVE THE EXACT CONTRACT/ASSETS, AND PRODUCE THE REAL MP4. REPORT VOICEOVER AUDIO SEPARATELY AND TRUTHFULLY.
