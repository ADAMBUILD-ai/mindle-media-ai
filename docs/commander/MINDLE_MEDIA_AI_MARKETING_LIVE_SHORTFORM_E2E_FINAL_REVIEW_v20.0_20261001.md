# MINDLE MEDIA AI v20 Marketing Live Shortform E2E Review

## Result

**MARKETING_AUTH_ENV_REQUIRED**

- Repository: `ADAMBUILD-ai/mindle-media-ai`
- Branch: `feature/ad-shortform-bridge-p0-20260926`
- Code head under test: `46ce1f510959565424565de012acc13c7d4ed872`
- Marketing source: `mindle-marketing-department`, commit `3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a`, workflow `36852551111 SUCCESS`

## Work completed

The MEDIA 503 shortform stub was replaced with a stdlib HTTP client using the exact configured Marketing base URL/path, explicit timeout, `Accept: application/json`, JSON content type, and Bearer authentication when the secure token is present. Missing token returns `MARKETING_AUTH_ENV_REQUIRED`; provider failures are fail-closed. No token is logged or persisted.

A narrow request adapter and Marketing-contract normalization layer were added and statically tested. The raw Marketing identity is preserved as external; `resolved_assets`, `scene_id`, generic platform, and `handoff_ready + approve` are mapped explicitly without copying Marketing planning logic into MEDIA AI.

## Live verification

The configured provider `http://127.0.0.1:4318` refused connection. `MARKETING_SHORTFORM_BRIDGE_TOKEN` was absent from the secure environment. Therefore the approved Contract and six assets could not be retrieved, and no fake fixture or replacement asset was used.

The MEDIA gateway was exercised with explicit context and returned HTTP 503 `MARKETING_AUTH_ENV_REQUIRED`. Python regression passed 52 tests and UI regression passed 2 tests. Base MEDIA AI, F27E UI, v18.2 action identity/order, and v19 closeout remain frozen PASS.

No MP4 is claimed. Render, Preview, MP4 export, asset hash, and audible voiceover gates remain VERIFY_REQUIRED until the verified Marketing runtime and token are present. This is an authentication/provider availability blocker, not a base-product failure.

## Evidence

- Machine: `evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_E2E_FINAL_EVIDENCE_v20_0_20261001.json`
- Detail directory: `evidence/pc_remote/media-ai-marketing-live-shortform-v20-20261001/`
- Required detail files: 16
