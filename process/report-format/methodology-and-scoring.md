# Methodology And Scoring

## Purpose

> **Scope:** Auditing methodology and scoring rubric sections
> **Key items:** method, standards, evidence ledger, score bands, ISO crosswalk

## Auditing Methodology

Define how the audit was conducted and the framework used to evaluate findings.

The earlier dashboard is a summary, its scores refer to the methodology and rubric here.

**Methodology overview**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

State that the audit uses evidence-based reasoning across 18 core assessment categories grouped into
six pillars, plus conditional assessments (data flow, design patterns, threat model, API contract,
skill definition, standards conformance) applied when the subject warrants them,
and the conditional API Compatibility & Versioning Discipline pillar for libraries and packages.

List the pillars:

- **Architecture & Design** - Design principles, maintainability, change management, documentation,
  non-functional requirements
- **Code Quality** - Testing, code quality, stack best practices
- **Security & Compliance** - Security, compliance and data protection
- **Infrastructure & CI/CD** - Dependencies, deployment, rollback, observability, error handling,
  operational readiness
- **AI Provenance & Code Origin** - Explicit attribution, generated-artifact validation, and SDLC
  evidence, without authorship inference from style
- **Copyrights & Originality** - Code originality, license compliance, attribution, dependency
  license compatibility
- **API Compatibility & Versioning Discipline** - Public API stability, versioning consistency, and
  breaking-change tracking. Conditional, applied only when the subject is a reusable library or
  package.

When the report language is not English, apply the pillar name translations from the matching
`translations/` file.

**Reference standards**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Name the external standards the audit aligns with,
so the methodology is credible to an external reader.

Cite only the standards actually applied to the subject.

Typical references:

- **ISO/IEC 25010:2023** - nine-characteristic product quality coverage, using the explicit
  crosswalk
  in `synthesis/project-scorecard.md`, not an ISO scoring formula.
- **OWASP ASVS 5.0.0** - selected version-qualified security controls, with scope and level stated.
- **CWE and CVSS** - weakness classification and vulnerability severity where applicable.
- **SSDF and SAMM** - selected secure-development practices when process evidence is assessed.
- **OWASP Top 10 (2025)** and, for APIs, **OWASP API Security Top 10 (2023)** - for the security
  category coverage.
- **NIST SP 800-30** - risk assessment process, for the risk register and threat model.
- **STRIDE** - threat enumeration framework, when a threat model is included.
- **CISQ / SQALE** - structural quality and technical-debt cost model, when a technical debt
  register is included.
- **ISO 19011** and **NIST RMF** - audit follow-up and continuous monitoring, when a re-audit plan
  is included.

Beyond the generic standards above, name the stack-specific canonical sources applied,
selected per `references/stack-standards.md`:
for example the Rust API Guidelines and the RustSec Advisory Database for Rust,
or the Framework Design Guidelines and NuGet package authoring best practices for .NET.

Stack-specific sources are the primary reference set for the detected stack,
not optional decoration.

Cite a standard only when its corresponding section or assessment is present in the report.

Do not list a standard that was not applied.

**Audit evidence statement**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Begin the Methodology section with 2-3 sentences stating exactly what was inspected.

Include:

- The number of source files, test files, and configuration files reviewed. State whether
  `.gitignore` exclusions were applied. If `.gitignore` was absent, record that fact without
  assuming a defect.
- Whether Git history was examined.
- Which documented check results, such as CI output, coverage reports, or scan artifacts, were
  supplied or committed.

Example: "This audit inspected 147 source files, 8 test files,
and 4 configuration files from the repository root, excluding files listed in `.gitignore`.

Git commit history was reviewed for the last 15 commits.

No builds, tests, or tools were executed,
all findings are based on static inspection of the repository contents."

**Verification And Evidence Ledger**

Include the per-project check summary and evidence records from `process/audit-workflow.md`.

| Evidence ID | Project   | Check / Source      | Execution | Result   | Type          | Artifact      |
|-------------|-----------|---------------------|-----------|----------|---------------|---------------|
| EVD-001     | <project> | <source or command> | <state>   | <result> | <obs/concern> | <path or gap> |

The `Type` column carries `Observation` or `Concern` per `principles/evaluation-rules.md`:

`Observation` for a fact another auditor could re-derive from the same artifact,
`Concern` for a risk judgment built on observations.

Most ledger rows are `Observation`.

The tag is enforced mechanically: `scripts/validate-report.py` flags every `| EVD-` row and every
finding block whose `Type` cell or field is missing or carries another value,
so the Validation Record attestation is backed by a check rather than memory.

