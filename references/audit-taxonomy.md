# Audit Type Taxonomy

## Purpose

> **Scope:** Canonical software audit types, the fixed coverage-status vocabulary, and the
> verified source corpus the taxonomy and related methodology draw on
> **Key items:** audit-type table, coverage statuses, source corpus, coverage matrix rules

This file names the audit types a synthesis report distinguishes and defines the fixed status
vocabulary used by the Audit Type Coverage & Assurance Matrix in `process/report-format.md`.
It also registers the external sources the skill's audit-type rules were derived from, so the
report's References section can cite them the same way it cites standards.

Apply `principles/evaluation-rules.md` throughout.

## Status Vocabulary

The Coverage Matrix uses exactly these statuses, and no others:

| Status              | Meaning                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------|
| `Covered`           | The report answers this audit type's core questions within the source-only evidence model |
| `Partially` | Some of this type's dimensions are answered, and the named limits remain explicit         |
| `Not done`     | This is a distinct engagement type the audit deliberately does not run                    |
| `Not Applicable`    | This audit type does not apply to the subject under audit                                 |

`Not done` declares a scope decision about an engagement kind, never a defect of the subject.
`Not Applicable` differs: the type's trigger condition is absent entirely, for example an AI
Governance Audit for a project with no AI dependency.

## Canonical Audit Types

Render the full row set in every report. The default status applies unless the audit's evidence
or the subject justifies a different one, and the Rationale column always states why.

| Report type                                 | Answered by                                                        | Default status    |
|---------------------------------------------|--------------------------------------------------------------------|-------------------|
| Software Architecture Review                | Architectural Assessment, Trade-off Analysis                       | Covered           |
| Code Quality Audit                          | Code Quality pillar findings, Technical Debt Register              | Covered           |
| Security Vulnerability Assessment           | Security pillar findings, Threat Model, CWE mappings               | Covered           |
| Open Source License Compliance Review       | License & IP Compliance Review, SBOM license pass                  | Covered           |
| Penetration Test                            | Nothing equivalent, Exploitability Narratives are theoretical only | Not done          |
| Performance Audit                           | NFR review of stated targets and design, no load measurement       | Partially         |
| Cloud Infrastructure Audit                  | Deployment and IaC inspection, no live environment state           | Partially         |
| AI Governance Audit                         | AI System Assessment when applicable                               | Covered or N/A    |
| Technical Due Diligence                     | Engineering dimensions plus Delivery Practice & Team Continuity    | Partially         |
| SBOM / Software Composition Analysis        | Software Bill of Materials section, manifest-derived               | Covered           |
| Compliance Certification (SOC 2, ISO 27001) | Standards used as scoring rubrics only                             | Not done          |

The AI Governance Audit row takes `Covered` when the AI System Assessment applies per
`assessment/ai-system.md`, and `Not Applicable` otherwise.

## Per-Type Rationale

These defaults keep the matrix honest about what a source-only audit is.

**Software Architecture Review.** Source inspection covers structure, coupling, layering, data
flow, and recorded decisions. The audit cannot validate behavior under real load or organizational
ownership, both of which stay visible in Limitations and Unknowns.

**Code Quality Audit.** The report reviews code by inspection and reasons about complexity,
duplication, and standards adherence. No metric tooling runs, so figures such as cyclomatic
complexity appear only when committed reports supply them, labeled `Reported`.

**Security Vulnerability Assessment.** Manual source review plus threat modeling maps to the
SAST-equivalent tier of a vulnerability assessment. No scanner executes, and CWE-to-analyzer
mappings from `references/cwe-analyzer-map.md` name checks that would run, not checks that ran.

**Open Source License Compliance Review.** License inspection over manifests, notices, and
vendored code answers the core license-compliance question. Undeterminable dependency licenses are
recorded as `Unknown` and assessed as a gap, per `references/license-compliance.md`.

**Penetration Test.** A penetration test validates exploitability against a running target.
Source-only audits never execute the subject, so this row is always `Not done` unless the
engagement scope explicitly lifts the no-execution constraint. Exploitability Narratives carry the
attack-path reasoning habit at `Theoretical` confidence only.

