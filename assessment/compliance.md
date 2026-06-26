# Compliance and Data Protection

## Purpose

> **Scope:** Data protection, privacy, regulatory obligations, licensing, auditability
> **Key items:** personal data handling, retention, consent, regulatory scope, license compliance, audit trail

This file guides assessment of legal and regulatory obligations that apply to a system, especially one handling user or business data in production.

Apply `principles/evaluation-rules.md` throughout. State obligations only where the input or the system's domain makes them applicable. This is a technical assessment of observable controls, not legal advice.

## What To Evaluate

- Personal data: whether the system collects, stores, or transmits personal or sensitive data.
- Data protection: whether data is minimized, protected, and retained for a bounded period.
- Consent and rights: whether consent and data-subject rights are handled where applicable.
- Regulatory scope: whether a regime such as data-protection or sector regulation plausibly applies.
- Licensing: whether the project's own license and third-party obligations are satisfied.
- Auditability: whether security-relevant actions leave an audit trail.

## Evidence To Look For

| Signal                  | Where It Appears                                   |
|-------------------------|----------------------------------------------------|
| Personal data handling  | Data models, storage of user or sensitive fields   |
| Retention and deletion  | Retention policy, deletion paths, expiry logic     |
| Consent and rights      | Consent flows, export or delete capabilities       |
| Project license         | License file, headers, distribution terms          |
| Third-party obligations | Attribution, copyleft, notice files                |
| Audit trail             | Audit logs of access and changes to sensitive data |

## Status Criteria

- `PASS`: Applicable obligations are identified and matching controls are present, with evidence.
- `PARTIAL`: Some controls exist but coverage of applicable obligations is incomplete or unclear.
- `FAIL`: An applicable obligation has no matching control, with evidence.
- `UNKNOWN`: Data handling or legal artifacts were not provided.
- `N/A`: The system handles no regulated data and has no applicable regime, with justification.

## Common Risks

- Unbounded retention of personal data raises exposure and regulatory risk.
- Absence of deletion or export paths blocks data-subject rights where they apply.
- Unsatisfied third-party license obligations create legal and distribution risk.
- No audit trail leaves access to sensitive data unaccountable.

## What Raises Confidence

- A clear inventory of what data is collected and why.
- Bounded retention with working deletion and export paths where rights apply.
- A satisfied project license and recorded third-party obligations.
- An audit trail for access to and changes of sensitive data.

Use `N/A` only when the system genuinely processes no regulated data, with a one-line justification. When in doubt between `N/A` and `UNKNOWN`, prefer `UNKNOWN`. Do not assert legal conclusions; report observable controls and applicable obligations.
