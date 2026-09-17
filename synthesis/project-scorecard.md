# Project Scorecard

## Purpose

> **Scope:** The 1-10 project scorecard, dimensions, scoring rubric, with optional 1-5, 1-3, and
> star-bar scales
> **Key items:** fixed dimensions, integer scores, star bars, evidence per score, unknown handling

This file defines the comparative project scorecard. It appears in the report under the heading
"Project Scorecard". Derive each score from the matching `assessment/` findings.

Apply `principles/evaluation-rules.md` throughout. A score is a summary of evidence, not an
impression.

## Table Format

Use this fixed column order and dimension set:

| Dimension               | Score | Notes |
|-------------------------|-------|-------|
| Testability             |       |       |
| Design Soundness        |       |       |
| Code Quality            |       |       |
| Stack Alignment         |       |       |
| Dependency Health       |       |       |
| Maintainability         |       |       |
| Deployability           |       |       |
| Scalability             |       |       |
| Security                |       |       |
| Compliance              |       |       |
| Observability           |       |       |
| Operational Safety      |       |       |
| AI Provenance           |       |       |
| Originality & Licensing |       |       |
| Skill Definition        |       |       |
| API Compatibility       |       |       |

Keep the dimension names and order identical across every audit so scores are comparable.

The API Compatibility dimension applies only when the subject is a reusable library or package,
per `assessment/api-compatibility.md`. For a deployable service or application it is `N/A`.

When the report language is not English, apply the column header and dimension name translations
from the matching `translation/` file.

## Scoring Rubric

The default scale is integers from `1` to `10`. Explicit alternatives are `1-5`, `1-3`,
`5 stars`, and `3 stars`. Star scales use the matching numeric rubric and render the score as a
star bar.

**Zero is not a score.** The value `0` is reserved and never used as a rated score in any scale.
When a dimension cannot apply, mark it `N/A` rather than assigning a numeric value.

### Quantitative Band Definitions (1-10)

Present this rubric matrix in the report so that scores are objective and reproducible.

| Band      | Score Range | Definition                                                   |
|-----------|-------------|--------------------------------------------------------------|
| Excellent | 9-10        | Capability is comprehensive and verified by strong evidence  |
| Good      | 7-8         | Capability is solid overall, minor or noticeable gaps exist  |
| Average   | 4-6         | Capability is present but uneven, limited, or inconsistent   |
| Poor      | 1-3         | Capability is minimal, fragmentary, or absent where required |

When the report language is not English, apply the band name and definition translations from the
matching `translation/` file.

Per-score meanings:

| Score | Meaning                                                       |
|-------|---------------------------------------------------------------|
| 10    | Capability is comprehensive and verified by strong evidence   |
| 9     | Capability is nearly comprehensive, with only trivial gaps    |
| 8     | Capability is solid with minor gaps                           |
| 7     | Capability is good overall, with some noticeable gaps         |
| 6     | Capability is adequate but uneven                             |
| 5     | Capability is present but limited or inconsistent             |
| 4     | Capability is present but significantly limited               |
| 3     | Capability is minimal or barely evidenced                     |
| 2     | Fragments present, mostly unevidenced                         |
| 1     | Capability is absent where required, with evidence of absence |

When the report language is not English, apply the header and per-score description translations
from the matching `translation/` file.

### Alternative Rubric (1-5)

Use this scale when the user selects `1-5` or `5 stars`.

| Band      | Score Range | Definition                                                  |
|-----------|-------------|-------------------------------------------------------------|
| Excellent | 5           | Capability is comprehensive and verified by strong evidence |
| Good      | 4           | Capability is solid with minor gaps                         |
| Average   | 3           | Capability is adequate but uneven                           |
| Poor      | 1-2         | Capability is minimal, limited, or absent where required    |

When the report language is not English, apply the same band translations from the matching
`translation/` file.

| Score | Meaning                                                       |
|-------|---------------------------------------------------------------|
| 5     | Capability is comprehensive and verified by strong evidence   |
| 4     | Capability is solid with minor gaps                           |
| 3     | Capability is adequate but uneven                             |
| 2     | Capability is present but limited or inconsistent             |
| 1     | Capability is absent where required, with evidence of absence |

When the report language is not English, apply the header and description translations from the
matching `translation/` file.

### Compact Rubric (1-3)

Use this scale when the user selects `1-3` or `3 stars`.

| Band      | Score | Definition                                                  |
|-----------|-------|-------------------------------------------------------------|
| Excellent | 3     | Capability is comprehensive and verified by strong evidence |
| Average   | 2     | Capability is adequate but uneven                           |
| Poor      | 1     | Capability is minimal, limited, or absent where required    |

| Score | Meaning                                                       |
|-------|---------------------------------------------------------------|
| 3     | Capability is comprehensive and verified by strong evidence   |
| 2     | Capability is adequate but uneven                             |
| 1     | Capability is absent where required, with evidence of absence |

When the report language is not English, apply the same band and description translations from
the matching `translation/` file.

### Star Display

Use `★` for each filled position and `☆` for each empty position.

For `5 stars`, use the `1-5` rubric and five positions. Examples: `★★★★★` for `5`,
`★★★☆☆` for `3`, and `★☆☆☆☆` for `1`.

