# Report Format

## Purpose

> **Scope:** The required structure and template for the final audit report
> **Key items:** document information, technology stack, executive summary, health dashboard, auditing methodology, scoring rubrics, system context, architectural assessment, detailed technical findings, unified risk register, trade-off analysis, remediation roadmap, scope exclusions

This file defines the exact shape of the audit report. Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development, or an already-running production system. Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`. A present-but-empty section signals a gap; a missing section hides it.

## Formatting Rules

Use a hybrid table-paragraph format in every section.

Tables provide the scannable summary. Paragraphs below the table provide the detailed evidence, risks, and reasoning.

In tables, use shortened, general values. One or two words per cell. Do not crowd table cells with long explanations. Save detail for the paragraphs.

Align table columns by padding every cell value with trailing spaces so that all `|` column separators align vertically in plain text. Use consistent spacing within each table.

Do not number section headings. Use the section name as the heading, for example "Executive Summary", not "2. Executive Summary". When the user requests a specific language, translate the section heading into that language.

Keep column headers identical to the templates below across every audit. When the user requests a specific language, translate the column headers into that language while keeping the structure identical.

Within a table cell, separate multiple points with a semicolon or a line break, not with sub-bullets.

Place descriptive paragraphs immediately after each table. In the paragraphs, explain every aspect with concrete evidence, file paths, and reasoning. Use short sentences separated by blank lines; each sentence stands on its own line with an empty line between consecutive sentences.

Start each detailed paragraph with a bold heading on its own line. Put the status, score, or severity inline after the heading, separated by a space. Then add an empty line, then the paragraph body. Do not run the heading and the body together on the same line.

Use this bold-heading pattern for paragraphs that expand on a table row. For actual section or subsection titles, use markdown header syntax (`##` or `###`) rather than bold text.

Example for finding summary:

```markdown
**FND-SEC-001: Hardcoded JWT signing key** `CRITICAL`

`src/Portal.Api/appsettings.json` contains a plaintext JWT symmetric key.
```

Example for scorecard dimension:

```markdown
**Security** Score: `2/10`

The repository contains multiple plaintext secrets in tracked files.
```

**Hyphen rule**

Use the standard ASCII hyphen-minus `-` (U+002D) for all hyphens, dashes, and minus signs. Do not use the em dash `—` (U+2014) or en dash `–` (U+2013) anywhere in the report.

**No closing line**

Do not add a closing line such as "End of audit report." or "---" at the end of the document. The Scope Exclusions section is the final section; end the report after it without any trailing boilerplate.

## Report Delivery And Parameter Configuration

Report delivery is determined during the Parameter Configuration phase in `process/workflow.md`. Do not ask delivery questions here; they are handled upstream.

When the user names an output file in the original request, for example "write the audit to AUDIT.md", honor that filename without asking again.

When the user invokes an audit without naming an output file, for example "perform lens on this service" or "make audit report on the codebase", the Parameter Configuration phase determines delivery and filename.

Default delivery is **Inline** (direct response). Default filename is **AUDYT.md** for Polish reports or **AUDIT.md** for all other languages when File mode is selected.

For a single-dimension request that produces only a short subsection, returning the result inline is acceptable without asking, unless the user asked for a file.

## Detail Level Configuration

The report adapts to the detail level chosen during Parameter Configuration.

**Standard**

All fifteen sections are present in full:

- Document Information
- Technology Stack
- Executive Summary
- Health Dashboard
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- System Context
- Architectural Assessment
- Strengths & What's Working
- Detailed Technical Findings (all findings with full Description, Impact, Remediation, and Verification)
- Unified Risk Register
- Trade-off Analysis
- Actionable Remediation Roadmap (full matrix with P1-P4, impact/effort/complexity, verification)
- Scope Exclusions

**Detailed**

Same fifteen sections as Standard, plus the following extensions:

