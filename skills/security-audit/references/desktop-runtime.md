---
applies-when: detect reports project_kind "electron" (Electron / Chromium / desktop renderer)
read-when: Phase 1 gate `reference_gates.desktop-runtime` is true
---

# Desktop runtime checklist (Electron / Chromium)

Gated. Apply only when `audit_scan.py detect` reports `electron` among
`project_kinds` (an Obsidian plugin counts: it runs in Electron's
renderer). For a pure web app, CLI, or library, skip this file.

An Electron app carries a threat model that generic OWASP/CWE checks
miss entirely: the renderer bridges untrusted web content and full Node
capability. The single most valuable check here is the isolation
invariant; the rest hardens the bridge.

## The isolation invariant (check first, highest severity)

- `sandbox` iframe attribute: `allow-scripts` and `allow-same-origin`
  MUST NOT appear together. Together they let sandboxed script reach out
  of the sandbox (same origin -> can rewrite the parent). This is a
  Critical finding wherever a dynamic-code surface relies on the sandbox
  as its only boundary.
- `webPreferences`: `contextIsolation: true`, `nodeIntegration: false`,
  `sandbox: true` on every `BrowserWindow` / `<webview>`. Any window
  that loads remote or user content with `nodeIntegration: true` is
  Critical.
- `webSecurity: false` or `allowRunningInsecureContent: true`: Critical
  unless justified with a documented reason and a compensating control.
- `vm.runInNewContext` / `vm.runInThisContext` / `child_process.fork`
  are NOT security boundaries. If code treats them as a sandbox for
  untrusted input, that is a finding regardless of options.

## Content Security Policy

- Review the actual CSP (meta tag AND HTTP/response header; the header
  wins). Flag `unsafe-eval` and `unsafe-inline` in `script-src`.
- `default-src 'none'` as the baseline; every widened directive
  (`connect-src`, `frame-src`, `img-src`) needs a reason.
- A CSP that allows `unsafe-eval` only inside an origin-isolated sandbox
  frame can be acceptable; verify the isolation, do not just flag the
  token.

## IPC and postMessage bridge

- Every `window.addEventListener('message', ...)` handler MUST check
  `event.origin` (and `event.source` where applicable) before trusting
  `event.data`. A missing origin check is a High finding.
- `postMessage(..., '*')` with no receiving-side auth: High (any frame
  can inject).
- `ipcMain.handle` / `ipcMain.on`: validate `event.senderFrame` /
  channel arguments; never `eval`/`exec` on IPC payloads.
- `contextBridge.exposeInMainWorld`: the exposed surface must be minimal
  and must not leak Node builtins or live objects across the boundary.
  A bridge that exposes `require`, `fs`, `child_process`, or a broad
  passthrough is a High finding.

## OS reach from the renderer

- `shell.openExternal(url)` / `shell.openPath(p)` with an
  attacker-influenced argument = arbitrary program launch via URI
  handler. Require a scheme allowlist (https only) and trace argument
  provenance. High.
- Custom protocol handlers (`registerProtocol`, `setAsDefaultProtocolClient`,
  `obsidian://`): every deep link is triggerable from any web page.
  Check for side effects without confirmation, reentrancy, and OAuth
  redirect abuse. High.
- Local / loopback HTTP server (`127.0.0.1`): check for DNS-rebinding
  (validate the `Host` header against an allowlist; a simple GET skips
  CORS preflight), and that "CORS" is not mistaken for server auth.
  Token files on disk need restrictive permissions cross-platform.
- `will-navigate` / `window.open` / `setWindowOpenHandler`: block or
  validate navigation targets; `window.open` without `noopener` is a
  Low finding.

## Secrets at rest

- Prefer the OS keychain (Electron `safeStorage`). A plaintext fallback
  when the keychain is unavailable must be disclosed to the user and
  recorded, never silent.

## Dependency reach (complements SCA)

- The renderer with Node integration can `require` any Node builtin;
  enumerate which builtins are reachable from untrusted-input paths.
- Native modules (`.node`, prebuilt binaries): `npm audit` does not
  cover binary provenance. Note this as an SCA blindspot.

## Recommended tools

- `electronegativity` (Doyensec) for the webPreferences/CSP surface.
  Record it in the tools ledger only if it actually ran.
