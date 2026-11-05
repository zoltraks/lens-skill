# Calibration

## Purpose

> **Scope:** Repeated-audit agreement procedure for scoring policy 3.
> **Key items:** paired independent runs, agreement tolerances, tightening loop, recording.

Scoring reproducibility is tested by running the audit twice on the same subject and
comparing the two canonical models with `scripts/compare-models.py`.

## Paired Runs

- Two independent audits of the same subject, identical parameters - style, detail
  level, scale, evidence mode, catalogue version - in separate sessions.
- The second run never reads the first run's model, report, or notes.
- Both runs freeze `requirements[]` from the same spec documents and use the same
  `scope.history` and `automation_census` determinations - a disagreement there is a
  finding, not noise.

## Tolerances

A pair agrees when both hold:

- Per-dimension point scores differ by at most 1 point on the report's scale.
- `product`, `process`, and `single` scores differ by at most 0.5.

Publish state and flags must also match - a pair where one side reports `Not
published` or a different `single.flag` is out of tolerance regardless of numbers.

## Out Of Tolerance

- Diff the two models with `compare-models.py` and name the criteria levels whose
  divergence produced the breach.
- Tighten the catalogue's level text or method field for those criteria, bump the
  catalogue version, and rerun both audits once.
- A second tightening round requires explicit user approval - the loop does not run
  open-ended.

## Recording

The run notes record per-dimension deltas, headline deltas, publish-state agreement,
and which criteria caused any breach, so the catalogue change traces to evidence.
