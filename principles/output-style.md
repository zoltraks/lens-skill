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

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

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

Put exactly one empty line between sentences in a paragraph for readability in simple consoles or text viewers.

Put exactly one empty line before and after lists of items.

For nested lists, put an empty line between the parent list item and its sublist.

For lists of short sentences, do not use blank lines between list items. For complex lists, use blank lines.

Avoid numbered lists for non-sequential items. Use bullet points.

For process or workflow steps, use bold headers separated by empty lines instead of numbered lists.

Keep tables readable as plain text and align columns by padding cell values.

Keep section names short. Do not put qualifiers in section names using parentheses.

Use headers for section titles rather than bold runs of text.

In English, use "Title Case" in section and chapter names.

Use standard ASCII double quotes rather than typographic quotes.

Prefer ASCII characters for normal text.

Box-drawing characters like "│", "├", "└" are allowed in code blocks for directory trees and simple diagrams. If a diagram already uses box-drawing characters, keep them. Do not replace box-drawing characters with "+", "-", or "`".

Do not leave blank lines as the first or last line inside a fenced code block.

**Hexadecimal and byte values**: Enclose in backticks (e.g., `` `FF` ``).

**Key terms**: Bold key terms when defining them (e.g., **Term**: Definition).

## Multilingual Output

When the user requests a specific natural language for the report, translate all user-facing prose into that language.

**What must be translated:**

- All section headings (e.g., "Technology Stack", "Executive Summary", "Quality Assessment")
- All table column headers (e.g., "Layer", "Technology", "Category", "Status", "Risks", "Notes", "Dimension", "Score")
- All category names in the Quality Assessment summary table and detailed paragraphs (e.g., "Testing and Testability", "Design Principles", "Code Quality")
- All dimension names in the Project Scorecard (e.g., "Testability", "Design Soundness", "Code Quality")
- All risk names in the Risk Register
- All trade-off names in the Trade-off Analysis
- All recommendation option summaries
- All descriptive paragraphs, evidence, reasoning, and justification text
- "Summary description" and observation paragraph headings

**What stays in English (fixed vocabularies):**

- Status markers: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`
- Severity values: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Maturity levels: `Prototype`, `Early development`, `Pre-production`, `Production-ready`, `Undetermined`
- Score format: `Score: X/5` (the word "Score" is part of the fixed format)
- Missing-information tokens: `UNKNOWN`, `NOT SPECIFIED`, `INSUFFICIENT INFORMATION`
- File paths, config keys, commands, code snippets, and direct quotes from the input
- The `SEVERITY:` prefix in risk register paragraphs

**Language-specific style rules:**

- In English, use "Title Case" in section and chapter names.
- In Polish, do not use "Title Case" in section and chapter names; use sentence case.
- In Polish, use "Przykład zawartości" instead of "Content Example".
- In Polish, use Polish equivalents for standard headings:
  - "Stos technologiczny" for "Technology Stack"
  - "Podsumowanie wykonawcze" for "Executive Summary"
  - "Kluczowe obserwacje" for "High-Level Observations"
  - "Kontekst systemu" for "System Context"
  - "Ocena jakości" for "Quality Assessment"
  - "Analiza ryzyk" for "Risk Register"
  - "Ocena projektu" for "Project Scorecard"
  - "Analiza kompromisów" for "Trade-off Analysis"
  - "Podsumowanie końcowe" for "Recommendation Summary"
  - "Zależności" for "Dependency Health" (scorecard dimension)
  - "Poprawność projektowa" for "Design Soundness" (scorecard dimension)

## Determinism

Given the same input, aim to produce the same findings, statuses, and scores.

Anchor every judgement to a rule in this skill and to evidence in the input, so that the result is reproducible rather than stylistic.
