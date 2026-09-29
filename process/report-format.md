# Report Format

## Purpose

> **Scope:** The required structure and template for the final audit report
> **Key items:** document information, technology stack, executive summary, health dashboard,
> auditing methodology, scoring rubrics, system context, architectural assessment, detailed
> technical findings, unified risk register, trade-off analysis, remediation roadmap, scope
> exclusions

This file defines the exact shape of the audit report and indexes the per-section
specifications under `process/report-format/`.

The review report type produced on explicit review requests follows
`process/review-report.md` instead of this file.

Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development,
or an already-running production system.

Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`.

A present-but-empty section signals a gap, a missing section hides it.

## Contents

| Section                                     | Line | What it covers                              |
|---------------------------------------------|------|---------------------------------------------|
| Formatting Rules                            | 40   | Formatting Rules guidance                   |
| Report Delivery And Parameter Configuration | 258  | Report delivery and output configuration    |
| Detail Level Configuration                  | 304  | Standard, detailed, and brief reports       |
| Conditional Sections                        | 398  | Inclusion criteria for conditional sections |
| Section Order                               | 448  | Single-project and multi-project order      |
| Specification Files                         | 535  | Per-section specification file index        |
| Pre-Delivery Mechanical Checklist           | 560  | Final mechanical checks                     |

## Formatting Rules

Use a hybrid table-paragraph format in every section.

Tables provide the scannable summary.

Paragraphs below the table provide the detailed evidence, risks, and reasoning.

In tables, use shortened, general values.

One or two words per cell.

Do not crowd table cells with long explanations.

Save detail for the paragraphs.

Do not number section headings.

Use the section name as the heading, for example "Executive Summary", not "2.

Executive Summary".

When the user requests a specific language, translate the section heading into that language.

Use `#` for the document title, `##` for top-level sections,
and `###` for subsections and finding or register blocks.

Do not use `####` or deeper headings.

Use Title Case for English section names and keep them short,
avoid trailing punctuation and descriptive qualifiers in parentheses.

The matching `translations/` file defines the casing rule for non-English reports.

Keep column headers identical to the templates below across every audit.

When the user requests a specific language,
translate the column headers into that language while keeping the structure identical.

Keep table cells single-line and use commas for compact lists, placing explanations below the table.

Preserve identifiers and gap tokens intact even when they exceed the usual cell word limit.

Place descriptive paragraphs immediately after each table.

In the paragraphs, explain every aspect with concrete evidence, file paths, and reasoning.

Use short sentences separated by blank lines,
each sentence stands on its own line with an empty line between consecutive sentences.

Start each detailed paragraph with a bold heading on its own line.

Put the status, score, or severity inline after the heading, separated by a space.

Then add an empty line, then the paragraph body.

Do not run the heading and the body together on the same line.

Use this bold-heading pattern for paragraphs that expand on a table row.

For actual section or subsection titles, use markdown header syntax (`##` or `###`)
rather than bold text.

Break prose lines that exceed the selected wrap width - 100 characters by default - at a natural
boundary such as after a comma or clause end, per `STYLE.md`.

Offer the width choice per the Selecting The Wrap Width rules in `STYLE.md` before wrapping.

Do not break inside inline code, file paths, or URLs.

The limit does not apply to table rows, URLs, links, or file paths,
so a line carrying an unbreakable URL may remain over the limit.

Do not use the semicolon character in prose.

Join closely related clauses with a comma or split them into separate sentences.

The rule does not apply to code blocks, inline code, or file paths, per `STYLE.md`.

Use a language tag on fenced code blocks that contain code.

Leave diagrams, directory trees, console output, and plain text untagged,
and do not leave a blank line as the first or last line inside a fenced block.

Do not add a Contents or table-of-contents section.

`STYLE.md` requires one in documents over 300 lines,
but the report navigates by its fixed section order and the Health Dashboard,
so the omission is deliberate.

### Table Formatting Rules

Apply these rules to every table in the report.

**Delimiters**: Use pipe characters (`|`) to delimit columns.

Place one space after the leading pipe and one space before the trailing pipe.

**Header separator**: Place a separator line immediately after the header row.

The separator contains only hyphens and pipe characters.

The hyphens are contiguous with the pipe characters - do not add spaces between pipes and hyphens.

The separator width for each column equals the column width plus two hyphens.

Minimum column width is three characters.

Correct separator format:

```markdown
|---------|--------|
```

Incorrect separator format (spaces around hyphens):

```markdown
| ------- | ------ |
```

**Cell padding**: Pad every cell with trailing spaces so it matches the widest cell in that column.

Empty cells must also be padded.

Use left alignment for all cells.

Never truncate cell contents.

