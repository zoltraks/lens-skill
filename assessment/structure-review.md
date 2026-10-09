# Structure Review

## Purpose

> **Scope:** Physical organization of directories, files, source code components, and
> supporting artifacts
> **Key items:** directory hierarchy, naming conventions, component placement, artifact
> placement, stack conventions, organizational consistency

This file guides assessment of how a project organizes its directories, files, source code
components, and supporting artifacts.

Apply `principles/evaluation-rules.md` throughout.

Evaluate the structure against the project's actual language, framework, application type,
architecture, and scale - never against a universal directory template.

## Boundary

This assessment owns physical organization: directory layout, file and component placement,
naming patterns, and supporting-artifact placement.

Logical modularity, coupling, dependency direction, and technical-debt signals belong to
`assessment/maintainability-review.md`.

Code-level idioms and framework usage patterns belong to `assessment/best-practices.md` -
this file consumes ecosystem layout conventions from `references/stack-standards.md` and the
per-stack digests, it does not re-derive them.

Logical architecture decisions belong to the Architectural Assessment - a misplaced component
is a structural finding, a poorly chosen architecture is not.

## Context First

Before judging the structure, establish from intake and inspection:

- Programming language(s) and framework, when applicable.
- Application type - service, web application, library, CLI tool, worker, mobile or desktop
  application.
- Architectural approach - layered, feature-based, modular monolith, plugin, or none apparent.
- Project scale and the build and deployment model where they shape layout.

Do not assume a framework or a formally defined architecture.

## What To Evaluate

- Directory hierarchy: nesting depth, redundancy, and separation of source, tests,
  configuration, documentation, resources, generated files, and build artifacts.
- Organizational principle: grouping by technical responsibility, feature, or domain, applied
  coherently - and consistency of that principle across the project.
- Component placement: where interfaces, implementations, models, services, controllers,
  repositories, adapters, converters, and utilities live, where such roles exist.
- Modules and packages: appropriate use of namespaces and subprojects, cohesion within each,
  and clear boundaries between layers or domains.
- Discoverability: whether entry points and important functionality are easy to locate, and
  whether catch-all directories or ambiguous locations hide them.
- Naming: consistent patterns for equivalent elements, singular/plural discipline,
  abbreviation discipline, interface-versus-implementation distinction, and names that
  communicate responsibility rather than incidental detail.
- Supporting artifacts: placement of application and environment configuration, build and
  dependency files, CI/CD definitions, containerization, scripts, fixtures, templates,
  migrations, and generated output - locatable, separated, and consistent with the build and
  deployment workflow.
- Consistency and maintainability: competing organizational models without justification,
  duplicate structures, ambiguous ownership of shared functionality, and structural complexity
  that raises the cost of change.

## Evidence To Look For

| Signal                 | Where It Appears                                                         |
|------------------------|--------------------------------------------------------------------------|
| Tree census            | `git ls-files` grouping by top levels, depth and fan-out counts          |
| Missing baseline files | Expected stack files (`LICENSE`, `README`, lockfile, CI config) absent   |
| Registration drift     | Files on disk missing from manifests, index files, or build definitions  |
| Naming census          | Equivalent directories or files named by competing patterns              |
| Catch-all directories  | `util`, `common`, `misc` directories holding unrelated responsibilities  |
| Misplaced artifacts    | Tests beside source, generated code under source roots, config scattered |
| Structural duplication | Parallel directory trees serving no distinct purpose                     |

Count what the census counts and record the method beside the figure, per
`references/census-commands.md`, so a re-audit reproduces the number.

## Convention Tiers

Classify every judgment before reporting it:

- **Required** - imposed by the language, framework, build system, platform, or explicit
  project standards; a deviation is a defect.
- **Established** - a consistent pattern the project already follows; an unexplained break is
  a consistency finding.
- **Recommended** - a common practice that would improve clarity; a deviation is an
  improvement opportunity, not a violation.
- **Context-dependent** - a choice that cannot be judged without project requirements; report
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
