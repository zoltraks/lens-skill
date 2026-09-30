# Quality Models Baseline

## Purpose

> **Scope:** Vocabulary anchors for quality characteristics, technical debt, and test/review
> practice
> **Key items:** ISO 25010 characteristic map, ISO 19011 scope, CISQ/SQALE debt vocabulary,
> test pyramid, review-practice expectations

This file distills the ISO portal pages, CISQ, SQALE, test-pyramid, and review-practice
sources listed in `references/source-catalog.md` into the vocabulary an audit uses for quality
findings.

Snapshot date: 2026-09-30.

ISO standards are paywalled: only the public characteristic names are distilled here. Clause
text is never reproduced.

Feeds `assessment/code-quality.md`, `assessment/maintainability-review.md`, and
`synthesis/project-scorecard.md`.

## ISO/IEC 25010

From https://iso25000.com/index.php/en/iso-25000-standards/iso-25010 (public map) and
https://www.iso.org/standard/78176.html (paywalled standard page).

- The product-quality model has nine characteristics: Functional Suitability, Performance
  Efficiency, Compatibility, Interaction Capability (formerly Usability), Reliability,
  Security, Maintainability, Flexibility (formerly Portability), and Safety (added in the
  2023 revision).
- The model names the quality axes. It does not prescribe measurement - the report's pillar
  names map to these characteristics but the scores stay Lens's own rubric.
- Sub-characteristics (for example Maintainability > Modularity, Reusability, Analysability,
  Modifiability, Testability) give findings their vocabulary.

## ISO 19011 And Audit Vocabulary

From https://www.iso.org/standard/70017.html (paywalled - scope citation only).

- ISO 19011 governs management-system audit programs. Lens borrows only the audit-cycle
  vocabulary (criteria, evidence, finding, conclusion), not its conformance requirements.

## CISQ And Technical Debt

From https://www.it-cisq.org/ and
https://www.it-cisq.org/standards/code-quality-standards/. SQALE terms from
http://www.sqale.org/ and the restricted Cutter summary.

- CISQ maintains the OMG-adopted code-quality standards (ASCQM measures covering
  Reliability, Security, Performance Efficiency, Maintainability) - the debt-register pillar
  names map to these.
- SQALE supplies the remediation vocabulary: remediation cost (effort to fix),
  non-remediation cost (ongoing burden), quality index, and the remediation-order classes
  (reliability before testability, and so on).
- `synthesis/debt-register.md` owns the `TDR-` inventory. These sources provide only the
  vocabulary anchors.

## Test Pyramid And Review Practice

From https://martinfowler.com/articles/practical-test-pyramid.html and
https://google.github.io/eng-practices/.

- The pyramid orders tests by scope and count: many unit tests, fewer service/integration
  tests, minimal end-to-end tests. An inverted pyramid (mostly e2e) is a test-strategy
  observation.
- Test quality signals: tests assert behavior not implementation, run fast, and are
  independent. Flaky-test budgets and `xtest`/`it.skip` counts are census items.
- Google eng-practices anchors review expectations: reviews are small, descriptive,
  approved-labeled, and scoped. A repository with no review trail and claims of review
  practice is a docs-to-code drift finding.

## Live Check

When web fetch is available, confirm the ISO 25010 characteristic names against iso25000.com
and note edition drift.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