**Column width**: Calculate the column width as the maximum character width of all cells in that
column, including the header.

Include all Markdown formatting characters (backticks, asterisks, spaces, punctuation)
in the width measurement.

**Compacting**: After calculating column widths,
compact the table by removing any padding that exceeds the widest cell in each column.

The compacted version - minimum width that fits every cell - is the correct version.

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

Format every table with a script, do not count column widths by hand.

Manual counting is error-prone and produces misaligned columns, per `STYLE.md`.

Before delivering a File-mode report, run a script that implements the checklist above:
parse each table, measure every cell width in source text including formatting characters,
pad each cell to the column maximum, and rebuild each separator as the column width plus two
hyphens.

Handle both `\n` and `\r\n` input and preserve the file's original line-ending style.

`scripts/format-table.py` in the skill repository is the canonical implementation.

Copy it into the audited repository under a `.tmp.` name, for example `format-table.tmp.py`,
instead of writing a new formatter by hand.

Place the script copy in `work/` when that directory exists in the audited repository.

Use an existing `temp` or `temporary` directory when `work/` is unavailable,
and use the repository root only when none exists.

Run it on the report file, verify that all `|` separators align vertically, then remove the copy.

For Inline delivery, apply the same formatting to the report text before emitting the response.

Running the formatting script on the report file is part of producing the report.

It is not execution of the audited project.

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

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs.

Do not use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

**No closing line**

Do not add a closing line such as "End of audit report." or "---" at the end of the document.

The final section is the References section,
end the report after the final section without any trailing boilerplate.

## Report Delivery And Parameter Configuration

Report delivery and output-file selection are determined during the Parameter Configuration phase in
`process/audit-workflow.md`.

Do not ask delivery questions here, they are handled upstream.

The delivery question presents `Inline`, each applicable concrete file path,
and `Custom report file` in one prompt.

Selecting a file path chooses both delivery and output location.

When the user names an output file in the original request,
for example "write the audit to AUDIT.md", honor that filename without asking again.

Resolve the output directory using the location rules in `process/audit-workflow.md` unless a full
path was given.

When the user states only a File preference without naming a path,
ask the same question with `Inline` omitted.

Retain the applicable file-location and `Custom report file` options.

When the user invokes an audit without naming an output file, the Parameter Configuration phase
resolves the output base and offers the applicable file paths in the delivery question.

Default delivery is **File** when an `audit/` or `report/` directory exists under `docs/`,
`document/`, or `doc/` in the audited repository or directory, otherwise **Inline**.

Location resolution, subdirectory-pattern matching,
and the delivery-question options are defined in `process/audit-workflow.md`,
which is the single source of truth: the pattern recorded during Output location discovery there
determines whether a version-numbered, date-named, or plain base path is offered.

The default filename carries the report revision: `AUDIT-1.0.md` for a first English audit,
or the language-specific revisioned name such as `AUDYT-1.0.md`,
with the plain stem offered as an alternative.

When a previous audit report exists, the filename carries the new revision whether the audit mode is
re-audit or fresh audit, for example `AUDIT-2.0.md`, and the previous file is never overwritten.

`Custom report file` asks the user to specify the location and filename before writing.

For a single-dimension request that produces only a short subsection, returning the result
inline is acceptable without asking, unless the user asked for a file.

## Detail Level Configuration

The report adapts to the detail level chosen during Parameter Configuration.

The default detail level is `Detailed`.

`Standard` and `Brief` remain available when the user selects them during configuration or
explicitly requests them.

**Standard**

All twenty-one baseline sections are present in full, subject to explicit parameter exclusions:

- Document Information
- Audit Type Coverage & Assurance Matrix
- Executive Summary
- System Context (including the Technology Stack subsection)
- Software Bill of Materials
- License & IP Compliance Review
- Health Dashboard
- Delivery Practice & Team Continuity
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment
- Trade-off Analysis
- Strengths & What's Working
- Detailed Technical Findings (all findings with full Description, Impact, Recommendation, and
  Method)
- Unified Risk Register
- Actionable Remediation Roadmap (full matrix with P1-P4, impact/effort/complexity, verification)
- Scope Exclusions
- Limitations and Unknowns
- Validation Record
- References

In addition, any conditional sections whose criteria are met are included in full.

See the Conditional Sections rule below for the inclusion criteria of the Data Flow Diagram,
Design Patterns, Architecture Decision Records, Threat Model, API Contract Conformance,
Skill Definition Conformance, Standards Conformance, Technical Debt Register,
and Re-audit And Follow-up Plan.

**Detailed**

Same sections as Standard, plus the following extensions.

