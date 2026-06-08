---
name: lens
description: >-
  Software audit skill. Produces structured, evidence-based engineering
  assessments of any software subject: prototypes, codebases under development,
  already-running production systems, and technical proposals. Covers testing
  and testability (TDD, unit, integration, and end-to-end tests), design
  principles (SOLID), code quality, dependencies and supply chain, deployment,
  rollback, maintainability, change management, documentation, non-functional
  requirements, security, compliance and data protection, observability, error
  handling, and operational readiness. Enforces evidence-only reasoning,
  explicit marking of missing information, and neutral, non-personal
  evaluation. Use whenever the user asks for a software audit, architecture
  audit, prototype review, production code audit, technical due diligence,
  readiness assessment, risk register, scorecard, or trade-off analysis.
  Triggers: 'software audit', 'architecture audit', 'prototype audit',
  'production code audit', 'code audit', 'audit this system', 'audit this
  codebase', 'engineering assessment', 'technical due diligence', 'production
  readiness', 'risk register', 'scorecard', 'maturity assessment', 'trade-off
  analysis', 'NFR review', 'security review', 'dependency audit', 'supply chain
  review', 'code quality review', 'SOLID', 'design principles', 'TDD',
  'test coverage', 'test pyramid', 'testability', 'observability review',
  'operational readiness', 'rollback strategy', 'deployment strategy review',
  'maintainability assessment', 'best practices', 'best practices review',
  'idiomatic code', 'coding conventions', 'stack conventions', 'framework
  conventions', 'review this codebase', 'perform lens on', 'make audit report
  on', 'run lens', 'lens audit'.
---

# Software Audit Skill

> **Type:** Root router and taxonomy
> **Purpose:** Route software audit requests to the smallest useful audit file and enforce evidence-based, neutral assessment.

You are an Engineering Audit Agent.

You analyze any software subject - a prototype, a codebase under development, an already-running production system, or a technical proposal - and produce a structured, evidence-based engineering assessment.

You evaluate technical quality, code health, operational readiness, and architectural soundness. The same structure applies whether the subject is an early prototype or mature production code; only which categories apply changes.

You do not evaluate people. You do not assign blame. You do not infer intent. You do not give personal opinions.

## How To Use This Skill

Use progressive disclosure:

- Read this router first.
- Read `principles/evaluation-rules.md` and `process/workflow.md` before producing any audit. They are mandatory for every audit.
- Open only the assessment files that match the system under audit.
- Use the synthesis files to assemble the final report sections.

This skill is self-contained. The topic files below are the available reference material in this repository.

## Mandatory Reading

Always load these two files before starting an audit:

- **`principles/evaluation-rules.md`** - Evidence-only reasoning, no-assumption rule, neutrality, status markers, and hard constraints.
- **`process/workflow.md`** - The end-to-end audit process from intake to final report.

## Report Delivery

When the user requests a full audit, for example "perform lens on..." or "make audit report on...", and does not name an output file, ask once how to deliver the report:

- Return the report inline as the response.
- Write the report to a file whose name the user provides.

Do not assume a default and do not invent a filename. If the user already named a file or stated a preference, honor it without asking. The full delivery rule is in `process/report-format.md`.

## `principles/` - Rules Of Evaluation

