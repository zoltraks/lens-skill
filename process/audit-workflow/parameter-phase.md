# Parameter Phase

## Purpose

> **Scope:** The Parameter Configuration phase of the audit workflow - acceptance gate,
> delivery and output file, report language and style, evidence mode,
> and detail **Key items:** parameters-acceptance, report-delivery, evidence mode, bypass

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it after intake.

On completion, proceed to `process/audit-workflow/scope-definition.md`.

## Contents

| Section                                    | Line | What it covers                             |
|--------------------------------------------|------|--------------------------------------------|
| Parameter Configuration                    | 36   | Parameter Configuration                    |
| Saved Parameters (`work/lens-params.json`) | 171  | Saved Parameters (`work/lens-params.json`) |
| Parameter Prompts                          | 197  | Parameter Prompts                          |
| Delivery And Output File                   | 225  | Delivery And Output File                   |
| Previous Report Files                      | 377  | Previous Report Files                      |
| Report Language                            | 397  | Report Language                            |
| Report Style                               | 419  | Report Style                               |
| Project Layout                             | ?    | Project Layout                             |
| Evidence Mode                              | 453  | Evidence Mode                              |
| Detail Level                               | 497  | Detail Level                               |
| Evaluation Scale                           | 513  | Evaluation Scale                           |
| Improvement Suggestions                    | 542  | Improvement Suggestions                    |
| Trade-off Analysis                         | 555  | Trade-off Analysis                         |
| Descriptive Mode                           | 567  | Descriptive Mode                           |
| Bypass Rule                                | 581  | Bypass Rule                                |


## Parameter Configuration

Before beginning the audit, ask the user whether to accept the default parameters,
configure the core parameters, or specify the operation to run - the `parameters-acceptance`
`choice` parameter under JSON exchange.

Present the defaults in a compact summary.

Default parameters:

| Parameter               | Default                                                                                                                                                                                                                                                                        |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Report style            | a style named in the request, then the recovered previous style on re-audit - `audit` governance contract, `hunt` defect-hunt genre, `review` execution-register genre; `audit` is the fallback default                                                                        |
| Report delivery         | File if `audit/` or `report/` exists under `docs/`, `document/`, or `doc/` - `review/` or `reviews/` for a review report - else Inline                                                                                                                                         |
| Output filename         | `AUDIT-1.0.md` or language-specific revisioned name, `AUDIT-<revision>.md` on re-audit - `HUNT.md` for a first hunt, `REVIEW.md` for a first review                                                                                                                            |
| Report language         | Match the language of the user's request                                                                                                                                                                                                                                       |
| Language output         | `pair` when the report language is not English, or when the previous report was a language pair, the English report plus its translation - the pair convention survives a report-style switch, `single` when the request scopes to one language and no pair convention applies |
| Detail level            | Detailed                                                                                                                                                                                                                                                                       |
| Evaluation scale        | 1-10 (options: 1-5, 1-3, Stars - count via follow-up)                                                                                                                                                                                                                          |
| Improvement suggestions | Include with priorities (P1-P4 roadmap)                                                                                                                                                                                                                                        |
| Trade-off analysis      | Standalone section + embedded into relevant findings                                                                                                                                                                                                                           |
| Project layout          | `separate` - each project gets its own `##` block (multi-project only); `combined` groups every register into shared tables with a `Project` column                                                                                                                            |
| Descriptive mode        | Enabled - a Glossary section defines every acronym used and body occurrences link to it                                                                                                                                                                                        |
| Evidence mode           | `source-only` - `executed-readonly` runs commissioned non-mutating analyzers, `executed-commands` adds commissioned non-mutating commands such as tests and builds                                                                                                             |

When intake detected a runnable suite or build - test directories, CI configuration,
or test scripts - the presented summary annotates the `Evidence mode` row with a note such as
`a runnable suite exists at <path>; executed-commands could run it`.

The annotation is informational only - it adds no question surface,
and automated runs keep the `source-only` default.

The same intake note names each declared check the audit cannot run under `source-only` -
a declared coverage gate, advisory sweep, or packaging check stays visible as a declared-but-unrun
item so the evidence-mode decision sees the full declared surface, never only the test suite.

**Gate** - `parameters-acceptance`: a blocking gate per `process/decision-modes.md`.

The agent MUST ask the user and MUST NOT skip this step.