Place documented commands, source locations, revisions, declared tool or report versions,
exclusions, and limitations below the table rather than abbreviating away traceability.

An anchor may be a line range or a mechanism description when no single line carries the defect,
an honest range beats a fabricated line.

Include documented checks that were not run, and label supplied or committed results as
reported.

For dependencies, summarize inventory/SBOM scope, schema version, license policy, advisory triage,
and artifact paths, not just direct manifest versions.

When no SBOM exists, record the source-derived component inventory produced per
`references/dependency-manifests.md`, labeled as manifest-derived rather than shipped content.

For testing, distinguish inspected test counts from documented coverage and mutation outcomes.

Link every finding to supporting `EVD-XXX` records.

Identifiers apply only within a single report and may be reassigned in later revisions.

Cite a previous report's evidence as `EVD-XXX` plus the report name,
for example `EVD-017 in AUDIT-1.2`.

**Severity definitions**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Add a 4-row rubric defining each qualitative severity band.

These definitions anchor the severity values used in findings and risks.

| Severity | Meaning                  | Readiness Treatment       |
|----------|--------------------------|---------------------------|
| CRITICAL | Critical contextual risk | Gate resolution           |
| HIGH     | Major contextual risk    | Gate resolution           |
| MEDIUM   | Material contained risk  | Track and plan            |
| LOW      | Limited contextual risk  | Proportionate improvement |

Derive these bands from the impact/likelihood matrix in `synthesis/risk-register.md`.

Print one line of clarification under the severity table in every report:
severity derives from the impact/likelihood matrix, not CVSS.

Do not assign a fixed likelihood to each severity band or confuse CVSS with this matrix.

Use `UNKNOWN` for an unsupported rating and list unrated risks separately from the risk map.

When the report language is not English, apply the column header and severity description
translations from the matching `translations/` file.

Use these definitions consistently across the Detailed Technical Findings and the Unified Risk
Register.

## Scoring Rubrics

Present the scoring framework after Auditing Methodology and before detailed finding assessments.

Apply `process/readiness-and-scoring.md` for deterministic status-to-score mapping, confidence,
score caps, maturity, readiness gates, and multi-project aggregation.

The earlier dashboard summarizes these scores and should reference this rubric.

**Scoring rubric**

Present the rubric matrix that defines what constitutes each score band.

Use the default `1-10` scale unless the user requested `1-5`, `1-3`, `5 stars`, or `3 stars`.

For the `1-10` scale:

| Band      | Score Range | Definition                                                   |
|-----------|-------------|--------------------------------------------------------------|
| Excellent | 9-10        | Capability is comprehensive and verified by strong evidence  |
| Good      | 7-8         | Capability is solid overall, minor or noticeable gaps exist  |
| Average   | 4-6         | Capability is present but uneven, limited, or inconsistent   |
| Poor      | 1-3         | Capability is minimal, fragmentary, or absent where required |

When the report language is not English, apply the band name and definition translations from
the matching `translations/` file.

For the `1-5` and `5 stars` scales:

| Band      | Score Range | Definition                                                  |
|-----------|-------------|-------------------------------------------------------------|
| Excellent | 5           | Capability is comprehensive and verified by strong evidence |
| Good      | 4           | Capability is solid with minor gaps                         |
| Average   | 3           | Capability is adequate but uneven                           |
| Poor      | 2           | Capability is minimal or fragmentary where required         |
| Bad       | 1           | Capability is absent or negligible where required           |

For the `1-3` and `3 stars` scales:

| Band      | Score | Definition                                                  |
|-----------|-------|-------------------------------------------------------------|
| Excellent | 3     | Capability is comprehensive and verified by strong evidence |
| Average   | 2     | Capability is adequate but uneven                           |
| Poor      | 1     | Capability is minimal, limited, or absent where required    |

When the report language is not English, apply the same band translations from the matching
`translations/` file.

For `5 stars`, render each score as a five-position star bar using `★` for filled positions and `☆`
for empty positions, such as `★★★☆☆` for `3`.

For `3 stars`, use three positions, such as `★★☆` for `2`.

Render `UNKNOWN` and `N/A` as text, not as star bars.

**Zero is not a score.** The value `0` is reserved and never used.

When a dimension cannot apply, mark it `N/A`.

Apply the ISO/IEC 25010:2023 crosswalk in `synthesis/project-scorecard.md` and show coverage gaps.

For every numeric or star score, include evidence references and confidence in its supporting
paragraph.

If an overall score is shown, disclose its formula, weights, rounding, and coverage denominator.
State the lowest-scoring applicable dimension and its score in a paragraph below the table, per
`synthesis/project-scorecard.md`.
