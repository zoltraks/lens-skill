# Polish Translation

## Purpose

> **Scope:** Polish rendering of the audit report and parameter prompts: analysis model, status
> and severity vocabulary, fixed vocabulary values, terminology dictionary, prompt phrasing,
> section headings, table headers, style rules, encoding, and diacritics preservation
> **Key items:** English-first analysis, translation tables, terminology dictionary, prompt
> phrasing, status and severity mapping, style rules, diacritics

This file defines the Polish rendering of the audit report and of the parameter-configuration
prompts.

When the report language is Polish, apply every translation and rule in this file to the
corresponding English terms.

The default report language is English.

This file is loaded only when the report language is Polish.

## Contents

| Section                                     | Line | What it covers                              |
|---------------------------------------------|------|---------------------------------------------|
| Analysis And Rendering                      | 80   | Analysis model and terminology precedence   |
| Status And Severity Vocabulary              | 102  | Status And Severity Vocabulary guidance     |
| Fixed Vocabulary Values                     | 254  | Polish renderings of descriptive values     |
| Terminology                                 | 313  | English to Polish technical dictionary      |
| Calque And Style Replacements               | 472  | Forbidden calques and their replacements    |
| Parameter Prompts                           | 573  | Polish phrasing for configuration questions |
| Style Rules                                 | 629  | Style Rules guidance                        |
| Diacritics Frequently Misspelled            | 772  | Diacritics Frequently Misspelled guidance   |
| Output Filename                             | 807  | Output Filename guidance                    |
| Document Information                        | 828  | Document Information guidance               |
| Audit Type Coverage                         | 876  | Coverage rendering                          |
| Project Inventory                           | 912  | Project Inventory guidance                  |
| Glossary                                    | 921  | Glossary guidance                           |
| Technology Stack                            | 980  | Technology Stack guidance                   |
| Executive Summary                           | 997  | Executive Summary guidance                  |
| Health Dashboard                            | 1015 | Health Dashboard guidance                   |
| Scorecard                                   | 1026 | Scorecard guidance                          |
| Scoring Rubrics                             | 1051 | Scoring Rubrics guidance                    |
| Delivery Practice & Team Continuity         | 1075 | Delivery and continuity rendering           |
| High-Level Observations                     | 1099 | High-Level Observations guidance            |
| Auditing Methodology                        | 1106 | Auditing Methodology guidance               |
| System Context                              | 1120 | System Context guidance                     |
| Software Bill of Materials                  | 1133 | SBOM section rendering                      |
| License Compliance Review                   | 1151 | License and IP section rendering            |
| Architectural Assessment                    | 1169 | Architectural Assessment guidance           |
| Architectural Subsections                   | 1176 | Architectural Subsections guidance          |
| Skill Definition Conformance                | 1191 | Skill Definition Conformance guidance       |
| Agent Guidance Conformance                  | 1199 | Agent Guidance Conformance guidance         |
| AI System Assessment                        | 1213 | AI System Assessment guidance               |
| Standards Conformance                       | 1224 | Standards Conformance guidance              |
| Engineering Baseline Conformance            | 1245 | Engineering Baseline Conformance guidance   |
| References                                  | 1259 | References guidance                         |
| Strengths And What's Working                | 1268 | Strengths And What's Working guidance       |
| Detailed Technical Findings                 | 1274 | Detailed Technical Findings guidance        |
| Technical Debt Register                     | 1335 | Technical Debt Register guidance            |
| Unified Risk Register                       | 1347 | Unified Risk Register guidance              |
| Trade-off Analysis                          | 1367 | Trade-off Analysis guidance                 |
| Actionable Remediation Roadmap              | 1379 | Actionable Remediation Roadmap guidance     |
| Recommendation Classification               | 1394 | Recommendation Classification guidance      |
| Changes Since Previous Audit                | 1409 | Changes Since Previous Audit guidance       |
| Scope Exclusions                            | 1443 | Scope Exclusions guidance                   |
| Limitations And Unknowns                    | 1451 | Limitations And Unknowns guidance           |
| Re-audit And Follow-up Plan                 | 1468 | Re-audit And Follow-up Plan guidance        |
| Operator Verification Handoff               | 1478 | Operator Verification Handoff guidance      |
| Executed Evidence Log                       | 1491 | Executed Evidence Log guidance              |
| Hunt Style Sections                         | 1504 | Hunt Style Sections guidance                |
| Review Style Sections                       | 1533 | Review Style Sections guidance              |
| Validation Record                           | 1563 | Validation Record guidance                  |
| Threat Model                                | 1597 | Threat Model guidance                       |
| API Contract Conformance                    | 1607 | API Contract Conformance guidance           |
| API Compatibility And Versioning Discipline | 1616 | API Compatibility And Versioning guidance   |
| Evidence And Decision Terms                 | 1625 | Evidence And Decision Terms guidance        |
| Skill Definition Conformance Table          | 1686 | Skill Definition Conformance Table guidance |
| Structure Review                            | 1701 | Structure Review guidance                   |

## Analysis And Rendering

Analysis runs in English regardless of the report language.

Evidence notes, finding drafts, partial conclusions,
and assembled part files are written in English,
and the report is rendered into Polish in a single pass that applies this file.

Reasoning in English keeps the analysis anchored to the English rules, rubrics, and fixed
vocabularies in the rest of the skill, and a single render pass applies one terminology convention
to the whole document.

When the audited project establishes its own Polish terminology, for example a project glossary or
Polish design documents, prefer those established forms over the defaults in this file and record
the choice.

Direct quotes, code, configuration keys, file paths, identifiers,
and record IDs are never translated.

Fixed report tokens - statuses, severities,
and result markers - render in Polish per Status And Severity Vocabulary.

## Status And Severity Vocabulary

Fixed report tokens render in Polish in the report body.

The English forms remain the analysis and validation vocabulary - mechanical checks run on the
English-mapped working copy.

Tokens that do not decline keep fixed label forms:

| English token              | Polish render                 |
|----------------------------|-------------------------------|
| `PASS`                     | `OK`                          |
| `PARTIAL` / `Partially`    | `Częściowo`                   |
| `N/A`                      | `N/D`                         |
| `ERROR`                    | `Błąd`                        |
| `EXCLUDED BY SCOPE`        | `Poza zakresem`               |
| `Out of scope`             | `Poza zakresem`               |
| `Not Applicable`           | `Nie dotyczy`                 |
| `INSUFFICIENT INFORMATION` | `Niewystarczające informacje` |
| `SEVERITY:`                | `Ważność:`                    |
| `Score:`                   | `Wynik:`                      |
| `Observation`              | `Obserwacja`                  |
| `Concern`                  | `Zastrzeżenie`                |

`Observation` and `Concern` are the evidence/finding type tags:
`Obserwacja` records an independently re-derivable fact,
`Zastrzeżenie` is a judgment built on observations - never `Wniosek`,
which means conclusion.

In `* **Field:**` bullet lists they render title-cased `Obserwacja`/`Zastrzeżenie`.

The Due Diligence Coverage column named `Concern` keeps its separate rendering `Obszar ryzyka`,
the two uses are not the same word's job.

Declinable values agree in gender with the noun their column header or `* **Field:**` label
names.

The governed nouns are masculine `wynik`, `status`, `charakter odstępstwa`, `wpływ`,
`wysiłek`, `priorytet`, and `poziom`, feminine `ważność`, `złożoność`, `pewność oceny`,
`gotowość`, `zmiana`, `weryfikacja`, `klasa`, `ocena`, `zgodność`, and `licencja`, and neuter
`prawdopodobieństwo`, `wykorzystanie podatności`, `ryzyko rezydualne`, and
`ryzyko licencyjne`.

In a two-column key-value table the row label's head noun governs - `Poziom szczegółowości`
takes `Szczegółowy` and `Gotowość` takes `Niegotowa`.

A header that names no declinable noun - `Bezpośredni/przechodni`, `Podstawa`, `Uwagi`,
`Poprzedni`, `Bieżący` - defers to the row's subject noun, so a transition-table cell
describing an `ustalenie` renders the neuter form `Otwarte`/`Nowe`/`Zamknięte` and a
`Bezpośredni/przechodni` cell for a `zależność` renders `deweloperska`.

| English                  | Masculine                 | Feminine                  | Neuter                    |
|--------------------------|---------------------------|---------------------------|---------------------------|
| `CRITICAL`               | Krytyczny                 | Krytyczna                 | Krytyczne                 |
| `HIGH`                   | Wysoki                    | Wysoka                    | Wysokie                   |
| `MEDIUM`                 | Średni                    | Średnia                   | Średnie                   |
| `LOW`                    | Niski                     | Niska                     | Niskie                    |
| `MODERATE`               | Umiarkowany               | Umiarkowana               | Umiarkowane               |
| `FAIL`                   | Niezaliczony              | Niezaliczona              | Niezaliczone              |
| `UNKNOWN`                | Nieznany                  | Nieznana                  | Nieznane                  |
| `NOT RUN`                | Nieuruchomiony            | Nieuruchomiona            | Nieuruchomione            |
| `NOT ASSESSED`           | Nieoceniony               | Nieoceniona               | Nieocenione               |
| `NOT INSPECTED`          | Niezbadany                | Niezbadana                | Niezbadane                |
| `NOT COLLECTED`          | Niezebrany                | Niezebrana                | Niezebrane                |
| `NOT SPECIFIED`          | Nieokreślony              | Nieokreślona              | Nieokreślone              |
| `COVERED`                | Objęty                    | Objęta                    | Objęte                    |
| `NOT DONE`               | Niewykonany               | Niewykonana               | Niewykonane               |
| `OPEN`                   | Otwarty                   | Otwarta                   | Otwarte                   |
| `CLOSED`                 | Zamknięty                 | Zamknięta                 | Zamknięte                 |
| `IN PROGRESS`            | Trwający                  | Trwająca                  | Trwające                  |
| `RESOLVED`               | Rozwiązany                | Rozwiązana                | Rozwiązane                |
| `ACCEPTED`               | Zaakceptowany             | Zaakceptowana             | Zaakceptowane             |
| `TRANSFERRED`            | Przeniesiony              | Przeniesiona              | Przeniesione              |
| `MONITORING`             | Monitorowany              | Monitorowana              | Monitorowane              |
| `NEW`                    | Nowy                      | Nowa                      | Nowe                      |
| `UNCHANGED`              | Niezmieniony              | Niezmieniona              | Niezmienione              |
| `REOPENED`               | Wznowiony                 | Wznowiona                 | Wznowione                 |
| `VERIFIED` / `INSPECTED` | Zweryfikowany             | Zweryfikowana             | Zweryfikowane             |
| `CONFIRMED`              | Potwierdzony              | Potwierdzona              | Potwierdzone              |
| `REPORTED`               | Zadeklarowany             | Zadeklarowana             | Zadeklarowane             |
| `INFERRED`               | Wniosekowany              | Wniosekowana              | Wniosekowane              |
| `APPLIED`                | Zastosowany               | Zastosowana               | Zastosowane               |
| `READY`                  | Gotowy                    | Gotowa                    | Gotowe                    |
| `NOT READY`              | Niegotowy                 | Niegotowa                 | Niegotowe                 |
| `PENDING EVIDENCE`       | Oczekujący                | Oczekująca                | Oczekujące                |
| `RECOMMENDED`            | Zalecany                  | Zalecana                  | Zalecane                  |
| `OPTIONAL`               | Opcjonalny                | Opcjonalna                | Opcjonalne                |
| `NOT RECOMMENDED`        | Niezalecany               | Niezalecana               | Niezalecane               |
| `THEORETICAL`            | Teoretyczny               | Teoretyczna               | Teoretyczne               |
| `STATIC-CONFIRMED`       | Potwierdzony statycznie   | Potwierdzona statycznie   | Potwierdzone statycznie   |
| `DYNAMICALLY-VERIFIED`   | Zweryfikowany dynamicznie | Zweryfikowana dynamicznie | Zweryfikowane dynamicznie |
| `DELIBERATE`             | Świadomy                  | Świadoma                  | Świadome                  |
| `BLOCKED`                | Zablokowany               | Zablokowana               | Zablokowane               |
| `SKIPPED`                | Pominięty                 | Pominięta                 | Pominięte                 |
| `PLANNED`                | Zaplanowany               | Zaplanowana               | Zaplanowane               |
| `UNRESOLVED`             | Nierozstrzygnięty         | Nierozstrzygnięta         | Nierozstrzygnięte         |

