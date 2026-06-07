# Report Format

## Purpose

> **Scope:** The required structure and table-driven template for the final audit report
> **Key items:** technology stack, executive summary, system context, quality assessment, risk register, project scorecard, trade-offs, recommendations

This file defines the exact shape of the audit report. Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development, or an already-running production system. Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`. A present-but-empty section signals a gap; a missing section hides it.

## Formatting Rules

Use a hybrid table-paragraph format in every section.

Tables provide the scannable summary. Paragraphs below the table provide the detailed evidence, risks, and reasoning.

In tables, use shortened, general values. One or two words per cell. Do not crowd table cells with long explanations. Save detail for the paragraphs.

Do not number section headings. Use the section name as the heading, for example "Quality Assessment", not "3. Quality Assessment".

Keep column headers identical to the templates below across every audit.

Within a table cell, separate multiple points with a semicolon or a line break, not with sub-bullets.

Place descriptive paragraphs immediately after each table. In the paragraphs, explain every aspect with concrete evidence, file paths, and reasoning. Use short sentences separated by line breaks.

Start each detailed paragraph with a bold heading on its own line, followed by an empty line, then the paragraph body. Do not run the heading and the body together on the same line.

Example:

```markdown
**Continue current approach**

This option involves fixing only the most critical issues.
```

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

Present all categories in one summary table, then follow it with a detailed paragraph per category.

**Summary table:**

| Category | Status | Risks | Notes |
|----------|--------|-------|-------|

Keep the summary table short. Use one to three words per cell.

- **Status**: one of `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`, with the matching glyph.
- **Risks**: a short risk label, or `None identified`.
- **Notes**: a brief label, or `N/A` with one-line justification per `principles/evaluation-rules.md`.

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

**Detailed paragraphs:**

After the summary table, write one paragraph per category in the same order. Start each paragraph with a bold heading on its own line (the category name), followed by an empty line, then the body. Each paragraph restates the status and explains the evidence, concrete risks, and reasoning in detail. Anchor every claim to a file path, config key, or observed fact.

Keep each paragraph self-contained so it can be read independently of the table. Use short sentences separated by line breaks.

Include every category as a row. When a category cannot apply to the system's deployment model, mark it `N/A` with justification rather than dropping the row.

## Risk Register

Present a summary table followed by detailed risk paragraphs.

**Summary table:**

| Risk | Category | Severity | Mitigation |
|------|----------|----------|------------|

Keep the summary table short. Use concise risk names and one-word severity values.

Severity must be one of `Low`, `Medium`, `High`, `Critical`.

**Detailed paragraphs:**

After the summary table, write one paragraph per risk in the same order. Start each paragraph with a bold heading on its own line (the risk name), followed by an empty line, then the body. Each paragraph restates the risk, describes the impact and likelihood with evidence, then evaluates the mitigation. Anchor every claim to a specific finding from the Quality Assessment.

## Project Scorecard

Present a summary table followed by one paragraph per dimension.

**Summary table:**

| Dimension | Score | Notes |
|-----------|-------|-------|

Keep the summary table short. Use integer scores `0` to `5`, or `UNKNOWN` or `N/A`. Notes should be one phrase.

Use the rubric in `synthesis/scorecard.md`. Mark a dimension `UNKNOWN` when evidence is absent rather than scoring it `0`, and `N/A` when all of its source categories are `N/A`.

**Detailed paragraphs:**

After the summary table, write one paragraph per dimension in the same order. Start each paragraph with a bold heading on its own line (the dimension name), followed by an empty line, then the body. Each paragraph restates the score, cites the evidence from the Quality Assessment that supports it, and explains any gaps or strengths. Anchor every claim to a specific file or observation.

## Trade-off Analysis

Present a summary table followed by one paragraph per trade-off.

**Summary table:**

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

Keep the summary table short. Use concise phrases for each cell.

Present each trade-off neutrally, without declaring a winner unless the user asked for a recommendation.

**Detailed paragraphs:**

After the summary table, write one paragraph per trade-off in the same order. Start each paragraph with a bold heading on its own line (the trade-off name), followed by an empty line, then the body. Each paragraph restates the tension, describes the evidence in the system that reveals it, and explains the implication under the stated context. Anchor every claim to a file, config, or design choice.

## Recommendation Summary

Present a summary table followed by one paragraph per option.

**Summary table:**

| Option | Summary | Pros | Cons | Risk Level |
|--------|---------|------|------|------------|

Keep the summary table short. Use concise phrases. Pros and cons should be brief labels separated by semicolons.

Risk Level uses the severity vocabulary: `Low`, `Medium`, `High`, `Critical`.

Offer a small set of distinct options, for example continue current approach, incremental improvement, or partial redesign of specific components.

**Detailed paragraphs:**

After the summary table, write one paragraph per option in the same order. Start each paragraph with a bold heading on its own line (the option name), followed by an empty line, then the body. Each paragraph restates the option, explains the pros and cons with evidence from the Quality Assessment and Risk Register, and evaluates the residual risk. Anchor every claim to a specific finding.

Do not issue absolute directives unless the user explicitly requests them.