At the Detailed level, evaluate every conditional section's criterion explicitly and include each
one that applies:

- Executive Summary includes a longer Production Readiness Threshold paragraph.
- Health Dashboard includes an expanded Risk Map with all risks plotted.
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
- Changes Since Previous Audit (report reference and finding transition tables only) when a
  re-audit was confirmed
- System Context (Technology Stack subsection only)
- Health Dashboard (scorecard summary and risk map only)
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
register, full trade-offs, full roadmap, and Recommendation Classification.

Retain a compact check summary and evidence IDs in Scope Exclusions, and blocked/unrun checks in
Limitations and Unknowns.

Do not omit critical decision limitations to meet the shorter format.

## Conditional Sections

Some sections and subsections apply only to certain kinds of system.

Include a section only when it is relevant to the subject under audit.

A section that does not apply must be omitted entirely, not included as an empty placeholder.

This differs from the rule for always-present sections,
where a present-but-empty section signals a gap.

The conditional sections below describe a specific capability (an API, a trust boundary,
recurring structure) that some subjects simply do not have,
forcing such a section would mislead the reader.

When a conditional section is omitted, state the omission once in the Scope Exclusions section with
a one-line justification, so the reader knows the omission was deliberate.

The following sections and subsections are conditional.

Each lists its inclusion criterion and the assessment file that governs it:

| Section / Subsection                                        | Include When                                                       | Governing File                        |
|-------------------------------------------------------------|--------------------------------------------------------------------|---------------------------------------|
| Data Flow Diagram (in Architectural Assessment)             | The system moves data across one or more trust boundaries          | `assessment/data-flow.md`             |
| Design Patterns (in Architectural Assessment)               | The codebase is large enough to exhibit recurring structure        | `assessment/design-patterns.md`       |
| Architecture Decision Records (in Architectural Assessment) | The system is production-bound with significant decisions          | `assessment/change-management.md`     |
| Threat Model (standalone)                                   | The system has a security-relevant attack surface or boundary      | `assessment/threat-model.md`          |
| API Contract Conformance (standalone)                       | The system defines, exposes, or consumes an API contract           | `assessment/api-contract.md`          |
| Skill Definition Conformance (standalone)                   | The subject holds `SKILL.md` files or other agent-facing artifacts | `assessment/skill-definition.md`      |
| AI System Assessment (standalone)                           | The project trains, serves, or materially depends on AI            | `assessment/ai-system.md`             |
| Standards Conformance (standalone)                          | The project contains documented development standards              | `assessment/standards-conformance.md` |
| API Compatibility & Versioning Discipline (standalone)      | The subject is a reusable library or package                       | `assessment/api-compatibility.md`     |
| Technical Debt Register (standalone)                        | Structural debt distinct from risks is surfaced                    | `synthesis/debt-register.md`          |
| Re-audit And Follow-up Plan (standalone)                    | The roadmap contains a P1 or P2 recommendation                     | `synthesis/re-audit-plan.md`          |
| Changes Since Previous Audit (standalone)                   | Previous report found and confirmed as the re-audit baseline       | `synthesis/report-comparison.md`      |
| Glossary (standalone)                                       | Descriptive mode is enabled (default)                              | `process/report-format.md`            |
| Recommendation Classification (standalone)                  | Detail level is Standard or Detailed and the roadmap exists        | `synthesis/remediation-roadmap.md`    |

In a multi-project report, evaluate each criterion independently per project.

A section may apply to one project and be omitted for another,
record each deliberate omission in Scope Exclusions.

When in doubt about whether a conditional section applies,
prefer including it with explicit `N/A` or `NOT SPECIFIED` markers over silently dropping a relevant
concern.

Only omit a section when it genuinely cannot apply to the subject.

## Section Order

The report has these top-level sections, in this order, with unnumbered headings.

The Specification Files table below maps each section to its specification file.

Sections marked *(conditional)* are included only when their criterion in the Conditional Sections
table is met.

For a **single-project** audit:

- Document Information
- Audit Type Coverage & Assurance Matrix
- Glossary *(when Descriptive mode is enabled)*
- Executive Summary
- Changes Since Previous Audit *(conditional)*
- System Context (contains the Technology Stack subsection)
- Software Bill of Materials
- License & IP Compliance Review
- Health Dashboard
- Delivery Practice & Team Continuity
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
- Recommendation Classification *(conditional)*
- Scope Exclusions
- Limitations and Unknowns
- Re-audit And Follow-up Plan *(conditional)*
- Validation Record
- References

For a **multi-project** audit, the structure changes.

See `process/report-format/multi-project.md` for the full layout.

In summary:

