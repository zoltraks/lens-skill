# Multi-Project Report Structure

## Purpose

> **Scope:** The combined multi-project report layout
> **Key items:** project inventory, shared sections, per-project blocks

When the audit covers more than one project in a repository or directory,
the report uses a combined structure.

Each project is assessed independently and receives its own complete set of sections within the
report.

**Document Information** appears once at the top.

The title uses the repository or directory name, not a single project name.

Include a `Projects` row in the table listing the audited projects.

The **Audit Type Coverage** table appears once, immediately after Document
Information and before the Project Inventory.

**Project Inventory** appears after the Coverage Matrix.

It lists each project confirmed at the intake inclusion question with its path, version, and a
one-line description.

Projects the user unchecked, or that intake classified as installed or external, do not appear
here: they are disclosed once in Scope Exclusions with their exclusion reason.

```
| Project        | Path           | Version | Description            |
|----------------|----------------|---------|------------------------|
| <project name> | <project path> | <ver>   | <one-line description> |
```

When the report language is not English, apply the column header translations from the matching
`translations/` file.

**Combined summary sections** appear immediately after the Project Inventory, so orientation
material precedes per-project detail.

The **Executive Summary** is a condensed combined summary.

Write a short orientation paragraph, then a compact table with one row per project:

```
| Project        | Score                   | Lowest              | Risks                   | Readiness         |
|----------------|-------------------------|---------------------|-------------------------|-------------------|
| <project name> | <mean>/<scale> (<band>) | <dimension> <score> | <top RSK-XXX or `NONE`> | <readiness state> |
```

The **Changes Since Previous Audit** section is combined at report level when a re-audit was
confirmed.

Give each compared project its own level-3 subsection inside this section and keep project-qualified
finding IDs.

Do not repeat the section inside the per-project blocks.

**Per-project sections** follow the combined summary sections.

Each project gets a level-2 heading (`##`) with the project name,
followed by the full set of report sections for that project:

- Executive Summary
- System Context (with the Technology Stack subsection)
- Software Bill of Materials
- License Compliance Review
- Health Dashboard
- Delivery Practice & Team Continuity
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- Architectural Assessment (with conditional subsections)
- Trade-off Analysis
- Threat Model *(conditional)*
- API Contract Conformance *(conditional)*
- Skill Definition Conformance *(conditional)*
- Agent Guidance Conformance *(conditional)*
- AI System Assessment *(conditional)*
- Standards Conformance *(conditional)*
- API Compatibility & Versioning Discipline *(conditional)*
- Strengths & What's Working
- Detailed Technical Findings
- Technical Debt Register *(conditional)*
- Unified Risk Register
- Actionable Remediation Roadmap
- Recommendation Classification *(conditional)*

Use level-3 headings (`###`) for subsections within each project block.

**Finding IDs** are scoped per project.

Each project's findings start at `FND-XXX-001`.

Risk IDs and recommendation IDs also reset per project.

Qualify each finding heading with the project identifier as a trailing parenthetical so the
reader can navigate.

For example: `### FND-ARC-001: Missing input validation (api-service)`.

On a re-audit, a prior cross-cutting finding that now maps to one project keeps its identifier
and gains that project's `(<project>)` suffix, and the mapping is recorded in the Changes Since
Previous Audit section.

A prior finding that applies to several projects splits into one scoped finding per project,
each carrying the same base identifier under its own project suffix, and the split is recorded
in the Changes section.

**Shared sections** appear once at the end of the report, after all per-project sections:

- Trade-off Analysis (combined)
- Scope Exclusions
- Limitations and Unknowns
- Re-audit And Follow-up Plan *(conditional)*
- Validation Record
- References

The combined **Trade-off Analysis** holds only cross-project trade-offs.

A trade-off is cross-project only when the decision was made once and constrains more than one
project, such as a shared dependency choice or a repository-wide workspace or build decision.

The same issue type appearing independently in two projects is a repeated per-project finding,
not a cross-project trade-off, and stays in the per-project Trade-off Analysis after that project's
Architectural Assessment.

The combined table adds a leading `Project` column.

When no cross-project trade-off qualifies,
the section stays present and the table carries a single `N/A` row with a one-line justification.

The Scope Exclusions, Limitations and Unknowns, Validation Record,
and Re-audit sections cover all projects and carry the exclusion disclosures.

Qualify rows per project using the project identifier.

The validator enforces three multi-project rules once a `Project Inventory` exists:

- A shared-table cell never carries an ambiguous project label - `both`, `either`, and
  `the projects` all fail, so split the row or name each project explicitly.
- Identifiers in shared sections qualify with the project name and a `::` separator,
  `api-service::FND-SEC-001`, so a reader can tell which register owns the entry.
- The Project column appears only in combined and shared tables - a single-project report
  without a Project Inventory must not carry one, and the evidence ledger follows the same rule.

**Single-project reports** use the standard structure without the Project Inventory table and
without per-project level-2 headings.

The sections appear directly under level-2 headings as in a standard report.