- Executive Summary includes a longer Production Readiness Threshold paragraph.
- Health Dashboard includes an expanded Risk Heat Map with all risks plotted.
- Architectural Assessment includes deeper critique with additional industry baseline comparisons.
- Strengths section includes 8-10 bullet points.
- Each finding includes extended verification methods and alternative remediation paths.
- Trade-off Analysis includes additional trade-offs surfaced during assessment.
- Remediation Roadmap includes additional context for each recommendation (blocking dependencies, estimated timeframes).

**Brief**

Condensed output for rapid review:

- Document Information (full)
- Technology Stack (full)
- Executive Summary (summary table only)
- Health Dashboard (scorecard summary and risk heat map only)
- High-Level Observations (full)
- Strengths & What's Working (top 3 bullets only)
- Top 5 findings only (summary table and abbreviated detail blocks)
- Top 5 risks only (summary table)
- Key trade-offs only (top 2, no full table)
- Key recommendations only (top 5, no full matrix)
- Scope Exclusions (full)

Omitted in Brief: Auditing Methodology, Scoring Rubrics, System Context, Architectural Assessment detailed critique, full Detailed Technical Findings list, full Unified Risk Register, full Trade-off Analysis, full Actionable Remediation Roadmap.

## Section Order

The report has these top-level sections, in this order, with unnumbered headings:

- Document Information
- Technology Stack
- Executive Summary
- Health Dashboard
- High-Level Observations
- Auditing Methodology
- Scoring Rubrics
- System Context
- Architectural Assessment
- Strengths & What's Working
- Detailed Technical Findings
- Unified Risk Register
- Trade-off Analysis
- Actionable Remediation Roadmap
- Scope Exclusions

## Document Information

Open the report with a document title as a level-1 markdown heading (`#`), followed by a short metadata block. Each metadata field must appear on its own line with a blank line separating it from the next field. Do not run fields together on the same line.

Format:

```markdown
# <System Name> Software Audit Report

**Version**: <version number>

**Date**: <audit date>

**State**: <Draft / Final>

**Detail Level**: <Standard / Detailed / Brief>
```

Use double asterisks for the label and a single space after the colon. Each label-value pair is followed by an empty line. This ensures proper rendering in all markdown viewers.

When the report language is Polish, translate the labels into Polish: `Wersja`, `Data`, `Stan`, `Poziom szczegółowości`.

## Technology Stack

Open the report with a factual inventory of the technologies the subject uses. Describe the stack only; do not judge it here.

Use a key-value table:

| Layer            | Technology                                                      |
|------------------|-----------------------------------------------------------------|
| Languages        | <languages and versions>                                        |
| Frameworks       | <application and UI frameworks>                                 |
| Runtime/Platform | <runtime, OS, or host platform>                                 |
| Build tooling    | <build system, bundler, compilers>                              |
| Test tooling     | <test frameworks and runners>                                   |
| Package manager  | <dependency and package manager>                                |
| Key libraries    | <notable third-party libraries>                                 |
| Data stores      | <databases, caches, file formats>, or `NOT SPECIFIED`           |
| Target platforms | <where the software runs or ships>                              |

Anchor each entry to evidence, such as a manifest, lockfile, or config file. Mark any layer the input does not reveal as `NOT SPECIFIED`. Add or omit rows to fit the subject, but keep the layer names in this column and translate them into the report language.

## Executive Summary

Provide a compact overview a reader can absorb without the detail sections.

Use a key-value table:

| Field          | Value                                                                          |
|----------------|--------------------------------------------------------------------------------|
| System type    | <prototype / codebase / production system / proposal>                          |
| Scope          | <what was reviewed and what was excluded>                                      |
| Source basis   | <running system / inspected code / description>                                |
| Maturity level | <`Prototype` / `Early development` / `Pre-production` / `Production-ready` / `Undetermined`> |

When the report language is Polish, translate the table headers and field names into Polish: `Obszar`, `Wartość`, `Typ systemu`, `Zakres`, `Źródło danych`, `Poziom dojrzałości`.

