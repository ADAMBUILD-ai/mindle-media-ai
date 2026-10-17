# MINDLE MEDIA AI — MARKETING LIVE SHORTFORM E2E FINAL COMPLETION DIRECTIVE v20.0

Date: 2026-10-01
Status: ACTIVE — FINAL LIVE SHORTFORM E2E
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261001-V20

## 0. Commander acceptance baseline

The following are FROZEN PASS and MUST NOT be reopened without regression evidence:

- v14 base product runtime TESTED_PASS
- v18.1 approved F27E visual UI TESTED_PASS
- v18.2 additive Shortform UI correction TESTED_PASS
- v19 base product final integrated closeout accepted
- PHOTO segmentation PASS
- PHOTO 4x PASS
- VIDEO tracking PASS
- Korean STT PASS
- Project Save / Export / Reopen PASS
- F27E UI SSOT hash:
  f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

This cycle exists ONLY because the Marketing AI live Shortform dependency has now been delivered.

## 1. Verified Marketing AI source

Repository:
ADAMBUILD-ai/mindle-marketing-department

PR:
#4 — P0: Add MINDLE ADA shortform bridge marketing pipeline

Head branch:
feature/shortform-bridge-p0-20260926

Verified head commit:
3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a

Verified workflow:
Shortform P0 Verification

Workflow run:
36852551111

Workflow result:
SUCCESS

Do not merge or modify Marketing PR #4 from MEDIA AI.
Use the exact Marketing branch/commit only as the live provider source.

## 2. Marketing handoff documents — authoritative for this cycle

Marketing repository exact files:

docs/handoff/MINDLE_MEDIA_TO_MARKETING_SHORTFORM_LIVE_E2E_CONNECTION_PACKAGE_20261001.md

docs/evidence/MINDLE_MARKETING_SHORTFORM_LIVE_BRIDGE_IMPLEMENTATION_INSPECTION_20261001.json

examples/shortform-live-e2e-approved-contract.json

Read these at exact Marketing commit:
3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a

## 3. Marketing live runtime

Same-device Local / Dev runtime:

Base URL:
http://127.0.0.1:4318

Start command in Marketing repository:
npm run start:shortform

Marketing ENV:

MARKETING_SHORTFORM_HOST=127.0.0.1
MARKETING_SHORTFORM_PORT=4318
MARKETING_SHORTFORM_ENV=local
MARKETING_SHORTFORM_BASE_URL=http://127.0.0.1:4318

Authentication ENV:
MARKETING_SHORTFORM_BRIDGE_TOKEN

IMPORTANT:
- do not print the token
- do not commit the token
- do not write the token into Evidence
- do not copy the token into chat/docs
- use existing secure environment injection only
- Marketing local server can disable auth when token is absent, but the Marketing handoff explicitly requires Token for MEDIA Live E2E
- therefore unauthenticated fallback does NOT count as final Live E2E PASS

If MARKETING_SHORTFORM_BRIDGE_TOKEN is absent:
RESULT = MARKETING_AUTH_ENV_REQUIRED
Continue every non-auth-dependent verification, but do not fake a full PASS.

## 4. Marketing endpoints

Health:
GET /v1/shortform/health
Authentication: not required

Create Contract:
POST /v1/shortform/contracts
Authentication: Bearer

Approved E2E Contract:
GET /v1/shortform/e2e/approved-contract
Authentication: Bearer

Approved Asset:
GET /v1/shortform/assets/{asset_id}
Authentication: Bearer

## 5. Approved deterministic E2E fixture

Campaign:
mindle-shortform-live-e2e-15

Expected:
- duration: 15 sec
- aspect_ratio: 9:16
- scenes: 5
- timeline: 0–3 / 3–6 / 6–11 / 11–13 / 13–15
- subtitles: 5
- voiceover text: 5
- BGM asset: e2e-bgm
- transitions: first cut, then soft_cut
- brand outro: e2e-brand-outro
- approval_state: handoff_ready
- representative_approval.decision: approve
- approval_scope: E2E_TEST_ONLY
- no external publishing
- no ad spend

## 6. Approved asset identity

Verify all six through actual HTTP GET and SHA-256.

1. e2e-source-image
SHA-256:
b2f326b40abf6f8c23e81167b5e2b37b06e1779d0ad6c8ee7f45a5046dc2f2d0

2. e2e-before
SHA-256:
32bde5320b67e57bda5aa3fc40d01870116c2765afe450635b66d6085fe19254

3. e2e-process
SHA-256:
98389d8ef5016d0055b30d2121f9ad27148bf23445e80a26ca48ce49e0edffa4

4. e2e-completed-result
SHA-256:
cf13533b552afcbc6727b4797b464a25544b13c1e72975b7f60374d9221cffcd

5. e2e-brand-outro
SHA-256:
3be617a919eb092c4bbd50da18f967a953375ad202c4e2cf8e202d6fe909e57a

