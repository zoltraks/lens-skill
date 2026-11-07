# Audit Intake

## Purpose

> **Scope:** The intake phase of the audit workflow - input reading,
> artifact and stack classification, project identification,
> and the audit-mode decision **Key items:** deliverable classification, gates,
> project census, audit mode

This file is a phase of the audit workflow indexed by `process/audit-workflow.md`.

Follow it at the start of every audit.
Confirm completeness against the Intake Checklist in `process/audit-workflow.md`.

On completion, proceed to `process/audit-workflow/parameter-phase.md`.

## Contents

| Section                                   | Line | What it covers                            |
|-------------------------------------------|------|-------------------------------------------|
| Intake                                    | 37   | Intake                                    |
| Deliverable Classification                | 48   | Deliverable Classification                |
| Automated Run                             | 123  | Automated Run                             |
| Report Parity Discovery                   | 161  | Report Parity Discovery                   |
| Output Location Discovery                 | 174  | Output Location Discovery                 |
| Development Standards Discovery           | 207  | Development Standards Discovery           |
| Nested Repository And Working-tree Census | 232  | Nested Repository And Working-tree Census |
| Snapshot Identity                         | 271  | Snapshot Identity                         |
| External Report Discovery                 | 286  | External Report Discovery                 |
| Agent-facing Artifact Discovery           | 295  | Agent-facing Artifact Discovery           |
| Project Identification                    | 342  | Project Identification                    |
| Automation Signal Census                  | 424  | Automation Signal Census                  |
| Stack And Subject Classification          | 444  | Stack And Subject Classification          |
| Audit Mode And Previous Reports           | 491  | Audit Mode And Previous Reports           |


## Intake

Read everything the user supplied: description, code, configuration, diagrams, logs, prior reports.

Identify the artifact type: prototype, codebase under development, running production system,
or written proposal.

Note the source format.

Findings from a description are weaker than findings from inspected code or configuration.

## Deliverable Classification

Classify what the request asks to receive before anything else.

This workflow produces a report artifact and runs only when the request names one - an audit, hunt,
or review report, a defect hunt, a structure review, a scorecard, a risk register,
an assessment or readiness report, or an equivalent named deliverable.

A request that asks only to understand, explain, or describe a subject - "take a look at X",
"analyse how it is built", "describe what it brings" - names no report artifact and never
enters this workflow.

Answer it as descriptive analysis: read the subject under
`principles/evaluation-rules.md` and respond inline.

No parameter gate, intake discovery, register, scoring, output resolution,
or report file runs for such a request.

The descriptive answer stays inside the request's own scope - it never upgrades into an audit,
and it never presents an audit or a report as the implied next deliverable.

Only a request that names a report artifact, or a later message that asks for one,
enters this workflow.

Determine the report style from the request wording: `audit` by default,
`hunt` when the request asks for a defect hunt,
and `review` when the request explicitly names a review or check report - `check` remains an
accepted alias for the execution-register style.

Bare "review this codebase" wording stays `audit`.
The style is selected when the request names the report, not the activity.

A request scoped to the project structure - "make a structure review",
"review the structure" - resolves to `review` with `Review Scope: Structure` per
`process/report-format/structure-review.md`, and a request scoped to a change set - a commit range,
pull or merge request, or branch diff - produces a `review` -style report scoped to that change set.

Determine the natural language of the user's request.

The report language must match the request language unless the user explicitly states otherwise.

When the request language is ambiguous or cannot be determined, default to English.

When the report language is not English,
also look for project-established terminology in that language,
such as a project glossary or design documents written in the report language,
and record the established forms.

They take precedence over the defaults in the matching `translations/` file.

The audit itself is always performed and stored in English - evidence gathering,
partial composition, and intermediate artifacts carry English,
and the report language other than English is produced by translation of that English artifact,
never by native drafting.

