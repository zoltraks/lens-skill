# Report Format

## Purpose

> **Scope:** The required structure and table-driven template for the final audit report
> **Key items:** technology stack, executive summary, system context, quality assessment, risk register, project scorecard, trade-offs, recommendations

This file defines the exact shape of the audit report. Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development, or an already-running production system. Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`. A present-but-empty section signals a gap; a missing section hides it.

## Formatting Rules

Use tables as the primary presentation in every section. Tables keep findings scannable and comparable across audits.

Do not number section headings. Use the section name as the heading, for example "Quality Assessment", not "3. Quality Assessment".

Keep column headers identical to the templates below across every audit.

Put narrative only where a table cannot carry it, and keep it to one or two lines near the relevant table.

Within a table cell, separate multiple points with a semicolon or a line break, not with sub-bullets.

## Report Delivery

Before producing a full report, confirm where it should go.

When the user names an output file, for example "write the audit to AUDIT.md", write the report to that path and confirm the location.

When the user invokes an audit without naming an output file, for example "perform lens on this service" or "make audit report on the codebase", ask which delivery they want before writing the full report:

- Return the report inline as the response.
- Write the report to a file whose name the user provides.

Ask this once, early, as a single question. Do not assume a default and do not invent a filename. If the user has already stated a preference in the same request, honor it without asking again.

For a single-dimension request that produces only a short subsection, returning the result inline is acceptable without asking, unless the user asked for a file.

## Section Order

The report has these top-level sections, in this order, with unnumbered headings:

- Technology Stack
- Executive Summary
- System Context
- Quality Assessment
- Risk Register
- Project Scorecard
- Trade-off Analysis
- Recommendation Summary

## Technology Stack

Open the report with a factual inventory of the technologies the subject uses. Describe the stack only; do not judge it here.

Use a key-value table:

| Layer            | Technology                                                      |
|------------------|-----------------------------------------------------------------|
| Languages        | <languages and versions>                                        |
| Frameworks       | <application and UI frameworks>                                 |
| Runtime/Platform | <runtime, OS, or host platform>                                 |
| Build tooling    | <build system, bundler, compilers>                              |
| Test tooling     | <test frameworks and runners>                                   |
| Package manager  | <dependency and package manager>                                |
| Key libraries    | <notable third-party libraries>                                 |
| Data stores      | <databases, caches, file formats>, or `NOT SPECIFIED`           |
| Target platforms | <where the software runs or ships>                              |

Anchor each entry to evidence, such as a manifest, lockfile, or config file. Mark any layer the input does not reveal as `NOT SPECIFIED`. Add or omit rows to fit the subject, but keep the layer names in this column.

## Executive Summary

Provide a compact overview a reader can absorb without the detail sections.

Use a key-value table:

| Field          | Value                                                                          |
|----------------|--------------------------------------------------------------------------------|
| System type    | <prototype / codebase / production system / proposal>                          |
| Scope          | <what was reviewed and what was excluded>                                      |
| Source basis   | <running system / inspected code / description>                                |
| Maturity level | <`Prototype` / `Early development` / `Pre-production` / `Production-ready` / `Undetermined`> |

Follow it with a high-level observations table, at most five rows:

| # | High-Level Observation |
|---|------------------------|
| 1 | <observation>          |

The maturity level must be justified by evidence in later sections, not asserted.

## System Context

Describe the system as understood from the input, without judgement.

Use a key-value table:

| Aspect                | Detail                                          |
|-----------------------|-------------------------------------------------|
| Functional description| <what the system does>                          |
| Architecture overview | <high-level structure>                          |
| Key components        | <named components or modules>                   |
| External dependencies | <services, libraries, platforms>                |
| Assumptions           | <only if explicitly stated, else `NOT SPECIFIED`> |

Mark any unknown aspect as `NOT SPECIFIED`.

## Quality Assessment

Present all categories in one table, in the fixed order below. One row per category.

| Category | Status | Evidence | Risks | Notes |
|----------|--------|----------|-------|-------|

Column rules:

- **Status**: one of `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`, with the matching glyph.
- **Evidence**: explicit facts anchored to a file, config, command, or quote.
- **Risks**: concrete technical risks; `None identified` is allowed when evidence supports it.
- **Notes**: neutral commentary; for `N/A`, state the one-line applicability justification per `principles/evaluation-rules.md`.

Category order:

- Testing and Testability
- Design Principles
- Code Quality
- Dependencies and Supply Chain
- Deployment Strategy
- Rollback Strategy
- Maintainability
- Change Management
- Documentation
- Non-Functional Requirements
- Security
- Compliance and Data Protection
- Observability
- Error Handling
- Operational Readiness

Include every category as a row. When a category cannot apply to the system's deployment model, mark it `N/A` with justification rather than dropping the row.

## Risk Register

Provide the risk register table defined in `synthesis/risk-register.md`. Column order is fixed:

| Risk | Category | Impact | Likelihood | Severity | Mitigation |
|------|----------|--------|------------|----------|------------|

Severity must be one of `Low`, `Medium`, `High`, `Critical`.

## Project Scorecard

Provide the project scorecard table defined in `synthesis/scorecard.md`. Column order is fixed:

| Dimension | Score | Evidence | Notes |
|-----------|-------|----------|-------|

Dimensions are scored `0` to `5`. Use the rubric in `synthesis/scorecard.md`. Mark a dimension `UNKNOWN` when evidence is absent rather than scoring it `0`, and `N/A` when all of its source categories are `N/A`.

## Trade-off Analysis

Surface the key trade-offs using `synthesis/trade-off-analysis.md`. Use a table:

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

Present each trade-off neutrally, without declaring a winner unless the user asked for a recommendation.

## Recommendation Summary

Provide non-prescriptive options using `synthesis/recommendations.md`. Use a table:

| Option | Summary | Pros | Cons | Risk Level |
|--------|---------|------|------|------------|

Risk Level uses the severity vocabulary: `Low`, `Medium`, `High`, `Critical`.

Offer a small set of distinct options, for example continue current approach, incremental improvement, or partial redesign of specific components.

Do not issue absolute directives unless the user explicitly requests them.
