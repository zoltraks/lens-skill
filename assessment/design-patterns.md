# Design Patterns

## Purpose

> **Scope:** Identification of design patterns in use, their fitness for the context, and anti-pattern detection
> **Key items:** GoF catalog (creational, structural, behavioral), POSA, pattern fitness, anti-patterns, inconsistent application

This file guides assessment of which design patterns the code uses and whether they are applied appropriately. It complements `assessment/design-principles.md` (SOLID) and `assessment/maintainability.md` (module structure): this file names the concrete patterns and judges their fitness.

Apply `principles/evaluation-rules.md` throughout. Name patterns from observable code, not from intent. A pattern that fits the stated context is a strength; a pattern applied inconsistently or where it adds no value is an anti-pattern.

## When This Applies

This assessment applies to any codebase large enough to exhibit recurring structure, typically when there is more than one module or more than a handful of types. It is most useful for production-bound systems and architectural reviews.

It may be marked `N/A` for a trivial single-purpose script with no recurring structure, with a one-line justification.

## What To Evaluate

Identify patterns from the Gang of Four (GoF) catalog and POSA where present, across the three categories:

- **Creational**: how objects are created (for example, Factory Method, Builder, Singleton, Dependency Injection container).
- **Structural**: how objects are composed (for example, Adapter, Facade, Repository, Proxy, Decorator).
- **Behavioral**: how objects interact (for example, Strategy, Command, Observer, Template Method, State).

For each pattern in use, assess:

- **Presence**: where the pattern appears, anchored to a file or type.
- **Fitness**: whether the pattern fits the problem and the stated constraints.
- **Consistency**: whether the pattern is applied uniformly or only in some places.
- **Injectability**: for behavioral patterns such as Strategy, whether the variant is injected or hardcoded.

## Evidence To Look For

| Signal | Where It Appears |
|--------|------------------|
| Repository pattern | An interface or trait abstracting a data store, with concrete implementations |
| Strategy pattern | Interchangeable algorithms; check whether selected at runtime or hardcoded |
| Builder / Factory Method | Construction helpers; check whether shared or duplicated across files |
| Command pattern | Encapsulated requests, especially for CLI dispatch or undoable actions |
| Adapter / Facade | Wrappers over third-party libraries or subsystems |
| Anti-patterns | God objects, duplicated construction logic, inconsistent factory application, Strategy with hardcoded weights |

## Common Anti-Patterns

- A construction helper (Factory Method or Builder) duplicated across many files instead of extracted to one place. The duplication is itself an inconsistent application of the pattern.
- A Strategy whose variant is hardcoded rather than injected, removing the flexibility the pattern exists to provide (for example, fixed scoring weights inline instead of configured).
- Ad hoc dispatch where a Command pattern would fit, for example a large match statement routing CLI subcommands without a common command abstraction.
- A god object that concentrates responsibilities a pattern would normally separate.

## Status Criteria

- `PASS`: Patterns in use are appropriate, consistently applied, and fit the stated constraints, with evidence.
- `PARTIAL`: Some patterns fit well but others are applied inconsistently, hardcoded where they should be injected, or duplicated.
- `FAIL`: Patterns are misapplied or anti-patterns dominate where the scale clearly calls for structure, with evidence.
- `UNKNOWN`: Source was not provided in enough depth to identify patterns.
- `N/A`: The codebase is too trivial to exhibit recurring structure, with justification.

## How To Present

Render this as a subsection of the Architectural Assessment, as described in `process/report-format.md`. Present a table of patterns with their fitness verdict, then describe each material pattern or anti-pattern with evidence.

Where an anti-pattern is also a code-origin signal (for example, a construction helper duplicated by an AI tool across files), cross-reference the relevant `FND-AIP-XXX` finding.

## Rules

- Name the pattern using its standard catalog name (GoF or POSA). Do not invent names.
- Anchor every pattern to a concrete file or type.
- A pattern that fits the stated context is a strength, not a weakness, even if unusual elsewhere.
- Flag a pattern as an anti-pattern only when its application is inconsistent, redundant, or removes the value the pattern exists to provide.