**Summary description**

When the report language is Polish, use `Opis podsumowujący` instead of `Summary description`.

Write one paragraph immediately after the table. State the system's purpose in one sentence. Summarize the overall condition in one sentence. Note the maturity level and anchor it to evidence from later sections. Mention any critical finding that the reader should know first. Keep the paragraph to four sentences maximum.

The maturity level must be justified by evidence in later sections, not asserted.

**Production Readiness Threshold**

When the report language is Polish, use `Próg gotowości produkcyjnej` instead of `Production Readiness Threshold`.

Add a short paragraph at the end of the Executive Summary stating the minimum conditions required for the maturity label to change from its current level to `Production-ready`. Tie these conditions explicitly to specific risk IDs (for example: "To reach Production-ready, RSK-001 and RSK-002 must be closed by removing hardcoded secrets, and RSK-003 must be closed by achieving 60% test coverage"). This paragraph gives the reader a concrete bar for re-audit.

## Health Dashboard

Present the quantitative health summary in a consolidated view. This section contains the Risk Heat Map and the Scorecard Summary.

**Risk Heat Map**

Provide a consolidated Likelihood vs Impact matrix summarizing the top risks. Use a table:

| Impact | LOW | MEDIUM | HIGH |
|--------|-----|--------|------|
| CRITICAL |     |        |      |
| HIGH |     |        |      |
| MEDIUM |     |        |      |
| LOW |     |        |      |

When the report language is Polish, translate the axis labels into Polish: `Wpływ`, `Prawdopodobieństwo`.

Populate cells with `RSK-XXX` identifiers from the Unified Risk Register. Leave empty cells blank. Do not include plaintext secrets, passwords, or cryptographic keys in this summary. Use generic descriptions or masked placeholders.

**Scorecard Summary**

When the report language is Polish, use `Scorecard - podsumowanie` instead of `Scorecard Summary`.

Provide a compact summary of the project scorecard dimensions:

| Dimension | Score | Notes |
|-----------|-------|-------|
| Testability |       |       |
| Design Soundness |       |       |
| Code Quality |       |       |
| Stack Alignment |       |       |
| Dependency Health |       |       |
| Maintainability |       |       |
| Deployability |       |       |
| Scalability |       |       |
| Security |       |       |
| Compliance |       |       |
| Observability |       |       |
| Operational Safety |       |       |
| AI Provenance |       |       |
| Originality & Licensing |       |       |

When the report language is Polish, translate the column headers and dimension names into Polish using the equivalents defined in `principles/output-style.md`.

## High-Level Observations

Surface the most important findings in a compact table a reader can scan before reading the detail sections. Include at most five observations. Each observation should be a single concrete finding, not a category summary.

Use this single-column table:

| Observation                     |
|---------------------------------|
| <observation>                   |

When the report language is Polish, translate the table header into Polish: `Obserwacja`.

Write one paragraph per observation immediately after the table, in the same order as the table rows. Start each paragraph with a bold heading on its own line (the observation text, abbreviated if needed), then add an empty line, then the body. Each paragraph explains why the observation matters and what risk or opportunity it represents. Anchor every claim to a specific finding in the Detailed Technical Findings.

Keep each observation brief. The full technical detail lives in the numbered finding blocks later in the report. This section exists to give non-technical readers a fast-skim path.

## Auditing Methodology

This section defines how the audit was conducted and the framework used to evaluate findings. Present it before any scored findings.

**Methodology overview**

When the report language is Polish, use `Przegląd metodologiczny` instead of `Methodology overview`.

State that the audit uses evidence-based reasoning across 18 assessment categories grouped into six pillars. List the pillars:

- **Architecture & Design** - Design principles, maintainability, change management, documentation, non-functional requirements
- **Code Quality** - Testing, code quality, stack best practices
- **Security & Compliance** - Security, compliance and data protection
- **Infrastructure & CI/CD** - Dependencies, deployment, rollback, observability, error handling, operational readiness
- **AI Provenance & Code Origin** - AI-generated code detection, Vibe Coding risks, Agent Driven Engineering maturity, SDLC discipline
- **Copyrights & Originality** - Code originality, license compliance, attribution, dependency license compatibility

