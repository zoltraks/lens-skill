# Stack Best Practices

## Purpose

> **Scope:** Idiomatic use of the chosen languages, frameworks, runtimes, and libraries; stack-specific conventions and anti-patterns
> **Key items:** language idioms, framework conventions, ecosystem layout, official style guides, recommended libraries, deprecated APIs, version-appropriate patterns

This file guides assessment of how closely the code follows the documented best practices and idioms of its own technology stack.

Apply `principles/evaluation-rules.md` throughout. Judge adherence to the conventions of the stack the subject already uses. Do not penalize the stack choice itself or compare it against a preferred stack, per the architectural-neutrality rule. Generic, language-agnostic design principles are assessed in `assessment/design-principles.md`; code-level metrics such as linting and complexity in `assessment/code-quality.md`; this file covers stack-specific convention.

## What To Evaluate

- Language idioms: whether the code uses the language's standard constructs rather than patterns ported from another language.
- Framework conventions: whether the code follows the framework's prescribed structure, lifecycle, data flow, and extension points.
- Ecosystem layout: whether project structure and file naming match the ecosystem's accepted conventions.
- Stack style guide: whether an official or community style guide and the ecosystem-standard tooling are adopted.
- Recommended libraries: whether the stack's established libraries are used instead of reimplementing solved problems.
- Deprecated APIs: whether deprecated or discouraged APIs of the language, framework, or libraries are avoided.
- Version-appropriate patterns: whether the code uses the patterns the installed stack version offers rather than outdated ones it has superseded.
- Stack anti-patterns: whether anti-patterns known to the specific stack are absent.

## Evidence To Look For

| Signal                       | Where It Appears                                             |
|------------------------------|--------------------------------------------------------------|
| Idiomatic language use       | Native constructs and idioms over ported patterns            |
| Framework conventions        | Prescribed layout, lifecycle hooks, official APIs            |
| Ecosystem layout             | Conventional project structure and file naming               |
| Stack style guide            | Adopted style guide, ecosystem-standard tooling config       |
| Recommended libraries        | Established ecosystem libraries over hand-rolled equivalents |
| Deprecated APIs              | Absence of calls the stack flags as deprecated               |
| Version-appropriate patterns | Features matching the installed runtime or framework version |


## Status Criteria

- `PASS`: The code consistently follows the documented idioms and conventions of its stack, with evidence across representative areas.
- `PARTIAL`: Conventions are followed in places but violated in others, such as foreign idioms, off-pattern framework use, or deprecated APIs.
- `FAIL`: The code broadly ignores the stack's established conventions where they clearly apply, with evidence.
- `UNKNOWN`: The stack could not be identified, or source was not provided in enough depth to judge convention.

## Common Risks

- Foreign idioms make the code harder for stack-experienced maintainers to read and review.
- Off-pattern framework use forfeits framework guarantees and complicates upgrades.
- Non-standard project layout slows onboarding and breaks tooling that expects conventions.
- Hand-rolled replacements for standard libraries carry defects the established library has already solved.
- Deprecated APIs are removed in later versions, blocking upgrades and creating future breakage.
- Outdated patterns miss safety and clarity improvements the current stack version provides.

## What Raises Confidence

- Code that reads as idiomatic to an experienced practitioner of the stack.
- Framework features used as the framework intends, through its documented extension points.
- Project layout and naming that follow the ecosystem's conventions.
- An adopted, enforced stack style guide and standard tooling.
- Established libraries used for solved problems, with no deprecated APIs in active paths.

Mark each missing signal explicitly rather than inferring its presence. Anchor every judgement to the stack's own documented convention, not to a preferred alternative stack.
