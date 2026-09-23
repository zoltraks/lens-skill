# Polish Translation

## Purpose

> **Scope:** Polish rendering of the audit report and parameter prompts: analysis model, status
> and severity vocabulary, fixed vocabulary values, terminology dictionary, prompt phrasing,
> section headings, table headers, style rules, encoding, and diacritics preservation
> **Key items:** English-first analysis, translation tables, terminology dictionary, prompt
> phrasing, status and severity mapping, style rules, diacritics

This file defines the Polish rendering of the audit report and of the parameter-configuration
prompts. When the report language is Polish, apply every translation and rule in this file to the
corresponding English terms.

The default report language is English. This file is loaded only when the report language is
Polish.

## Contents

| Section                                     | Line | What it covers                              |
|---------------------------------------------|------|---------------------------------------------|
| Analysis And Rendering                      | 68   | Analysis model and terminology precedence   |
| Status And Severity Vocabulary              | 86   | Status And Severity Vocabulary guidance     |
| Fixed Vocabulary Values                     | 150  | Polish renderings of descriptive values     |
| Terminology                                 | 188  | English to Polish technical dictionary      |
| Parameter Prompts                           | 303  | Polish phrasing for configuration questions |
| Style Rules                                 | 328  | Style Rules guidance                        |
| Diacritics Frequently Misspelled            | 396  | Diacritics Frequently Misspelled guidance   |
| Output Filename                             | 430  | Output Filename guidance                    |
| Document Information                        | 439  | Document Information guidance               |
| Audit Type Coverage & Assurance Matrix      | 467  | Coverage and assurance rendering            |
| Project Inventory                           | 490  | Project Inventory guidance                  |
| Glossary                                    | 499  | Glossary guidance                           |
| Technology Stack                            | 514  | Technology Stack guidance                   |
| Executive Summary                           | 531  | Executive Summary guidance                  |
| Health Dashboard                            | 549  | Health Dashboard guidance                   |
| Scorecard                                   | 560  | Scorecard guidance                          |
| Scoring Rubrics                             | 585  | Scoring Rubrics guidance                    |
| Delivery Practice & Team Continuity         | 609  | Delivery and continuity rendering           |
| High-Level Observations                     | 633  | High-Level Observations guidance            |
| Auditing Methodology                        | 640  | Auditing Methodology guidance               |
| System Context                              | 654  | System Context guidance                     |
| Software Bill of Materials                  | 667  | SBOM section rendering                      |
| License & IP Compliance Review              | 685  | License and IP section rendering            |
| Architectural Assessment                    | 703  | Architectural Assessment guidance           |
| Architectural Subsections                   | 710  | Architectural Subsections guidance          |
| Skill Definition Conformance                | 721  | Skill Definition Conformance guidance       |
| AI System Assessment                        | 727  | AI System Assessment guidance               |
| Standards Conformance                       | 738  | Standards Conformance guidance              |
| References                                  | 759  | References guidance                         |
| Strengths And What's Working                | 768  | Strengths And What's Working guidance       |
| Detailed Technical Findings                 | 774  | Detailed Technical Findings guidance        |
| Technical Debt Register                     | 806  | Technical Debt Register guidance            |
| Unified Risk Register                       | 818  | Unified Risk Register guidance              |
| Trade-off Analysis                          | 839  | Trade-off Analysis guidance                 |
| Actionable Remediation Roadmap              | 851  | Actionable Remediation Roadmap guidance     |
| Changes Since Previous Audit                | 865  | Changes Since Previous Audit guidance       |
| Scope Exclusions                            | 894  | Scope Exclusions guidance                   |
| Limitations And Unknowns                    | 902  | Limitations And Unknowns guidance           |
| Re-audit And Follow-up Plan                 | 914  | Re-audit And Follow-up Plan guidance        |
| Validation Record                           | 924  | Validation Record guidance                  |
| Threat Model                                | 935  | Threat Model guidance                       |
| API Contract Conformance                    | 944  | API Contract Conformance guidance           |
| API Compatibility And Versioning Discipline | 952  | API Compatibility And Versioning guidance   |
| Evidence And Decision Terms                 | 961  | Evidence And Decision Terms guidance        |
| Skill Definition Conformance Table          | 1021 | Skill Definition Conformance Table guidance |

