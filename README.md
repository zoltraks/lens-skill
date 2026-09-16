# Lens - Software Audit Skill

```
 /\_/\  
( o.o ) 
 > ^ <
```

> Evidence-based engineering audits of any software subject - prototypes, codebases under development, and already-running production systems.
>
> [Versioning Policy](./VERSIONING.md)

Lens is a structured audit process packaged as an agent skill. It guides an AI coding agent through a complete engineering assessment of a codebase, producing a neutral, repeatable report anchored to concrete facts rather than impressions.

Unlike a generic "review my code" prompt, Lens enforces a fixed workflow: intake, parameter
configuration, scope definition, evidence gathering, per-category assessment, synthesis, and
validation.

The output is a standardized report with sixteen baseline sections - document
information, technology stack, executive summary, health dashboard, high-level observations,
auditing methodology, scoring rubrics, system context, architectural assessment, strengths and
what's working, detailed technical findings, unified risk register, trade-off analysis, actionable
remediation roadmap, scope exclusions, and references - plus conditional sections (data flow
diagram, design patterns, architecture decision records, threat model, API contract conformance,
skill definition conformance, standards conformance, technical debt register, changes since
previous audit, and re-audit plan) that appear only when the subject warrants them.

Every section uses a hybrid table-paragraph format for scannable summaries backed by detailed
evidence.

---

## What the skill does

When you ask for an audit, the agent loads the skill and performs the following:

**Reads everything you supplied**

Code, configuration, documentation, logs, and prior reports. It identifies the artifact type (prototype, codebase, production system, or proposal) and records the source format.

**Configures parameters**

Asks whether to accept default parameters (report delivery, detail level, evaluation scale, improvement suggestions) or configure them individually. The user may bypass at any stage to proceed with defaults.

**Defines scope explicitly**

Lists what is in scope and what is excluded. Marks unstated constraints as `NOT SPECIFIED` rather than assuming industry norms.

**Gathers evidence before judging**

Collects concrete anchors - file paths, config keys, commands, pipeline steps - before forming conclusions. Separates collection from judgment to avoid confirmation bias.

**Assesses across 18 categories**

Testing, design principles, code quality, stack best practices, dependencies, deployment, rollback, maintainability, change management, documentation, non-functional requirements, security, compliance, observability, error handling, operational readiness, AI-generated code detection and provenance, and copyrights and originality. Each category receives one of five statuses: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or `N/A`.

**Synthesizes findings**

Builds a unified risk register with bidirectional cross-referencing to findings, a 1-10 scorecard from category findings (1-5 available on request), and an actionable remediation roadmap with prioritized impact-vs-effort tracking.

**Produces a validated report**

Re-checks every finding against the evaluation rules: no assumptions, no personal judgment, no emotional language, every claim anchored to a concrete fact.

---

## Evidence And Decision Quality

Lens separates inspected source, executed checks, reported claims, and inference.

Every audit records a verification plan and evidence ledger with revision, exact command or source,
tool/database version, result, artifact, and limitations, including checks that could not run.

Safe, available checks are used when permitted, tool installation and untrusted execution are not
implied by an audit request.

Serious findings receive a counter-check for reachability, existing guards, and alternative
explanations before they reach the executive summary.

Security findings use justified CWE mappings and CVSS vectors where applicable, while engineering
and business risks retain the Lens risk matrix.

The guides cover Rust baseline checks, coverage, mutation/fuzz testing, unsafe-use statistics,
dependency advisories, SBOMs, and license policies, with equivalent tools selected for other stacks.

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

## Core principles

Every audit follows these non-negotiable rules:

- **Evidence only** - findings trace to a concrete fact: a file, a config value, a command, a log line.
- **No assumptions** - missing information is marked `UNKNOWN`, `NOT SPECIFIED`, or `INSUFFICIENT INFORMATION`.
- **No personal judgement** - the report evaluates the system, never the people who built it.
- **Architectural neutrality** - choices are judged within stated constraints, not against a favored stack.
- **Contextual applicability** - categories that cannot apply to the deployment model are marked `N/A` with justification, not treated as failures.

---

## Report format

The skill uses a hybrid table-paragraph format throughout:

- **Tables** provide scannable summaries with one to three words per cell.
- **Paragraphs** below each table provide detailed evidence, file paths, and reasoning.
- **Finding IDs** are shown as `FND-[PILLAR]-[001]` in the detailed findings section.
- **Risk IDs** are shown as `RSK-[001]` and cross-referenced to source findings.
- **Recommendation IDs** are shown as `REC-[001]` and traced to specific findings.
- **Scores** in the scorecard are shown as `Score: 7/10` inline after the dimension name (or `Score: X/5` when the 1-5 scale is selected).
- **Severities** are shown as `SEVERITY: CRITICAL` inline after the finding title.
- **High-Level Observations** provide a fast-skim path for non-technical readers.
- **Strengths & What's Working** balances the tone with 5-8 acknowledged positives.
- **Trade-off Analysis** surfaces architectural tensions in a dedicated table.

This format keeps the report readable in plain-text consoles while preserving depth.

---

## When to use this skill

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
| "Check conformance with our dev standards"       | **Yes** - use `assessment/standards-conformance.md` |
| "Compare these two architectural options"        | **Yes** - embed trade-offs into relevant findings   |
| "Write the feature for me"                       | No - this skill assesses, it does not build         |
| "Tell me which team member caused this"          | No - this skill never evaluates people              |

---

## Example prompts

**Full audit**
> Audit this production codebase. Produce a full engineering assessment with a unified risk register, scorecard, and actionable remediation roadmap.

**Audit to a file**
> Perform lens on this service and write the audit report to AUDIT.md. (The agent will accept the filename and ask whether to accept other defaults or configure parameters.)

**Audit without a named file**
> Make audit report on this codebase. (The agent will ask whether to accept default parameters or configure them, then whether to reply inline or write to a file.)

**Readiness assessment**
> Is this system production-ready? Assess testing, deployment, rollback, observability, and operational readiness, and state the maturity level with evidence.

**Single dimension**
> Review only the security posture of this codebase. Mark anything you cannot determine from the provided files.

**SOLID and testability**
> Assess this codebase against SOLID principles and its testing strategy: test pyramid balance, TDD signals, and how testable the code is.

**Stack best practices**
> Review whether this code follows the idiomatic best practices of its stack: language idioms, framework conventions, ecosystem layout, and any deprecated APIs.

**Dependency and supply-chain audit**
> Audit the dependencies of this project: flag outdated and vulnerable packages, license compatibility, and whether builds are locked and reproducible.

**Risk register**
> Build a risk register for this architecture proposal. Use Low / Medium / High / Critical severities and tie each risk to evidence.

**Architectural trade-off**
> Evaluate the trade-off between keeping in-memory state versus introducing an external store for this prototype, given a single-instance target. Include a standalone trade-off table and embed the analysis into the relevant architectural finding.

**Re-audit**
> Re-run the audit on this codebase after the latest fixes. (The agent finds the previous report, writes a new versioned file such as `AUDIT-1.1.md` without overwriting it, and adds a Changes Since Previous Audit section.)

**Thin input**
> Here is a one-paragraph description of a service. Audit what you can and list exactly what additional artifacts would raise confidence.

**Skill definition audit**
> Audit this Agent Skill for spec conformance. Check the SKILL.md frontmatter against the Agent Skills specification, verify all file references resolve, and assess whether the description triggers correctly.

---

## What's inside

