# Recommendation Summary

## Purpose

> **Scope:** Non-prescriptive recommendation options with pros, cons, and risk level
> **Key items:** option set, pros and cons, risk level, no absolute directives

This file guides the recommendation section. The goal is to present options, not to dictate a path.

Apply `principles/evaluation-rules.md` throughout. Do not issue absolute directives unless the user explicitly requests them.

## Option Set

Offer a small, mutually understandable set of options. A typical set:

- Option 1: Continue the current approach.
- Option 2: Incremental improvement of specific gaps.
- Option 3: Partial redesign of specific components.

Adjust the set to the system, but keep options distinct and comparable.

## Per-Option Structure

Present options as one table. One row per option. Use this fixed column order:

| Option | Summary | Pros | Cons | Risk Level |
|--------|---------|------|------|------------|

Column meanings:

- **Option**: a short name, for example "Continue current approach".
- **Summary**: a one-line description of the option.
- **Pros**: benefits, each anchored to a finding; separate multiple with a semicolon.
- **Cons**: costs or risks, each anchored to a finding; separate multiple with a semicolon.
- **Risk Level**: one of `Low`, `Medium`, `High`, `Critical`, matching the risk-register vocabulary.

A reusable example row:

```text
| Incremental improvement | Add CI gate and dependency scanning | Closes top risks with bounded effort; reuses existing tests | Requires pipeline setup | Medium |
```

## Rules

- Tie every pro and con to a finding from the assessment or risk register.
- Keep options non-prescriptive. Present them as choices with consequences.
- Do not rank or select an option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored to evidence, and the residual risk.
- Keep language neutral and free of blame.

## Relationship To Other Sections

Recommendations summarize, they do not introduce new findings.

Every option must trace back to gaps in the Quality Assessment, entries in the Risk Register, or tensions in the Trade-off Analysis.

If a recommendation would require information that was never provided, state the missing information rather than assuming it.
