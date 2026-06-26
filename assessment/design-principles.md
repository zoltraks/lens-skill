# Design Principles

## Purpose

> **Scope:** SOLID principles, cohesion and coupling, DRY, separation of concerns
> **Key items:** SRP, OCP, LSP, ISP, DIP, high cohesion, low coupling, no needless duplication

This file guides assessment of object and module design quality against established design principles.

Apply `principles/evaluation-rules.md` throughout. Assess observable design properties from the code, not intent. Architectural module boundaries are assessed in `assessment/maintainability.md`; code-level metrics in `assessment/code-quality.md`; this file covers design principles.

## What To Evaluate

Evaluate each SOLID principle as an observable property of the code:

- Single Responsibility (SRP): each unit has one reason to change; classes and modules are not catch-alls.
- Open/Closed (OCP): behavior can be extended without modifying existing, tested code, typically via abstraction.
- Liskov Substitution (LSP): subtypes are usable wherever their base type is expected without surprising behavior.
- Interface Segregation (ISP): clients depend on narrow interfaces, not large ones with unused members.
- Dependency Inversion (DIP): high-level modules depend on abstractions, not on concrete low-level details.

Also evaluate the companion principles:

- Cohesion: related behavior is grouped; a unit's members serve one purpose.
- Coupling: units depend on each other minimally and through stable contracts.
- DRY: knowledge is represented once, without harmful duplication.
- Separation of concerns: distinct concerns live in distinct units rather than being intertwined.

## Evidence To Look For

| Signal                | Where It Appears                                              |
|-----------------------|---------------------------------------------------------------|
| SRP                   | Focused classes and modules; absence of god objects           |
| OCP                   | Extension via interfaces, strategies, or plugins              |
| LSP                   | Subtypes honoring base contracts; no type-checking branches   |
| ISP                   | Small, role-specific interfaces                               |
| DIP                   | Dependencies injected as abstractions, not constructed inline |
| Cohesion and coupling | Module imports, dependency direction, fan-out                 |
| DRY                   | Shared helpers instead of repeated logic                      |

## Status Criteria

- `PASS`: The design consistently follows SOLID and the companion principles, with evidence across representative units.
- `PARTIAL`: Principles are followed in places but violated in others, such as god objects, concrete dependencies, or duplication.
- `FAIL`: The design broadly violates these principles where the scale clearly calls for them, with evidence.
- `UNKNOWN`: Source was not provided in enough depth to judge design.

## Common Risks

- SRP violations create god objects that are hard to change and test.
- Missing OCP forces edits to tested code for every extension, raising regression risk.
- LSP violations cause surprising behavior when subtypes are substituted.
- Fat interfaces (ISP) couple clients to methods they do not use.
- Concrete dependencies (DIP) block substitution and unit testing in isolation.
- High coupling and duplication multiply the cost and risk of change.

## What Raises Confidence

- Focused units with a single clear responsibility.
- Extension points expressed through abstractions rather than edits to core code.
- Dependencies injected as interfaces, supporting both DIP and testability.
- Narrow, role-specific interfaces and minimal cross-module coupling.
- Shared abstractions in place of repeated logic.

Mark each missing signal explicitly rather than inferring its presence. Judge each principle separately; a design can satisfy some and violate others, which the notes should make clear.