**Performance Audit.** Stated performance targets, NFR evidence, and design-level scalability are
reviewable in source. Throughput, latency, and resource consumption are not measurable without
execution, so the row stays `Partially`.

**Cloud Infrastructure Audit.** Committed IaC, deployment configuration, and pipeline files are
inspectable. Live console state, IAM effective permissions, and runtime configuration drift are
not, keeping the row `Partially`.

**AI Governance Audit.** The conditional AI System Assessment covers model, data, and risk-control
evidence present in source. Certification-grade governance review remains outside scope.

**Technical Due Diligence.** The report covers the engineering pillars of a due diligence
engagement: architecture, code, security, licensing, and delivery-practice proxies. Interviews,
team assessment, business fit, and commercial analysis are not performed, so the row stays
`Partially`.

**SBOM / Software Composition Analysis.** The manifest-derived inventory answers the inventory
question. It is not a shipped-artifact SBOM and performs no advisory-database lookups, per
`references/sbom-schema.md`.

**Compliance Certification.** Standards such as SOC 2, ISO 27001, and PCI-DSS are used as scoring
rubrics and coverage checklists. The report makes no conformance or certification claim.

## Consistency Rules

- The matrix rows are fixed. Do not add, drop, or rename rows inside a report.
- A status other than the default carries a one-line justification in the Rationale column.
- The matrix must agree with Scope Exclusions: no `Covered` row may be disclaimed later, and no
  exclusion may contradict a `Covered` status. PAR-11 enforces this.
- `Not done` rows reference the corresponding exclusion bullet in Scope Exclusions.
- In a multi-project report the matrix appears once, before the Project Inventory, and statuses
  reflect the engagement as a whole. Per-project differences go in the Rationale column.

## Source Corpus

These are the external sources the taxonomy, the coverage model, and the borrowed report
structures derive from. Cite an entry in the report's References section only when its
methodology was actually applied, per `process/report-format.md`.

| Source                                                             | Publisher       | What it grounds                                                                 |
|--------------------------------------------------------------------|-----------------|---------------------------------------------------------------------------------|
| Software Audit Services: What They Cover and When You Need One     | Netguru         | The canonical audit-type taxonomy and remediation-roadmap sequencing            |
| What You Really Get From a Software Audit and When It Matters Most | Okoone (Spark)  | Cross-check of the audit-type taxonomy and per-type purpose statements          |
| Code Auditing                                                      | Wiz Academy     | Code-audit vs penetration-test timing and method distinction                    |
| Penetration Testing Report guides                                  | Simpa Labs      | Pentest report structure: executive summary, scope, findings, remediation       |
| PentestReports.com report collection                               | PentestReports  | Real-world pentest report conventions for the Exploitability Narrative          |
| Code Quality Audit service page                                    | FossID          | Code-quality metric set: cyclomatic complexity, maintainability index, Halstead |
| SBOM Reports: What to Include and How to Use Them                  | Kiuwan          | SBOM definition and field expectations for the SBOM section                     |
| What's in a Technical Due Diligence Report                         | Made with Love  | Observations-vs-concerns discipline and key-person risk framing                 |
| Technical Due Diligence in 2026                                    | Papermark       | The nine-area TDD scope and delivery-practice measurement                       |
| Technical Audit & Due Diligence                                    | Orange & Bronze | Code, architecture, security, and process audits as a bundled engagement        |
| M&A Software Due Diligence                                         | Black Duck      | Combined architecture, quality, and open-source audit precedent                 |
| What Is a Code Audit                                               | reinteractive   | Code-audit practice and CISQ cost-of-poor-quality context                       |
| 2026 Minimum Elements for a Software Bill of Materials             | CISA et al.     | SBOM completeness touchstone, including the Component License element           |
| Cost of Poor Software Quality in the US, 2022 report               | CISQ            | Macro-context figures only, never a scoring input                               |
| DORA software delivery performance metrics                         | DORA (dora.dev) | The five-metric delivery model behind Delivery Practice & Team Continuity       |

The corpus lists methodology sources, not scoring inputs. Prefer primary standards for report
citations per `references/stack-standards.md`, while these entries ground the report's structure
and terminology choices.
