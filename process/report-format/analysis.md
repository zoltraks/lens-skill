# Analysis

## Purpose

> **Scope:** Trade-off analysis and threat model sections
> **Key items:** engineering trade-offs, STRIDE threats

## Trade-off Analysis

Present engineering trade-offs immediately after the Architectural Assessment,
in the same pass as the decisions they discuss.

A trade-off is a deliberate exchange of one quality for another.

Use a table with this fixed column order:

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Column meanings:

- **Trade-off**: a short name for the tension.
- **Context**: the stated constraint or goal that frames the choice, or `NOT SPECIFIED`.
- **Option A**: the quality gained and the quality reduced for the first side.
- **Option B**: the quality gained and the quality reduced for the alternative.
- **Evidence**: what in the system shows this trade-off.
- **Implication**: the neutral consequence under the stated context.

**Rules**

- Frame each trade-off against a stated constraint. If no constraint is stated, put `NOT SPECIFIED`
  in Context and present the trade-off without judging the choice.
- Do not label either side as right or wrong outside an explicit recommendation request.
- A choice that fits the stated context is not a weakness, even if it would be unusual in a
  different context.
- Keep cell language neutral and anchored to evidence.
- Trade-off reasoning may also be embedded into individual finding blocks (under Description or
  Impact) when it directly explains a specific finding. The standalone table here surfaces the
  system-level tensions.
- For a multi-project report, each project block carries its own Trade-off Analysis after that
  project's Architectural Assessment. A combined report-level Trade-off Analysis holds only
  cross-project trade-offs, per the Multi-Project Report Structure section.
- When the trade-off analysis includes an explicit recommendation, that recommendation must also
  appear as a `REC-XXX` entry in the Actionable Remediation Roadmap, traced to the relevant
  `FND-XXX`.

## Threat Model

Include this section only when the system has a security-relevant attack surface,
per `assessment/threat-model.md`.

Omit it for a single-user local utility with no trust boundary,
and note the omission in Scope Exclusions.

Apply STRIDE to the evidenced trust boundaries in the Data Flow Diagram.

Identify selected NIST SP 800-30 or ASVS requirements only when actually assessed, do not claim
ASVS Level 2 coverage merely because a threat table exists.

Present one table keyed by trust boundary and STRIDE category, then describe each material threat
with evidence and its linked `FND-XXX` and `RSK-XXX`.

| Boundary        | STRIDE            | Threat Description                | Control              | Finding     |
|-----------------|-------------------|-----------------------------------|----------------------|-------------|
| Network ingress | Spoofing          | Token forgery if signing key weak | JWT HS256 validation | FND-SEC-XXX |
| Write path      | Tampering         | Path traversal on write           | None (gap)           | FND-SEC-XXX |
| API surface     | Denial of Service | No rate limiting                  | None (gap)           | FND-SEC-XXX |

A threat with no linked finding leaves the `Finding` cell empty rather than writing `none`.

The six STRIDE categories are `Spoofing`, `Tampering`, `Repudiation`, `Information Disclosure`,
`Denial of Service`, and `Elevation of Privilege`.

Every unmitigated threat must trace to a finding and a risk.

Never output plaintext secrets when describing an information-disclosure threat.

When the report language is not English, apply the column header translations from the matching
`translations/` file.
