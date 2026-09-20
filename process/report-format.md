# Report Format

## Purpose

> **Scope:** The required structure and template for the final audit report
> **Key items:** document information, technology stack, executive summary, health dashboard,
> auditing methodology, scoring rubrics, system context, architectural assessment, detailed
> technical findings, unified risk register, trade-off analysis, remediation roadmap, scope
> exclusions

This file defines the exact shape of the audit report. Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development, or an
already-running production system. Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`. A present-but-empty section signals a gap, a
missing section hides it.

## Contents

| Section                                     | Line | What it covers                                        |
|---------------------------------------------|------|-------------------------------------------------------|
| Formatting Rules                            | 58   | Formatting Rules guidance                             |
| Report Delivery And Parameter Configuration | 216  | Report delivery and output configuration              |
| Detail Level Configuration                  | 254  | Standard, detailed, and brief reports                 |
| Conditional Sections                        | 338  | Inclusion criteria for conditional sections           |
| Section Order                               | 378  | Single-project and multi-project order                |
| Document Information                        | 448  | Report metadata and revisions                         |
| Glossary                                    | 529  | Abbreviation and acronym definitions                  |
| Multi-Project Report Structure              | 616  | Combined and project-specific sections                |
| Executive Summary                           | 708  | Executive summary and readiness threshold             |
| Changes Since Previous Audit                | 791  | Re-audit comparison structure                         |
| System Context                              | 852  | Context and technology stack                          |
| Health Dashboard                            | 912  | Heat map, scorecard, and continuity                   |
| High-Level Observations                     | 986  | Reader-facing finding summary                         |
| Auditing Methodology                        | 1010 | Method, standards, and evidence ledger                |
| Scoring Rubrics                             | 1152 | Score bands and ISO crosswalk                         |
| Architectural Assessment                    | 1214 | Architecture, principles, and conditional subsections |
| Trade-off Analysis                          | 1349 | Neutral engineering trade-offs                        |
| Threat Model                                | 1389 | STRIDE analysis                                       |
| API Contract Conformance                    | 1416 | API contract and security conformance                 |
| Skill Definition Conformance                | 1436 | Agent Skill conformance                               |
| AI System Assessment                        | 1459 | Conditional AI-system review                          |
| Standards Conformance                       | 1471 | Internal standards quality and code conformance       |
| API Compatibility & Versioning Discipline   | 1527 | Library compatibility gates                           |
| Strengths & What's Working                  | 1554 | Evidence-based positive baselines                     |
| Detailed Technical Findings                 | 1584 | Finding summary and detail blocks                     |
| Technical Debt Register                     | 1681 | Distinct accumulated debt                             |
| Unified Risk Register                       | 1722 | Cross-referenced risks                                |
| Actionable Remediation Roadmap              | 1809 | Prioritized recommendations                           |
| Scope Exclusions                            | 1873 | Explicit coverage limits                              |
| Limitations and Unknowns                    | 1925 | Unrun checks and missing evidence                     |
| Re-audit and Follow-up Plan                 | 1949 | Closure evidence and ownership                        |
| Validation Record                           | 1978 | Mechanical and semantic gate results                  |
| References                                  | 2003 | Consulted external sources                            |
| Pre-Delivery Mechanical Checklist           | 2041 | Final mechanical checks                               |

## Formatting Rules

Use a hybrid table-paragraph format in every section.

Tables provide the scannable summary. Paragraphs below the table provide the detailed evidence,
risks, and reasoning.

In tables, use shortened, general values. One or two words per cell. Do not crowd table cells with
long explanations. Save detail for the paragraphs.

Do not number section headings. Use the section name as the heading, for example "Executive
Summary", not "2. Executive Summary". When the user requests a specific language, translate the
section heading into that language.

Use `#` for the document title, `##` for top-level sections, and `###` for subsections and finding
or register blocks. Do not use `####` or deeper headings.

Use Title Case for English section names and keep them short, avoid trailing punctuation and
descriptive qualifiers in parentheses. The matching `translation/` file defines the casing rule for
non-English reports.

Keep column headers identical to the templates below across every audit. When the user requests a
specific language, translate the column headers into that language while keeping the structure
identical.

Keep table cells single-line and use commas for compact lists, placing explanations below the table.

Preserve identifiers and gap tokens intact even when they exceed the usual cell word limit.

Place descriptive paragraphs immediately after each table. In the paragraphs, explain every aspect
with concrete evidence, file paths, and reasoning. Use short sentences separated by blank lines,
each sentence stands on its own line with an empty line between consecutive sentences.

Start each detailed paragraph with a bold heading on its own line. Put the status, score, or
severity inline after the heading, separated by a space. Then add an empty line, then the paragraph
body. Do not run the heading and the body together on the same line.

Use this bold-heading pattern for paragraphs that expand on a table row. For actual section or
subsection titles, use markdown header syntax (`##` or `###`) rather than bold text.

Break prose lines that exceed 100 characters at a natural boundary such as after a comma or clause
end, per `STYLE.md`. Do not break inside inline code, file paths, or URLs. The limit does not apply
to table rows, URLs, links, or file paths, so a line carrying an unbreakable URL may remain over 100
characters.

Do not use the semicolon character in prose. Join closely related clauses with a comma or split them
into separate sentences. The rule does not apply to code blocks, inline code, or file paths, per
`STYLE.md`.

Use a language tag on fenced code blocks that contain code. Leave diagrams, directory trees, console
output, and plain text untagged, and do not leave a blank line as the first or last line inside a
fenced block.

Do not add a Contents or table-of-contents section. `STYLE.md` requires one in documents over 300
lines, but the report navigates by its fixed section order and the Health Dashboard, so the omission
is deliberate.

### Table Formatting Rules

Apply these rules to every table in the report.

**Delimiters**: Use pipe characters (`|`) to delimit columns. Place one space after the leading pipe
and one space before the trailing pipe.

**Header separator**: Place a separator line immediately after the header row. The separator
contains only hyphens and pipe characters. The hyphens are contiguous with the pipe characters - do
not add spaces between pipes and hyphens. The separator width for each column equals the column
width plus two hyphens. Minimum column width is three characters.

Correct separator format:
```markdown
|---------|--------|
```
Incorrect separator format (spaces around hyphens):
```markdown
| ------- | ------ |
```

**Cell padding**: Pad every cell with trailing spaces so it matches the widest cell in that column.
Empty cells must also be padded. Use left alignment for all cells. Never truncate cell contents.

**Column width**: Calculate the column width as the maximum character width of all cells in that
column, including the header. Include all Markdown formatting characters (backticks, asterisks,
spaces, punctuation) in the width measurement.

**Compacting**: After calculating column widths, compact the table by removing any padding that
exceeds the widest cell in each column. The compacted version - minimum width that fits every cell -
is the correct version.

**Checklist for every table**:
- Identify all cells including the header row.
- Measure each cell width including all formatting characters.
- Determine the maximum width per column.
- Pad every cell with trailing spaces to match the column maximum.
- Build the separator with hyphens equal to the column width plus two, no spaces.
- Verify all `|` separators align vertically in plain text.
- Never put a literal `|` inside a cell, even inside backticks or code spans. Table parsers split
  on every `|` regardless of code formatting, so write "pipe" or use a different character.

**Automated formatting**

Format every table with a script, do not count column widths by hand. Manual counting is error-prone
and produces misaligned columns, per `STYLE.md`.

Before delivering a File-mode report, run a script that implements the checklist above: parse each
table, measure every cell width in source text including formatting characters, pad each cell to the
column maximum, and rebuild each separator as the column width plus two hyphens. Handle both `\n`
and `\r\n` input and preserve the file's original line-ending style.

`tools/format-table.py` in the skill repository is the canonical implementation. Copy it into the
audited repository under a `.tmp.` name, for example `format-table.tmp.py`, instead of writing a
new formatter by hand.

Place the script copy in `work/` when that directory exists in the audited repository.
Use an existing `temp` or `temporary` directory when `work/` is unavailable, and use the repository
root only when none exists. Run it on the report file, verify that all `|` separators align
vertically, then remove the copy.

For Inline delivery, apply the same formatting to the report text before emitting the response.

Running the formatting script on the report file is part of producing the report. It is not
execution of the audited project.

Example for finding summary:

```markdown
**FND-SEC-001: Hardcoded JWT signing key** `CRITICAL`

`src/backend/appsettings.json` contains a plaintext JWT symmetric key.
```

Example for scorecard dimension:

```markdown
**Security** Score: `2/10`

The repository contains multiple plaintext secrets in tracked files.
```

When `5 stars` is selected, the same dimension uses a five-position star bar:

```markdown
**Security** Score: `★★☆☆☆`

The repository contains multiple plaintext secrets in tracked files.
```

**Hyphen rule**

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs. Do not
use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

**No closing line**

Do not add a closing line such as "End of audit report." or "---" at the end of the document. The
final section is the References section, end the report after the final section without any trailing
boilerplate.

## Report Delivery And Parameter Configuration

Report delivery and output-file selection are determined during the Parameter Configuration
phase in `process/audit-workflow.md`. Do not ask delivery questions here, they are handled
upstream.

The delivery question presents `Inline`, each applicable concrete file path, and
`Custom report file` in one prompt. Selecting a file path chooses both delivery and output
location.

When the user names an output file in the original request, for example "write the audit to
AUDIT.md", honor that filename without asking again. Resolve the output directory using the
location rules in `process/audit-workflow.md` unless a full path was given.

When the user states only a File preference without naming a path, ask the same question with
`Inline` omitted. Retain the applicable file-location and `Custom report file` options.

When the user invokes an audit without naming an output file, the Parameter Configuration phase
resolves the output base and offers the applicable file paths in the delivery question.

Default delivery is **File** when `docs/audit/` or `docs/report/` exists in the audited
repository or directory, otherwise **Inline**. When File is selected, resolve the output
location in this order: `docs/audit/`, then `docs/report/`, then `docs/`, then the root.

An existing version-numbered subdirectory pattern produces a path such as
`docs/report/<version>/AUDIT.md`. An existing date-named pattern produces a path such as
`docs/report/<current-date>/AUDIT.md`. When no pattern exists, the question offers the base path
plus version-numbered and date-named alternatives under `docs/audit/` or `docs/report/`.

The default filename is `AUDIT.md` for English reports, or the language-specific filename from
the matching `translation/` file. When a previous audit report exists, the filename carries the
new revision, for example `AUDIT-2.0.md`, and the previous file is never overwritten.

