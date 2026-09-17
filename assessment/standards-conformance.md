# Standards Conformance

## Purpose

> **Scope:** Project-internal development standards and their conformance with the codebase, plus the quality of the standards themselves against external best practices
> **Key items:** standards discovery, code-to-standards conformance, standards-to-best-practices quality, external references

This file guides assessment of whether the project documents its own development standards and whether the codebase conforms to them. It also evaluates whether the documented standards are themselves consistent with good practices for the technology stack, programming language, and software type.

Apply `principles/evaluation-rules.md` throughout. This assessment is conditional: it applies only when the project contains documented development standards that its documentation indicates should be followed. When no such documents exist, omit this category and note the omission in Scope Exclusions.

## What To Evaluate

- **Standards discovery**: whether the project contains development standard documents that prescribe how source code should be written, which frameworks to use, which library functions are preferred, naming conventions, project structure, or technology-stack rules.
- **Standards scope**: whether the standards cover the relevant dimensions for the stack: language version, project structure, naming conventions, error handling, testing, formatting and linting, dependency management, build, comments, and security considerations.
- **Code conformance**: whether the codebase follows the documented standards across the areas the standards cover.
- **Standards quality**: whether the documented standards are themselves consistent with the established good practices for the technology stack, programming language, and software type (browser application, web service, desktop application, console tool, library, embedded firmware, and so on).
- **Standards currency**: whether the standards reference current versions of the language, framework, and tooling, or whether they are stale relative to the versions the project actually uses.
- **Enforcement**: whether the standards are enforced through tooling (linters, formatters, CI checks) or exist only as documentation that drifts from practice.

## Evidence To Look For

| Signal                       | Where It Appears                                                     |
|------------------------------|----------------------------------------------------------------------|
| Standards documents          | `docs/standard/`, `docs/guidelines/`, `STANDARDS.md`, or similar     |
| Standards references         | `README.md`, `AGENTS.md`, `docs/GUIDELINES.md` pointing to standards |
| Language version rules       | Standards file naming the required language or runtime version       |
| Project structure rules      | Standards file prescribing directory layout and file naming          |
| Naming convention rules      | Standards file prescribing code and file naming patterns             |
| Error handling rules         | Standards file prescribing error handling patterns                   |
| Testing rules                | Standards file prescribing test framework and coverage               |
| Formatting and linting rules | Standards file prescribing formatters, linters, and CI checks        |
| Tooling enforcement          | CI config, pre-commit hooks, editor config matching the standards    |
| Code conformance             | Source files matching or diverging from the documented rules         |

## Status Criteria

- `PASS`: The project documents development standards, the codebase conforms to them across the covered areas, and the standards are themselves consistent with established good practices for the stack.
- `PARTIAL`: Standards exist but conformance is uneven, or the standards are partly inconsistent with good practices for the stack, or enforcement is missing in areas the standards cover.
- `FAIL`: Standards exist and are referenced as authoritative, but the codebase broadly ignores them, or the standards contradict established good practices for the stack in material ways.
- `UNKNOWN`: Standards are referenced but were not provided, or the codebase was not inspected in enough depth to judge conformance.
- `N/A`: The project contains no documented development standards. Omit this category and note the omission in Scope Exclusions.

## Common Risks

- Documented standards that the codebase ignores create a false sense of quality and make review harder, because reviewers check against rules the code does not follow.
- Standards that contradict established good practices for the stack push the codebase toward patterns that experienced practitioners would flag as anti-patterns.
- Stale standards that reference older language or framework versions block adoption of safer or clearer patterns the current version offers.
- Standards without tooling enforcement drift from practice over time, because nothing catches deviations.
- Standards that cover only some areas leave the rest to convention, which fragments as the team grows.
- Missing standards in a multi-project repository let each project invent its own conventions, increasing cross-project review cost.

## What Raises Confidence

- Standards documents that cover the dimensions relevant to the stack and software type.
- Code that consistently follows the documented rules across representative files.
- Standards that align with established good practices for the language, framework, and software type.
- Tooling that enforces the standards in CI or pre-commit, so conformance is verified automatically.
- Standards kept current with the language and framework versions the project actually uses.
- Standards referenced from `README.md` or `AGENTS.md` so they are discoverable and treated as authoritative.

Mark each missing signal explicitly rather than inferring its presence. Anchor every conformance judgement to a specific rule in the standards document and a specific file or pattern in the codebase. Anchor every standards-quality judgement to a named external best practice, style guide, or convention for the stack.

## Requirement Interpretation

Quote or closely paraphrase the actual rule and record whether it is mandatory, recommended,
optional, or conditional before judging conformance.

Honor alternatives and scope, for example "thiserror or manual errors where needed" does not
require a particular dependency in every module.

Verify process requirements using process evidence, not unrelated source-code properties.

Documentation-before-code needs change history or review evidence, not a count of doc comments.

Keep standards-quality analysis separate from implementation analysis.

A standards document that is silent on authorization does not prescribe broken authorization.

Record that silence as a coverage gap where relevant, and assess the implementation separately.

An external best practice supports advice unless it was adopted as a requirement or implements a
necessary security invariant.

## External References

When this assessment is included, collect every external source referenced during the standards-quality evaluation. Examples include official language style guides, framework conventions documentation, ecosystem best-practice guides, and standards documents for the software type. `references/stack-standards.md` provides the canonical starting set per detected stack. These references appear in the References section at the end of the audit report, per `process/report-format.md`.

Record each reference with its title, publisher or author, and URL when available. Do not invent references. Only list sources actually consulted during the assessment.
