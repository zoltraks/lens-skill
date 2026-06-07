# Project Scorecard

## Purpose

> **Scope:** The 0-5 project scorecard, dimensions, scoring rubric
> **Key items:** fixed dimensions, integer scores, evidence per score, unknown handling

This file defines the comparative project scorecard. It appears in the report under the heading "Project Scorecard". Derive each score from the matching `assessment/` findings.

Apply `principles/evaluation-rules.md` throughout. A score is a summary of evidence, not an impression.

## Table Format

Use this fixed column order and dimension set:

| Dimension          | Score | Evidence | Notes |
|--------------------|-------|----------|-------|
| Testability        | 0-5   |          |       |
| Design Soundness   | 0-5   |          |       |
| Code Quality       | 0-5   |          |       |
| Dependency Health  | 0-5   |          |       |
| Maintainability    | 0-5   |          |       |
| Deployability      | 0-5   |          |       |
| Scalability        | 0-5   |          |       |
| Security           | 0-5   |          |       |
| Compliance         | 0-5   |          |       |
| Observability      | 0-5   |          |       |
| Operational Safety | 0-5   |          |       |

Keep the dimension names and order identical across every audit so scores are comparable.

## Scoring Rubric

Scores are integers from `0` to `5`.

| Score | Meaning                                                                 |
|-------|-------------------------------------------------------------------------|
| 5     | Capability is comprehensive and verified by strong evidence             |
| 4     | Capability is solid with minor gaps                                     |
| 3     | Capability is adequate but uneven                                       |
| 2     | Capability is present but limited or inconsistent                       |
| 1     | Capability is minimal or barely evidenced                               |
| 0     | Capability is absent where required, with evidence of absence           |

## Handling Unknowns

Do not score a dimension `0` when evidence is simply missing.

When evidence is absent, leave the score blank or write `UNKNOWN` and explain in the notes. Reserve `0` for evidenced absence of a required capability.

## Handling Not Applicable

When every source category for a dimension is `N/A`, mark the dimension `N/A` rather than scoring it.

Put the applicability justification in the notes, anchored to the deployment model.

Do not let `N/A` dimensions drag a summary score. A dimension that cannot apply is excluded, not counted as zero. Use `N/A` only under the contextual-applicability rule in `principles/evaluation-rules.md`.

## Dimension To Category Mapping

Each scorecard dimension summarizes one or more assessment categories.

| Dimension          | Source Categories                                   |
|--------------------|-----------------------------------------------------|
| Testability        | Testing and Testability                             |
| Design Soundness   | Design Principles                                   |
| Code Quality       | Code Quality                                        |
| Dependency Health  | Dependencies and Supply Chain                       |
| Maintainability    | Maintainability, Change Management, Documentation   |
| Deployability      | Deployment Strategy, Rollback Strategy              |
| Scalability        | Non-Functional Requirements                         |
| Security           | Security                                            |
| Compliance         | Compliance and Data Protection                      |
| Observability      | Observability                                       |
| Operational Safety | Operational Readiness, Error Handling, Rollback Strategy |

## Rules

- Every score must cite evidence in the evidence column.
- Keep notes neutral and technical.
- Do not average away a critical gap. If a dimension has a critical weakness, the score must reflect it and the notes must name it.
- Scores describe the system, never the people who built it.