`Custom report file` asks the user to specify the location and filename before writing.

For a single-dimension request that produces only a short subsection, returning the result
inline is acceptable without asking, unless the user asked for a file.

## Detail Level Configuration

The report adapts to the detail level chosen during Parameter Configuration.

The default detail level is `Detailed`. `Standard` and `Brief` remain available when the user
selects them during configuration or explicitly requests them.

**Standard**

All seventeen baseline sections are present in full, subject to explicit parameter exclusions:

- Document Information
- Executive Summary
- System Context (including the Technology Stack subsection)
- Health Dashboard
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment
- Trade-off Analysis
- Strengths & What's Working
- Detailed Technical Findings (all findings with full Description, Impact, Remediation, and
  Verification)
- Unified Risk Register
- Actionable Remediation Roadmap (full matrix with P1-P4, impact/effort/complexity, verification)
- Scope Exclusions
- Limitations and Unknowns
- Validation Record
- References

In addition, any conditional sections whose criteria are met are included in full. See the
Conditional Sections rule below for the inclusion criteria of the Data Flow Diagram, Design
Patterns, Architecture Decision Records, Threat Model, API Contract Conformance, Skill Definition
Conformance, Standards Conformance, Technical Debt Register, and Re-audit and Follow-up Plan.

**Detailed**

Same sections as Standard, plus the following extensions. At the Detailed level, evaluate every
conditional section's criterion explicitly and include each one that applies:

- Executive Summary includes a longer Production Readiness Threshold paragraph.
- Health Dashboard includes an expanded Risk Heat Map with all risks plotted.
- Architectural Assessment includes deeper critique with additional industry baseline comparisons.
- Strengths section includes 8-10 bullet points.
- Each finding includes extended verification methods and alternative remediation paths.
- Trade-off Analysis includes additional trade-offs surfaced during assessment.
- Remediation Roadmap includes additional context for each recommendation (blocking dependencies,
  estimated timeframes).
- Threat Model expands reasoning for all six STRIDE categories at each boundary, which are checked
  at every detail level, including explicit no-material-threat outcomes.
- Technical Debt Register, when included, lists cost of delay for every item rather than only the
  top items.

**Brief**

Condensed output for rapid review:

- Document Information (full)
- Glossary (when Descriptive mode is enabled)
- Executive Summary (summary table, evidence limits, readiness gate, and cost uncertainty)
- Changes Since Previous Audit (report reference and finding transition tables only) when a previous
  report exists
- System Context (Technology Stack subsection only)
- Health Dashboard (scorecard summary and risk heat map only)
- High-Level Observations (full)
- Strengths & What's Working (top 3 bullets only)
- Top 5 findings only (summary table and abbreviated detail blocks)
- Top 5 risks only (summary table)
- Key trade-offs only (top 2, no full table)
- Key recommendations only (top 5, no full matrix)
- Scope Exclusions (full)
- Limitations and Unknowns (full)
- Validation Record (full)
- References (full)

Omitted in Brief: full Auditing Methodology, Scoring Rubrics, the System Context aspects beyond
the Technology Stack subsection, Architectural Assessment critique, full findings, full risk
register, full trade-offs, and full roadmap.

Retain a compact check summary and evidence IDs in Scope Exclusions, and blocked/unrun checks in
Limitations and Unknowns.

Do not omit critical decision limitations to meet the shorter format.

## Conditional Sections

Some sections and subsections apply only to certain kinds of system. Include a section only when it
is relevant to the subject under audit. A section that does not apply must be omitted entirely, not
included as an empty placeholder.

This differs from the rule for always-present sections, where a present-but-empty section signals a
gap. The conditional sections below describe a specific capability (an API, a trust boundary,
recurring structure) that some subjects simply do not have, forcing such a section would mislead the
reader.

When a conditional section is omitted, state the omission once in the Scope Exclusions section with
a one-line justification, so the reader knows the omission was deliberate.

The following sections and subsections are conditional. Each lists its inclusion criterion and the
assessment file that governs it:

| Section / Subsection                                        | Include When                                                  | Governing File                        |
|-------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------|
| Data Flow Diagram (in Architectural Assessment)             | The system moves data across one or more trust boundaries     | `assessment/data-flow.md`             |
| Design Patterns (in Architectural Assessment)               | The codebase is large enough to exhibit recurring structure   | `assessment/design-patterns.md`       |
| Architecture Decision Records (in Architectural Assessment) | The system is production-bound with significant decisions     | `assessment/change-management.md`     |
| Threat Model (standalone)                                   | The system has a security-relevant attack surface or boundary | `assessment/threat-model.md`          |
| API Contract Conformance (standalone)                       | The system defines, exposes, or consumes an API contract      | `assessment/api-contract.md`          |
| Skill Definition Conformance (standalone)                   | The subject is an Agent Skill with a `SKILL.md` file          | `assessment/skill-definition.md`      |
| AI System Assessment (standalone)                           | The project trains, serves, or materially depends on AI       | `assessment/ai-system.md`             |
| Standards Conformance (standalone)                          | The project contains documented development standards         | `assessment/standards-conformance.md` |
| API Compatibility & Versioning Discipline (standalone)      | The subject is a reusable library or package                  | `assessment/api-compatibility.md`     |
| Technical Debt Register (standalone)                        | Structural debt distinct from risks is surfaced               | `synthesis/debt-register.md`          |
| Re-audit and Follow-up Plan (standalone)                    | The roadmap contains a P1 or P2 recommendation                | `synthesis/re-audit-plan.md`          |
| Changes Since Previous Audit (standalone)                   | A previous audit report was found during intake               | `synthesis/report-comparison.md`      |
| Glossary (standalone)                                       | Descriptive mode is enabled (default)                         | `process/report-format.md`            |

In a multi-project report, evaluate each criterion independently per project. A section may apply
to one project and be omitted for another, record each deliberate omission in Scope Exclusions.

When in doubt about whether a conditional section applies, prefer including it with explicit `N/A`
or `NOT SPECIFIED` markers over silently dropping a relevant concern. Only omit a section when it
genuinely cannot apply to the subject.

## Section Order

The report has these top-level sections, in this order, with unnumbered headings. Sections marked
*(conditional)* are included only when their criterion in the Conditional Sections table is met.

For a **single-project** audit:

- Document Information
- Glossary *(when Descriptive mode is enabled)*
- Executive Summary
- Changes Since Previous Audit *(conditional)*
- System Context (contains the Technology Stack subsection)
- Health Dashboard
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment (contains the Design Principles subsection and may contain the
  conditional Data Flow Diagram, Design Patterns, and Architecture Decision Records subsections)
- Trade-off Analysis
- Threat Model *(conditional)*
- API Contract Conformance *(conditional)*
- Skill Definition Conformance *(conditional)*
- AI System Assessment *(conditional)*
- Standards Conformance *(conditional)*
- API Compatibility & Versioning Discipline *(conditional)*
- Strengths & What's Working
- Detailed Technical Findings
- Technical Debt Register *(conditional)*
- Unified Risk Register
- Actionable Remediation Roadmap
- Scope Exclusions
- Limitations and Unknowns
- Re-audit and Follow-up Plan *(conditional)*
- Validation Record
- References

For a **multi-project** audit, the structure changes. See the Multi-Project Report Structure section
below for the full layout. In summary:

- Document Information (once)
- Project Inventory (once)
- Glossary *(when Descriptive mode is enabled)* (once)
- Executive Summary (condensed, combined)
- Changes Since Previous Audit *(conditional)* (combined)
- Per project (level-2 heading per project, full section set each):
  - Executive Summary
  - System Context (with the Technology Stack subsection)
  - Health Dashboard
  - High-Level Observations
  - Auditing Methodology
  - Scoring Rubrics
  - Architectural Assessment
  - Trade-off Analysis
  - Threat Model *(conditional)*
  - API Contract Conformance *(conditional)*
  - Skill Definition Conformance *(conditional)*
  - Standards Conformance *(conditional)*
  - API Compatibility & Versioning Discipline *(conditional)*
  - Strengths & What's Working
  - Detailed Technical Findings
  - Technical Debt Register *(conditional)*
  - Unified Risk Register
  - Actionable Remediation Roadmap
- Trade-off Analysis (combined, cross-project trade-offs only)
- Scope Exclusions (once, shared)
- Limitations and Unknowns (once, shared)
- Re-audit and Follow-up Plan *(conditional)* (once, shared)
- Validation Record (once, shared)
- References (once, shared)

## Document Information

Open the report with a document title as a level-1 markdown heading (`#`), followed by the
`## Document Information` section.

Present the document metadata as a two-column table with an empty header row and no column
names:

```markdown
# <System Name> Software Audit Report

## Document Information

|                  |                                              |
|------------------|----------------------------------------------|
| Report Revision  | 1.2                                          |
| Report Date      | 2026-09-17                                   |
| State            | Final                                        |
| Detail Level     | Detailed                                     |
| Evaluation Scale | 1-10                                         |
| Previous Report  | docs/audit/26.7.0/AUDIT-1.1.md, revision 1.1 |
```

Pad the empty header cells to the column width like any other cell.

Rows appear in this order, each label in the first column and its value in the second:

- `Report Revision` - the report document revision, assigned per the report revision rules below.
- `Report Date` - the audit date.
- `State` - `Draft` or `Final`.
- `Detail Level` - `Standard`, `Detailed`, or `Brief`.
- `Evaluation Scale` - `1-10`, `1-5`, `1-3`, `5 stars`, or `3 stars`.
- `Descriptive Mode` - `Enabled` or `Disabled`. Always recorded so re-audits recover the
  setting.
- `Language` - the report language.
- `Audit Purpose` - engineering improvement, production readiness, or technical due diligence.
- `Target Environment` - where the software runs or ships.
- `Verification Scope` - always `source-only`.
- `Subject Revision` - the audited revision of the subject, such as a commit hash.
- `Dirty-Tree State` - the working tree state at audit time.
- `Skill Version` - the version of the audit skill that produced the report.
- `Previous Report` - the previous report path and revision, only when a previous report exists.
- `Projects` - the audited project names, multi-project reports only.

Omit a row entirely when the input does not establish its value. Never write an empty value cell
or a `NOT SPECIFIED` token in this table.

