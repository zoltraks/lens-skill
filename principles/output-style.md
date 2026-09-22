# Output Style

## Purpose

> **Scope:** Output style, terminology, status and severity vocabularies, consistency rules
> **Key items:** precise structured prose, tables over paragraphs, fixed vocabularies, repeatable
> output

This file defines how the audit report should read.

It complements `principles/evaluation-rules.md`, which defines what may be said.

The goal is consistency. Two audits of similar systems should produce reports of similar shape,
vocabulary, and rigor.

## Tone And Register

Be precise, structured, and neutral.

Use technical terminology accurately and consistently.

Avoid ambiguity. Prefer a marked gap over a vague hedge.

Avoid emotional, judgmental, or marketing language.

Write about the system, not the author.

## Structure Preferences

Use a hybrid table-paragraph format throughout the report.

Tables provide scannable summaries. Paragraphs below tables provide detailed evidence, reasoning,
and context. This keeps the report readable in plain-text consoles while preserving depth.

In tables, use shortened, general values. One to three words per cell. Do not crowd table cells with
long explanations.

Apply the table formatting rules defined in `process/report-format.md` (Table Formatting Rules
section) to every table in the report: compact column widths, trailing-space padding on every cell,
and hyphens contiguous with pipes in the separator row.

In paragraphs, use short sentences separated by blank lines. Each sentence should stand on its own
line, with an empty line between consecutive sentences. Anchor every claim to a concrete fact: a
file path, a config key, a command, or a direct quote.

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

Use `N/A` only under the contextual-applicability rule in `principles/evaluation-rules.md`, always
with a one-line justification.

Missing-information tokens:

- `UNKNOWN`
- `NOT SPECIFIED`
- `INSUFFICIENT INFORMATION`

Severity values:

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

Use `UNKNOWN` for a missing severity rating, not as a new severity band.

Evidence basis labels are Inspected, Reported, and Inferred. The audit never executes checks,
externally produced results are `Reported`.

Confidence uses `HIGH`, `MEDIUM`, and `LOW`, separately from severity.

Ledger execution states produced by the audit are `NOT RUN` for documented checks that were not
executed and `N/A` for source observations, separately from category status or scanner
findings.

Validation Record results are `Applied`, `PASS`, or `N/A`, separately from category status. An
`N/A` always carries a justification.

**Machine tokens**: Keep status markers, validation results, execution states, evidence IDs,
finding IDs, risk IDs, recommendation IDs, debt IDs, CWE IDs, CVSS vectors, OWASP IDs, and tool
commands unchanged in every report language. Translate surrounding labels and explanatory prose,
not the tokens used for comparison or validation.

Maturity levels:

- `Prototype`
- `Early development`
- `Pre-production`
- `Production-ready`
- `Undetermined`

Score scale: integers `1` to `10` by default, with an optional `1` to `5` scale, defined in
`synthesis/project-scorecard.md`. The value `0` is reserved and never used as a score.

## Consistency Rules

Use the same category names and the same order across every audit, as listed in the report format.

Use the same column headers in the risk register and scorecard tables across every audit.

When a category cannot apply to the system's deployment model, keep the section and mark it `N/A`
with a one-line justification, rather than silently dropping it or marking it `FAIL`. When a
category could apply but no evidence was provided, mark it `UNKNOWN`.

Do not introduce new status or severity words. If a nuance is needed, place it in the notes column,
not in the marker.

## Plain-Text Friendly Formatting

Write short sentences.

Separate distinct statements with line breaks so the report reads well in plain consoles.

Break lines that exceed the selected wrap width - 100 characters by default - at a natural boundary
such as after a comma or clause end, per the Selecting The Wrap Width rule in `STYLE.md`. Do not
break inside inline code, file paths, or URLs.

Do not use the semicolon character in prose. Join closely related clauses with a comma or split them
into separate sentences. The prose scope includes sentences, headings, table cells, and list items,
only code blocks, inline code, and file paths are exempt.

Prefer single-sentence paragraphs. Every sentence in a prose paragraph must be on its own line,
separated from the next sentence by an empty line.

Put exactly one empty line before and after lists of items.

For nested lists, put an empty line between the parent list item and its sublist.

For lists of short sentences, do not use blank lines between list items. For complex lists, use
blank lines.

Avoid numbered lists for non-sequential items. Use bullet points.

When a prose paragraph lists three or more related items, use a bullet list instead of an inline
comma-separated list.

For process or workflow steps, use bold headers separated by empty lines instead of numbered lists.

Keep tables readable as plain text. Align columns by padding every cell value with trailing spaces
so that all `|` column separators in a table align vertically in plain text.

Format every table with an automated script per the Table Formatting Rules in
`process/report-format.md`, do not count column widths by hand.

Keep section names short. Do not put qualifiers in section names using parentheses.

Use headers for section titles rather than bold runs of text.

Put exactly one empty line after every markdown header (`#`, `##`, `###`) before the first content
line.