Token columns (`Wynik`, `Status`, `Zmiana`, `Weryfikacja`, `Ważność`, `Wpływ`,
`Prawdopodobieństwo`, `Klasa`, `Ocena`, `Gotowość`, `Pewność oceny`,
`Charakter odstępstwa`) and token-definition tables use the agreed title-case form -
the first letter uppercase, the rest lowercase.

All-caps Polish words never appear in report cells: Polish reads them as shouted
abbreviations, so `WYSOKA`, `TEORETYCZNE`, or `WNIOSEK` are always wrong.
Only true abbreviations stay uppercase: `OK`, `N/D`.
`scripts/lint-polish.py` flags all-caps Polish token forms as errors.

A token-column cell is one word - only the indeclinable phrase tokens (`Częściowo`,
`Poza zakresem`, `Nie dotyczy`, `Niewystarczające informacje`) run longer.

In `* **Field:**` bullet lists, values keep title case consistent with neighboring values,
for example `Ważność: Wysoka` next to `Status: Otwarty` - never `Niskie` next to `Otwarty`.

Running prose cites a token as a bold declined lowercase word - `ustalenia o ważności
**wysokiej**`, `gotowość oceniona jako **niegotowa**`, `wynik **nieokreślony**`.

Narrative table cells use natural sentence case - `sześć ustaleń wysokich`.

A `Wynik`/`Result` column draws its values only from `OK`, `Częściowo`, `Niezaliczony`,
`Nieznany`, `N/D`, `Nieuruchomiony`, `Nieoceniony`, `Niezbadany`, `Poza zakresem`,
`Zastosowany`, `Zweryfikowany`, `Zadeklarowany`, `Wniosekowany`, and the numeric or star
forms the selected scale defines.

The `Status` column carries lifecycle states - `Otwarty`, `Zamknięty`, `OK`, `Trwający`,
`Rozwiązany`, `Zaakceptowany`, `Przeniesiony`, `Monitorowany` - and coverage states `Objęty`,
`Częściowo`, `Niewykonany`, `Nie dotyczy`.

The `Zmiana` column carries only movement since the previous audit: `Nowa`, `Niezmieniona`,
`Wznowiona`, `Zamknięta`. The `Status` and `Zmiana` columns never share values on the same
row beyond the deliberate `Zamknięty`/`Zamknięta` overlap.

The `Weryfikacja` state column carries `Zweryfikowana`, `Potwierdzona`, or `Zadeklarowana`
and stays empty for a `Nowa` finding.

The `Klasa` column carries `Zalecana`, `Opcjonalna`, or `Niezalecana`, the `Ocena` column
carries `OK`, `Częściowo`, `Niezaliczona`, or `N/D`, and the `Gotowość` column and
`Gotowość` key-value rows carry `Gotowa`, `Niegotowa`, `Oczekująca`, or `Nieoceniona`.

The `Charakter odstępstwa` bullet values are `Brak udokumentowanego uzasadnienia`,
`Świadomy - udokumentowana decyzja`, `Nieokreślony`, or `N/D`.

Reports written before this revision carried neuter fixed forms (`Otwarte`, `Nowe`,
`Niezaliczone`) and all-caps agreed forms (`WYSOKA`, `NIEZALICZONE`) in governed
columns - a re-audit reads all of them.

Record identifiers (`FND-001`, `EVD-042`, `RSK-010`), priority codes (`P1`-`P4`), `CWE-####`,
CVSS vectors, commands, and anything inside verbatim evidence stay unchanged.

When the `1-5` or `1-3` numeric scale is selected, use `Wynik: X/5` or `Wynik: X/3`.

When `5 stars` or `3 stars` is selected, use `Wynik:` followed by the unchanged star bar.

## Fixed Vocabulary Values

Descriptive values are rendered in Polish and agree in gender with the noun they describe:
`wpływ`, `wysiłek`, and `priorytet` take `Wysoki`/`Średni`/`Niski`, `złożoność` and
`ważność` take `Wysoka`/`Średnia`/`Niska`, `prawdopodobieństwo` and `ryzyko` take
`Wysokie`/`Średnie`/`Niskie`.

| English                          | Polish                                   |
|----------------------------------|------------------------------------------|
| `Draft`                          | `Roboczy`                                |
| `Final`                          | `Gotowy`                                 |
| `Detailed`                       | `Szczegółowy`                            |
| `Standard`                       | `Standardowy`                            |
| `Brief`                          | `Skrócony`                               |
| `5 stars`                        | `5 gwiazd`                               |
| `3 stars`                        | `3 gwiazdy`                              |
| `Stars` (prompt option)          | `Gwiazdy`                                |
| `Enabled`                        | `Włączony` or `Aktywny`                  |
| `Error`                          | `Błąd`                                   |
| `Disabled`                       | `Wyłączony`                              |
| `Prototype`                      | `Prototyp`                               |
| `Early development`              | `Wczesny rozwój`                         |
| `Pre-production`                 | `Etap przedprodukcyjny`                  |
| `Production-ready`               | `Gotowość produkcyjna`                   |
| `Undetermined`                   | `Nieokreślony`                           |
| `Ready`                          | `Gotowy`                                 |
| `Not ready`                      | `Niegotowy`                              |
| `Pending evidence`               | `Oczekujące`                             |
| `Not assessed`                   | `Nieoceniony`                            |
| `Full`                           | `Pełna`                                  |
| `Partial`                        | `Częściowa`                              |
| `None`                           | `Brak`                                   |
| `Not applicable`                 | `nie dotyczy`                            |
| `source-only`                    | `wyłącznie na podstawie kodu źródłowego` |
| `executed-readonly`              | `wykonanie tylko do odczytu`             |
| `executed-commands`              | `wykonanie zleconych poleceń`            |
| `audit` (report style)           | `audyt`                                  |
| `hunt` (report style)            | `polowanie na usterki`                   |
| `review` (report style)          | `przegląd`                               |
| `Source` (evidence level)        | `Źródło`                                 |
| `Model` (evidence level)         | `Model`                                  |
| `App` (evidence level)           | `Aplikacja`                              |
| `Deployed` (evidence level)      | `Wdrożenie`                              |
| `Unknown` (evidence level)       | `Nieznany`                               |
| `Internal` (breaking change)     | `wewnętrzne`                             |
| `Public API` (breaking change)   | `publiczne API`                          |
| `engineering improvement`        | `doskonalenie inżynieryjne`              |
| `production readiness`           | `gotowość produkcyjna`                   |
| `technical due diligence`        | `due diligence techniczne`               |
| `No documented rationale`        | `Brak udokumentowanego uzasadnienia`     |
| `Deliberate - recorded decision` | `Świadome - udokumentowana decyzja`      |
| `New`                            | `Nowe`                                   |
| `Unchanged`                      | `Niezmienione`                           |
| `Reopened`                       | `Wznowione`                              |
| `Closed`                         | `Zamknięte`                              |
| `Confirmed`                      | `Potwierdzone`                           |

Numeric scales `1-10`, `1-5`, and `1-3` stay unchanged.

## Terminology

The dictionary maps recurring English technical terms to their preferred Polish forms.

Entries with two forms separated by `/` are context-dependent,
pick the form that fits the sentence rather than always translating the same English word
identically.