Do not include a `Delivery Mode` or `Report Delivery` row. Whether the report was delivered as a
file or an inline response is evident from the delivery itself.

The word `revision` refers to the report document. The word `version` refers to the audited
software, a project, a library, or the skill itself, as in `Subject Revision` for the audited
commit and `Skill Version` for the skill.

For a multi-project audit, use the repository or directory name as the system name in the title
and include the `Projects` row.

These fields support reproducible re-audits and prevent historical tool results being attributed
to a different tree.

`Final` means the scoped report is complete, not that the system is approved for production.

**Report revision**

The first audit of a subject is revision `1.0`.

When a previous audit report exists, read the `Report Revision` value from its Document
Information table, increment the minor component up to 9 (for example, `1.0` to `1.1`, `1.9` to
`2.0`, `9.9` to `10.0`), and write the incremented revision into the new report. When the
previous report records no revision, treat it as `1.0` and assign `1.1`.

Earlier reports may record the document revision differently: a bold-label `Version` field, or a
`Field`/`Value` table with a `Version` row. Read any of these forms as the report revision.

The previous report file is never overwritten. The new report is written to a separate file
carrying the new revision in its name, for example `AUDIT-1.1.md`, per
`synthesis/report-comparison.md`.

When the report language is not English, apply the label translations from the matching
`translation/` file.

## Glossary

The Glossary defines every abbreviation and acronym used in the report. It is present when
Descriptive mode is `Enabled` (the default) and omitted when Descriptive mode is `Disabled`.
When omitted, record the deliberate omission with a one-line justification in Scope Exclusions.

The section appears immediately after `## Document Information`, or after
`## Project Inventory` in a multi-project report, and always before `## Executive Summary`.
A multi-project report carries one shared Glossary covering terms used in every project block.

**Index table**

Present the terms as a two-column table, one row per term, sorted alphabetically ignoring case.
The Term cell holds the acronym in plain form, or a markdown link when the term carries a long
description below the table. The Definition cell gives the expansion plus one clause of
plain-language meaning or role in context.

```markdown
## Glossary

| Term                               | Definition                                                     |
|------------------------------------|----------------------------------------------------------------|
| API                                | Application Programming Interface - the frontend-backend contract |
| [RPO](#rpo-recovery-point-objective) | Recovery Point Objective - tolerable data loss measured as time |
| [SLO](#slo-service-level-objective)  | Service Level Objective - measurable service-quality target    |
```

**Long descriptions**

Terms that need more than an expansion get a `###` subsection below the index table, still inside
`## Glossary`, sorted alphabetically by term. Name each subsection `### TERM (Expansion)` when the
expansion is established, or `### TERM` when it is not. A term with a subsection links its table
cell to that subsection's anchor, for example `[SLO](#slo-service-level-objective)`. Derive the
anchor from the heading text: lowercase it, remove punctuation, and replace spaces with hyphens.

Choose the subset deliberately. Good candidates are operational objectives such as `SLO`, `RPO`,
and `RTO`, report-internal identifier prefixes such as `EVD`, `FND`, `RSK`, `REC`, `TDR`, and
`PAR`, and subject-specific terms whose role needs explanation. Most terms stay index-only.

```markdown
### SLO (Service Level Objective)

A measurable target for service quality, for example "99.9% of API requests succeed" or "p95
latency under 300ms". SLOs tell operators, and an audit, what "healthy" means quantitatively.
Without them there is no agreed threshold for when the platform is failing its users.
```

**Body linking**

Every occurrence of a glossary term in the report body is a markdown link. When the term has a
long-description subsection, link to that subsection's anchor, for example
`[SLO](#slo-service-level-objective)`. Otherwise link to the index table at `#glossary`, for
example `[API](#glossary)`.

Apply the rule to prose and table cells. Exempt:

- The Glossary section itself, including its index table and `###` descriptions.
- Headings, fenced code blocks, inline code, existing link text, and URLs.
- Occurrences inside a longer hyphenated or slashed identifier, such as `FND` inside
  `FND-SEC-001`, `REC` inside `REC-BE-01`, or `PAR` inside `PAR-10`, and occurrences inside a
  longer word, such as `SQL` inside `SQLite` or `API` inside `OpenAPI`. Link the whole compound
  instead when the compound itself is a glossary term, such as `[SI-API](#si-api)` or
  `[ISO/IEC](#glossary)`.
- Inflected forms keep the suffix inside the link text, for example
  `[SLOs](#slo-service-level-objective)`.

**Coverage**

Include every abbreviation and acronym used anywhere in the report body:

- Report-internal identifier prefixes such as `EVD`, `FND`, `RSK`, `REC`, `TDR`, and `PAR`.
- Priority tiers `P1`-`P4` and abbreviation-shaped tokens such as `N/A`.
- Technology and standard names such as `API`, `CWE`, `CVSS`, `OWASP`, `STRIDE`, `SBOM`,
  `SLO`, `RPO`, `RTO`, `PWA`, `SPA`, `CI/CD`, `TOTP`, `HMAC`, `CSP`, and `i18n`.
- Subject-specific terms established by the audited project, such as product or protocol names.

Each definition expands the abbreviation and adds one clause of plain-language meaning or role in
context, as in the SLO, RPO, and RTO examples above.

Do not list ordinary words, brand or product names that are not abbreviations, file extensions,
command names, or fixed vocabulary tokens that are complete words such as `PASS`, `FAIL`,
`UNKNOWN`, or `NOT SPECIFIED`. Do not invent expansions for product names the audited source
does not establish, describe the term's role instead.

When the report language is not English, keep each term in its original form and write the
definition in the report language, per the matching `translation/` file.

## Multi-Project Report Structure

When the audit covers more than one project in a repository or directory, the report uses a combined
structure. Each project is assessed independently and receives its own complete set of sections
within the report.

**Document Information** appears once at the top. The title uses the repository or directory name,
not a single project name. Include a `Projects` row in the table listing the audited projects.

**Project Inventory** appears immediately after Document Information. It lists each project with its
path, version, and a one-line description.

```
| Project        | Path           | Version | Description            |
|----------------|----------------|---------|------------------------|
| <project name> | <project path> | <ver>   | <one-line description> |
```

When the report language is not English, apply the column header translations from the matching
`translation/` file.

**Combined summary sections** appear immediately after the Project Inventory, so orientation
material precedes per-project detail.

The **Executive Summary** is a condensed combined summary. Write a short orientation paragraph,
then a compact table with one row per project:

```
| Project        | Score                   | Lowest              | Top Risks               | Readiness         |
|----------------|-------------------------|---------------------|-------------------------|-------------------|
| <project name> | <mean>/<scale> (<band>) | <dimension> <score> | <top RSK-XXX or `NONE`> | <readiness state> |
```

The **Changes Since Previous Audit** section is combined at report level when a previous report
exists. Give each compared project its own level-3 subsection inside this section and keep
project-qualified finding IDs. Do not repeat the section inside the per-project blocks.

**Per-project sections** follow the combined summary sections. Each project gets a level-2
heading (`##`) with the project name, followed by the full set of report sections for that
project:

- Executive Summary
- System Context (with the Technology Stack subsection)
- Health Dashboard
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment (with conditional subsections)
- Trade-off Analysis
- Threat Model *(conditional)*
- API Contract Conformance *(conditional)*
- Skill Definition Conformance *(conditional)*
- AI System Assessment *(conditional)*
- Standards Conformance *(conditional)*
- API Compatibility & Versioning Discipline *(conditional)*
- Strengths & What's Working
- Detailed Technical Findings
- Technical Debt Register *(conditional)*
- Unified Risk Register
- Actionable Remediation Roadmap

Use level-3 headings (`###`) for subsections within each project block.

**Finding IDs** are scoped per project. Each project's findings start at `FND-XXX-001`. Risk IDs and
recommendation IDs also reset per project. Prefix each finding heading with the project identifier
so the reader can navigate. For example: `### FND-ARC-001: [api-service] Missing input validation`.

**Shared sections** appear once at the end of the report, after all per-project sections:

- Trade-off Analysis (combined)
- Scope Exclusions
- Limitations and Unknowns
- Re-audit and Follow-up Plan *(conditional)*
- Validation Record
- References

The combined **Trade-off Analysis** holds only cross-project trade-offs. A trade-off is
cross-project only when the decision was made once and constrains more than one project, such
as a shared dependency choice or a repository-wide workspace or build decision. The same issue
type appearing independently in two projects is a repeated per-project finding, not a
cross-project trade-off, and stays in the per-project Trade-off Analysis after that project's
Architectural Assessment. The combined table adds a leading `Project` column. When no
cross-project trade-off qualifies, the section stays present and the table carries a single
`N/A` row with a one-line justification.

The Scope Exclusions, Limitations and Unknowns, Validation Record, and Re-audit sections cover
all projects. Qualify rows per project using the project identifier.

**Single-project reports** use the standard structure without the Project Inventory table and
without per-project level-2 headings. The sections appear directly under level-2 headings as in a
standard report.

## Executive Summary

Provide a compact overview a reader can absorb without the detail sections.

Precede the table with a one-line legend naming the band for each score range of the selected
scale, so no score appears before its band is defined:

- `1-10`: `1-3 Poor · 4-6 Average · 7-8 Good · 9-10 Excellent`
- `1-5`: `1-2 Poor · 3 Average · 4 Good · 5 Excellent`
- `1-3`: `1 Poor · 2 Average · 3 Excellent`
- `5 stars`: `★-★★ Poor · ★★★ Average · ★★★★ Good · ★★★★★ Excellent`
- `3 stars`: `★ Poor · ★★ Average · ★★★ Excellent`

Use a key-value table:

| Field          | Value                                                 |
|----------------|-------------------------------------------------------|
| System type    | <prototype / codebase / production system / proposal> |
| Scope          | <what was reviewed and what was excluded>             |
| Source basis   | <running system / inspected code / description>       |
| Maturity level | <maturity level>                                      |
| Overall score  | <score display>, lowest: <dimension> <score display>  |

Maturity level is one of: `Prototype`, `Early development`, `Pre-production`, `Production-ready`, or
`Undetermined`.

For numeric scales, use `<mean>/<scale> (<band>)` and `<score>/<scale>`. For `5 stars` or
`3 stars`, use the rounded star bar followed by the exact mean in parentheses, for example
`★★★☆☆ (3.4/5)` and `lowest: Security ★★☆☆☆`.