When the report language is Polish, translate the pillar names into Polish using the equivalents defined in `principles/output-style.md`.

**Audit evidence statement**

When the report language is Polish, use `Oświadczenie o dowodach` instead of `Audit evidence statement`.

Begin the Methodology section with 2-3 sentences stating exactly what was inspected. Include:

- The number of source files, test files, and configuration files reviewed. State whether `.gitignore` exclusions were applied. If `.gitignore` was not present, note this as a gap.
- Whether Git history was examined.
- Whether a running environment was observed.

Example: "This audit inspected 147 source files, 8 test files, and 4 configuration files from the repository root, excluding files listed in `.gitignore`. Git commit history was reviewed for the last 15 commits. No running application or live environment was observed; all findings are based on static code analysis."

**Severity definitions**

When the report language is Polish, use `Definicje ważności` instead of `Severity definitions`.

Add a 4-row rubric defining each qualitative severity band. These definitions anchor the severity values used in findings and risks.

| Severity | Impact | Likelihood | Blocks Production Readiness |
|----------|--------|------------|----------------------------|
| CRITICAL | Data loss, breach, or full system compromise | Expected without intervention | Yes |
| HIGH | Major function loss or data integrity concern | Plausible under normal operation | Yes |
| MEDIUM | Degraded function or contained outage | Requires specific conditions | No (but must be tracked) |
| LOW | Limited or cosmetic effect | Unusual combination required | No |

When the report language is Polish, translate the column headers and severity descriptions into Polish. Use `Ważność` for `Severity`, `Wpływ` for `Impact`, `Prawdopodobieństwo` for `Likelihood`, and `Blokuje gotowość produkcyjną` for `Blocks Production Readiness`.

Use these definitions consistently across the Detailed Technical Findings and the Unified Risk Register.

## Scoring Rubrics

This section defines the scoring framework so that scores are objective and reproducible. Present it after the Auditing Methodology and before any scored findings.

**Scoring rubric**

Present the rubric matrix that defines what constitutes each score band. Use the default 1-10 scale unless the user requested the 1-5 alternative.

For the 1-10 scale:

| Band | Score Range | Definition |
|------|-------------|------------|
| Excellent | 9-10 | Capability is comprehensive and verified by strong evidence |
| Good | 7-8 | Capability is solid overall; minor or noticeable gaps exist |
| Average | 4-6 | Capability is present but uneven, limited, or inconsistent |
| Poor | 1-3 | Capability is minimal, fragmentary, or absent where required |

When the report language is Polish, translate the band names and definitions into Polish:
- `Doskonała` for `Excellent`
- `Dobra` for `Good`
- `Średnia` for `Average`
- `Słaba` for `Poor`
- Translate `Definition` into `Definicja` and `Score Range` into `Zakres wyników`.

For the 1-5 alternative scale:

| Band | Score Range | Definition |
|------|-------------|------------|
| Excellent | 5 | Capability is comprehensive and verified by strong evidence |
| Good | 4 | Capability is solid with minor gaps |
| Average | 3 | Capability is adequate but uneven |
| Poor | 1-2 | Capability is minimal, limited, or absent where required |

When the report language is Polish, apply the same band translations as above.

**Zero is not a score.** The value `0` is reserved and never used. When a dimension cannot apply, mark it `N/A`.

## System Context

Describe the system as understood from the input. Present the factual context without critique.

| Aspect | Detail |
|--------|--------|
| Functional description | <what the system does> |
| Architecture overview | <high-level structure> |
| Key components | <named components or modules> |
| External dependencies | <services, libraries, platforms> |
| Assumptions | <only if explicitly stated, else `NOT SPECIFIED`> |

