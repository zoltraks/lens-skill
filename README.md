# Lens - Software Audit And Review Skill

```
 /\_/\
( o.o )
 > ^ <
```

> Evidence-based engineering audits of any software subject - prototypes, codebases under
> development, and already-running production systems - plus explicit review reports with
> amendment instructions.
>
> [Versioning Policy](./docs/VERSIONING.md)
>
> [Agent Skills Specification](https://agentskills.io/specification)

## Contents

| Section                            | Line | What it covers                                      |
|------------------------------------|------|-----------------------------------------------------|
| Overview                           | 38   | Audit purpose and standard report shape             |
| What The Skill Does                | 81   | Update check, evidence, assessment, synthesis       |
| Installation                       | 159  | Clone and update instructions                       |
| Usage                              | 189  | Activation, parameters, and report delivery         |
| Example Prompts                    | 220  | Full and focused audit requests                     |
| Workflow Diagrams                  | 286  | ASCII and Mermaid audit pipelines                   |
| Evidence And Decision Quality      | 346  | Evidence strength and verification limits           |
| Core Principles                    | 403  | Evaluation constraints and status rules             |
| Report Format                      | 419  | Report structure, identifiers, and style            |
| When To Use This Skill             | 454  | Supported requests and exclusions                   |
| What's Inside                      | 477  | Documents, references, tools, and conditional files |
| Document Style                     | 613  | Pointer to the style rules file                     |
| Specification                      | 623  | Agent Skills specification conformance              |
| Verification For Skill Maintenance | 644  | Maintenance checks and regression scenarios         |
| License                            | 670  | License for the skill itself                        |
| Credits                            | 676  | Authorship and attribution                          |

## Overview

Lens is a structured audit process packaged as an agent skill.

It guides an AI coding agent through a complete engineering assessment of any software subject - a
prototype, codebase under development, production system, or technical proposal - producing a
neutral, repeatable report anchored to concrete facts rather than impressions.

Unlike a generic "review my code" prompt, Lens enforces a fixed workflow: intake, parameter
configuration, scope definition, evidence gathering, per-category assessment, synthesis, and
validation.

The intake, evidence gathering, and assessment pipeline is shared by both report types;
only the synthesis stage and the validation contract differ.

The default output is an Audit report with twenty-one baseline sections: Document Information, the
Audit Type Coverage table, Executive Summary, System Context (including the technology
stack), a source-derived Software Bill of Materials, License Compliance Review, Health
Dashboard, Delivery Practice & Team Continuity, High-Level Observations, Auditing Methodology,
Scoring Rubrics, Architectural Assessment, Trade-off Analysis, Strengths & What's Working, Detailed
Technical Findings with theoretical exploitability narratives on serious security findings, Unified
Risk Register, Actionable Remediation Roadmap, Scope Exclusions, Limitations and Unknowns,
Validation Record, and References.

Conditional sections appear only when the subject warrants them: Data Flow Diagram, Design
Patterns, Architecture Decision Records, Threat Model, API Contract Conformance, Skill Definition
Conformance, AI System Assessment, Standards Conformance, API Compatibility & Versioning Discipline,
Technical Debt Register, Changes Since Previous Audit, and Re-audit Plan.

At Standard and Detailed detail levels the roadmap is followed by a Recommendation Classification
section that assigns every recommendation a `Recommended`, `Optional`, or `Not recommended` class,
so the report can serve directly as a basis for change documents.

Every section uses a hybrid table-paragraph format for scannable summaries backed by detailed
evidence.

An explicit request for a review report, a set of corrections, or an improvement plan produces a
Review report instead: the same evidence discipline in a compact findings-and-corrections layout
with required changes, a suggested amendment order, and a public source register, defined in
`process/review-report.md`.

---

## What The Skill Does

When you ask for an audit, the agent loads the skill and performs the following:

**Checks for updates**

Once per session, the agent runs a git self-update check on the skill's own repository and offers
to pull incoming commits before starting, when the skill lives in a git clone.

**Reads everything you supplied**

Code, configuration, documentation, logs, and prior reports.

It identifies the artifact type (prototype, codebase, production system, or proposal)
and records the source format.

**Configures parameters**

Asks whether to accept default parameters or configure the core report parameters.

Detail level defaults to `Detailed`, improvement suggestions default to a prioritized roadmap,
trade-off analysis defaults to a standalone section with embedded reasoning,
and descriptive mode defaults to enabled,
adding a `Glossary` section that indexes every abbreviation used, describes selected terms in depth,
and is linked from every acronym occurrence in the report.

Advanced parameters can still be changed when explicitly specified.

When the request asks for machine-readable parameters, every pending intake question emits as a
JSON parameter document per `process/json-exchange.md`; under a diagnostic or verbose request the
document is emitted for information first, then the question menus still run.

**Defines scope explicitly**

Lists what is in scope and what is excluded.

When several projects are found, intake asks a confirmation question listing every project,
with authored work checked by default and externally installed directories such as vendored
skills listed unchecked.

Marks unstated constraints as `NOT SPECIFIED` rather than assuming industry norms.

**Gathers evidence before judging**

Collects concrete anchors - file paths, config keys, documented commands,
pipeline steps - before forming conclusions.

Separates collection from judgment to avoid confirmation bias.

The analysis never builds, tests, or executes the project.

**Assesses across 18 categories**

Testing, design principles, code quality, stack best practices, dependencies, deployment, rollback,
maintainability, change management, documentation, non-functional requirements, security,
compliance, observability, error handling, operational readiness,
AI-generated code detection and provenance, and copyrights and originality.

Each category receives one of five statuses: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or `N/A`.

A conditional seventh pillar, API Compatibility & Versioning Discipline,
applies when the subject is a reusable library or package.

**Synthesizes findings**

Builds a unified risk register with bidirectional cross-referencing to findings,
a 1-10 scorecard from category findings,
and an actionable remediation roadmap with prioritized impact-vs-effort tracking.

Optional scales are `1-5`, `1-3`, `5 stars`, and `3 stars`.

**Produces a validated report**

Re-checks every finding against the evaluation rules: no assumptions, no personal judgment, no
emotional language, every claim anchored to a concrete fact.

---

## Installation

Lens is a filesystem-based [Agent Skill](https://agentskills.io/specification).

Clone the repository and place the `lens-skill/` directory in your agent's configured skills
directory:

```bash
git clone https://github.com/zoltraks/lens-skill.git
```

### Updating

Once per session, Lens checks its own Git upstream.

If an update is available, it asks whether to pull or skip.

It pulls only when the repository is clean and a fast-forward is possible.

The check also reports `tip_sha` and `tip_date` for the incoming upstream tip, so the new
state can be reviewed and pinned to a specific commit before pulling.

To update the clone manually:

```bash
git -C <skills-dir>/lens-skill pull --ff-only
```

---

## Usage

Lens activates when you request a software audit, architecture audit, prototype review, production
code audit, technical due diligence, readiness assessment, risk register, scorecard, or remediation
roadmap.

Name the software subject and the audit or assessment you want, such as an architecture audit,
production-readiness assessment, dependency review, or technical due diligence.

Audit remains the default report type.

An explicit request to review a document or subject and produce corrections, amendments, or an
improvement plan selects the Review report type, which supports any subject.

Before a new audit, Lens asks whether to accept the default parameters or configure the core report
settings.

A confirmed re-audit reuses the prior report's recorded parameters unless you request changes.

The report can be returned inline or written to a file, according to the resolved output location
and your choice.

Lens assesses software.

It does not implement changes.

The audit inspects repository contents and does not build, test, scan, or execute the audited
project.

---

## Example Prompts

**Full audit**
> Audit this production codebase. Produce a full engineering assessment with a unified risk
> register, scorecard, and actionable remediation roadmap.

**Audit to a file**
> Perform lens on this service and write the audit report to AUDIT.md. (The agent will accept
> the filename and ask whether to accept other defaults or configure core parameters.)

**Audit without a named file**
> Make audit report on this codebase. (The agent will ask whether to accept default parameters or
> configure core parameters, then offer inline, concrete file-location, and custom-file choices.)

**Readiness assessment**
> Is this system production-ready? Assess testing, deployment, rollback, observability, and
> operational readiness, and state the maturity level with evidence.

**Single dimension**
> Review only the security posture of this codebase. Mark anything you cannot determine from the
> provided files.

**SOLID and testability**
> Assess this codebase against SOLID principles and its testing strategy: test pyramid balance, TDD
> signals, and how testable the code is.

**Stack best practices**
> Review whether this code follows the idiomatic best practices of its stack: language idioms,
> framework conventions, ecosystem layout, and any deprecated APIs.

**Dependency and supply-chain audit**
> Audit the dependencies of this project: flag outdated and vulnerable packages, license
> compatibility, and whether builds are locked and reproducible.

**Risk register**
> Build a risk register for this architecture proposal. Use Low / Medium / High / Critical
> severities and tie each risk to evidence.

**Architectural trade-off**
> Evaluate the trade-off between keeping in-memory state versus introducing an external store for
> this prototype, given a single-instance target. Include a standalone trade-off table and embed the
> analysis into the relevant architectural finding.

**Re-audit**
> Re-run the audit on this codebase after the latest fixes. (The agent finds the previous report
> and asks you to choose a mode: re-audit against it, re-audit with changed parameters, or a
> fresh audit that ignores its content. It then writes a new revision-numbered file such as
> `AUDIT-1.1.md` without overwriting it and adds a Changes Since Previous Audit section on
> either re-audit mode.)

**Thin input**
> Here is a one-paragraph description of a service. Audit what you can and list exactly what
> additional artifacts would raise confidence.

**Skill definition audit**
> Audit this Agent Skill for spec conformance. Check the SKILL.md frontmatter against the Agent
> Skills specification, verify all file references resolve, and assess whether the description
> triggers correctly.

**Review report**
> Review PREPARATION.md and produce amendment instructions. (The agent writes a Review report -
> findings and corrections, required changes, a suggested amendment order, and a public source
> register - to `REVIEW-1.0.md` unless you name a different file.)

---

## Workflow Diagrams

The diagrams show the audit pipeline from the session update check through report delivery.

The audit uses inspected repository contents as evidence and never executes the audited project.

### ASCII Workflow

```
User request
    |
    v
Once-per-session update check
    |
    v
Intake: classify report type, subject, boundaries, and prior reports
    |
    v
Resolve prior-report mode or baseline when applicable
    |
    v
Configure parameters or reuse confirmed re-audit settings
    |
    v
Define scope
    |
    v
Gather source-only evidence
    |
    v
Assess applicable categories
    |
    v
Synthesize findings, risks, scorecard, and roadmap
    |
    v
Run report parity and validation checks
    |
    v
Deliver inline or to a file
```

### Mermaid Workflow

```mermaid
flowchart TD
    A[User request] --> B[Once-per-session update check]
    B --> C[Intake: classify report type, subject, boundaries, and prior reports]
    C --> D[Resolve prior-report mode or baseline when applicable]
    D --> E[Configure parameters or reuse confirmed re-audit settings]
    E --> F[Define scope]
    F --> G[Gather source-only evidence]
    G --> H[Assess applicable categories]
    H --> I[Synthesize findings, risks, scorecard, and roadmap]
    I --> J[Run report parity and validation checks]
    J --> K[Deliver inline or to a file]
```

---

## Evidence And Decision Quality

Lens separates inspected source, executed checks, reported claims, and inference.

Every audit records a verification plan and evidence ledger with revision, documented command or
source, declared tool or report version, recorded result when one exists in the repository,
artifact, and limitations, including checks that were not run.

The audit inspects repository contents only.

It never builds, tests, or executes the project, and tool availability is not assumed.
Documented or committed check results count as reported evidence, not verification.

Serious findings receive a counter-check for reachability, existing guards, and alternative
explanations before they reach the executive summary.

Security findings use justified CWE mappings and CVSS vectors where applicable,
while engineering and business risks retain the Lens risk matrix.

Each CWE-classified finding also names the equivalent static-analyzer rule for the detected stack,
per `references/cwe-analyzer.md`, so follow-up verification is concrete.

Audits select canonical, stack-specific references from `references/stack-standards.md` rather than
relying on generic standards alone.

Dependency manifests and lockfiles yield a source-derived component inventory per
`references/dependency-manifests.md`, with no tool execution.

Every overall score is reported with its lowest-scoring dimension in a paragraph below the table,
and every material piece of collected evidence must surface in the report.

The guides cover how to assess documented or committed evidence for baseline checks, coverage,
mutation and fuzz testing, unsafe-use statistics, dependency advisories, SBOMs, and license
policies across stacks.

A clean scan is not proof of security, and a source-only audit is not runtime verification.

The quality crosswalk uses ISO/IEC 25010:2023 without claiming ISO certification.

ASVS 5.0.0, OWASP Top 10:2025, API Top 10:2023, and RFC 9457 are applied only where relevant,
with versions and coverage recorded and publication status checked at audit time.

Technical due diligence includes support continuity, operating costs, roadmap feasibility, supplier
risk, IP rights, and data lifecycle evidence through the existing categories.

Missing business inputs remain visible rather than being filled with invented budgets or owners.

Operational reviews distinguish SLO targets from measured results and use the current five-metric
DORA model when production delivery data is available.

Remediation costs use supported ranges and disclose unestimated work, common work is counted once.

Unknown authorship stays unknown, tidy code and uniform tests are not AI-origin evidence.

Production sign-off remains pending when required verification or confirmed ownership is missing,
even when the scoped report is final.

## Core Principles

Every audit follows these non-negotiable rules:

- **Evidence only** - findings trace to a concrete fact: a file, a config value, a command, a log
  line.
- **No assumptions** - missing information is marked `UNKNOWN`, `NOT SPECIFIED`, or
  `INSUFFICIENT INFORMATION`.
- **No personal judgement** - the report evaluates the system, never the people who built it.
- **Architectural neutrality** - choices are judged within stated constraints, not against a favored
  stack.
- **Contextual applicability** - categories that cannot apply to the deployment model are marked
  `N/A` with justification, not treated as failures.

---

## Report Format

Audit and Review reports share a hybrid table-paragraph format throughout:

- **Tables** provide scannable summaries with one to three words per cell.
- **Paragraphs** below each table provide detailed evidence, file paths, and reasoning.
- **Finding IDs** are shown as `FND-[PILLAR]-[001]` in the detailed findings section.
- **Risk IDs** are shown as `RSK-[001]` and cross-referenced to source findings.
- **Recommendation IDs** are shown as `REC-[001]` and traced to specific findings.
- **Scores** use `Score: 7/10` for the default scale, `Score: X/5` or `Score: X/3` for
  alternate numeric scales, and a star bar for star scales.

  ```
  Score: ★★★★☆
  Score: ★★☆
  ```

- **Severities** are shown as `SEVERITY: CRITICAL` inline after the finding title. Severity,
  status, and result-marker tokens localize per the report language's `translations/` file.
- **High-Level Observations** provide a fast-skim path for non-technical readers.
- **Strengths & What's Working** balances the tone with 5-8 acknowledged positives.
- **Trade-off Analysis** surfaces architectural tensions in a dedicated table.
- **Document style** - generated reports follow the same Markdown rules as the skill's documents:
  `#`/`##`/`###` headings only, one-sentence paragraphs, prose wrapping at a selectable width
  (default 100), and tables aligned by a temporary formatting script.

This format keeps the report readable in plain-text consoles while preserving depth.

Audit reports follow `process/report-format.md` and carry `AUDIT-<revision>.md` filenames.

Review reports follow the compact findings-and-corrections contract in
`process/review-report.md` and carry `REVIEW-<revision>.md` filenames.

---

## When To Use This Skill

| Situation                                        | Use this skill?                                     |
|--------------------------------------------------|-----------------------------------------------------|
| "Audit the architecture of this system"          | **Yes**                                             |
| "Audit this production codebase"                 | **Yes**                                             |
| "Review this prototype for production readiness" | **Yes**                                             |
| "Do technical due diligence on this codebase"    | **Yes**                                             |
| "Audit our dependencies and supply chain"        | **Yes** - use `assessment/dependency-review.md`     |
| "Build me a risk register and scorecard"         | **Yes**                                             |
| "Review only the security posture"               | **Yes** - single-dimension audit                    |
| "Check if this code is idiomatic for its stack"  | **Yes** - use `assessment/best-practices.md`        |
| "Audit this skill for spec conformance"          | **Yes** - use `assessment/skill-definition.md`      |
| "Audit our skills collection"                    | **Yes** - per-skill conformance matrix              |
| "Check conformance with our dev standards"       | **Yes** - use `assessment/standards-conformance.md` |
| "Compare these two architectural options"        | **Yes** - embed trade-offs into relevant findings   |
| "Review this document and list required changes" | **Yes** - Review report type                        |
| "Prepare an improvement plan for this guide"     | **Yes** - Review report type                        |
| "Write the feature for me"                       | No - this skill assesses, it does not build         |
| "Tell me which team member caused this"          | No - this skill never evaluates people              |

---

## What's Inside

```
lens-skill/
├── SKILL.md                               # Root router - load this first
├── AGENTS.md                              # Agent-facing entry point for repository authoring
├── docs/
│   ├── README.md                          # Index of the repository-governance documents
│   ├── STYLE.md                           # Document style rules for all files in this skill
│   ├── MAINTENANCE.md                     # Repository structure, registration, and validation policy
│   ├── VERSIONING.md                      # Skill versioning policy
│   ├── CONTRIBUTING.md                    # Maintainer model and pre-merge validation expectations
│   └── SECURITY.md                        # Private vulnerability reporting path
├── evals/
│   └── evals.json                         # Skill-creator behavioral regression prompts
├── principles/
│   ├── evaluation-rules.md                # Evidence-only, no assumptions, neutrality, status markers, constraints
│   └── output-style.md                    # Tone, fixed vocabularies, consistency, determinism
├── process/
│   ├── audit-workflow.md                  # Intake, scope, evidence, assessment, synthesis, validation
│   ├── json-exchange.md                   # Machine-readable parameter documents for intake questions
│   ├── report-format.md                   # Audit report format index: rules, section order, spec map
│   ├── report-format/                     # Per-section report specifications
│   │   ├── report-opening.md              # Document Information, coverage matrix, Glossary
│   │   ├── multi-project.md               # Combined multi-project report structure
│   │   ├── summary-changes.md             # Executive Summary, Changes Since Previous Audit
│   │   ├── context-compliance.md          # System Context, SBOM, License Compliance review
│   │   ├── dashboard-observations.md      # Health Dashboard, delivery, observations
│   │   ├── methodology-scoring.md         # Auditing Methodology, Scoring Rubrics
│   │   ├── architectural-assessment.md    # Architectural Assessment and subsections
│   │   ├── report-analysis.md             # Trade-off Analysis, Threat Model
│   │   ├── conditional-conformance.md     # Conditional conformance sections
│   │   ├── findings-registers.md          # Findings, debt, risk, roadmap, and classification
│   │   ├── hunt-style.md                  # `hunt` report style: verdict, journeys, domain findings
│   │   └── report-closing.md              # Exclusions, limitations, handoff, validation, references
│   ├── report-contract.md                 # One-page mechanically enforced report contract
│   ├── report-parity.md                   # Audit parity checklist and consistency gate before final
│   ├── readiness-scoring.md               # Deterministic scores, confidence, maturity, and readiness gates
│   └── review-report.md                   # Review report contract: sections, amendments, naming
├── assessment/
│   ├── testing-review.md                  # Test pyramid (unit/integration/e2e), TDD, coverage, testability
│   ├── design-principles.md               # SOLID, cohesion and coupling, DRY, separation of concerns
│   ├── code-quality.md                    # Static analysis, type safety, complexity, duplication, dead code
│   ├── best-practices.md                  # Stack idioms, framework conventions, ecosystem layout, deprecated APIs
│   ├── dependency-review.md               # Dependency freshness, vulnerabilities, licenses, lockfiles, SBOM
│   ├── deployment-review.md               # Build pipeline, release process, frequency, absent-automation assessment
│   ├── rollback-review.md                 # Rollback mechanism, deploy safety, versioning
│   ├── maintainability-review.md          # Modularity, coupling, structure, technical debt
│   ├── change-management.md               # Feature flags, ADRs, release governance
│   ├── documentation-review.md            # Entry, API, inline docs, onboarding, knowledge transfer
│   ├── nfr-review.md                      # Performance, scalability, availability, reliability, resilience
│   ├── security-review.md                 # Auth, authorization, input validation, OWASP, data exposure
│   ├── compliance-review.md               # Data protection, privacy, regulatory scope, licensing, audit trail
│   ├── observability-review.md            # Logging, metrics, tracing, alerting
│   ├── error-handling.md                  # Exceptions, retries, fallbacks, user-facing errors
│   ├── operational-readiness.md           # Runbooks, on-call, capacity, backups, incident response
│   ├── generated-code.md                  # Explicit provenance, generated-artifact validation, SDLC evidence
│   ├── ai-system.md                       # (conditional) AI lifecycle, evaluation, safety, and provenance
│   ├── copyright-review.md                # Code originality, license compliance, attribution
│   ├── data-flow.md                       # (conditional) DFD, trust boundaries, inter-process flows
│   ├── design-patterns.md                 # (conditional) GoF/POSA pattern fitness and anti-patterns
│   ├── threat-model.md                    # (conditional) STRIDE threat enumeration per trust boundary
│   ├── api-contract.md                    # (conditional) API spec conformance, RFC 9457, OWASP API Top 10
│   ├── skill-definition.md                # (conditional) Agent Skills spec conformance
│   ├── agent-guidance.md                  # (conditional) Agent-guidance set topology and authority
│   ├── standards-conformance.md           # (conditional) Project development standards conformance and quality
│   └── api-compatibility.md               # (conditional) API compat gates, versioning, breaking-change tracking
├── synthesis/
│   ├── risk-register.md                   # Unified risk register with FND cross-referencing
│   ├── project-scorecard.md               # Project scorecard, rubric, and scale display rules
│   ├── tradeoff-analysis.md               # Engineering trade-offs in standalone table and embedded findings
│   ├── remediation-roadmap.md             # Actionable remediation roadmap with priority matrix and classification
│   ├── report-triangulation.md            # Contradiction register and external-report reconciliation
│   ├── debt-register.md                   # (conditional) TDR inventory with CISQ/SQALE cost model
│   ├── reaudit-plan.md                    # (conditional) Verification ownership, sign-off gates, re-audit triggers
│   └── report-comparison.md               # (conditional) Previous report discovery, revisions, comparison
├── references/
│   ├── stack-standards.md                 # Stack, supply-chain, and AI reference sources
│   ├── cwe-analyzer.md                    # CWE to static-analyzer-rule cross-reference per ecosystem
│   ├── dependency-manifests.md            # Text-only manifest readers, source-derived component inventory
│   ├── census-commands.md                 # Canonical reproducible census methods
│   ├── domain-profiles.md                 # Project-nature classification and mandatory stack/purpose checks
│   ├── audit-taxonomy.md                  # Canonical audit types, coverage statuses, source corpus
│   ├── sbom-schema.md                     # Report-level source-derived component inventory schema
│   ├── license-compliance.md              # License classes, copyleft, notices, ownership checks
│   ├── delivery-practice.md               # DORA proxies, bus-factor rubric, continuity evidence
│   ├── exploitability-narrative.md        # Theoretical attack-path narrative format and tiers
│   ├── agent-skills.md                    # Agent Skills specification corpus, live-check baseline
│   ├── agent-configuration.md             # AGENTS.md, rules, plugin, subagent, MCP, guidance-set baselines
│   ├── source-catalog.md                  # Authoritative source registry and corpus index
│   ├── stacks/                            # Per-stack offline baselines, indexed in source-catalog.md
│   ├── methodology/                       # Methodology digests, indexed in source-catalog.md
│   └── topics/                            # Domain digests, indexed in source-catalog.md
├── scripts/
│   ├── format-table.py                    # Source-width Markdown table formatter
│   ├── align-comments.py                  # Plain-text `#` comment column aligner
│   ├── link-glossary.py                   # Glossary body-link inserter, run before the formatter
│   ├── validate-report.py                 # Audit and Review report validator (`--dump-contract` JSON)
│   ├── new-report.py                      # Report skeleton generator (audit or hunt)
│   ├── finalize-report.py                 # Runs link, format, and validate in order on a report
│   ├── validate-skill.py                  # Dependency-light Agent Skill validator
│   ├── check-references.py                # Relative-reference integrity checker
│   ├── check-contents.py                  # Contents-table versus heading drift checker
│   ├── check-update.py                    # Git upstream self-update checker for the skill repo
│   ├── lint-polish.py                     # Polish report linter for calques and typography
│   ├── lint-prose.py                      # Pre-assembly prose linter for report drafts
│   ├── common.py                          # Shared helpers for skill-maintenance tools
│   └── README.md                          # Tool usage, safety, and cleanup rules
└── translations/
    └── polish-language.md                 # Polish rendering: vocabulary and style rules
```

The `scripts/` utilities are report-production and skill-maintenance tools.

They do not build, test, scan, or execute the audited project.

Copy report-production scripts into the audited repository's `work/` directory under a `.tmp.` name.

Use an existing `temp` or `temporary` directory when `work/` is unavailable,
and use the repository root only when none exists.

Run them only against report artifacts and remove the copies after use.

File-mode reports are composed as `.tmp.<stem>-part-NN.md` part files in the same scratch
locations, concatenated in section order into the output file, and the parts are deleted only
after the assembled report passes validation - they are checkpoints against mid-flight loss.

Sections marked *(conditional)* appear in a report only when the subject warrants them.

A system with no API gets no API Contract section,
a single-user local utility with no trust boundary gets no Threat Model.

The inclusion criteria are defined in the Conditional Sections table of `process/report-format.md`.

---

## Document Style

Every document that is part of this skill must follow the rules specified in
[docs/STYLE.md](./docs/STYLE.md).

That file compiles Markdown text style, table formatting, and Agent Skills document requirements
into a single reference.

---

## Specification

Lens conforms to the [Agent Skills specification](https://agentskills.io/specification).

`SKILL.md` declares `name`, `description`, `license`, `compatibility`, `metadata`, and
`allowed-tools` in YAML frontmatter, and the repository follows the conventional `scripts/`,
`references/` layout with progressive disclosure.

Verify the structure and file references:

```text
python scripts/validate-skill.py .
python scripts/check-references.py .
```

`assessment/skill-definition.md` encodes the same conformance rules for auditing other skills,
and `references/agent-configuration.md` extends the coverage to `AGENTS.md`, rules
directories, plugin manifests, subagent definitions, instruction files, and MCP configuration.

---

## Verification For Skill Maintenance

This repository contains Markdown instructions, not an application build or an automated model
benchmark suite.

When changing the skill, follow `docs/MAINTENANCE.md` and:

- Run `python scripts/validate-skill.py .`, `python scripts/check-references.py .`, and
  `python scripts/check-contents.py .` after changing skill files.
- The maintainer runs the same validators before merging a pull request.
- Run `git diff --check` to detect whitespace errors.
- Format edited tables using an automated source-width formatter per `docs/STYLE.md`.
- Check Contents tables in files over 300 lines and preserve encoding and line endings.
- Review router, workflow, templates, synthesis guides, and translations for agreement.
- Exercise the regression scenarios in `process/audit-workflow.md` and record limitations.

Name temporary validation scripts with a `.tmp.` infix, place them in `work/` when it exists and in
the repository root otherwise, and remove them after use.

Report part files follow the same `.tmp.` infix and scratch placement,
and may sit beside the output file during assembly when the scratch tree is not writable by
file tools.

Structural checks do not prove that future agents will follow the instructions, a fresh audit or
independent model evaluation is a separate behavioral verification step.

## License

MIT - see [LICENSE](./LICENSE).

---

## Credits

Built by Filip Golewski.

If you use this skill in a project, a link back is appreciated but not required.
