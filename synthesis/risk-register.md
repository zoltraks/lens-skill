# Unified Risk Register

## Purpose

> **Scope:** Risk table format, impact and likelihood rating, severity scale, bidirectional cross-referencing with findings
> **Key items:** structured risks, fixed columns, `Low`, `Medium`, `High`, `Critical`, `RSK-[001]` indexing, `FND-XXX` traceability

This file defines how to record risks surfaced during assessment. Build the register from the risks already noted in each `assessment/` file.

Apply `principles/evaluation-rules.md` throughout. Every risk must trace to evidence or to a clearly marked gap. Every risk must reference its source finding.

## Table Format

Use this fixed column order:

| Risk ID | Risk | Source Finding | Impact | Likelihood | Severity | Mitigation |
|---------|------|----------------|--------|------------|----------|------------|

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

Likelihood bands:

- `LOW`: would require an unusual combination of conditions.
- `MEDIUM`: plausible under normal operation.
- `HIGH`: expected to occur without intervention.

## Severity Scale

Derive severity from impact and likelihood, then record it explicitly.

| Impact \ Likelihood | LOW      | MEDIUM   | HIGH      |
|---------------------|----------|----------|-----------|
| CRITICAL            | HIGH     | CRITICAL | CRITICAL  |
| HIGH                | MEDIUM   | HIGH     | CRITICAL  |
| MEDIUM              | LOW      | MEDIUM   | HIGH      |
| LOW                 | LOW      | LOW      | MEDIUM    |

Severity must always be one of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

## Cross-Referencing Rules

- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- When multiple findings contribute to one risk, list the primary `FND-XXX`.
- Do not create risks that do not trace to a finding in the Detailed Technical Findings.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

## Rules

- One row per distinct risk. Do not merge unrelated risks.
- State each risk as a property of the system, never as a fault of a person.
- When a risk rests on missing information, mark its likelihood basis as `INSUFFICIENT INFORMATION` in the risk text.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for directives.
- Keep risk wording consistent with the finding notes that produced it.

## Example Row

```text
| RSK-001 | Hardcoded JWT signing key in committed config | FND-SEC-001 | Authentication bypass or token forgery | High | CRITICAL | Move key to secrets manager and rotate |
```