## Analysis And Rendering

Analysis runs in English regardless of the report language. Evidence notes, finding drafts,
partial conclusions, and assembled part files are written in English, and the report is rendered
into Polish in a single pass that applies this file.

Reasoning in English keeps the analysis anchored to the English rules, rubrics, and fixed
vocabularies in the rest of the skill, and a single render pass applies one terminology convention
to the whole document.

When the audited project establishes its own Polish terminology, for example a project glossary or
Polish design documents, prefer those established forms over the defaults in this file and record
the choice.

Direct quotes, code, configuration keys, file paths, identifiers, and record IDs are never
translated. Fixed report tokens - statuses, severities, and execution states - render in Polish
per Status And Severity Vocabulary.

## Status And Severity Vocabulary

Fixed report tokens render in Polish in the report body. The English forms remain the analysis
and validation vocabulary - mechanical checks run on the English-mapped working copy.

Statuses and execution states use fixed label forms:

| English token              | Polish render                 |
|----------------------------|-------------------------------|
| `PASS`                     | `OK`                          |
| `PARTIAL`                  | `CZĘŚCIOWO`                   |
| `FAIL`                     | `NIEZALICZONE`                |
| `UNKNOWN`                  | `NIEZNANE`                    |
| `N/A`                      | `N/D`                         |
| `ERROR`                    | `BŁĄD`                        |
| `NOT RUN`                  | `NIEURUCHOMIONE`              |
| `NOT ASSESSED`             | `NIEOCENIONE`                 |
| `NOT INSPECTED`            | `NIEZBADANE`                  |
| `NOT COLLECTED`            | `NIEZEBRANE`                  |
| `EXCLUDED BY SCOPE`        | `POZA ZAKRESEM`               |
| `INSUFFICIENT INFORMATION` | `NIEWYSTARCZAJĄCE INFORMACJE` |
| `SEVERITY:`                | `WAŻNOŚĆ:`                    |
| `Score:`                   | `Wynik:`                      |
| `Covered`                  | `OBJĘTE`                      |
| `Partially`                | `CZĘŚCIOWO`                   |
| `Not done`                 | `NIEWYKONANE`                 |
| `Not Applicable`           | `NIE DOTYCZY`                 |
| `Observation`              | `OBSERWACJA`                  |
| `Concern`                  | `ZASTRZEŻENIE`                |
| `Theoretical`              | `TEORETYCZNY`                 |
| `Static-Confirmed`         | `POTWIERDZONE STATYCZNIE`     |
| `Dynamically-Verified`     | `ZWERYFIKOWANE DYNAMICZNIE`   |

`Observation` and `Concern` are the evidence/finding type tags. In `* **Field:**` bullet lists
they render title-cased `Obserwacja`/`Zastrzeżenie`. The Due Diligence Coverage column named
`Concern` keeps its separate rendering `Obszar ryzyka`, the two uses are not the same word's
job.

Severity agrees in gender with the governed noun: feminine for `ważność`, `pewność`, and
`złożoność`, masculine for `wpływ`, `priorytet`, and `wysiłek`, neuter for `prawdopodobieństwo`
and `ryzyko`.

| English    | Feminine  | Masculine | Neuter    |
|------------|-----------|-----------|-----------|
| `CRITICAL` | KRYTYCZNA | KRYTYCZNY | KRYTYCZNE |
| `HIGH`     | WYSOKA    | WYSOKI    | WYSOKIE   |
| `MEDIUM`   | ŚREDNIA   | ŚREDNI    | ŚREDNIE   |
| `LOW`      | NISKA     | NISKI     | NISKIE    |

In prose, decline the token naturally: `ustalenia o ważności WYSOKIEJ`, `na poziomie WYSOKIM`,
`ryzyko NISKIE`.

Token columns in tables (`Ważność`, `Wpływ`, `Status`, `Wykonanie`, `Wynik`) and token-definition
tables use the uppercase forms. In `* **Field:**` bullet lists, values use title case consistent
with neighboring values, for example `Ważność: Wysoka` next to `Status: Otwarte` - never `NISKIE`
next to `Otwarte`.

