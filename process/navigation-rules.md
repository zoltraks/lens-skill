# Navigation Rules

## Purpose

> **Scope:** File-selection, section-placement, and report-construction rules applied
> to every audit, hunt, or review report
> **Key items:** assessment file routing, evidence and tagging rules, report skeleton
> and style rules, multi-project and conditional-section rules

- Always apply `principles/evaluation-rules.md` and `principles/output-style.md` to every report.
- The `audit` report style is the default deliverable. A `review` style report renders per
  `process/report-format/review-style.md`, and a structure-scoped review renders the variant
  contract in `process/report-format/structure-review.md`.
- Never compile, build, test, or execute the audited project, and never run linters, scanners,
  or generators against it - `executed-readonly` permits only commissioned non-mutating analyzers.
  Verification claims rest on inspected contents, documented results are `Reported` evidence.
- Assemble the audit report skeleton from `process/report-format.md` and its section files before
  filling in findings, present every section as a table and use unnumbered headings.
- Every audit report opens with the Audit Type Coverage table built from the fixed
  types and statuses in `references/audit-taxonomy.md`, kept consistent with Scope Exclusions.
- Every finding and every Evidence Ledger row carries a `Type` tag: `Observation` for an
  independently re-derivable fact, `Concern` for a risk judgment built on observations.
- The generated report follows the skill's Markdown rules adapted by `process/report-format.md`:
  `#`/`##`/`###` headings only, one-sentence paragraphs, wrap at a selectable width (default 100),
  no semicolons, tables aligned by a formatting script, no Contents table.
- Test layers, TDD, coverage, and design-for-testability belong in `assessment/testing-review.md`.
- SOLID and design principles (SRP, OCP, LSP, ISP, DIP), cohesion, coupling, and DRY belong in
  `assessment/design-principles.md`, code-level metrics (lint, type safety, complexity, duplication)
  belong in `assessment/code-quality.md`, module layout in `assessment/maintainability-review.md`.
- Physical organization - directory layout, file placement, naming conventions, language-idiomatic
  code division, component placement and physical boundaries, supporting-artifact layout. Belongs
  in `assessment/structure-review.md` and `references/naming-and-layout.md`, while in-code naming,
  style consistency, and readability belong in `assessment/code-style.md`. Logical modularity,
  coupling, dependency direction, and technical debt stay in `assessment/maintainability-review.md`,
  and code-level runtime idioms stay in `assessment/best-practices.md`. The structure assessment
  runs for `audit` and `review` reports and never loads under `Report Style: hunt`.
- Stack-specific idioms and conventions (language idioms, framework patterns, ecosystem layout,
  deprecated APIs) belong in `assessment/best-practices.md`, keep it distinct from the principles in
  `assessment/design-principles.md` and the code-level metrics in `assessment/code-quality.md`.
  Assess adherence to the stack the subject already uses, do not judge the stack choice itself.
- Dependency Inversion overlaps testability, assess the principle in
  `assessment/design-principles.md` and its testing impact in `assessment/testing-review.md`.
- Third-party dependency and supply-chain posture belongs in `assessment/dependency-review.md`,
  project-internal change control belongs in `assessment/change-management.md`.
- Deployment automation belongs in `assessment/deployment-review.md`, reverting a release belongs in
  `assessment/rollback-review.md`. A `none` census bounds it to one observation, `external`
  records outside-the-tree automation as `Reported` evidence rather than an absence.
- Performance, scalability, availability, reliability, and resilience belong in
  `assessment/nfr-review.md`, day-two operations belong in `assessment/operational-readiness.md`.
- Logging and metrics belong in `assessment/observability-review.md`, failure handling in code
  belongs in `assessment/error-handling.md`.
- Data protection, privacy, and licensing belong in `assessment/compliance-review.md`.
- Code provenance and generated-artifact validation belong in `assessment/generated-code.md`,
  concrete quality defects remain in their technical categories regardless of origin.
- Code originality, license compliance, and attribution belong in `assessment/copyright-review.md`.
- Data flow modeling and trust boundaries belong in `assessment/data-flow.md`, STRIDE threat
  enumeration belongs in `assessment/threat-model.md` and depends on the data flow model,
  control-level security review belongs in `assessment/security-review.md`.
- Concrete design pattern identification and fitness belong in `assessment/design-patterns.md`, keep
  it distinct from the SOLID principles in `assessment/design-principles.md`.
- API specification conformance and the OWASP API Security Top 10 belong in
  `assessment/api-contract.md`, ADR gap assessment belongs in `assessment/change-management.md`.
