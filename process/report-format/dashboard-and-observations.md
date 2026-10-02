# Dashboard And Observations

## Purpose

> **Scope:** Health dashboard, delivery practice, and reader-facing observations
> **Key items:** risk map, scorecard, continuity proxies, observation blocks

## Health Dashboard

Present the quantitative health summary in a consolidated view.

This section contains the Risk Map, the Scorecard Summary, and the Team & Continuity line.

**Risk Map**

Provide a consolidated Likelihood vs Impact matrix summarizing the top risks.

Use a table:

| Impact   | LOW | MEDIUM | HIGH |
|----------|-----|--------|------|
| CRITICAL |     |        |      |
| HIGH     |     |        |      |
| MEDIUM   |     |        |      |
| LOW      |     |        |      |

When the report language is not English, apply the axis label translations from the matching
`translations/` file.

Populate cells with `RSK-XXX` identifiers from the Unified Risk Register.

Leave empty cells blank.

Do not include plaintext secrets, passwords, or cryptographic keys in this summary.

Use generic descriptions or masked placeholders.

**Scorecard Summary**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Provide a compact summary of the project scorecard dimensions.

Precede the table with the same one-line score-band legend defined for the Executive Summary,
so no score appears before its band is defined.

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
| Delivery & Continuity   |       |       |
| AI Provenance           |       |       |
| Originality & Licensing |       |       |
| Skill Definition        |       |       |
| API Compatibility       |       |       |

Omit rows whose Score is `N/A` from the table entirely: the table lists scored dimensions only.

The Delivery & Continuity dimension is `N/A` when Git history was not in scope, per
`references/delivery-practice.md`.

The API Compatibility dimension is `N/A` unless the subject is a reusable library or package,
per `assessment/api-compatibility.md`.

At the `Detailed` level, add a paragraph below the table naming each omitted `N/A` dimension and
its applicability reason, for example `API Compatibility - the subject is not a reusable library
or package`.

Render each Score cell in the selected evaluation scale: `7/10` for `1-10`, `4/5` for `1-5`,
`2/3` for `1-3`, `★★★★☆` for `5 stars`, and `★★☆` for `3 stars`.

Render `UNKNOWN` as text, not as a star bar; `N/A` rows are omitted from the table entirely.

When the report language is not English, apply the translations from the matching `translations/`
file.

**Team & Continuity**

Write one line summarizing contributor and continuity evidence collected during Evidence Gathering:
author concentration, commit cadence, tag and release history,
and any documented ownership or maintenance statement.

Anchor it to evidence IDs.

When Git history or repository data was not in scope,
mark it `NOT COLLECTED` rather than omitting the line.

Keep it neutral and aggregate, never personal.

Commit concentration is a proxy for continuity, not a measure of operational access or expertise.

This line is the at-a-glance summary.

The full delivery-practice proxies and concentration detail live in the Delivery Practice & Team
Continuity section.

When the report language is not English, apply the heading translation from the matching
`translations/` file.

## Delivery Practice & Team Continuity

Assess how the project delivers changes and how concentrated its contributor base is,
using only what the repository shows.

Apply `references/delivery-practice.md` for the proxy procedures, the bus-factor rubric,
and the marking rules.

**Delivery metrics**

Present the DORA five-metric view.

Two metrics are computable as Git-derived proxies,
three are not measurable from source and must stay `NOT SPECIFIED` with the reason:

|  | DORA metric                     | Result           | Basis                                   |
|--|---------------------------------|------------------|-----------------------------------------|
|  | Change lead time                | <proxy interval> | Proxy: median commit-to-tag interval    |
|  | Deployment frequency            | <proxy cadence>  | Proxy: tag cadence over observed window |
|  | Failed deployment recovery time | `NOT SPECIFIED`  | Requires incident and deployment data   |
|  | Change fail rate                | `NOT SPECIFIED`  | Requires incident and rollback data     |
|  | Deployment rework rate          | `NOT SPECIFIED`  | Requires production incident data       |

Label computed values as proxies, never as measured DORA metrics.

A project with no tags reports the proxy rows as `NOT SPECIFIED` with the reason,
commits are not deployments.

A repository with no tags and no release or deployment data reports `NOT SPECIFIED` on all
five rows: no proxy is computable and nothing else is measurable from source.

When Git history was not in scope, mark the whole table `NOT COLLECTED`.

**Contributor concentration**

State the bus-factor rating from `references/delivery-practice.md`: the top-author commit share,
the active-contributor count, the observation window, and the resulting `HIGH`, `MODERATE`,
or `LOW` concentration rating, anchored to `EVD-XXX` rows.

The rating renders as a fixed-vocabulary token in uppercase, matching `NOT SPECIFIED` and
`NOT COLLECTED` usage in the same section.

Reviewer diversity is `NOT SPECIFIED` unless the repository itself records review data,
pull-request reviews do not live in Git history.

Follow with one short paragraph noting documented ownership or maintenance statements,
and any continuity-relevant `FND-INF` or `RSK-XXX` references.

Keep the content aggregate and neutral, never a personal assessment.

When the report language is not English, apply the heading, column header, and status
translations from the matching `translations/` file.

## High-Level Observations

Surface the most important findings in a compact table a reader can scan before reading the detail
sections.

Include at most five observations.

Each observation should be a single concrete finding, not a category summary.

Use this single-column table:

| Observation   |
|---------------|
| <observation> |

When the report language is not English, apply the table header translation from the matching
`translations/` file.

Write one paragraph per observation immediately after the table,
in the same order as the table rows.

Start each paragraph with a bold heading on its own line (the observation text,
abbreviated if needed), then add an empty line, then the body.

Each paragraph explains why the observation matters and what risk or opportunity it represents.

Anchor every claim to a specific finding in the Detailed Technical Findings.

Keep each observation brief.

The full technical detail lives in the numbered finding blocks later in the report.

This section exists to give non-technical readers a fast-skim path.
