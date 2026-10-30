# Assessment Categories

## Purpose

> **Scope:** Index of the per-dimension assessment guides loaded during an audit,
> hunt, or review
> **Key items:** core assessment files, conditional assessment files, loading rules

Open only the assessment files that match the system under audit - a
single-dimension request loads its one matching file, a full audit loads every
relevant file.

## Core Files

- **`assessment/testing-review.md`** - Test pyramid, TDD, coverage, CI automation, testability.
- **`assessment/design-principles.md`** - SOLID, cohesion and coupling, DRY, separation of concerns.
- **`assessment/code-quality.md`** - Static analysis, typing, complexity, duplication, dead code.
- **`assessment/correctness-review.md`** - Functional correctness: defect-pattern census,
  shipped-surface completeness, read-confirmation discipline.
- **`assessment/best-practices.md`** - Stack idioms, framework conventions, deprecated APIs.
- **`assessment/dependency-review.md`** - Freshness, vulnerabilities, licenses, lockfiles, SBOM.
- **`assessment/deployment-review.md`** - Build pipeline, release process and frequency,
  manual steps, absent-automation assessment.
- **`assessment/rollback-review.md`** - Rollback mechanism, deploy safety, versioning, recovery.
- **`assessment/maintainability-review.md`** - Modularity, coupling, code structure, technical debt.
- **`assessment/structure-review.md`** - Directory layout, file placement, naming, component
  boundaries, supporting artifacts.
- **`assessment/code-style.md`** - In-code naming, style consistency, readability, conventions.
- **`assessment/change-management.md`** - Feature flags, ADR usage, release governance.
- **`assessment/documentation-review.md`** - Documentation coverage, onboarding, transfer.
- **`assessment/nfr-review.md`** - Performance, scalability, availability, reliability, resilience.
- **`assessment/security-review.md`** - Authentication, authorization, input validation, OWASP.
- **`assessment/compliance-review.md`** - Data protection, privacy, regulatory scope, licensing.
- **`assessment/observability-review.md`** - Logging, metrics, tracing, alerting.
- **`assessment/error-handling.md`** - Exception strategy, retries, fallbacks, user-facing errors.
- **`assessment/frontend-review.md`** - Client injection surface, storage residue,
  accessibility, dead features, frontend-backend agreement.
- **`assessment/operational-readiness.md`** - Runbooks, on-call, capacity, backups.
- **`assessment/generated-code.md`** - Code provenance, generated-artifact validation.
- **`assessment/copyright-review.md`** - Originality, license compliance, attribution.

## Conditional Files

Load these only when the subject meets an inclusion criterion in `process/report-format.md`.

- **`assessment/data-flow.md`** - Data flows, trust boundaries. Include for cross-boundary systems.
- **`assessment/design-patterns.md`** - GoF/POSA pattern fitness. Include for recurring structure.
- **`assessment/threat-model.md`** - STRIDE threats. Include for a security-relevant attack surface.
- **`assessment/api-contract.md`** - API contract conformance. Include when the system has an API.
- **`assessment/skill-definition.md`** - Agent Skill spec conformance, collections, embedded skills.
- **`assessment/agent-guidance.md`** - Agent-guidance set topology. Include for guidance sets.
- **`assessment/ai-system.md`** - AI system lifecycle. Include for AI-dependent projects.
- **`assessment/standards-conformance.md`** - Project development standards conformance.
- **`assessment/baseline-conformance.md`** - Engineering floor against bundled stack and
  purpose baselines. Include for code-bearing subjects a bundled digest covers.
- **`assessment/api-compatibility.md`** - API compatibility. Include for libraries and packages.
- **`assessment/requirements-conformance.md`** - Product requirements and acceptance-criteria
  conformance. Include when the subject carries a requirements or acceptance-criteria
  document.
