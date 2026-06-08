# Project Scorecard

## Purpose

> **Scope:** The 1-10 project scorecard, dimensions, scoring rubric, with an optional 1-5 scale
> **Key items:** fixed dimensions, integer scores, evidence per score, unknown handling

This file defines the comparative project scorecard. It appears in the report under the heading "Project Scorecard". Derive each score from the matching `assessment/` findings.

Apply `principles/evaluation-rules.md` throughout. A score is a summary of evidence, not an impression.

## Table Format

Use this fixed column order and dimension set:

| Dimension          | Score | Notes |
|--------------------|-------|-------|
| Testability        |       |       |
| Design Soundness   |       |       |
| Code Quality       |       |       |
| Stack Alignment    |       |       |
| Dependency Health  |       |       |
| Maintainability    |       |       |
| Deployability      |       |       |
| Scalability        |       |       |
| Security           |       |       |
| Compliance         |       |       |
| Observability      |       |       |
| Operational Safety |       |       |

Keep the dimension names and order identical across every audit so scores are comparable.

## Scoring Rubric

The default scale is integers from `1` to `10`. When the user explicitly requests a `1-5` scale, use the Alternative Rubric below.

**Zero is not a score.** The value `0` is reserved and never used as a rated score in either scale. When a dimension cannot apply, mark it `N/A` rather than assigning a numeric value.

| Score | Meaning                                                                 |
|-------|-------------------------------------------------------------------------|
| 10    | Capability is comprehensive and verified by strong evidence             |
| 9     | Capability is nearly comprehensive, with only trivial gaps            |
| 8     | Capability is solid with minor gaps                                     |
| 7     | Capability is good overall, with some noticeable gaps                   |
| 6     | Capability is adequate but uneven                                       |
| 5     | Capability is present but limited or inconsistent                       |
| 4     | Capability is present but significantly limited                         |
| 3     | Capability is minimal or barely evidenced                               |
| 2     | Fragments present, mostly unevidenced                                   |
| 1     | Capability is absent where required, with evidence of absence           |

### Alternative Rubric (1-5)

Use this scale only when explicitly requested.

| Score | Meaning                                                                 |
|-------|-------------------------------------------------------------------------|
| 5     | Capability is comprehensive and verified by strong evidence             |
| 4     | Capability is solid with minor gaps                                     |
| 3     | Capability is adequate but uneven                                       |
| 2     | Capability is present but limited or inconsistent                       |
| 1     | Capability is absent where required, with evidence of absence           |

## Handling Unknowns

Do not assign the minimum score when evidence is simply missing.

When evidence is absent, leave the score blank or write `UNKNOWN` and explain in the notes. Reserve the minimum score for evidenced absence of a required capability.

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
| Stack Alignment    | Stack Best Practices                                |
| Dependency Health  | Dependencies and Supply Chain                       |
| Maintainability    | Maintainability, Change Management, Documentation   |
| Deployability      | Deployment Strategy, Rollback Strategy              |
| Scalability        | Non-Functional Requirements                         |
| Security           | Security                                            |
| Compliance         | Compliance and Data Protection                      |
| Observability      | Observability                                       |
| Operational Safety | Operational Readiness, Error Handling, Rollback Strategy |

## Rules

- Every score must cite evidence in the detailed paragraph body.
- Keep notes neutral and technical.
- Do not average away a critical gap. If a dimension has a critical weakness, the score must reflect it and the notes must name it.
- Scores describe the system, never the people who built it.
