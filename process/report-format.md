# Report Format

## Purpose

> **Scope:** The required structure and template for the final audit report
> **Key items:** document metadata, executive summary with health dashboard, methodology, system context, detailed findings, unified risk register, remediation roadmap, scope exclusions

This file defines the exact shape of the audit report. Produce the sections in this order.

The report applies to any software subject: a prototype, a codebase under development, or an already-running production system. Adjust which categories apply, not the structure.

Keep every section even when content is `UNKNOWN`. A present-but-empty section signals a gap; a missing section hides it.

## Formatting Rules

Use a hybrid table-paragraph format in every section.

Tables provide the scannable summary. Paragraphs below the table provide the detailed evidence, risks, and reasoning.

In tables, use shortened, general values. One or two words per cell. Do not crowd table cells with long explanations. Save detail for the paragraphs.

Do not number section headings. Use the section name as the heading, for example "Executive Summary & Health Dashboard", not "2. Executive Summary & Health Dashboard". When the user requests a specific language, translate the section heading into that language.

Keep column headers identical to the templates below across every audit. When the user requests a specific language, translate the column headers into that language while keeping the structure identical.

Within a table cell, separate multiple points with a semicolon or a line break, not with sub-bullets.

Place descriptive paragraphs immediately after each table. In the paragraphs, explain every aspect with concrete evidence, file paths, and reasoning. Use short sentences separated by line breaks.

Start each detailed paragraph with a bold heading on its own line. Put the status, score, or severity inline after the heading, separated by a space. Then add an empty line, then the paragraph body. Do not run the heading and the body together on the same line.

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

## Report Delivery And Parameter Configuration

Report delivery is determined during the Parameter Configuration phase in `process/workflow.md`. Do not ask delivery questions here; they are handled upstream.

When the user names an output file in the original request, for example "write the audit to AUDIT.md", honor that filename without asking again.

When the user invokes an audit without naming an output file, for example "perform lens on this service" or "make audit report on the codebase", the Parameter Configuration phase determines delivery and filename.

Default delivery is **Inline** (direct response). Default filename is **AUDIT.md** when File mode is selected.

For a single-dimension request that produces only a short subsection, returning the result inline is acceptable without asking, unless the user asked for a file.

## Detail Level Configuration

The report adapts to the detail level chosen during Parameter Configuration.

**Standard**

All eight sections are present in full:

- Document & Stack Metadata
- Executive Summary & Health Dashboard
- Auditing Methodology & Scoring Rubrics
- System Context & Architectural Assessment
- Detailed Technical Findings & Assessment (all findings with full Description, Impact, Remediation, and Verification)
- Unified Risk Register
- Actionable Remediation Roadmap (full matrix with P1-P4, impact/effort/complexity, verification)
- Scope Exclusions

**Detailed**

Same eight sections as Standard, plus the following extensions:

- Executive Summary includes an expanded Risk Heat Map with all risks plotted.
- Architectural Assessment includes deeper critique with additional industry baseline comparisons.
- Each finding includes extended verification methods and alternative remediation paths.
- Remediation Roadmap includes additional context for each recommendation (blocking dependencies, estimated timeframes).

**Brief**

Condensed output for rapid review:

- Document & Stack Metadata (full)
- Executive Summary & Health Dashboard (full summary table and risk heat map)
- Scorecard Summary table only (omits the per-dimension detailed paragraphs)
- Top 5 findings only (summary table and abbreviated detail blocks)
- Top 5 risks only (summary table)
- Key recommendations only (top 5, no full matrix)
- Scope Exclusions (full)

Omitted in Brief: Auditing Methodology & Scoring Rubrics, System Context & Architectural Assessment detailed critique, full Detailed Technical Findings list, full Unified Risk Register, full Actionable Remediation Roadmap.

## Section Order

The report has these top-level sections, in this order, with unnumbered headings:

- Document & Stack Metadata
- Executive Summary & Health Dashboard
- Auditing Methodology & Scoring Rubrics
- System Context & Architectural Assessment
- Detailed Technical Findings & Assessment
- Unified Risk Register
- Actionable Remediation Roadmap
- Scope Exclusions

