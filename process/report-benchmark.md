# Report Benchmark

## Purpose

> **Scope:** Comparing a Lens-generated report with an externally produced report of the same
> subject, and converting the methodological delta into skill improvements
>
> **Key items:** revision alignment, claim verification, coverage matrix, findings cross-map,
> gap attribution, adjustment plan, skill application

This file defines the report-benchmark operation: a Lens report and a foreign report -
produced by a prompt, another tool, or a human audit - are verified against the subject,
compared, and their differences attributed so confirmed gaps land in the skill.

Follow it when the request asks to compare audit reports, benchmark a report, or improve
the skill from an external audit - "compare these two audit reports",
"benchmark the lens report against this audit", "improve lens-skill from this comparison".

## When This Applies

The request supplies or names an external report of a subject Lens also reported on -
or asks for the comparison alone, which still runs the verification and gap phases
and delivers the comparison document.

The subject is the audited project - the procedure reads its tree and documents but never
modifies them.

## Procedure

### Intake And Revision Alignment

Locate the Lens report and the external report, and record each report's declared subject
revision and generation parameters.

A revision divergence between the two audited snapshots is recorded first and attributed later -
identical findings at different revisions are never silently merged or silently discounted.

Read the subject's document conventions before writing anything - the comparison document
follows the subject's own report naming and location, never the skill's report contract.

### Tree Verification

Verify every material claim from both reports against the subject tree at each report's
own audited revision where the revision is available.

Classify each claim `verified`, `failed`, or `unverifiable` and record the check that decided -
a claim count or executed-command row that cannot be reproduced is a report defect,
and a command the manifest does not declare is a phantom row, never evidence.

Verification runs read-only commands and file inspection only -
the benchmark never builds, tests, or deploys the subject unless the user commissioned it.

### Comparison

Compare the reports on their own terms before comparing them to the tree.

- Report metadata: subject revision, model or skill version, report style, evidence mode.
- Methodology: verification surface exercised, evidence classes used, claim standards applied.
- Scoring: the scoring model each report used, whether the systems are comparable,
  and how each treated unresolved or unknown evidence.
- Coverage matrix: which declared checks, gates, documents, and surfaces each report exercised.
- Findings cross-map: convergent findings, findings unique to each report,
  and each unique finding's verification status.
- Verdict defensibility: whether each readiness or score verdict follows from its own evidence.

### Gap Attribution

Attribute every material difference to exactly one class before proposing a change:

- **Subject divergence** - the snapshots differ; the difference is not a methodology signal.
- **Report defect** - a phantom command, wrong count, or impossible evidence row in a report.
- **Mechanics gap** - a skill behavior that produced or permitted the weaker result.

Only mechanics gaps feed the adjustment plan - subject divergence is explained,
report defects are listed, and neither becomes a skill edit.

Map each mechanics gap to the owning skill file before proposing it -
a gap that names no file is a topic for `work/` planning, not an edit.

### Deliverable

Deliver the comparison document to the subject's report location per its own conventions.

The document carries the verification results, the coverage and findings maps,
the attribution for each difference, and an adjustment plan naming the owning skill files.

Neither report is rewritten - defects are documented, not repaired.

The adjustment plan proposes changes - it does not apply them.

### Skill Application

Confirmed gaps land only through the skill's own change paths:
a described change under development mode, or the approval gate in
`process/session-review.md` when the request asks to improve the skill from the session.

Structural proposals larger than a single rule edit land as `work/` plans per
`process/session-review.md`, and the anonymized-examples rule applies -
the skill corpus never absorbs the compared subject's names, paths, or identifiers.

## What Does Not Apply

- A comparison against the previous Lens report of the same skill is a re-audit comparison
  under `synthesis/report-comparison.md`, not a benchmark - the benchmark compares
  different provenance, not different revisions.
- The operation never modifies the audited subject and never repairs the compared reports.
- Parameter resolution and report contracts do not apply - no audit runs.
- A benchmark that produces no mechanics gaps still delivers its document and stops -
  it never invents improvements.

## Relation To Maintenance

This file is the external-comparison path inside skill maintenance.

The `Maintain the skill` operation routes here when the request names a report comparison
or benchmark, `process/session-review.md` governs how confirmed findings land,
and `docs/MAINTENANCE.md` governs the edits.
