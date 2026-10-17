# MINDLE MEDIA AI v20.2.6 workspace-to-desktop mirror review

## Applied

- Restored `ui/approved_visual.css` to the exact Git blob from `97900cc6c784e74b4224333fa2cc84d29c611f87`.
- Removed the rejected v20.2.5 forced row-height/clipping block.
- Preserved the branded icon, favicon, no-cache headers, Shortform controls, and canonical launcher.
- Added `/api/runtime-identity` so the launcher verifies repository root, branch, full HEAD, and UI fingerprint before reuse.
- Launcher now stops only a stale MEDIA AI `product_server` process when identity does not match.
- Workspace mirror validator passes.

## Verification

- Control plane: `MEDIA-AI-20261002-V20.2.6` PASS
- Golden CSS Git blob match: PASS
- Node UI tests: 2/2 PASS
- Python tests: 52/52 PASS
- Runtime identity: current repository / branch / HEAD / fingerprint returned by port 8768
- Remote readback: current branch equals `aff9bcccaf5dc7f5e32f85ee51b2e35a417e8e78`

## Evidence limitation

The active desktop bridge could expose the UI accessibility tree but could not save native Windows screenshots or run browser-JS geometry evaluation. Required PNG captures are therefore not fabricated, and machine evidence remains `FAIL` until the six native captures and direct workspace-vs-desktop numeric comparison are available.