Do not use `####` or deeper headings in the report.

In English, use "Title Case" in section and chapter names.

Use standard ASCII double quotes rather than typographic quotes.

Prefer ASCII characters for normal text.

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs. Do not
use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

Use ASCII `->` for arrows in prose, do not use `→` or other typographic arrows outside code
blocks.

Box-drawing characters like "│", "├", "└" are allowed in code blocks for directory trees and simple
diagrams. If a diagram already uses box-drawing characters, keep them. Do not replace box-drawing
characters with "+", "-", or "`".

Do not leave blank lines as the first or last line inside a fenced code block.

Use a language tag on fenced code blocks that contain code. Leave diagrams, directory trees, console
output, and plain text untagged.

**Hexadecimal and byte values**: Enclose in double backticks (e.g., `` `FF` ``).

**Key terms**: Bold key terms when defining them (e.g., **Term**: Definition).

## Multilingual Output

When the user requests a specific natural language for the report, translate all user-facing prose
into that language.

The default report language is English. When the request language is ambiguous or cannot be
determined, default to English.

**Analysis language**

Analysis runs in English regardless of the report language. Evidence notes, finding drafts,
partial conclusions, and assembled part files are written in English, and the report is rendered
into the report language in a single pass that applies the matching `translation/` file.

Reasoning in English keeps the analysis anchored to the English rules, rubrics, and fixed
vocabularies in this skill, and a single render pass applies one terminology convention to the
whole document.

When the audited project establishes its own terminology in the report language, for example a
project glossary or design documents, prefer those established forms over the translation file's
defaults and record the choice.

Direct quotes, code, configuration keys, file paths, and machine tokens are never translated.

**Translation files**

Translation rules for each supported language live in the `translation/` directory. Each file is
named after the language (for example, `translation/polish-language.md`). When the report language
is not English, load the matching translation file and apply every translation defined there.

To add support for a new language, create a new file in `translation/` following the structure of
the existing files. The file must define translations for status and severity vocabulary, section
headings, table headers, style rules, and any language-specific encoding or diacritics requirements.

**What must be translated:**

- All section headings (e.g., "Technology Stack", "Executive Summary", "Health Dashboard", "Detailed
  Technical Findings")
- All table column headers (e.g., "Layer", "Technology", "Category", "Status", "Risks", "Notes",
  "Dimension", "Score")
- All finding pillar names in the Detailed Technical Findings summary table (e.g., "Architecture &
  Design", "Code Quality", "Security & Compliance", "Infrastructure & CI/CD", "AI Provenance & Code
  Origin", "Copyrights & Originality")
- All dimension names in the Scorecard Summary (e.g., "Testability", "Design Soundness", "Code
  Quality")
- All risk names in the Unified Risk Register
- All recommendation summaries in the Actionable Remediation Roadmap
- All descriptive paragraphs, evidence, reasoning, and justification text
- "Summary description" and observation paragraph headings
- All descriptive fixed values: maturity levels (`Prototype`, `Early development`,
  `Pre-production`, `Production-ready`, `Undetermined`), report state (`Draft`, `Final`), detail
  level, evaluation scale names, readiness states, and audit-purpose values, rendered per the
  matching `translation/` file

**What stays in English (fixed vocabularies):**

- Missing-information tokens: `UNKNOWN`, `NOT SPECIFIED`, `INSUFFICIENT INFORMATION`
- File paths, config keys, commands, code snippets, and direct quotes from the input

**Status, severity, and score format:**

The English markers (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`, `LOW`, `MEDIUM`, `HIGH`,
`CRITICAL`, `Score:`, `SEVERITY:`) are the default. Each translation file defines the equivalents
for its language, which may localize the markers themselves, including execution states such as
`NOT RUN`, `NOT ASSESSED`, and `INSUFFICIENT INFORMATION`. The English forms remain the analysis
and validation vocabulary. The inline format remains identical: the marker follows the bold
heading separated by a space.

**Language-specific style rules:**

Each translation file may override English style rules where the target language requires it. For
example, heading capitalization, gender rules for acronyms, diacritics preservation, and encoding
requirements are defined per language in the translation file.

## Information Security In Output

Never reproduce plaintext secrets, passwords, or cryptographic keys in summaries, observations, risk
descriptions, or recommendation text.

When a finding involves a secret, describe the location and nature of the exposure without quoting
the value. Use `[REDACTED]` as a placeholder or a generic phrase such as "plaintext database
credentials found in tracking file".

The file path and configuration key that contains the secret may still be cited as evidence. Only
the secret value itself is redacted.

## Report Termination

Do not add a closing line such as "End of audit report." or a trailing horizontal rule `---` at the
end of the document.

References is the final section, following the Re-audit And Follow-up Plan when applicable.

End after References without trailing boilerplate.

## Determinism

Given the same input, aim to produce the same findings, statuses, and scores.

Anchor every judgement to a rule in this skill and to evidence in the input, so that the result is
reproducible rather than stylistic.