When the report language is not English, also resolve the language output:
by default the run ships a file pair - the canonical English report plus its single-pass
translation, per `principles/output-style.md` - and only an explicit request scoped to a single
language ("only the Polish report") produces the translated file alone.

The same `pair` default applies when the report language is English but the discovered previous
report exists as a language pair - sibling files sharing the English stem and differing only by a
language suffix, such as `AUDIT-1.4-EN.md` with `AUDIT-1.4-PL.md`.

Preserve the convention on every mode: the new report ships its own `<stem>-EN` file plus the
translation sibling in the previous pair's second language,
including when the new report switches the style family.

An explicit single-language request overrides the convention in either direction.

The audit start timestamp is recorded later, the moment the last parameter question is resolved,
before the remaining skill rule documents are loaded.

See the timing rule under `process/audit-workflow/parameter-phase.md`.

## Automated Run

When the request asks for an automated, autonomous, unattended,
or non-interactive run - wording such as "audit automatically", "automated mode",
"do the audit automatically", "unattended",
or "without asking" - record the run as `automated` before any gate below.

An automated run asks no questions: every blocking gate and routine prompt resolves to its
discovered or default answer, and the report writes to the resolved location without a
confirmation prompt.

- The skill update check applies its merge without asking when the reported state allows it,
  and the run continues with a brief note when it does not.
- `audit-mode` resolves to re-audit against the highest-revision previous report found,
  or to a fresh audit at revision `1.0` when none exists - explicit re-audit or fresh-audit wording
  in the request still wins.
- `skills-scope` resolves to `Assess skills as components of the project`.
- `project-inclusion` resolves to the recommended set:
  recommended projects are included and not-recommended ones excluded with their reasons recorded -
  held members audit as independent projects and `unfetched` members are excluded with
  reason `not fetched`.
- `parameters-acceptance` resolves to accept - recovered parameters on a re-audit,
  defaults otherwise - and `parameters-to-change` keeps every recovered value.
- `report-style` resolves to a style named in the request,
  then the recovered previous style on re-audit, then the `audit` default.
- `language-output` resolves to the recovered pair when a previous report shipped one,
  then to the `pair` / `single` default the rules above produce.
- `project-layout` resolves to `separate`.
- `report-delivery`, `review-scope`, `detail-level`, `evaluation-scale`,
  and `star-count` resolve to the defaults `process/audit-workflow/parameter-phase.md` produces.
- Thin-input clarifications are not asked - missing inputs record `Unknown` or
  `Not specified` instead.

Explicit parameter statements in the request win over every automated resolution.

Every automated resolution is recorded exactly like an answered question - the same working notes,
the same `work/lens-params.json`, and the same completion-message disclosure.

## Report Parity Discovery

When searching for a previous report during intake,
also record the most recent audit report found for ANY subject in the searched locations,
with its path and revision.

When the located report carries a language suffix - `<stem>-<LANG>` such as `-EN` or `-PL` - also
check for sibling files sharing the stem,
and record whether the previous report was produced as a language pair and in which second language.

The consistency gate in `process/report-parity.md` diffs the new report's capability set against it
before the report is marked final.

## Output Location Discovery

During intake, inspect the documentation roots `docs/`, `document/`, and `doc/` and their `audit/`,
`report/`, and review-family (`review/`, `reviews/`) subdirectories.

Record the resolved base output directory, the detected subdirectory pattern,
the project version used, and the resolved output directory.

When the resolved base is a `report/` directory that contains a subdirectory matching the report
style - `audit/` for the `audit` or `hunt` style,
`review/` for the `review` style - descend into that subdirectory and record it as the base,
so a `docs/report/audit/` landing zone wins over the bare `docs/report/` for an
`audit` -style report.

A dedicated `review/` or `reviews/` directory under a documentation root is the review-purpose base
for a `review` -style report, and its date-named subdirectories record the `date-named` pattern for
the subdirectory grouping.

Classify the subdirectory names inside the resolved base output directory:

- `version-numbered` - names matching `\d+\.\d+(\.\d+)?` with an optional `v` prefix,
  such as `1.0.1` or `v2.3.1`.
- `date-named` - names in ISO `YYYY-MM-DD` format, such as `2026-09-21`.
- `mixed` - both kinds are present. Follow the pattern of the subdirectory holding the most recent
  audit report by `Report Date` or `Report Revision`,
  or the pattern with more entries when neither holds a report, and disclose the choice.
- `none` - no matching subdirectories.

The recorded result is consumed unchanged by the delivery question and re-checked before
the report is written.

When the user named a full output path in the request, detection still runs but the named path wins.

## Development Standards Discovery

During intake, look for project-internal development standards documents.

These are documents that prescribe how source code should be written for the project's technology
stack: language version, project structure, naming conventions, error handling, testing, formatting,
dependency management, and similar rules.

Search in these locations, in order:

- `docs/standard/` and any file inside it, such as `docs/standard/go-development.md`
- `docs/standards/`
- `docs/guidelines/`
- `STANDARDS.md` at the repository root
- Any file referenced from `README.md`, `AGENTS.md`,
  or `docs/GUIDELINES.md` as a development standard

Record whether standards documents exist, their paths,
and which technology stack or software type each one covers.

This determines whether the Standards Conformance assessment applies.

When no standards documents are found, the Standards Conformance assessment is omitted and the
omission is noted in Scope Exclusions.

## Nested Repository And Working-tree Census

During intake, detect nested repositories: directories carrying their own `.git`,
including submodules, vendored checkouts, and embedded clones.

Each nested repository has its own history and is a project-boundary signal.

Record each with its path and its classification: submodule per `.gitmodules`,
vendored dependency per manifest or ignore rules, or an unclassified embedded repository.

For a submodule, also record its fetch state: `fetched` when its working tree carries content,
`unfetched` when the directory is empty or `git submodule status` marks it with a `-` prefix.

Record the pin state: a `+` prefix on `git submodule status` means the checkout sits at a non-pinned
commit, no prefix means it sits at the recorded pin.

Vendored and installed trees are `not recommended` for inclusion per the
project-inclusion rules below.

Submodule and embedded members of the audited location are `recommended` project candidates.

They audit at their checked-out commit, with the pinned-versus-checkout delta recorded
under Snapshot identity.

An `unfetched` member stays recorded as a held member:
it is excluded from the inclusion default with reason `not fetched`,
disclosed in Scope Exclusions with the init hint,
and never silently dropped from the census or the Skills Inventory.

Census manifests and lockfiles in the working tree, not only tracked paths.

An untracked manifest or lockfile means dependency evidence differs from the committed state.

Record untracked manifests separately and never count them in the tracked inventory,
per the tracked-artifact rules under Evidence Gathering.

Prior-audit discovery stays bounded: search only the locations named under Audit mode and previous
reports, and never descend into dependency, vendor, or nested-repository trees to find reports.

## Snapshot Identity

During intake, record the audited tree's identity so every claim can be anchored:

- For each audited repository root, record `git rev-parse HEAD`,
  the current branch or detached state, and `git status --porcelain` to classify the
  tree as clean or dirty.
- For a submodule member, additionally record the pinned commit and whether the checkout sits at the
  pin or ahead of it, so member claims bind to the audited state, not the pin.
- A dirty tree lists its dirty paths in the evidence ledger, not in Document Information.
- When no VCS metadata exists, record `unversioned working tree` plus the capture timestamp.

These values render in Document Information per `process/report-format/report-opening.md`,
and every claim in the report binds to this snapshot.

## External Report Discovery

During intake, look for audit or assessment reports of the same subject produced outside this
workflow, in the documentation roots and the repository root.

Each external report is triangulation input per `synthesis/report-triangulation.md`:
contradictory claims become Contradiction Register rows resolved against the declared snapshot,
never adopted truth and never dismissed.