The Overall score row always pairs the unweighted mean with the lowest-scoring applicable
dimension and its score, so a weak pillar is never hidden inside the average. Exclude `N/A` and
`UNKNOWN` dimensions from both values. When several dimensions tie for the lowest score, name
them all. Omit the row only when no dimensions were scored.

When the report language is not English, apply the table header and field name translations from the
matching `translation/` file.

Do not add a "Summary description" row to this table. Long descriptive text in a table cell makes
the table unreadable in plain text. The summary description belongs in a paragraph after the table,
as described below.

**Summary description**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

Write one paragraph immediately after the table. State the system's purpose in one sentence.
Summarize the overall condition in one sentence. Note the maturity level and anchor it to evidence
from later sections. Mention any critical finding that the reader should know first. Keep the
paragraph to four sentences maximum. Break lines that exceed 100 characters per `STYLE.md`.

The maturity level must be justified by evidence in later sections, not asserted.

**Production Readiness Threshold**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

State the conditions and evidence required to justify `Production-ready` for the stated deployment.

Tie conditions to risk IDs and required verification, without inventing numeric coverage thresholds.

Distinguish adopted acceptance criteria from proposed improvements and identify who must confirm
unapproved criteria.

For readiness or due diligence, add an **Evidence And Decision Limits** paragraph stating which
required checks are documented, which were not run, critical uncertainties, and sign-off state.

Keep any "builds", "tests pass", "secure", or "production-ready" claim within the evidence actually
collected, carrying the same qualifications as the detailed findings.

Add **Readiness Cost** using `synthesis/remediation-roadmap.md`, with the supported range or
`INSUFFICIENT INFORMATION`, known subtotal, exclusions, and unestimated work.

For due diligence, summarize support continuity, ownership cost, roadmap, supplier, IP, and data
obligations, including missing business evidence.

Proposed targets and gates are not stakeholder-approved requirements until confirmed.

Incomplete required checks or unassigned verification ownership leave sign-off pending, regardless
of the scorecard average.

## Changes Since Previous Audit

Include this section only when a previously created audit report was found during intake, per
`synthesis/report-comparison.md`. Omit it entirely for a first audit. The absence of a previous
report is the normal case, so no omission note is needed in Scope Exclusions.

Open with a report reference table:

| Field            | Previous Report | Current Report |
|------------------|-----------------|----------------|
| File             | <path>          | <filename>     |
| Revision         | <revision>      | <revision>     |
| Date             | <date>          | <date>         |
| Detail level     | <level>         | <level>        |
| Evaluation scale | <scale>         | <scale>        |

When the previous report records no revision, show `1.0 (assumed)` in the Revision row.

When parameters differ between reports, state the difference in a paragraph below the table
before comparing content, since a scale or detail-level change affects comparability.

When the report language is not English, apply the column header translations from the matching
`translation/` file.

**Finding transitions**

Present a table of findings that changed remediation state or first appeared since the
previous report:

| Finding | Previous | Current | Note               |
|---------|----------|---------|--------------------|
| FND-XXX | Open     | Closed  | <closing evidence> |
| FND-XXX | Open     | Open    | still reproduces   |
| FND-XXX | -        | New     | first reported     |

A previous finding that no longer reproduces stays in the table as `Closed` with the evidence
that closes it, it is never silently dropped.

**Score delta**

Present a per-dimension score comparison:

| Dimension | Previous | Current | Direction |
|-----------|----------|---------|-----------|
| <name>    | <score>  | <score> | Up        |

Direction uses `Up`, `Down`, or `Unchanged`. When the evaluation scale changed between
reports, mark the direction `UNKNOWN` for affected dimensions instead of comparing raw numbers.

After the tables, write one paragraph per material change. Summarize which findings moved
state, which `RSK-XXX` risks were added or mitigated, and which category statuses changed.
Anchor every claim to a `FND-XXX`, `RSK-XXX`, or `EVD-XXX` in the current report.

**Rules**

- New findings keep their assigned `FND-XXX` IDs and appear as `New` in the transition table.
- Mark a comparison element `UNKNOWN` when the previous report cannot supply it, do not guess.
- For multi-project reports, place this section inside each project block and qualify every
  identifier with the project identifier.
- Do not include plaintext secrets, passwords, or cryptographic keys in comparison text.

## System Context

Describe the system as understood from the input. Present the factual context without critique.

| Aspect                 | Detail                                            |
|------------------------|---------------------------------------------------|
| Functional description | <what the system does>                            |
| Architecture overview  | <high-level structure>                            |
| Key components         | <named components or modules>                     |
| External dependencies  | <services, libraries, platforms>                  |
| Assumptions            | <only if explicitly stated, else `NOT SPECIFIED`> |

When the report language is not English, apply the table header and aspect name translations from
the matching `translation/` file.

Mark any unknown aspect as `NOT SPECIFIED`.

### Technology Stack

Present a factual inventory of the technologies the subject uses. Describe the stack only, do not
judge it here.

Use a key-value table:

| Layer            | Technology                                            |
|------------------|-------------------------------------------------------|
| Languages        | <languages and versions>                              |
| Frameworks       | <application and UI frameworks>                       |
| Runtime/Platform | <runtime, OS, or host platform>                       |
| Build tooling    | <build system, bundler, compilers>                    |
| Test tooling     | <test frameworks and runners>                         |
| Package manager  | <dependency and package manager>                      |
| Key libraries    | <notable third-party libraries>                       |
| Data stores      | <databases, caches, file formats>, or `NOT SPECIFIED` |
| Target platforms | <where the software runs or ships>                    |

Anchor each entry to evidence, such as a manifest, lockfile, or config file. Mark any layer the
input does not reveal as `NOT SPECIFIED`. Add or omit rows to fit the subject, but keep the layer
names in this column and translate them into the report language.

After the tables, add further subsections for major components (e.g., `### Backend`, `### Frontend`,
`### Deployment`). Put exactly one empty line after each subsection header before the first
sentence. Separate every sentence with an empty line.

For operated systems, add a compact **Operational Objectives** table with metric, target, measured
result, window, source, and owner, using the NFR and operational-readiness guides.

Keep SLIs/SLOs, error budgets, RPO/RTO, and DORA delivery measures distinct.

Use `UNKNOWN` for missing measurements and `NOT SPECIFIED` for unapproved targets.

For technical due diligence, add a **Due Diligence Coverage** table with concern, status, evidence,
and missing artifact or next step.

Cover continuity, ownership cost, roadmap feasibility, supplier continuity, IP rights, and data
obligations using `assessment/operational-readiness.md` and its related category guides.

Add a data-lifecycle summary under Compliance findings when relevant, referencing categories,
stores, recipients, retention/deletion, and the applicable obligation basis.

## Health Dashboard

Present the quantitative health summary in a consolidated view. This section contains the Risk Heat
Map, the Scorecard Summary, and the Team & Continuity line.

**Risk Heat Map**

Provide a consolidated Likelihood vs Impact matrix summarizing the top risks. Use a table:

| Impact   | LOW | MEDIUM | HIGH |
|----------|-----|--------|------|
| CRITICAL |     |        |      |
| HIGH     |     |        |      |
| MEDIUM   |     |        |      |
| LOW      |     |        |      |

When the report language is not English, apply the axis label translations from the matching
`translation/` file.

Populate cells with `RSK-XXX` identifiers from the Unified Risk Register. Leave empty cells blank.
Do not include plaintext secrets, passwords, or cryptographic keys in this summary. Use generic
descriptions or masked placeholders.

**Scorecard Summary**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

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
| AI Provenance           |       |       |
| Originality & Licensing |       |       |
| Skill Definition        |       |       |
| API Compatibility       |       |       |

The API Compatibility dimension is `N/A` unless the subject is a reusable library or package,
per `assessment/api-compatibility.md`.

Render each Score cell in the selected evaluation scale: `7/10` for `1-10`, `4/5` for `1-5`,
`2/3` for `1-3`, `★★★★☆` for `5 stars`, and `★★☆` for `3 stars`. Render `UNKNOWN` and `N/A`
as text, not as star bars.

When the report language is not English, apply the translations from the matching `translation/`
file.

**Team & Continuity**

Write one line summarizing contributor and continuity evidence collected during Evidence
Gathering: author concentration, commit cadence, tag and release history, and any documented
ownership or maintenance statement. Anchor it to evidence IDs. When Git history or repository
data was not in scope, mark it `NOT COLLECTED` rather than omitting the line. Keep it neutral
and aggregate, never personal. Commit concentration is a proxy for continuity, not a measure of
operational access or expertise.

When the report language is not English, apply the heading translation from the matching
`translation/` file.

## High-Level Observations

Surface the most important findings in a compact table a reader can scan before reading the detail
sections. Include at most five observations. Each observation should be a single concrete finding,
not a category summary.

Use this single-column table:

| Observation   |
|---------------|
| <observation> |

When the report language is not English, apply the table header translation from the matching
`translation/` file.

Write one paragraph per observation immediately after the table, in the same order as the table
rows. Start each paragraph with a bold heading on its own line (the observation text, abbreviated if
needed), then add an empty line, then the body. Each paragraph explains why the observation matters
and what risk or opportunity it represents. Anchor every claim to a specific finding in the Detailed
Technical Findings.

Keep each observation brief. The full technical detail lives in the numbered finding blocks later in
the report. This section exists to give non-technical readers a fast-skim path.

## Auditing Methodology

Define how the audit was conducted and the framework used to evaluate findings.

The earlier dashboard is a summary, its scores refer to the methodology and rubric here.

**Methodology overview**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

State that the audit uses evidence-based reasoning across 18 core assessment categories grouped into
six pillars, plus conditional assessments (data flow, design patterns, threat model, API contract,
skill definition, standards conformance) applied when the subject warrants them, and the conditional
API Compatibility & Versioning Discipline pillar for libraries and packages. List the pillars:

- **Architecture & Design** - Design principles, maintainability, change management, documentation,
  non-functional requirements
- **Code Quality** - Testing, code quality, stack best practices
- **Security & Compliance** - Security, compliance and data protection
- **Infrastructure & CI/CD** - Dependencies, deployment, rollback, observability, error handling,
  operational readiness
- **AI Provenance & Code Origin** - Explicit attribution, generated-artifact validation, and SDLC
  evidence, without authorship inference from style
- **Copyrights & Originality** - Code originality, license compliance, attribution, dependency
  license compatibility