For `3 stars`, use the `1-3` rubric and three positions. Examples: `★★★` for `3`, `★★☆` for
`2`, and `★☆☆` for `1`.

Render `UNKNOWN` and `N/A` as text, not as star bars.

For an overall mean under a star scale, round to the nearest integer for the star bar and keep
the exact mean in parentheses, for example `★★★☆☆ (3.4/5)`.

## Handling Unknowns

Do not assign the minimum score when evidence is simply missing.

When evidence is absent, leave the score blank or write `UNKNOWN` and explain in the notes. Reserve
the minimum score for evidenced absence of a required capability.

## Handling Not Applicable

When every source category for a dimension is `N/A`, mark the dimension `N/A` rather than scoring
it.

Put the applicability justification in the notes, anchored to the deployment model.

Do not let `N/A` dimensions drag a summary score. A dimension that cannot apply is excluded, not
counted as zero. Use `N/A` only under the contextual-applicability rule in
`principles/evaluation-rules.md`.

## Dimension To Category Mapping

Each scorecard dimension summarizes one or more assessment categories.

| Dimension               | Source Categories                                        |
|-------------------------|----------------------------------------------------------|
| Testability             | Testing and Testability                                  |
| Design Soundness        | Design Principles                                        |
| Code Quality            | Code Quality                                             |
| Stack Alignment         | Stack Best Practices                                     |
| Dependency Health       | Dependencies and Supply Chain                            |
| Maintainability         | Maintainability, Change Management, Documentation        |
| Deployability           | Deployment Strategy, Rollback Strategy                   |
| Scalability             | Non-Functional Requirements                              |
| Security                | Security                                                 |
| Compliance              | Compliance and Data Protection                           |
| Observability           | Observability                                            |
| Operational Safety      | Operational Readiness, Error Handling, Rollback Strategy |
| AI Provenance           | AI-Generated Code & Provenance                           |
| Originality & Licensing | Copyrights & Originality                                 |
| Skill Definition        | Skill Definition Conformance                             |
| API Compatibility       | API Compatibility And Versioning Discipline              |

## ISO/IEC 25010:2023 Crosswalk

Use this crosswalk as a coverage aid, not a claim of ISO certification or an ISO-defined scoring
formula.

Lens scores remain the existing rubric, and process/governance dimensions are complementary rather
than direct ISO product-quality ratings.

| Quality Characteristic | Lens Evidence                                           |
|------------------------|---------------------------------------------------------|
| Functional Suitability | Required behavior, correctness, contract tests          |
| Performance Efficiency | NFR measurements and resource use                       |
| Compatibility          | Interface and interoperability checks                   |
| Interaction Capability | User workflows, accessibility, error prevention         |
| Reliability            | Tests, resilience, recovery evidence                    |
| Security               | Security controls and dependency findings               |
| Maintainability        | Design, code quality, testability, documentation        |
| Flexibility            | Adaptation, installation, replacement, scalability      |
| Safety                 | Hazards, fail-safe behavior, warnings, safe integration |

The 2023 edition uses Interaction Capability and Flexibility and adds Safety compared with 2011.

Consult the [ISO publication record](https://www.iso.org/standard/78176.html) and identify when
only a public summary, such as the
[arc42 revision overview](https://quality.arc42.org/articles/iso-25010-update-2023), was accessible.

Do not claim clause-level assessment from a summary.

For a full audit, check all nine characteristics for applicability and identify assessed, unknown,
and inapplicable coverage in Scoring Rubrics or Scope Exclusions.

Functional completeness, interoperability, and user interaction need explicit evidence even when no
Lens dimension maps to them one-to-one.

Do not invent extra scores or claim the existing dimensions cover every characteristic completely.

Operational Safety is broader than ISO Safety, map only evidenced hazards and harm-prevention
controls to Safety.

## Score Confidence And Aggregation

Apply `process/readiness-and-scoring.md` for status-to-score mapping, confidence, score caps,
readiness gates, and multi-project aggregation.

Cite supporting evidence IDs, material findings, and confidence for each scored dimension.

Do not reward an unexecuted build or unverified runtime behavior as demonstrated capability.

If an overall score is requested, state the aggregation formula, weights, rounding rule, and scored
versus applicable dimensions, excluding `UNKNOWN` and `N/A` from the numeric denominator.

Always pair the mean with the floor: name the lowest-scoring applicable dimension and its score,
for example "Overall 5.8/10 (Average), lowest dimension: Security at 4/10". Under `5 stars` or
`3 stars`, render both values as star bars while keeping the exact mean in parentheses, for
example "Overall ★★★☆☆ (3.4/5), lowest dimension: Security ★★☆☆☆". When several dimensions
tie for the lowest score, name them all. The floor appears wherever the overall score appears,
including the Executive Summary and the Health Dashboard.

In a multi-project report, state the floor per project. Do not collapse unrelated projects into
one aggregate.

Disclose missing coverage beside the result, and do not compare aggregates with different scopes
without explaining the difference.

An average never overrides a material risk or incomplete production-readiness gate.

## Rules

- Every score must cite evidence in the detailed paragraph body.
- Keep notes neutral and technical.
- Do not average away a critical gap. If a dimension has a critical weakness, the score must reflect
  it and the notes must name it.
- Scores describe the system, never the people who built it.