6. e2e-bgm
SHA-256:
8b0443c1eab709804698901f190c095d036088bbd15f34d3c4ee95484a800498

Expected media:
- five SVG 1080 × 1920 frames
- one 15 sec WAV BGM

## 7. Current MEDIA AI implementation gap — MUST FIX

Current MEDIA AI product server still hardcodes:

POST /api/integrations/marketing/shortform
→ HTTP 503 VERIFY_REQUIRED

This is now obsolete because the Marketing live dependency is available.

Replace the stub with a real fail-closed Marketing HTTP client.

Required MEDIA ENV support:

MARKETING_SHORTFORM_BASE_URL
default for this local cycle:
http://127.0.0.1:4318

MARKETING_SHORTFORM_CONTRACT_PATH
default:
/v1/shortform/contracts

MARKETING_SHORTFORM_E2E_CONTRACT_PATH
default:
/v1/shortform/e2e/approved-contract

MARKETING_SHORTFORM_BRIDGE_TOKEN
secret, no default persisted in repo

Implementation requirements:
- stdlib HTTP client or existing dependency only
- explicit timeout
- Authorization Bearer when token present
- Accept: application/json
- Content-Type: application/json
- fail closed on 401/4xx/5xx
- no token logging
- no endpoint invention
- no hard-coded credential
- no silent unauthenticated fallback for final E2E

## 8. Request adapter

Existing MEDIA request builder produces:
- command
- project_id
- approval policy
- no publish
- no ad spend

Marketing POST requires:
- request_text
- product_or_project
- target
- campaign_goal
- duration
- platform
- available_assets
- brand_context
- evidence

Implement a narrow adapter.

Do not copy Marketing planning logic into MEDIA AI.

MEDIA may:
- map natural-language command into request_text
- use explicit/default test fixture fields only for v20 E2E
- keep allow_publish=false
- keep allow_ad_spend=false

For production behavior, missing product/target/campaign context must fail or request context; do not invent business claims.

## 9. Contract compatibility adapter

The approved Marketing Contract is not byte-for-byte identical to the current MEDIA shortform reader assumptions.

Known differences that MUST be handled explicitly:

Marketing:
- product_or_project
- resolved_assets
- scene field is scene_id
- platform = generic
- approval_state = handoff_ready
- representative_approval.decision = approve

Existing MEDIA reader currently assumes:
- product
- media_assets
- raw["id"] for scene identity
- platform in youtube_shorts / instagram_reels / tiktok / other
- approval_state in draft / preview_ready / representative_approved / exported

DO NOT mutate or overwrite the raw Marketing Contract.

Create a documented adapter/normalization layer that:
- preserves raw contract bytes/content for Evidence
- maps product_or_project into internal production identity without pretending MINDLE ADA is one of the seven products
- accepts Marketing resolved_assets as the approved asset source
- accepts scene_id
- supports generic platform semantics safely
- treats handoff_ready + representative_approval.decision=approve as the approved E2E handoff state for this E2E fixture
- does not authorize external publishing/ad spend
- does not reuse E2E_TEST_ONLY approval as real campaign approval

All mapping decisions must be tested.

## 10. Asset retrieval and integrity

Retrieve all six approved assets through the live Marketing HTTP server.

Requirements:
- Bearer auth for final E2E
- save exact bytes in v20 runtime staging
- verify expected SHA-256
- verify SVG dimensions/metadata where applicable
- verify WAV duration approximately 15 seconds
- reject any hash mismatch
- no replacement assets

## 11. Real Shortform rendering

Build the actual 15 sec 1080 × 1920 MP4 using the approved fixture.

Required visual sequence:
- scene 01: 0–3
- scene 02: 3–6
- scene 03: 6–11
- scene 04: 11–13
- scene 05: 13–15

Required:
- 9:16 output
- five approved visual assets
- subtitle text from Contract
- transition instructions
- approved BGM
- approved brand outro
- H.264 MP4 or current approved local video codec path
- no external publishing

Use existing local ffmpeg boundary where appropriate.
Do not introduce a new paid service.

## 12. Voiceover honesty gate

IMPORTANT:
The Marketing Contract includes five voiceover TEXT entries.
The delivered asset list contains five SVG files plus one WAV BGM.
It does NOT currently identify a voiceover audio asset.

MEDIA repository currently has no approved TTS model in the adopted model manifest.

Therefore:

1. inspect whether an already-approved existing local speech synthesis capability is present and documented in the current MEDIA product baseline
2. if YES, use only that approved capability and record its identity
3. if NO, DO NOT add or download a new TTS model silently
4. render subtitles/BGM/visuals as far as possible
5. status must explicitly record:
   VOICE_AUDIO_DEPENDENCY_VERIFY_REQUIRED

FULL_TESTED_PASS is forbidden unless audible voiceover is genuinely present and its production path is approved/evidenced.

Do not count voiceover text as voiceover audio.

## 13. Preview and approval