- **API Compatibility & Versioning Discipline** - Public API stability, versioning consistency, and
  breaking-change tracking. Conditional, applied only when the subject is a reusable library or
  package.

When the report language is not English, apply the pillar name translations from the matching
`translation/` file.

**Reference standards**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

Name the external standards the audit aligns with, so the methodology is credible to an external
reader. Cite only the standards actually applied to the subject. Typical references:

- **ISO/IEC 25010:2023** - nine-characteristic product quality coverage, using the explicit
  crosswalk
  in `synthesis/project-scorecard.md`, not an ISO scoring formula.
- **OWASP ASVS 5.0.0** - selected version-qualified security controls, with scope and level stated.
- **CWE and CVSS** - weakness classification and vulnerability severity where applicable.
- **SSDF and SAMM** - selected secure-development practices when process evidence is assessed.
- **OWASP Top 10 (2025)** and, for APIs, **OWASP API Security Top 10 (2023)** - for the security
  category coverage.
- **NIST SP 800-30** - risk assessment process, for the risk register and threat model.
- **STRIDE** - threat enumeration framework, when a threat model is included.
- **CISQ / SQALE** - structural quality and technical-debt cost model, when a technical debt
  register is included.
- **ISO 19011** and **NIST RMF** - audit follow-up and continuous monitoring, when a re-audit plan
  is included.

Beyond the generic standards above, name the stack-specific canonical sources applied, selected
per `references/stack-standards.md`: for example the Rust API Guidelines and the RustSec
Advisory Database for Rust, or the Framework Design Guidelines and NuGet package authoring best
practices for .NET. Stack-specific sources are the primary reference set for the detected stack,
not optional decoration.

Cite a standard only when its corresponding section or assessment is present in the report. Do not
list a standard that was not applied.

**Audit evidence statement**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

Begin the Methodology section with 2-3 sentences stating exactly what was inspected. Include:

- The number of source files, test files, and configuration files reviewed. State whether
  `.gitignore` exclusions were applied. If `.gitignore` was absent, record that fact without
  assuming a defect.
- Whether Git history was examined.
- Which documented check results, such as CI output, coverage reports, or scan artifacts, were
  supplied or committed.

Example: "This audit inspected 147 source files, 8 test files, and 4 configuration files from the
repository root, excluding files listed in `.gitignore`. Git commit history was reviewed for the
last 15 commits. No builds, tests, or tools were executed, all findings are based on static
inspection of the repository contents."

**Verification And Evidence Ledger**

Include the per-project check summary and evidence records from `process/audit-workflow.md`.

| Evidence ID | Project   | Check / Source      | Execution | Result   | Artifact      |
|-------------|-----------|---------------------|-----------|----------|---------------|
| EVD-001     | <project> | <source or command> | <state>   | <result> | <path or gap> |

Place documented commands, source locations, revisions, declared tool or report versions,
exclusions, and limitations below the table rather than abbreviating away traceability.

An anchor may be a line range or a mechanism description when no single line carries the defect,
an honest range beats a fabricated line.

Include documented checks that were not run, and label supplied or committed results as
reported.

For dependencies, summarize inventory/SBOM scope, schema version, license policy, advisory triage,
and artifact paths, not just direct manifest versions. When no SBOM exists, record the
source-derived component inventory produced per `references/dependency-manifests.md`, labeled
as manifest-derived rather than shipped content.

For testing, distinguish inspected test counts from documented coverage and mutation outcomes.

Link every finding to supporting `EVD-XXX` records.

Evidence IDs are scoped per report and are not stable across revisions. Cite a previous report's
evidence as `EVD-XXX` plus the report name, for example `EVD-017 in AUDIT-1.2`.

**Severity definitions**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

Add a 4-row rubric defining each qualitative severity band. These definitions anchor the severity
values used in findings and risks.

| Severity | Meaning                  | Readiness Treatment       |
|----------|--------------------------|---------------------------|
| CRITICAL | Critical contextual risk | Gate resolution           |
| HIGH     | Major contextual risk    | Gate resolution           |
| MEDIUM   | Material contained risk  | Track and plan            |
| LOW      | Limited contextual risk  | Proportionate improvement |

Derive these bands from the impact/likelihood matrix in `synthesis/risk-register.md`.

Print one line of clarification under the severity table in every report: severity derives from
the impact/likelihood matrix, not CVSS. Do not assign a fixed likelihood to each severity band
or confuse CVSS with this matrix.

Use `UNKNOWN` for an unsupported rating and list unrated risks separately from the heat map.

When the report language is not English, apply the column header and severity description
translations from the matching `translation/` file.

Use these definitions consistently across the Detailed Technical Findings and the Unified Risk
Register.

## Scoring Rubrics

Present the scoring framework after Auditing Methodology and before detailed finding assessments.

Apply `process/readiness-and-scoring.md` for deterministic status-to-score mapping, confidence,
score caps, maturity, readiness gates, and multi-project aggregation.

The earlier dashboard summarizes these scores and should reference this rubric.

**Scoring rubric**

Present the rubric matrix that defines what constitutes each score band. Use the default `1-10`
scale unless the user requested `1-5`, `1-3`, `5 stars`, or `3 stars`.

For the `1-10` scale:

| Band      | Score Range | Definition                                                   |
|-----------|-------------|--------------------------------------------------------------|
| Excellent | 9-10        | Capability is comprehensive and verified by strong evidence  |
| Good      | 7-8         | Capability is solid overall, minor or noticeable gaps exist  |
| Average   | 4-6         | Capability is present but uneven, limited, or inconsistent   |
| Poor      | 1-3         | Capability is minimal, fragmentary, or absent where required |

When the report language is not English, apply the band name and definition translations from
the matching `translation/` file.

For the `1-5` and `5 stars` scales:

| Band      | Score Range | Definition                                                  |
|-----------|-------------|-------------------------------------------------------------|
| Excellent | 5           | Capability is comprehensive and verified by strong evidence |
| Good      | 4           | Capability is solid with minor gaps                         |
| Average   | 3           | Capability is adequate but uneven                           |
| Poor      | 1-2         | Capability is minimal, limited, or absent where required    |

For the `1-3` and `3 stars` scales:

| Band      | Score | Definition                                                  |
|-----------|-------|-------------------------------------------------------------|
| Excellent | 3     | Capability is comprehensive and verified by strong evidence |
| Average   | 2     | Capability is adequate but uneven                           |
| Poor      | 1     | Capability is minimal, limited, or absent where required    |

When the report language is not English, apply the same band translations from the matching
`translation/` file.

For `5 stars`, render each score as a five-position star bar using `★` for filled positions and
`☆` for empty positions, such as `★★★☆☆` for `3`. For `3 stars`, use three positions, such as
`★★☆` for `2`. Render `UNKNOWN` and `N/A` as text, not as star bars.

**Zero is not a score.** The value `0` is reserved and never used. When a dimension cannot
apply, mark it `N/A`.

Apply the ISO/IEC 25010:2023 crosswalk in `synthesis/project-scorecard.md` and show coverage gaps.

For every numeric or star score, include evidence references and confidence in its supporting
paragraph.

If an overall score is shown, disclose its formula, weights, rounding, and coverage denominator.
State the lowest-scoring applicable dimension and its score alongside the mean, per
`synthesis/project-scorecard.md`.

## Architectural Assessment

Provide an architectural critique against industry baselines. Evaluate coupling, cohesion, state
management, separation of concerns, and pattern consistency against the stated constraints. Anchor
every claim to a concrete file path or design decision. Do not judge the stack choice itself.

Structure this section with four subsections: `### What Works`, `### What Needs Attention`,
`### Design Principles`, and `### Industry Baseline Comparison`. Use Title Case for all subsection
titles. Put exactly one empty line after each subsection header before the first sentence.

When listing multiple related items (e.g., typical production practices), use a bullet list rather
than an inline comma-separated paragraph. Put an empty line between the intro sentence and the first
bullet.

The Architectural Assessment may also carry up to three conditional subsections, included only when
their criteria are met. When included, place them in this order, after `### Design Principles` and
before `### Industry Baseline Comparison`.

### Design Principles

Always include this subsection. Evaluate the code against the SOLID principles and DRY per
`assessment/design-principles.md`. Present one row per principle:

| Principle             | Status | Evidence |
|-----------------------|--------|----------|
| Single Responsibility |        |          |
| Open/Closed           |        |          |
| Liskov Substitution   |        |          |
| Interface Segregation |        |          |
| Dependency Inversion  |        |          |
| DRY                   |        |          |

Reuse evidence already gathered for other findings instead of re-investigating it. When a
violation was already described elsewhere, for example a Liskov Substitution breach logged as a
contract defect, name and cross-reference that finding here rather than duplicating the analysis.
Mark each principle `N/A` when no source was inspected for it.

### Data Flow Diagram

Include this subsection only when the system moves data across a trust boundary, per
`assessment/data-flow.md`. It is the foundation for the Threat Model section.

Present a Level-0 (context) and a Level-1 (decomposition) view. Use a fenced ASCII block or a flow
table. Then list the trust boundaries.

**Level-0 (context)**

```
    ╭────────────╮         ╭──────────────╮
    │            │         │              │
    │ MCP Client │────────>│ SQLite Index │
    │            │         │              │
    ╰────────────╯         ╰──────────────╯
            │
            │
            v
    ╭─────────────╮         ╭──────────────╮
    │             │         │              │
    │ REST Client │────────>│ Filesystem   │
    │             │         │              │
    ╰─────────────╯         ╰──────────────╯
            ^
            │
    ╭────────────╮
    │            │
    │ Git Remote │
    │            │
    ╰────────────╯
            ^
            │
    ╭──────────────╮
    │              │
    │ Index Server │
    │              │
    ╰──────────────╯
```

**Trust boundaries**

| Boundary        | From    | To         | Crossing Control      |
|-----------------|---------|------------|-----------------------|
| Network ingress | Client  | Auth layer | JWT validation        |
| Storage         | Handler | Filesystem | Path canonicalization |

Use framed nodes with box-drawing characters for every DFD element.

Each frame must have exactly three content rows: an empty line, a centered label, and an empty line.

Keep exactly one space between the frame border and the label text on all sides. Do not use two
spaces or asymmetric padding.

Do not enclose labels in brackets. Write the label as plain centered text without `[..]`, `(..)`, or
`{..}`.