When the report language is Polish, translate the table headers and aspect names into Polish: `Aspekt`, `Szczegóły`, `Opis funkcjonalny`, `Przegląd architektury`, `Kluczowe komponenty`, `Zależności zewnętrzne`, `Założenia`.

Mark any unknown aspect as `NOT SPECIFIED`.

After the table, add subsections for major components (e.g., `### Backend`, `### Frontend`, `### Deployment`). Put exactly one empty line after each subsection header before the first sentence. Separate every sentence with an empty line.

## Architectural Assessment

Provide an architectural critique against industry baselines. Evaluate coupling, cohesion, state management, separation of concerns, and pattern consistency against the stated constraints. Anchor every claim to a concrete file path or design decision. Do not judge the stack choice itself.

Structure this section with three subsections: `### What Works`, `### What Needs Attention`, and `### Industry Baseline Comparison`. Use Title Case for all subsection titles. Put exactly one empty line after each subsection header before the first sentence.

When listing multiple related items (e.g., typical production practices), use a bullet list rather than an inline comma-separated paragraph. Put an empty line between the intro sentence and the first bullet.

## Strengths & What's Working

Add a short section with 5-8 bullet points acknowledging what the system does well. This balances the tone of the report and anchors the scorecard with positive baselines.

Use a bullet list. When a strength requires more than one sentence, start the bullet with a bold heading on its own line, then add an empty line, then the body. Anchor every claim to a concrete file, pattern, or decision. Examples:

```markdown
- **TypeScript strict mode is enabled in both backend and frontend**.

`backend/tsconfig.json` and `frontend/tsconfig.app.json` both set `"strict": true`.

This catches a broad class of type errors at compile time.
```

For single-sentence strengths, keep them as plain bullets:

- Dependency injection is consistently applied in `Program.cs`, enabling testable service registration.
- Nullable reference types are enabled project-wide, reducing null-reference defects.
- Firebird SQL connection pooling is configured with sensible `MinPoolSize` and `MaxPoolSize` values.
- JWT bearer authentication is implemented with standard ASP.NET Core middleware.

Do not invent strengths. Only list what is evidenced in the provided files.

## Detailed Technical Findings

Present all findings grouped under six pillars. Each finding receives a unique deterministic index.

**Summary table:**

When the report language is Polish, use `Tabela podsumowania` instead of `Summary table`.

Present a compact summary of all findings:

| Finding ID | Pillar | Severity | Title | Status | Remediation Status |
|------------|--------|----------|-------|--------|-------------------|
| FND-ARC-001 | Architecture & Design | <severity> | <title> | <status> | Open |
| FND-CQ-001 | Code Quality | <severity> | <title> | <status> | Open |
| FND-SEC-001 | Security & Compliance | <severity> | <title> | <status> | Open |
| FND-INF-001 | Infrastructure & CI/CD | <severity> | <title> | <status> | Open |
| FND-AIP-001 | AI Provenance & Code Origin | <severity> | <title> | <status> | Open |
| FND-CPR-001 | Copyrights & Originality | <severity> | <title> | <status> | Open |

When the report language is Polish, translate the column headers into Polish: `Identyfikator`, `Filtr`, `Ważność`, `Tytuł`, `Status`, `Status naprawy`.

Pillar abbreviations for IDs:

- `ARC` - Architecture & Design
- `CQ` - Code Quality
- `SEC` - Security & Compliance
- `INF` - Infrastructure & CI/CD
- `AIP` - AI Provenance & Code Origin
- `CPR` - Copyrights & Originality

When the report language is Polish, translate the pillar names into Polish using the equivalents defined in `principles/output-style.md`.

Severity values: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
Status values: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`.

**Detailed findings**

After the summary table, write one block per finding in the same order. Use this exact markdown block pattern:

```markdown
### FND-[PILLAR]-[NUMBER]: [Clear, Concise Title of Finding]

