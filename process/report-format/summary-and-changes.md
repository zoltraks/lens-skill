# Summary And Changes

## Purpose

> **Scope:** Executive summary and the previous-audit comparison block
> **Key items:** readiness threshold, changes since previous audit

## Executive Summary

Provide a compact overview a reader can absorb without the detail sections.

Precede the table with a one-line legend naming the band for each score range of the selected
scale, so no score appears before its band is defined:

- `1-10`: `1-3 Poor · 4-6 Average · 7-8 Good · 9-10 Excellent`
- `1-5`: `1 Bad · 2 Poor · 3 Average · 4 Good · 5 Excellent`
- `1-3`: `1 Poor · 2 Average · 3 Excellent`
- `5 stars`: `★ Bad · ★★ Poor · ★★★ Average · ★★★★ Good · ★★★★★ Excellent`
- `3 stars`: `★ Poor · ★★ Average · ★★★ Excellent`

Use a key-value table:

| Field          | Value                                                 |
|----------------|-------------------------------------------------------|
| System type    | <prototype / codebase / production system / proposal> |
| Scope          | <what was reviewed and what was excluded>             |
| Source basis   | <running system / inspected code / description>       |
| Maturity level | <maturity level>                                      |
| Overall score  | <score display>                                       |

Maturity level is one of: `Prototype`, `Early development`, `Pre-production`, `Production-ready`,
or `Undetermined`.

When the report language is not English,
the value is rendered per the matching `translations/` file.

For numeric scales, use `<mean>/<scale> (<band>)` and `<score>/<scale>`.

For `5 stars` or `3 stars`, use the rounded star bar followed by the exact mean in parentheses,
for example `★★★☆☆ (3.4/5)`.

The Overall score cell holds only the score display.

The lowest-scoring applicable dimension and its score go in a paragraph directly below the table,
so a weak pillar is never hidden inside the average,
for example `Lowest-scoring dimensions: Security ★★☆☆☆.` Exclude `N/A` and `UNKNOWN` dimensions from
both values.

When several dimensions tie for the lowest score, name them all.

Omit the row and the paragraph only when no dimensions were scored.

When the report language is not English, apply the table header and field name translations from the
matching `translations/` file.

Do not add a "Summary description" row to this table.

Long descriptive text in a table cell makes the table unreadable in plain text.

The summary description belongs in a paragraph after the table, as described below.

**Summary description**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Write one paragraph immediately after the table.

State the system's purpose in one sentence.

Summarize the overall condition in one sentence.

Note the maturity level and anchor it to evidence from later sections.

Mention any critical finding that the reader should know first.

Keep the paragraph to four sentences maximum.

Break lines that exceed the selected wrap width (default 100) per `STYLE.md`.

The maturity level must be justified by evidence in later sections, not asserted.

**Coverage and risk flags**

Point the reader at the Audit Type Coverage & Assurance Matrix in one line,
naming only the statuses that matter for reading the report,
for example "This report covers the engineering audit types.

No penetration test or compliance certification was performed".

Flag a `High` contributor-concentration rating from Delivery Practice & Team Continuity and any
`Conflict` license risk from License & IP Compliance Review here, one line each,
since both are material deal-level facts a summary reader should not have to dig for.

Omit a flag line when it does not apply.

**Production Readiness Threshold**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

State the conditions and evidence required to justify `Production-ready` for the stated deployment.

Tie conditions to risk IDs and required verification, without inventing numeric coverage thresholds.

Distinguish adopted acceptance criteria from proposed improvements and identify who must confirm
unapproved criteria.

For readiness or due diligence, add an **Evidence And Decision Limits** paragraph stating which
required checks are documented, which were not run, critical uncertainties, and sign-off state.

Keep any "builds", "tests pass", "secure", or "production-ready" claim within the evidence actually
collected, carrying the same qualifications as the detailed findings.

Add **Readiness Cost** using `synthesis/remediation-roadmap.md`, with the supported range or
`INSUFFICIENT INFORMATION`, known subtotal, exclusions, and unestimated work.

For due diligence, summarize support continuity, ownership cost, roadmap, supplier, IP, and data
obligations, including missing business evidence.

Proposed targets and gates are not stakeholder-approved requirements until confirmed.

Incomplete required checks or unassigned verification ownership leave sign-off pending, regardless
of the scorecard average.

## Changes Since Previous Audit

Include this section only when a previously created audit report was found during intake and
confirmed as the re-audit baseline, per `synthesis/report-comparison.md`.

Omit it entirely for a first audit or a fresh audit.

Both are normal cases, so no omission note is needed in Scope Exclusions.

Open with a report reference table:

| Field            | Previous Report | Current Report |
|------------------|-----------------|----------------|
| File             | <path>          | <filename>     |
| Revision         | <revision>      | <revision>     |
| Date             | <date>          | <date>         |
| Detail level     | <level>         | <level>        |
| Evaluation scale | <scale>         | <scale>        |

When the previous report records no revision, show `1.0 (assumed)` in the Revision row.

When parameters differ between reports, state the difference in a paragraph below the table
before comparing content, since a scale or detail-level change affects comparability.

When the report language is not English, apply the column header translations from the matching
`translations/` file.

**Finding transitions**

Present a table of findings that changed remediation state or first appeared since the
previous report:

| Finding | Previous | Current | Note               |
|---------|----------|---------|--------------------|
| FND-XXX | Open     | Closed  | <closing evidence> |
| FND-XXX | Open     | Open    | still reproduces   |
| FND-XXX | -        | New     | first reported     |

A previous finding that no longer reproduces stays in the table as `Closed` with the evidence
that closes it, it is never silently dropped.

**Score delta**

Present a per-dimension score comparison:

| Dimension | Previous | Current | Direction |
|-----------|----------|---------|-----------|
| <name>    | <score>  | <score> | Up        |

Direction uses `Up`, `Down`, or `Unchanged`.

When the evaluation scale changed between reports,
mark the direction `UNKNOWN` for affected dimensions instead of comparing raw numbers.

After the tables, write one paragraph per material change.

Summarize which findings moved state, which `RSK-XXX` risks were added or mitigated,
and which category statuses changed.

Anchor every claim to a `FND-XXX`, `RSK-XXX`, or `EVD-XXX` in the current report.

**Rules**

- New findings keep their assigned `FND-XXX` IDs and appear as `New` in the transition table.
- Mark a comparison element `UNKNOWN` when the previous report cannot supply it, do not guess.
- For multi-project reports, place this section inside each project block and qualify every
  identifier with the project identifier.
- Do not include plaintext secrets, passwords, or cryptographic keys in comparison text.