Record identifiers (`FND-001`, `EVD-042`, `RSK-010`), priority codes (`P1`-`P4`), `CWE-####`,
CVSS vectors, commands, and anything inside verbatim evidence stay unchanged.

When the `1-5` or `1-3` numeric scale is selected, use `Wynik: X/5` or `Wynik: X/3`.

When `5 stars` or `3 stars` is selected, use `Wynik:` followed by the unchanged star bar.

## Fixed Vocabulary Values

Descriptive values are rendered in Polish and agree in gender with the noun they describe:
`wpływ`, `wysiłek`, and `priorytet` take `Wysoki`/`Średni`/`Niski`, `złożoność` and `ważność`
take `Wysoka`/`Średnia`/`Niska`, `prawdopodobieństwo` and `ryzyko` take `Wysokie`/`Średnie`/`Niskie`.

| English                   | Polish                                   |
|---------------------------|------------------------------------------|
| `Draft`                   | `Roboczy`                                |
| `Final`                   | `Gotowy`                                 |
| `Detailed`                | `Szczegółowy`                            |
| `Standard`                | `Standardowy`                            |
| `Brief`                   | `Skrócony`                               |
| `5 stars`                 | `5 gwiazdek`                             |
| `3 stars`                 | `3 gwiazdki`                             |
| `Enabled`                 | `Włączony` or `Aktywny`                  |
| `Error`                   | `Błąd`                                   |
| `Disabled`                | `Wyłączony`                              |
| `Prototype`               | `Prototyp`                               |
| `Early development`       | `Wczesny rozwój`                         |
| `Pre-production`          | `Etap przedprodukcyjny`                  |
| `Production-ready`        | `Gotowość produkcyjna`                   |
| `Undetermined`            | `Nieokreślony`                           |
| `Ready`                   | `Gotowy`                                 |
| `Not ready`               | `Niegotowy`                              |
| `Pending evidence`        | `Oczekuje na dowody`                     |
| `Not assessed`            | `Nieoceniony`                            |
| `Full`                    | `Pełna`                                  |
| `Partial`                 | `Częściowa`                              |
| `None`                    | `Brak`                                   |
| `Not applicable`          | `nie dotyczy`                            |
| `source-only`             | `wyłącznie na podstawie kodu źródłowego` |
| `engineering improvement` | `doskonalenie inżynieryjne`              |
| `production readiness`    | `gotowość produkcyjna`                   |
| `technical due diligence` | `due diligence techniczne`               |

Numeric scales `1-10`, `1-5`, and `1-3` stay unchanged.

## Terminology

The dictionary maps recurring English technical terms to their preferred Polish forms. Entries
with two forms separated by `/` are context-dependent, pick the form that fits the sentence rather
than always translating the same English word identically.

