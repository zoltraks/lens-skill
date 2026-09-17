# Unified Risk Register

## Purpose

> **Scope:** Risk table format, impact and likelihood rating, severity scale, bidirectional
> cross-referencing with findings
> **Key items:** structured risks, fixed columns, `Low`, `Medium`, `High`, `Critical`, `RSK-[001]`
> indexing, `FND-XXX` traceability

This file defines how to record risks surfaced during assessment. Build the register from the risks
already noted in each `assessment/` file.

Apply `principles/evaluation-rules.md` throughout. Every risk must trace to evidence or to a clearly
marked gap. Every risk must reference its source finding.

## Table Format

Use this fixed column order:

| Risk ID | Risk | Source Finding | Impact | Likelihood | Severity | Mitigation |
|---------|------|----------------|--------|------------|----------|------------|

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Risk ID**: `RSK-[001]` ascending sequentially.
- **Risk**: a concrete technical risk, stated neutrally.
- **Source Finding**: the `FND-[PILLAR]-[NNN]` identifier that produced this risk.
- **Impact**: the consequence if the risk is realized.
- **Likelihood**: how probable the risk is given the evidence.
- **Severity**: one of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- **Mitigation**: a neutral, optional action that would reduce the risk.

## Rating Guidance

Rate impact and likelihood from evidence, not intuition.

Impact bands:

- `LOW`: limited or cosmetic effect.
- `MEDIUM`: degraded function or contained outage.
- `HIGH`: major function loss or data integrity concern.
- `CRITICAL`: data loss, breach, or full outage.

When an impact sits between bands, compare the blast radius. A dead subsystem is `HIGH`
unless it is the system's sole function, a data-corrupting write or an authentication bypass
is `CRITICAL`, a degraded but still working path is `MEDIUM`.

Likelihood bands:

- `LOW`: would require an unusual combination of conditions.
- `MEDIUM`: plausible under normal operation.
- `HIGH`: expected to occur without intervention.

Likelihood rates the probability that the risk materializes for the subject, not the
probability that the underlying defect exists. A defect that always manifests, for example a
stub that always returns zeros, gives its risk `HIGH` likelihood. A defect that needs a
trigger, such as an attacker in position, a compromised file, or a configured feature, is
`MEDIUM` or `LOW` by the trigger's plausibility.

## Severity Scale

Derive severity from impact and likelihood, then record it explicitly.

| Impact \ Likelihood | LOW    | MEDIUM   | HIGH     |
|---------------------|--------|----------|----------|
| CRITICAL            | HIGH   | CRITICAL | CRITICAL |
| HIGH                | MEDIUM | HIGH     | CRITICAL |
| MEDIUM              | LOW    | MEDIUM   | HIGH     |
| LOW                 | LOW    | LOW      | MEDIUM   |

A supported severity must be one of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

Use the missing-information rules below when a rating cannot be supported.

## Classification And Confidence

Use CWE and CVSS from `assessment/security-review.md` only for applicable security findings.

Link those classifications through the source finding rather than replacing this business-risk
matrix with a vulnerability score.

Explain any difference between technical vulnerability severity and the contextual Lens severity.

Keep confidence and verification limits visible in risk detail.

If impact or likelihood lacks a defensible basis, use `UNKNOWN` for the rating and severity rather
than forcing a matrix value, and identify the evidence needed to rate it.

`UNKNOWN` here denotes a missing rating, not an additional severity band.

List unrated risks beside the heat map instead of placing them in an invented cell.

## Cross-Referencing Rules

- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- When multiple findings contribute to one risk, list the primary `FND-XXX`.
- Do not create risks that do not trace to a finding in the Detailed Technical Findings.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

## Rules

- One row per distinct risk. Do not merge unrelated risks.
- State each risk as a property of the system, never as a fault of a person.
- When a risk rests on missing information, mark its likelihood basis as `INSUFFICIENT INFORMATION`
  in the risk text.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for
  directives.
- Keep risk wording consistent with the finding notes that produced it.
- Re-derive every matrix placement during a re-audit. When re-derivation moves a risk's
  severity, record the band change and the matrix rationale in the Changes section, never
  silently preserve or adjust a prior rating.
- Every rated risk occupies exactly one heat-map cell. The union of heat-map cells must equal
  the register's rated risk set, `UNKNOWN`-rated risks are listed beside the map instead.

## Example Row

```text
| RSK-001 | Hardcoded JWT signing key in committed config | FND-SEC-001 | Authentication bypass or token forgery | High | CRITICAL | Move key to secrets manager and rotate |
```