The agent MUST wait for user response before proceeding to Scope Definition.

The question offers three answers: `Accept defaults`, `Configure options`, and `Specify operation`.

`Accept defaults` proceeds immediately to Scope Definition
(`process/audit-workflow/scope-definition.md`) using the values above.

`Configure options` asks only the unresolved core parameter prompts in the order below.

`Specify operation` asks which operation the skill should run - the `operation-selection` `choice`
parameter under JSON exchange - with three options:

- `Full audit` (default) - the operation the request already implied,
  resolves the acceptance as `Accept defaults` and proceeds to Scope Definition.
- `List all operations` - delivers the operations catalog inline per
  `process/operations-catalog.md`, then re-presents the `operation-selection` question.
- `Custom operation` - asks for a free-text description of the requested operation,
  the `operation-description` `text` parameter under JSON exchange.
  A description naming a report artifact applies the named report style or review scope as an
  explicit parameter statement and proceeds to Scope Definition with the remaining defaults,
  a description naming another skill operation routes to that operation's own procedure,
  and a descriptive request answers inline without entering this workflow.

An automated run skips the question and resolves parameters per the Automated Run block in
`process/audit-workflow/audit-intake.md` - the parameter-resolution timestamp rule
below still applies.

Output filename carries the report revision: `AUDIT-1.0.md` for a first English audit,
or the language-specific revisioned name from the matching `translations/` file
such as `AUDYT-1.0.md`.

When the language output is `pair`, both files share the English report stem and differ only by the
language suffix - `AUDIT-1.0-EN.md` and `AUDIT-1.0-PL.md` for a Polish rendering - and the
language-specific stem such as `AUDYT` names only a single-language report.

Resolve the pair filenames during intake,
before authoring starts - a report written as a bare `<stem>.md` and given a translation sibling
later still needs the rename.

When a translation sibling is produced for a report that already exists under a bare `<stem>.md`
name, rename the existing file to its `<stem>-<LANG>` form first so the pair shares the suffix
convention, and add or update the `Translations` row in both files' Document Information tables.

For the `hunt` report style the stem is `HUNT` - or the language-specific stem such as `POLOWANIE` -
and a first hunt defaults to the bare stem `HUNT.md`,
with `HUNT-1.0.md` offered as the revisioned alternative.

For `review` the stem is `REVIEW` - or the language-specific stem such as `PRZEGLĄD` - under the
same bare-first default.

When a previous report exists, the filename carries the new revision - the last decimal component
increments and carries on nine: `1.0` becomes `1.1`, `1.9` becomes `2.0`,
`9.9` becomes `10.0` - per `synthesis/report-comparison.md`.

When the previous report is a bare `<stem>.md` file in the resolved output directory,
it is renamed to `<stem>-<revision>.md` before the new report is written,
per `synthesis/report-comparison.md`.

Plain `AUDIT.md` or the language-specific filename without the revision number remains an
offered alternative.

Used only when delivery is File.

Improvement suggestions and trade-off analysis are advanced parameters.

Apply their defaults unless the user explicitly specifies another setting.

If the user accepts defaults or says "bypass", "defaults", or equivalent,
proceed immediately to Scope Definition (`process/audit-workflow/scope-definition.md`)
using the values above.

If the user chooses to configure, ask only the unresolved core parameter prompts in this order:
delivery and output file, report style, project layout (multi-project only), detail level,
evaluation scale, and evidence mode.

At each prompt, offer a bypass option to accept the remaining defaults and proceed.

When every parameter question is resolved - defaults accepted, configured answers given,
or a bypass taken - read the current system time immediately and record it as the
audit start timestamp.

Do this before loading the remaining audit rule documents (report-format, assessment, synthesis,
and reference files) and before any auditing work begins in Scope Definition and Evidence Gathering,
so the elapsed time covers document familiarization as well as the audit itself rather than the
parameter discussion.

The elapsed time is later written to the `Time taken` row in Document Information.

Create `work/audit-state.json` at the same moment and record the run's initial phase,
the gates already resolved (audit mode, project inclusion, parameters),
and the start timestamp into `run.started`, per `process/run-state.md`.

Each later phase boundary and gate resolution updates the state file,
which stays the run's resume and reconciliation record for the rest of the audit.

## Saved Parameters (`work/lens-params.json`)

