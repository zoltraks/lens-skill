# Threat Model

## Purpose

> **Scope:** Structured threat enumeration using STRIDE, mapped to trust boundaries and data flows
> **Key items:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege, attack surface, trust boundaries

This file guides a structured threat model of the system using the STRIDE framework, anchored to the data flow model in `assessment/data-flow.md`. It complements the control-level review in `assessment/security.md`: security findings are symptoms, the threat model maps the attack surface systematically.

Apply `principles/evaluation-rules.md` throughout. This is a defensive analysis. Enumerate threats from observable structure; do not perform offensive actions or credential harvesting.

## When This Applies

This assessment applies when the system has a security-relevant attack surface: a network service, an API, an authentication or authorization boundary, multi-tenant data, or any flow that crosses a trust boundary.

It does not apply to a single-user local utility with no network surface, no untrusted input, and no shared data. In that case, mark the section `N/A` with a one-line justification anchored to the deployment model. When in doubt between `N/A` and including the section, include it.

## Framework

STRIDE enumerates six threat categories, each the inverse of a security property:

| Threat | Violates | Question to ask at each boundary |
|--------|----------|----------------------------------|
| Spoofing | Authentication | Can an actor impersonate another identity? |
| Tampering | Integrity | Can data or code be modified in transit or at rest? |
| Repudiation | Non-repudiation | Can an actor deny an action without an audit trail? |
| Information Disclosure | Confidentiality | Can data be read by an unauthorized party? |
| Denial of Service | Availability | Can the system be made unavailable? |
| Elevation of Privilege | Authorization | Can an actor gain rights beyond their grant? |

## Method

This method aligns with NIST SP 800-30 (risk assessment) and OWASP ASVS Level 2 architecture and threat modeling requirements.

**Establish the model**

Use the Level-1 data flow model from `assessment/data-flow.md`. List the trust boundaries.

**Enumerate per boundary**

For each flow that crosses a trust boundary, ask each of the six STRIDE questions. Record any plausible threat as a row.

**Link to findings and risks**

Each confirmed threat that rests on a concrete gap becomes or references a finding (`FND-SEC-XXX`) and a risk (`RSK-XXX`). Threats that are already mitigated are recorded as mitigated, with the control cited.

## Evidence To Look For

| Signal | Where It Appears |
|--------|------------------|
| Spoofing surface | Token issuance, credential checks, session handling |
| Tampering surface | Write endpoints, deserialization, file writes, unsigned data |
| Repudiation surface | Absence of audit logs on sensitive actions |
| Disclosure surface | Error messages, logs, unencrypted transport, broad responses |
| DoS surface | Unbounded input, missing rate limits, unbounded retries |
| Elevation surface | Authorization checks, role enforcement, privilege transitions |

## How To Present

Render the threat model as described in `process/report-format.md`. Present one table keyed by trust boundary and STRIDE category, then describe each material threat with evidence and its linked `FND-XXX` / `RSK-XXX`.

## Common Threat Examples

Use these examples to avoid overlooking categories that are often missed:

- **Information Disclosure**: Unencrypted network transport (for example, `ws://` instead of `wss://`), verbose error messages revealing internal paths, log files containing sensitive tokens, broad API responses exposing extra fields.
- **Elevation of Privilege**: Filesystem access without path validation (for example, loading ROM files from user input allowing directory traversal), missing authorization checks on administrative endpoints, ability to escalate from guest to admin via parameter tampering.
- **Repudiation**: Absence of audit logs on security-relevant actions (for example, WebSocket connection events, configuration changes, authentication attempts), missing timestamps or actor attribution in logs.
- **Spoofing**: Missing origin validation on cross-origin requests, weak or absent token verification, unauthenticated WebSocket connections.
- **Tampering**: Unsigned serialized data, lack of integrity checks on downloaded artifacts, writable configuration without validation.
- **Denial of Service**: Unbounded input buffers, missing rate limits, unauthenticated endpoints that trigger heavy computation.

## Status Criteria

- `PASS`: All trust boundaries are enumerated and each material STRIDE threat has an evidenced mitigating control.
- `PARTIAL`: Boundaries are enumerated but some STRIDE categories have unmitigated or unverified threats.
- `FAIL`: Material threats exist at a trust boundary with no mitigating control, with evidence.
- `UNKNOWN`: The attack surface could not be determined from the input.
- `N/A`: The system has no security-relevant trust boundary, with justification.

## Rules

- Check all six STRIDE categories at every trust boundary. A threat model with fewer than six categories examined is incomplete.
- Anchor every threat to a specific trust boundary and flow from the data flow model.
- Do not list a threat that does not map to a concrete boundary or flow.
- Distinguish a present control from a verified-effective control.
- Every unmitigated threat must trace to a finding and a risk; do not leave threats floating outside the register.
- Do not output plaintext secrets, tokens, or keys when describing a disclosure threat.
- If a STRIDE category yields no material threat at a boundary, record it as `None identified` with a one-line justification rather than omitting it.
