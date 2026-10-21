# Code Style

## Purpose

> **Scope:** The conditional Code Style section of the report
> **Key items:** convention profile, consistency census, naming quality review, structure and
> comprehension, enforcement and drift, style sub-scores, craft notes

This file specifies the `Code Style` report section produced by `assessment/code-style.md`.

## Inclusion And Position

Include this section only when the subject contains source code files.

Omit it entirely for a subject with no source code, and note the omission in Scope
Exclusions.

It sits after `Structure Conformance` and before `API Compatibility & Versioning
Discipline` in the section order of `process/report-format.md`, and renders for `audit` and
`review` reports, never under `Report Style: hunt`.

## Section Contents

**Convention Profile**

One row per partition above the minimum-share threshold, recording the resolved yardstick:

| Partition | Language | Tier          | Dominant shapes                | Idiomatic               | Forced exclusions |
|-----------|----------|---------------|--------------------------------|-------------------------|-------------------|
| `<path>`  | `<lang>` | `T<n> <name>` | `<kind: shape share>` per kind | `Yes`/`Deliberate`/`No` | `<count or none>` |

The `Tier` cell carries the winning tier with its name, for example `T1 Declared` or
`T2 Observed`.

`Idiomatic` is `Yes`, `Deliberate deviation`, or `No` for the ecosystem in
`references/language-conventions.md`.

**Consistency Census**

One row per partition and identifier kind, with the census evidence ID:

| Partition | Kind     | Dominant  | Share      | Outliers | Trend       | Evidence  |
|-----------|----------|-----------|------------|----------|-------------|-----------|
| `<path>`  | `<kind>` | `<shape>` | `<n/N, %>` | `<n>`    | `<verdict>` | `EVD-NNN` |

`Trend` is `converging`, `stable`, `decaying`, or `n/a` when Git history was out of scope.

**Naming Quality Review**

The SL-3 results with up to 10 representative `file:line` examples, grouped by smell
(noise names, misleading names, wrong part of speech, missing units, abbreviation class
(d)+(e), typos and near-collisions, boundary leakage), each group flagged by blast radius
(public API, serialized field, config key, CLI flag, database column, or local scope).

**Structure, Comprehension And Cognitive Load**

The SL-4 to SL-6 results as a compact status table:

| Lens                      | Status  | Evidence         |
|---------------------------|---------|------------------|
| Structure and granularity | `<tkn>` | `<files or EVD>` |
| Comprehension aids        | `<tkn>` | `<files or EVD>` |
| Cognitive load            | `<tkn>` | `<files or EVD>` |

**Enforcement And Drift**

The SL-8 result: configured rules versus sampled code, suppression density, and the
`FND-INF-001` CI cross-reference when one exists.

**Style Sub-Scores**

One row per lens with status and justification, feeding the `Code Style` scorecard
dimension:

| Lens | Status  | Justification |
|------|---------|---------------|
| SL-1 | `<tkn>` | `<one line>`  |

**Craft Notes**

At most 10 one-line subjective suggestions tagged `Suggestion`, never counted in findings,
risks, or recommendations:

```markdown
- `Suggestion`: <one line>
```

Strengths found by this assessment are also summarized in Strengths & What's Working.

## Finding Conventions

Style findings use the `CQY` pillar and the shared finding template.

The `Basis` field opens with the resolved tier, for example
`Tier T2 Observed: 88% snake_case across parameter names (EVD-041)`.

Every consistency finding quantifies prevalence (n/N and %) and lists at least three
`file:line` examples, or all of them when fewer exist.

`Mitigating factors` considers interop, forced names, and the cost of change.

Severity follows the guide in `assessment/code-style.md`: `Low` by default, `Medium` for
public-API splits, security or safety paths, or more than 25% of a core partition, `High`
only with a demonstrated hazard, and never `Critical`.

Naming-quality findings are `Concern` at `MEDIUM` confidence or lower, and mechanical census
findings may carry `HIGH` confidence.

Recommendations follow the remediation ladder in `assessment/code-style.md`, and no `REC`
proposes a bulk rename of a consistent convention for ecosystem purity alone.

## Detail Levels

At `Detailed` the section carries every subsection above.

At `Standard` and `Brief` it carries the `Code Style` scorecard row, the Convention Profile
table, and the top 3 style findings, while the censuses stay in the Evidence Ledger.

## Evidence Rows

One `EVD` row per partition census, one per semantic sample with its sampling frame, one
for the T1 configuration inventory, one for suppression counts, and `NOT RUN` rows for the
subject's linters and formatters.

Each census row records the exact pattern or command per `references/census-commands.md`.

When the report language is not English, apply the heading and column header translations
from the matching `translations/` file.