Once intake resolves, write the resolved values to `work/lens-params.json` in the audited repository
- a plain JSON object carrying `subject`, `revision`, `projects`, `report_style`, `report_language`,

`language_output`, `detail_level`, `evaluation_scale`, `evidence_mode`, `output_dir`,
and `output_filename` - a `pair` language output records the two filenames in
`output_filenames` instead.

The file locks intake for the session: a later request for another report style - or a re-run after
an aborted assembly - reads the saved values instead of re-asking the parameter questions,
and `scripts/new-report.py --params` consumes them when scaffolding the next report.

A request that explicitly changes a parameter overrides the file and rewrites it.

The file never carries secrets, credentials, or fetched content.
Resolved intake values only - and it changes nothing about the source-only boundary.

The parameter file and `work/audit-state.json` are siblings: the params file locks resolved choices,
the state file locks run progress, and neither duplicates the other's content.

A fresh audit rewrites all three artifacts from this run: stale `work/lens-params.json`,
`work/audit-model.json`, and `work/audit-state.json` content from an earlier run is replaced,
never merged - registers, findings, and identifier sequences never carry over under fresh-audit
semantics, and only a confirmed re-audit inherits from the previous run's model.

## Parameter Prompts

When the request asks for machine-readable parameters or names a diagnostic or verbose mode,
all pending question surfaces emit per `process/json-exchange.md` instead of, or ahead
of, the menus below.

Present each prompt as a single question with clear options.

After each answer, confirm the choice and move to the next parameter.

Every routine prompt carries three kinds of choices:

1. The concrete options, with the default marked `(default)`.
2. A fixed trailing option `Use default: <value>` that accepts the default for this question and
   continues to the next prompt.
3. A fixed trailing option `Use defaults for all remaining questions` that accepts every remaining
   default and proceeds directly to Scope Definition.

Routine prompts are limited to delivery and output file, report style, detail level,
evaluation scale, and evidence mode.

Report language follows the request language unless the user explicitly specifies another language.
`Language output` resolves to `pair` when the request language is not English or the previous report
was a language pair, unless the request scopes to a single language - it is resolved from the
request and the discovered pair convention, not asked.

Advanced parameters use their defaults unless explicitly specified.

## Delivery And Output File

Documentation roots are `docs/`, `document/`, and `doc/`, checked in that order,
and each may contain `audit/`, `report/`, or review-family (`review/`, `reviews/`) subdirectories.

Before asking, consume the base output directory recorded during Output Location
Discovery at intake.
When intake did not record one, resolve it using the following rules,
applied in order against the root of the repository or directory being audited:

1. For a `review` -style report, if any `<root>/review/` or `<root>/reviews/` directory exists,
   use the first one in the documentation root order as the base output directory.
2. For an `audit` - or `hunt` -style report, if any `<root>/audit/` directory exists,
   use the first one in the documentation root order as the base output directory.
3. Else if any `<root>/report/` directory exists,
   use the first one in the documentation root order as the base output directory.
4. Else if the report is `review` -styled and any `<root>/audit/` directory exists,
   use the first one in the documentation root order as the base output directory.
5. Else if any bare documentation root exists,
   use the first one in the documentation root order as the base output directory.
6. Otherwise use the root of the audited repository or directory as the base output directory.

When the resolved base is a `report/` directory containing a subdirectory that matches the report
style - `audit/` for the `audit` or `hunt` style,
`review/` for the `review` style - descend into it:
the base becomes `<root>/report/audit/` or `<root>/report/review/` respectively.

After selecting the base output directory,
consume the subdirectory pattern recorded during Output location discovery at intake.

Do not re-detect the pattern here.

Resolve the output directory deterministically from the record:

| Recorded pattern   | Resolved output directory                                       |
|--------------------|-----------------------------------------------------------------|
| `version-numbered` | `<base>/<version>` using the recorded project version           |
| `date-named`       | `<base>/<current-date>` using the ISO `YYYY-MM-DD` current date |
| `none`             | `<base>` directly                                               |
| `mixed`            | Follows the pattern recorded as most recent at intake           |

When the recorded pattern is `version-numbered` but no project version can be determined,
resolve to `<base>` and note why in the question context.

The final output location must fit the existing directory structure.

Do not mix patterns: if the existing structure uses version numbers, use a version subdirectory,
if it uses dates, use a date subdirectory.

