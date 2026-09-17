# Polish Translation

## Purpose

> **Scope:** Polish translations for the audit report, including status and severity vocabulary, section headings, table headers, style rules, and diacritics
> **Key items:** translation tables, status and severity mapping, style rules, encoding, diacritics preservation

This file defines the Polish translations for the audit report. When the report language is Polish, apply every translation in this file to the corresponding English terms in the report.

The default report language is English. This file is loaded only when the user requests a Polish-language report.

## Contents

| Section                                     | Line | What it covers                              |
|---------------------------------------------|------|---------------------------------------------|
| Status And Severity Vocabulary              | 49   | Status And Severity Vocabulary guidance     |
| Style Rules                                 | 73   | Style Rules guidance                        |
| Diacritics Frequently Misspelled            | 81   | Diacritics Frequently Misspelled guidance   |
| Output Filename                             | 113  | Output Filename guidance                    |
| Document Information                        | 120  | Document Information guidance               |
| Project Inventory                           | 132  | Project Inventory guidance                  |
| Technology Stack                            | 141  | Technology Stack guidance                   |
| Executive Summary                           | 158  | Executive Summary guidance                  |
| Health Dashboard                            | 173  | Health Dashboard guidance                   |
| Scorecard                                   | 184  | Scorecard guidance                          |
| Scoring Rubrics                             | 208  | Scoring Rubrics guidance                    |
| High-Level Observations                     | 222  | High-Level Observations guidance            |
| Auditing Methodology                        | 229  | Auditing Methodology guidance               |
| System Context                              | 243  | System Context guidance                     |
| Architectural Assessment                    | 256  | Architectural Assessment guidance           |
| Skill Definition Conformance                | 262  | Skill Definition Conformance guidance       |
| Standards Conformance                       | 268  | Standards Conformance guidance              |
| References                                  | 288  | References guidance                         |
| Strengths And What's Working                | 297  | Strengths And What's Working guidance       |
| Detailed Technical Findings                 | 303  | Detailed Technical Findings guidance        |
| Technical Debt Register                     | 333  | Technical Debt Register guidance            |
| Unified Risk Register                       | 345  | Unified Risk Register guidance              |
| Trade-off Analysis                          | 358  | Trade-off Analysis guidance                 |
| Actionable Remediation Roadmap              | 370  | Actionable Remediation Roadmap guidance     |
| Changes Since Previous Audit                | 384  | Changes Since Previous Audit guidance       |
| Scope Exclusions                            | 412  | Scope Exclusions guidance                   |
| Re-audit And Follow-up Plan                 | 420  | Re-audit And Follow-up Plan guidance        |
| Threat Model                                | 430  | Threat Model guidance                       |
| API Contract Conformance                    | 439  | API Contract Conformance guidance           |
| API Compatibility And Versioning Discipline | 447  | API Compatibility And Versioning guidance   |
| Evidence And Decision Terms                 | 456  | Evidence And Decision Terms guidance        |
| Skill Definition Conformance Table          | 518  | Skill Definition Conformance Table guidance |

## Status And Severity Vocabulary

Use these Polish equivalents instead of the English markers:

| English     | Polish         |
|-------------|----------------|
| `PASS`      | `OK`           |
| `PARTIAL`   | `CZĘŚCIOWO`    |
| `FAIL`      | `NIEZALICZONE` |
| `UNKNOWN`   | `NIEZNANE`     |
| `N/A`       | `ND`           |
| `LOW`       | `NISKIE`       |
| `MEDIUM`    | `ŚREDNIE`      |
| `HIGH`      | `WYSOKIE`      |
| `CRITICAL`  | `KRYTYCZNE`    |
| `SEVERITY:` | `WAŻNOŚĆ:`     |
| `Score:`    | `Wynik:`       |

The inline format remains identical: the marker follows the bold heading separated by a space. For example, `**Strategia wdrożenia** CZĘŚCIOWO` or `**Testowalność** Wynik: 8/10`.

When the `1-5` or `1-3` numeric scale is selected, use `Wynik: X/5` or `Wynik: X/3`.

