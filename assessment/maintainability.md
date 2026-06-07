# Maintainability

## Purpose

> **Scope:** Modularity, coupling, code structure, technical-debt signals
> **Key items:** module boundaries, dependency direction, structure clarity, debt markers

This file guides assessment of how easily the system can be understood and changed.

Apply `principles/evaluation-rules.md` throughout. Describe code properties, never the authors.

## What To Evaluate

- Modularity: whether the system is divided into coherent units with clear responsibilities.
- Coupling: how strongly modules depend on each other, and the direction of dependencies.
- Code structure: consistency of layout, naming, and layering.
- Technical-debt signals: duplicated logic, dead code, long files, and explicit debt markers.

## Evidence To Look For

| Signal                       | Where It Appears                                   |
|------------------------------|----------------------------------------------------|
| Module boundaries            | Directory layout, package structure, interfaces    |
| Dependency direction         | Imports, dependency graphs, layering rules         |
| Consistency                  | Naming conventions, repeated patterns              |
| Debt markers                 | TODO and FIXME comments, deprecation notes         |
| Size signals                 | Very large files, very long functions              |
| Duplication                  | Repeated blocks, copy-paste patterns               |

## Status Criteria

- `PASS`: Clear module boundaries, controlled coupling, consistent structure, and few debt signals, with evidence.
- `PARTIAL`: Reasonable structure with notable coupling, inconsistency, or localized debt.
- `FAIL`: No clear boundaries, pervasive coupling, or structural disorder, with evidence.
- `UNKNOWN`: Source structure was not provided for inspection.

## Common Risks

- High coupling means a change in one module forces changes across many others.
- Inconsistent structure slows onboarding and raises change error rates.
- Accumulated duplication makes fixes incomplete and inconsistent.
- Unbounded module growth hides responsibilities and complicates testing.

## What Raises Confidence

- Coherent modules with single, stated responsibilities.
- Dependencies that flow in one direction across clear layers.
- Consistent naming and layout across the codebase.
- Debt that is tracked explicitly rather than hidden.

Mark each missing signal explicitly rather than inferring its presence.
