# Structure Review

## Purpose

> **Scope:** Physical organization of directories, files, source code components, code
> division, and in-code identifier naming
> **Key items:** per-component evaluation, directory hierarchy, file naming, language-idiomatic
> code division, class/method/variable naming, supporting-artifact placement, fallback for
> unlisted stacks

This file guides assessment of how a project organizes its directories, files, source code
components, code division, and identifier naming.

Apply `principles/evaluation-rules.md` throughout.

Evaluate the structure against the project's actual language, framework, application type,
architecture, and scale - never against a universal directory template.

## Boundary

This assessment owns physical organization and naming: directory layout, file and component
placement, language-idiomatic code division across files, directory/file/identifier naming
conventions, and supporting-artifact placement.

Logical modularity, coupling, dependency direction, and technical-debt signals belong to
`assessment/maintainability-review.md`.

Code-level runtime idioms and API usage patterns belong to `assessment/best-practices.md` -
this file consumes ecosystem layout and naming conventions from
`references/naming-and-layout.md`, `references/stack-standards.md`, and the per-stack digests,
it does not re-derive them.

Logical architecture decisions belong to the Architectural Assessment - a misplaced component
is a structural finding, a poorly chosen architecture is not.

## Context First

Before judging the structure, establish from intake and inspection for each component
independently:

- Component boundary and purpose (`library`, `service`, `application`, `cli`, `test-suite`,
  `documentation`, or `agent-package`) per `references/domain-profiles.md` and
  `references/naming-and-layout.md` -
  different layout and naming rules govern libraries, applications, services, and
  documentation trees.
- Programming language(s) and framework, when applicable, and the authoritative naming and
  layout sources from `references/naming-and-layout.md`, `references/stack-standards.md`, and
  `references/source-catalog.md`.
- Architectural approach - layered, feature-based, modular monolith, plugin, or none apparent.
- Project scale and the build and deployment model where they shape layout.

Do not assume a framework or a formally defined architecture.

For a collection or container subject, each held member is a project of its own: member
internals are assessed inside the member's own project block, and the collection-root
project's structure verdicts judge the collection layout - the index, member directories, and
governance files - against the agent-package conventions in `references/agent-skills.md` and
`references/agent-configuration.md`.

When a component uses a language, framework, or documentation format not pre-cataloged in the
skill, follow the fallback order in `references/naming-and-layout.md`: project-declared
standards first, then standard-library and official toolchain rules, live official
documentation when permitted, and internal consistency across the component itself.

## What To Evaluate

Audit each component independently across the three structural and naming pillars:

- **Organization of code into directories**:
  - Nesting depth, redundancy, and separation of source, tests, configuration, documentation,
    resources, generated files, and build artifacts according to the component's purpose
    (`library` public-surface isolation vs `service` transport/domain/persistence separation vs
    `application`/`cli` thin composition root).
  - Directory naming discipline: full words versus arbitrary abbreviations (such as `App`
    instead of `Application`, `Config` instead of `Configuration`, `Auth` instead of
    `Authentication`, or `Docs` instead of `Documentation` in ecosystems that prescribe full
    words), singular versus plural consistency across peer folders, and directory-to-namespace
    or directory-to-package alignment.
  - Absence of catch-all directories (`Misc`, `Util`, `Utils`, `Common`, `Helpers`) that mix
    unrelated responsibilities.
- **Naming and language-idiomatic division of source code files**:
  - File naming casing (`PascalCase.cs`/`.java`/`.php`, `snake_case.py`/`.rs`/`.go`/`.cpp`,
    `kebab-case.js`/`.ts`, dotted `Namespace.Unit.pas` in Delphi, lowercase `unit.pas` in Free
    Pascal) and test-file naming parity (`test_*.py`, `*Test.java`, `*Tests.cs`, `*_test.go`,
    `*.test.ts`, `*Test.php`, `*_test.cpp`).
  - Code division according to practices natural for the language: one public top-level type per
    file in Java, C#, and PHP PSR-4 versus cohesive multi-symbol modules in Python, Go, and
    Rust, `include/<pkg>/*.hpp` header versus `src/*.cpp` source split in C++20, and
    `interface` versus `implementation` sections in Pascal units.
  - Separation of abstractions from implementations: Java interfaces (`OrderService`,
    `OrderRepository`) and concrete implementations (`DefaultOrderService`,
    `JpaOrderRepository`), C# `I`-prefixed interfaces (`IOrderService`, `IRevocationStore`),
    abstract base classes, and concrete or null-object classes (`NullRevocationStore`) in
    separate files, Go consumer-defined interfaces, and Python `Protocol`/`ABC` contracts.