When multiple projects are present and each has a different version,
resolve the output directory once using the repository root.

The single combined report is written to one location.

Do not create per-project subdirectories unless the user explicitly requests
separate files per project.

Resolve the filename before asking.

The default filename carries the report revision:

`<stem>-<revision>.md`, where `<stem>` is `AUDIT` for `audit` -style reports,
`REVIEW` for `review` -style reports, `HUNT` for `hunt` -style reports,
or the language-specific stem from the matching `translations/` file.

A first audit uses `AUDIT-1.0.md` or the language-specific equivalent such as `AUDYT-1.0.md`.

A first hunt or review report instead defaults to the bare stem `HUNT.md` / `REVIEW.md` or its
language-specific equivalent such as `POLOWANIE.md` / `PRZEGLĄD.md`,
with the revisioned name offered as the alternative.

When a previous report exists, use the incremented filename defined in
`synthesis/report-comparison.md`.

When that previous report is a bare `<stem>.md` file in the resolved output directory,
rename it to `<stem>-<revision>.md` before writing the new report,
per `synthesis/report-comparison.md`.

The filename without the revision number, `AUDIT.md` or its language-specific equivalent,
is offered as an alternative file option for audit-style reports,
and is the default for a first hunt or review report.

**Gate** - `report-delivery`: a blocking gate per `process/decision-modes.md`,
resolved without asking only when the request already named the delivery.

Ask: "How should the report be delivered?"

Present each applicable option as a concrete choice:

- `Inline` - return the full report as the direct response.
  This is the default when no `audit/` or `report/` directory exists under any documentation root.
- `File - <resolved-path>` - write the report to the resolved path using the revisioned filename.
  This is the default when an `audit/` or `report/` directory exists under a documentation root.
- `File - <location>/<filename>` - one option for each other existing documentation location:
  remaining `audit/` and `report/` directories, remaining bare documentation roots,
  and the repository root. For example, `document/AUDIT-1.0.md` or `AUDIT-1.0.md`.
- `File - <base>/<version>/<filename>` - file location using the project version.
  Offer this only when the recorded pattern is `none` and the project version can be determined.
  When the base is a bare documentation root, offer `<base>/report/<version>/<filename>` instead.
  For example, `docs/report/<version>/AUDIT-1.0.md`.
- `File - <base>/<current-date>/<filename>` - file location using the ISO `YYYY-MM-DD` current date.
  Offer this only when the recorded pattern is `none`. When the base is a bare documentation root,
  offer `<base>/report/<current-date>/<filename>` instead. For example,
  `docs/report/<date>/AUDIT-1.0.md` for a first audit.
  Under a `pair` language output every filename option names both files,
  for example `docs/audit/AUDIT-1.0-EN.md` and `docs/audit/AUDIT-1.0-PL.md`.
- `File - <resolved-path>/<filename without the revision number>` - the resolved path using the
  filename without the revision number, such as `docs/report/AUDIT.md`,
  offered as an alternative to the revisioned default.
  For a `hunt` - or `review` -style report this option is the default and the revisioned filename
  becomes the alternative.
- `Custom report file` - ask the user to specify the location and filename.

For example, when `docs/report/` and `document/` exist with no subdirectory pattern,
the question can offer `docs/report/AUDIT-1.0.md`, `docs/report/<version>/AUDIT-1.0.md`,
`docs/report/<date>/AUDIT-1.0.md`, `document/AUDIT-1.0.md`, `AUDIT-1.0.md`,
and `docs/report/AUDIT.md` alongside `Inline` and `Custom report file`.

When `docs/report/1.6.7` exists and the project version is `1.7.3`,
the question instead offers `docs/report/1.7.3/AUDIT-1.0.md` as the only structured path,
with no date alternative.

When a subdirectory pattern was recorded at intake, do not offer the alternative pattern.

A `version-numbered` record yields only the version path,
a `date-named` record yields only the date path,
and `mixed` follows the pattern recorded as most recent.

`Custom report file` remains the escape hatch.

Like every routine prompt, the question ends with `Use default: <default option>` and
`Use defaults for all remaining questions`.

Under JSON exchange this is the `report-delivery` `choice` parameter.

Choosing a subdirectory option creates the subdirectory inside the base directory.

Subsequent audits then follow the established pattern per the rules above.

Always place the file inside the audited repository or directory.

