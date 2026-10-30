# Requirements Conformance

## Purpose

> **Scope:** Conformance of the codebase with the subject's declared product requirements
> and acceptance criteria
> **Key items:** requirements inventory, per-requirement grading, spec-to-code
> traceability, unmet-requirement findings

This file guides assessment of whether the product does what its own requirements document
says it must do.

Apply `principles/evaluation-rules.md` throughout.

This assessment is conditional: it applies only when the subject carries a document that
declares product requirements or acceptance criteria.

When no such document exists, omit this category and note the omission in Scope Exclusions.

## When This Applies

The inclusion criterion is a document that declares what the product must do: a
`PROJECT.md`, a product requirements document, a specification, or a user-story
acceptance list.

Neighboring assessments cover different contract kinds:

- `assessment/standards-conformance.md` measures development standards - rules about how
  code is written, not what the product does.
- Documented-Claim Verification in `assessment/documentation-review.md` measures
  quantitative documentation drift - counts, commands, and paths that disagree with the
  repository.
- `assessment/api-contract.md` measures interface contracts - the shapes a system promises
  its consumers.

A requirements document is none of these: it declares product behavior, and this
assessment grades each declared behavior against the code and configuration that should
deliver it.

## What To Evaluate

- **Requirements inventory**: list the requirements and acceptance-criteria documents
  found in the subject, and enumerate every stated requirement and acceptance criterion
  in them, each with its spec location.
- **Per-requirement grading**: evaluate each requirement against code and configuration
  evidence and grade it `Pass`, `Partial`, `Fail`, or `Unknown`.
- **Unmet requirements**: every `Partial` or `Fail` requirement produces a `FND-XXX`
  finding that cites the spec location and the code or configuration evidence that fails
  to satisfy it.
- **Spec quality**: requirement statements that are untestable, contradictory, or stale
  relative to the product the code implements.

## Evidence To Look For

| Signal                 | Where It Appears                                                      |
|------------------------|-----------------------------------------------------------------------|
| Requirements documents | `PROJECT.md`, `PRD.md`, `docs/requirements/`, spec files, story lists |
| Acceptance criteria    | Story cards, issue templates, spec sections with checkable conditions |
| Requirement anchors    | Section numbers, story IDs, or quoted clauses in the requirements doc |
| Implementation proof   | Code paths, configuration, and tests that satisfy each requirement    |
| Counter-evidence       | Code paths, configuration, or stubs that contradict a requirement     |

## Status Criteria

- `PASS`: Every applicable stated requirement is satisfied by code or configuration
  evidence, and no graded requirement fails.
- `PARTIAL`: Some requirements pass but others are partially met, unmet, or unverifiable
  from the evidence.
- `FAIL`: Material requirements the document declares are unmet by the implementation,
  with evidence.
- `UNKNOWN`: Requirements exist but the implementation was not inspected deeply enough to
  grade them.
- `N/A`: The subject carries no requirements or acceptance-criteria document. Omit this
  category and note the omission in Scope Exclusions.

## Requirement Interpretation

Anchor every grade to a specific clause in the requirements document and a specific file
or pattern in the codebase.

Quote or closely paraphrase the clause and record whether the document marks it mandatory,
recommended, optional, or future before judging conformance.

Missing evidence grades `Unknown`, never `Pass` - a requirement is not satisfied because
nothing contradicts it.

Requirements the spec itself marks future, optional, or out of scope stay out of the
denominator and are disclosed, not graded.

A requirement that names a mechanism is met only by that mechanism or a documented
equivalent - "shall log access" is not met by a logging dependency nothing calls.

Grade the product, not the spec: an untestable or self-contradictory clause is a
spec-quality finding, and its requirement grade is `Unknown`.

## How To Present

Render this as a standalone section, as described in
`process/report-format/conditional-conformance.md`, only when the subject carries a
requirements or acceptance-criteria document.

Present a conformance table across the enumerated requirements - one row per requirement
with its spec location, grade, and evidence - then describe each unmet or partial
requirement with its linked `FND-XXX`.

## Rules

- Anchor every grade to a spec location and to code or configuration evidence.
- Missing evidence grades `Unknown`, never `Pass`.
- Requirements the spec marks future or optional stay out of the denominator.
- Every `Partial` or `Fail` requirement produces a `FND-XXX` finding citing both sides.
- Do not grade unstated expectations - a requirement the document never declares is a
  standards or baseline question, not a requirements failure.