| English                                | Polish                                                           |
|----------------------------------------|------------------------------------------------------------------|
| AI-assisted development workflow       | proces wytwarzania oprogramowania wspomagany przez AI            |
| access token                           | token dostępu                                                    |
| API contract validation                | kontrola poprawności kontraktu API                               |
| attack path                            | ścieżka ataku                                                    |
| attack surface                         | powierzchnia ataku                                               |
| assurance                              | zapewnienie                                                      |
| attribution                            | przypisanie autorstwa                                            |
| authoritative source                   | źródło autorytatywne                                             |
| automated compliance check/enforcement | automatyczna weryfikacja zgodności                               |
| automated enforcement                  | automatyczne egzekwowanie reguł                                  |
| backup restore                         | odtworzenie z kopii zapasowej                                    |
| backup restore test                    | test odtwarzania kopii zapasowej                                 |
| backup retention                       | retencja kopii zapasowych                                        |
| build                                  | proces budowania                                                 |
| build artifact                         | artefakt wynikowy / artefakt wdrożeniowy                         |
| build job                              | zadanie budowania                                                |
| build reproducibility                  | powtarzalność procesu budowania                                  |
| bus factor                             | czynnik autobusowy                                               |
| code provenance                        | pochodzenie kodu                                                 |
| code provenance traceability           | identyfikowalność pochodzenia kodu                               |
| Common Weakness Enumeration            | klasyfikacja typowych błędów bezpieczeństwa oprogramowania       |
| concern (evidence/finding tag)         | zastrzeżenie                                                     |
| contract test                          | test zgodności kontraktu / test kontraktowy                      |
| contract/implementation mismatch       | rozbieżność między kontraktem a implementacją                    |
| copyleft                               | copyleft (nie tłumaczyć)                                         |
| credentials                            | poświadczenia                                                    |
| demo credentials                       | poświadczenia demonstracyjne                                     |
| delivery practice                      | praktyka dostarczania                                            |
| dependency analysis                    | analiza zależności                                               |
| dependency vulnerability scanning      | analiza podatności zależności / skanowanie podatności zależności |
| deploy                                 | wdrażać                                                          |
| deployability                          | zdolność do wdrażania                                            |
| deployment                             | wdrożenie                                                        |
| deployment gate                        | warunek dopuszczenia do wdrożenia                                |
| deployment job                         | zadanie wdrożeniowe                                              |
| documentation drift                    | rozbieżność dokumentacji ze stanem systemu / dezaktualizacja     |
| endpoint                               | punkt końcowy API / endpoint                                     |
| error-report intake                    | przyjęcie raportów błędów                                        |
| evidence                               | materiał dowodowy / dowód                                        |
| evidence register                      | rejestr materiału dowodowego                                     |
| exploitability narrative               | narracja wykorzystania podatności                                |
| fail-fast                              | natychmiastowe przerwanie przy błędzie                           |
| fallback                               | mechanizm awaryjny / obsługa zastępcza                           |
| finding                                | ustalenie                                                        |
| host key pinning                       | przypięcie klucza hosta                                          |
| key-person risk                        | ryzyko koncentracji kompetencji                                  |
| license compliance                     | zgodność licencyjna                                              |
| likelihood                             | prawdopodobieństwo                                               |
| lockfile                               | plik blokady zależności                                          |
| maintainability                        | utrzymywalność                                                   |
| manual deployment gate                 | ręczne zatwierdzenie wdrożenia                                   |
| maturity level                         | poziom dojrzałości                                               |
| mitigation                             | środek ograniczający ryzyko                                      |
| mismatch                               | rozbieżność / niezgodność                                        |
| non-conformity / gap                   | niezgodność / luka                                               |
| observability                          | obserwowalność                                                   |
| observation                            | obserwacja                                                       |
| operational readiness                  | gotowość operacyjna                                              |
| operational security                   | bezpieczeństwo operacyjne                                        |
| pipeline / CI pipeline                 | proces / proces CI / proces CI/CD                                |
| pre-production                         | etap przedprodukcyjny / środowisko przedprodukcyjne              |
| production / prod                      | środowisko produkcyjne                                           |
| production-ready                       | gotowość produkcyjna                                             |
| public error-report intake             | publiczny punkt przyjęcia raportów błędów                        |
| quality gate                           | kryterium jakości / warunek jakości                              |
| rate limiting                          | ograniczenie częstotliwości żądań                                |
| recommendation                         | zalecenie / zalecenie naprawcze                                  |
| refresh token                          | token odświeżania                                                |
| remediation                            | działanie naprawcze                                              |
| remediation plan                       | plan działań naprawczych                                         |
| reproducible build                     | powtarzalny proces budowania                                     |
| residual risk                          | ryzyko rezydualne                                                |
| reuse detection                        | wykrywanie ponownego użycia tokenu                               |
| risk register                          | rejestr ryzyk                                                    |
| root cause                             | przyczyna źródłowa                                               |
| runtime                                | środowisko uruchomieniowe                                        |
| runtime scope                          | zakres uruchomieniowy                                            |
| scalability                            | skalowalność                                                     |
| scorecard                              | karta oceny                                                      |
| security control                       | środek bezpieczeństwa / mechanizm kontrolny                      |
| sign-off                               | zatwierdzenie / akceptacja formalna                              |
| seed data                              | dane inicjalizacyjne                                             |
| seeding                                | inicjalizacja danych                                             |
| seeding mechanism                      | mechanizm inicjalizacji danych                                   |
| Software Bill of Materials             | zestawienie składników oprogramowania                            |
| source of truth                        | źródło prawdy                                                    |
| source-only                            | wyłącznie na podstawie kodu źródłowego                           |
| stakeholder                            | interesariusz                                                    |
| testability                            | testowalność                                                     |
| test inventory                         | rozbudowany zakres testów                                        |
| threat                                 | zagrożenie                                                       |
| threat model                           | model zagrożeń                                                   |
| TLS termination                        | terminacja TLS / zakończenie połączenia TLS                      |
| token reuse                            | ponowne użycie tokenu                                            |
| toolchain                              | łańcuch narzędzi                                                 |
| trade-off                              | kompromis                                                        |
| trust boundary                         | granica zaufania                                                 |
| unauthenticated                        | bez uwierzytelnienia                                             |
| version drift                          | rozbieżność wersji / niespójność wersjonowania                   |
| version pinning                        | zamrożenie wersji                                                |
| vulnerability                          | podatność                                                        |
| vulnerability assessment               | ocena podatności                                                 |
| vulnerability triage                   | weryfikacja i klasyfikacja podatności                            |
| weakness                               | błąd bezpieczeństwa / podatność bezpieczeństwa                   |
| weakness classification                | klasyfikacja błędów bezpieczeństwa                               |
| workflow                               | przepływ pracy / proces                                          |

