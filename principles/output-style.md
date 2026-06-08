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

Score scale: integers `1` to `10` by default, with an optional `1` to `5` scale, defined in `synthesis/scorecard.md`. The value `0` is reserved and never used as a score.

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

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs. Do not use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

Box-drawing characters like "│", "├", "└" are allowed in code blocks for directory trees and simple diagrams. If a diagram already uses box-drawing characters, keep them. Do not replace box-drawing characters with "+", "-", or "`".

Do not leave blank lines as the first or last line inside a fenced code block.

**Hexadecimal and byte values**: Enclose in backticks (e.g., `` `FF` ``).

**Key terms**: Bold key terms when defining them (e.g., **Term**: Definition).

## Multilingual Output

When the user requests a specific natural language for the report, translate all user-facing prose into that language.

**What must be translated:**

- All section headings (e.g., "Technology Stack", "Executive Summary", "Health Dashboard", "Detailed Technical Findings")
- All table column headers (e.g., "Layer", "Technology", "Category", "Status", "Risks", "Notes", "Dimension", "Score")
- All finding pillar names in the Detailed Technical Findings summary table (e.g., "Architecture & Design", "Code Quality", "Security & Compliance", "Infrastructure & CI/CD", "AI Provenance & Code Origin", "Copyrights & Originality")
- All dimension names in the Scorecard Summary (e.g., "Testability", "Design Soundness", "Code Quality")
- All risk names in the Unified Risk Register
- All recommendation summaries in the Actionable Remediation Roadmap
- All descriptive paragraphs, evidence, reasoning, and justification text
- "Summary description" and observation paragraph headings

**What stays in English (fixed vocabularies):**

- Maturity levels: `Prototype`, `Early development`, `Pre-production`, `Production-ready`, `Undetermined`
- Score format: `Score: X/10` in English, `Wynik: X/10` in Polish. When the 1-5 scale is selected, use `Score: X/5` and `Wynik: X/5`.
- Missing-information tokens: `UNKNOWN`, `NOT SPECIFIED`, `INSUFFICIENT INFORMATION`
- File paths, config keys, commands, code snippets, and direct quotes from the input

**Status and severity translations by language:**

When the report language is Polish, use these Polish equivalents instead of the English markers:

| English | Polish |
|---------|--------|
| `PASS` | `OK` |
| `PARTIAL` | `CZĘŚCIOWO` |
| `FAIL` | `NIEZALICZONE` |
| `UNKNOWN` | `NIEZNANE` |
| `N/A` | `ND` |
| `LOW` | `NISKIE` |
| `MEDIUM` | `ŚREDNIE` |
| `HIGH` | `WYSOKIE` |
| `CRITICAL` | `KRYTYCZNE` |
| `SEVERITY:` | `WAŻNOŚĆ:` |
| `Score:` | `Wynik:` |

The inline format remains identical: the marker follows the bold heading separated by a space. For example, `**Strategia wdrożenia** CZĘŚCIOWO` or `**Testowalność** Wynik: 8/10`.

**Language-specific style rules:**

- In English, use "Title Case" in section and chapter names.
- In Polish, do not use "Title Case" in section and chapter names; use sentence case.
- In Polish, use "Przykład zawartości" instead of "Content Example".
- In Polish, use Polish equivalents for standard headings and table headers:
  - "Informacje o dokumencie" for "Document Information"
  - "Stos technologiczny" for "Technology Stack"
  - "Podsumowanie wykonawcze" for "Executive Summary"
  - "Panel zdrowia" for "Health Dashboard"
  - "Kluczowe obserwacje" for "High-Level Observations"
  - "Metodologia audytu" for "Auditing Methodology"
  - "Skale oceny" for "Scoring Rubrics"
  - "Kontekst systemu" for "System Context"
  - "Ocena architektury" for "Architectural Assessment"
  - "Mocne strony i co działa" for "Strengths & What's Working"
  - "Szczegółowe wyniki techniczne" for "Detailed Technical Findings"
  - "Jednolity rejestr ryzyk" for "Unified Risk Register"
  - "Analiza kompromisów" for "Trade-off Analysis"
  - "Plan działania i mapa naprawcza" for "Actionable Remediation Roadmap"
  - "Wyłączenia z zakresu" for "Scope Exclusions"
  - "Zależności" for "Dependency Health" (scorecard dimension)
  - "Poprawność projektowa" for "Design Soundness" (scorecard dimension)
  - "Pochodzenie AI" for "AI Provenance" (scorecard dimension)
  - "Oryginalność i licencjonowanie" for "Originality & Licensing" (scorecard dimension)
  - "Obszar" for "Field" (Executive Summary table header)
  - "Wartość" for "Value" (Executive Summary table header)
  - "Wymiar" for "Dimension" (Project Scorecard table header)
  - "Wynik" for "Score" (Project Scorecard table header)
- In Polish, use neuter gender for acronyms treated as nouns: "czyste PWA" (not "czysta PWA"), "czyste SPA" (not "czysta SPA").

## Information Security In Output

Never reproduce plaintext secrets, passwords, or cryptographic keys in summaries, observations, risk descriptions, or recommendation text.

When a finding involves a secret, describe the location and nature of the exposure without quoting the value. Use `[REDACTED]` as a placeholder or a generic phrase such as "plaintext database credentials found in tracking file".

The file path and configuration key that contains the secret may still be cited as evidence. Only the secret value itself is redacted.

## Report Termination

Do not add a closing line such as "End of audit report." or a trailing horizontal rule `---` at the end of the document. The Scope Exclusions section is the final section; end the report after it without any trailing boilerplate.

## Determinism

Given the same input, aim to produce the same findings, statuses, and scores.

Anchor every judgement to a rule in this skill and to evidence in the input, so that the result is reproducible rather than stylistic.