Flow arrows (`─>`, `│`) must align with the center of the frame they connect to.

When placing a label above or below a horizontal arrow, the label row must span the exact same width
as the arrow row so the frames above and below remain aligned.

Anchor every node to a file or module.

### Design Patterns

Include this subsection only when the codebase exhibits recurring structure, per
`assessment/design-patterns.md`.

Present a table of the patterns in use with a fitness verdict, then describe each material pattern
or anti-pattern with evidence.

| Pattern        | Location                   | Assessment | Description                                      |
|----------------|----------------------------|------------|--------------------------------------------------|
| Repository     | `KnowledgeBase` trait      | PASS       | Clean abstraction with injectable implementation |
| Strategy       | hybrid search weighting    | PARTIAL    | Hardcoded, not runtime interchangeable           |
| Factory Method | `build_router` per handler | FAIL       | Duplicated construction logic, anti-pattern      |

Name patterns using their standard GoF or POSA names. Cross-reference any anti-pattern that is also
a code-origin signal to its `FND-AIP-XXX` finding.

### Architecture Decision Records

Include this subsection only when the system is production-bound with significant decisions, per the
ADR gap guidance in `assessment/change-management.md`.

Present a table of decisions that should carry an ADR, each marked `Recorded` or `Missing`, anchored
to the code that embodies the decision.

| Decision             | Location                  | ADR Status |
|----------------------|---------------------------|------------|
| Data store choice    | `Cargo.toml`, `src/db.rs` | Missing    |
| Web framework choice | `Cargo.toml`              | Missing    |
| Session state model  | `main.rs`                 | Missing    |

Missing decision rationale limits confidence regardless of origin, do not infer AI authorship or
an AI default from absent ADRs.

## Trade-off Analysis

Present engineering trade-offs immediately after the Architectural Assessment, in the same pass as
the decisions they discuss. A trade-off is a deliberate exchange of one quality for another.

Use a table with this fixed column order:

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Trade-off**: a short name for the tension.
- **Context**: the stated constraint or goal that frames the choice, or `NOT SPECIFIED`.
- **Option A**: the quality gained and the quality reduced for the first side.
- **Option B**: the quality gained and the quality reduced for the alternative.
- **Evidence**: what in the system shows this trade-off.
- **Implication**: the neutral consequence under the stated context.

**Rules**

- Frame each trade-off against a stated constraint. If no constraint is stated, put `NOT SPECIFIED`
  in Context and present the trade-off without judging the choice.
- Do not label either side as right or wrong outside an explicit recommendation request.
- A choice that fits the stated context is not a weakness, even if it would be unusual in a
  different context.
- Keep cell language neutral and anchored to evidence.
- Trade-off reasoning may also be embedded into individual finding blocks (under Description or
  Impact) when it directly explains a specific finding. The standalone table here surfaces the
  system-level tensions.
- For a multi-project report, each project block carries its own Trade-off Analysis after that
  project's Architectural Assessment. A combined report-level Trade-off Analysis holds only
  cross-project trade-offs, per the Multi-Project Report Structure section.
- When the trade-off analysis includes an explicit recommendation, that recommendation must also
  appear as a `REC-XXX` entry in the Actionable Remediation Roadmap, traced to the relevant
  `FND-XXX`.

## Threat Model

Include this section only when the system has a security-relevant attack surface, per
`assessment/threat-model.md`. Omit it for a single-user local utility with no trust boundary, and
note the omission in Scope Exclusions.

Apply STRIDE to the evidenced trust boundaries in the Data Flow Diagram.

Identify selected NIST SP 800-30 or ASVS requirements only when actually assessed, do not claim
ASVS Level 2 coverage merely because a threat table exists.

Present one table keyed by trust boundary and STRIDE category, then describe each material threat
with evidence and its linked `FND-XXX` and `RSK-XXX`.

| Boundary        | Threat (STRIDE)   | Threat Description                | Mitigating Control   | Finding     |
|-----------------|-------------------|-----------------------------------|----------------------|-------------|
| Network ingress | Spoofing          | Token forgery if signing key weak | JWT HS256 validation | FND-SEC-XXX |
| Write path      | Tampering         | Path traversal on write           | None (gap)           | FND-SEC-XXX |
| API surface     | Denial of Service | No rate limiting                  | None (gap)           | FND-SEC-XXX |

The six STRIDE categories are `Spoofing`, `Tampering`, `Repudiation`, `Information Disclosure`,
`Denial of Service`, and `Elevation of Privilege`. Every unmitigated threat must trace to a finding
and a risk. Never output plaintext secrets when describing an information-disclosure threat.

When the report language is not English, apply the column header translations from the matching
`translation/` file.

## API Contract Conformance

Include this section only when the system exposes an API, per `assessment/api-contract.md`. Omit it
entirely for a system with no API surface, and note the omission in Scope Exclusions.

Present a conformance table across the evaluated dimensions, then describe each gap with evidence
and its linked `FND-XXX`. Map each API security gap to its OWASP API Security Top 10 (2023) code
where one applies.

| Dimension                  | Status  | Evidence                                        |
|----------------------------|---------|-------------------------------------------------|
| Specification present      | PASS    | `openapi/openapi.yaml`                          |
| Schema validation enforced | PARTIAL | typed deserialization, no rejection tests       |
| Adopted error contract     | FAIL    | observed response contradicts declared schema   |
| Versioning strategy        | UNKNOWN | compatibility policy not supplied               |
| Spec-to-code agreement     | PARTIAL | `/health` marked `security: []` but behind auth |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

## Skill Definition Conformance

Include this section only when the subject is an Agent Skill, per `assessment/skill-definition.md`.
Omit it entirely for a project that is not a skill, and note the omission in Scope Exclusions.

Present a conformance table across the evaluated dimensions, then describe each gap with evidence
and its linked `FND-XXX`.

| Dimension                | Status  | Evidence                                               |
|--------------------------|---------|--------------------------------------------------------|
| Frontmatter present      | PASS    | `SKILL.md` has YAML frontmatter with required fields   |
| Name field conformance   | PASS    | `name` is lowercase, matches directory, under 64 chars |
| Description conformance  | PARTIAL | Description is 1200 chars, exceeds 1024-char limit     |
| Optional field validity  | PASS    | `license`, `compatibility`, `metadata` all valid       |
| Directory structure      | PASS    | `scripts/`, `references/` directories present          |
| Progressive disclosure   | PASS    | `SKILL.md` is 180 lines, references split out          |
| File reference integrity | FAIL    | `references/missing.md` referenced but does not exist  |
| Description triggering   | PARTIAL | Description lacks specific trigger keywords            |
| Body content quality     | PASS    | Instructions, examples, and edge cases present         |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

## AI System Assessment

Include this section only when the project trains, serves, or materially depends on an AI or
machine-learning system, per `assessment/ai-system.md`.

Keep this section distinct from AI-generated-code provenance. A project can have AI-assisted source
without having an AI system, and an AI system can contain no evidence about how its source was authored.

Present the evaluated lifecycle, model and data provenance, evaluation evidence, safety boundaries,
operational controls, and unresolved limitations. Use NIST AI RMF or ISO/IEC 42001 only when the
selected practices were actually assessed.

## Standards Conformance

Include this section only when the project contains documented development standards, per
`assessment/standards-conformance.md`. Omit it entirely for a project with no development standards
documents, and note the omission in Scope Exclusions.

This section evaluates two dimensions: whether the codebase conforms to the project's documented
development standards, and whether those standards are themselves consistent with established good
practices for the technology stack, programming language, and software type.

**Standards inventory**

List the development standards documents found in the project:

| Document | Path   | Stack Coverage                         |
|----------|--------|----------------------------------------|
| <title>  | <path> | <languages, frameworks, software type> |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

**Code conformance**

Present a conformance table across the areas the standards cover, then describe each gap with
evidence and its linked `FND-XXX`:

| Area                  | Standard Rule         | Status  | Evidence                                  |
|-----------------------|-----------------------|---------|-------------------------------------------|
| Language version      | <rule from standards> | PASS    | <file or config matching the rule>        |
| Project structure     | <rule from standards> | PARTIAL | <file or pattern diverging from the rule> |
| Naming conventions    | <rule from standards> | FAIL    | <file or pattern violating the rule>      |
| Error handling        | <rule from standards> | UNKNOWN | <not enough evidence to judge>            |
| Testing               | <rule from standards> | PASS    | <test files matching the rule>            |
| Formatting and lint   | <rule from standards> | PARTIAL | <CI config present, not enforced>         |
| Dependency management | <rule from standards> | PASS    | <manifest and lockfile matching the rule> |
| Security              | <rule from standards> | FAIL    | <file or pattern violating the rule>      |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

**Standards quality**

Evaluate whether the documented standards are consistent with established good practices for the
stack. Anchor every judgement to a named external best practice, style guide, or convention:

| Area   | Standards Position             | External Best Practice  | Alignment                      |
|--------|--------------------------------|-------------------------|--------------------------------|
| <area> | <what the standards prescribe> | <named external source> | Aligned / Partially / Diverges |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

After the table, describe each divergence with evidence. Name the external source and explain how
the standards position differs from the established practice. Cross-reference any conformance gap
that also produces a `FND-XXX` finding.

## API Compatibility & Versioning Discipline

Include this section only when the subject is a reusable library or package, per
`assessment/api-compatibility.md`. Omit it entirely for a deployable service or application, and
note the omission in Scope Exclusions.

Present a conformance table across the evaluated dimensions, then describe each gap with evidence
and its linked `FND-XXX`.

| Dimension                  | Status  | Evidence                                          |
|----------------------------|---------|---------------------------------------------------|
| Public surface tracked     | PARTIAL | API baseline or exports list, or none found       |
| Compatibility gate present | FAIL    | No ApiCompat or semver-checks configuration found |
| Versioning scheme declared | PASS    | `VERSIONING.md` names the scheme                  |
| Versioning practice        | PARTIAL | Tag and changelog history vs the declared scheme  |
| Deprecation policy         | UNKNOWN | Deprecation markers and removal timeline          |
| Breaking changes tracked   | FAIL    | Known items bound to a named future major version |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

After the table, list each known future-breaking item and the version it is bound to. An item with
no target version is open-ended and must be named as such.

Configured tooling is evidence of intent, not proof of execution. Treat a configured gate as
`Reported` unless the audit can verify it ran.

## Strengths & What's Working

