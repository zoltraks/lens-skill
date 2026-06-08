# Trade-off Analysis

## Purpose

> **Scope:** Surfacing and presenting engineering trade-offs as a standalone section and within findings
> **Key items:** option comparisons, cost versus quality, speed versus maintainability, simplicity versus flexibility

This file guides trade-off reasoning that appears in two places:

- A standalone **Trade-off Analysis** section in the report, before the Actionable Remediation Roadmap.
- Embedded into individual `FND-ARC-XXX`, `FND-CQ-XXX`, `FND-AIP-XXX`, or `FND-CPR-XXX` finding blocks, under the Description or Impact bullet, when the trade-off directly explains a specific finding.

A trade-off is a deliberate exchange of one quality for another.

Apply `principles/evaluation-rules.md` throughout. Present trade-offs neutrally. Do not declare a winner unless the user asked for a recommendation.

## What A Trade-off Is

A trade-off exists when improving one property tends to cost another.

State the two sides explicitly and the context that determines which side matters more.

Tie each trade-off to evidence in the system, not to general theory.

## Common Axes

Consider these axes where the system shows tension:

- Option A versus Option B, where two concrete designs were possible.
- Cost versus quality.
- Speed of delivery versus long-term maintainability.
- Simplicity versus flexibility.
- Performance versus readability.
- Consistency versus availability in distributed data.

## How To Present

Present trade-offs as one table. One row per trade-off. Use this fixed column order:

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

When the report language is Polish, translate the column headers into Polish using the equivalents defined in `principles/output-style.md`.

Column meanings:

- **Trade-off**: a short name for the tension.
- **Context**: the stated constraint or goal that frames the choice, or `NOT SPECIFIED`.
- **Option A**: the quality gained and the quality reduced for the first side.
- **Option B**: the quality gained and the quality reduced for the alternative.
- **Evidence**: what in the system shows this trade-off.
- **Implication**: the neutral consequence under the stated context.

## Rules

- Frame each trade-off against a stated constraint. If no constraint is stated, put `NOT SPECIFIED` in Context and present the trade-off without judging the choice.
- Do not label either side as right or wrong outside an explicit recommendation request.
- A choice that fits the stated context is not a weakness, even if it would be unusual in a different context.
- Keep cell language neutral and anchored to evidence.

## Example

```text
| In-memory vs external store | Single-instance prototype, no stated scale | Simplicity / no horizontal scaling | Scaling / added operational surface | State held in process variables, no datastore config | Simpler design fits the stated context; scaling later needs rework |
```