Do not write to an absolute path outside it unless the user explicitly provides one.

If the user already named a file or stated an Inline preference in the original request,
honor it without asking again.

Resolve the output directory using the rules above unless a full path was given.

If the user stated only a File preference without a path,
ask the same delivery question with `Inline` omitted and the applicable file-location and
`Custom report file` options retained.

## Previous Report Files

When a previous audit report exists (for example, `AUDIT.md`, `AUDIT-1.0.md`,
or a language-specific audit file), do not overwrite it.

Write the new report to a separate file named `<base>-<revision>.md`, for example `AUDIT-1.1.md`.

Read the `Report Revision` value from the previous report's Document Information section,
increment the minor component up to 9 (for example, `1.0` becomes `1.1`, `1.9` becomes `2.0`,
`9.9` becomes `10.0`), and write the incremented revision into the new report.

When the previous report records no revision, treat it as `1.0` and assign `1.1`.

Older reports may record the revision as a bold-label `Version` field or a `Field` / `Value` table
row, read any of these forms.

The previous report remains unchanged so that audit history stays comparable.

Full rules live in `synthesis/report-comparison.md`.

## Report Language

The default is the language of the user's request.

When the request language is ambiguous, mixed, or cannot be determined with confidence,
default to English and apply the English document style rules.

When the user explicitly specifies a different report language,
apply it without a routine follow-up question.

When the report language is not English,
load the matching `translations/` file and apply every translation, style rule,
and encoding requirement defined there.

The default filename changes to the language-specific filename defined in the translation file,
and the report must be written in UTF-8 encoding with all language-specific diacritics preserved.

Analysis runs in English regardless of the report language: evidence notes, finding drafts,
and assembled part files are written in English,
and the report is rendered into the report language in a single pass,
per `principles/output-style.md`.

## Report Style

Ask: "Which report style should the report use?"

- **`audit`** (default) - the governance contract defined across `process/report-format/`:
  per-project assurance blocks, scorecard, risk and debt registers, validation record.
- **`hunt`** - the defect-hunt genre defined in `process/report-format/hunt-style.md`:
  a verdict-first, domain-organized engineering report with `file:line` evidence, journey traces,
  breaking-change assessment, and a phase-mapped roadmap.
- **`review`** - the execution-oriented genre defined in `process/report-format/review-style.md`:
  a run register of commissioned checks with per-check status, evidence levels,
  a verdict with permitted-use gates, and a retest register.

All three styles share the same evidence rigor, finding schema,
and completeness rules - style changes presentation, never what must be found.

`check` wording selects the `review` style - the old style name remains an accepted alias.

The question ends with `Use default: audit` and `Use defaults for all remaining questions`.

Under JSON exchange this is the `report-style` `choice` parameter.

## Project Layout

When intake confirmed more than one included project, ask whether findings, observations,
and registers group across projects or describe per project - the `project-layout` `choice`
parameter under JSON exchange:

- `separate` (default) - each project gets its own complete set of sections.
- `combined` - registers group into shared tables with a `Project` column.

When the user does not choose or the run is automated, `separate` applies,
per `process/report-format/multi-project.md`.

## Evidence Mode

Use **`source-only`** by default.

Under `Configure options` this is a routine prompt - ask:
"Which evidence mode should the audit use?"

Under `Accept defaults` it is never asked and the default applies.

Apply `executed-readonly` or `executed-commands` only when the user explicitly commissions the mode
- through this prompt's answer or a statement in the request.

- ** `source-only` ** (default) - the audit executes nothing: no build, test, linter, scanner,
  or generator runs against the project, and verification steps become Further Verification entries.
- ** `executed-readonly` ** - additionally runs non-mutating, read-only analyzers the user names,
  such as dependency advisory or policy scanners (`cargo audit`, `cargo deny check`).
  The project itself is still never built, tested, or run,
  no tool is installed or upgraded for the audit,
  and every executed check is recorded in the Executed Evidence with tool, version, exact command,
  and timestamp per `process/report-format/report-closing.md`.
- ** `executed-commands` ** - additionally runs the explicitly commissioned non-mutating commands
  the user names, which may include test suites, builds, lint, typecheck, coverage runs,
  and isolated reproduction harnesses. The subject is still never deployed, mutated,
  or connected to live systems, no tool is installed or upgraded unless the user commissioned it,
  and every executed command lands in the Executed Evidence - or the Execution Register under
  `Report Style: review` - with tool, version, exact command, timestamp, exit status,
  and result per `process/report-format/report-closing.md`.
  Commissioned commands run per the procedure in `references/topics/execution-isolation.md`.