| English                                | Polish                                                                      |
|----------------------------------------|-----------------------------------------------------------------------------|
| AI-assisted development workflow       | proces wytwarzania oprogramowania wspomagany przez AI                       |
| absence assessment                     | charakter odstępstwa                                                        |
| access token                           | token dostępu                                                               |
| action                                 | działanie                                                                   |
| API contract validation                | kontrola poprawności kontraktu API                                          |
| attack path                            | ścieżka ataku                                                               |
| attack surface                         | powierzchnia ataku                                                          |
| assurance                              | zapewnienie                                                                 |
| attribution                            | przypisanie autorstwa                                                       |
| authoritative source                   | źródło autorytatywne                                                        |
| automated compliance check/enforcement | automatyczna weryfikacja zgodności                                          |
| automated enforcement                  | automatyczne egzekwowanie reguł                                             |
| baseline                               | wartość bazowa / lista zaakceptowanych odchyleń                             |
| backup restore                         | odtworzenie z kopii zapasowej                                               |
| backup restore test                    | test odtwarzania kopii zapasowej                                            |
| backup retention                       | retencja kopii zapasowych                                                   |
| build                                  | proces budowania                                                            |
| build artifact                         | artefakt wynikowy / artefakt wdrożeniowy                                    |
| build job                              | zadanie budowania                                                           |
| build reproducibility                  | powtarzalność procesu budowania                                             |
| bus factor                             | bus factor (ryzyko koncentracji wiedzy)                                     |
| change document                        | dokument zmiany                                                             |
| change review                          | przegląd zmian                                                              |
| code provenance                        | pochodzenie kodu                                                            |
| code provenance traceability           | identyfikowalność pochodzenia kodu                                          |
| commit                                 | zatwierdzenie                                                               |
| Common Weakness Enumeration            | klasyfikacja typowych błędów bezpieczeństwa oprogramowania                  |
| concern (evidence/finding tag)         | zastrzeżenie (never `wniosek` - that means conclusion)                      |
| control execution                      | kontrola dynamiczna                                                         |
| contract test                          | test zgodności kontraktu / test kontraktowy                                 |
| contract/implementation mismatch       | rozbieżność między kontraktem a implementacją                               |
| copyleft                               | copyleft (nie tłumaczyć)                                                    |
| credentials                            | poświadczenia                                                               |
| deadline                               | termin                                                                      |
| demo credentials                       | poświadczenia demonstracyjne                                                |
| delivery practice                      | praktyka dostarczania                                                       |
| decision                               | decyzja                                                                     |
| dependency analysis                    | analiza zależności                                                          |
| dependency vulnerability scanning      | analiza podatności zależności / skanowanie podatności zależności            |
| deploy                                 | wdrażać                                                                     |
| deployability                          | zdolność do wdrażania                                                       |
| deployment                             | wdrożenie                                                                   |
| deployment gate                        | warunek dopuszczenia do wdrożenia                                           |
| deployment job                         | zadanie wdrożeniowe                                                         |
| documentation drift                    | rozbieżność dokumentacji ze stanem systemu / dezaktualizacja                |
| endpoint                               | punkt końcowy API / endpoint                                                |
| error-report intake                    | przyjęcie raportów błędów                                                   |
| evidence                               | informacje ustalone na podstawie repozytorium / dowód                       |
| evidence register                      | rejestr dowodów audytowych                                                  |
| exploitability narrative               | narracja wykorzystania podatności                                           |
| fail-closed                            | odmowa dostępu / zamknięcie w przypadku błędu                               |
| fail-fast                              | natychmiastowe przerwanie przy błędzie                                      |
| fallback                               | mechanizm awaryjny / obsługa zastępcza                                      |
| finding                                | ustalenie                                                                   |
| guard                                  | mechanizm ochronny                                                          |
| handler                                | handler / procedura obsługi                                                 |
| hardening                              | utwardzanie                                                                 |
| host key pinning                       | przypięcie klucza hosta                                                     |
| installation package                   | pakiet instalacyjny                                                         |
| join                                   | łączenie                                                                    |
| key-person risk                        | ryzyko koncentracji kompetencji                                             |
| license compliance                     | zgodność licencyjna                                                         |
| likelihood                             | prawdopodobieństwo                                                          |
| lockfile                               | plik blokady zależności                                                     |
| lookup                                 | wyszukiwanie                                                                |
| maintainability                        | utrzymywalność                                                              |
| materialized risk                      | ryzyko się zrealizowało                                                     |
| manual deployment gate                 | ręczne zatwierdzenie wdrożenia                                              |
| maturity level                         | poziom dojrzałości                                                          |
| merge                                  | włączenie do gałęzi / scalenie                                              |
| merge request / pull request           | żądanie włączenia zmian                                                     |
| mitigation                             | środek ograniczający ryzyko                                                 |
| mismatch                               | rozbieżność / niezgodność                                                   |
| network surface                        | powierzchnia ataku dostępna przez sieć                                      |
| non-conformity / gap                   | niezgodność / luka                                                          |
| observability                          | obserwowalność                                                              |
| observation                            | obserwacja                                                                  |
| parity                                 | zgodność / równoważność                                                     |
| path canonicalization / canonicalize   | normalizacja ścieżek / normalizować                                         |
| path traversal                         | manipulacja ścieżką                                                         |
| operational readiness                  | gotowość operacyjna                                                         |
| operational security                   | bezpieczeństwo operacyjne                                                   |
| owner                                  | właściciel                                                                  |
| package                                | pakiet                                                                      |
| pipeline / CI pipeline                 | proces / proces CI / proces CI/CD                                           |
| prefetch                               | wstępne pobranie / pobranie                                                 |
| pre-production                         | etap przedprodukcyjny / środowisko przedprodukcyjne                         |
| production / prod                      | środowisko produkcyjne                                                      |
| promise (JavaScript)                   | Promise (nie tłumaczyć)                                                     |
| re-audit                               | ponowny audyt                                                               |
| production-ready                       | gotowość produkcyjna                                                        |
| public error-report intake             | publiczny punkt przyjęcia raportów błędów                                   |
| quality gate                           | kryterium jakości / warunek jakości                                         |
| rate limiting                          | ograniczenie częstotliwości żądań                                           |
| recommendation                         | zalecenie / zalecenie naprawcze                                             |
| recommendation classification          | klasyfikacja zaleceń                                                        |
| refresh token                          | token odświeżania                                                           |
| remediation                            | działanie naprawcze                                                         |
| remediation plan                       | plan działań naprawczych                                                    |
| reproducible build                     | powtarzalny proces budowania                                                |
| residual risk                          | ryzyko rezydualne                                                           |
| resolve                                | ustalić (lokalizacja, wartość) / rozstrzygnąć (spór) / usunąć (diagnostyka) |
| reuse detection                        | wykrywanie ponownego użycia tokenu                                          |
| review                                 | przegląd                                                                    |
| risk register                          | rejestr ryzyk                                                               |
| root cause                             | przyczyna źródłowa                                                          |
| routing                                | kierowanie                                                                  |
| runtime                                | środowisko uruchomieniowe                                                   |
| runtime scope                          | zakres uruchomieniowy                                                       |
| scalability                            | skalowalność                                                                |
| scorecard                              | karta oceny                                                                 |
| seam (testability)                     | punkt podstawienia                                                          |
| security control                       | środek bezpieczeństwa / mechanizm kontrolny                                 |
| sign-off                               | zatwierdzenie / akceptacja formalna                                         |
| seed data                              | dane inicjalizacyjne                                                        |
| seeding                                | inicjalizacja danych                                                        |
| seeding mechanism                      | mechanizm inicjalizacji danych                                              |
| severity                               | waga                                                                        |
| Software Bill of Materials             | zestawienie składników oprogramowania                                       |
| source of truth                        | źródło prawdy                                                               |
| source-only                            | wyłącznie na podstawie kodu źródłowego                                      |
| stakeholder                            | interesariusz                                                               |
| static handler                         | statyczny handler                                                           |
| status                                 | status                                                                      |
| surface area of code                   | zakres kodu                                                                 |
| testability                            | testowalność                                                                |
| test inventory                         | rozbudowany zakres testów                                                   |
| threat                                 | zagrożenie                                                                  |
| threat model                           | model zagrożeń                                                              |
| TLS termination                        | terminacja TLS / zakończenie połączenia TLS                                 |
| token reuse                            | ponowne użycie tokenu                                                       |
| toolchain                              | łańcuch narzędzi                                                            |
| trade-off                              | kompromis                                                                   |
| triage                                 | przegląd i klasyfikacja                                                     |
| trust boundary                         | granica zaufania                                                            |
| unauthenticated                        | bez uwierzytelnienia                                                        |
| verdict                                | werdykt                                                                     |
| verified in sources                    | zweryfikowany w repozytorium                                                |
| version drift                          | rozbieżność wersji / niespójność wersjonowania                              |
| version pinning                        | zamrożenie wersji                                                           |
| visual designer                        | projektowanie wizualne                                                      |
| vulnerability                          | podatność                                                                   |
| vulnerability assessment               | ocena podatności                                                            |
| vulnerability triage                   | weryfikacja i klasyfikacja podatności                                       |
| weakness                               | błąd bezpieczeństwa / podatność bezpieczeństwa                              |
| weakness classification                | klasyfikacja błędów bezpieczeństwa                                          |
| weight                                 | waga                                                                        |
| workflow                               | przepływ pracy / proces                                                     |

## Calque And Style Replacements

This table is machine-readable - `scripts/lint-polish.py` parses it and flags every
`Instead of` form it finds in Polish report output.

Keep entries as single words or short fixed phrases the checker can match literally.

| Instead of                 | Use                                              | Note                                                  |
|----------------------------|--------------------------------------------------|-------------------------------------------------------|
| rozjazd                    | rozbieżność / niezgodność                        | calque of English drift/mismatch                      |
| dryf dokumentacji          | dezaktualizacja dokumentacji                     | drift is `narastająca rozbieżność` elsewhere          |
| dryf                       | narastająca rozbieżność / odchylenie             | context-dependent                                     |
| baseline                   | wartość bazowa / lista zaakceptowanych odchyleń  | spell out or keep English only in tool output         |
| brama                      | warunek / kontrola blokująca                     | `gate`, `quality gate`, `lint gate`                   |
| bramka                     | warunek / kontrola blokująca                     | same calque, diminutive                               |
| martwa brama               | nieskuteczna kontrola                            | dead gate                                             |
| strażnik                   | mechanizm ochronny                               | guard                                                 |
| triaż                      | przegląd i klasyfikacja                          | vulnerability triage                                  |
| parzystość                 | zgodność / równoważność                          | parity is not parzystość                              |
| paritet                    | zgodność / równoważność                          | parity is not paritet                                 |
| powierzchnia kodu          | zakres kodu                                      | surface area of code                                  |
| powierzchnia sieci         | powierzchnia ataku dostępna przez sieć           | network surface                                       |
| kontrola wykonawcza        | kontrola dynamiczna                              | control execution                                     |
| zmaterializowane ryzyko    | ryzyko się zrealizowało                          | name the concrete effect where possible               |
| czynnik autobusowy         | bus factor (ryzyko koncentracji wiedzy)          | gloss at first use, then `bus factor`                 |
| commitowany                | commit / dodany do repozytorium                  | jargon derivative - use the loanword or a description |
| onboardowanie              | wdrażanie nowych osób / wprowadzenie             | onboarding                                            |
| progresywne ujawnianie     | stopniowe ujawnianie                             | progressive disclosure                                |
| wielorazowy                | wielokrotnego użytku                             | reusable                                              |
| linkowanych                | połączonych / powiązanych                        | linked                                                |
| multi-agentowy             | wieloagentowy                                    | multi-agent                                           |
| dostawczone                | dostarczone                                      | misspelling of dostarczone                            |
| wydawniczy                 | wydaniowy                                        | release lifecycle, not publishing                     |
| siostrzana gałąź           | pozostała gałąź / gałąź równoległa               | sibling branch                                        |
| siostrzany                 | pozostały / równoległy                           | sibling                                               |
| konsumowana                | używana / pobierana                              | consumed                                              |
| zaadresować                | rozwiązać / uwzględnić                           | address an issue                                      |
| celują w                   | kierują do / dotyczą                             | aim at                                                |
| kosztują kontekst          | zajmują kontekst / zużywają kontekst             | cost context                                          |
| przypięty (wersja)         | zamrożony (wersja)                               | `przypięcie` is reserved for host keys                |
| nieprzypięty toolchain     | nieustalona wersja środowiska                    | unpinned toolchain                                    |
| pod                        | poniżej / w ramach / zgodnie z                   | `under` calque: `pod nagłówkiem` -> `w sekcji`        |
| plus (spójnik)             | oraz / a także                                   | `plus` never joins Polish clauses                     |
| per (przyimek)             | dla każdego / na                                 | `per project` -> `dla każdego projektu`               |
| niesie (cecha)             | wnosi / powoduje                                 | a branch does not carry traits like a person          |
| dotyka                     | dotyczy / zmienia                                | touches                                               |
| zyskuje                    | zostaje wzbogacony o / otrzymuje                 | gains                                                 |
| właściciel (dokumentu)     | dokument nadrzędny                               | owner of a document                                   |
| mieszkają                  | znajdują się / są umieszczone                    | files do not live                                     |
| żyje (plik)                | znajduje się                                     | same personification                                  |
| lustro                     | kopia struktury / kopia                          | mirror                                                |
| ładunek                    | zawartość / blok danych                          | payload                                               |
| zakotwiczone               | osadzone / utrwalone                             | anchored                                              |
| wskaźnik (odnośnik)        | odnośnik / wskaźnik                              | `wskaźnik` is a metric, a link is `odnośnik`          |
| wyposażenie                | zawartość / skład                                | files are not equipped                                |
| rekursują                  | przechodzą rekurencyjnie / schodzą rekurencyjnie | recurse                                               |
| rozstrzygnięta lokalizacja | ustalona lokalizacja                             | calque of resolved location                           |
| zastany                    | istniejący wcześniej / odziedziczony             | pre-existing                                          |
| delta kodowa               | zakres zmian w kodzie                            | code delta                                            |
| rozdzielczy (rzeczownik)   | plik kierujący                                   | router file                                           |
| paczka                     | pakiet                                           | package                                               |
| joiny                      | łączenia                                         | joins                                                 |
| lookupy                    | wyszukiwania                                     | lookups                                               |
| tylko, gdy                 | tylko wtedy, gdy                                 | syntax                                                |
| w. (skrót wierszy)         | wiersze / linie                                  | no `w.` abbreviation                                  |
| potok                      | proces / proces CI                               | pipeline                                              |
| deployować                 | wdrażać                                          | deploy                                                |
| requestować                | zgłaszać                                         | request                                               |
| fixować                    | poprawiać                                        | fix                                                   |
| kastomizacja               | dostosowanie                                     | customization                                         |
| stakeholderzy              | interesariusze                                   | stakeholders                                          |
| ownerzy biznesowi          | właściciele biznesowi                            | business owners                                       |
| status report              | raport o statusie                                |                                                       |
| meeting minutes            | protokół zebrania                                |                                                       |
| dane skrapane              | dane skrapowane                                  | scraped data                                          |
| usankcjonować              | sankcjonować / formalizować                      | misspelling                                           |
| prozatorski                | opisowy / narracyjny                             | prosaic                                               |
| tier                       | poziom                                           | exploitability tier                                   |
| drift                      | rozbieżność / dezaktualizacja                    | English word inside Polish prose                      |
| uplok                      | wgrywanie / przesyłanie                          | misspelled `upload`                                   |
| upload                     | wgrywanie / przesyłanie                          | upload to a remote store                              |
| seed                       | dane inicjalizacyjne / wpis inicjalizacyjny      | seed data, seeded account                             |
| fallback                   | mechanizm awaryjny / obsługa zastępcza           | bare noun - `fallbackData` in code stays verbatim     |
| pipeline                   | proces CI / proces                               | bare noun - a job name in code stays verbatim         |
| konsumuj                   | używają / pobierają                              | consume                                               |
| skanery podatności         | skanowanie podatności                            | the unrun activity, not the tools                     |
| skanerów podatności        | skanowania podatności                            | same phrase, genitive                                 |
| stem                       | podstawa nazwy pliku                             | filename stem, for example in the delivery prompt     |
| traversowanie              | manipulacja ścieżką                              | path traversal                                        |
| traversowania              | manipulacji ścieżką                              | path traversal, genitive                              |
| kanonikalizacja            | normalizacja ścieżek                             | path canonicalization                                 |
| kanonikalizować            | normalizować                                     | canonicalize - `kanoniczny` stays as the adjective    |
| hartowanie                 | utwardzanie                                      | hardening                                             |
| hartowania                 | utwardzania                                      | hardening, genitive                                   |
| szew podstawienia          | punkt podstawienia                               | seam                                                  |
| szew                       | punkt podstawienia                               | seam in the testability sense                         |
| szwy                       | punkty podstawienia                              | seams, plural                                         |
| statyczne procedury        | statyczne handlery                               | static handlers                                       |
| statycznych procedur       | statycznych handlerów                            | static handlers, genitive                             |
| przemierzona lokalizacja   | lokalizacja wskazana przez ścieżkę               | traversed location                                    |