## Document & Stack Metadata

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

Anchor each entry to evidence, such as a manifest, lockfile, or config file. Mark any layer the input does not reveal as `NOT SPECIFIED`. Add or omit rows to fit the subject, but keep the layer names in this column.

## Executive Summary & Health Dashboard

Provide a compact overview a reader can absorb without the detail sections.

Use a key-value table:

| Field          | Value                                                                          |
|----------------|--------------------------------------------------------------------------------|
| System type    | <prototype / codebase / production system / proposal>                          |
| Scope          | <what was reviewed and what was excluded>                                      |
| Source basis   | <running system / inspected code / description>                                |
| Maturity level | <`Prototype` / `Early development` / `Pre-production` / `Production-ready` / `Undetermined`> |

**Summary description**

Write one paragraph immediately after the table. State the system's purpose in one sentence. Summarize the overall condition in one sentence. Note the maturity level and anchor it to evidence from later sections. Mention any critical finding that the reader should know first. Keep the paragraph to four sentences maximum.

The maturity level must be justified by evidence in later sections, not asserted.

**Risk Heat Map**

Provide a consolidated Likelihood vs Impact matrix summarizing the top risks. Use a table:

| Impact \ Likelihood | LOW | MEDIUM | HIGH |
|---------------------|-----|--------|------|
| CRITICAL            |     |        |      |
| HIGH                |     |        |      |
| MEDIUM              |     |        |      |
| LOW                 |     |        |      |

Populate cells with `RSK-XXX` identifiers from the Unified Risk Register. Leave empty cells blank. Do not include plaintext secrets, passwords, or cryptographic keys in this summary. Use generic descriptions or masked placeholders.

**Scorecard Summary**

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

## Auditing Methodology & Scoring Rubrics

This section defines the evaluation framework so that scores are objective and reproducible. Present it before any scored findings.

**Methodology overview**

State that the audit uses evidence-based reasoning across 16 assessment categories grouped into four pillars. List the pillars:

- **Architecture & Design** - Design principles, maintainability, change management, documentation, non-functional requirements
- **Code Quality** - Testing, code quality, stack best practices
- **Security & Compliance** - Security, compliance and data protection
- **Infrastructure & CI/CD** - Dependencies, deployment, rollback, observability, error handling, operational readiness

**Scoring rubric**

Present the rubric matrix that defines what constitutes each score band. Use the default 1-10 scale unless the user requested the 1-5 alternative.

For the 1-10 scale:

| Band | Score Range | Definition |
|------|-------------|------------|
| Excellent | 9-10 | Capability is comprehensive and verified by strong evidence |
| Good | 7-8 | Capability is solid overall; minor or noticeable gaps exist |
| Average | 4-6 | Capability is present but uneven, limited, or inconsistent |
| Poor | 1-3 | Capability is minimal, fragmentary, or absent where required |

For the 1-5 alternative scale:

| Band | Score Range | Definition |
|------|-------------|------------|
| Excellent | 5 | Capability is comprehensive and verified by strong evidence |
| Good | 4 | Capability is solid with minor gaps |
| Average | 3 | Capability is adequate but uneven |
| Poor | 1-2 | Capability is minimal, limited, or absent where required |

**Zero is not a score.** The value `0` is reserved and never used. When a dimension cannot apply, mark it `N/A`.

## System Context & Architectural Assessment

Describe the system as understood from the input, then provide an architectural critique against industry baselines.

**System context table:**

| Aspect                | Detail                                          |
|-----------------------|-------------------------------------------------|
| Functional description| <what the system does>                          |
| Architecture overview | <high-level structure>                          |
| Key components        | <named components or modules>                   |
| External dependencies | <services, libraries, platforms>                |
| Assumptions           | <only if explicitly stated, else `NOT SPECIFIED`> |

Mark any unknown aspect as `NOT SPECIFIED`.

**Architectural assessment**

After the context table, write one or more paragraphs critiquing the architecture. Evaluate coupling, cohesion, state management, separation of concerns, and pattern consistency against the stated constraints. Anchor every claim to a concrete file path or design decision. Do not judge the stack choice itself.