When `5 stars` or `3 stars` is selected, use `Wynik:` followed by the unchanged star bar.

## Style Rules

- Do not use "Title Case" in section and chapter names, use sentence case.
- Use "Przykład zawartości" instead of "Content Example".
- Use neuter gender for acronyms treated as nouns: "czyste PWA" (not "czysta PWA"), "czyste SPA" (not "czysta SPA").
- Preserve all Polish diacritics (for example, "ą", "ę", "ć", "ł", "ń", "ó", "ś", "ź", "ż", "Ą", "Ę", "Ć", "Ł", "Ń", "Ó", "Ś", "Ź", "Ż") in every section, heading, table cell, and paragraph. Do not transliterate or strip diacritics.
- Write the report in UTF-8 encoding. Do not use ASCII-only fallback for Polish text.

## Diacritics Frequently Misspelled

The following Polish words are frequently written without diacritics by mistake. Always use the correct form with diacritics:

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

## Output Filename

The default output filename for a Polish-language report is `AUDYT.md` instead of `AUDIT.md`.

When a previous report exists, the default filename carries the new version, for example
`AUDYT-1.1.md`, and the previous file is never overwritten.

## Document Information

| English              | Polish                  |
|----------------------|-------------------------|
| Document Information | Informacje o dokumencie |
| Version              | Wersja                  |
| Date                 | Data                    |
| State                | Stan                    |
| Detail Level         | Poziom szczegółowości   |
| Previous Report      | Poprzedni raport        |
| Projects             | Projekty                |

## Project Inventory

| English     | Polish  |
|-------------|---------|
| Project     | Projekt |
| Path        | Ścieżka |
| Version     | Wersja  |
| Description | Opis    |

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

## Health Dashboard

| English           | Polish                   |
|-------------------|--------------------------|
| Health Dashboard  | Panel zdrowia            |
| Risk Heat Map     | Mapa ciepła ryzyk        |
| Impact            | Wpływ                    |
| Likelihood        | Prawdopodobieństwo       |
| Scorecard Summary | Scorecard - podsumowanie |
| Team & Continuity | Zespół i ciągłość        |

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
| Deployability           | Wdrażalność                    |
| Scalability             | Skalowalność                   |
| Security                | Bezpieczeństwo                 |
| Compliance              | Zgodność                       |
| Observability           | Obserwowalność                 |
| Operational Safety      | Bezpieczeństwo operacyjne      |
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

| English     | Polish         |
|-------------|----------------|
| Score Range | Zakres wyników |
| Definition  | Definicja      |

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

## Architectural Assessment

| English                  | Polish             |
|--------------------------|--------------------|
| Architectural Assessment | Ocena architektury |

## Skill Definition Conformance

| English                      | Polish                          |
|------------------------------|---------------------------------|
| Skill Definition Conformance | Zgodność definicji umiejętności |

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
| References          | Referencje        |
| Reference           | Referencja        |
| Publisher or Author | Wydawca lub autor |
| Used In             | Zastosowane w     |

## Strengths And What's Working

| English                    | Polish                   |
|----------------------------|--------------------------|
| Strengths & What's Working | Mocne strony i co działa |

## Detailed Technical Findings

| English                     | Polish                        |
|-----------------------------|-------------------------------|
| Detailed Technical Findings | Szczegółowe wyniki techniczne |
| Summary table               | Tabela podsumowania           |
| Finding ID                  | Identyfikator                 |
| Pillar                      | Filtr                         |
| Severity                    | Ważność                       |
| Title                       | Tytuł                         |
| Status                      | Status                        |
| Remediation Status          | Status naprawy                |
| Target Files/Modules        | Pliki/Moduły docelowe         |
| Description                 | Opis                          |
| Impact                      | Wpływ                         |
| Remediation Recommendation  | Rekomendacja naprawcza        |
| Verification Method         | Metoda weryfikacji            |

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

