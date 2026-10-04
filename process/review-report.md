# Review Report

## Purpose

> **Scope:** The review report type: an evidence-based evaluation of any subject that ends in
> amendment instructions and a suggested amendment order
> **Key items:** report type resolution, review structure, findings and corrections, required
> changes, amendment order, public source register, review validation

This file defines the second report type Lens produces: the review report.

The audit report defined in `process/report-format.md` stays the default deliverable,
and auditing software remains the skill's main purpose.

A review report evaluates a subject and specifies the changes needed to improve it.

The subject may be anything the user supplies: a document, a specification, a plan,
a configuration set, a codebase, or a proposal.

## Contents

| Section                             | Line | What it covers                   |
|-------------------------------------|------|----------------------------------|
| Report Type Resolution              | 36   | Report Type Resolution guidance  |
| Subject Scope                       | 66   | Subject Scope guidance           |
| Workflow Deltas                     | 73   | Workflow Deltas guidance         |
| Report Structure                    | 152  | Report Structure guidance        |
| Change Review Variant               | 246  | Change Review Variant guidance   |
| What A Review Report Never Contains | 353  | Excluded report machinery        |
| Formatting                          | 371  | Formatting guidance              |
| Re-Review And Revisions             | 379  | Re-Review And Revisions guidance |
| Detail Levels                       | 389  | Detail Levels guidance           |
| Languages                           | 399  | Languages guidance               |
| Validation                          | 406  | Validation guidance              |

## Report Type Resolution

The report type is resolved during intake from the request's wording.

`Audit` is the default and is never overridden silently.

`Review` applies only when the request explicitly asks for a review deliverable:
an evaluation that ends in corrections, amendment instructions, a change specification,
or an improvement plan for the subject.

Signals of a review request include "review this document and propose amendments",
"produce an improvement plan for", "evaluate X and describe the required changes",
and "suggest corrections to".

A bare "review this codebase" or "review only the security posture" stays an audit
or a single-dimension audit, per `process/audit-workflow.md`.

A review request that scopes the subject to a change set - a commit range, a pull or
merge request, or a branch diff - resolves to the Change Review Variant defined below.

When the request is ambiguous, use `Audit` and say so in the Parameter Configuration
summary so the user can correct the choice before work proceeds.

The resolved type appears as the `Report type` row in the Parameter Configuration
defaults table of `process/audit-workflow.md`.

The type is never a routine question and never changes silently.

A user correction restarts Parameter Configuration.

## Subject Scope

A review report covers one subject: the artifact the request names.

When a request names several subjects, produce one review report per subject,
or confirm a single combined scope with the user before proceeding.

## Workflow Deltas

A review follows the same intake, scope, evidence, and assessment pipeline as an audit,
per `process/audit-workflow.md`.

The phases run unchanged except for the deltas below.

**Intake**

Resolve the report type per Report Type Resolution.

Previous-report discovery searches the review filename family (`REVIEW.md`,
`REVIEW-<revision>.md`, and the language-specific stem such as `PRZEGLĄD-1.0.md`)
instead of audit filenames.

An audit report is never a review baseline, and a review report is never an audit baseline.

The audit-mode question and its options apply unchanged to a found review report,
with "re-review" substituted for "re-audit" in the wording.

**Parameter Configuration**

The defaults table shows the resolved `Report type`.

The evaluation-scale prompt is skipped: a review report carries no scorecard.

Descriptive mode does not apply: a review report carries no Glossary.

**Scope Definition**

Record the request's stated requirements as the review's conformance baseline.

Every requirement the request states receives a verdict in the review - met, partially
met, or missed - with the subject anchor that supports it.

**Evidence Gathering**

Unchanged.

The review is source-only: it never executes, builds, tests, or scans the subject,
and externally produced results are `REPORTED` evidence.

The evidence ledger stays internal working material.

The review report cites concrete anchors inline and never renders the ledger.

**Category Assessment**

Load the `assessment/` files that fit the subject and the request's review questions,
governed by the same conditional criteria in `process/report-format.md`.

For a document subject, `assessment/documentation-review.md` applies, and
`assessment/standards-conformance.md` applies when the subject declares or implies
standards to check against.

**Synthesis**

Render the review sections defined below instead of the audit section set.

**Validation**

Run the review validation contract in the Validation section below.

`scripts/validate-report.py` detects the review shape and applies the review contract
instead of the audit checks.

The audit parity gate in `process/report-parity.md` does not run on review reports.

**Delivery**

Output-location resolution is unchanged.

The filename stem is `REVIEW`, so a first review of a subject defaults to
`REVIEW-1.0.md` with plain `REVIEW.md` offered as the alternative.

The change-review variant shares the `REVIEW` filename family and revision numbering:
a `REVIEW`-family name carrying a custom suffix marks the report custom and relaxes
the section contract, per Validation.

## Report Structure

A review report carries exactly these elements, in this order.

### Title And Preamble

The title is `# <Subject name> Review and Amendment Instructions`, naming the subject,
not the skill.

The preamble carries two label lines and one scope paragraph before the first section.