The question ends with `Use default: source-only` and `Use defaults for all remaining questions`.

When the answer is `executed-readonly` or `executed-commands`,
the audit first enumerates the subject's declared check surface per
`references/check-surface.md` - every runnable test, coverage, lint, format, typecheck,
build, packaging, advisory, and scan check the repository declares -
and the free-text follow-up presents that set as the proposed commission with the
readiness-relevant entries marked.

The user confirms the set, narrows it, or replaces it - an "all" or empty answer commissions
the proposed set, and only the commissioned set may run.

Under JSON exchange this is the `evidence-mode` `choice` parameter,
and the commission follow-up is the `commissioned-commands` `text` parameter.

## Detail Level

Ask: "What level of detail should the report include?"

- **Detailed** (default) - full report plus extended remediation steps,
  additional verification methods, deeper architectural critique, and expanded impact analysis.
- **Standard** - full report with all twenty-two baseline sections,
  subject to explicit parameter exclusions plus any conditional sections whose criteria are met,
  complete findings, risk register, scorecard, and remediation roadmap.
- **Brief** - Executive Summary, Health Dashboard (scorecard summary and risk map only),
  top risks only, and key recommendations. Detailed findings are summarized, not itemized.

The question ends with `Use default: Detailed` and `Use defaults for all remaining questions`.

Under JSON exchange this is the `detail-level` `choice` parameter.

## Evaluation Scale

Ask: "Which evaluation scale should be used for the scorecard?"

- **1-10** (default) - default scale with band definitions Poor (1-3), Average (4-6), Good
  (7-8), Excellent (9-10).
- **1-5** - compact numeric scale.
- **1-3** - minimal numeric scale.
- **Stars** - a star-bar scale whose star count is resolved by a follow-up question.

Always present all four options in this order.

The question ends with `Use default: 1-10` and `Use defaults for all remaining questions`.

Under JSON exchange this is the `evaluation-scale` `choice` parameter.

When `Stars` is selected, ask the follow-up question: "How many stars should the scale use?"

- **5 stars** (default) - uses the `1-5` rubric and displays filled and empty star
  bars, such as `★★★☆☆`.
- **3 stars** - uses the `1-3` rubric and displays filled and empty star bars, such as `★★☆`.

The follow-up ends with `Use default: 5 stars` and `Use defaults for all remaining questions` like
every routine prompt.

Under JSON exchange it is the `star-count` `choice` parameter.

The resolved scale is named `5 stars` or `3 stars` wherever the report records the scale.

## Improvement Suggestions

Use **Include with priorities** by default.

Do not ask this as a routine prompt.

Apply another option only when the user explicitly specifies it.

- **Include with priorities** (default) - full Remediation Roadmap with P1-P4 priority tiers,
  impact/effort/complexity matrix, and verification steps.
- **Brief only** - top 5 recommendations without the full matrix or verification steps.
- **None** - omit the Remediation Roadmap. Include only findings and risks.

## Trade-off Analysis

Use **Standalone and embedded** by default.

Do not ask this as a routine prompt.

Apply another option only when the user explicitly specifies it.

- **Standalone and embedded** (default) - a summary section and reasoning in relevant findings.
- **Embed into findings** - reasoning only in relevant finding blocks.
- **Omit** - do not include trade-off reasoning.

## Descriptive Mode

Use **Enabled** by default.

Do not ask this as a routine prompt.

Apply another option only when the user explicitly specifies it.

- **Enabled** (default) - the report includes a `Glossary` section that indexes every abbreviation
  and acronym used, carries longer descriptions for selected terms,
  and links every acronym occurrence in the body to its description or the index table,
  per the Glossary rules in `process/report-format.md`.
- **Disabled** - omit the `Glossary` section. Record the deliberate omission in Scope Exclusions.

## Bypass Rule

Every routine prompt ends with the named option `Use defaults for all remaining questions`.

Selecting it, or responding with "bypass", "skip", "defaults", or equivalent at any prompt,
immediately accepts all remaining defaults and proceeds to Scope Definition
(`process/audit-workflow/scope-definition.md`).

