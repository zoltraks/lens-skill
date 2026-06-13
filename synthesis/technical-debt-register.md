# Technical Debt Register

## Purpose

> **Scope:** A formal inventory of technical debt items, distinct from the risk register
> **Key items:** `TDR-[001]` indexing, debt category, remediation cost, cost of delay, `FND-XXX` traceability

This file defines the Technical Debt Register (TDR), a structured inventory of debt items that are not security risks but compound over time. It is distinct from the Unified Risk Register: risks describe what could go wrong, debt describes accumulated cost that is already present and invisible.

The TDR convention is analogous to Architecture Decision Records. The cost model follows CISQ structural quality characteristics and the SQALE method, which separates remediation cost (effort to fix) from cost of delay (ongoing cost of leaving the debt in place).

Apply `principles/evaluation-rules.md` throughout. Every debt item must trace to a concrete finding or a concrete observation in the code.

## When This Applies

Include the TDR when the assessment surfaces structural debt items that are not captured as risks: dead code, duplicated logic, low-value tests, hardcoded values that should be configurable, advisory-only checks, or shortcuts.

When no such items exist, mark the section `N/A` rather than fabricating debt. Do not duplicate the risk register here.

## Table Format

Use this fixed column order:

| Debt ID | Debt Item | Category | Source Finding | Remediation Cost | Cost of Delay | Status |
|---------|-----------|----------|----------------|------------------|---------------|--------|

When the report language is Polish, translate the column headers into Polish: `Identyfikator długu`, `Pozycja długu`, `Kategoria`, `Źródło`, `Koszt naprawy`, `Koszt zwłoki`, `Status`.

Column meanings:

- **Debt ID**: `TDR-[001]` ascending sequentially.
- **Debt Item**: a concrete, neutrally stated debt, anchored to a file or pattern.
- **Category**: one of the CISQ characteristics the debt degrades: `Reliability`, `Performance Efficiency`, `Security`, `Maintainability`.
- **Source Finding**: the `FND-XXX` identifier that produced this item, or `Direct observation` when it stems from code review without a standalone finding.
- **Remediation Cost**: estimated effort to fix (`High`, `Medium`, `Low`).
- **Cost of Delay**: the ongoing cost of leaving the debt (`High`, `Medium`, `Low`).
- **Status**: `Open` by default.

## What Belongs Here

- Dead code and suppressed-warning annotations that mask unused code.
- Low-value or structure-only tests that assert no real behavior.
- Duplicated logic that should be a shared abstraction.
- Hardcoded values that should be named constants or configuration.
- Advisory-only checks whose result is computed but discarded.
- Workarounds and shortcuts documented as such.

## What Does Not Belong Here

- Security risks. Those belong in the Unified Risk Register.
- Missing features. The TDR records debt in existing code, not absent functionality.
- Subjective style preferences with no maintainability cost.

## Rules

- One row per distinct debt item. Do not merge unrelated items.
- Every item must trace to a `FND-XXX` or be marked `Direct observation` with a cited file.
- State each item as a property of the code, never as a fault of a person.
- Keep remediation cost and cost of delay anchored to evidence, not intuition.
- A debt item may also be a recommendation target; reference it from the roadmap by its source finding, not by `TDR-XXX`.

## Example Row

```text
| TDR-001 | Eight #[allow(dead_code)] annotations mask unused code | Maintainability | FND-CQ-002 | Low | Medium | Open |
```
