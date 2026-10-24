# One-click Windows runtime execution plan

This is a prebuild implementation plan, not a compiled or validated launcher.

1. Obtain the actual current PC Work validator result using the immutable activated control files. Preserve all General Work source at 9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb and its disabled controls.
2. Inventory the working local Python/native DLL/FFmpeg/font/model closure. Resolve redistribution evidence before adding binaries. Preserve model revision and SHA-256 lineage. Include a redistributable CJK font from an approved source rather than copying an arbitrary Windows font.
3. Build a native GUI launcher with an appended, hash-pinned local runtime payload. A statically linked Go/Win32 bootstrap is a candidate to avoid introducing an additional MSVC requirement in the launcher itself; compiler/toolchain availability and license manifest still require verification. Do not claim this solves Python/backend MSVC requirements.
4. On double-click, validate the payload and safely materialize into a versioned per-user runtime directory. Reject absolute/traversal/case-duplicate ZIP entries. Use staging plus atomic replacement and a validated manifest. Subsequent launches reuse verified files. Keep persistent project data outside the runtime and migrate/reuse the existing safe data location when present.
5. Serialize launches with an OS-level lock/mutex. Check application identity, manifest, PID/health before reusing a server. Recover stale locks without killing unrelated processes. Choose a deterministic free loopback port. Catch child process exit immediately and show a GUI error instead of a blind wait.
6. Start only packaged pythonw and package-local source/FFmpeg/models with sanitized environment. Add a runtime health endpoint only as lifecycle wiring if needed. No Git, system Python, pip, token or first-run model downloads.
7. After health readiness, open one UI through a Windows default-browser mechanism. Repeated clicks activate/reuse the existing product as far as the browser permits. Provide a clear association fallback or GUI error. No Chrome requirement and no terminal UX.
8. Place only the delivery artifact in an ordinary employee-style Windows profile, then perform the full 24-scenario real double-click/model/save/export/relaunch test plus negative tests. A sandbox/CI bootstrap test does not substitute for this gate.

The old installer scripts remain historical and are not the normal user entry. External Marketing/AVORA remains DEFERRED_EXTERNAL. No new repository, worktree, branch, force push or PR merge is authorized.