```
lens-skill/
├── SKILL.md                       # Root router - load this first
├── STYLE.md                       # Document style rules for all files in this skill
├── principles/
│   ├── evaluation-rules.md        # Evidence-only, no assumptions, neutrality, status markers, constraints
│   └── output-style.md            # Tone, fixed vocabularies, consistency, determinism
├── process/
│   ├── audit-workflow.md          # Intake, scope, evidence, assessment, synthesis, validation
│   └── report-format.md           # The table-driven, unnumbered report template
├── assessment/
│   ├── testing-review.md          # Test pyramid (unit/integration/e2e), TDD, coverage, testability
│   ├── design-principles.md       # SOLID, cohesion and coupling, DRY, separation of concerns
│   ├── code-quality.md            # Static analysis, type safety, complexity, duplication, dead code
│   ├── best-practices.md          # Stack idioms, framework conventions, ecosystem layout, deprecated APIs
│   ├── dependency-review.md      # Dependency freshness, vulnerabilities, licenses, lockfiles, SBOM
│   ├── deployment-review.md      # Build pipeline, release process, frequency, manual steps
│   ├── rollback-review.md        # Rollback mechanism, deploy safety, versioning
│   ├── maintainability-review.md # Modularity, coupling, structure, technical debt
│   ├── change-management.md       # Feature flags, ADRs, release governance
│   ├── documentation-review.md   # Entry, API, inline docs, onboarding, knowledge transfer
│   ├── nfr-review.md             # Performance, scalability, availability, reliability, resilience
│   ├── security-review.md        # Auth, authorization, input validation, OWASP, data exposure
│   ├── compliance-review.md      # Data protection, privacy, regulatory scope, licensing, audit trail
│   ├── observability-review.md   # Logging, metrics, tracing, alerting
│   ├── error-handling.md          # Exceptions, retries, fallbacks, user-facing errors
│   ├── operational-readiness.md   # Runbooks, on-call, capacity, backups, incident response
│   ├── ai-generated-code.md       # Explicit provenance, generated-artifact validation, SDLC evidence
│   ├── copyright-review.md       # Code originality, license compliance, attribution
│   ├── data-flow.md               # (conditional) DFD, trust boundaries, inter-process flows
│   ├── design-patterns.md         # (conditional) GoF/POSA pattern fitness and anti-patterns
│   ├── threat-model.md            # (conditional) STRIDE threat enumeration per trust boundary
│   ├── api-contract.md            # (conditional) API spec conformance, RFC 9457, OWASP API Top 10
│   ├── skill-definition.md        # (conditional) Agent Skills spec conformance, frontmatter, progressive disclosure
│   └── standards-conformance.md   # (conditional) Project development standards conformance and quality
├── synthesis/
│   ├── risk-register.md           # Unified risk register with FND cross-referencing
│   ├── project-scorecard.md      # 1-10 project scorecard and rubric (1-5 optional)
│   ├── trade-off-analysis.md      # Engineering trade-offs in standalone table and embedded findings
│   ├── remediation-roadmap.md     # Actionable remediation roadmap with priority matrix
│   ├── debt-register.md           # (conditional) TDR inventory with CISQ/SQALE cost model
│   ├── re-audit-plan.md           # (conditional) Verification ownership, sign-off gates, re-audit triggers
│   └── report-comparison.md       # (conditional) Previous report discovery, versioning, comparison section
└── translation/
    └── polish-language.md         # Polish translations: status, severity, headings, table headers, style rules
```

Sections marked *(conditional)* appear in a report only when the subject warrants them. A system with no API gets no API Contract section, a single-user local utility with no trust boundary gets no Threat Model. The inclusion criteria are defined in the Conditional Sections table of `process/report-format.md`.

The skill activates automatically when you ask for a software audit, architecture audit, production code audit, technical due diligence, readiness assessment, risk register, scorecard, or remediation roadmap.

---

## Document Style

Every document that is part of this skill must follow the rules specified in [STYLE.md](./STYLE.md).

That file compiles Markdown text style, table formatting, and Agent Skills document requirements into a single reference.

---

## Verification For Skill Maintenance

This repository contains Markdown instructions, not an application build or an automated model
benchmark suite.

When changing the skill:

- Run `git diff --check` to detect whitespace errors.
- Check frontmatter lengths, skill name, unchanged version, and root-router references.
- Format edited tables using an automated source-width formatter per `STYLE.md`.
- Check Contents tables in files over 300 lines and preserve encoding and line endings.
- Review router, workflow, templates, synthesis guides, and translations for agreement.
- Exercise the regression scenarios in `process/audit-workflow.md` and record limitations.

Use `work/` for temporary validation scripts and remove only the temporary artifacts you created.

Structural checks do not prove that future agents will follow the instructions, a fresh audit or
independent model evaluation is a separate behavioral verification step.

## License

MIT - see [LICENSE](./LICENSE).

---

## Credits

Built by Filip Golewski.

If you use this skill in a project, a link back is appreciated but not required.
