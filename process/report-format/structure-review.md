# Structure Review Format

## Purpose

> **Scope:** The Structure Review section, structure findings in review-style reports, and
> the structure-review variant contract
> **Key items:** section layout, verdict table, `FND-STR-` pillar, variant section order

This file defines how structure assessment output renders: as a baseline section in
`audit`-style reports, as findings inside `review`-style reports, and as a standalone
structure-scoped variant of the `review` style.

The analysis itself is governed by `assessment/structure-review.md`.

## Structure Review Section

The `audit` style carries a `Structure Review` section immediately after
`Architectural Assessment` and before `Trade-off Analysis`.

Structure the section with these elements, in order:

1. **Context line** - one sentence naming the stack, application type, architectural approach,
   and scale signal the verdicts were judged against, referencing Document Information and
   System Context rather than restating them.
2. **Structural overview** - a compact description of the existing directory, file, and
   component organization, plus a component-inventory table when the tree is large.

   | Level | Directory | Contents | Role |
   |-------|-----------|----------|------|
   | `1`   | ...       | ...      | ...  |

3. **Verdict table** - one row per evaluation area, with a status token and evidence basis.

   | Area                        | Verdict | Basis |
   |-----------------------------|---------|-------|
   | Directory organization      |         |       |
   | Naming conventions          |         |       |
   | Component placement         |         |       |
   | Supporting-artifact layout  |         |       |
   | Consistency                 |         |       |

   Verdict cells carry `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or `N/A`, and the Basis cell names
   the convention tier per `assessment/structure-review.md` - required, established,
   recommended, or context-dependent.
4. **Finding summary** - `FND-STR-` rows inline or cross-referenced to Detailed Technical
   Findings.
5. **Positive practices** - organizational decisions worth preserving, each with evidence.
6. **Recommendations pointer** - the structural recommendations land in the Actionable
   Remediation Roadmap like any other finding resolution; this element names the `REC-XXX`
   identifiers that resolve them.
7. **Limitations** - areas that could not be evaluated and assumptions the verdicts rest on.

On a subject carrying no source tree - a document-only proposal - the section stays present
with each verdict marked `N/A` and the justification stated, never silently omitted.

In a multi-project report the section renders once per project block, per
`process/report-format/multi-project.md`.

## Structure Findings In Review-Style Reports

The `review` style has no Structure Review section.

Structure findings render inside Domain Findings under the `### Maintainability` domain,
carrying `FND-STR-` identifiers and the standard finding block schema with the `Evidence
level` field per `process/report-format/findings-registers.md`.

A `hunt` report never loads the structure assessment and never renders `FND-STR-` findings.

## Structure Review Variant

A `review`-style request scoped to the project structure - wording such as "make a structure
review" or "review the project structure" - renders a dedicated report instead of the
execution-register contract.

The variant carries exactly these top-level sections, in order:

1. `Document Information` - per `process/report-format/report-opening.md`, including
   `Report Style: review` and a `Review Scope: Structure` row.
2. `Project Context` - language, framework, application type, architectural approach, scale,
   and build/deployment model as established at intake, plus the constraints the structure
   must satisfy.
3. `Structural Overview` - a concise description of the existing directory, file, and
   component organization, with the component-inventory table.
4. `Findings` - `FND-STR-` finding blocks per the shared schema, each naming the affected
   location, the observed condition, the applicable convention tier and criterion, the impact
   on maintainability or discoverability, and a recommendation where justified.
5. `Positive Practices` - organizational decisions that are consistent, effective, or worth
   preserving, each with evidence.
6. `Recommendations` - specific, proportionate changes with rationale, tied to findings.
7. `Prioritization` - each recommendation classified as `Necessary`, `Meaningful`, or
   `Optional` - corrections, improvements, and refinements respectively.
8. `Limitations and Assumptions` - areas that could not be evaluated and conclusions that
   depend on unverified assumptions.

Unnumbered headings, `##` sections only, tables per the Formatting Rules in
`process/report-format.md`.

The variant ends after Limitations and Assumptions - it carries no scorecard, risk register,
roadmap, validation record, or glossary, and no closing line follows the last section.

The variant uses the `REVIEW` filename family with the same bare-stem-first default and
revision rules as the full-scope contract.

It baselines only against prior `REVIEW`-family files carrying the same
`Review Scope: Structure` row, per `synthesis/report-comparison.md`.
