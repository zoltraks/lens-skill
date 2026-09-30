# Markdown And Documentation Baseline

## Purpose

> **Scope:** Checkable anchors for Markdown conformance and documentation architecture
> **Key items:** CommonMark conformance surface, Diataxis documentation quadrants, prose
> format contracts

This file distills the CommonMark spec and Diataxis sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/documentation-review.md` and the style surface of `docs/STYLE.md`-governed docs.

## CommonMark

From https://spec.commonmark.org/0.31.2/ (version pinned for stability).

- CommonMark defines the conforming subset: ATX/Setext headings, fenced/indented code,
  lists, links, images, tables are NOT core (GFM extension).
- Heading depth and blank-line discipline the report validator enforces
  (`#`/`##`/`###`, one blank after) are Lens's own contract - CommonMark accepts more, the
  contract is stricter on purpose.
- Tables, footnotes, strikethrough, and task lists are GFM or platform extensions. A doc
  relying on them declares a renderer assumption.
- Reference-style links and inline links both conform. `](/)`-style bare brackets and
  unclosed emphasis markers are the common defects.
- Fence info strings are free-form. Non-alphanumeric info strings may not render per
  renderer.

## Diataxis

From https://diataxis.fr/.

- Diataxis splits documentation into four quadrants: Tutorials (learning), How-to guides
  (tasks), Reference (facts), Explanation (context) - a doc set missing one quadrant has a
  documented gap.
- Reference docs describe, how-tos guide, tutorials teach, explanations clarify. A README
  trying to be all four usually fails the how-to side.
- The audit checks *presence and separation* of the forms in a doc corpus, not compliance
  with Diataxis as a doctrine - it is a lens for coverage, not a score.

## Report Contract Recap

- `docs/STYLE.md` owns the prose rules for shipped skill docs: UTF-8/LF, H1 + Purpose, one
  sentence per paragraph, no H4+, `## Contents` over 300 lines.
- `process/report-format.md` owns the report's own stricter contract. `lint-prose.py`
  enforces the prose subset mechanically.

## Live Check

When web fetch is available, spot-check the CommonMark spec version and the Diataxis quadrant
names.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
