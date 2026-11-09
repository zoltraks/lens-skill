# Report Validation

## Purpose

> **Scope:** The Validation phase of the audit workflow - the mechanical validation chain and the
> evidence and decision checks **Key items:** tool chain, fix loop, evidence and decision checks

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after Synthesis.

## Contents

| Section                      | Line | What it covers               |
|------------------------------|------|------------------------------|
| Validation                   | 20   | Validation                   |
| Evidence And Decision Checks | 336  | Evidence And Decision Checks |


## Validation

`scripts/validate-report.py` detects the report style and applies that style's contract.

Run `scripts/check-model.py work/audit-model.json` first - a model that fails is never generated
from - then run `validate-report.py` with `--model work/audit-model.json` and
`--state work/audit-state.json` so scorecard cells, overall scores, register blocks,
evidence citations, criteria outcomes, and the run-state vocabulary reconcile with the
records they render from.
`finalize-report.py` accepts the same two flags and passes them through.

Re-check every finding against `principles/evaluation-rules.md`.

Confirm no finding rests on an assumption, that every status has evidence or a gap token,
and that no language evaluates people.

Confirm every `FND-XXX` finding uses the correct pillar abbreviation and report-global sequential
numbering - one sequence per register family across the whole report,
`FND` contiguous per pillar across projects.

Confirm every `RSK-XXX` references its source `FND-XXX`.

Confirm every `REC-XXX` resolves a specific `FND-XXX`.

Confirm every `REC-XXX` appears exactly once in the Recommendation Classification subsection of the
Remediation Roadmap when the detail level is Standard or Detailed.

Confirm every finding that records an absent capability carries an `Absence` token with a
one-line evidence basis.

Confirm no `Security`, `Exploitability`, or `Absence` field line renders `N/A`.
The field is omitted instead - and no `Owner` line renders an unspecified value.

Confirm identifiers cited in narrative prose match register rows: a `RSK-XXX`, `FND-XXX`,
or `REC-XXX` named in a summary, readiness paragraph,
or changes section must exist in the corresponding register and refer to the same item.

Confirm no plaintext secrets, passwords, or cryptographic keys appear in summaries, observations,
or risk descriptions.

Confirm High-Level Observations contains at most five observations in the template's table and
paragraph format, each anchored to a specific `FND-XXX`.

Confirm strengths fit the selected detail level and are evidenced,
use fewer than the suggested count when the input supports fewer, rather than padding the report.

Confirm the Solution Comparison section uses the standard table format and frames each trade-off
against a stated constraint.

Confirm every adverse finding in an initial audit has `Status` `Open`.

For re-audits, preserve IDs and update closure states only from the required evidence.

On a fresh audit over an existing report,
confirm the new report carries no Changes Since Previous Audit section, no `Previous Report` row,
and no identifier or remediation status carried over from the previous report,
while its revision still increments.

When the previous report predates the current schema,
read its field and column names through the legacy mapping in `synthesis/report-comparison.md`
before comparing, and name the rename as a capability change in the Changes Since
Previous Audit section.

When a Changes Since Previous Audit section is present,
confirm the previous report file still matches the checksum recorded at baseline confirmation,
the new filename carries the incremented revision, every transition cites current evidence,
and no identifier from the previous report was reused for a different finding.

Confirm each conditional section was evaluated: it is either present because its criteria are met,
or omitted with a deliberate one-line justification in Scope Exclusions.

No conditional section may be present-but-empty,
and none relevant to the subject may be silently dropped.

Changes Since Previous Audit is the exception, its absence in a first audit needs no omission note.

When a Threat Model is present, confirm every unmitigated threat traces to a `FND-XXX` and a
`RSK-XXX`, and that no plaintext secret appears in a disclosure threat.

When an API Contract Conformance section is present,
confirm each security gap maps to an OWASP API Security Top 10 (2023) code where one applies.

When a Standards Conformance section is present,
confirm every conformance judgement cites a specific rule in the standards document and a specific
file or pattern in the codebase, and that every standards-quality judgement cites a named
external best practice.