## Parameter Prompts

The Parameter Configuration questions are asked in Polish when the user's request is in Polish.
Apply these phrasing rules:

- Report delivery uses `sposób dostarczania raportu` or `dostarczenie raportu`, never `dostawa`.
  Ask `Jak dostarczyć raport?` or `Gdzie zapisać plik raportu?`.
- The file option without the revision number is `Plik bez numeru rewizji` (for example
  `docs/report/AUDYT.md`). The English `stem` is never used in a Polish prompt.
  For a `polowanie na usterki` or `przegląd` report this bare option
  (`docs/report/POLOWANIE.md`, `docs/report/PRZEGLĄD.md`) is the default and the
  revisioned `POLOWANIE-1.0.md`/`PRZEGLĄD-1.0.md` is the alternative.
- Date-named subdirectory options use `katalogi dzienne` or `ścieżka daty`/`ścieżka dzienna`.
  `Datowy` and `datowa` are not proper Polish words and must not be used.
- The detail-level question is `Jaki poziom szczegółowości powinien mieć raport?` with options
  `Szczegółowy` (domyślny), `Standardowy`, and `Skrócony`.
- The evaluation-scale question is `Jaką skalę ocen zastosować dla karty wyników?` with options
  `1-10` (domyślna), `1-5`, `1-3`, and `Gwiazdy`. When `Gwiazdy` is selected, ask the follow-up
  `Ile gwiazd ma mieć skala?` with options `5 gwiazd` (domyślnie) and `3 gwiazdy`.
- `Inline` is offered as `W treści odpowiedzi` and `Custom report file` as `Własny plik raportu`.
- The trailing bypass options are `Użyj wartości domyślnej: <wartość>` and
  `Użyj wartości domyślnych dla wszystkich pozostałych pytań`.
- The Skill Update Check question is `Dostępna jest aktualizacja umiejętności (<n> nowych
  commitów). Zaktualizować teraz czy pominąć w tej sesji?` with options `Zaktualizuj teraz` and
  `Pomiń w tej sesji`.
- The `Report style` row in the defaults summary renders `Styl raportu` with values `audyt`,
  `polowanie na usterki`, and `przegląd`.
- When a previous review report is found, the audit-mode question reads `Znaleziono poprzedni
  raport przeglądu: <ścieżka> (rewizja <n>, data <d>). Czy wykonać ponowny przegląd względem
  tego raportu, czy nowy przegląd?` with the `Ponowny przegląd` and `Nowy przegląd` option
  forms matching the audit-mode variants.
- The audit-mode question is `Znaleziono poprzedni raport audytu: <ścieżka> (rewizja <n>, data
  <d>). Czy wykonać ponowny audyt względem tego raportu, czy nowy audyt?` with options
  `Ponowny audyt - porównaj z <plik>`, `Ponowny audyt ze zmienionymi parametrami - porównaj
  i zmień parametry`, and `Nowy audyt - zignoruj poprzedni raport`. The baseline-confirmation
  variant is `Potwierdź, że <ścieżka> to poprawna podstawa ponownego audytu.` with options
  `Potwierdź - ponowny audyt względem <plik>`, `Ponowny audyt ze zmienionymi parametrami`, and
  `Nowy audyt`. The changed-parameters follow-up is `Które parametry zmienić?`, and the
  recovered value on each prompt is marked `(poprzednia, domyślna)`. When a requested re-audit
  finds no previous report, ask `Nie znaleziono poprzedniego raportu audytu. Wykonać nowy
  audyt (rewizja 1.0)?` with the option `Wykonaj nowy audyt`. Mark the recommended option with
  `(zalecane)`.
- The project-inclusion question is `Które projekty uwzględnić w audycie?`, a multi-select list
  naming each project by path and kind, with recommended projects checked by default and
  installed or external directories listed unchecked with the reason `zainstalowane/zewnętrzne`.
  An all-unchecked answer asks `Wykluczono wszystkie projekty. Przerwać audyt?`.
- The skills-scope question is `Ocenić umiejętności jako komponenty projektu czy jako niezależne
  projekty?` with options `Oceń jako komponenty projektu` (zalecane) and `Oceń każdą umiejętność
  jako niezależny projekt`.
- JSON parameter documents per `process/json-exchange.md` keep English keys, parameter `id`s, and
  `menu` letters untranslated. Only `question` and `description` text and option labels render in
  Polish.
- The diagnostic-mode context description following the emitted document is `Oczekujące decyzje:
  <lista parametrów>. Dokument JSON powyżej ma charakter informacyjny - pytania zostaną zadane
  jak zwykle.`

## Style Rules

- Do not use "Title Case" in section and chapter names, use sentence case.
- Use "Przykład zawartości" instead of "Content Example".
- Use neuter gender for acronyms treated as nouns: "czyste PWA" (not "czysta PWA"), "czyste SPA"
  (not "czysta SPA").
- Preserve all Polish diacritics (for example, "ą", "ę", "ć", "ł", "ń", "ó", "ś", "ź", "ż", "Ą",
  "Ę", "Ć", "Ł", "Ń", "Ó", "Ś", "Ź", "Ż") in every section, heading, table cell, and paragraph. Do
  not transliterate or strip diacritics.
- Write the report in UTF-8 encoding. Do not use ASCII-only fallback for Polish text.
- Prefer the Polish form from the Terminology table. Established anglicisms such as `endpoint`,
  `frontend`, `backend`, `CI/CD`, and `lint` may stay untranslated. Never combine both forms of
  one term in a single phrase: write `środowisko uruchomieniowe` or `runtime`, never
  `środowisko uruchomieniowe runtime`.
- `Runtime` compounds translate in full: `środowisko uruchomieniowe definicji` for `definition
  runtime`, or the standalone `środowisko uruchomieniowe` when the qualifier can be dropped. A
  bare `Runtime` never modifies a Polish noun, so `Runtime definicji` is wrong.
- `Package` renders `pakiet`, never `paczka`, and `installation package` renders `pakiet
  instalacyjny`. Compounds follow the same rule: `anatomia pakietu`, `anatomia pakietu
  definicji`, or the shorter `anatomia definicji`, never `anatomia paczki definicji`.
- `Join` renders `łączenie` (`łączenia` in plural), never `joiny`, and `lookup` renders
  `wyszukiwanie` (`wyszukiwania` in plural), never `lookupy`.
- `Prefetch` renders `wstępne pobranie` or the shorter `pobranie`.
- `Visual designer` renders `projektowanie wizualne`, never `designer wizualny`.
- `Fail-closed` renders `odmowa dostępu` or `zamknięcie w przypadku błędu`, depending on
  context.
- Do not translate one English word the same way everywhere. Software-engineering terms are
  context-dependent: `weakness` is `błąd bezpieczeństwa` or `podatność bezpieczeństwa`, `drift` is
  `rozbieżność` or `dezaktualizacja`, `gate` is `warunek` or `kontrola`, `workflow` is
  `przepływ pracy` or `proces`, `fallback` is `mechanizm awaryjny` or `obsługa zastępcza`.
- Avoid literal calques. Use `rozbieżność` or `niezgodność` instead of `rozjazd`,
  `dezaktualizacja dokumentacji` or `rozbieżność dokumentacji ze stanem systemu` instead of
  `dryf dokumentacji`, `nieustalona wersja środowiska` (for example `nieustalona wersja
  środowiska Node.js`) instead of `nieprzypięty toolchain`, `nieskuteczna kontrola lintowania`
  instead of `martwa brama lint`, `warunki weryfikacyjne` instead of `bramy weryfikacji`, and
  `weryfikacja i klasyfikacja podatności` instead of `triaż podatności`.
- Describe `CWE` as `klasyfikacja typowych błędów bezpieczeństwa oprogramowania`. CWE classifies
  weakness types that can lead to vulnerabilities, CVE identifies concrete vulnerabilities.
- Describe `CSP` as `polityka bezpieczeństwa`, not `polityka nagłówkowa`.
- Describe `CI/CD` as `ciągłe budowanie i wdrażanie`, not `potok budowania i wdrażania`.
- `ASCII` needs no Polish gloss such as `ograniczony zestaw znaków`.
- `CRLF`, `CR`, and `LF` are character codes, do not expand or describe them.
- Use `odpowiednie do przedmiotu` for "applicable to the subject", not `stosowne do przedmiotu`.
- Within a table column, keep capitalization consistent: when most cells in a column start with an
  uppercase letter, capitalize the first letter of every value in that column. The rule covers the
  value column of the `Informacje o dokumencie` table the same way - `Doskonalenie inżynieryjne`,
  `Wewnętrzne środowisko produkcyjne` - while literal values (versions, dates, paths, revisions,
  links) stay verbatim.
- A value cell that carries a fixed-vocabulary token renders the agreed title-case form, and the
  `Wersja umiejętności` cell carries the bare version (`2.0.2`), never a product-name prefix.
- When one modifier governs a likelihood-impact pair in prose, name `prawdopodobieństwo` first
  and join with `oraz`: `o wysokim prawdopodobieństwie oraz wpływie`.
- The static-scope sentence reads `Nie uruchamiano aplikacji, testów, budowania ani skanowania
  podatności.` - `skanowanie` names the unrun activity, `skanery` would name tools.
- In a multi-project report the project tag trails the title or heading as a parenthetical -
  `Brak pliku LICENSE (backend)`, `### FND-SEC-001: Tytuł (backend)` - never a `[backend]`
  prefix.
- `* **Field:**` bullet-list values start with an uppercase letter, for example
  `Podstawa: Kontrola dostępu bez uwierzytelnienia`. Values that start with a code span
  or link stay verbatim.
- In the Słownik, definition cells and the Polish gloss after ` - ` start with an uppercase
  letter: `Secure Shell - Szyfrowana powłoka`, `znaki końca linii` renders `Znaki końca linii`.