## Parameter Prompts

The Parameter Configuration questions are asked in Polish when the user's request is in Polish.
Apply these phrasing rules:

- Report delivery uses `sposób dostarczania raportu` or `dostarczenie raportu`, never `dostawa`.
  Ask `Jak dostarczyć raport?`.
- Date-named subdirectory options use `katalogi dzienne` or `ścieżka daty`/`ścieżka dzienna`.
  `Datowy` and `datowa` are not proper Polish words and must not be used.
- Detail-level options are `Szczegółowy` (default), `Standardowy`, and `Skrócony`.
- `Inline` is offered as `W treści odpowiedzi` and `Custom report file` as `Własny plik raportu`.
- The trailing bypass options are `Użyj wartości domyślnej: <wartość>` and
  `Użyj wartości domyślnych dla wszystkich pozostałych pytań`.
- The Skill Update Check question is `Dostępna jest aktualizacja umiejętności (<n> nowych
  commitów). Zaktualizować teraz czy pominąć w tej sesji?` with options `Zaktualizuj teraz` and
  `Pomiń w tej sesji`.
- The audit-mode question is `Znaleziono poprzedni raport audytu: <ścieżka> (rewizja <n>, data
  <d>). Czy wykonać ponowny audyt względem tego raportu, czy nowy audyt?` with options
  `Ponowny audyt - porównaj z <plik>` and `Nowy audyt - zignoruj poprzedni raport`. The
  baseline-confirmation variant is `Potwierdź, że <ścieżka> to poprawna podstawa ponownego
  audytu.` with options `Potwierdź - ponowny audyt względem <plik>` and `Nowy audyt`. When a
  requested re-audit finds no previous report, ask `Nie znaleziono poprzedniego raportu audytu.
  Wykonać nowy audyt (rewizja 1.0)?` with the option `Wykonaj nowy audyt`. Mark the recommended
  option with `(zalecane)`.

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
  uppercase letter, capitalize the first letter of every value in that column.
- `* **Field:**` bullet-list values start with an uppercase letter, for example
  `Podstawa wymagania: Kontrola dostępu bez uwierzytelnienia`. Values that start with a code span
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
- `Inferred` renders `Wnioskowane`, not `Wywnioskowane`.
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
- Use `N/D` for `N/A` and `BŁĄD`/`Błąd` for `ERROR`/`Error` in Polish reports.
- The score-band legend is labeled `Skala oceny`, never `Legenda pasm` or `Skala ocen`.
- Broad test coverage is `rozbudowany zakres testów`, not `szeroki inwentarz testowy`.
- Effort estimates use plain units: `godziny`, not `godziny-dzień`.
- The verb `rozejść się` uses the past-tense forms `rozszedł się`, `rozeszła się`,
  `rozeszło się`, and `rozeszli`/`rozeszły się`, never `rozeszedł się`, for example `kontrakt
  rozszedł się z implementacją`.

## Diacritics Frequently Misspelled

