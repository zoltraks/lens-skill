# Report Reformat

## Purpose

> **Scope:** The `reformat report` operation - bring an existing report to the
> current report contract **Key items:** mechanical pass, tool pipeline, manual tail

When a user asks to reformat a report - "reformat AUDIT-x.y", "bring this report to
current format", "apply the current conventions" - run this pipeline rather than
hand-editing. Hand transformation is how stale surfaces survive: every rule below
exists because a manual pass once missed it.

## Pipeline

Run the steps in order against the report file, from the skill root:

1. `python3 scripts/reformat-report.py <report>` - the mechanical pass:
   title to `# <Name> Audit Report`, `## Table of Contents` removal,
   English `Language` row removal, `**Overall score**` bolding, bare `Projects`
   names, Doc Info value capitalization, natural evidence-mode forms,
   `Not collected` line removal, empty Risk Map row removal, and
   `## Evaluation Legend` hoisting in multi-project reports.
   `--check` lists pending changes without writing.
2. `python3 scripts/link-references.py <report>` - re-anchor register links
   after any title or heading change.
3. `python3 scripts/format-table.py <report>` - mechanical table alignment.
4. `python3 scripts/reflow-prose.py --wrap --width 100 [--convert] <report>` -
   width rewrap. Add `--convert` when the source layout is unwrapped.
5. `python3 scripts/validate-report.py <report>` - contract check.

## Manual Tail

Whatever remains after step 5 is a judgment fix, not a script gap:
overlong register titles flagged `NOTE` get terse renames (re-run steps 2-3
after renaming), missing sections get authored per `process/report-format/`,
and stale field vocabularies get rewritten per the owning format file.
Re-run the full pipeline after every manual pass - formatting and links
drift when prose moves.

## Exit Condition

The operation completes only when `validate-report.py` reports zero issues
and a visual pass finds no stale conventions the checker tolerates - the
validator is the floor, not the ceiling.
