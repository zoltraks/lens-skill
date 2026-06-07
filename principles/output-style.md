# Output Style

## Purpose

> **Scope:** Output style, terminology, status and severity vocabularies, consistency rules
> **Key items:** precise structured prose, tables over paragraphs, fixed vocabularies, repeatable output

This file defines how the audit report should read. It complements `evaluation-rules.md`, which defines what may be said.

The goal is consistency. Two audits of similar systems should produce reports of similar shape, vocabulary, and rigor.

## Tone And Register

Be precise, structured, and neutral.

Use technical terminology accurately and consistently.

Avoid ambiguity. Prefer a marked gap over a vague hedge.

Avoid emotional, judgmental, or marketing language.

Write about the system, not the author.

## Structure Preferences

Use a hybrid table-paragraph format throughout the report.

Tables provide scannable summaries. Paragraphs below tables provide detailed evidence, reasoning, and context. This keeps the report readable in plain-text consoles while preserving depth.

In tables, use shortened, general values. One to three words per cell. Do not crowd table cells with long explanations.

In paragraphs, use short sentences separated by line breaks. Anchor every claim to a concrete fact: a file path, a config key, a command, or a direct quote.

Use headers for section titles rather than bold runs of text.

Keep each finding self-contained so it can be read out of order.

Lead with the status, then the evidence, then the risk, then neutral notes.

## Fixed Vocabularies

Use only the defined vocabularies so that output stays machine-comparable across audits.

Status values:

- `PASS`
- `PARTIAL`
- `FAIL`
- `UNKNOWN`
- `N/A`

Use `N/A` only under the contextual-applicability rule in `principles/evaluation-rules.md`, always with a one-line justification.

Missing-information tokens:

- `UNKNOWN`
- `NOT SPECIFIED`
- `INSUFFICIENT INFORMATION`

Severity values:

- `Low`
- `Medium`
- `High`
- `Critical`

Maturity levels:

- `Prototype`
- `Early development`
- `Pre-production`
- `Production-ready`
- `Undetermined`

Score scale: integers `0` to `5`, defined in `synthesis/scorecard.md`.

## Consistency Rules

Use the same category names and the same order across every audit, as listed in the report format.

Use the same column headers in the risk register and scorecard tables across every audit.

When a category cannot apply to the system's deployment model, keep the section and mark it `N/A` with a one-line justification, rather than silently dropping it or marking it `FAIL`. When a category could apply but no evidence was provided, mark it `UNKNOWN`.

Do not introduce new status or severity words. If a nuance is needed, place it in the notes column, not in the marker.

## Plain-Text Friendly Formatting

Write short sentences.

Separate distinct statements with line breaks so the report reads well in plain consoles.

Keep tables readable as plain text and align columns by padding cell values.

Use standard ASCII double quotes rather than typographic quotes.

Do not leave blank lines as the first or last line inside a fenced code block.

## Determinism

Given the same input, aim to produce the same findings, statuses, and scores.

Anchor every judgement to a rule in this skill and to evidence in the input, so that the result is reproducible rather than stylistic.