Add a short section with 5-8 bullet points acknowledging what the system does well. This balances
the tone of the report and anchors the scorecard with positive baselines.

Use a bullet list. When a strength requires more than one sentence, start the bullet with a bold
heading on its own line, then add an empty line, then the body. Anchor every claim to a concrete
file, pattern, or decision. Examples:

```markdown
- **TypeScript strict mode is enabled in both backend and frontend**.

`backend/tsconfig.json` and `frontend/tsconfig.app.json` both set `"strict": true`.

This catches a broad class of type errors at compile time.
```

For single-sentence strengths, keep them as plain bullets:

- Dependency injection is consistently applied in `Program.cs`, enabling testable service
  registration.
- Nullable reference types are enabled project-wide, reducing null-reference defects.
- SQL database connection pooling is configured with sensible `MinPoolSize` and `MaxPoolSize`
  values.
- JWT bearer authentication is implemented with standard ASP.NET Core middleware.

Do not invent strengths. Only list what is evidenced in the provided files.

Use fewer than the suggested count when evidence is thin and state the limitation.

## Detailed Technical Findings

Present all findings grouped under six pillars, plus the conditional API Compatibility & Versioning
Discipline pillar when the subject is a reusable library or package. Each finding receives a unique
deterministic index.

**Summary table:**

When the report language is not English, apply the heading translation from the matching
`translation/` file.

Present a compact summary of all findings:

| Finding ID  | Pillar                                    | Severity   | Title   | Status   | Remediation Status |
|-------------|-------------------------------------------|------------|---------|----------|--------------------|
| FND-ARC-001 | Architecture & Design                     | <severity> | <title> | <status> | Open               |
| FND-CQY-001 | Code Quality                              | <severity> | <title> | <status> | Open               |
| FND-SEC-001 | Security & Compliance                     | <severity> | <title> | <status> | Open               |
| FND-INF-001 | Infrastructure & CI/CD                    | <severity> | <title> | <status> | Open               |
| FND-AIP-001 | AI Provenance & Code Origin               | <severity> | <title> | <status> | Open               |
| FND-CPR-001 | Copyrights & Originality                  | <severity> | <title> | <status> | Open               |
| FND-API-001 | API Compatibility & Versioning Discipline | <severity> | <title> | <status> | Open               |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Pillar abbreviations for IDs:

- `ARC` - Architecture & Design
- `CQY` - Code Quality
- `SEC` - Security & Compliance
- `INF` - Infrastructure & CI/CD
- `AIP` - AI Provenance & Code Origin
- `CPR` - Copyrights & Originality
- `API` - API Compatibility & Versioning Discipline (conditional, libraries and packages only)

When the report language is not English, apply the pillar name translations from the matching
`translation/` file.

Severity values: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
Status values: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`.

**Detailed findings**

After the summary table, write one block per finding in the same order. Use this exact markdown
block pattern:

```markdown
### FND-[PILLAR]-[NUMBER]: [Clear, Concise Title of Finding]

* **Pillar:** [Architecture & Design | Code Quality | Security & Compliance | Infrastructure & CI/CD | AI Provenance & Code Origin | Copyrights & Originality | API Compatibility & Versioning Discipline]
* **Severity:** [Critical | High | Medium | Low]
* **Target Files/Modules:** [Exact paths or components evaluated]
* **Requirement Basis:** [Applicable requirement or explicitly optional improvement]
* **Evidence:** [EVD IDs, source lines, and inspected/executed/reported/inferred basis]
* **Confidence:** [HIGH / MEDIUM / LOW with rationale]
* **Verification State:** [Observed result, or pending with limitations]
* **Counter-check:** [Refuting evidence examined and remaining uncertainty]
* **Security Classification:** [CWE and rationale, CVSS version/vector/score or gap, or N/A]
* **Description:** [Detailed technical explanation of the discovered state, architectural anti-pattern, or code flaw]
* **Impact:** [Concrete operational, business, or security consequence if left unremediated]
* **Remediation Recommendation:** [Step-by-step technical guidance to resolve the finding]
* **Verification Method:** [Specific test, command, or process to confirm the fix is successful]
```

When the report language is not English, apply the bullet label translations from the matching
`translation/` file.

Each finding must cite concrete evidence: file paths, config keys, commands, or direct quotes. Do
not crowd the bullet list with long prose. Use short sentences separated by blank lines, each
sentence stands on its own line with an empty line between consecutive sentences.

Every finding must include a detailed Description, Impact, Remediation Recommendation, and
Verification Method. A finding with only a title and status is incomplete. The Description must
explain what the discovered state is, where it is located (citing file paths and line numbers), and
why it constitutes a finding. The Impact must state the concrete consequence. The Remediation
Recommendation must provide step-by-step technical guidance. The Verification Method must specify a
test or command to confirm the fix.

When referencing secrets, credentials, or keys in the Description or Impact fields, replace exact
values with `[REDACTED]` or generic descriptions such as "plaintext database credentials found in
tracking file".

Keep trade-offs in the standalone section and embed relevant reasoning in the finding.

Every `CRITICAL` or `HIGH` finding needs an explicit counter-check.

For applicable security findings, place full CWE/CVSS rationale and versioned OWASP/ASVS mappings
below the summary table, following `assessment/security-review.md`.

Do not assign a CVSS score or adverse severity to an ordinary positive observation.

Place strengths in Strengths & What's Working rather than using `PASS` as a severity.

In shared sections, qualify IDs with the project identifier, including evidence, debt, risk, and
recommendation links.

## Technical Debt Register

Include this section only when the assessment surfaces structural debt distinct from risks, per
`synthesis/debt-register.md`. Omit it when no such debt exists.

This register is distinct from the Unified Risk Register: risks describe what could go wrong, debt
describes accumulated cost that is already present.

Use the CISQ categories and SQALE-inspired cost guidance in `synthesis/debt-register.md`, claiming
full method application only when its models were used.

Use this fixed column order:

| Debt ID | Debt Item   | Category         | Source Finding | Remediation Cost | Cost of Delay | Status |
|---------|-------------|------------------|----------------|------------------|---------------|--------|
| TDR-001 | <debt item> | <characteristic> | <FND ID>       | <range or gap>   | <cost or gap> | Open   |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Category is one of the CISQ characteristics: `Reliability`, `Performance Efficiency`, `Security`,
`Maintainability`. Every item must trace to a `FND-XXX` or be marked `Direct observation` with a
cited file. Do not duplicate security risks here, those belong in the Unified Risk Register.

After the table, write one block per debt item in the same order. Use this exact markdown block
pattern:

```markdown
### TDR-[NUMBER]: [Clear, Concise Title of Debt Item]

* **Category:** [Reliability | Performance Efficiency | Security | Maintainability]
* **Source Finding:** [FND-XXX or Direct observation]
* **Description:** [Detailed technical explanation of the debt, what it is, where it is located, and why it constitutes debt]
* **Remediation Cost:** [Supported effort range, unit, basis, confidence, or gap token]
* **Cost of Delay:** [Supported ongoing cost, horizon, basis, confidence, or gap token]
* **Status:** [Open | In progress | Resolved]
```

When the report language is not English, apply the bullet label translations from the matching
`translation/` file.

## Unified Risk Register

This section builds a cross-referenced risk table from the risks surfaced during assessment. Every
risk must trace back to a specific finding.

**Table format:**

| Risk ID | Risk            | Source Finding | Impact        | Likelihood    | Severity   | Mitigation |
|---------|-----------------|----------------|---------------|---------------|------------|------------|
| RSK-001 | <concrete risk> | FND-XXX        | <consequence> | <probability> | <severity> | <action>   |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Risk ID**: `RSK-[001]` ascending.
- **Risk**: a concrete technical risk, stated neutrally.
- **Source Finding**: the `FND-XXX` identifier that produced this risk.
- **Impact**: the consequence if the risk is realized.
- **Likelihood**: how probable the risk is given the evidence.
- **Severity**: one of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- **Mitigation**: a neutral, optional action that would reduce the risk.

**Rating guidance**

Rate impact and likelihood from evidence, not intuition.

Impact bands:

- `LOW`: limited or cosmetic effect.
- `MEDIUM`: degraded function or contained outage.
- `HIGH`: major function loss or data integrity concern.
- `CRITICAL`: data loss, breach, or full outage.

Likelihood bands:

- `LOW`: would require an unusual combination of conditions.
- `MEDIUM`: plausible under normal operation.
- `HIGH`: expected to occur without intervention.

**Severity matrix**

| Impact \ Likelihood | LOW    | MEDIUM   | HIGH     |
|---------------------|--------|----------|----------|
| CRITICAL            | HIGH   | CRITICAL | CRITICAL |
| HIGH                | MEDIUM | HIGH     | CRITICAL |
| MEDIUM              | LOW    | MEDIUM   | HIGH     |
| LOW                 | LOW    | LOW      | MEDIUM   |

When the report language is not English, apply the axis label translations from the matching
`translation/` file.

**Rules**

- One row per distinct risk. Do not merge unrelated risks.
- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- State each risk as a property of the system, never as a fault of a person.
- When a rating is unsupported, use `UNKNOWN`, state the missing evidence, and omit it from
  numeric aggregation and heat-map placement, per `synthesis/risk-register.md`.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for
  directives.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

After the table, write one block per risk in the same order. Use this exact markdown block pattern:

```markdown
### RSK-[NUMBER]: [Clear, Concise Title of Risk]