`Reviewed baseline:` identifies the evaluated subject revision: filename and version or
date for a document, path and commit identifier plus dirty-tree state for a repository.

`Review date:` is the ISO `YYYY-MM-DD` date the review ran.

The scope paragraph states that the report is an evaluation and an amendment
specification, that it does not modify the subject, and that it does not execute any
procedure the subject itself defines.

The preamble carries no table and no Document Information section.

### Assessment

`## Assessment` opens the report body with the narrative verdict: the subject's strongest
elements, the central improvement theme, and why additive fixes cannot repair rules that
contradict each other when such contradictions exist.

### Findings And Corrections

`### Findings and Corrections` sits inside Assessment and holds the findings table.

| Existing section  | Finding         | Required correction            |
|-------------------|-----------------|--------------------------------|
| <subject section> | <what is wrong> | <what the change must achieve> |

For a document subject the first column is `Existing section` and names the subject's own
section titles.

For a code or configuration subject the first column is `Component` and names file paths
or modules.

Every row names a concrete subject anchor.

Paragraphs after the table carry cross-cutting issues that no single row covers.

### Verification

`## Verification of <subject's proposal>` is conditional.

Include it when the subject asserts a process, design, or standard that public
authoritative sources can check, or when the request asks for external verification.

The section states what the sources support, and its `###` subsections describe the
recommended externally-grounded model the amendment instructions adopt, citing register
entries as `[S#]`.

Omit it when the review is internal-consistency only.

### Required Changes

`## Required Changes to <subject>` is always present.

Its opening paragraph states that the instructions are the amendment specification and
that the subject's own conventions - language, heading style, and structure - are
preserved, amending existing text rather than appending competing instructions.

Each `###` change group holds imperative instructions.

Short example tables, lists, or a suggested-text blockquote are allowed inside a group.

### Suggested Amendment Order

`## Suggested Amendment Order` is always present.

Bold-phase paragraphs order the change groups, naming which decisions must land first
and why later groups depend on them.

### Public Source Register

`## Public Source Register` is always the last section.

An intro line states when the sources were reviewed and what they support versus what
remains a tailored proposal.

| ID | Source   | Relevance and limit             |
|----|----------|---------------------------------|
| S1 | <source> | <what it grounds and its limit> |

Every `[S#]` cited in the body resolves to a register row, and every register row is cited
in the body.

The report ends after the register with no closing line.

## Change Review Variant

The change-review variant is a second form of the review report: a source-only
evaluation of a code change set - a commit range, a pull or merge request, or a branch
diff - that ends in findings, a readiness assessment, and proposed actions.

### Variant Resolution

The variant applies when the request scopes the subject to a change set rather than a
whole artifact: "review these commits", "review this pull request", "przegląd zmian".

A request to review a repository, codebase, or document as a whole stays an audit or a
canonical review report.

The resolved variant appears in the Parameter Configuration summary next to the report
type.

### Change Review Structure

The variant carries exactly these elements, in this order.

### Identification Table

A key-value table opens the report directly under the title with an empty header row:
the labels are self-describing, so header cells stay blank while the separator row is
kept.

Rows render only for established facts.

A row whose value is unavailable is omitted rather than filled with `UNKNOWN` or a
translated equivalent.

Canonical labels are `Change review` (the MR/PR reference, or `On-request review` when
no MR/PR exists), `Branches`, `Commit range`, `Authors`, `Review date`, `Change size`,
`Change documents`, and `Decision`.

`Authors` lists human authors only and never names the agent, the tool, or the skill.

`Decision` carries the verdict enum verbatim - `APPROVE`, `APPROVE WITH COMMENTS`,
`REQUEST CHANGES`, or `REJECT` - and is the verdict's only home: no dedicated decision
section exists.

### Change Summary

`## Change Summary` summarizes the change set in a table keyed by `Category`, `Files`,
and `Key change`: the changed content first, the review process second.

### Review Scope

`## Review Scope` states what was reviewed - the range, the source-only method, any
exclusions, and which evidence is reported rather than observed.

### Findings

`## Findings` is two-layered.

A scan table carries `Identifier`, `Severity`, `Location`, `Recommendation`, and
`Status` - no description column, since table cells hold neither paragraphs nor
per-row anchors.

Severity is a closed adjectival scale - `Critical`, `High`, `Medium`, `Low` - and `Low`
covers informational findings.

Below the table, each finding renders an `<a id="f-xx">` anchor, a `**F-xx**` bold
label, and a paragraph carrying the fact plus its consequence.

Identifiers inside the scan table stay plain text.

Every `F-xx` in prose or another table is a `[F-xx](#f-xx)` link to its description.

### Dimension Assessment

`## Dimension Assessment` evaluates the review dimensions in a table whose `Evidence`
column holds finding links or source anchors.

### Verification And Testing

`## Verification and Testing` states which verification ran - usually none, since the
review is source-only - and what remains for testers.

### Production Readiness

`## Production Readiness` carries the risk level and merge conditions in prose.

### Action Proposals

