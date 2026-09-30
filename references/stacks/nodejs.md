# Node.js And npm Baseline

## Purpose

> **Scope:** Checkable constraints for Node.js runtimes, npm packages, Express/Fastify services,
> and Node-based CLIs
> **Key items:** release floor, manifest fields, lockfile rules, security checklist, testing and
> packaging expectations

This file distills the authoritative Node.js, npm, Express, Fastify, and OWASP sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source alone.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/security-review.md`,
`assessment/dependency-review.md`, and `assessment/testing-review.md` for JavaScript backends.

## Runtime Floor

The Node.js release schedule (https://nodejs.org/en/about/previous-releases) and the
machine-readable mirror (https://endoflife.date/api/node.json) give the support floor.

- Production deployments run an Active LTS or Maintenance LTS line. At snapshot time Node 24
  (Krypton) is LTS, Node 22 (Jod) is LTS, and Node 26 is Current.
- Node 20 reached end-of-life 2026-04-30. Odd-numbered lines before Node 27 expire six months
  after release and from Node 27 every major moves to LTS.
- `engines.node` in `package.json` should express the floor the code actually uses. The floor
  has no effect unless `.npmrc` sets `engine-strict=true` or the installer runs with
  `--engine-strict`.
- A runtime older than the oldest Maintenance LTS line is a finding regardless of test status.

## Manifest And Lockfile

From the npm documentation (https://docs.npmjs.com/cli/v11/configuring-npm/package-json,
https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json,
https://docs.npmjs.com/cli/v11/commands/npm-ci,
https://docs.npmjs.com/cli/v11/commands/npm-audit).

- Published packages need `name`, `version`, `description`, `license`, and an entry surface
  (`main`, `exports`, or `bin`). `files` whitelists the published surface.
- `exports` is authoritative when present: subpaths not listed are unreachable, which changes
  what "public API" means for a compatibility audit.
- Libraries should not commit `package-lock.json` unless the project policy says otherwise.
  applications should always commit it.
- `npm ci` is the reproducible install: it deletes `node_modules`, installs strictly from the
  lockfile, and fails when the manifest and lockfile disagree, so it is the CI form.
- `lockfileVersion` 3 is the npm 9+ default. Version 1 lacks the hidden lockfile metadata.
- `npm audit` output is advisory evidence, not execution evidence of vulnerable code paths.
- `npm publish --provenance` emits a Sigstore attestation tying the artifact to a public repo
  and workflow. Its absence is at most an observation.

## Node.js Security Baseline

From the Node.js security best-practices page
(https://nodejs.org/en/learn/getting-started/security-best-practices) and the OWASP Node.js
cheat sheet (https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html).

The official threat list names the classes an audit checks directly:

- HTTP server DoS (CWE-400): servers need socket error handlers, request timeouts, and body
  size limits. The runtime does not bound request bodies for the application.
- DNS rebinding (CWE-346): services bound to public interfaces must not trust `Host` blindly.
- Timing attacks (CWE-208): secret comparison uses `crypto.timingSafeEqual`, never `===`.
- Prototype pollution (CWE-1321): avoid merging attacker-controlled objects. Prefer `Map`,
  `Object.create(null)`, or schema validation.
- Uncontrolled search path (CWE-427): child-process spawn resolves binaries against `PATH`.
  pin absolute paths or control the environment.
- Malicious third-party modules (CWE-1357): typosquatting and takeover are dependency-review
  items. Lockfile pinning and `ignore-scripts` reduce install-time execution.
- Monkey patching (CWE-349) and experimental flags: code that patches globals or needs
  `--experimental-*` in production is a finding.

Checkable hardening items:

- `eval`, `new Function`, and `vm` module use are flagged. The `vm` module documentation states
  it is not a security sandbox.
- `child_process.exec` with interpolated strings enables shell injection. `execFile`/`spawn`
  with argument arrays avoids a shell.
- Regular expressions on user input carry ReDoS risk. Untested regexes on request paths are
  reportable.
- Secrets never live in source or `package.json`. `.npmrc` tokens and `NODE_OPTIONS` misuse are
  checked in `assessment/security-review.md`.
- `process.env` is the 12-factor configuration surface. Missing validation of required
  variables at startup is an absent-control observation.
- The `node:test` runner (`node --test`, `describe`/`it`, `mock`, coverage flags) is the stdlib
  harness. Its presence satisfies the "has tests" floor without extra dependencies.

## Express

From the Express security guide (https://expressjs.com/en/advanced/best-practice-security.html),
error-handling guide (https://expressjs.com/en/guide/error-handling.html), Express 5 API
(https://expressjs.com/en/5x/api.html), and migration guide
(https://expressjs.com/en/guide/migrating-5.html).

- Express 2.x and 3.x are unmaintained. Their presence is a finding.
- `app.disable('x-powered-by')` or Helmet removes the fingerprinting header.
- Helmet's default set covers CSP, HSTS, `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Origin-Agent-Cluster`, and removes `X-Powered-By`. A service without
  Helmet or an equivalent header layer is an observation.
- Session middleware must not use default cookie names or insecure options. The built-in
  memory session store is documented as unsuitable for production.
- Open redirects must validate target hosts before `res.redirect`.
- Error-handling middleware has the four-argument `(err, req, res, next)` signature. A missing
  error handler leaves stack-trace leakage to defaults, and production expects
  `NODE_ENV=production`.
- Rate limiting (`express-rate-limit` or equivalent) belongs on authentication and
  resource-heavy endpoints.
- Express 5 changed route syntax (`*` wildcards became `/*splat`, optional segments changed),
  `req.host` no longer strips the port, and middleware moved out of the core. A v4-to-v5 port
  inherits those deltas.

## Fastify And CLIs

From the Fastify server reference (https://fastify.dev/docs/latest/Reference/Server/) and the
CLI guidelines at https://clig.dev/.

- Fastify validates request and response payloads with JSON Schema per route. Routes without
  schemas skip that check.
- `trustProxy` controls whether `X-Forwarded-For` is trusted for client IPs. A proxied service
  without it mis-attributes callers.
- CLI conventions: `-h`/`--help` and `--version` exist, errors go to stderr with a non-zero
  exit code, output is machine-parseable on stdout, color is disabled when piped or under
  `NO_COLOR`, and stdin input is supported where it makes sense.

## Package Surface

From https://publint.dev/ and https://arethetypeswrong.github.io/.

- Published packages should survive `publint` and `arethetypeswrong` checks: correct `exports`
  conditions, `types` present under `exports`, no dual CJS/ESM hazard, `files` covering the
  entry surface.
- `main` without `exports`, missing `types`, or `type: module` mismatches are package-surface
  findings for libraries.

## Testing And Analysis Expectations

- `node:test` covers the floor. Vitest and Jest configs are covered in
  `references/stacks/typescript.md`.
- `supertest` (https://github.com/forwardemail/supertest) provides HTTP-level assertions
  against an app instance without binding a port.
- `eslint-plugin-security` (https://github.com/eslint-community/eslint-plugin-security) and
  `eslint-plugin-n` (https://github.com/eslint-community/eslint-plugin-n) supply the CWE-linked
  rule names consumed by `references/cwe-analyzer.md`.
- `node-jsonwebtoken` (https://github.com/auth0/node-jsonwebtoken) callers must pin
  `algorithms` in `jwt.verify`. Omitting it accepts whatever the token header claims,
  including `none` where configured.

## Live Check

When web fetch is available, compare the runtime floor against `endoflife.date` and the Node.js
releases page, and spot-check one security list item against the OWASP cheat sheet.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
