# Delivery Metrics Baseline

## Purpose

> **Scope:** Vocabulary and proxy rules for delivery-performance and reliability metrics
> **Key items:** DORA five metrics, capability catalog, SLO/SLI definitions, SSDF
> verification-loop tasks

This file distills the DORA, Google SRE, and NIST SSDF sources listed in
`references/source-catalog.md` into the anchors the Health Dashboard and delivery-practice
assessments use.

Snapshot date: 2026-09-30.

Feeds `references/delivery-practice.md`, `process/readiness-scoring.md`, and
`assessment/deployment-review.md`.

## DORA Metrics

From https://dora.dev/, https://dora.dev/capabilities/, and
https://dora.dev/guides/dora-metrics-four-keys/.

- The five metrics: Deployment Frequency, Lead Time for Changes, Change Failure Rate,
  Failed Deployment Recovery Time (MTTR), and Reliability (added to the canonical set).
- Source-only audits cannot observe the metrics. `references/delivery-practice.md` defines
  the labeled proxies (release cadence from tags/changelog, merge-to-deploy path, rollback
  mechanism presence, incident evidence).
- When neither tags, release artifacts, nor telemetry exist, all five metrics read
  `NOT SPECIFIED` - the shorthand the report-format spec now states.
- The capabilities catalog links each metric to practices (CI, loosely-coupled architecture,
  trunk-based development). Audit findings cite the capability gap, not the metric itself.

## SLO And SLI

From https://sre.google/sre-book/service-level-objectives/.

- SLI is the measured indicator (for example successful-request ratio), SLO is the target
  bound over a window, SLA is the contractual consequence-bearing form.
- Source-only evidence can verify a *declared* SLO (documented target, error-budget policy)
  but never its attainment - attainment claims are `Reported` evidence at best.
- Error budget = 1 - SLO. A documented budget burn policy is the operability signal.

## NIST SSDF

From https://csrc.nist.gov/pubs/sp/800/218/final (SP 800-218, public domain).

- SSDF organizes secure development into four groups: Prepare the Organization (PO), Protect
  the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV).
- Checkable task anchors: PO.1 security requirements, PS.2 toolchain hygiene, PS.3 artifact
  integrity, PW.4 reuse reviewed components, PW.5 secure defaults, PW.7 code review,
  PW.8 test/verify executable code, RV.1 vulnerability intake (security contact),
  RV.2 root-cause analysis.
- A repository cannot prove PW.8 execution. The audit records whether the *capability*
  (CI running tests, required reviews) exists rather than claiming execution.

## Live Check

When web fetch is available, confirm the current DORA metric names against dora.dev and
spot-check one SSDF task ID against the NIST publication.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