## Agent-facing Artifact Discovery

During intake, enumerate every agent-facing artifact inside the audited root:
`SKILL.md` at the root, under `skills/` and `plugins/` one level down,
under agent configuration directories (`.claude/skills/`, `.agents/skills/`, `.devin/skills/`,
`.cursor/skills/`, `.windsurf/skills/`, `.codeium/skills/`),
and any other `*/SKILL.md` found one level deep, plus `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
rules directories (`.cursor/rules/`, `.windsurf/rules/`, `.devin/rules/`, `.claude/rules/`),
deprecated flat files (`.cursorrules`, `.windsurfrules`, `CLAUDE.local.md`),
`.claude/agents/` definitions, `.claude-plugin/` manifests, `.github/copilot-instructions.md`,
`.github/instructions/`, and MCP server configuration such as `.mcp.json`.

For each skill directory found, record its path, its declared `name`,
whether the name matches the directory name, and its provenance classification: `authored`,
`installed`, `external member`, or `undetermined`,
per the signal table in `assessment/skill-definition.md`.

Skills inside dependency or vendor directories, referenced by install or marketplace manifests,
or documented as third-party are `installed`, not audit subjects by default.

For each non-skill artifact, record its path, format, and scope.

How discovered authored skills enter the report depends on the subject shape:

- The subject IS a skill (root `SKILL.md` and nothing else)
  - run Skill Definition Conformance directly against it, no inventory needed.
- The subject IS a collection (multiple `SKILL.md` under skill directories and no dominant product
  project) - each fetched member skill joins the project list as an independent project per Project
  Identification, and the Skills Inventory matrix plus the collection-level checks render inside the
  collection-root project's Skill Definition Conformance section,
  with member rows linking to the member's own project block.
  An `unfetched` member is listed in the matrix marked `Out of scope - not fetched`.
- A non-skill project CONTAINS authored skills - ask the skills-scope question before Parameter
  Configuration: `Assess skills as components of the project` (recommended)
  produces the Skills Inventory inside Skill Definition Conformance.
  `Assess each skill as an independent project` routes each skill through the multi-project
  workflow. Wait for the answer, record it, and do not re-ask in the session.
  Under an automated run the recommended component option applies without asking.
  Under JSON exchange this is the `skills-scope` `choice` parameter per `process/json-exchange.md`.

Installed skills bypass the skills-scope question entirely.

The discovery result decides whether Skill Definition Conformance applies and which
shape the section takes.

When nothing is found, the section is omitted and the omission is noted in Scope Exclusions.

## Project Identification

After reading the input, identify whether the repository or directory contains one project
or multiple projects.

A project is a self-contained unit with its own manifest, configuration, or entry point.

The audited root is itself a project only when it carries project signals of its own: a manifest,
a `SKILL.md`, an entry point, or a dedicated configuration directory.

A root that carries none of these is a pure container - the audit subject is the location,
Document Information names the location, and the held projects below are the only projects.

Signals of a project boundary include a package manifest (`package.json`, `Cargo.toml`,
`composer.json`, `go.mod`, `pom.xml`, `*.csproj`), a dedicated configuration directory,
a `SKILL.md` file (for an Agent Skill), or a clearly separated component with its own
build and entry point.

A `SKILL.md` found under an agent-skill location is not automatically a separate project.

The skills-scope decision made during agent-facing artifact discovery routes it:
as a component it is inventoried inside the parent project's Skill Definition Conformance section,
as an independent project it joins the multi-project list in `process/audit-workflow.md`.

A member skill directory of a collection subject is always a separate project:
fetched members join the project list as `recommended` independent projects at their checked-out
state, unfetched members stay excluded with reason `not fetched` per the nested-repository census,
and the skills-scope question is not asked.

When multiple project manifests or boundaries exist at the top level or in clearly separated
subdirectories, treat each as an independent project.

Record the list of identified projects with their paths, their provenance (`in-tree`, `submodule`,
or `embedded`), and, if determinable, their version numbers,
marking each project `recommended` or `not recommended` for inclusion:
a directory classified `installed` during agent-facing artifact discovery,
any dependency/vendor path, or an `unfetched` member is `not recommended`,
and everything else defaults to `recommended`.

When only one project is present, proceed with the standard single-project workflow without asking.

When multiple projects are present, ask the project-inclusion question before
Parameter Configuration.

**Gate** - `project-inclusion`: a blocking decision gate per `process/decision-modes.md`,
presenting a checkbox-style multi-select list of every identified project with its path and kind.

The gate is multi-select by definition.
Every listed project must be selectable at once,
so an all-inclusive answer is a first-class outcome, never an `Other` escape.

When the question tooling exposes a multi-select or checkbox mode,
use it for this gate rather than a single-choice list that forces an either/or answer.

Recommended projects are checked by default and not-recommended ones are listed unchecked with their
reason, such as `installed/external`.

Usually all projects belong in the audit, so the question exists to focus or exclude,
not to confirm the obvious.

Wait for the answer, record the included and excluded lists with reasons,
and do not re-ask in the session.

Under an automated run the recommended set applies without asking,
so the cancel-confirmation surface never arises.

Under JSON exchange this is the `project-inclusion` `selection` parameter per
`process/json-exchange.md`, with recommended projects in `default`.

An answer that unchecks every project asks the user to confirm cancelling the audit rather than
producing an empty report - the `cancel-confirmation` `choice` parameter under exchange.

Excluded projects are disclosed once in Scope Exclusions with their reason,
and excluded skill directories still appear in the Skills Inventory marked `Out of scope`.

The included projects then run independently through the audit.

Each project receives its own complete assessment, findings, scorecard,
and risk register within a single combined report.

See the Multi-Project Audits section of `process/audit-workflow.md` for the per-project workflow.

## Automation Signal Census

For each identified project, enumerate the signals that delivery automation exists or was envisaged:
pipeline files and workflow directories, CI configuration files (`*.gitlab-ci.yml`, `.circleci/`,
`Jenkinsfile`, `azure-pipelines.yml`), badges, pull request templates,
or branch rules that reference automated checks, documented pipelines or release procedures,
and build, deploy, or release scripts.

Record the outcome per project as one of three tokens:

- `signals` - automation configuration or envisaged-automation signals exist in the tree.
- `external` - repository evidence points at automation living outside the audited tree,
  such as documentation or badges naming an external pipeline - recorded as `Reported` evidence,
  not as an absent capability.
- `none` - the tree carries no signal that automation was ever envisaged.

The census feeds the criteria-planning applicability decision and the reduced-depth rule in
`assessment/deployment-review.md`, and `assessment/testing-review.md` consumes the same outcome for
its CI-automation judgement.

## Stack And Subject Classification

For each identified project, detect the language and ecosystem from manifest and file signals:
`Cargo.toml` for Rust, `*.csproj` or `*.sln` for .NET, `go.mod` for Go, `package.json` for Node,
`pom.xml` or `build.gradle` for JVM stacks, `pyproject.toml` for Python, and so on.

Record the detected stacks and consult `references/stack-standards.md` for the canonical references
to apply during assessment and cite in the report.

Baseline consultation order for every conformance judgement:

1. The subject's own development standards documents, when found during intake.
2. The bundled corpus digests under `references/stacks/`, `references/methodology/`,
   `references/topics/`, and the flat `references/` files,
   mapped through `references/source-catalog.md`.
3. The live authoritative URL named by the digest,
   only when the two earlier sources leave the question open and fetching is permitted.

Record which baseline decided each judgement,
and record the digest's snapshot date when a corpus file supplied it.

For every project, also record the governing layout and naming baseline the Structure Review
verdicts rest on: the detected stack or stacks,
the application nature assigned under Domain profile,
and the consulted baseline - the subject's own standards,
a bundled digest or the component-role rules in `references/naming-and-layout.md`,
or the fallback rung used when no digest covers the stack.

This record feeds the Auditing Methodology reference-standards step and the PAR-20 justification in
`process/report-parity.md`.

The selected stack and nature together decide which purpose-baseline digests under
`references/topics/` apply (CLI contract, MCP server, UI automation, performance budgets,
inline scripting, data persistence) - apply a purpose digest only when its applicability signals
fire, never as a universal checklist.

These rows feed the conditional Engineering Baseline Conformance section per
`assessment/baseline-conformance.md`.

Classify each project as a reusable library or package versus a deployable service or application.

Signals of a library subject include a package manifest with a published name and version
(`*.nuspec`, a `Cargo.toml` or `package.json` naming a published artifact),
library guidance in documentation, or consumption by other projects.

This classification controls the API Compatibility And Versioning Discipline conditional assessment.

## Audit Mode And Previous Reports

When the user asks to rerun, regenerate, or update an audit report,
or the audited location already contains an audit report,
first check whether a previous report exists.

Search the location indicated in the request,
the resolved output directory and its versioned or dated subdirectories,
the default locations (`audit/` and `report/` directories and the bare root under `docs/`,
`document/`, and `doc/`, then the repository root), and the rest of the document structure,
per `synthesis/report-comparison.md`.

Inside a `report/` directory, also search its `audit/` subdirectory when the report style is `audit`
or `hunt`, or its `review/` subdirectory when the report style is `review`.

For a `review` -style report, also search dedicated `review/` and `reviews/` directories under the
documentation roots, including their dated subdirectories.

A previous report may be named `AUDIT.md`, `AUDIT-<revision>.md`, or the language-specific filename.

For a `hunt` report style the same rules apply to the hunt filename family: `HUNT.md`,
`HUNT-<revision>.md`, and the language-specific stem such as `POLOWANIE-<revision>.md`.

For a `review` report style the family is `REVIEW.md`, `REVIEW-<revision>.md`,
and the language-specific stem such as `PRZEGLĄD-<revision>.md`.

A `review` -family file serves as a baseline only when it carries `Report Style: review` and the
same `Review Scope` value - a structure-variant report baselines a structure-variant report,
and a full-scope review baselines a full-scope review.

A `REVIEW` -family file carrying a custom suffix is treated as a custom report and still appears as
a baseline candidate.

A `REVIEW` -family file without the `Report Style` row is a legacy shape and never serves as a
baseline, though its name still occupies the revision slot.

A legacy `CHECK` -family file is never identified as a previous `review` -style report and never
serves as a baseline.

A report never baselines a report of another style - an `audit` report never baselines a `review`
report, a `review` report never baselines an `audit` or `hunt` report, and so on.

When several exist, present the one with the highest revision as the candidate baseline.

The audit mode is a user decision, never an assumption from the file system.

When a previous report exists and the mode is not yet confirmed,
ask the audit-mode question and wait for the answer before Parameter Configuration,
because the answer decides whether parameters are recovered or asked.

**Gate** - `audit-mode`: a blocking decision gate per `process/decision-modes.md`:
it presents concrete options with one marked `(recommended)` and never carries the `Use default`
trailing options of routine prompts.

Under an automated run the gate is not asked and the mode resolves per the Automated run block above
- the confirmed-re-audit recovery below then applies as if the user had confirmed.

Under JSON exchange it emits as the `audit-mode` `choice` parameter per `process/json-exchange.md`.

- No audit mode was stated and a previous report was found: present the candidate file's path,
  revision, and report date, and ask which audit mode to run. Options:
  `Re-audit - compare against <filename>`,
  `Re-audit with changed parameters - compare but reconfigure`, and
  `Fresh audit - ignore the previous report's content`.