The following Polish words are frequently written without diacritics by mistake. Always use the
correct form with diacritics:

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
| Skill Version        | Wersja umiejętności     |
| Time taken           | Czas wykonania          |
| Previous Report      | Poprzedni raport        |
| Projects             | Projekty                |

The `Stan` row is written only while the report is `Roboczy`; it is omitted when the report is
final. The `Stan prac` row is written only when the working tree is dirty; it is omitted when the
tree is clean.

The `Descriptive Mode` row is omitted. The setting is evident from the presence or absence of the
`Słownik` section, and a re-audit recovers it that way.

Value cells use the Fixed Vocabulary Values table for `State`, `Detail Level`, `Evaluation Scale`,
`Audit Purpose`, and `Verification Scope`, and `Polski` for `Language`.

## Audit Type Coverage & Assurance Matrix

| English                                     | Polish                                              |
|---------------------------------------------|-----------------------------------------------------|
| Audit Type Coverage & Assurance Matrix      | Macierz pokrycia typów audytu i poziomu zapewnienia |
| Report type                                 | Typ raportu                                         |
| Status                                      | Status                                              |
| Rationale                                   | Uzasadnienie                                        |
| Software Architecture Review                | Przegląd architektury oprogramowania                |
| Code Quality Audit                          | Audyt jakości kodu                                  |
| Security Vulnerability Assessment           | Ocena podatności bezpieczeństwa                     |
| Open Source License Compliance Review       | Przegląd zgodności licencji open source             |
| Penetration Test                            | Test penetracyjny                                   |
| Performance Audit                           | Audyt wydajności                                    |
| Cloud Infrastructure Audit                  | Audyt infrastruktury chmurowej                      |
| AI Governance Audit                         | Audyt zarządzania AI                                |
| Technical Due Diligence                     | Techniczne due diligence                            |
| SBOM / Software Composition Analysis        | SBOM / analiza składu oprogramowania                |
| Compliance Certification (SOC 2, ISO 27001) | Certyfikacja zgodności (SOC 2, ISO 27001)           |

The four coverage statuses render per Status And Severity Vocabulary: `OBJĘTE`,
`CZĘŚCIOWO`, `NIEWYKONANE`, `NIE DOTYCZY`.

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

Each term cell stays in its original form. A term cell is a markdown link only when the term
carries a longer `###` description below the index table, pointing to that description's anchor.
Acronym occurrences in the report body link to the description, or to the index table at
`#słownik` when there is none. Acronyms inside capitalized compound names are not linked, for
example `AI` in `AI Provenance` or `UI` in `Material UI`, and adjacent acronym pairs such as
`NIST RMF` count as one compound. Definitions and descriptions are written in Polish.

Identifier descriptions in `###` subsections prefer short, direct phrasing, for example
`Identyfikatory obowiązują tylko w tym raporcie i w kolejnych wersjach mogą być inne.` and
`Identyfikator zalecenia w planie działań naprawczych`.

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
| Top Risks                      | Najważniejsze ryzyka        |
| Readiness                      | Gotowość                    |

## Health Dashboard

| English           | Polish                     |
|-------------------|----------------------------|
| Health Dashboard  | Panel zdrowia              |
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
| Bus-factor rating                   | Ocena czynnika autobusowego              |
| High concentration risk             | Wysokie ryzyko koncentracji              |
| Moderate                            | Umiarkowane                              |
| Low                                 | Niskie                                   |
| Support / cost obligations          | Zobowiązania wsparcia i kosztów          |

Metric cells keep machine-readable `NOT SPECIFIED` rendering as `NIEOKREŚLONE`, matching the
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

## License & IP Compliance Review

| English                         | Polish                                  |
|---------------------------------|-----------------------------------------|
| License & IP Compliance Review  | Przegląd zgodności licencyjnej i IP     |
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

| English                       | Polish                              |
|-------------------------------|-------------------------------------|
| What Works                    | Co działa                           |
| What Needs Attention          | Co wymaga uwagi                     |
| Data Flow Diagram             | Diagram przepływu danych            |
| Design Patterns               | Wzorce projektowe                   |
| Architecture Decision Records | Rejestry decyzji architektonicznych |
| Industry Baseline Comparison  | Porównanie z praktyką branżową      |

## Skill Definition Conformance

