# Risk Register

## Purpose

> **Scope:** Risk table format, impact and likelihood rating, severity scale
> **Key items:** structured risks, fixed columns, `Low`, `Medium`, `High`, `Critical`

This file defines how to record risks surfaced during assessment. Build the register from the risks already noted in each `assessment/` file.

Apply `principles/evaluation-rules.md` throughout. Every risk must trace to evidence or to a clearly marked gap.

## Table Format

Use this fixed column order:

| Risk | Category | Impact | Likelihood | Severity | Mitigation |
|------|----------|--------|------------|----------|------------|

Column meanings:

- **Risk**: a concrete technical risk, stated neutrally.
- **Category**: the assessment category the risk came from.
- **Impact**: the consequence if the risk is realized.
- **Likelihood**: how probable the risk is given the evidence.
- **Severity**: one of `Low`, `Medium`, `High`, `Critical`.
- **Mitigation**: a neutral, optional action that would reduce the risk.

## Rating Guidance

Rate impact and likelihood from evidence, not intuition.

Impact bands:

- `Low`: limited or cosmetic effect.
- `Medium`: degraded function or contained outage.
- `High`: major function loss or data integrity concern.
- `Critical`: data loss, breach, or full outage.

Likelihood bands:

- `Low`: would require an unusual combination of conditions.
- `Medium`: plausible under normal operation.
- `High`: expected to occur without intervention.

## Severity Scale

Derive severity from impact and likelihood, then record it explicitly.

| Impact \ Likelihood | Low      | Medium   | High      |
|---------------------|----------|----------|-----------|
| Critical            | High     | Critical | Critical  |
| High                | Medium   | High     | Critical  |
| Medium              | Low      | Medium   | High      |
| Low                 | Low      | Low      | Medium    |

Severity must always be one of `Low`, `Medium`, `High`, `Critical`.

## Rules

- One row per distinct risk. Do not merge unrelated risks.
- State each risk as a property of the system, never as a fault of a person.
- When a risk rests on missing information, mark its likelihood basis as `INSUFFICIENT INFORMATION` in the risk text.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for directives.
- Keep risk wording consistent with the category notes that produced it.

## Example Row

```text
| Manual release steps with no checklist | Deployment | Failed or partial release | Medium | High | Document and automate the release path |
```