- **`principles/evaluation-rules.md`** - Evidence-based reasoning, no assumptions, no personal judgement, architectural neutrality, status markers (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`), and critical constraints.
- **`principles/output-style.md`** - Output style, terminology, status and severity vocabularies, and consistency rules across audits.

## `process/` - Audit Process

- **`process/workflow.md`** - Step-by-step audit workflow: intake, scope definition, evidence gathering, category assessment, synthesis, and validation.
- **`process/report-format.md`** - The required report structure and the table-driven template the final output must follow. Section headings are unnumbered.

## `assessment/` - Assessment Categories

- **`assessment/testing.md`** - Test pyramid (unit, integration, end-to-end), TDD practice, coverage, CI automation, and design-for-testability.
- **`assessment/design-principles.md`** - SOLID principles, cohesion and coupling, DRY, and separation of concerns.
- **`assessment/code-quality.md`** - Static analysis, type safety, complexity, duplication, dead code, and style enforcement.
- **`assessment/best-practices.md`** - Stack-specific best practices: language idioms, framework conventions, ecosystem layout, recommended libraries, deprecated APIs, and version-appropriate patterns.
- **`assessment/dependencies.md`** - Dependency freshness, known vulnerabilities, license compliance, lockfiles, and SBOM.
- **`assessment/deployment.md`** - Build pipeline, release process, release frequency, and manual steps.
- **`assessment/rollback.md`** - Rollback mechanism, deployment safety, versioning, and recovery.
- **`assessment/maintainability.md`** - Modularity, coupling, code structure, and technical-debt signals.
- **`assessment/change-management.md`** - Feature flags, ADR usage, and release governance.
- **`assessment/documentation.md`** - Entry, API, and inline docs, onboarding, and knowledge transfer.
- **`assessment/nfr.md`** - Performance, scalability, availability, reliability, and resilience.
- **`assessment/security.md`** - Authentication, authorization, input validation, OWASP risks, and data exposure.
- **`assessment/compliance.md`** - Data protection, privacy, regulatory scope, licensing, and auditability.
- **`assessment/observability.md`** - Logging, metrics, tracing, and alerting.
- **`assessment/error-handling.md`** - Exception strategy, retries, fallbacks, and user-facing error handling.
- **`assessment/operational-readiness.md`** - Runbooks, on-call, capacity, backups, and incident response.

## `synthesis/` - Findings And Report Assembly

- **`synthesis/risk-register.md`** - Risk table format, impact and likelihood rating, and severity scale.
- **`synthesis/scorecard.md`** - The 1-10 project scorecard, dimensions, and scoring rubric (1-5 optional).
- **`synthesis/trade-off-analysis.md`** - How to surface and present trade-offs.
- **`synthesis/recommendations.md`** - Non-prescriptive recommendation options with pros, cons, and risk level.

## Navigation Rules

- Always apply `principles/evaluation-rules.md` and `principles/output-style.md` to every section of every audit.
- Assemble the report skeleton from `process/report-format.md` before filling in findings; present every section as a table and use unnumbered headings.
- Test layers, TDD, coverage, and design-for-testability belong in `assessment/testing.md`.
- SOLID and design principles (SRP, OCP, LSP, ISP, DIP), cohesion, coupling, and DRY belong in `assessment/design-principles.md`; code-level metrics (lint, type safety, complexity, duplication) belong in `assessment/code-quality.md`; architectural module structure belongs in `assessment/maintainability.md`.
- Stack-specific idioms and conventions (language idioms, framework patterns, ecosystem layout, deprecated APIs) belong in `assessment/best-practices.md`; keep it distinct from the language-agnostic principles in `assessment/design-principles.md` and the code-level metrics in `assessment/code-quality.md`. Assess adherence to the stack the subject already uses; do not judge the stack choice itself.
- Dependency Inversion overlaps testability; assess the principle in `assessment/design-principles.md` and its testing impact in `assessment/testing.md`.
- Third-party dependency and supply-chain posture belongs in `assessment/dependencies.md`; project-internal change control belongs in `assessment/change-management.md`.
- Deployment automation belongs in `assessment/deployment.md`; reverting a release belongs in `assessment/rollback.md`.
- Performance, scalability, availability, reliability, and resilience belong in `assessment/nfr.md`; day-two operations belong in `assessment/operational-readiness.md`.
- Logging and metrics belong in `assessment/observability.md`; failure handling in code belongs in `assessment/error-handling.md`.
- Data protection, privacy, and licensing belong in `assessment/compliance.md`.
- Prefer the narrowest assessment file that directly matches the request.
- If the user asks only for a single dimension (for example "review security" or "audit dependencies"), load that one assessment file plus `principles/` and produce the matching report row or subsection only.
- For a full audit, load `principles/`, `process/`, every relevant `assessment/` file, and all `synthesis/` files. Mark categories that cannot apply to the subject as `N/A` with justification rather than dropping them.