`## Action Proposals` closes the report with a table of proposed actions whose columns
are `Action`, `Owner`, `Related identifiers`, `Deadline / condition`, and `Status`.

The table carries no ordinal column - row order already expresses the sequence, and
findings are referenced through `Related identifiers` links rather than row numbers.

### Change Review Conventions

Headings carry no section numbers and use the shortest complete two-word names.

A one-off change review carries no history section: an iteration record appears only
when the review revision exceeds `1.0`.

Descriptive cells in every table follow the capitalization rule of
`principles/output-style.md`: they start uppercase, while identifiers, branch names,
user names, proper names, and code spans stay verbatim.

A column is dropped when its values carry no information beyond the other columns, and
dropping one edits the header, the separator, and every row - then
`scripts/format-table.py --drop-empty-columns` removes leftovers.

## What A Review Report Never Contains

A canonical review report never carries audit-report machinery: Document Information,
the coverage
and assurance matrix, Glossary, Executive Summary, scorecard or rubrics, risk or debt
registers, a remediation roadmap with `REC-` identifiers, `EVD`/`FND`/`RSK` identifiers,
Scope Exclusions, a dedicated Limitations section, a Validation Record, or a References
section.

The change-review variant additionally never carries the canonical review machinery:
Assessment, Findings and Corrections, Required Changes, Suggested Amendment Order, or
a Public Source Register.

The Public Source Register takes the place of References.

Information that cannot be established is stated inline where it matters with `UNKNOWN`,
`NOT SPECIFIED`, or `INSUFFICIENT INFORMATION`, never dropped silently.

## Formatting

The Formatting Rules of `process/report-format.md` apply unchanged: `#`/`##`/`###`
headings only, one-sentence paragraphs, the selected wrap width, no semicolons in prose,
ASCII hyphens, and tables aligned by `scripts/format-table.py`.

No Contents section is added: the report navigates by its fixed section order.

## Re-Review And Revisions

The first review of a subject is revision `1.0` and defaults to `REVIEW-1.0.md`.

Each subsequent review increments the revision and writes a new file per
`synthesis/report-comparison.md`, and the previous file is never overwritten.

A re-review re-evaluates the subject's current revision and carries no dedicated
comparison section: the `Reviewed baseline` preamble records what was evaluated.

## Detail Levels

`Standard` renders the full structure above.

`Detailed` deepens verification and adds per-instruction rationale and worked examples
inside Required Changes.

`Brief` condenses the findings table and the change groups, but Assessment, Required
Changes, Suggested Amendment Order, and Public Source Register are still present.

## Languages

A non-English review renders through the matching `translations/` file per
`principles/output-style.md`, with analysis still running in English.

The Polish filename stem is `PRZEGLĄD`, defined in `translations/polish-language.md`.

## Validation

`scripts/validate-report.py` detects a review report by an H1 ending in
`Review and Amendment Instructions` or by a canonical `REVIEW`-family or
`PRZEGLĄD`-family filename (a bare stem or a `-<revision>` suffix), and then runs:

- The shared mechanical checks: heading depth and spacing, semicolons, non-ASCII dashes
  and arrows, table alignment, output-location pattern, and trailing whitespace.
- Required sections present: `## Assessment` with `### Findings and Corrections`,
  `## Required Changes`, `## Suggested Amendment Order`, and `## Public Source Register`.
- The findings table carries `Finding` and `Required correction` columns.
- Required Changes holds at least one `###` change group.
- Every `[S#]` citation resolves to a register row and every register row is cited in
  the body.

A `REVIEW`-family filename carrying a custom suffix - a subject, slug, or date instead
of a revision number - is a custom report and receives the shared mechanical checks
only: a user-supplied template overrides the canonical section contract.

A canonical review filename carrying `## Findings` and `## Action Proposals` but no
`### Findings and Corrections` selects the change-review contract instead:

- The seven canonical sections present in order: Change Summary, Review Scope,
  Findings, Dimension Assessment, Verification and Testing, Production Readiness,
  Action Proposals.
- The first table of the report is the identification table: an empty header row and
  no row rendering an unavailable value.
- The findings table carries `Identifier`, `Severity`, `Location`, `Recommendation`,
  `Status`, and no description column.
- The actions table carries `Action`, `Owner`, `Related identifiers`, `Status`, and no
  ordinal column.
- Severity values come from the closed `Critical`/`High`/`Medium`/`Low` scale.
- Every `F-xx` row resolves to an `<a id="f-xx">` anchor and a `**F-xx**` description
  label, and every `[F-xx](#f-xx)` link resolves to an anchor.
- Every `F-xx` outside the identifier column is a link.

Audit-only checks - baseline sections, `FND`/`RSK`/`REC` cross-references, finding blocks,
PAR rows, glossary, and the final-state gate - do not run on a review report.

For a non-English review, run the validator on the English-mapped working copy described
in `scripts/README.md`, with the review headings and the title suffix mapped to English.

Produce the report in this order: finish all content, run `scripts/format-table.py`,
then run `scripts/validate-report.py`, iterating until it reports zero issues.

`link-glossary.py` does not run on review reports, which carry no Glossary.