- Glossary glosses name the thing precisely, without padding: `SSH - Szyfrowana powłoka`,
  `SMTP - Protokół wysyłania poczty`, `npm - Menedżer pakietów Node`,
  `SCP - Kopiowanie plików protokołem SSH`, `TLS - Szyfrowana warstwa transportu`,
  `TTL - Czas życia`, `RSK - Identyfikator w rejestrze ryzyk`.
- Describe `pipeline` as `proces`, `proces CI`, or `proces CI/CD`, never `potok`.
- Use `bez uwierzytelnienia` instead of `nieuwierzytelniony`: `kontrola dostępu bez
  uwierzytelnienia`, `punkt przyjęcia raportów błędów bez uwierzytelnienia`.
- `version pinning` renders `zamrożenie wersji`, and `przypięcie` is reserved for host keys
  (`przypięcie klucza hosta`, `przypięcie known_hosts`).
- `new endpoint` as a unit of change reads `nowa operacja`, and the standalone anglicism `endpoint`
  stays.
- `Inferred` renders `Wnioskowane` in descriptive use and `Wniosekowany`/`Wniosekowana`/
  `Wniosekowane` in token columns, never `Wywnioskowane`. `Wniosekowany` belongs to
  `wnioskować` (to infer) - it is unrelated to `Zastrzeżenie`, the `Concern` tag.
- Keep one register per report. The default register is everyday Polish software-engineering
  usage (`audyt`, `audytor`, `audytowanie`), not the ISO-standards register that writes
  `audit`/`auditor`. The ISO spelling is a documented exception only, never mixed in with the
  default, and never a per-section choice.
- `commit`, `pull request`, `merge`, `roadmapa`, `due diligence`, `copyleft`, and `SBOM`
  (spelled out once as `zestawienie składników oprogramowania`) are settled loanwords and stay
  untranslated.
- Every English term the skill adds to report headings or scored dimensions gets a Terminology
  entry before it is used in a Polish report. Polish reports are checked against this file
  verbatim under PAR-16, ad hoc translation is not allowed.
- Use `N/D` for `N/A` and `Błąd` for `ERROR`/`Error` in Polish reports.
- The score-band legend is labeled `Skala oceny`, never `Legenda pasm` or `Skala ocen`.
- Broad test coverage is `rozbudowany zakres testów`, not `szeroki inwentarz testowy`.
- Effort estimates use plain units: `godziny`, not `godziny-dzień`.
- The verb `rozejść się` uses the past-tense forms `rozszedł się`, `rozeszła się`,
  `rozeszło się`, and `rozeszli`/`rozeszły się`, never `rozeszedł się`, for example `kontrakt
  rozszedł się z implementacją`.
- Keep one thought per sentence. Most prose sentences run 15-25 words,
  and approximately 35 words is the practical upper limit.
  Split longer sentences instead of chaining clauses.
- Never join two independent clauses with a bare comma. Use a full stop,
  a colon when the second clause explains the first, or a conjunction
  (`więc`, `natomiast`, `ponieważ`).
- Every prose sentence carries an explicit predicate. Nominal fragments belong
  in table cells and bullet labels, not in running prose.
- The grammatical subject that performs an action is a person, a tool, or a process.
  Files, branches, sections, and repositories do not act - describe their state with a
  passive or nominal construction: `gałąź została rozszerzona` or `rozszerzenie gałęzi`,
  not `gałąź dodaje`.
- An adverbial participle (`imiesłów przysłówkowy`) is allowed only when its subject
  matches the main clause's subject: `przechodząc do` is wrong when the subject of the
  main clause is a document or a table.
- Keep enumeration members in the same grammatical form. Prefer a bulleted list once
  an enumeration exceeds four members or carries nested structure.
- Noun chains stop at three members - expand beyond that into a prepositional phrase.
- One concept carries one name through the whole report. Precedence order: established
  Polish term, then a settled English loanword used uninflected and glossed at first use,
  then a Polish description. Jargon derivatives such as `commitowany` or `onboardowanie`
  are replaced by the loanword or a description.
- A term without a settled Polish equivalent takes a first-use gloss with the English
  word in parentheses - `punkt podstawienia (ang. seam)` - then the bare Polish form.
  The gloss stays out of headings and table titles, which must match verbatim.
- Technical names keep canonical spelling - `Git`, `SemVer`, `Docker`, `Node.js` -
  and product names decline normally where grammar requires (`Dockera`).
  Filenames, commands, and identifiers never decline and take a generic noun instead:
  `plik \`AGENTS.md\``, `system GitLab`. Abbreviations expand at first use and enter
  the Słownik: `MR`, `SAST`. Do not abbreviate `wierszy` as `w.`.
- Verbatim foreign-language quotations are marked as quotations and carry a Polish gloss
  beside them, and they are never woven into Polish grammar. Own renderings are paraphrased
  or marked as translations, not presented as quotes.
- Polish report output uses ASCII punctuation by default: straight quotes `"` and `'`,
  the spaced hyphen ` - ` for dashes, `...` for an ellipsis, and `->` or a word
  (`→` spelled out) for arrows. Typographic forms (`„…"`, `–`, `—`, `→`, `…`) appear only
  when the task or the source document explicitly establishes them - for audit reports
  they are never introduced on the writer's own initiative.
- Defined Polish names are used verbatim mid-sentence without extra capitalization:
  `źródła prawdy`, not `Źródła Prawdy`, in the middle of a sentence.
- `referencja Git (ref)` at first use, then `ref`.
- Finding titles in summary tables are copied verbatim from the `### FND-…` headings -
  never rephrased. The same verbatim-copy rule covers recommendation titles from the
  `### REC-…` headings and every later repetition of either title: risk registers,
  roadmaps, follow-up plans, and the Validation Record all cite the title exactly as
  the heading states it.
- A `Typ systemu` value, `Poziom dojrzałości`, `Cel audytu`, and readiness gates must not
  contradict one another: a `środowisko produkcyjne` claim alongside an
  `etap przedprodukcyjny` engagement context is a defect to fix before delivery.

## Diacritics Frequently Misspelled

The following Polish words are frequently written without diacritics by mistake.

Always use the correct form with diacritics:

- `Poziom dojrzałości` (not `Poziom dojrzalosci`)
- `Testowalność` (not `Testowalnosc`)
- `Jakość` (not `Jakosc`)
- `Jakość kodu` (not `Jakosc kodu`)
- `Zgodność` (not `Zgodnosc`)
- `Zgodność ze stosem` (not `Zgodnosc ze stosem`)
- `Utrzymywalność` (not `Utrzymywalnosc`)
- `Zdolność do wdrażania` (not `Zdolnosc do wdrazania`)
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
- `Szczegółowy` (not `Szczegolowy`)
- `Przegląd` (not `Przeglad`)
- `Oświadczenie` (not `Oswiadczenie`)
- `Założenia` (not `Zalozenia`)
- `Wysiłek` (not `Wysilek`)
- `Złożoność` (not `Zlozonosc`)
- `Oryginalność` (not `Oryginalnosc`)
- `Wdrażanie` (not `Wdrazanie`)

## Output Filename

The default output filename for a Polish-language report carries the report revision:
`AUDYT-1.0.md` for a first audit instead of `AUDIT-1.0.md`, with plain `AUDYT.md` offered as an
alternative.

When a previous report exists, the default filename carries the new revision, for example
`AUDYT-1.1.md`, and the previous file is never overwritten.

A `polowanie na usterki` report uses the `POLOWANIE` stem and inverts the default:
`POLOWANIE.md` for a first hunt, with `POLOWANIE-1.0.md` offered as the revisioned
alternative, and `POLOWANIE-<revision>.md` once a previous hunt report exists.

A `przegląd` report uses the `PRZEGLĄD` stem under the same bare-first default:
`PRZEGLĄD.md` for a first review, `PRZEGLĄD-1.0.md` as the revisioned alternative,
and `PRZEGLĄD-<revision>.md` once a previous review report exists.

When the previous report is a bare `<podstawa>.md` file in the resolved output directory,
it is renamed to `<podstawa>-<rewizja>.md` before the new report is written - for example
`POLOWANIE.md` becomes `POLOWANIE-1.0.md` and the new hunt takes `POLOWANIE-1.1.md`.

## Document Information

The Document Information table uses an empty header row with no column names.

| English              | Polish                  |
|----------------------|-------------------------|
| Document Information | Informacje o dokumencie |
| Report Revision      | Rewizja raportu         |
| Report Date          | Data raportu            |
| State                | Stan                    |
| Detail Level         | Poziom szczegółowości   |
| Evaluation Scale     | Skala oceny             |
| Language             | Język                   |
| Audit Purpose        | Cel audytu              |
| Target Environment   | Środowisko docelowe     |
| Verification Scope   | Zakres weryfikacji      |
| Subject Revision     | Wersja źródeł           |
| Dirty-Tree State     | Stan prac               |
| Report Style         | Styl raportu            |
| Review Scope         | Zakres przeglądu        |
| Evidence Mode        | Tryb dowodów            |
| Skill Version        | Wersja umiejętności     |
| Time taken           | Czas wykonania          |
| Previous Report      | Poprzedni raport        |
| Projects             | Projekty                |

The `Stan` row is written only while the report is `Roboczy`.

It is omitted when the report is final.

The `Stan prac` row is written only when the working tree is dirty.

It is omitted when the tree is clean.

The `Descriptive Mode` row is omitted.

The setting is evident from the presence or absence of the `Słownik` section,
and a re-audit recovers it that way.

Value cells use the Fixed Vocabulary Values table for `State`, `Detail Level`, `Evaluation Scale`,
`Audit Purpose`, `Verification Scope`, `Report Style`, and `Evidence Mode`, and `Polski` for `Language`.

The `Czas wykonania` cell carries the audit run's own duration, identical to the English
report. A Polish rendering produced in a later pass keeps that figure, and when it
records its own generation time instead, the cell annotates the difference, for example
`hh:mm (czas wygenerowania wersji PL - audyt EN: hh:mm)` - a bare mismatch with the
English value is a defect.

## Audit Type Coverage

| English                               | Polish                                  |
|---------------------------------------|-----------------------------------------|
| Audit Type Coverage                   | Zakres typów audytu                     |
| Report type                           | Typ raportu                             |
| Status                                | Status                                  |
| Rationale                             | Uzasadnienie                            |
| Software Architecture Review          | Przegląd architektury oprogramowania    |
| Code Quality Audit                    | Audyt jakości kodu                      |
| Security Vulnerability Assessment     | Ocena podatności bezpieczeństwa         |
| Open Source License Compliance Review | Przegląd zgodności licencji open source |
| Penetration Test                      | Test penetracyjny                       |
| Performance Audit                     | Audyt wydajności                        |
| Cloud Infrastructure Audit            | Audyt infrastruktury chmurowej          |
| AI Governance Audit                   | Audyt zarządzania AI                    |
| Technical Due Diligence               | Techniczne due diligence                |
| SBOM / Software Composition Analysis  | SBOM / analiza składu oprogramowania    |
| ISO/IEC 27001 Certification           | Certyfikacja ISO/IEC 27001              |
| SOC 2 Attestation Examination         | Badanie atestacyjne SOC 2               |

The four coverage statuses render per Status And Severity Vocabulary: `Objęty`,
`Częściowo`, `Niewykonany`, `Nie dotyczy`.

A row classified `Nie dotyczy` is omitted from the table entirely.

SOC 2 is an attestation examination performed by a CPA firm, not a certification -
keep the two rows separate and never write `certyfikacja SOC 2`.

The table records which audit types the report does and does not answer,
and it never claims an assurance level the audit does not define.

An `Audyt zarządzania AI` row omitted as `Nie dotyczy` never suppresses AI-provenance
findings in the `Pochodzenie AI` pillar - the row answers whether governance of an
AI system was assessed, the pillar answers how the source was authored.

## Project Inventory

