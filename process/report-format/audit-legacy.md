# Audit Legacy Style

## Purpose

> **Scope:** The `audit (legacy)` report variant - the pre-redesign metadata-first
> audit layout **Key items:** canonical section order, long-form scorecard, wide
> roadmap matrix, optional Contents, penultimate roadmap

This file defines the report produced when `report-style: audit (legacy)` is resolved during
Parameter Configuration in `process/audit-workflow/parameter-phase.md`
or recovered from a previous report whose Document Information records
`Report Style: Audit (legacy)`.

The default `audit` style is the reorganized contract in `process/report-format.md`.

The legacy variant exists so an audit report in the earlier layout - Document Information
leading, metadata before the scorecard, findings and roadmap before the closing sections -
can still be produced on request, for example when a revision continues an established
report series.

A report under this variant records `Report Style: Audit (legacy)` in Document Information.

A `Report Style: Audit` row without the `(legacy)` suffix selects the reorganized contract,
never this file.

Both variants share one evidence base and one set of section contracts:
the same evidence gathering, the same finding schema,
the same completeness rules, and the same readiness gates.

Style changes presentation, never what must be found.

Read the sections the task needs - grep the `## ` headings for the section map.

## Shared Contract

The following carry over unchanged from `process/report-format.md` and its spec files:

- Document Information per `report-opening.md`, including `Report Style: Audit (legacy)`.
- Audit Coverage, Project Inventory, and System Context per `report-opening.md` and
  `context-compliance.md`.
- Executive Summary per `summary-changes.md`, minus the `### Immediate Actions` subsection -
  the legacy layout has no immediate-action preview.
- The finding block schema, Technical Findings summary, risk register,
  roadmap records, and Recommendation Classification per `findings-registers.md`.
- Auditing Methodology and Scoring Rubrics per `methodology-scoring.md`.
- Scope Exclusions, Known Limitations, Verification Handoff or Executed Evidence,
  Validation Protocol, and Reference Sources per `report-closing.md`.
- Snapshot identity, read-depth table, evidence ledger,
  and claim traceability rules per `process/audit-workflow/audit-intake.md` and
  `process/audit-workflow/evidence-gathering.md`.
- Multi-project reporting per `multi-project.md` under the section orders defined here.

The variant's differences are layout only - every rule in this file is a presentation
delta from the reorganized contract.

## Report Opening

The report opens with the `#` document title and `## Document Information` as the
first section - the same opening the reorganized contract uses.

A `## Contents` section may follow Document Information when the report keeps one;
it is optional, flat, and lists the top-level sections without grouping labels.

## Section Order

Produce these top-level sections in this order, with unnumbered headings.

Sections marked *(conditional)* follow the inclusion criteria in
`process/report-format.md`'s Conditional Sections table.

For a **single-project** audit:

- Document Information
- Audit Coverage
- Glossary Index *(when Descriptive mode is enabled)*
- Executive Summary
- Changes Since Previous Audit *(conditional)*
- System Context (contains the Technology Stack subsection)
- Software Bill of Materials
- License Compliance
- Health Dashboard (Risk Map first, then the Legend, then Scorecard Summary)
- Delivery Practice
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment
- Structure Review
- Solution Comparison
- Threat Model *(conditional)*
- API Contract Conformance *(conditional)*
- Skill Definition Conformance *(conditional)*
- Guidance Conformance *(conditional)*
- AI System Assessment *(conditional)*
- Standards Conformance *(conditional)*
- Requirements Conformance *(conditional)*
- Baseline Conformance *(conditional)*
- Structure Conformance *(conditional)*
- Code Style *(conditional)*
- API Compatibility & Versioning Discipline *(conditional)*
- Strengths and What's Working
- Technical Findings
- Technical Debt Register *(conditional)*
- Risk Register
- Scope Exclusions
- Known Limitations
- Further Verification *(source-only mode)* / Executed Evidence
  *(executed-readonly or executed-commands mode, conditional)*
- Validation Protocol
- Remediation Roadmap (with Recommendation Classification and Follow-up Plan subsections)
- Reference Sources

For a **multi-project** audit:

- Document Information (once)
- Audit Coverage (once)
- Project Inventory (once)
- Glossary Index *(when Descriptive mode is enabled)* (once)
- Executive Summary (condensed, combined)
- Changes Since Previous Audit *(conditional)* (combined)
- For `project-layout: combined` - the single shared section set from System Context
  through Risk Register, with a `Project` column in the register tables.
- For `project-layout: separate` - one level-2 `## Project <name>` section per project,
  each carrying Executive Summary through Risk Register as `###` subsections,
  then Solution Comparison (once, combined - cross-project trade-offs only).
- Scope Exclusions (once, shared)
- Known Limitations (once, shared)
- Further Verification *(source-only mode)* / Executed Evidence *(executed-readonly or
  executed-commands mode, conditional)* (once, shared)
- Validation Protocol (once, shared)
- Remediation Roadmap (once, shared - consolidated matrix and registers with a
  Project column, carrying Recommendation Classification and Follow-up Plan subsections)
- Reference Sources (once, shared)

## Health Dashboard

The dashboard keeps the legacy element order: `**Risk Map**`, `**Legend**`,
then `**Scorecard Summary**`, then `**Team & Continuity**`.

The multi-project scorecard renders long-form - `| Project | Dimension | Score |` -
never the reorganized Dimension x project pivot.

The dashboard carries no `**Interpretation limits**` label and no project overview table;
the readiness interpretation lives in Executive Summary per `summary-changes.md`.

## Technical Findings

The findings summary may carry the wider column set - `Project`, `Finding`, `Pillar`,
`Severity`, `Title`, `Result`, plus lifecycle columns such as `Status`, `Change`,
and `Verification` when they carry data.

Every rule in `findings-registers.md` about linked finding IDs and complete detail
blocks applies unchanged.

## Remediation Roadmap

The roadmap overview may keep the consolidated matrix - `| Project | Rec | Priority |
Finding | Recommendation | Impact | Effort | Complexity | Verification |`, plus a
`Breaking` column when findings assess it - followed by the `### REC-` detail records.

Remediation Roadmap is the penultimate section: it immediately precedes Reference Sources.

## Detail Levels

`Standard` and `Detailed` produce the full register.

`Brief` keeps Document Information, Audit Coverage, Executive Summary, System Context,
Health Dashboard, High-Level Observations, Strengths and What's Working, Scope Exclusions,
Known Limitations, and Reference Sources.

## Output Filename

The audit filename stem is `AUDIT`, or the language-specific stem from the matching
`translations/` file.

The variant changes no filename or revision rules - they follow
`process/audit-workflow/parameter-phase.md` and `synthesis/report-comparison.md` unchanged.