- Agent Skills specification conformance belongs in `assessment/skill-definition.md` when the
  subject holds `SKILL.md` files or agent-facing artifacts, with `references/agent-skills.md`
  and `references/agent-configuration.md` as baselines. Intake classifies each discovered
  skill as authored, external member, installed, or undetermined. Installed skills are not
  audit subjects, an external member audits as an independent project at its checked-out state.
- Agent-guidance set topology - entry routes, index of record, topic owners, role resolution -
  belongs in `assessment/agent-guidance.md` for a structured guidance set. Per-artifact format
  conformance stays with `assessment/skill-definition.md`.
- A location that holds multiple projects, including skill collections with submodule or nested
  members, audits each included member as an independent project per `process/audit-workflow.md`
  and `process/report-format/multi-project.md`, unfetched members disclosed in Scope Exclusions.
- Standards conformance belongs in `assessment/standards-conformance.md`, only for documented
  development standards. References lists every external source consulted.
- Engineering baseline conformance belongs in `assessment/baseline-conformance.md`: it measures
  the floor bundled stack and purpose digests define, applies only when the subject's detected
  stack or nature is covered, and records which baseline governed each judgement.
- Canonical stack references are re-derived from `references/stack-standards.md` during intake
  and cited in Auditing Methodology and References, never copied verbatim from a prior report.
- Every CWE-classified security finding names its equivalent static analyzer rule from
  `references/cwe-analyzer.md` or states none exists. The lookup never implies an analyzer ran.
- Source-derived dependency inventories follow `references/dependency-manifests.md` (manifests
  and lockfiles read as text) and render per `references/sbom-schema.md` with underivable
  fields `Unknown`, never an executed or shipped-artifact SBOM.
- The License Compliance Review follows `references/license-compliance.md` and
  separates observed license facts from inferred concerns without legal conclusions.
- The Delivery Practice & Team Continuity section follows `references/delivery-practice.md`:
  five DORA metrics with labeled source-derived proxies, telemetry-dependent metrics
  `NOT SPECIFIED`, and a bus-factor rating.
- Every `HIGH`/`CRITICAL` Security & Compliance finding carries an `Exploitability` field per
  `references/exploitability-narrative.md`: `Theoretical` tier by default, never an exploitation
  claim.
- API compatibility gates, versioning consistency, and breaking-change tracking belong in
  `assessment/api-compatibility.md`, only for a reusable library or package.
- An overall score always reports the lowest-scoring applicable dimension beside it, per
  `synthesis/project-scorecard.md`.
- Conditional sections appear only when their inclusion criterion is met per the table in
  `process/report-format.md`, with omissions noted in Scope Exclusions - never force one.
- The Technical Debt Register (`synthesis/debt-register.md`) is distinct from the Unified Risk
  Register: debt is cost already present, risk is what could go wrong. Never duplicate entries.
- The Re-audit And Follow-up Plan (`synthesis/reaudit-plan.md`) precedes Validation Record and
  maps P1/P2 findings to verification owners and closure evidence.
- Every absent-capability finding carries an `Absence` field built from repository signals per
  `principles/evaluation-rules.md`, never a claim about the authors' motives.
- Recommendation Classification (`synthesis/remediation-roadmap.md`) classes every `REC-XXX`,
  omitted at Brief with a Scope Exclusions note.
- The Changes Since Previous Audit section (`synthesis/report-comparison.md`) appears only
  when a previous report exists - never overwritten, the new file carries the next revision.
- `report-style: hunt` or `review` renders the same evidence base per
  `process/report-format/hunt-style.md`/`review-style.md` - intake records the snapshot,
  external reports reconcile per `synthesis/report-triangulation.md`.
- Limitations and Unknowns lists every unperformed check. Validation Record closes the report
  with the Mandatory Core Checklist result and the `process/report-parity.md` gate outcome.
- Multi-project reports: a condensed combined Executive Summary and Changes follow the
  Project Inventory, combined Trade-off Analysis holds only cross-project trade-offs.
- Each `translations/` file defines one report language, loaded only when needed.
- Prefer the narrowest assessment file matching the request: a single-dimension request loads
  that one file plus `principles/` and produces the matching finding pillar and risk row only.
- Trade-offs appear in Trade-off Analysis after Architectural Assessment and embedded in
  findings, per `synthesis/tradeoff-analysis.md`.
- For a full audit, load `principles/`, `process/`, every relevant `assessment/` file, and all
  `synthesis/` files, marking inapplicable categories `N/A` with justification.
