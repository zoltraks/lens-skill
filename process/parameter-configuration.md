# Parameter Configuration

## Purpose

> **Scope:** The audit parameter surfaces, their defaults, and the resolution rules
> applied before any audit begins
> **Key items:** core parameters table, the mandatory ask, automated resolution,
> output location and filename rules, re-audit parameters

Before beginning the audit, the agent runs the Parameter Configuration phase in
`process/audit-workflow.md` and MUST ask whether to accept defaults or configure.

Defaults are:

| Parameter               | Default                                                                                                                                                                                      |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Report style            | a style named in the request, then the recovered previous style on re-audit - `audit` governance report (fallback default), `hunt` defect-hunt report, or `review` execution-register report |
| Report delivery         | File if `audit/` or `report/` exists under `docs/`, `document/`, or `doc/` - `review/` or `reviews/` for a review report - else Inline                                                       |
| Output location         | Resolved across `docs/`, `document/`, `doc/` roots or the repository root                                                                                                                    |
| Output filename         | `AUDIT-1.0.md` or language-specific revisioned name, `AUDIT-<revision>.md` on re-audit - `HUNT.md`/`REVIEW.md` for a first hunt/review                                                       |
| Report language         | Match the language of the user's request                                                                                                                                                     |
| Detail level            | Detailed                                                                                                                                                                                     |
| Evaluation scale        | 1-10 (options: 1-5, 1-3, Stars - count via follow-up)                                                                                                                                        |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                                                                                                                                      |
| Trade-off analysis      | Standalone section + embedded into relevant findings                                                                                                                                         |
| Descriptive mode        | Enabled - a Glossary section defines every acronym used and body occurrences link to it                                                                                                      |
| Evidence mode           | `source-only` (default), `executed-readonly` analyzers, or `executed-commands` commissioned commands                                                                                         |

When intake detected a runnable suite or build - test directories, CI configuration, or test
scripts - the presented defaults summary annotates the `Evidence mode` row with a note such as
`a runnable suite exists at <path>; executed-commands could run it`.

The annotation is informational only - it adds no question surface, and automated runs keep
the `source-only` default.

The agent MUST ask this question, MUST NOT skip it, and MUST wait for the user response
before starting the audit - core configuration covers unresolved delivery and report-shape
choices, while advanced parameters apply the defaults unless explicitly requested.

An automated, unattended, or non-interactive request suppresses every question surface per
`process/audit-workflow.md` and `process/decision-modes.md` - gates resolve to discovered or
default answers, the report writes without asking, and explicit parameter statements still
win.

Output location resolves under the audited root: `audit/` > `report/` > bare root across `docs/`,
`document/`, `doc/` > repository root - a `report/` base descends into its style-matching `audit/`
or `review/` subdirectory, a dedicated `review/` or `reviews/` directory wins for a review
report, and a recorded version or date subdirectory pattern is reused.

The output filename carries the report revision: `AUDIT-1.0.md` for a first audit or the
language-specific revisioned name such as `AUDYT-1.0.md`. The bare filename is the audit-style
alternative, while a first hunt or review takes the bare `HUNT.md`/`REVIEW.md` stem with
`HUNT-1.0.md`/`REVIEW-1.0.md` revisioned, a previous report gives the incremented revision -
the last decimal component increments and carries on nine, so `1.0` becomes `1.1`, `1.9`
becomes `2.0`, and `9.9` becomes `10.0` - and is never overwritten, a bare `<stem>.md` is renamed to its revisioned
name first, and the agent confirms with the user before writing unless the run is automated.

If the user accepts defaults or says "bypass", the agent proceeds immediately.

On configure the agent asks the unresolved core parameter questions in `process/audit-workflow.md`.

Each prompt marks the default and ends with `Use default: <value>` and `Use defaults for all
remaining questions` - when the request asks for parameters in JSON or another machine-readable
format, or names a diagnostic, timing, or verbose mode, apply `process/json-exchange.md` to every
pending question surface. A diagnostic, timing, verbose, or informational mode applies
`process/operation-timing.md` to the operation's closing report. Non-English reports load the
matching `translations/` file and apply every translation, style, and encoding rule.

## Rerunning An Audit

When the user asks to rerun, regenerate, or update an audit, or a previous report exists in the
audited location, resolve the audit mode per `process/audit-workflow.md` and
`synthesis/report-comparison.md`: re-audit, re-audit with changed parameters, or fresh audit.

The previous report is never overwritten - write the next revision-numbered file such as
`AUDIT-1.1.md`, renaming a bare `<stem>.md` previous report to its revisioned name first.

A style named in the request takes precedence over the recovered previous style - asking for a
general audit report after a `HUNT` report proposes `audit` - while an unnamed style keeps the
recovered value as the proposed default.

## Evidence Parameters

Two advanced parameters govern what evidence may be touched.

They apply the defaults unless the request names them.

| Parameter               | Default | What it controls                                                         |
|-------------------------|---------|--------------------------------------------------------------------------|
| `evidence-exclusions`   | none    | User-declared paths or patterns withheld from evidence gathering         |
| `dependency-advisories` | `off`   | Whether a commissioned advisory sweep may run or be fetched for the SBOM |

`evidence-exclusions` lists paths, file names, or glob patterns the audit never opens,
quotes, or summarizes - the canonical use is a prior report when the user asks for a
fresh, independent audit.

Honored exclusions are recorded in the Auditing Methodology section, and every parallel
scout brief repeats them per `process/parallel-execution.md`.

Excluding the previous report degrades a re-audit to a full audit - no baseline exists
to diff against, and the report states the exclusion rather than a changes section.

`dependency-advisories` permits the sweep only where the evidence mode allows it -
`executed-readonly` for non-mutating scanners such as `npm audit` or `osv-scanner`,
`executed-commands` for other commissioned commands, or an explicit web-fetch commission
for public advisory data.

When the sweep runs, advisory IDs land in the SBOM `Advisory` column per
`assessment/dependency-review.md`.

When it is `off` or the evidence mode disallows it, the column keeps its honest
`Not checked` or `N` entries - freshness flags alone never claim advisory status.
