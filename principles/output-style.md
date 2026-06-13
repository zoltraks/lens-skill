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

In paragraphs, use short sentences separated by blank lines. Each sentence should stand on its own line, with an empty line between consecutive sentences. Anchor every claim to a concrete fact: a file path, a config key, a command, or a direct quote.

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

Prefer single-sentence paragraphs. Every sentence in a prose paragraph must be on its own line, separated from the next sentence by an empty line.

Put exactly one empty line before and after lists of items.

For nested lists, put an empty line between the parent list item and its sublist.

For lists of short sentences, do not use blank lines between list items. For complex lists, use blank lines.

Avoid numbered lists for non-sequential items. Use bullet points.

When a prose paragraph lists three or more related items, use a bullet list instead of an inline comma-separated list.

For process or workflow steps, use bold headers separated by empty lines instead of numbered lists.

Keep tables readable as plain text. Align columns by padding every cell value with trailing spaces so that all `|` column separators in a table align vertically in plain text.

Keep section names short. Do not put qualifiers in section names using parentheses.

Use headers for section titles rather than bold runs of text.

Put exactly one empty line after every markdown header (`#`, `##`, `###`) before the first content line.

In English, use "Title Case" in section and chapter names.

Use standard ASCII double quotes rather than typographic quotes.

Prefer ASCII characters for normal text.

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs. Do not use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

Box-drawing characters like "│", "├", "└" are allowed in code blocks for directory trees and simple diagrams. If a diagram already uses box-drawing characters, keep them. Do not replace box-drawing characters with "+", "-", or "`".

Do not leave blank lines as the first or last line inside a fenced code block.

**Hexadecimal and byte values**: Enclose in double backticks (e.g., `` `FF` ``).

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
  - "Wersja" for "Version" (Document Information label)
  - "Data" for "Date" (Document Information label)
  - "Stan" for "State" (Document Information label)
  - "Poziom szczegółowości" for "Detail Level" (Document Information label)
  - "Stos technologiczny" for "Technology Stack"
  - "Warstwa" for "Layer" (Technology Stack table header)
  - "Technologie" for "Technology" (Technology Stack table header)
  - "Języki" for "Languages" (Technology Stack layer)
  - "Frameworki" for "Frameworks" (Technology Stack layer)
  - "Środowisko uruchomieniowe/Platforma" for "Runtime/Platform" (Technology Stack layer)
  - "Narzędzia budowania" for "Build tooling" (Technology Stack layer)
  - "Narzędzia testowe" for "Test tooling" (Technology Stack layer)
  - "Zarządzanie pakietami" for "Package manager" (Technology Stack layer)
  - "Kluczowe biblioteki" for "Key libraries" (Technology Stack layer)
  - "Magazyny danych" for "Data stores" (Technology Stack layer)
  - "Docelowe platformy" for "Target platforms" (Technology Stack layer)
  - "Podsumowanie wykonawcze" for "Executive Summary"
  - "Obszar" for "Field" (Executive Summary table header)
  - "Wartość" for "Value" (Executive Summary table header)
  - "Typ systemu" for "System type" (Executive Summary field)
  - "Zakres" for "Scope" (Executive Summary field)
  - "Źródło danych" for "Source basis" (Executive Summary field)
  - "Poziom dojrzałości" for "Maturity level" (Executive Summary field)
  - "Opis podsumowujący" for "Summary description" (paragraph heading)
  - "Próg gotowości produkcyjnej" for "Production Readiness Threshold" (paragraph heading)
  - "Panel zdrowia" for "Health Dashboard"
  - "Mapa ciepła ryzyk" for "Risk Heat Map"
  - "Wpływ" for "Impact" (Risk Heat Map axis)
  - "Prawdopodobieństwo" for "Likelihood" (Risk Heat Map axis)
  - "Scorecard - podsumowanie" for "Scorecard Summary"
  - "Wymiar" for "Dimension" (Project Scorecard table header)
  - "Wynik" for "Score" (Project Scorecard table header)
  - "Uwagi" for "Notes" (Project Scorecard table header)
  - "Testowalność" for "Testability" (scorecard dimension)
  - "Jakość kodu" for "Code Quality" (scorecard dimension)
  - "Zgodność ze stosem" for "Stack Alignment" (scorecard dimension)
  - "Zależności" for "Dependency Health" (scorecard dimension)
  - "Utrzymywalność" for "Maintainability" (scorecard dimension)
  - "Wdrażalność" for "Deployability" (scorecard dimension)
  - "Skalowalność" for "Scalability" (scorecard dimension)
  - "Bezpieczeństwo" for "Security" (scorecard dimension)
  - "Zgodność" for "Compliance" (scorecard dimension)
  - "Obserwowalność" for "Observability" (scorecard dimension)
  - "Bezpieczeństwo operacyjne" for "Operational Safety" (scorecard dimension)
  - "Pochodzenie AI" for "AI Provenance" (scorecard dimension)
  - "Oryginalność i licencjonowanie" for "Originality & Licensing" (scorecard dimension)
  - "Kluczowe obserwacje" for "High-Level Observations"
  - "Obserwacja" for "Observation" (High-Level Observations table header)
  - "Metodologia audytu" for "Auditing Methodology"
  - "Przegląd metodologiczny" for "Methodology overview"
  - "Oświadczenie o dowodach" for "Audit evidence statement"
  - "Definicje ważności" for "Severity definitions"
  - "Skale oceny" for "Scoring Rubrics"
  - "Kontekst systemu" for "System Context"
  - "Aspekt" for "Aspect" (System Context table header)
  - "Szczegóły" for "Detail" (System Context table header)
  - "Ocena architektury" for "Architectural Assessment"
  - "Mocne strony i co działa" for "Strengths & What's Working"
  - "Szczegółowe wyniki techniczne" for "Detailed Technical Findings"
  - "Tabela podsumowania" for "Summary table"
  - "Identyfikator" for "Finding ID" (findings summary table header)
  - "Filtr" for "Pillar" (findings summary table header)
  - "Ważność" for "Severity" (findings summary table header)
  - "Tytuł" for "Title" (findings summary table header)
  - "Status" for "Status" (findings summary table header)
  - "Status naprawy" for "Remediation Status" (findings summary table header)
  - "Pliki/Moduły docelowe" for "Target Files/Modules" (finding detail label)
  - "Opis" for "Description" (finding detail label)
  - "Wpływ" for "Impact" (finding detail label)
  - "Rekomendacja naprawcza" for "Remediation Recommendation" (finding detail label)
  - "Metoda weryfikacji" for "Verification Method" (finding detail label)
  - "Jednolity rejestr ryzyk" for "Unified Risk Register"
  - "Identyfikator ryzyka" for "Risk ID" (risk register table header)
  - "Ryzyko" for "Risk" (risk register table header)
  - "Źródło" for "Source Finding" (risk register table header)
  - "Prawdopodobieństwo" for "Likelihood" (risk register table header)
  - "Ograniczenie" for "Mitigation" (risk register table header)
  - "Analiza kompromisów" for "Trade-off Analysis"
  - "Kompromis" for "Trade-off" (trade-off table header)
  - "Kontekst" for "Context" (trade-off table header)
  - "Opcja A: zysk / koszt" for "Option A: gain / cost" (trade-off table header)
  - "Opcja B: zysk / koszt" for "Option B: gain / cost" (trade-off table header)
  - "Dowód" for "Evidence" (trade-off table header)
  - "Implikacja" for "Implication" (trade-off table header)
  - "Plan działania i mapa naprawcza" for "Actionable Remediation Roadmap"
  - "Identyfikator rekomendacji" for "Rec ID" (recommendation table header)
  - "Priorytet" for "Priority" (recommendation table header)
  - "Znalezisko" for "Finding" (recommendation table header)
  - "Rekomendacja" for "Recommendation" (recommendation table header)
  - "Wysiłek" for "Effort" (recommendation table header)
  - "Złożoność" for "Complexity" (recommendation table header)
  - "Weryfikacja" for "Verification" (recommendation table header)
  - "Wyłączenia z zakresu" for "Scope Exclusions"
  - "Zakres" for "Scope" (Scope Exclusions table header)
  - "Uzasadnienie" for "Justification" (Scope Exclusions table header)