After rendering:
- expose the produced MP4 in the live MEDIA Preview
- verify it decodes
- verify dimensions
- verify duration
- verify video stream
- verify audio stream
- verify subtitle visibility
- verify brand outro
- record output SHA-256

Representative approval:
The Marketing E2E Contract already contains:
representative_approval.decision = approve

For E2E_TEST_ONLY this may authorize the test export after exact contract identity and asset integrity are verified.

Do not interpret this as approval for real publishing/ad spend.

## 14. MP4 export

Final export must be an actual MP4 file.

Record:
- filename
- bytes
- SHA-256
- duration
- width
- height
- video codec
- audio codec
- audio stream present YES/NO
- voiceover audio present YES/NO
- subtitle present YES/NO
- brand outro present YES/NO

Do not use the existing project ZIP export as a substitute for the requested Shortform MP4 evidence.

## 15. Regression protection

Run:
python scripts/validate_pc_work_control_plane.py

Expected:
CONTROL_PLANE_PASS

Run:
pytest -q

Run:
node --test ui/ssot_structure.test.js ui/interaction.test.js

Preserve:
- base MEDIA AI TESTED_PASS
- F27E UI TESTED_PASS
- v18.2 action order
- Save/Export/Reopen
- model identities
- screenshot-cheat PASS

## 16. Exact v20 Evidence paths

Human review:
docs/commander/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_REVIEW_v20.0_20261001.md

Machine Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_EVIDENCE_v20_0_20261001.json

Detail directory:
evidence/pc_remote/media-ai-marketing-live-shortform-v20-20261001/

Required files:
1. MANIFEST.json
2. CONTROL_PLANE_VALIDATION.txt
3. MARKETING_SOURCE_VERIFICATION.json
4. MARKETING_RUNTIME_HEALTH.json
5. MARKETING_AUTH_ENV_CHECK.json
6. APPROVED_CONTRACT_RAW.json
7. CONTRACT_COMPATIBILITY_ADAPTER.json
8. ASSET_HTTP_HASH_VERIFY.json
9. MEDIA_GATEWAY_LIVE_RESULT.json
10. SHORTFORM_RENDER_RESULT.json
11. VOICEOVER_DEPENDENCY_AUDIT.json
12. PREVIEW_VERIFY.json
13. MP4_EXPORT_VERIFY.json
14. REGRESSION_TEST_RESULTS.txt
15. OUTPUT_HASHES.sha256
16. REMOTE_PUSH_VERIFY.txt

All 16 files must exist remotely.

Do not store token values in any Evidence.

## 17. Allowed final results

### FULL_TESTED_PASS
Only if:
- Marketing live service health PASS
- authenticated approved Contract GET PASS
- all six asset HTTP/hash checks PASS
- MEDIA live gateway PASS
- Contract compatibility adapter PASS
- actual 15 sec 1080×1920 MP4 produced
- subtitles PASS
- BGM PASS
- transitions PASS
- brand outro PASS
- audible voiceover PASS through an approved existing capability
- Preview PASS
- MP4 export PASS
- regressions PASS
- remote Evidence PASS

### LIVE_E2E_PASS_VOICE_AUDIO_DEPENDENCY
Use if:
- Marketing live connection PASS
- Contract/assets PASS
- visuals/subtitles/BGM/transitions/brand outro MP4 PASS
- Preview/MP4 PASS
- only remaining gap is approved voiceover audio/TTS capability

### MARKETING_AUTH_ENV_REQUIRED
Use only if:
- exact Marketing service is reachable
- token is absent from secure environment
- no unauthenticated shortcut is used for final E2E

### FAIL
Use if:
- live Marketing connection/code is defective
- hash mismatch
- Contract adapter defect
- render defect
- regression
- Evidence incomplete

Base MEDIA AI remains frozen PASS unless a new reproducible base regression is found.

## 18. End-of-cycle response

RESULT:
Repository:
Branch:
Final HEAD:
Evidence commit:
Review path:
Evidence JSON path:
Detail directory:
Marketing commit:
Marketing workflow:
Marketing health:
Authenticated Contract GET:
Asset hash verify:
MEDIA gateway:
Contract adapter:
Render:
Preview:
MP4:
MP4 SHA-256:
Duration:
Resolution:
BGM:
Subtitles:
Transitions:
Brand outro:
Voiceover audio:
UI regression:
Python regression:
Base product preserved:
Remaining blocker:
REMOTE_PUSH_VERIFIED: YES

## Final governing sentence

THE MARKETING LIVE DEPENDENCY IS NOW AVAILABLE. REPLACE THE MEDIA 503 STUB WITH A REAL FAIL-CLOSED CONNECTION, VERIFY THE EXACT APPROVED CONTRACT AND ASSETS, PRODUCE A REAL 15-SECOND 9:16 MP4, AND REPORT VOICEOVER AUDIO TRUTHFULLY—NEVER COUNT TEXT AS AUDIO AND NEVER INTRODUCE AN UNAPPROVED TTS MODEL.
