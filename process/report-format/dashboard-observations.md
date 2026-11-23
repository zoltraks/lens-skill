# Dashboard And Observations

## Purpose

> **Scope:** Health dashboard, delivery practice,
> and reader-facing observations **Key items:** risk map, scorecard, continuity
> proxies, observation blocks

Read the sections the task needs - grep the `## ` headings for the section map.

## Health Dashboard

Present the quantitative health summary in a consolidated view.

Under the `audit` style this section closes the report's front block,
directly behind the summary material:
the scorecard leads, the risk overview follows it,
and a reader deciding from the summary sees scores, limits, and risks together.

A multi-project dashboard opens with a project overview table naming each project,
its published score, its readiness, and its key qualification:

| Project | Published score | Readiness | Key qualification |
|---------|-----------------|-----------|-------------------|

The section then contains, in order, the `### Scorecard Summary` subsection,
a `**Interpretation limits**` note, the `**Risk Map**`,
and the `**Team & Continuity**` line.

Under `audit (legacy)` the order is Risk Map, Legend, Scorecard Summary,
Team & Continuity, with no overview table and no Interpretation limits note -
see `process/report-format/audit-legacy.md`.

**Risk Map**

Provide a consolidated Likelihood vs Impact matrix summarizing the top risks.
Impact rows that carry no risk in any Likelihood cell are omitted - the matrix shows only occupied
bands, never an empty severity band.

Use a table:

| Impact   | Low | Medium | High |
|----------|-----|--------|------|
| Critical |     |        |      |
| High     |     |        |      |
| Medium   |     |        |      |
| Low      |     |        |      |

When the report language is not English,
apply the axis label translations from the matching `translations/` file.

Populate cells with `RSK-XXX` identifiers from the Risk Register.

Leave empty cells blank.

Do not include plaintext secrets, passwords, or cryptographic keys in this summary.

Use generic descriptions or masked placeholders.

**Interpretation limits**

Place a brief `**Interpretation limits**` note adjacent to the scorecard - before the Risk Map.

It names the material execution and coverage limits in one or two sentences and distinguishes
project readiness from deployment approval: `Ready` never claims that every check passed
or that production was verified - the details stay in Scope Exclusions and Known Limitations.

### Scorecard Summary

Under the `audit` style the scorecard is a level-3 heading so Contents can link it directly;
under `audit (legacy)` it stays a `**Scorecard Summary**` bold label in the legacy order.

When the report language is not English,
apply the heading translation from the matching `translations/` file.

Provide a compact summary of the project scorecard dimensions.

A multi-project `audit` report pivots the matrix - one `Dimension` column followed by
one column per project, each header cell naming the project identifier verbatim
(for example `` `backend` ``), preserving every project's score per dimension.
A single-project report and every `audit (legacy)` report keep the long form:
`Dimension | Score`, or `Project | Dimension | Score` for a legacy multi-project report.

Precede the table with a `**Legend**` label and a `Band` / `Score` table naming the band for each
score range of the selected scale, so no score appears before its band is defined.
In a multi-project report emit the legend once - a shared `## Evaluation Legend` section before the
first `## Project` heading - rather than repeating the identical table inside every
project's Health Dashboard:

| Band      | Score |
|-----------|-------|
| Poor      | 1-3   |
| Average   | 4-6   |
| Good      | 7-8   |
| Excellent | 9-10  |

Band names come from the selected scale's vocabulary - `Bad`, `Poor`, `Average`, `Good`,
`Excellent` - and the Score cell carries the range token (`1-3`, `5`, `★★`).

| Dimension               | Score | Notes |
|-------------------------|-------|-------|
| Functional Suitability  |       |       |
| Testability             |       |       |
| Design Soundness        |       |       |
| Code Quality            |       |       |
| Code Style              |       |       |
| Stack Alignment         |       |       |
| Dependency Health       |       |       |
| Maintainability         |       |       |
| Structure               |       |       |
| Deployability           |       |       |
| Scalability             |       |       |
| Security                |       |       |
| Compliance              |       |       |
| Observability           |       |       |
| Operational Safety      |       |       |
| Documentation           |       |       |
| API Compatibility       |       |       |
| Delivery & Continuity   |       |       |
| Originality & Licensing |       |       |
| Skill Definition        |       |       |

Omit rows whose Score is `N/A` from the table entirely: the table lists scored dimensions only -
under the pivot form, drop only a row that is `N/A` for every project and render per-project `N/A`
cells inside scored rows.

The Delivery & Continuity dimension is `N/A` when Git history was not in scope,
per `references/delivery-practice.md`.

The API Compatibility dimension is `N/A` unless the subject is a reusable library or package,
per `assessment/api-compatibility.md`.