- In Polish, use neuter gender for acronyms treated as nouns: "czyste PWA" (not "czysta PWA"), "czyste SPA" (not "czysta SPA").
- When producing a Polish-language report, preserve all Polish diacritics (e.g., "ą", "ę", "ć", "ł", "ń", "ó", "ś", "ź", "ż", "Ą", "Ę", "Ć", "Ł", "Ń", "Ó", "Ś", "Ź", "Ż") in every section, heading, table cell, and paragraph. Do not transliterate or strip diacritics.
- Write Polish-language reports in UTF-8 encoding. Do not use ASCII-only fallback for Polish text.
- The following Polish words are frequently written without diacritics by mistake. Always use the correct form with diacritics:
  - `Poziom dojrzałości` (not `Poziom dojrzalosci`)
  - `Testowalność` (not `Testowalnosc`)
  - `Jakość` (not `Jakosc`)
  - `Jakość kodu` (not `Jakosc kodu`)
  - `Zgodność` (not `Zgodnosc`)
  - `Zgodność ze stosem` (not `Zgodnosc ze stosem`)
  - `Utrzymywalność` (not `Utrzymywalnosc`)
  - `Wdrażalność` (not `Wdrazalnosc`)
  - `Skalowalność` (not `Skalowalnosc`)
  - `Bezpieczeństwo` (not `Bezpieczenstwo`)
  - `Bezpieczeństwo operacyjne` (not `Bezpieczenstwo operacyjne`)
  - `Poprawność projektowa` (not `Poprawnosc projektowa`)
  - `Obserwowalność` (not `Obserwowalnosc`)
  - `Środowisko` (not `Srodowisko`)
  - `Narzędzia` (not `Narzedzia`)
  - `Zarządzanie` (not `Zarzadzanie`)
  - `Wartość` (not `Wartosc`)
  - `Wpływ` (not `Wplyw`)
  - `Prawdopodobieństwo` (not `Prawdopodobienstwo`)
  - `Szczegóły` (not `Szczegoly`)
  - `Przegląd` (not `Przeglad`)
  - `Oświadczenie` (not `Oswiadczenie`)
  - `Założenia` (not `Zalozenia`)
  - `Wysiłek` (not `Wysilek`)
  - `Złożoność` (not `Zlozonosc`)
  - `Oryginalność` (not `Oryginalnosc`)
  - `Wdrażanie` (not `Wdrazanie`)

## Information Security In Output

Never reproduce plaintext secrets, passwords, or cryptographic keys in summaries, observations, risk descriptions, or recommendation text.

When a finding involves a secret, describe the location and nature of the exposure without quoting the value. Use `[REDACTED]` as a placeholder or a generic phrase such as "plaintext database credentials found in tracking file".

The file path and configuration key that contains the secret may still be cited as evidence. Only the secret value itself is redacted.

## Report Termination

Do not add a closing line such as "End of audit report." or a trailing horizontal rule `---` at the end of the document. The Scope Exclusions section is the final section; end the report after it without any trailing boilerplate.

## Determinism

Given the same input, aim to produce the same findings, statuses, and scores.

Anchor every judgement to a rule in this skill and to evidence in the input, so that the result is reproducible rather than stylistic.