Confirm the Reference Sources section lists every external source consulted during the audit,
renders a `[title](url)` link paragraph per row,
and keeps internal repository artifacts out - files, manifests,
and paths belong to the evidence ledger, not to Reference Sources.

Confirm every material evidence item collected during Evidence Gathering surfaces in the report as a
finding, a risk, a dashboard element, or a strength,
or is recorded as deliberately unused with a reason.

Git history signals such as author concentration, commit cadence,
and tag history must appear at least as the Team & Continuity line in the Health Dashboard.

Confirm every CWE-classified security finding names its equivalent static analyzer rule from
`references/cwe-analyzer.md` with its enablement evidence,
or states that no direct rule exists for the CWE in that stack.

Confirm no finding implies an analyzer ran.

Confirm the Audit Coverage table is present after Document Information and consistent with Scope
Exclusions: every `Not done` row has a matching exclusion bullet and no `Covered` row
is disclaimed later.

Confirm every SBOM row has a License cell populated from an inspected declaration or marked
`Unknown`, every direct component is manifest-sourced,
and `Advisory` is `Y` only where committed advisory evidence exists.

Confirm every evidence-ledger row and every finding carries an `Observation` or `Concern` tag.

Confirm every `High` or `Critical` Security & Compliance finding on a network-facing surface carries
an Exploitability narrative with the tier and attack-path reasoning,
and that the field is omitted on every other finding.

Confirm no narrative claims a tier above the evidence,
`Dynamically-Verified` under the default scope is a defect.

Confirm the Delivery Practice section is present per project:
computable metrics are labeled as proxies, unmeasurable metrics are `Not specified` with reasons,
and the bus-factor rating carries its commit-share, contributor-count, and window basis.

Confirm the audit Executive Summary carries the `Product Quality` and `Engineering Process` rows in
the headline table and states the overall once, bolded,
in the key-value `Overall score` row - each numeric sub-score names its lowest dimensions,
and the paragraph below the headline table names `Product-only` and `ceiling` when they apply - per
`process/report-format/summary-changes.md`, and every place an overall score appears reports the
lowest-scoring applicable dimension and its score in a paragraph below the table,
per `synthesis/project-scorecard.md`.

Confirm the Requirements Conformance table keeps one row per requirement - a merged range row such
as `A-01 through A-11` is a defect.

Confirm every numeric dimension has evidence IDs, confidence, and a justified score point or cap.

Confirm `Unknown` and `N/A` dimensions are excluded from the mean.

Confirm the maturity level, readiness state, blocking risks,
and sign-off status agree with `process/readiness-scoring.md`.

When an API Compatibility And Versioning Discipline section is present,
confirm it addresses gate presence, versioning-scheme consistency, and breaking-change tracking,
and that configured tools are treated as intended checks, not executed ones.

When a Technical Debt Register is present,
confirm every `TDR-XXX` traces to a `FND-XXX` or a cited direct observation,
and that no security risk is duplicated from the Unified Risk Register.

When a Follow-up Plan subsection is present,
confirm every row references a `FND-XXX` and that owners or dates absent from the input are marked
`Not specified` rather than invented.

Confirm the Auditing Methodology cites only the reference standards actually applied,
including the stack-specific canonical sources from `references/stack-standards.md` that were
consulted, and the Scope Exclusions state the OWASP category coverage.

Confirm the report follows `process/report-format.md` section by section.

Confirm the report path matches the output directory recorded during Output location discovery.

If it does not, correct the path before writing.

Confirm the report follows the Formatting Rules in `process/report-format.md`:
headings stop at `###`, prose lines over the selected wrap width (default 100) are wrapped,
prose contains no semicolons, and every table was formatted with an automated script so all `|`
separators align vertically in plain text.

When the report language is not English,
confirm the rendered language checks in the matching `translations/` file pass:
all calque-table forms absent, status tokens rendered in the report language,
and the language-consistency checks clean.