At the `Detailed` level, add a paragraph below the table naming each omitted `N/A` dimension and its
applicability reason, for example
`API Compatibility. The subject is not a reusable library or package`.

Render each Score cell in the selected evaluation scale: `7/10` for `1-10`, `4/5` for `1-5`,
`2/3` for `1-3`, `★★★★☆` for `5 stars`, and `★★☆` for `3 stars`.

Render `UNKNOWN` as text, not as a star bar - `N/A` rows are omitted from the table entirely.

Never add an `Overall score` row to this table:
the validator recomputes the mean from every numeric Score cell,
and a numeric overall row enters that mean and corrupts it.

The overall score belongs to the Executive Summary key-value table,
per `process/report-format/summary-changes.md`,
and the validator compares the stated overall against the recomputed mean.
They must agree under the documented rounding.

When the report language is not English,
apply the translations from the matching `translations/` file.

**Team & Continuity**

Write one line summarizing contributor and continuity evidence collected during Evidence Gathering:
author concentration, commit cadence, tag and release history,
and any documented ownership or maintenance statement.

Anchor it to evidence IDs.

When no contributor or continuity evidence exists,
omit the line entirely - do not write `Not collected` or any reason clause,
because the absence reason (no Git history, no window)
already appears in Scope Exclusions and Known Limitations.

Never render the line as a pointer to another section - `Team & Continuity - see Delivery Practice`
duplicates a section that follows immediately and misnames it.

Delivery Practice carries the delivery-side continuity proxies (cadence, windows, bus factor).
the dashboard line summarizes the contributor side only.

When Git history or repository data was not in scope,
mark it `Not collected` rather than omitting the line.

Keep it neutral and aggregate, never personal.

Commit concentration is a proxy for continuity, not a measure of operational access or expertise.

This line is the at-a-glance summary.

The full delivery-practice proxies and concentration detail live in the Delivery Practice &
Team Continuity section.

When the report language is not English,
apply the heading translation from the matching `translations/` file.

## Delivery Practice

Assess how the project delivers changes and how concentrated its contributor base is,
using only what the repository shows.

Apply `references/delivery-practice.md` for the proxy procedures, the bus-factor rubric,
and the marking rules.

**Delivery metrics**

Present the DORA five-metric view.

Two metrics are computable as Git-derived proxies,
three are not measurable from source and must stay `None` with the reason:

| DORA metric                     | Result           | Basis                                   |
|---------------------------------|------------------|-----------------------------------------|
| Change lead time                | <proxy interval> | Proxy: median commit-to-tag interval    |
| Deployment frequency            | <proxy cadence>  | Proxy: tag cadence over observed window |
| Failed deployment recovery time | `None`           | Requires incident and deployment data   |
| Change fail rate                | `None`           | Requires incident and rollback data     |
| Deployment rework rate          | `None`           | Requires production incident data       |

Label computed values as proxies, never as measured DORA metrics.

A project with no tags reports the proxy rows as `None` with the reason,
commits are not deployments.

A repository with no tags and no release or deployment data reports `None` on all five rows:
no proxy is computable and nothing else is measurable from source.

When Git history was not in scope, mark the whole table `Not collected`.

**Contributor concentration**

State the bus-factor rating from `references/delivery-practice.md`: the top-author commit share,
the active-contributor count, the observation window, and the resulting `High`, `Moderate`,
or `Low` concentration rating, anchored to `EVD-XXX` rows.

The rating renders as a natural fixed-vocabulary form,
matching `None` and `Not collected` usage in the same section.

Reviewer diversity is `None` unless the repository itself records review data,
pull-request reviews do not live in Git history.

Follow with one short paragraph noting documented ownership or maintenance statements,
and any continuity-relevant `FND-INF` or `RSK-XXX` references.

Keep the content aggregate and neutral, never a personal assessment.

When the report language is not English, apply the heading, column header,
and status translations from the matching `translations/` file.

## High-Level Observations

Surface the most important findings in a compact table a reader can scan before reading
the detail sections.

Include at most five observations.

Each observation should be a single concrete finding, not a category summary.

Use this single-column table:

| Observation   |
|---------------|
| <observation> |

When the report language is not English,
apply the table header translation from the matching `translations/` file.

Write one paragraph per observation immediately after the table,
in the same order as the table rows.

Start each paragraph with a bold heading on its own line (the observation text,
abbreviated if needed), then add an empty line, then the body.

Each paragraph explains why the observation matters and what risk or opportunity it represents.

Anchor every claim to a specific finding in the Technical Findings.

Keep each observation brief.

The full technical detail lives in the numbered finding blocks later in the report.

This section exists to give non-technical readers a fast-skim path.