| English               | Polish                  |
|-----------------------|-------------------------|
| Unified Risk Register | Jednolity rejestr ryzyk |
| Risk ID               | Identyfikator ryzyka    |
| Risk                  | Ryzyko                  |
| Source Finding        | Źródło                  |
| Impact                | Wpływ                   |
| Likelihood            | Prawdopodobieństwo      |
| Severity              | Ważność                 |
| Mitigation            | Ograniczenie            |

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

| English                        | Polish                          |
|--------------------------------|---------------------------------|
| Actionable Remediation Roadmap | Plan działania i mapa naprawcza |
| Rec ID                         | Identyfikator rekomendacji      |
| Priority                       | Priorytet                       |
| Finding                        | Znalezisko                      |
| Recommendation                 | Rekomendacja                    |
| Impact                         | Wpływ                           |
| Effort                         | Wysiłek                         |
| Complexity                     | Złożoność                       |
| Verification                   | Weryfikacja                     |

## Changes Since Previous Audit

| English                      | Polish                        |
|------------------------------|-------------------------------|
| Changes Since Previous Audit | Zmiany od poprzedniego audytu |
| Field                        | Obszar                        |
| Previous Report              | Poprzedni raport              |
| Current Report               | Bieżący raport                |
| File                         | Plik                          |
| Version                      | Wersja                        |
| Date                         | Data                          |
| Detail level                 | Poziom szczegółowości         |
| Evaluation scale             | Skala oceny                   |
| Finding transitions          | Zmiany stanu znalezisk        |
| Finding                      | Znalezisko                    |
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

| English          | Polish               |
|------------------|----------------------|
| Scope Exclusions | Wyłączenia z zakresu |
| Scope            | Zakres               |
| Justification    | Uzasadnienie         |

## Re-audit And Follow-up Plan

| English                 | Polish                     |
|-------------------------|----------------------------|
| Finding                 | Znalezisko                 |
| Priority                | Priorytet                  |
| Verification Owner      | Właściciel weryfikacji     |
| Closure Evidence        | Dowód zamknięcia           |
| Target Re-audit Trigger | Wyzwalacz ponownego audytu |

## Threat Model

| English            | Polish                 |
|--------------------|------------------------|
| Boundary           | Granica                |
| Threat (STRIDE)    | Zagrożenie (STRIDE)    |
| Threat Description | Opis zagrożenia        |
| Mitigating Control | Kontrola ograniczająca |

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

| English                          | Polish                            |
|----------------------------------|-----------------------------------|
| Evidence And Decision Limits     | Dowody i ograniczenia decyzji     |
| Verification And Evidence Ledger | Rejestr weryfikacji i dowodów     |
| Evidence ID                      | Identyfikator dowodu              |
| Check / Source                   | Kontrola / źródło                 |
| Execution                        | Wykonanie                         |
| Result                           | Wynik                             |
| Artifact                         | Artefakt                          |
| Requirement Basis                | Podstawa wymagania                |
| Confidence                       | Pewność oceny                     |
| Verification State               | Stan weryfikacji                  |
| Counter-check                    | Kontrola kontrargumentów          |
| Security Classification          | Klasyfikacja bezpieczeństwa       |
| Inspected                        | Sprawdzone w źródłach             |
| Reported                         | Zadeklarowane                     |
| Inferred                         | Wywnioskowane                     |
| Readiness Cost                   | Koszt osiągnięcia gotowości       |
| Operational Objectives           | Cele operacyjne                   |
| Due Diligence Coverage           | Zakres due diligence              |
| Work Item                        | Pakiet prac                       |
| Source Recommendations           | Rekomendacje źródłowe             |
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

Execution states produced by the audit are `NOT RUN` and `N/A` to preserve the ledger's
machine-readable vocabulary, explain their meanings in Polish prose.

Keep `UNKNOWN`, `NOT SPECIFIED`, and `INSUFFICIENT INFORMATION` when used as missing-information
tokens, while category statuses use the existing Polish translations.

## Skill Definition Conformance Table

| English   | Polish |
|-----------|--------|
| Dimension | Wymiar |
| Status    | Status |
| Evidence  | Dowód  |