- Document Information (once)
- Audit Type Coverage & Assurance Matrix (once)
- Project Inventory (once)
- Glossary *(when Descriptive mode is enabled)* (once)
- Executive Summary (condensed, combined)
- Changes Since Previous Audit *(conditional)* (combined)
- Per project (level-2 heading per project, full section set each):
  - Executive Summary
  - System Context (with the Technology Stack subsection)
  - Software Bill of Materials
  - License & IP Compliance Review
  - Health Dashboard
  - Delivery Practice & Team Continuity
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
  - Recommendation Classification *(conditional)*
- Trade-off Analysis (combined, cross-project trade-offs only)
- Scope Exclusions (once, shared)
- Limitations and Unknowns (once, shared)
- Re-audit And Follow-up Plan *(conditional)* (once, shared)
- Validation Record (once, shared)
- References (once, shared)

## Specification Files

Each report section is specified in a file under `process/report-format/`.

| File                            | Sections                                                      |
|---------------------------------|---------------------------------------------------------------|
| `opening.md`                    | Document Information, Audit Type Coverage & Assurance Matrix, |
|                                 | Glossary                                                      |
| `multi-project.md`              | Multi-Project Report Structure                                |
| `summary-and-changes.md`        | Executive Summary, Changes Since Previous Audit               |
| `context-and-compliance.md`     | System Context, Software Bill of Materials, License & IP      |
|                                 | Compliance Review                                             |
| `dashboard-and-observations.md` | Health Dashboard, Delivery Practice & Team Continuity,        |
|                                 | High-Level Observations                                       |
| `methodology-and-scoring.md`    | Auditing Methodology, Scoring Rubrics                         |
| `architectural-assessment.md`   | Architectural Assessment and its conditional subsections      |
| `analysis.md`                   | Trade-off Analysis, Threat Model                              |
| `conformance.md`                | API Contract, Skill Definition, AI System, Standards,         |
|                                 | API Compatibility & Versioning Discipline                     |
| `findings-and-registers.md`     | Strengths, Detailed Technical Findings, Technical Debt        |
|                                 | Register, Unified Risk Register, Remediation Roadmap,         |
|                                 | Recommendation Classification                                 |
| `closing.md`                    | Scope Exclusions, Limitations and Unknowns, Re-audit And      |
|                                 | Follow-up Plan, Validation Record, References                 |

## Pre-Delivery Mechanical Checklist

Run this checklist after writing the report body and before running the formatting script.

It consolidates the mechanical rules from this file and `principles/output-style.md` in one place,
every item is mechanical and takes seconds to verify.

| Check           | Rule                                                                                        |
|-----------------|---------------------------------------------------------------------------------------------|
| Headings        | `#` title, `##` sections, `###` subsections and blocks, never `####` or deeper              |
| Heading space   | Exactly one empty line after every heading                                                  |
| Delimiters      | Pipe-delimited columns, one space inside leading and trailing pipes                         |
| Separators      | Hyphens contiguous with pipes, width equals column width plus two                           |
| Alignment       | Every column aligned by the formatting script, never padded by hand                         |
| Semicolons      | None outside code blocks, inline code, and file paths                                       |
| Dashes          | ASCII `-` only, no em dash or en dash                                                       |
| Arrows          | ASCII `->` in prose, no Unicode arrow                                                       |
| Prose width     | Lines broken near the selected width (default 100), exempt table rows, URLs, links, paths   |
| Finding blocks  | Every required field present, see the template in Detailed Technical Findings               |
| Coverage matrix | Present after Document Information, consistent with Scope Exclusions                        |
| SBOM            | Every License cell populated or `Unknown`, direct components manifest-sourced               |
| Type tags       | `Observation` or `Concern` on every evidence-ledger row and every finding                   |
| Exploitability  | `Exploitability` field present on every `HIGH`/`CRITICAL` security finding, `N/A` justified |
| Glossary        | Every acronym indexed, every body occurrence linked to its anchor                           |
| Diagrams        | Fenced, untagged, no leading or trailing blank line inside the fence                        |
| Registers       | Every RSK cites an FND, every REC cites an FND, risk-map covers rated risks                 |
| Classification  | At Standard/Detailed, Recommendation Classification lists every REC exactly once            |
| Project scope   | Inventory lists only intake-confirmed projects, exclusions disclosed in Scope Exclusions    |
| Location        | Report path matches the output directory recorded during intake                             |
| Ending          | References is the last section, no closing line after it                                    |

`scripts/format-table.py` in the skill repository is the canonical formatting script,
copy it into the audited repository's `work/` directory before use.

`scripts/validate-report.py` runs the scriptable items in this checklist plus finding-block field,
register cross-reference, and PAR-row checks, copy and run it the same way.