* **Source Finding:** [FND-XXX]
* **Description:** [Detailed technical explanation of the risk, what could go wrong, and under what conditions]
* **Impact:** [Concrete consequence if the risk is realized]
* **Likelihood:** [How probable the risk is given the evidence, with justification]
* **Severity:** [LOW | MEDIUM | HIGH | CRITICAL]
* **Confidence:** [HIGH | MEDIUM | LOW with rationale]
* **Triggering Condition:** [Threat, failure event, or predisposing condition]
* **Existing Controls:** [Present controls and verification state]
* **Mitigation:** [Neutral, optional action that would reduce the risk]
* **Residual Risk:** [Remaining risk after the proposed mitigation, or `UNKNOWN`]
* **Treatment State:** [Open | Accepted | Transferred | Monitoring | Closed]
* **Owner:** [Role or `NOT SPECIFIED`]
* **Closure Trigger:** [Evidence or event that starts re-verification]
```

When the report language is not English, apply the bullet label translations from the matching
`translation/` file.

## Actionable Remediation Roadmap

This section transforms recommendations into a prioritized, traceable remediation plan. Every
recommendation must resolve a specific finding.

**Prioritized matrix**

Present recommendations as a table. One row per recommendation. Use this fixed column order:

| Rec ID  | Priority | Finding | Recommendation | Impact         | Effort         | Complexity     | Verification        |
|---------|----------|---------|----------------|----------------|----------------|----------------|---------------------|
| REC-001 | <P1-P4>  | FND-XXX | <action>       | <High/Med/Low> | <High/Med/Low> | <High/Med/Low> | <verification step> |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Column meanings:

- **Rec ID**: `REC-[001]` ascending.
- **Priority**: `P1` (immediate), `P2` (short-term), `P3` (medium-term), `P4` (long-term).
- **Finding**: the `FND-XXX` identifier this recommendation resolves.
- **Recommendation**: a concise, actionable technical step.
- **Impact**: the business or technical impact of applying this fix (`High`, `Medium`, `Low`).
- **Effort**: the estimated engineering effort to implement (`High`, `Medium`, `Low`).
- **Complexity**: the architectural or organizational complexity of the change (`High`, `Medium`,
  `Low`).
- **Verification**: a specific test, command, or process to confirm the fix is successful.

**Rules**

- Every `REC-XXX` entry must resolve a specific `FND-XXX`.
- Do not introduce new findings in this section. Recommendations must trace back to gaps in the
  Detailed Technical Findings.
- Keep language neutral and free of blame.
- Do not rank or select a single option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored
  to evidence, and the residual risk.
- When a recommendation would require information that was never provided, state the missing
  information rather than assuming it.

After the table, write one block per recommendation in the same order. Use this exact markdown block
pattern:

```markdown
### REC-[NUMBER]: [Clear, Concise Title of Recommendation]

* **Priority:** [P1 | P2 | P3 | P4]
* **Finding:** [FND-XXX]
* **Description:** [Detailed technical explanation of the recommended action, what it changes, and how it resolves the finding]
* **Impact:** [Business or technical impact of applying this fix]
* **Effort:** [Estimated engineering effort with one-line justification]
* **Complexity:** [Architectural or organizational complexity with one-line justification]
* **Verification:** [Specific test, command, or process to confirm the fix is successful]
```

When the report language is not English, apply the bullet label translations from the matching
`translation/` file.

For readiness or due diligence, include the supported cost rollup and dependency ordering from
`synthesis/remediation-roadmap.md`, counting shared work only once.

Numeric totals require evidence-based compatible units, unknown work remains visible beside any
known subtotal.

## Scope Exclusions

Explicitly define the limits of the analysis.

List components or environments that were not inspected unless they were explicitly provided in the
input scope. Format each exclusion as a bullet with a bold label, followed by an empty line, then
the explanation. Example:

```markdown
- **SQL database schema and stored procedures**.

The database layer was assessed only from the API side. The actual tables, views, triggers, and stored procedures were not provided.
```

Typical exclusions include:

- Operational runtime infrastructure (live servers, VMs, containers)
- Live network topologies and firewall rules
- Third-party authentication provider implementations
- Physical deployment environments
- End-user devices or browser clients
- Data backups or disaster-recovery procedures
- Penetration-test results or security audits performed by external firms

Mark each item as `NOT INSPECTED` or `EXCLUDED BY SCOPE`. If the user provided some of these, list
them as `INCLUDED`.

State any extrapolations made from sampled code to the whole system.

**Standard coverage statement**

When the audit referenced security standards, state which categories were in scope and which were
not, so the reader does not assume full coverage.

For a web application, name the OWASP Top 10 (2025) categories (`A01`-`A10`) that were and were not
assessed.
For an API, name the OWASP API Security Top 10 (2023) categories (`API1`-`API10`).
For a full audit, use the nine ISO/IEC 25010:2023 characteristics in the scorecard crosswalk to
identify coverage and justify exclusions.

Do not present Lens dimension names such as Operational Safety as ISO characteristic names.
Mark categories that could not be assessed from the provided input as `NOT ASSESSED` with a one-line
reason.

**Omitted conditional sections**

When a conditional section was omitted because it does not apply (for example, the API
Contract Conformance section for a system with no API, or the Threat Model for a single-user
local utility), state the omission here with a one-line justification so the reader knows it
was deliberate. The Changes Since Previous Audit section is the exception, a first audit has
no previous report to compare, so its absence needs no note.

## Limitations and Unknowns

List every check that would require execution and was therefore not performed, plus every
unresolved unknown the report carries.

This section exists because the audit is source-only. An unrun check is a limitation of the
report, never a defect of the subject.

Use a table:

| Item               | Type        | Reason                                 | Resolution                                |
|--------------------|-------------|----------------------------------------|-------------------------------------------|
| <check or unknown> | Unrun check | Requires execution, out of audit scope | <command or artifact that would run it>   |
| <check or unknown> | Unknown     | <why the evidence was unavailable>     | <input or artifact that would resolve it> |

Rows come from two sources:

- Every `NOT RUN` row of the verification plan and evidence ledger in
  `process/audit-workflow.md`, with the verification method that would have run it.
- Every unresolved `UNKNOWN`, `NOT SPECIFIED`, or `INSUFFICIENT INFORMATION` token from the
  findings and registers, with the input that would resolve it.

For multi-project reports, qualify each row with the project identifier.

## Re-audit and Follow-up Plan

Include this section only when the Actionable Remediation Roadmap contains at least one P1 or P2
recommendation, per `synthesis/re-audit-plan.md`.

It precedes the Validation Record and References sections.

This section makes the report actionable in a governance sense. It follows ISO 19011 (follow-up
auditing) and the monitor step of the NIST Risk Management Framework.

Present a table mapping findings to verification ownership and closure evidence. Include one row per
P1 and P2 finding at minimum.

| Finding | Priority | Verification Owner        | Closure Evidence      | Target Re-audit Trigger        |
|---------|----------|---------------------------|-----------------------|--------------------------------|
| FND-XXX | P1       | <role or `NOT SPECIFIED`> | <verifiable artifact> | <milestone or `NOT SPECIFIED`> |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

After the table, state sign-off gates tied to project-qualified `RSK-XXX` IDs and an evidenced
re-audit schedule.

Apply `synthesis/re-audit-plan.md` for confirmed ownership, revision-specific closure evidence,
residual risk, and the separation of final-report state from production sign-off.

Unknown owners or missing required verification leave sign-off pending, proposed roles are not
assignments.

## Validation Record

Close the analysis with a self-check table verifying the report's internal consistency. This
section renders the report's capability set so a future report can diff it mechanically, per
`process/report-parity.md`.

Use a table:

| Check | Result  | Evidence / Justification          |
|-------|---------|-----------------------------------|
| PAR-1 | Applied | <evidence or `N/A` justification> |

Rows appear in this order:

1. One row per Mandatory Core Checklist item, `PAR-1` through `PAR-9`, in fixed order.
2. Internal consistency checks: `FND-XXX`/`RSK-XXX`/`REC-XXX` cross-referencing, count
   reconciliation across summary tables and registers, conditional-section evaluation, and
   formatting rules.
3. A `Parity baseline` row naming the report diffed against, or `none found`.

Result values are `Applied`, `PASS`, or `N/A`. An `N/A` always carries a justification in the
Evidence / Justification column.

For multi-project reports, qualify per-project checks with the project identifier.

## References

This section lists every external source referenced during the audit. It is always the final
section of the report.

Collect references from all sections of the report. Sources include the standards named in Auditing
Methodology, the external best practices cited in Standards Conformance, and any documentation
consulted during any assessment category.

Present the references as a table:

| Reference | Publisher or Author   | Used In         |
|-----------|-----------------------|-----------------|
| <title>   | <publisher or author> | <section names> |

When the report language is not English, apply the column header translations from the matching
`translation/` file.

Only list sources actually consulted during the audit. Do not invent references.

For each source, record edition/version, publisher, access date, applied controls or claims, and any
access limitation in the supporting paragraph.

Prefer primary standards and tool documentation over marketing summaries.

Verify publication status at audit time, distinguishing released editions, drafts, and legacy
baselines, and avoid claiming full conformance from sampled coverage.

Offline audits should identify dated cached sources and leave current advisory status unknown when
it cannot be checked.

After the table, add one paragraph per reference that has a URL. Format each link as a Markdown
link: `[<title>](<url>)`. Do not put URLs in the table itself, because long URLs make the table
unreadable in plain text. Group rows by section when the same source is used in multiple sections,
or list one row per source with all sections in the Used In column separated by commas. Keep the
order stable: methodology standards first, then standards-conformance best practices, then any other
sources in the order they first appear in the report.

## Pre-Delivery Mechanical Checklist

Run this checklist after writing the report body and before running the formatting script. It
consolidates the mechanical rules from this file and `principles/output-style.md` in one
place, every item is mechanical and takes seconds to verify.

| Check          | Rule                                                                           |
|----------------|--------------------------------------------------------------------------------|
| Headings       | `#` title, `##` sections, `###` subsections and blocks, never `####` or deeper |
| Heading space  | Exactly one empty line after every heading                                     |
| Delimiters     | Pipe-delimited columns, one space inside leading and trailing pipes            |
| Separators     | Hyphens contiguous with pipes, width equals column width plus two              |
| Alignment      | Every column aligned by the formatting script, never padded by hand            |
| Semicolons     | None outside code blocks, inline code, and file paths                          |
| Dashes         | ASCII `-` only, no em dash or en dash                                          |
| Arrows         | ASCII `->` in prose, no Unicode arrow                                          |
| Prose width    | Lines broken near 100 characters, exempt table rows, URLs, links, paths        |
| Finding blocks | Every required field present, see the template in Detailed Technical Findings  |
| Glossary       | Present when Descriptive Mode is Enabled, alphabetical, body occurrences link  |
| Diagrams       | Fenced, untagged, no leading or trailing blank line inside the fence           |
| Registers      | Every RSK cites an FND, every REC cites an FND, heat-map covers rated risks    |
| Ending         | References is the last section, no closing line after it                       |

`tools/format-table.py` in the skill repository is the canonical formatting script, copy it into
the audited repository's `work/` directory before use. `tools/validate-report.py` runs the
scriptable items in this checklist plus finding-block field, register cross-reference, and
PAR-row checks, copy and run it the same way.