| English                      | Polish                          |
|------------------------------|---------------------------------|
| Skill Definition Conformance | Zgodność definicji umiejętności |

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

| English                     | Polish                            |
|-----------------------------|-----------------------------------|
| Detailed Technical Findings | Szczegółowe ustalenia techniczne  |
| Summary table               | Tabela podsumowania               |
| Finding ID                  | Identyfikator                     |
| Pillar                      | Filar                             |
| Severity                    | Ważność                           |
| Title                       | Tytuł                             |
| Status                      | Status                            |
| Remediation Status          | Status naprawy                    |
| Target Files/Modules        | Pliki lub moduły                  |
| Type                        | Typ                               |
| Exploitability Narrative    | Narracja wykorzystania podatności |
| Description                 | Opis                              |
| Impact                      | Wpływ                             |
| Remediation Recommendation  | Zalecenie naprawcze               |
| Verification Method         | Metoda weryfikacji                |

### Pillar Names

| English                                   | Polish                                  |
|-------------------------------------------|-----------------------------------------|
| Architecture & Design                     | Architektura i projektowanie            |
| Code Quality                              | Jakość kodu                             |
| Security & Compliance                     | Bezpieczeństwo i zgodność               |
| Infrastructure & CI/CD                    | Infrastruktura i CI/CD                  |
| AI Provenance & Code Origin               | Pochodzenie AI i kod                    |
| Copyrights & Originality                  | Prawa autorskie i oryginalność          |
| API Compatibility & Versioning Discipline | Zgodność API i dyscyplina wersjonowania |

## Technical Debt Register

| English          | Polish              |
|------------------|---------------------|
| Debt ID          | Identyfikator długu |
| Debt Item        | Pozycja długu       |
| Category         | Kategoria           |
| Source Finding   | Źródło              |
| Remediation Cost | Koszt naprawy       |
| Cost of Delay    | Koszt zwłoki        |
| Status           | Status              |

## Unified Risk Register

| English               | Polish                          |
|-----------------------|---------------------------------|
| Unified Risk Register | Jednolity rejestr ryzyk         |
| Risk ID               | Identyfikator ryzyka            |
| Risk                  | Ryzyko                          |
| Source Finding        | Źródło                          |
| Impact                | Wpływ                           |
| Likelihood            | Prawdopodobieństwo              |
| Severity              | Ważność                         |
| Mitigation            | Środek ograniczający ryzyko     |
| Description           | Opis                            |
| Confidence            | Pewność oceny                   |
| Triggering Condition  | Warunek wyzwalający             |
| Existing Controls     | Istniejące mechanizmy kontrolne |
| Residual Risk         | Ryzyko rezydualne               |
| Treatment State       | Stan obsługi ryzyka             |
| Owner                 | Właściciel                      |
| Closure Trigger       | Wyzwalacz zamknięcia            |

## Trade-off Analysis

| English               | Polish                |
|-----------------------|-----------------------|
| Trade-off Analysis    | Analiza kompromisów   |
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
| Rec ID                         | Identyfikator zalecenia  |
| Priority                       | Priorytet                |
| Finding                        | Ustalenie                |
| Recommendation                 | Zalecenie                |
| Impact                         | Wpływ                    |
| Effort                         | Wysiłek                  |
| Complexity                     | Złożoność                |
| Verification                   | Weryfikacja              |

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
| Finding                      | Ustalenie                     |
| Previous                     | Poprzedni                     |
| Current                      | Bieżący                       |
| Note                         | Uwaga                         |
| Score delta                  | Zmiana wyników                |
| Dimension                    | Wymiar                        |
| Direction                    | Kierunek                      |
| Up                           | W górę                        |
| Down                         | W dół                         |
| Unchanged                    | Bez zmian                     |
| New                          | Nowe                          |
| Open                         | Otwarte                       |
| Closed                       | Zamknięte                     |

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

## Re-audit And Follow-up Plan

| English                 | Polish                     |
|-------------------------|----------------------------|
| Finding                 | Ustalenie                  |
| Priority                | Priorytet                  |
| Verification Owner      | Właściciel weryfikacji     |
| Closure Evidence        | Dowód zamknięcia           |
| Target Re-audit Trigger | Wyzwalacz ponownego audytu |