- **Naming of classes, methods, fields, constants, and variables within the code**:
  - Adherence to stack casing and prefix rules for packages/namespaces, classes/records/enums,
    interfaces/traits/protocols, methods/functions, local variables/parameters, private fields,
    and constants/enum members per `references/naming-and-layout.md`.
  - Absence of cross-language naming holdovers (for example Delphi enum prefixes such as
    `psNew`, type-letter method suffixes such as `ValueI`/`ValueB`, or BCL type names `Boolean`
    instead of C# `bool` in a C# port, or C#-style `I` prefixes on TypeScript/Java interfaces).
  - Role-suffix accuracy and consistency across peer components (for example mixing
    `*Controller`, `*Handler`, and `*Endpoints` on Minimal API static endpoint classes that do
    not inherit from `ControllerBase`).
- **Supporting artifacts and overall consistency**:
  - Placement of application and environment configuration, build and dependency files, CI/CD
    definitions, containerization, scripts, fixtures, templates, migrations, and generated
    output - locatable, separated, and consistent with the build and deployment workflow.
  - Absence of competing organizational models without justification, duplicate structures, or
    ambiguous ownership of shared functionality.

Cite the consulted authoritative naming and layout standards in `Auditing Methodology`, render
the detailed component-by-component matrices in `Naming And Layout Conformance`, and include
links to the authoritative sources in `References` so readers can retrieve the governing rules.

## Evidence To Look For

| Signal                 | Where It Appears                                                                |
|------------------------|---------------------------------------------------------------------------------|
| Tree census            | `git ls-files` grouping by top levels, depth and fan-out counts                 |
| Component role map     | Manifests, entry points, and exported surfaces per component (`src/*`, `tests`) |
| Directory naming drift | Truncated folder names (`App`, `Config`, `Auth`), mixed singular/plural folders |
| Multi-type files       | Single `.cs`/`.java`/`.php` files declaring multiple public top-level types     |
| In-code naming census  | Type, interface, method, field, parameter, constant, and enum-member patterns   |
| Ported-idiom holdovers | Foreign prefixes/suffixes (`psNew`, `ValueI`, `IOrderRepo` in TS/Java)          |
| Missing baseline files | Expected stack files (`LICENSE`, `README`, lockfile, CI config) absent          |
| Registration drift     | Files on disk missing from manifests, index files, or build definitions         |
| Catch-all directories  | `util`, `common`, `misc` directories or classes holding unrelated logic         |
| Misplaced artifacts    | Tests beside source, generated code under source roots, config scattered        |
| Structural duplication | Parallel directory trees serving no distinct purpose                            |

Count what the census counts and record the method beside the figure, per
`references/census-commands.md`, so a re-audit reproduces the number.

`scripts/scan-structure.py` produces the deterministic tree census - file classes and per-area
counts - and `references/organization-model.md` turns it into the area map and responsibility
inventory this assessment's placement, catch-all, and ownership judgments cite.

## Convention Tiers

Classify every judgment before reporting it:

- **Required** - imposed by the language, framework, build system, platform, or explicit
  project standards, and a deviation is a defect.
- **Established** - a consistent pattern the project already follows, while an unexplained break is
  a consistency finding.
- **Recommended** - a common practice that would improve clarity, and a deviation is an
  improvement opportunity, not a violation.
- **Context-dependent** - a choice that cannot be judged without project requirements, so report
  it neutrally or not at all.

A coherent deviation from a preferred convention is not a defect.

## Status Criteria

- `PASS`: A coherent organizational model is followed consistently, placement and naming match
  required and established conventions, and artifacts are locatable, with evidence.
- `PARTIAL`: A mostly coherent structure with localized inconsistencies, misplaced components,
  or unexplained competing patterns.
- `FAIL`: No discernible organizational principle, pervasive fragmentation or ambiguity that
  obscures responsibilities, with evidence.
- `UNKNOWN`: The source tree was not provided for inspection.
- `N/A`: The subject carries no source tree, for example a document-only proposal.

## Common Risks

- Fragmented organization raises the cost of every change and slows onboarding.
- Catch-all directories hide responsibilities and accumulate coupling.
- Competing organizational models make component location a guessing game.
- Structure that fights framework conventions breaks tooling expectations.
- Legacy layout conflicting with the current architecture misleads new work.

## What Raises Confidence

- A single coherent organizational principle applied consistently.
- Clear separation of source, tests, configuration, documentation, and generated output.
- Names that communicate responsibility and follow stack conventions.
- Deliberate deviations that are documented or self-evidently purposeful.
- Supporting artifacts placed where tooling and convention expect them.

Mark each missing signal explicitly rather than inferring its presence.

Distinguish a structural problem from an implementation-level problem: a component can be
poorly implemented yet correctly placed, and well-written code can sit in an unsuitable module.

Never recommend relocating files whose current location is required by tooling, deployment
conventions, or framework behavior, and never report personal preference as an objective
violation.