| English     | Polish  |
|-------------|---------|
| Project     | Projekt |
| Path        | Ścieżka |
| Version     | Wersja  |
| Description | Opis    |

## Glossary

| English    | Polish    |
|------------|-----------|
| Glossary   | Słownik   |
| Term       | Skrót     |
| Definition | Definicja |

Each term cell stays in its original form.

A term cell is a markdown link only when the term carries a longer `###` description below the index
table, pointing to that description's anchor.

Acronym occurrences in the report body link to the description,
or to the index table at `#słownik` when there is none.

Acronyms inside capitalized compound names are not linked,
for example `AI` in `AI Provenance` or `UI` in `Material UI`,
and adjacent acronym pairs such as `NIST RMF` count as one compound.

Definitions and descriptions are written in Polish.

The Słownik mirrors the English glossary term for term - nothing added, nothing dropped.
A term the English glossary does not carry, for example `MR`, is written as plain text
in the body and never takes a `#słownik` link; adding a row to satisfy an invented link
breaks parity in both directions.

Identifier descriptions in `###` subsections prefer short, direct phrasing, for example
`Identyfikatory obowiązują tylko w tym raporcie i w kolejnych wersjach mogą być inne.` and
`Identyfikator zalecenia w planie działań naprawczych`.

Every acronym used anywhere in the report gets a Słownik entry when the term is one the
Słownik defines - acronyms outside its set stay plain text per the mirror rule above.

The entry names the class of the thing precisely - an organization, a standard, a
specification, a framework, a metric set, a file format - not just the expansion:

- `OWASP` is an organization and its project names - `Fundacja OWASP` - never `standard OWASP`.
- `REST` is an architectural style - `styl architektoniczny` - not a contract or a protocol.
- `E2E` names whole-flow tests - `testy całego przepływu` - not a synonym for `UI tests`.
- `API` is `interfejs programowania aplikacji`.
- `ASVS` is `standard weryfikacji bezpieczeństwa aplikacji OWASP`.
- `DORA` is the metrics set - `metryki DORA` - not a process.
- `JWT` is `token JSON podpisany i opcjonalnie szyfrowany`.
- `RBAC` is `kontrola dostępu oparta na rolach`.
- `SSH` is `szyfrowana powłoka i protokół zdalnego dostępu`.
- `UI` is `interfejs użytkownika`.
- `ADR` is `rejestr decyzji architektonicznych` - a decision record, not a directory.
- `NFR` is `wymaganie niefunkcjonalne`.
- `OSS` is `oprogramowanie o otwartym kodzie źródłowym`.
- `RMF` is `ramy zarządzania ryzykiem NIST`.
- `CVE` is `identyfikator konkretnej podatności` - distinguished from `CWE`, which classifies
  weakness types.
- `ISO` is the organization `Międzynarodowa Organizacja Normalizacyjna` and `IEC` is
  `Międzynarodowa Komisja Elektrotechniczna` - separate entries, joint standards carry
  both marks as `ISO/IEC`.
- `TDD` collides with `test-driven development` - spell out `due diligence techniczne`
  in full and never abbreviate it `TDD` in a Polish report.

## Technology Stack

| English          | Polish                              |
|------------------|-------------------------------------|
| Technology Stack | Stos technologiczny                 |
| Layer            | Warstwa                             |
| Technology       | Technologie                         |
| Languages        | Języki                              |
| Frameworks       | Frameworki                          |
| Runtime/Platform | Środowisko uruchomieniowe/Platforma |
| Build tooling    | Narzędzia budowania                 |
| Test tooling     | Narzędzia testowe                   |
| Package manager  | Zarządzanie pakietami               |
| Key libraries    | Kluczowe biblioteki                 |
| Data stores      | Magazyny danych                     |
| Target platforms | Docelowe platformy                  |

## Executive Summary

| English                        | Polish                      |
|--------------------------------|-----------------------------|
| Executive Summary              | Podsumowanie wykonawcze     |
| Field                          | Obszar                      |
| Value                          | Wartość                     |
| System type                    | Typ systemu                 |
| Scope                          | Zakres                      |
| Source basis                   | Źródło danych               |
| Maturity level                 | Poziom dojrzałości          |
| Overall score                  | Wynik ogólny                |
| Summary description            | Opis podsumowujący          |
| Production Readiness Threshold | Próg gotowości produkcyjnej |
| Lowest                         | Najniższy                   |
| Risks                          | Ryzyka                      |
| Readiness                      | Gotowość                    |

## Health Dashboard

| English           | Polish                     |
|-------------------|----------------------------|
| Health Dashboard  | Panel oceny projektu       |
| Risk Map          | Mapa ryzyk                 |
| Impact            | Wpływ                      |
| Likelihood        | Prawdopodobieństwo         |
| Scorecard Summary | Karta oceny - podsumowanie |
| Team & Continuity | Zespół i ciągłość          |

## Scorecard

| English                 | Polish                         |
|-------------------------|--------------------------------|
| Dimension               | Wymiar                         |
| Score                   | Wynik                          |
| Notes                   | Uwagi                          |
| Testability             | Testowalność                   |
| Design Soundness        | Poprawność projektowa          |
| Code Quality            | Jakość kodu                    |
| Stack Alignment         | Zgodność ze stosem             |
| Dependency Health       | Zależności                     |
| Maintainability         | Utrzymywalność                 |
| Deployability           | Zdolność do wdrażania          |
| Scalability             | Skalowalność                   |
| Security                | Bezpieczeństwo                 |
| Compliance              | Zgodność                       |
| Observability           | Obserwowalność                 |
| Operational Safety      | Bezpieczeństwo operacyjne      |
| Delivery & Continuity   | Dostarczanie i ciągłość        |
| AI Provenance           | Pochodzenie AI                 |
| Originality & Licensing | Oryginalność i licencjonowanie |
| Skill Definition        | Definicja umiejętności         |
| API Compatibility       | Zgodność API                   |

## Scoring Rubrics

| English   | Polish    |
|-----------|-----------|
| Excellent | Doskonała |
| Good      | Dobra     |
| Average   | Średnia   |
| Poor      | Słaba     |
| Bad       | Zła       |

| English     | Polish         |
|-------------|----------------|
| Score Range | Zakres wyników |
| Definition  | Definicja      |

The one-line legend preceding a scorecard is labeled `Skala oceny` and names every band of the
selected scale:

- `1-10`: `Skala oceny: 1-3 Słaba · 4-6 Średnia · 7-8 Dobra · 9-10 Doskonała`
- `1-5`: `Skala oceny: 1 Zła · 2 Słaba · 3 Średnia · 4 Dobra · 5 Doskonała`
- `1-3`: `Skala oceny: 1 Słaba · 2 Średnia · 3 Doskonała`
- `5 stars`: `Skala oceny: ★ Zła · ★★ Słaba · ★★★ Średnia · ★★★★ Dobra · ★★★★★ Doskonała`
- `3 stars`: `Skala oceny: ★ Słaba · ★★ Średnia · ★★★ Doskonała`

## Delivery Practice & Team Continuity

| English                             | Polish                                   |
|-------------------------------------|------------------------------------------|
| Delivery Practice & Team Continuity | Praktyka dostarczania i ciągłość zespołu |
| DORA metric                         | Metryka DORA                             |
| Change lead time                    | Czas realizacji zmiany                   |
| Deployment frequency                | Częstotliwość wdrożeń                    |
| Failed deployment recovery time     | Czas odtworzenia po nieudanym wdrożeniu  |
| Change fail rate                    | Wskaźnik nieudanych zmian                |
| Deployment rework rate              | Wskaźnik prac poprawkowych po wdrożeniu  |
| Result                              | Wynik                                    |
| Basis                               | Podstawa                                 |
| Observed / proxy                    | Zmierzone / zastępcze                    |
| Commit-author concentration         | Koncentracja autorstwa commitów          |
| Bus-factor rating                   | Ocena bus factor                         |
| `HIGH`                              | `Wysokie`                                |
| `MODERATE`                          | `Umiarkowane`                            |
| `LOW`                               | `Niskie`                                 |
| Support / cost obligations          | Zobowiązania wsparcia i kosztów          |

Metric cells keep machine-readable `NOT SPECIFIED` rendering as `Nieokreślony`, matching the
fixed-vocabulary treatment of missing organizational data.

## High-Level Observations

| English                 | Polish              |
|-------------------------|---------------------|
| High-Level Observations | Kluczowe obserwacje |
| Observation             | Obserwacja          |

## Auditing Methodology

| English                     | Polish                       |
|-----------------------------|------------------------------|
| Auditing Methodology        | Metodologia audytu           |
| Methodology overview        | Przegląd metodologiczny      |
| Audit evidence statement    | Oświadczenie o dowodach      |
| Severity definitions        | Definicje ważności           |
| Reference standards         | Standardy odniesienia        |
| Severity                    | Ważność                      |
| Impact                      | Wpływ                        |
| Likelihood                  | Prawdopodobieństwo           |
| Blocks Production Readiness | Blokuje gotowość produkcyjną |

## System Context

| English                | Polish                |
|------------------------|-----------------------|
| System Context         | Kontekst systemu      |
| Aspect                 | Aspekt                |
| Detail                 | Szczegóły             |
| Functional description | Opis funkcjonalny     |
| Architecture overview  | Przegląd architektury |
| Key components         | Kluczowe komponenty   |
| External dependencies  | Zależności zewnętrzne |
| Assumptions            | Założenia             |

## Software Bill of Materials

| English                    | Polish                                |
|----------------------------|---------------------------------------|
| Software Bill of Materials | Zestawienie składników oprogramowania |
| Component                  | Komponent                             |
| Version                    | Wersja                                |
| Ecosystem                  | Ekosystem                             |
| Direct/Transitive          | Bezpośredni / przechodni              |
| License                    | Licencja                              |
| License Risk               | Ryzyko licencyjne                     |
| Advisory Checked           | Podatności zweryfikowane              |
| Evidence Source            | Źródło dowodu                         |
| Multi-project SBOM         | Zestawienie wieloprojektowe           |
| SBOM Source                | Źródło zestawienia                    |
| manifest-derived           | wyprowadzone z manifestów             |
| machine-readable SBOM      | maszynowy format zestawienia          |

## License Compliance Review

| English                         | Polish                                  |
|---------------------------------|-----------------------------------------|
| License Compliance Review       | Przegląd zgodności licencyjnej          |
| License class                   | Klasa licencji                          |
| Permissive                      | Permisyjna                              |
| Weak-copyleft                   | Słabe copyleft                          |
| Strong-copyleft                 | Silne copyleft                          |
| Proprietary                     | Własnościowa                            |
| License compatibility           | Zgodność licencji                       |
| Notice / attribution            | Nota licencyjna / przypisanie autorstwa |
| Source provenance               | Pochodzenie kodu                        |
| Ownership / assignment evidence | Dowód własności / cesji praw            |
| Copyleft linkage conflict       | Konflikt powiązania copyleft            |

License-class cells use the feminine adjective forms shown, agreeing with `licencja`.

## Architectural Assessment

| English                  | Polish             |
|--------------------------|--------------------|
| Architectural Assessment | Ocena architektury |
| Design Principles        | Zasady projektowe  |

## Architectural Subsections

| English                       | Polish                             |
|-------------------------------|------------------------------------|
| What Works                    | Co działa                          |
| What Needs Attention          | Co wymaga uwagi                    |
| Data Flow Diagram             | Diagram przepływu danych           |
| Design Patterns               | Wzorce projektowe                  |
| Architecture Decision Records | Rejestr decyzji architektonicznych |
| ADR                           | ADR                                |
| Industry Baseline Comparison  | Porównanie z praktyką branżową     |

`Rejestr decyzji architektonicznych` is the in-section label. Where the decisions list stands as
a main section, `Decyzje architektoniczne` is also correct.