- The user asked for a re-audit and a previous report was found:
  confirm the baseline even when the found file looks correct. Present its path, revision,
  and report date and ask the user to confirm it is the intended baseline. Options:
  `Confirm - re-audit against <filename>`, `Re-audit with changed parameters`,
  and `Fresh audit instead`, plus any other answer the user gives.
- The user asked for a re-audit and no previous report was found: say so,
  naming the searched locations, and ask whether to proceed as a fresh audit at revision `1.0`.
  The user may also supply the report path in another answer.
- The user asked for a fresh audit: honor it without asking,
  whether or not a previous report exists.

Mark `(recommended)` on the re-audit option when the found report appears to cover the same subject,
for example a matching system name or a file inside the subject's designated report directory,
and on the fresh-audit option when it appears to cover a different subject.

When unsure, recommend re-audit so history stays comparable.

Mark the changed-parameters option recommended instead only when the user's request already signals
a parameter change, for example "re-audit at a different scale".

On a confirmed re-audit, recover the previous report's detail level, scale, language, filename,
report style, Descriptive mode, and language output.

Recover Descriptive mode from the previous report's Document Information row when present,
otherwise from the presence or absence of its Glossary section.

Recover the language output from the sibling files themselves - `<stem>-<LANG>` files such as
`AUDIT-1.4-EN.md` plus `AUDIT-1.4-PL.md` mean the previous run shipped a `pair`.