Confirm `System type`, `Maturity level`, `Audit Purpose`,
and the readiness gates do not contradict one another - a `production system` claim against a
`pre-production` engagement context, or an `AI Governance Audit` exclusion used to suppress
AI-provenance findings, is a defect to resolve before delivery.

Confirm Document Information carries `Subject Revision` with the recorded commit SHA or the
`unversioned working tree` token, `Dirty-Tree State` when the tree is dirty, and the evidence mode.

When an external report was found during intake,
confirm the Contradiction Register is present with a status on every row per
`synthesis/report-triangulation.md`.

Confirm every finding's `Evidence` field cites `path:line` ranges wherever the claim
rests on source code.

A file-level citation is acceptable only for an absence claim that also names the search
performed or the hops traced.

Recompute the scorecard's stated overall from the displayed applicable dimensions and confirm it
equals the reported mean after the documented rounding rule.
`Unknown` and `N/A` dimensions stay out of the denominator.

Confirm no summary table promotes a finding's verification status beyond what its block carries.
A finding whose `Confirmation` field is not `Yes` cannot appear as execution-confirmed in any summary.

Under `executed-readonly`, confirm the Executed Evidence lists every executed check with tool,
version, exact command, and timestamp, and that the report claims no build, test, or project run.

Under `executed-commands`, confirm the same provenance in the log or Execution Register and that
only the commissioned commands ran.

Under `source-only`, confirm the Further Verification covers every material claim that could not be
resolved from source, each entry naming command, pass criteria,
and the finding it would confirm or close.

When the report style is `hunt` or `review`, confirm the layout, verdict block,
and rating columns match `process/report-format/hunt-style.md` or
`process/report-format/review-style.md`.

The fix-and-revalidate loop is bounded - three iterations of fix-then-re-validate,
then stop and surface the remaining issues instead of looping further.

In interactive mode present the leftover validator output and ask whether to try again,
deliver with named limitations, or pause for investigation.

In automated mode the run records the unresolved issues in the Validation Protocol and proceeds to
the publication-stop evaluation - a material validator error still blocks final publication per
`process/audit-model.md`.

Run the Pre-Delivery Mechanical Checklist in `process/report-format.md` and require zero violations.

Copy `scripts/validate-report.py` into the audited repository as `validate-report.tmp.py` and
run it on the report.

The validator prints at most ten problems per check, so fix, re-run the formatter,
and re-validate until it reports zero issues.

When the report language is not English,
`scripts/validate-report.py` refuses the file with exit 2 and guidance - the English contract never
runs on a translated report directly.

Instead, run
`scripts/map-translation.py <report> --rules translations/polish-language.md --en <english-sibling.md>`
to generate an English-mapped working copy:
it inverts the contract tables to translate `- **Field:**` finding-block labels,
fixed-vocabulary values, and section headings,
and remaps every report-internal anchor - glossary links, `### <ID>:` heading links,
the evidence-ledger and validation-protocol section anchors - to their English forms.

A copy that maps only field labels lets the validator skip the required-sections, glossary,
and final-state checks instead of running them.

The fuller mapping makes every check execute on the translated report.

Run the table formatter on the working copy as well, since anchor remapping changes cell widths.

The translated-report gates then run in this order:
`scripts/lint-polish.py <report> --rules <translations/polish-language.md>`,
`scripts/lint-prose.py <report>`, `scripts/link-glossary.py <report> --lang pl --check`,
`scripts/check-translation.py <report> --rules <translations/polish-language.md>` for summary-title
agreement, prose-count reconciliation, block field-label conformance, internal-anchor resolution,
untranslated-heading detection, field-value capitalization, governed tokens inside code spans,
the `TDD` ban, and the warn-level sentence-length review,
then the mapped-copy format and validation pair - the block-label and anchor checks must run first
so their failures surface as contract violations instead of inexplicable mapped-copy field losses.

The Validation Protocol names every checklist or validator violation the report carries.

Judge every gate by its own printed summary and exit code - a follow-up shell command such as
`grep -c` finding zero matches exits 1 on a passing run and does not mean the gate failed.

