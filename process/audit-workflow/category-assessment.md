# Category Assessment

## Purpose

> **Scope:** The Category Assessment phase of the audit workflow - per-category assessment
> dispatched to the matching assessment files **Key items:** category checklist
> dispatch, conditional files

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Evidence Gathering.

On completion, proceed to `process/audit-workflow/report-synthesis.md`.

## Category Assessment

For each category, open the matching `assessment/` file and apply its checklist.

For a full audit, this includes the two additional categories `assessment/generated-code.md` and
`assessment/copyright-review.md`, plus `assessment/structure-review.md` for the `audit` and `review`
report styles - the structure assessment never loads under `hunt`.

On a code-bearing subject `assessment/correctness-review.md` also loads for every style - its census
results feed the `FNC` criteria and the findings register.

On a code-bearing subject the same styles also load `assessment/code-style.md`,
which runs after `assessment/standards-conformance.md` has surfaced the project's declared
conventions and before `assessment/code-quality.md` consumes the enforcement findings.

Evaluate the inclusion criteria for each conditional assessment,
listed in the Conditional Sections table of `process/report-format.md`.

When the criteria are met, open the matching conditional file and apply it:
`assessment/data-flow.md`, `assessment/design-patterns.md`, `assessment/threat-model.md`,
`assessment/api-contract.md`, `assessment/skill-definition.md`, `assessment/ai-system.md`,
`assessment/standards-conformance.md`, and `assessment/api-compatibility.md`.

When the criteria are not met, omit that section and record the deliberate omission
for Scope Exclusions.

Do not force a conditional section onto a subject it does not fit.

Run every probe activated by the domain profile before assigning statuses.

A skipped probe needs a recorded reason.

Assign a status (`Pass`, `Partial`, `Fail`, `Unknown`, `N/A`)
per the rules in `principles/evaluation-rules.md`.

Under scoring policy 3 every criteria outcome lands on an anchor the entry declares - read the
allowed `levels` from `references/criteria-catalogue.json` before assigning a level,
since anchors differ per entry and an intermediate level an entry does not declare
fails the model check.

For each finding that records an absent capability,
also record its absence assessment per `principles/evaluation-rules.md`.

Record evidence, concrete risks, and neutral notes for each category.