## Skill Definition Conformance

| English                      | Polish                          |
|------------------------------|---------------------------------|
| Skill Definition Conformance | Zgodność definicji umiejętności |
| Skills Inventory             | Inwentaryzacja umiejętności     |
| Agent Artifacts              | Artefakty agentowe              |

## Agent Guidance Conformance

| English                    | Polish                         |
|----------------------------|--------------------------------|
| Agent Guidance Conformance | Zgodność wytycznych agentowych |
| Guidance inventory         | Inwentaryzacja wytycznych      |
| Entry route                | Ścieżka wejścia                |
| Index of record            | Indeks podstawowy              |
| Consolidated topology      | Topologia scalona              |
| Owner selection            | Dobór właściciela              |
| Role resolution            | Rozwiązanie ról                |
| Restricted directories     | Katalogi zastrzeżone           |
| Vendored documents         | Dokumenty dołączone            |

## AI System Assessment

| English                 | Polish                    |
|-------------------------|---------------------------|
| AI System Assessment    | Ocena systemu AI          |
| Model provenance        | Pochodzenie modelu        |
| Data provenance         | Pochodzenie danych        |
| Evaluation evidence     | Dowody ewaluacji          |
| Safety controls         | Kontrole bezpieczeństwa   |
| Monitoring and rollback | Monitorowanie i wycofanie |

## Standards Conformance

| English                | Polish                    |
|------------------------|---------------------------|
| Standards Conformance  | Zgodność ze standardami   |
| Standards inventory    | Inwentaryzacja standardów |
| Document               | Dokument                  |
| Path                   | Ścieżka                   |
| Stack Coverage         | Zakres stosu              |
| Code conformance       | Zgodność kodu             |
| Area                   | Obszar                    |
| Standard Rule          | Reguła standardu          |
| Standards quality      | Jakość standardów         |
| Standards Position     | Pozycja standardu         |
| External Best Practice | Zewnętrzna dobra praktyka |
| Alignment              | Zgodność                  |
| Aligned                | Zgodne                    |
| Partially aligned      | Częściowo zgodne          |
| Partially              | Częściowo                 |
| Diverges               | Rozbieżne                 |

## Engineering Baseline Conformance

| English                          | Polish                          |
|----------------------------------|---------------------------------|
| Engineering Baseline Conformance | Zgodność z podstawą inżynierską |
| Baseline                         | Podstawa                        |
| Applicability                    | Dotyczy                         |
| Runtime/toolchain pinning        | Przypięcie wykonania/toolchainu |
| Dependency reproducibility       | Powtarzalność zależności        |
| Lint/format gate                 | Brama lint/format               |
| Test floor                       | Podstawa testowa                |
| Secrets hygiene                  | Higiena sekretów                |
| CLI output contract              | Kontrakt wyjścia CLI            |

## References

| English             | Polish            |
|---------------------|-------------------|
| References          | Podstawy oceny    |
| Reference           | Odniesienie       |
| Publisher or Author | Wydawca lub autor |
| Used In             | Zastosowane w     |

## Strengths And What's Working

| English                    | Polish                   |
|----------------------------|--------------------------|
| Strengths & What's Working | Mocne strony i co działa |

## Detailed Technical Findings

| English                     | Polish                           |
|-----------------------------|----------------------------------|
| Detailed Technical Findings | Szczegółowe ustalenia techniczne |
| Summary table               | Tabela podsumowania              |
| Finding                     | Ustalenie                        |
| Pillar                      | Filar                            |
| Severity                    | Ważność                          |
| Title                       | Tytuł                            |
| Result                      | Wynik                            |
| Status                      | Status                           |
| Change                      | Zmiana                           |
| Verification                | Weryfikacja                      |
| Type                        | Typ                              |
| Security                    | Bezpieczeństwo                   |
| Targets                     | Obiekty                          |
| Basis                       | Podstawa                         |
| Absence                     | Charakter odstępstwa             |
| Description                 | Opis                             |
| Impact                      | Wpływ                            |
| Recommendation              | Zalecenie                        |
| Method                      | Metoda                           |
| Verified                    | Zweryfikowane                    |
| Runtime confirmed           | Potwierdzone uruchomieniem       |
| Breaking change             | Łamanie kompatybilności          |
| Applicability               | Dotyczy                          |
| Confidence                  | Pewność oceny                    |
| Mitigating factors          | Czynniki łagodzące               |
| Exploitability              | Wykorzystanie podatności         |
| Evidence                    | Dowód                            |

The `Zweryfikowane` field takes the value `tak` or `nie` followed by the evidence note, for
example `* **Zweryfikowane:** tak - obserwacja w źródłach`.

The `Potwierdzone uruchomieniem` field takes `tak`, `nie`, or `nie dotyczy`, and it never
renders a calque that leaves a bare `Runtime` before a Polish noun.

The `Łamanie kompatybilności` field takes `Brak`, `wewnętrzne`, or `publiczne API`, and the
`Dotyczy` field takes `dotyczy`, `warunkowe`, `nie dotyczy`, or `niezweryfikowane`.
`Pewność oceny` and `Wykorzystanie podatności` carry the same title-case token values as
every other field (`Wysoka`, `Teoretyczne`), and `Ważność`, `Status`, `Zmiana`, `Typ`,
and `Charakter odstępstwa` take title-case phrases
(`Wysoka`, `Otwarty`, `Nowa`, `Obserwacja`, `Nieokreślony`).

The exploitability narrative labels translate as `Warunek wstępny:`, `Ścieżka:`, `Wpływ:`, and
`Niepewność:` - they are part of the narrative prose, not fixed tokens.

### Pillar Names

| English                                   | Polish                                  |
|-------------------------------------------|-----------------------------------------|
| Architecture & Design                     | Architektura i projektowanie            |
| Structure & Organization                  | Struktura i organizacja                 |
| Code Quality                              | Jakość kodu                             |
| Security & Compliance                     | Bezpieczeństwo i zgodność               |
| Infrastructure & CI/CD                    | Infrastruktura i CI/CD                  |
| AI Provenance & Code Origin               | Pochodzenie AI i kod                    |
| Copyrights & Originality                  | Prawa autorskie i oryginalność          |
| API Compatibility & Versioning Discipline | Zgodność API i dyscyplina wersjonowania |

## Technical Debt Register

| English  | Polish    |
|----------|-----------|
| Debt     | Dług      |
| Item     | Pozycja   |
| Category | Kategoria |
| Source   | Źródło    |
| Cost     | Koszt     |
| Delay    | Zwłoka    |
| Status   | Status    |

## Unified Risk Register

| English               | Polish                      |
|-----------------------|-----------------------------|
| Unified Risk Register | Jednolity rejestr ryzyk     |
| Risk                  | Ryzyko                      |
| Description           | Opis                        |
| Source                | Źródło                      |
| Impact                | Wpływ                       |
| Likelihood            | Prawdopodobieństwo          |
| Severity              | Ważność                     |
| Mitigation            | Środek ograniczający ryzyko |
| Confidence            | Pewność oceny               |
| Trigger               | Wyzwalacz                   |
| Controls              | Mechanizmy kontrolne        |
| Residual              | Ryzyko rezydualne           |
| Status                | Status                      |
| Owner                 | Właściciel                  |
| Closure               | Zamknięcie                  |

## Trade-off Analysis

| English               | Polish                |
|-----------------------|-----------------------|
| Trade-off Analysis    | Przegląd kompromisów  |
| Trade-off             | Kompromis             |
| Context               | Kontekst              |
| Option A: gain / cost | Opcja A: zysk / koszt |
| Option B: gain / cost | Opcja B: zysk / koszt |
| Evidence              | Dowód                 |
| Implication           | Implikacja            |

## Actionable Remediation Roadmap

| English                        | Polish                   |
|--------------------------------|--------------------------|
| Actionable Remediation Roadmap | Plan działań naprawczych |
| Rec                            | Identyfikator zalecenia  |
| Priority                       | Priorytet                |
| Finding                        | Ustalenie                |
| Recommendation                 | Zalecenie                |
| Impact                         | Wpływ                    |
| Effort                         | Wysiłek                  |
| Complexity                     | Złożoność                |
| Verification                   | Weryfikacja              |
| Breaking                       | Łamanie                  |

## Recommendation Classification

| English                       | Polish                  |
|-------------------------------|-------------------------|
| Recommendation Classification | Klasyfikacja zaleceń    |
| Rec                           | Identyfikator zalecenia |
| Recommendation                | Zalecenie               |
| Class                         | Klasa                   |
| Basis                         | Podstawa                |
| Recommended                   | Zalecana                |
| Optional                      | Opcjonalna              |
| Not recommended               | Niezalecana             |

Wartość `Undetermined` w polu `Charakter odstępstwa` przyjmuje formę `Nieokreślony`.

## Changes Since Previous Audit

| English                      | Polish                        |
|------------------------------|-------------------------------|
| Changes Since Previous Audit | Zmiany od poprzedniego audytu |
| Field                        | Obszar                        |
| Previous Report              | Poprzedni raport              |
| Current Report               | Bieżący raport                |
| File                         | Plik                          |
| Revision                     | Rewizja                       |
| Version                      | Wersja                        |
| Date                         | Data                          |
| Detail level                 | Poziom szczegółowości         |
| Evaluation scale             | Skala oceny                   |
| Finding transitions          | Zmiany ustaleń                |
| Change                       | Zmiana                        |
| Finding                      | Ustalenie                     |
| Previous                     | Poprzedni                     |
| Current                      | Bieżący                       |
| Note                         | Uwaga                         |
| Score delta                  | Zmiana wyników                |
| Dimension                    | Wymiar                        |
| Direction                    | Kierunek                      |
| Up                           | W górę                        |
| Down                         | W dół                         |
| Unchanged                    | Niezmieniona                  |
| New                          | Nowa                          |
| Reopened                     | Wznowiona                     |
| Open                         | Otwarty                       |
| Closed                       | Zamknięta / Zamknięty         |
| Verified                     | Zweryfikowana                 |
| Confirmed                    | Potwierdzona                  |
| Reported                     | Zadeklarowana                 |

## Scope Exclusions

| English          | Polish             |
|------------------|--------------------|
| Scope Exclusions | Wyłączenia raportu |
| Scope            | Zakres             |
| Justification    | Uzasadnienie       |

## Limitations And Unknowns

| English                  | Polish                    |
|--------------------------|---------------------------|
| Limitations and Unknowns | Ograniczenia i niewiadome |
| Item                     | Pozycja                   |
| Type                     | Typ                       |
| Unrun check              | Niewykonana kontrola      |
| Unknown                  | Niewiadoma                |
| Reason                   | Powód                     |
| Resolution               | Rozwiązanie               |

A `Rejestr sprzeczności` block inside this section or a standalone section in the
`polowanie na usterki` and `sprawdzenie` styles renders its columns as `Temat`,
`Ten audyt`, `Stwierdzenie zewnętrzne`, `Wskazania dowodów`, and `Status`, with status
values `Potwierdzone`, `Obalone`, `Nieodtwarzalne`, or `Oczekujące`.

## Re-audit And Follow-up Plan

| English                 | Polish                     |
|-------------------------|----------------------------|
| Finding                 | Ustalenie                  |
| Priority                | Priorytet                  |
| Verification Owner      | Właściciel weryfikacji     |
| Closure Evidence        | Dowód zamknięcia           |
| Target Re-audit Trigger | Wyzwalacz ponownego audytu |

## Operator Verification Handoff

| English                       | Polish                              |
|-------------------------------|-------------------------------------|
| Operator Verification Handoff | Przekazanie weryfikacji operatorowi |
| Check                         | Kontrola                            |
| Finding                       | Ustalenie                           |
| Command                       | Polecenie                           |
| Expected evidence             | Oczekiwany dowód                    |

