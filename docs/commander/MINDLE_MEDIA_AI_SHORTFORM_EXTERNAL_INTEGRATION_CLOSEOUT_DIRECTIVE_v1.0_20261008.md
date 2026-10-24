# MINDLE MEDIA AI — SHORTFORM EXTERNAL INTEGRATION CLOSEOUT DIRECTIVE v1.0

Date: 2026-10-08
Status: ACTIVE — EXTERNAL SHORTFORM INTEGRATION CLOSEOUT ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261008-SHORTFORM-EXTERNAL-INTEGRATION-CLOSEOUT-R1

## 0. VERIFIED STARTING POINT

Do NOT rerun already-passed base product work unless an integration change touches it.

Frozen PASS:
- PHOTO segment and 4x upscale
- VIDEO tracking backend
- mp4v browser failure root cause captured with MediaError.code=4
- H.264 / yuv420p / faststart browser preview
- actual VIDEO playback in browser
- Korean STT backend + UI visibility
- Save / full close / Reopen restoration
- base product Export with download SHA and ZIP CRC
- Python 66 PASS / UI 2 PASS on product runner
- Control Plane PASS
- main unchanged
- PR #23 HOLD / DO NOT MERGE
- approved UI layout/colors unchanged

Current result:
BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION

Only remaining full-product gates:
- actual Marketing HTTP provider reachability
- actual bridge authentication
- approved AVORA asset
- 9:16 Shortform Preview
- Representative Approval gate
- approved MP4 Export
- final Evidence/readback

## 1. REQUIRED EXTERNAL CONNECTION INPUT

The Marketing integration owner must provide the runtime through environment configuration, not through chat or committed plaintext secrets.

Required:
- MARKETING_SHORTFORM_BASE_URL: actual URL reachable from the GitHub Actions/product E2E runner
- MARKETING_SHORTFORM_BRIDGE_TOKEN: GitHub Actions secret; never commit or print the token
- actual SHORTFORM BRIDGE Contract endpoint/path and HTTP method if not already encoded in current implementation
- approved AVORA asset/reference with stable identifier, origin, SHA-256 where applicable, and approval provenance
- representative-approval test path/state required before MP4 export

If the provider is localhost:
- the actual provider must be started in the same runner/job/service network before E2E begins
- do not point to 127.0.0.1 unless a real provider process is actually listening there

No mock server, stub, historical response, or fabricated approval may be counted as PASS.

## 2. EXECUTION ORDER

Execute only this chain:

1. validate MARKETING_SHORTFORM_BASE_URL is configured
2. verify provider health/reachability from the actual E2E runner
3. verify MARKETING_SHORTFORM_BRIDGE_TOKEN is present without printing it
4. make the real Marketing HTTP request
5. validate real response against the existing SHORTFORM BRIDGE Contract
6. ingest the approved AVORA asset/reference
7. verify 9:16 scene/timeline transformation
8. load and actually play the Shortform Preview in the browser
9. exercise Representative Approval gate
10. export the approved advertisement MP4
11. ffprobe the exported MP4 and record SHA-256
12. publish Review/Evidence and remote readback

Do not restart PHOTO/VIDEO/STT/Save/Reopen/Export base gates unless the Shortform change touches them.

## 3. REAL MARKETING HTTP GATE

PASS requires:
- actual non-mock provider
- network connection succeeds from the E2E runner
- request method/path/headers recorded with secret values redacted
- request body hash or stable receipt recorded
- HTTP success code recorded
- response schema/contract validated
- response correlation/job ID recorded
- no credential material written to Evidence

If unreachable:
BLOCKED_MARKETING_PROVIDER_UNREACHABLE

If token is absent:
BLOCKED_MARKETING_BRIDGE_TOKEN_MISSING

## 4. AVORA GATE

PASS requires an actually approved AVORA asset/reference.

Evidence:
- stable asset/reference identifier
- source/origin
- approval status/provenance
- SHA-256 for downloaded/local immutable artifact where applicable
- exact use in the Shortform request/scene

Do not substitute arbitrary media.

If unavailable:
BLOCKED_APPROVED_AVORA_ASSET_MISSING

## 5. SHORTFORM PREVIEW GATE

The product must create the actual 9:16 Shortform result and display it in the approved MINDLE MEDIA AI UI.

Browser Evidence:
- operation/job ID
- currentSrc
- readyState
- videoWidth/videoHeight
- MediaError
- actual playback start
- duration
- HTTP status / Content-Type
- preview SHA-256
- screenshot after successful decode

Required aspect:
9:16

## 6. REPRESENTATIVE APPROVAL GATE

Before final advertisement MP4 export:
- prove unapproved state blocks final export
- perform the approved representative-approval action/path
- record approval identifier/state/timestamp or stable receipt
- then prove export becomes available

Do not auto-approve in test code.

## 7. FINAL MP4 EXPORT GATE

PASS requires actual approved MP4 export.

Record:
- file name/path
- bytes
- SHA-256
- ffprobe codec/container/pix_fmt/width/height/duration
- 9:16 geometry
- browser/download receipt where applicable
- linkage to Marketing response + AVORA asset + approval receipt

No automatic publishing or ad-spend execution.

## 8. REGRESSION

After Shortform integration changes:
- Python baseline must remain >=66 PASS on the product runner unless the test count legitimately increases
- UI baseline >=2 PASS
- base VIDEO H.264 playback smoke PASS
- Korean STT smoke PASS
- Save/Reopen smoke PASS
- base Export smoke PASS
- pip check PASS
- Control Plane PASS

Do not re-run expensive PHOTO models unless touched by the change.

## 9. REQUIRED EVIDENCE

Review:
docs/commander/MINDLE_MEDIA_AI_SHORTFORM_EXTERNAL_INTEGRATION_CLOSEOUT_REVIEW_v1.0_20261008.md

Machine Evidence:
docs/evidence/media-ai-shortform-external-integration-closeout-20261008/EVIDENCE.json

Evidence root:
docs/evidence/media-ai-shortform-external-integration-closeout-20261008/

Required:
- PROVIDER_REACHABILITY.json
- MARKETING_HTTP_RESULT.json
- AVORA_APPROVED_ASSET_RESULT.json
- SHORTFORM_9X16_BROWSER_PREVIEW.json
- REPRESENTATIVE_APPROVAL_RESULT.json
- APPROVED_MP4_EXPORT_RESULT.json
- REGRESSION_RESULT.json
- REMOTE_READBACK.txt

## 10. FINAL RESULT

Only when every real external gate passes:
PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED

If the environment still lacks the required real provider/token/asset:
BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION

Full product PASS remains forbidden until real external Evidence exists.

## 11. REPOSITORY RULES

- canonical branch only
- no main/default merge
- no force push
- no new repo/worktree/branch
- PR #23 remains HOLD / DO NOT MERGE
- approved UI visual/layout unchanged
- employee package rebuild remains blocked until full product PASS
- no secret/token plaintext in repository or logs
- no historical Evidence deletion

## FINAL COMMAND

CLOSE ONLY THE REAL MARKETING / AVORA / SHORTFORM EXTERNAL GATES.
DO NOT REOPEN PASSED BASE PRODUCT WORK.
DO NOT USE MOCKS AS PASS.
DO NOT ASK THE OWNER TO COPY TOKENS THROUGH CHAT.
CONFIGURE THE RUNNER/REPOSITORY ENVIRONMENT SECURELY, RUN THE REAL E2E, PUBLISH EVIDENCE, AND READ IT BACK.