The recovered language output is proposed on every mode that exists alongside a discovered pair -
re-audit, fresh audit, and style-family switch alike - and the pair survives the switch:
a `HUNT` pair followed by an `audit` -style report ships `AUDIT-<revision>-EN.md` plus the
same second language.
Name the resolved set in the parameter summary, or in the decisions list on an automated run.

A report style named in the request always wins over the recovered style - a request for a general
audit report proposes `audit` even when the previous report was a `hunt` or `review`.
The recovered style remains listed as a non-default alternative in the parameter summary,
and a style switch starts the new family's revision track.
An unnamed style falls back to the recovered value.

Reuse the recovered parameters unless the user asks to change them,
then proceed to Scope Definition without repeating answered questions.

On `Re-audit with changed parameters`, the audit keeps comparison semantics - identifier continuity,
the Changes Since Previous Audit section,
and the incremented revision - while any core parameter may change.

Recover the previous report's parameters as defaults, present them in a compact summary,
and ask one follow-up question listing the core parameters:

`Which parameters should change?` The user names the parameters to reconfigure - the
`parameters-to-change` `selection` parameter under JSON exchange.

Run the parameter prompts only for the named parameters,
marking the recovered value `(previous, default)` on each option.

Parameters not named keep their recovered values.

Record every parameter that differs from the previous report in the Changes Since Previous Audit
field table and classify deltas the change produces as capability changes per
`synthesis/report-comparison.md`, never as product changes.

Record any missing parameters using defaults and disclose them,
rather than claiming they were specified in the prior report.

On a fresh audit the previous report's content is ignored: no parameters are recovered,
the full Parameter Configuration phase (`process/audit-workflow/parameter-phase.md`) runs,
and no `FND-XXX`, `RSK-XXX`, or `REC-XXX` identifiers carry over.

The report revision still increments from the highest revision found,
the previous file is never overwritten, and the new report omits the Changes Since Previous Audit
section and the `Previous Report` row.

The cross-subject parity baseline in `process/report-parity.md` still applies.

On a confirmed re-audit, do not reuse old execution permissions, tool results,
or readiness conclusions as current evidence.

The previous report is never overwritten.

On confirmation, record the previous report's checksum - or byte size and line count when hashing is
unavailable - in working notes as the baseline-integrity record.

The new report is written to a new revision-numbered file and carries a Changes Since Previous Audit
section, per `synthesis/report-comparison.md` and `process/report-format/summary-changes.md`.

If no previous report is found and the conversation context contains no record of previously chosen
parameters, treat the request as a new audit and run the full Parameter Configuration phase in
`process/audit-workflow/parameter-phase.md`.

