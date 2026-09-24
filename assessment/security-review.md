# Security

## Purpose

> **Scope:** Authentication, authorization, input validation, OWASP risks, data exposure
> **Key items:** identity, access control, untrusted input handling, secret management, data
> protection

This file guides assessment of the system's defensive posture.

Apply `principles/evaluation-rules.md` throughout. Assess only what the input shows. Do not perform
credential harvesting or offensive actions, this is a defensive review.

## What To Evaluate

- Authentication: how identity is established and protected.
- Authorization: how access to resources and actions is controlled.
- Input validation: how untrusted input is validated, encoded, and bounded.
- OWASP risks: presence of common web and application risk categories.
- Data exposure: how sensitive data and secrets are stored, transmitted, and logged.

## Evidence To Look For

| Signal                   | Where It Appears                                   |
|--------------------------|----------------------------------------------------|
| Authentication mechanism | Auth libraries, session or token handling          |
| Authorization checks     | Access control rules, role checks, policy code     |
| Input handling           | Validation, parameterized queries, output encoding |
| Secret management        | Secret stores, environment handling, key rotation  |
| Transport security       | TLS configuration, certificate handling            |
| Sensitive data in logs   | Logging of credentials, tokens, or personal data   |

## Control Verification

Trace identity, authorization, input validation, and the protected operation end to end.

For each exposed transport, check object, action, and tenant/path scope independently.

A policy function or middleware name does not prove the caller uses its result.

Check REST, MCP, background work, and direct library calls separately where applicable.

For filesystem operations, distinguish reading an existing path from creating a new destination.

Canonicalizing a nonexistent destination fails, and checking a path before using it can leave a
symlink or time-of-check/time-of-use race.

Recommendations should preserve valid operations while constraining them to the authorized root,
using platform-appropriate containment and atomic operations where needed.

Verify relative and absolute paths, platform-specific prefixes, missing parents, links, and
concurrent changes in an isolated fixture, not against real system files.

For local credential storage, evaluate file permissions or ACLs, inheritance, token lifetime,
backup exposure, and the OS threat model before rating severity.

Do not assert that process arguments or environment variables are readable by every user on every
OS.

Do not collect real credentials to demonstrate exposure.

## Weakness And Vulnerability Classification

For each security finding, record the most specific supported CWE root cause, its title, and a
short mapping rationale, or `UNKNOWN` if the evidence does not support a mapping.

Use `N/A` for findings that are not security weaknesses, including general documentation or
organizational gaps.

Follow [MITRE root-cause mapping guidance](https://cwe.mitre.org/documents/cwe_usage/guidance.html).

Missing authorization may map to CWE-862, incorrect authorization to CWE-863, and path traversal to
CWE-22 or a more specific child when justified by the trace.

Check the entry's mapping guidance rather than tagging by title alone.

The [2025 CWE Top 25](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) ranks CWE-862
fourth and CWE-22 sixth, but prevalence does not establish this project's severity or
exploitability.

For a supported vulnerability, prefer CVSS v4.0, retaining v3.1 where a stakeholder or advisory
requires it.

Record the version, full vector, calculated score, metric group, and rationale for each metric.

For v4.0 use `CVSS-B`, `CVSS-BT`, `CVSS-BE`, or `CVSS-BTE` to state the groups considered.

Validate score/vector agreement with the
[FIRST calculator](https://www.first.org/cvss/calculator/4.0)
or a verified implementation, never invent a score from the qualitative label.

If prerequisites or impact cannot be established, record `INSUFFICIENT INFORMATION` and the missing
metrics, or clearly label bounded scenario vectors as provisional.

When no calculator or verified implementation is accessible, record the derived vector and mark the
score `INSUFFICIENT INFORMATION`. Never emit a score that was not validated.

Separate a publisher's advisory vector from a locally assessed vector.

CVSS describes technical vulnerability severity, not the Lens risk-register likelihood or business
priority, as explained in the [FIRST user guide](https://www.first.org/cvss/v4.0/user-guide).

Retain Lens qualitative severities for engineering and business risks.

Do not apply CVSS to bus factor, debt, licensing uncertainty, or missing runbooks.

## Analyzer Cross-Reference

For every CWE-classified finding, consult `references/cwe-analyzer-map.md` for the equivalent
static analyzer rule in the detected stack.

When a rule exists, record it in the finding with its enablement state, for example "the
equivalent automated check is `CA5359`, not yet enabled". Enablement is determined from
repository evidence such as `.editorconfig` entries, ruleset files, or CI steps, per the
enablement table in `references/cwe-analyzer-map.md`.

When no direct rule exists for the CWE in the stack, state that plainly, for example "no direct
analyzer rule exists for CWE-327 in Rust". Do not present a related rule as coverage of the
whole weakness.

This is a documentation lookup. It names the check a team can enable and verify. It never
implies the analyzer ran during the audit.

## Exploitability Narrative

Every `HIGH` or `CRITICAL` finding on a network-facing surface carries an Exploitability
Narrative in its finding block, per `references/exploitability-narrative.md`. The
narrative reasons through precondition, attack path, and impact at an explicit confidence tier.
Under the default source-only scope the tier is `Theoretical` or `Static-Confirmed`, never
`Dynamically-Verified`.

A network-facing surface is a component reachable across a trust boundary: endpoints, listeners,
message consumers, and parsers of externally supplied input. Findings on internal-only code
paths carry the field as `N/A` with a one-line reason.

## Standards Coverage

Use [OWASP Top 10:2025](https://owasp.org/Top10/2025/) as an awareness taxonomy, including
A01 Broken Access Control and A03 Software Supply Chain Failures where relevant.

For APIs, retain the distinct OWASP API Security Top 10:2023 mapping.

For control verification, select applicable requirements from
[OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS) and record the chosen level and rationale.

Use version-qualified requirement IDs from the consulted release, not remembered IDs from another
version or the repository's development branch.

Report assessed, unassessed, and inapplicable controls with evidence IDs.

When ASVS is applied, cite version-qualified requirement identifiers such as `v5.0.0-1.2.5` and
record the selected level or rationale. Do not use unversioned requirement numbers when editions may
change them.

A sampled review does not establish full ASVS level conformance, and a Top 10 mapping is not a
security certification.

Recheck editions at audit time and preserve a requested legacy baseline with an explanation.

## Tool Corroboration

The audit does not run SAST engines or scanners. Corroboration comes from manual tracing plus
any committed scan results, CI security steps, or documented reviews.

When a committed report claims coverage, check that the engine supports the project's language
and framework.
[CodeQL lists Rust support](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) and
[Semgrep capabilities vary by engine and edition](https://docs.semgrep.dev/semgrep-ce-languages).

Neither language support nor a clean scan establishes coverage of custom authorization semantics.

`cargo audit` checks dependency advisories, and `cargo clippy` checks configured lints, neither
verifies application authorization or path containment, even when their output is documented.

For serious findings, recommend a targeted negative regression test and a valid-operation
control for the verification owner, recording why the audit cannot perform it.

## Status Criteria

- `PASS`: Identity, access control, and input handling are present and consistent, and secrets and
  sensitive data are protected, with evidence.
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

Mark each missing signal explicitly rather than inferring its presence. Do not claim a control is
effective merely because it is referenced.
