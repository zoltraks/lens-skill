# Report Parity

## Purpose

> **Scope:** The mandatory core checklist applied to every audit report and the consistency
> gate that runs before a report is marked `Final`
> **Key items:** core checklist, capability set, consistency gate, applicability
> justifications, cross-report discovery

This file defines what a complete audit report must contain regardless of subject, language,
or detail level.

Check the list explicitly before finalizing any report. Do not rely on per-run memory of what
a previous report happened to include.

## Mandatory Core Checklist

| Item   | Requirement                                                                                                                                     | Governing file                       |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| PAR-1  | Every security finding carries a CWE ID, `UNKNOWN`, or a justified `N/A`                                                                        | `assessment/security-review.md`      |
| PAR-2  | The severity table carries a one-line note that severity derives from the impact-likelihood matrix, not CVSS                                    | `process/report-format.md`           |
| PAR-3  | Scoring Rubrics include the ISO/IEC 25010:2023 coverage crosswalk as a mapping, not a conformance claim                                         | `synthesis/project-scorecard.md`     |
| PAR-4  | The Technical Debt Register separates remediation cost from cost of delay per CISQ/SQALE                                                        | `synthesis/debt-register.md`         |
| PAR-5  | The evidence pass ran the `git log` author/commit concentration check and surfaced it as the Team & Continuity line                             | `process/report-format.md`           |
| PAR-6  | A source-only component inventory was produced from the ecosystem's manifest or lockfile                                                        | `references/dependency-manifests.md` |
| PAR-7  | The Limitations and Unknowns section lists every check that would require execution and was not performed                                       | `process/report-format.md`           |
| PAR-8  | The Validation Record self-check table is present and complete                                                                                  | `process/report-format.md`           |
| PAR-9  | Reference standards were re-derived from the per-stack lookup for the detected stack, never copied verbatim from a prior report                 | `references/stack-standards.md`      |
| PAR-10 | When Descriptive mode is enabled, the Glossary indexes every acronym used and every body occurrence links to its description or the index table | `process/report-format.md`           |

PAR-5 may report `NOT COLLECTED` when Git history is unavailable, silence is not acceptable.

PAR-9 re-derivation means re-selecting references from the current stack lookup for the
detected stack. Identical output to a prior report is expected when the stack is unchanged,
the requirement forbids inheriting the list without re-deriving it.

## Capability Set

A report's capability set is the union of:

- Checklist items applied.
- Baseline and conditional sections present.
- Required per-section elements (severity clarification, ISO crosswalk, Team & Continuity
  line, component inventory, score formula, score floor, confidence, and readiness state).

The Validation Record renders this set so a future report can diff it mechanically.

## Consistency Gate

Run this gate before marking a report `State: Final`.

1. Build the report's capability set.
2. Diff it against the Mandatory Core Checklist: every item is `Applied` or `N/A` with an
   applicability justification.
3. Diff it against the most recent audit report found for ANY subject during intake
   discovery. Extract that report's capability set from its Validation Record when present,
   otherwise from its section headings.
4. Apply any capability present in that report but absent here, or record an explicit
   inapplicability justification (for example, "API Compatibility pillar: `N/A`, subject is a
   service, not a library"). Inheriting an omission from the subject's own prior revision is
   never a justification.
5. When no other report is accessible, record `none found` and gate on the checklist alone.
6. Run the semantic consistency checks for identifiers, scores, risk placement, evidence references,
   conditional-section justifications, translation tokens, and project-qualified shared references.
7. Record the outcome in the Validation Record, then set `State: Final` only when the structural and
   semantic gates both pass.

A report may be complete and useful while remaining `Draft` when a gate fails. Do not weaken the
report to make the gate pass.

When the most recent baseline predates the current skill version, the Validation Record names
which sections were added for parity versus which compare as content. Added structural sections
are capability differences, not product changes.

## Applicability And Justification

An item is `N/A` only when genuinely inapplicable to the subject. `N/A` never means "not
checked" - the check ran and was judged inapplicable.

Justifications live in the Validation Record's Evidence / Justification column. Omitted
conditional sections also appear in Scope Exclusions.

## Discovery Scope

The cross-report diff searches the same locations as previous-report discovery:
`docs/audit/`, `docs/report/`, `docs/`, the repository root, and the document structure when
governed by another skill.

"Most recent" is the audit report with the highest revision number and latest report date
among files matching the audit naming pattern. A report the user supplies also counts.

The gate is bounded by accessible files. Record that bound in the Validation Record when
discovery finds nothing.

## Rules

- *Run the checklist on every report, including Brief reports.*
- *A capability in a newer report on a different subject must be applied here or justified as
  inapplicable - never silently dropped.*
- *A failed gate keeps the report `Draft`.*
- *The Validation Record is part of the report - its absence fails the gate itself.*
- *A shared multi-project reference must use a stable project-qualified identifier.*
- *A machine-readable token must remain unchanged in translated reports.*
- *A passing structural check does not override a failed semantic check.*
