# Security

## Purpose

> **Scope:** Authentication, authorization, input validation, OWASP risks, data exposure
> **Key items:** identity, access control, untrusted input handling, secret management, data protection

This file guides assessment of the system's defensive posture.

Apply `principles/evaluation-rules.md` throughout. Assess only what the input shows. Do not perform credential harvesting or offensive actions; this is a defensive review.

## What To Evaluate

- Authentication: how identity is established and protected.
- Authorization: how access to resources and actions is controlled.
- Input validation: how untrusted input is validated, encoded, and bounded.
- OWASP risks: presence of common web and application risk categories.
- Data exposure: how sensitive data and secrets are stored, transmitted, and logged.

## Evidence To Look For

| Signal                       | Where It Appears                                   |
|------------------------------|----------------------------------------------------|
| Authentication mechanism     | Auth libraries, session or token handling          |
| Authorization checks         | Access control rules, role checks, policy code     |
| Input handling               | Validation, parameterized queries, output encoding |
| Secret management            | Secret stores, environment handling, key rotation  |
| Transport security           | TLS configuration, certificate handling            |
| Sensitive data in logs       | Logging of credentials, tokens, or personal data   |

## Status Criteria

- `PASS`: Identity, access control, and input handling are present and consistent, and secrets and sensitive data are protected, with evidence.
- `PARTIAL`: Some controls are present but inconsistent, incomplete, or only partly evidenced.
- `FAIL`: A required control is absent or clearly defeated, with evidence.
- `UNKNOWN`: Security-relevant artifacts were not provided.

## Common Risks

- Missing or weak authentication exposes protected functionality.
- Broken or absent authorization allows access beyond intended scope.
- Unvalidated input enables injection and related attacks.
- Secrets committed to source or logged in plaintext leak credentials.
- Sensitive data transmitted or stored without protection risks exposure.

## What Raises Confidence

- A consistent authentication and session or token strategy.
- Authorization enforced at every protected boundary.
- Parameterized data access and validated, encoded input and output.
- Secrets held in a dedicated store and kept out of logs and source.
- Transport encryption applied to all sensitive traffic.

Mark each missing signal explicitly rather than inferring its presence. Do not claim a control is effective merely because it is referenced.
