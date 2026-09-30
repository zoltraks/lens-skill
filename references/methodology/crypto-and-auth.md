# Crypto, Authentication, And Secrets Baseline

## Purpose

> **Scope:** Checkable anchors for credential handling, token validation, TLS posture, and
> secret-free configuration
> **Key items:** password-hash parameters, TLS expectations, JWT/OAuth rules, 12-factor
> config, never-logged data classes

This file distills the OWASP cheat sheets, JWT/OAuth RFCs, and 12-factor source listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md` and `references/cwe-analyzer.md` for credential-surface
findings.

## Password Storage

From https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html.

- Approved hashes: Argon2id (memory ≥19 MiB, iterations ≥2, parallelism 1 per RFC 9106
  calibration), bcrypt (work factor ≥10, ≤72-byte input), scrypt (N≥2^17, r=8, p=1), PBKDF2
  (≥600k iterations HMAC-SHA-256 per current guidance).
- Plain MD5/SHA-1/SHA-256 of passwords, or unsalted fast hashes, are critical findings.
  `password_hash`/`crypto.scrypt`/`bcrypt` usage is the expected shape.
- Pepper storage is server-side outside the database. Salts are per-user random.

## TLS

From https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html.

- TLS 1.2 is the floor, TLS 1.3 preferred. SSLv3/TLS 1.0/1.1 enabled is a finding.
- Certificate checks: SAN covering served names, unexpired, CA-issued in production.
  `rejectUnauthorized: false`, `verify=False`, `InsecureSkipVerify: true`, or
  `checkServerIdentity` stubs are critical TLS-disable findings.
- HTTP -> HTTPS redirect plus HSTS for browser-facing endpoints.

## JWT And OAuth

From https://datatracker.ietf.org/doc/html/rfc7519,
https://datatracker.ietf.org/doc/html/rfc8725,
https://www.rfc-editor.org/rfc/rfc6749, https://www.rfc-editor.org/rfc/rfc6750, and
https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html (the
`_for_Java` sheet was renamed. The crypto-and-validation content is what this file carries).

- `jwt.verify` must pin `algorithms`. `alg:none` and RS256 -> HS256 confusion (verify with the
  public key as an HMAC secret) are the classic bypasses - check the algorithm allowlist.
- Validate `exp`, `iat`, `iss`, `aud` per RFC 7519 claims processing. Missing `exp` means
  non-expiring tokens, a finding for session use.
- RFC 8725 rules: no implicit `none`, no unvalidated `iss`/`sub`, use the explicit algorithm
  allowlist, validate `aud` for the intended recipient.
- RFC 6749: authorization-code flow with PKCE for public clients. Implicit grant is
  deprecated. `client_secret` never in browser source.
- RFC 6750: bearer tokens in the `Authorization` header, `401` + `WWW-Authenticate` on
  missing/invalid. Tokens in URLs are findings (they land in logs/history).
- Long-lived JWTs need revocation strategy. Stateless tokens cannot be invalidated -
  short expiry plus refresh rotation is the expected shape.
- Session fixation: IDs rotate on login/elevation. Cookies `HttpOnly`, `Secure`,
  `SameSite` per the cheat sheet.

## Twelve-Factor Config

From https://12factor.net/config.

- Config (that varies between deploys) lives in environment variables. Credentials and
  endpoints never sit in code.
- `.env` files are developer convenience and must be gitignored. Committed `.env` files are
  a finding.
- `appsettings.json`/`config.json`/`config.yaml` with real secrets instead of placeholders
  are secret-resolution findings. The audit traces each secret's source chain.

## Logging Exclusions

From https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html.

- Never logged: session IDs, access tokens, passwords, PII (health/financial), full
  authorization headers, connection strings.
- Authentication events (login, lockout, password changes), authorization denials, and input
  validation failures are the required logging set. Their absence is a monitoring gap
  observation.

## Live Check

When web fetch is available, spot-check one password parameter against the Password Storage
cheat sheet and one JWT rule against RFC 8725.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
