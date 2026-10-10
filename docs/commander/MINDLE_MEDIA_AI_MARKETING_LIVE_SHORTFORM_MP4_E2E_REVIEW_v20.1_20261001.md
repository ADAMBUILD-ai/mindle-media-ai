# MINDLE MEDIA AI Marketing Live Shortform MP4 E2E Review v20.1

## Result

`LIVE_E2E_PASS_VOICE_AUDIO_DEPENDENCY`

The live Marketing runtime was checked out at the required commit, started with an ephemeral in-memory 256-bit bearer token, and reached `READY`. The authenticated approved contract was fetched from the live endpoint. All six approved assets returned HTTP 200 and matched their required SHA-256 hashes.

The MEDIA AI live gateway accepted the Marketing request and returned `bridge_contract_ready`. The real five-scene contract was normalized, subtitles were rendered, approved SVG source assets were rasterized locally without changing their source evidence hashes, and ffmpeg produced a 15-second 1080x1920 H.264/AAC MP4 with BGM, transitions, and the approved brand outro.

Voiceover remains an explicit dependency: the contract requests voiceover, but no approved TTS runtime was available, so no false voiceover PASS is claimed. BGM audio is present in the exported MP4.

## Verification

- Marketing checkout: `feature/shortform-bridge-p0-20260926` at `3921a4ac7f0ed13edcb1dcb4556286cbaa83c57a`
- Marketing health: `GET /v1/shortform/health` → HTTP 200 `READY`
- Approved contract: authenticated `GET /v1/shortform/e2e/approved-contract` → PASS
- Assets: 6/6 HTTP 200 and SHA-256 match
- MEDIA route: `POST /api/integrations/marketing/shortform` → HTTP 200 `bridge_contract_ready`
- Export: 172725 bytes, SHA-256 `641fc1323667168eb293cac8b3ec1a5d07c4d3a8d4818fa363dcb537e0faece4`
- Regression: `pytest -q` → 52 passed; UI Node tests → 2 passed, 0 failed

## Evidence

Machine evidence: `evidence/pc_remote/MINDLE_MEDIA_AI_MARKETING_LIVE_SHORTFORM_MP4_E2E_EVIDENCE_v20_1_20261001.json`

Detail evidence: `evidence/pc_remote/media-ai-marketing-live-shortform-v20_1-20261001/`

The ephemeral token was neither persisted nor logged. The old artifact/GitHub-login/Part-01 recovery loop was not used.