* **Pillar:** [Architecture & Design | Code Quality | Security & Compliance | Infrastructure & CI/CD | AI Provenance & Code Origin | Copyrights & Originality]
* **Severity:** [Critical | High | Medium | Low]
* **Target Files/Modules:** [Exact paths or components evaluated]
* **Description:** [Detailed technical explanation of the discovered state, architectural anti-pattern, or code flaw]
* **Impact:** [Concrete operational, business, or security consequence if left unremediated]
* **Remediation Recommendation:** [Step-by-step technical guidance to resolve the finding]
* **Verification Method:** [Specific test, command, or process to confirm the fix is successful]
```

When the report language is Polish, translate the bullet labels into Polish: `Filtr`, `Ważność`, `Pliki/Moduły docelowe`, `Opis`, `Wpływ`, `Rekomendacja naprawcza`, `Metoda weryfikacji`.

Each finding must cite concrete evidence: file paths, config keys, commands, or direct quotes. Do not crowd the bullet list with long prose. Use short sentences separated by blank lines; each sentence stands on its own line with an empty line between consecutive sentences.

When referencing secrets, credentials, or keys in the Description or Impact fields, replace exact values with `[REDACTED]` or generic descriptions such as "plaintext database credentials found in tracking file".

Trade-off analyses that were previously in a standalone section should be embedded directly into the relevant finding they impact, under the Description or Impact bullet.

## Unified Risk Register

This section builds a cross-referenced risk table from the risks surfaced during assessment. Every risk must trace back to a specific finding.

**Table format:**

| Risk ID | Risk | Source Finding | Impact | Likelihood | Severity | Mitigation |
|---------|------|----------------|--------|------------|----------|------------|
| RSK-001 | <concrete risk> | FND-XXX | <consequence> | <probability> | <severity> | <action> |

When the report language is Polish, translate the column headers into Polish: `Identyfikator ryzyka`, `Ryzyko`, `Źródło`, `Wpływ`, `Prawdopodobieństwo`, `Ważność`, `Ograniczenie`.

Column meanings:

- **Risk ID**: `RSK-[001]` ascending.
- **Risk**: a concrete technical risk, stated neutrally.
- **Source Finding**: the `FND-XXX` identifier that produced this risk.
- **Impact**: the consequence if the risk is realized.
- **Likelihood**: how probable the risk is given the evidence.
- **Severity**: one of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- **Mitigation**: a neutral, optional action that would reduce the risk.

**Rating guidance**

Rate impact and likelihood from evidence, not intuition.

Impact bands:

- `LOW`: limited or cosmetic effect.
- `MEDIUM`: degraded function or contained outage.
- `HIGH`: major function loss or data integrity concern.
- `CRITICAL`: data loss, breach, or full outage.

Likelihood bands:

- `LOW`: would require an unusual combination of conditions.
- `MEDIUM`: plausible under normal operation.
- `HIGH`: expected to occur without intervention.

**Severity matrix**

| Impact \ Likelihood | LOW      | MEDIUM   | HIGH      |
|---------------------|----------|----------|-----------|
| CRITICAL            | HIGH     | CRITICAL | CRITICAL  |
| HIGH                | MEDIUM   | HIGH     | CRITICAL  |
| MEDIUM              | LOW      | MEDIUM   | HIGH      |
| LOW                 | LOW      | LOW      | MEDIUM    |

When the report language is Polish, translate the axis labels into Polish: `Wpływ`, `Prawdopodobieństwo`.

**Rules**

- One row per distinct risk. Do not merge unrelated risks.
- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- State each risk as a property of the system, never as a fault of a person.
- When a risk rests on missing information, mark its likelihood basis as `INSUFFICIENT INFORMATION` in the risk text.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for directives.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

## Trade-off Analysis

Present engineering trade-offs as a dedicated section before the Remediation Roadmap. A trade-off is a deliberate exchange of one quality for another.

Use a table with this fixed column order:

| Trade-off | Context | Option A: gain / cost | Option B: gain / cost | Evidence | Implication |
|-----------|---------|-----------------------|-----------------------|----------|-------------|

When the report language is Polish, translate the column headers into Polish: `Kompromis`, `Kontekst`, `Opcja A: zysk / koszt`, `Opcja B: zysk / koszt`, `Dowód`, `Implikacja`.

Column meanings:

- **Trade-off**: a short name for the tension.
- **Context**: the stated constraint or goal that frames the choice, or `NOT SPECIFIED`.
- **Option A**: the quality gained and the quality reduced for the first side.
- **Option B**: the quality gained and the quality reduced for the alternative.
- **Evidence**: what in the system shows this trade-off.
- **Implication**: the neutral consequence under the stated context.

**Rules**

- Frame each trade-off against a stated constraint. If no constraint is stated, put `NOT SPECIFIED` in Context and present the trade-off without judging the choice.
- Do not label either side as right or wrong outside an explicit recommendation request.
- A choice that fits the stated context is not a weakness, even if it would be unusual in a different context.
- Keep cell language neutral and anchored to evidence.
- Trade-off reasoning may also be embedded into individual finding blocks (under Description or Impact) when it directly explains a specific finding. The standalone table here surfaces the system-level tensions.

## Actionable Remediation Roadmap

This section transforms recommendations into a prioritized, traceable remediation plan. Every recommendation must resolve a specific finding.

**Prioritized matrix**

Present recommendations as a table. One row per recommendation. Use this fixed column order:

| Rec ID | Priority | Finding | Recommendation | Impact | Effort | Complexity | Verification |
|--------|----------|---------|----------------|--------|--------|------------|--------------|
| REC-001 | <P1-P4> | FND-XXX | <action> | <High/Med/Low> | <High/Med/Low> | <High/Med/Low> | <verification step> |

When the report language is Polish, translate the column headers into Polish: `Identyfikator rekomendacji`, `Priorytet`, `Znalezisko`, `Rekomendacja`, `Wpływ`, `Wysiłek`, `Złożoność`, `Weryfikacja`.

Column meanings:

- **Rec ID**: `REC-[001]` ascending.
- **Priority**: `P1` (immediate), `P2` (short-term), `P3` (medium-term), `P4` (long-term).
- **Finding**: the `FND-XXX` identifier this recommendation resolves.
- **Recommendation**: a concise, actionable technical step.
- **Impact**: the business or technical impact of applying this fix (`High`, `Medium`, `Low`).
- **Effort**: the estimated engineering effort to implement (`High`, `Medium`, `Low`).
- **Complexity**: the architectural or organizational complexity of the change (`High`, `Medium`, `Low`).
- **Verification**: a specific test, command, or process to confirm the fix is successful.

**Rules**

- Every `REC-XXX` entry must resolve a specific `FND-XXX`.
- Do not introduce new findings in this section. Recommendations must trace back to gaps in the Detailed Technical Findings.
- Keep language neutral and free of blame.
- Do not rank or select a single option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored to evidence, and the residual risk.
- When a recommendation would require information that was never provided, state the missing information rather than assuming it.

## Scope Exclusions

Explicitly define the limits of the analysis.

List components or environments that were not inspected unless they were explicitly provided in the input scope. Format each exclusion as a bullet with a bold label, followed by an empty line, then the explanation. Example:

```markdown
- **Firebird database schema and stored procedures**.

The database layer was assessed only from the API side. The actual tables, views, triggers, and stored procedures in Firebird were not provided.
```

Typical exclusions include:

- Operational runtime infrastructure (live servers, VMs, containers)
- Live network topologies and firewall rules
- Third-party authentication provider implementations
- Physical deployment environments
- End-user devices or browser clients
- Data backups or disaster-recovery procedures
- Penetration-test results or security audits performed by external firms

Mark each item as `NOT INSPECTED` or `EXCLUDED BY SCOPE`. If the user provided some of these, list them as `INCLUDED`.

State any extrapolations made from sampled code to the whole system.