The handoff lists runtime checks the operator can run to convert `Potwierdzone uruchomieniem:
nie` findings into executed evidence.

## Executed Evidence Log

| English               | Polish                     |
|-----------------------|----------------------------|
| Executed Evidence Log | Rejestr dowodów wykonanych |
| Command               | Polecenie                  |
| Version               | Wersja                     |
| Scope                 | Zakres                     |
| Exit status           | Kod wyjścia                |
| Artifact              | Artefakt                   |

The log records every bounded execution a `wykonanie tylko do odczytu` report performed.

## Hunt Style Sections

| English                  | Polish                       |
|--------------------------|------------------------------|
| Verdict                  | Werdykt                      |
| Domain Ratings           | Oceny domen                  |
| Rating                   | Ocena                        |
| Basis                    | Podstawa                     |
| Journey Traces           | Ślady ścieżek funkcjonalnych |
| Domain Findings          | Ustalenia domenowe           |
| Risk Register            | Rejestr ryzyk                |
| Remediation Phases       | Fazy naprawcze               |
| Contradiction Register   | Rejestr sprzeczności         |
| Methodology And Evidence | Metodologia i dowody         |
| Domain                   | Domena                       |
| Journey                  | Ścieżka                      |
| Phase                    | Faza                         |
| Window                   | Okno                         |

The `Werdykt` paragraph takes `Gotowy`, `Warunkowo gotowy`, or `Niegotowy`, and a hard
readiness gate renders `Spełniona`, `Niespełniona`, or `Nieoceniona`.

The fixed domains render `Poprawność`, `Bezpieczeństwo`, `Niezawodność`, `Wydajność`,
`Zależności`, `Wdrożenie`, `Testowalność`, `Dokumentacja`, `Utrzymywalność`, and `Pochodzenie`,
with ratings `Czerwona`, `Bursztynowa`, `Zielona`, or `Nieoceniona` agreeing with `ocena`.

A `polowanie na usterki` report replaces the scorecard and recommendation classification with
domain verdicts and remediation phases, and `Kontekst systemu` carries the project discovery.

## Review Style Sections

| English                    | Polish                      |
|----------------------------|-----------------------------|
| Check Plan And Methodology | Plan kontroli i metodologia |
| Execution Register         | Rejestr wykonania           |
| Check                      | Kontrola                    |
| Command                    | Polecenie                   |
| Interpretation             | Interpretacja               |
| Artifact                   | Artefakt                    |
| Improvement Plan           | Plan poprawy                |
| Retest Register            | Rejestr retestów            |
| Metrics Snapshot           | Zestawienie metryk          |
| Artifact Manifest          | Manifest artefaktów         |
| Evidence level             | Poziom dowodu               |
| Defect scenario            | Scenariusz usterki          |
| Disposition                | Dyspozycja                  |
| Contradiction Register     | Rejestr sprzeczności        |
| Appendix                   | Załącznik                   |

A `przegląd` report replaces the scorecard and recommendation classification with the
execution register and improvement plan. Its `Werdykt` paragraph takes the same `Gotowy`,
`Warunkowo gotowy`, or `Niegotowy` values as `polowanie na usterki`. An optional appendix
heading renders `Załącznik <litera>: <tytuł>`. The `Rejestr wykonania` `Wynik` column carries
`OK`, `Niezaliczony`, `Błąd`, `Zablokowany`, `Pominięty`, `Nieuruchomiony`, or `N/D` -
the masculine forms agree with `wynik`. The `Dyspozycja` column carries `Zaplanowana`,
`Odroczona`, `Zaakceptowana - brak działania`, or `Nierozstrzygnięta`. A `Poziom dowodu`
field takes `Źródło`, `Model`, `Aplikacja`, `Wdrożenie`, or `Nieznany`, and a permitted-use
profile renders `laboratoryjny`, `kontrolowane udostępnienie`, or `produkcyjny`.

## Validation Record

| English                  | Polish                      |
|--------------------------|-----------------------------|
| Validation Record        | Weryfikacja raportu         |
| Check                    | Kontrola                    |
| Result                   | Wynik                       |
| Evidence / Justification | Dowód / uzasadnienie        |
| Applied                  | Zastosowany                 |
| Parity baseline          | Punkt odniesienia zgodności |

The `Weryfikacja raportu` carries rows `PAR-1` through `PAR-20` in fixed order.
`PAR-18` renders `N/D` under `Styl raportu: polowanie na usterki` or `przegląd` - neither
style carries a `Klasyfikacja zaleceń` section - and `PAR-20` renders `N/D` under
`polowanie na usterki`, which never runs the structure assessment.

A Polish report mirrors the English Validation Record row for row - the same checks in
the same order, no rows added or dropped, and check names and justifications rendered in
Polish. Tool names in evidence text stay as the English record names them
(`lint-prose.py`, `validate-report.py`, `format-table.py`).

Polish-language quality checks run as pre-delivery gates and never earn report rows:

- a spell-check pass over the rendered Polish text,
- `scripts/lint-polish.py` reporting zero errors,
- a sentence-length review against the Style Rules limits,
- reconciliation of every number and status in prose against the tables,
- verbatim agreement between summary-table titles and their `### FND-…`/`### REC-…`
  headings.

Where a row records translation parity, its evidence states `tokeny maszynowe
przetłumaczone, parytet strukturalny zachowany` - never a claim of preserved English
tokens, which the Polish token vocabulary contradicts.

## Threat Model

| English            | Polish               |
|--------------------|----------------------|
| Boundary           | Granica zaufania     |
| STRIDE             | STRIDE               |
| Threat Description | Opis zagrożenia      |
| Control            | Środek ograniczający |
| Finding            | Ustalenie            |

## API Contract Conformance

| English                  | Polish             |
|--------------------------|--------------------|
| API Contract Conformance | Zgodność kontraktu |
| Dimension                | Wymiar             |
| Status                   | Status             |
| Evidence                 | Dowód              |

## API Compatibility And Versioning Discipline

| English                                   | Polish                                  |
|-------------------------------------------|-----------------------------------------|
| API Compatibility & Versioning Discipline | Zgodność API i dyscyplina wersjonowania |
| Dimension                                 | Wymiar                                  |
| Status                                    | Status                                  |
| Evidence                                  | Dowód                                   |

## Evidence And Decision Terms

Translate prose labels below, while preserving machine tokens such as `EVD-001`, CWE IDs, CVSS
vectors, tool commands, and execution-state codes.

| English                          | Polish                            |
|----------------------------------|-----------------------------------|
| Evidence And Decision Limits     | Dowody i ograniczenia decyzji     |
| Verification And Evidence Ledger | Rejestr dowodów audytowych        |
| Evidence                         | Dowód                             |
| Check / Source                   | Kontrola / źródło                 |
| Result                           | Wynik                             |
| Artifact                         | Artefakt                          |
| Basis                            | Podstawa                          |
| Absence                          | Charakter odstępstwa              |
| Confidence                       | Pewność oceny                     |
| Verified                         | Zweryfikowane                     |
| Mitigating factors               | Czynniki łagodzące                |
| Security                         | Bezpieczeństwo                    |
| Inspected                        | Zweryfikowany                     |
| Reported                         | Zadeklarowany                     |
| Inferred                         | Wniosekowany                      |
| Readiness Cost                   | Koszt osiągnięcia gotowości       |
| Operational Objectives           | Cele operacyjne                   |
| Due Diligence Coverage           | Zakres weryfikacji                |
| Work Item                        | Pakiet prac                       |
| Source Recommendations           | Zalecenia źródłowe                |
| Effort Range                     | Zakres nakładu pracy              |
| Basis                            | Podstawa                          |
| Dependencies                     | Zależności                        |
| Metric                           | Metryka                           |
| Target                           | Cel                               |
| Measured Result                  | Wynik pomiaru                     |
| Window                           | Okres pomiaru                     |
| Source                           | Źródło                            |
| Owner                            | Właściciel                        |
| Concern                          | Obszar ryzyka                     |
| Missing Artifact / Next Step     | Brakujący artefakt / kolejny krok |
| Meaning                          | Znaczenie                         |
| Readiness Treatment              | Obsługa gotowości produkcyjnej    |
| Quality Characteristic           | Charakterystyka jakości           |
| Lens Evidence                    | Dowody w Lens                     |
| Functional Suitability           | Przydatność funkcjonalna          |
| Performance Efficiency           | Efektywność wydajnościowa         |
| Compatibility                    | Kompatybilność                    |
| Interaction Capability           | Zdolność interakcji               |
| Reliability                      | Niezawodność                      |
| Flexibility                      | Elastyczność                      |
| Safety                           | Bezpieczeństwo przed szkodami     |
| Support Continuity               | Ciągłość wsparcia                 |
| Ownership Cost                   | Koszt utrzymania                  |
| Roadmap Feasibility              | Wykonalność planu rozwoju         |
| Supplier Continuity              | Ciągłość dostawcy                 |
| IP Rights                        | Prawa własności intelektualnej    |
| Data Obligations                 | Obowiązki dotyczące danych        |

Result markers produced by the audit render in Polish: `Nieuruchomiony`, `Nieoceniony`,
`Niezbadany`, `Nieokreślony`, `Poza zakresem`, `Niewystarczające informacje`, and `N/D`.

Record identifiers, CWE IDs, CVSS vectors, tool commands, and code stay unchanged.

## Skill Definition Conformance Table

| English    | Polish         |
|------------|----------------|
| Dimension  | Wymiar         |
| Status     | Status         |
| Evidence   | Dowód          |
| Skill      | Umiejętność    |
| Path       | Ścieżka        |
| Name Match | Zgodność nazwy |
| Key Gaps   | Kluczowe luki  |
| Artifact   | Artefakt       |
| Type       | Typ            |
| Notes      | Uwagi          |

## Structure Review

The structure review content defined in `process/report-format/structure-review.md` renders
in Polish with the mappings below.

| English                     | Polish                        |
|-----------------------------|-------------------------------|
| Structure Review            | Przegląd struktury            |
| Project Context             | Kontekst projektu             |
| Structural Overview         | Przegląd struktury projektu   |
| Findings                    | Ustalenia                     |
| Positive Practices          | Pozytywne praktyki            |
| Recommendations             | Zalecenia                     |
| Prioritization              | Priorytetyzacja               |
| Limitations and Assumptions | Ograniczenia i założenia      |
| Review Scope                | Zakres przeglądu              |
| Structure                   | Struktura                     |
| Directory organization      | Organizacja katalogów         |
| Naming conventions          | Konwencje nazewnicze          |
| Component placement         | Rozmieszczenie komponentów    |
| Supporting-artifact layout  | Układ artefaktów pomocniczych |
| Consistency                 | Spójność                      |
| Level                       | Poziom                        |
| Directory                   | Katalog                       |
| Contents                    | Zawartość                     |
| Role                        | Rola                          |
| Area                        | Obszar                        |
| Verdict                     | Werdykt                       |
| Necessary                   | Konieczne                     |
| Meaningful                  | Znaczące                      |
| Optional                    | Opcjonalne                    |
| Practice                    | Praktyka                      |
| Evidence                    | Dowód                         |
| Recommendation              | Zalecenie                     |
| Rationale                   | Uzasadnienie                  |
| Addresses                   | Odnosi się do                 |

Verdict cells in the `Werdykt` column render `OK`, `Częściowo`, `Niezaliczony`, `Nieznany`,
or `N/D`, and `FND-STR-` identifiers stay unchanged.

A `przegląd` request scoped to a change set - a commit range, pull or merge request, or
branch diff - produces a standard review-style report scoped to that change set, with the
range recorded in the `Zakres przeglądu` row of `Informacje o dokumencie`.