Stage any validation working copies, `.tmp.` script copies,
and intermediate report parts under the audited repository's gitignored `work/` directory from the
start, and confirm they were removed or sit inside `work/` before reporting done - nothing
disposable lands in a tracked directory.

Run the Mandatory Core Checklist and Consistency Gate in `process/report-parity.md`.

Run the delivery gate as the last operation before the completion message -
`finalize-report.py --gate --model work/audit-model.json --state work/audit-state.json` - and
deliver only on `DELIVERY READY`.

The authored-side checklist in `references/delivery-checklist.md` consolidates what the validator
enforces - run it against the assembled report before the gate so the gate
confirms, never discovers.

Write the Known Limitations and Validation Protocol sections from their outcome.

The report is complete once every gate result is recorded in the Validation Protocol - generated
reports carry no state marker.

Before the completion message, reconcile the artifact declarations in `work/audit-state.json`
against disk per `process/run-state.md` - a missing declared path produces a `Missing artifacts`
block naming the path and its declaring phase,
reported without repair and never blocking completion.

Read the current system time again as the last operation when producing the report,
after the checklist, validator, and parity gate have all passed.

Compute the elapsed time from the post-configuration start timestamp to that final reading and write
it as `MM:SS` in the `Time taken` row of Document Information.

Include the same value in the completion message to the user, for example `Time taken 13:45`.

The measured window spans loading the audit rule documents, evidence gathering, part composition,
concatenation, formatting, and validation:
an interrupted or re-done assembly does not reset the start timestamp.

A context window nearing exhaustion never truncates or simplifies the audit process - the remaining
work divides into further phases or tasks,
transient state materializes in the working directory as `.tmp.` progress notes, ledgers,
and partial artifacts, and independent phases spawn scout subagents that read their
inputs from those files.

On a re-audit, state in the same completion message that the baseline file is unchanged
from the intake record.

When no reliable start timestamp exists - for example when revising a report whose audit predates
this rule - omit the row instead of inventing a duration.

## Evidence And Decision Checks

- Reconcile all counts with their source and scope, including tests, findings, risks, and scores.
- Ensure every `Critical` and `High` finding records a counter-check and verification limit.
- Keep build, test, scanner, and runtime claims consistent with the evidence ledger.
- Confirm no build, test, or tool execution was performed or implied by the audit.
- Distinguish observed defects, unverified threats, and missing evidence in every summary.
- Check applicable security findings for CWE mapping and justified CVSS vectors or gap tokens.
- Recompute risk-matrix placements and any totals rather than estimating them in prose.
- Check that shared references use project-qualified IDs, never ambiguous labels such as "both".
- Require applicable readiness evidence and confirmed verification ownership before sign-off.
- Report unknown cost inputs, unmeasured SLOs, and missing business artifacts prominently.
- Preserve evidence limitations even in Brief reports.
- Diff the final `git status --porcelain` output against the intake snapshot - any delta beyond
  audit-created artifacts is reported, never silently left.
- Sweep the finished report for every sensitive literal gathered during evidence collection -
  secrets, internal hostnames, addresses, and personal data appear only as redacted tokens.


## Double Verification

Validation runs at least twice, never once:

1. **Post-assembly pass** - immediately after the report body is complete:
   full `validate-report.py`, plus an eyeball pass over every table's column shape,
   every Document Information cell, and every register heading.
   An edit that applied zero replacements is a failed edit - assert each scripted change landed.
2. **Post-adjustment pass** - after `final-adjustments.md` or any manual fix:
   re-run the whole validation battery, not the failing check alone - fixes move prose,
   and moved prose breaks links, widths, and anchors elsewhere.

The validator is the floor, not the ceiling: it tolerates surfaces the spec forbids (stale sections,
verbose cells, duplicated legends). When the mechanical pass is clean,
compare the report's conventions against the newest shipped example report before declaring it done.

The audit workflow ends here - the completed report and its recorded Validation Protocol are
the final artifacts.
