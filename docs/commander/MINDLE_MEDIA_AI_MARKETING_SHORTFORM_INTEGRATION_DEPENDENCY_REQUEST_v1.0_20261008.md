# MINDLE MEDIA AI → Marketing / AVORA — Shortform External Integration Dependency Request v1.0

Date: 2026-10-08
Status: REQUIRED TO RESUME FINAL FULL-PRODUCT E2E
Requester: MINDLE MEDIA AI Product E2E lane

## Current verified state

MINDLE MEDIA AI base product runtime has passed:
- PHOTO segment / 4x
- VIDEO H.264 browser playback
- Korean STT UI
- Save / Close / Reopen
- Export

The only remaining blocker is the real external Marketing / AVORA / 광고 숏폼 integration.

Current blocker:
BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION

## Marketing integration owner must provide

1. Actual Marketing provider URL reachable from the GitHub Actions E2E runner.
   Configure as:
   MARKETING_SHORTFORM_BASE_URL

2. Bridge token.
   Configure only as GitHub Actions secret:
   MARKETING_SHORTFORM_BRIDGE_TOKEN

   Do NOT place the token in:
   - this document
   - source code
   - issue/PR comments
   - logs
   - chat messages

3. Confirm the real SHORTFORM BRIDGE Contract endpoint/path/method used by the provider.

4. Provide one approved AVORA asset/reference for the final E2E with:
   - stable ID/reference
   - approval provenance/status
   - origin
   - immutable SHA-256 where applicable

5. Provide/enable the Representative Approval flow required before final MP4 export.

## Runtime requirement

If the Marketing provider is local-only, the actual provider must be started inside the same GitHub Actions job/service network. A URL such as http://127.0.0.1:4318 is valid only when a real Marketing provider is actually listening there.

## Required final validation sequence

real Marketing HTTP
→ approved AVORA asset
→ 9:16 Shortform browser Preview
→ Representative Approval
→ approved MP4 Export
→ ffprobe / SHA-256
→ Evidence publication / remote readback

Mocks, stubs, historical responses, or fabricated approval cannot satisfy this request.

No automatic publishing or advertising spend is part of this test.