## Validation Record

| English                  | Polish                     |
|--------------------------|----------------------------|
| Validation Record        | Weryfikacja raportu        |
| Check                    | Kontrola                   |
| Result                   | Wynik                      |
| Evidence / Justification | Dowód / uzasadnienie       |
| Applied                  | Zastosowane                |
| Parity baseline          | Punkt odniesienia paritetu |

## Threat Model

| English            | Polish               |
|--------------------|----------------------|
| Boundary           | Granica zaufania     |
| Threat (STRIDE)    | Zagrożenie (STRIDE)  |
| Threat Description | Opis zagrożenia      |
| Mitigating Control | Środek ograniczający |

## API Contract Conformance

| English   | Polish |
|-----------|--------|
| Dimension | Wymiar |
| Status    | Status |
| Evidence  | Dowód  |

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

| English                          | Polish                                     |
|----------------------------------|--------------------------------------------|
| Evidence And Decision Limits     | Dowody i ograniczenia decyzji              |
| Verification And Evidence Ledger | Rejestr weryfikacji i materiału dowodowego |
| Evidence ID                      | Identyfikator dowodu                       |
| Check / Source                   | Kontrola / źródło                          |
| Execution                        | Wykonanie                                  |
| Result                           | Wynik                                      |
| Artifact                         | Artefakt                                   |
| Requirement Basis                | Podstawa wymagania                         |
| Confidence                       | Pewność oceny                              |
| Verification State               | Stan weryfikacji                           |
| Counter-check                    | Kontrola kontrargumentów                   |
| Security Classification          | Klasyfikacja bezpieczeństwa                |
| Inspected                        | Sprawdzone w źródłach                      |
| Reported                         | Zadeklarowane                              |
| Inferred                         | Wnioskowane                                |
| Readiness Cost                   | Koszt osiągnięcia gotowości                |
| Operational Objectives           | Cele operacyjne                            |
| Due Diligence Coverage           | Zakres weryfikacji                         |
| Work Item                        | Pakiet prac                                |
| Source Recommendations           | Zalecenia źródłowe                         |
| Effort Range                     | Zakres nakładu pracy                       |
| Basis                            | Podstawa                                   |
| Dependencies                     | Zależności                                 |
| Metric                           | Metryka                                    |
| Target                           | Cel                                        |
| Measured Result                  | Wynik pomiaru                              |
| Window                           | Okres pomiaru                              |
| Source                           | Źródło                                     |
| Owner                            | Właściciel                                 |
| Concern                          | Obszar ryzyka                              |
| Missing Artifact / Next Step     | Brakujący artefakt / kolejny krok          |
| Meaning                          | Znaczenie                                  |
| Readiness Treatment              | Obsługa gotowości produkcyjnej             |
| Quality Characteristic           | Charakterystyka jakości                    |
| Lens Evidence                    | Dowody w Lens                              |
| Functional Suitability           | Przydatność funkcjonalna                   |
| Performance Efficiency           | Efektywność wydajnościowa                  |
| Compatibility                    | Kompatybilność                             |
| Interaction Capability           | Zdolność interakcji                        |
| Reliability                      | Niezawodność                               |
| Flexibility                      | Elastyczność                               |
| Safety                           | Bezpieczeństwo przed szkodami              |
| Support Continuity               | Ciągłość wsparcia                          |
| Ownership Cost                   | Koszt utrzymania                           |
| Roadmap Feasibility              | Wykonalność planu rozwoju                  |
| Supplier Continuity              | Ciągłość dostawcy                          |
| IP Rights                        | Prawa własności intelektualnej             |
| Data Obligations                 | Obowiązki dotyczące danych                 |

Execution states produced by the audit render in Polish: `NIEURUCHOMIONE`, `NIEOCENIONE`,
`NIEZBADANE`, `POZA ZAKRESEM`, `NIEWYSTARCZAJĄCE INFORMACJE`, and `N/D`. Record identifiers,
CWE IDs, CVSS vectors, tool commands, and code stay unchanged.

## Skill Definition Conformance Table

| English   | Polish |
|-----------|--------|
| Dimension | Wymiar |
| Status    | Status |
| Evidence  | Dowód  |