## Detailed Technical Findings & Assessment

This section replaces the previous Quality Assessment and High-Level Observations. Present all findings grouped under four pillars. Each finding receives a unique deterministic index.

**Summary table:**

Present a compact summary of all findings:

| Finding ID | Pillar | Severity | Title | Status |
|------------|--------|----------|-------|--------|
| FND-ARC-001 | Architecture & Design | <severity> | <title> | <status> |
| FND-CQ-001 | Code Quality | <severity> | <title> | <status> |
| FND-SEC-001 | Security & Compliance | <severity> | <title> | <status> |
| FND-INF-001 | Infrastructure & CI/CD | <severity> | <title> | <status> |

Pillar abbreviations for IDs:

- `ARC` - Architecture & Design
- `CQ` - Code Quality
- `SEC` - Security & Compliance
- `INF` - Infrastructure & CI/CD

Severity values: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
Status values: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`.

**Detailed findings**

After the summary table, write one block per finding in the same order. Use this exact markdown block pattern:

```markdown
### FND-[PILLAR]-[NUMBER]: [Clear, Concise Title of Finding]

* **Pillar:** [Architecture & Design | Code Quality | Security & Compliance | Infrastructure & CI/CD]
* **Severity:** [Critical | High | Medium | Low]
* **Target Files/Modules:** [Exact paths or components evaluated]
* **Description:** [Detailed technical explanation of the discovered state, architectural anti-pattern, or code flaw]
* **Impact:** [Concrete operational, business, or security consequence if left unremediated]
* **Remediation Recommendation:** [Step-by-step technical guidance to resolve the finding]
* **Verification Method:** [Specific test, command, or process to confirm the fix is successful]
```

Each finding must cite concrete evidence: file paths, config keys, commands, or direct quotes. Do not crowd the bullet list with long prose. Use short sentences separated by line breaks.

When referencing secrets, credentials, or keys in the Description or Impact fields, replace exact values with `[REDACTED]` or generic descriptions such as "plaintext database credentials found in tracking file".

Trade-off analyses that were previously in a standalone section should be embedded directly into the relevant finding they impact, under the Description or Impact bullet.

## Unified Risk Register

This section builds a cross-referenced risk table from the risks surfaced during assessment. Every risk must trace back to a specific finding.

**Table format:**

| Risk ID | Risk | Source Finding | Impact | Likelihood | Severity | Mitigation |
|---------|------|----------------|--------|------------|----------|------------|
| RSK-001 | <concrete risk> | FND-XXX | <consequence> | <probability> | <severity> | <action> |

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

**Rules**

- One row per distinct risk. Do not merge unrelated risks.
- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- State each risk as a property of the system, never as a fault of a person.
- When a risk rests on missing information, mark its likelihood basis as `INSUFFICIENT INFORMATION` in the risk text.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for directives.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

## Actionable Remediation Roadmap

This section transforms recommendations into a prioritized, traceable remediation plan. Every recommendation must resolve a specific finding.

**Prioritized matrix**

Present recommendations as a table. One row per recommendation. Use this fixed column order:

| Rec ID | Priority | Finding | Recommendation | Impact | Effort | Complexity | Verification |
|--------|----------|---------|----------------|--------|--------|------------|--------------|
| REC-001 | <P1-P4> | FND-XXX | <action> | <High/Med/Low> | <High/Med/Low> | <High/Med/Low> | <verification step> |

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

List components or environments that were not inspected unless they were explicitly provided in the input scope. Typical exclusions include:

- Operational runtime infrastructure (live servers, VMs, containers)
- Live network topologies and firewall rules
- Third-party authentication provider implementations
- Physical deployment environments
- End-user devices or browser clients
- Data backups or disaster-recovery procedures
- Penetration-test results or security audits performed by external firms

Mark each item as `NOT INSPECTED` or `EXCLUDED BY SCOPE`. If the user provided some of these, list them as `INCLUDED`.

State any extrapolations made from sampled code to the whole system.
