# Electron And Desktop Baseline

## Purpose

> **Scope:** Checkable constraints for Electron shells and desktop-packaged web apps
> **Key items:** context isolation, nodeIntegration, IPC contracts, sandboxing, code signing
> and distribution

This file distills the Electron security, IPC, context-isolation, and process-model docs plus
electron-builder signing guidance listed in `references/source-catalog.md` into constraints an
audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md`, `assessment/best-practices.md`, and
`assessment/deployment-review.md` for desktop subjects.

## Security Checklist

From https://www.electronjs.org/docs/latest/tutorial/security - the headline controls.

- `contextIsolation: true` (default since Electron 12) must stay on. `contextIsolation:
  false` exposes the preload's Node.js bridge to page scripts - a finding.
- `nodeIntegration: false` on every `BrowserWindow`/`webview` that renders remote or
  untrusted content. Enabling it gives any XSS full system access.
- `sandbox: true` for renderers is the Chromium sandbox. `sandbox: false` needs justification.
- Do not enable `webviewTag` unless needed. It multiplies the untrusted-content surface.
- `setWindowOpenHandler` must deny or constrain `window.open`. The default allow is a
  navigation-escape finding.
- `will-navigate`/`will-attach-webview` handlers should restrict navigation to expected
  origins. Unrestricted remote navigation is a finding.
- Only load `https:`/`file:` content. `http:` loads and `allowRunningInsecureContent` are
  findings.
- Keep Electron current: the security doc states only the last few stable majors receive
  fixes. An Electron major more than ~2 versions behind the stable line is a freshness
  observation.

## Process Model And IPC

From https://www.electronjs.org/docs/latest/tutorial/process-model and
https://www.electronjs.org/docs/latest/tutorial/ipc.

- The main process owns Node.js and OS APIs. Renderers are web pages - main-process code
  reachable from a renderer must treat every argument as untrusted.
- `ipcMain.handle` + `ipcRenderer.invoke` is the request/response pattern. `send`/`on` is
  fire-and-forget - a renderer must never receive raw `ipcRenderer` or generic `send` of
  arbitrary channels.
- `contextBridge.exposeInMainWorld` (https://www.electronjs.org/docs/latest/tutorial/context-isolation)
  is the only supported bridge. The exposed object should be a narrow allowlist of methods,
  not `ipcRenderer` wholesale and not Node APIs.
- Validate/sanitize every IPC payload in the main process. Preload-level validation alone is
  bypassable from devtools.

## Distribution

From https://www.electron.build/docs/features/code-signing/.

- Signed binaries are the distribution baseline: macOS requires a Developer ID signature plus
  notarization for Gatekeeper, Windows uses Authenticode (EV or Azure Trusted Signing),
  Linux conventions are per-format.
- An unsigned or un-notarized shipped build is a finding: Gatekeeper/SmartScreen will block
  or warn, and unsigned updatable apps enable tampered-update paths (see
  `references/topics/git-integrity.md` for update-path integrity).
- `electron-builder`/`electron-forge` config fields (`appId`, `mac.category`,
  `win.signingHashAlgorithms`, `publish` target) are the checkable manifest surface.
- `autoUpdater` endpoints must be HTTPS and signature-checked. Plaintext or unchecked update
  feeds are critical findings.

## Live Check

When web fetch is available, spot-check the current recommended security defaults against
electronjs.org/docs/latest/tutorial/security.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
