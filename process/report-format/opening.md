# Opening Sections

## Purpose

> **Scope:** Document information, audit-type coverage, and glossary at the top of the report
> **Key items:** document information, coverage matrix, glossary, descriptive-mode gate

## Contents

| Section              | Line | What it covers                       |
|----------------------|------|--------------------------------------|
| Document Information | 16   | Report metadata and revisions        |
| Audit Type Coverage  | 121  | Coverage of canonical audit types    |
| Glossary             | 171  | Abbreviation and acronym definitions |

## Document Information

Open the report with a document title as a level-1 markdown heading (`#`), followed by the
`## Document Information` section.

Present the document metadata as a two-column table with an empty header row and no column
names:

```markdown
# <System Name> Software Audit Report

## Document Information

|                  |                                              |
|------------------|----------------------------------------------|
| Report Revision  | 1.2                                          |
| Report Date      | 2026-09-17                                   |
| Detail Level     | Detailed                                     |
| Evaluation Scale | 1-10                                         |
| Time taken       | 47:32                                        |
| Previous Report  | docs/audit/26.7.0/AUDIT-1.1.md, revision 1.1 |
```

Pad the empty header cells to the column width like any other cell.

Rows appear in this order, each label in the first column and its value in the second:

- `Report Revision` - the report document revision, assigned per the report revision rules below.
- `Report Date` - the audit date.
- `State` - `Draft` only. Write the row while the report is still in progress and omit it when the
  report is final, which is the expected end state and needs no marker.
- `Detail Level` - `Standard`, `Detailed`, or `Brief`.
- `Evaluation Scale` - `1-10`, `1-5`, `1-3`, `5 stars`, or `3 stars`.
- `Language` - the report language.
- `Audit Purpose` - engineering improvement, production readiness, or technical due diligence.
- `Target Environment` - where the software runs or ships.
- `Verification Scope` - always `static repository analysis (code, configuration,
  documentation, git history) - no execution`; the short token `source-only` may stand
  when a previous revision already established it.
- `Subject Revision` - the audited revision of the subject, such as a commit hash.
- `Dirty-Tree State` - the working tree state at audit time, written only when the tree is dirty.
  Omit the row when the tree is clean.
- `Skill Version` - the version of the audit skill that produced the report.
- `Time taken` - elapsed audit time in `MM:SS`, measured from the start timestamp recorded after
  parameter questions were resolved to the final clock reading before report delivery.
- `Previous Report` - the previous report path and revision, only on a confirmed re-audit. Omit
  the row on a fresh audit.
- `Projects` - the audited project names, multi-project reports only.

Omit a row entirely when the input does not establish its value.

Never write an empty value cell or a `NOT SPECIFIED` token in this table.

Do not include a `Delivery Mode` or `Report Delivery` row.

Whether the report was delivered as a file or an inline response is evident from the delivery
itself.

Do not include a `Descriptive Mode` row.

The setting is evident from the presence or absence of the Glossary section,
and a re-audit recovers it that way.

The word `revision` refers to the report document.

The word `version` refers to the audited software, a project, a library, or the skill itself,
as in `Subject Revision` for the audited commit and `Skill Version` for the skill.

For a multi-project audit, use the repository or directory name as the system name in the title
and include the `Projects` row.

These fields support reproducible re-audits and prevent historical tool results being attributed
to a different tree.

A report without a `State` row is final: the scoped report is complete, which does not mean the
system is approved for production.

**Report revision**

The first audit of a subject is revision `1.0`.

When a previous audit report exists, read the `Report Revision` value from its Document Information
table, increment the minor component up to 9 (for example, `1.0` to `1.1`, `1.9` to `2.0`,
`9.9` to `10.0`), and write the incremented revision into the new report.

This applies to both a confirmed re-audit and a fresh audit.

When the previous report records no revision, treat it as `1.0` and assign `1.1`.

Earlier reports may record the document revision differently: a bold-label `Version` field,
or a `Field`/`Value` table with a `Version` row.

Read any of these forms as the report revision.

The previous report file is never overwritten.

The new report is written to a separate file carrying the new revision in its name,
for example `AUDIT-1.1.md`, per `synthesis/report-comparison.md`.

When the report language is not English,
apply the label translations from the matching `translations/` file.

Descriptive values such as `State`, `Detail Level`, `Evaluation Scale`, `Audit Purpose`,
and `Verification Scope` are rendered per the same file.

## Audit Type Coverage

State at a glance which canonical audit types this report answers and which it deliberately does
not run.

The table makes the report's coverage explicit so it cannot be mistaken for a penetration test,
a certifying audit, or a full technical due diligence.

The section appears once per report, immediately after `## Document Information` and before
`## Project Inventory` in a multi-project report, or before `## Glossary` in a single-project
report.

Present the fixed table from `references/audit-taxonomy.md`, one row per canonical audit type
whose status is not `Not Applicable`.

A type classified `Not Applicable` produces no row - the table never mentions audit types that
do not apply to the subject.

|  | Report type                           | Status   | Rationale                              |
|--|---------------------------------------|----------|----------------------------------------|
|  | Software Architecture Review          | <status> | <why this status holds for this audit> |
|  | Code Quality Audit                    | <status> | <why this status holds for this audit> |
|  | Security Vulnerability Assessment     | <status> | <why this status holds for this audit> |
|  | Open Source License Compliance Review | <status> | <why this status holds for this audit> |
|  | Penetration Test                      | <status> | <why this status holds for this audit> |
|  | Performance Audit                     | <status> | <why this status holds for this audit> |
|  | Cloud Infrastructure Audit            | <status> | <why this status holds for this audit> |
|  | AI Governance Audit                   | <status> | <why this status holds for this audit> |
|  | Technical Due Diligence               | <status> | <why this status holds for this audit> |
|  | SBOM / Software Composition Analysis  | <status> | <why this status holds for this audit> |
|  | ISO/IEC 27001 Certification           | <status> | <why this status holds for this audit> |
|  | SOC 2 Attestation Examination         | <status> | <why this status holds for this audit> |

Status values come from the fixed vocabulary in `references/audit-taxonomy.md`: `Covered`,
`Partially`, `Not done`, `Not Applicable`.

A `Not Applicable` status is decided per type but never rendered as a row.

Default statuses and per-type rationale are defined there.

A status other than the default carries its reason in the Rationale column.

When the report language is not English, apply the column header, report-type, and status
translations from the matching `translations/` file.

The matrix must agree with Scope Exclusions: every `Not done` row has a matching exclusion bullet,
and no `Covered` row is later disclaimed.

PAR-11 checks this consistency.

## Glossary

The Glossary defines every abbreviation and acronym used in the report.

It is present when Descriptive mode is `Enabled` (the default)
and omitted when Descriptive mode is `Disabled`.

When omitted, record the deliberate omission with a one-line justification in Scope Exclusions.

The section appears immediately after `## Audit Type Coverage`, or after
`## Project Inventory` in a multi-project report, and always before `## Executive Summary`.
A multi-project report carries one shared Glossary covering terms used in every project block.

**Index table**

Present the terms as a two-column table, one row per term, sorted alphabetically ignoring case.

The Term cell holds the acronym in plain form,
or a markdown link when the term carries a long description below the table.

The Definition cell gives the expansion plus one clause of plain-language meaning or role in
context.

```markdown
## Glossary

| Term                                 | Definition                                                        |
|--------------------------------------|-------------------------------------------------------------------|
| API                                  | Application Programming Interface - the frontend-backend contract |
| [RPO](#rpo-recovery-point-objective) | Recovery Point Objective - tolerable data loss measured as time   |
| [SLO](#slo-service-level-objective)  | Service Level Objective - measurable service-quality target       |
```

**Long descriptions**

Terms that need more than an expansion get a `###` subsection below the index table,
still inside `## Glossary`, sorted alphabetically by term ignoring case, matching the index
table's ordering rule.

A term serving as a fixed identifier prefix throughout the report - `EVD`, `FND`, `RSK`,
`REC`, `TDR`, `PAR` - carries a `###` description rather than an index-only row, since the
reader meets it in every register and finding block.

Name each subsection `### TERM (Expansion)` when the expansion is established,
or `### TERM` when it is not.

A term with a subsection links its table cell to that subsection's anchor,
for example `[SLO](#slo-service-level-objective)`.

Derive the anchor from the heading text: lowercase it, remove punctuation,
and replace spaces with hyphens.

Choose the subset deliberately.

Good candidates are operational objectives such as `SLO`, `RPO`, and `RTO`,
report-internal identifier prefixes such as `EVD`, `FND`, `RSK`, `REC`, `TDR`, and `PAR`,
and subject-specific terms whose role needs explanation.

Most terms stay index-only.

```markdown
### SLO (Service Level Objective)

A measurable target for service quality, for example "99.9% of API requests succeed" or "p95
latency under 300ms". SLOs tell operators, and an audit, what "healthy" means quantitatively.
Without them there is no agreed threshold for when the platform is failing its users.
```

**Body linking**

Every occurrence of a glossary term in the report body is a markdown link.

When the term has a long-description subsection, link to that subsection's anchor,
for example `[SLO](#slo-service-level-objective)`.

Otherwise link to the index table at `#glossary`, for example `[API](#glossary)`.

Apply the rule to prose and table cells.

Exempt:

- The Glossary section itself, including its index table and `###` descriptions.
- Headings, fenced code blocks, inline code, existing link text, and URLs.
- Occurrences inside a longer hyphenated or slashed identifier, such as `FND` inside
  `FND-SEC-001`, `REC` inside `REC-BE-01`, or `PAR` inside `PAR-10`, and occurrences inside a
  longer word, such as `SQL` inside `SQLite` or `API` inside `OpenAPI`. Link the whole compound
  instead when the compound itself is a glossary term, such as `[SI-API](#si-api)` or
  `[ISO/IEC](#glossary)`.
- Acronyms that are part of a capitalized compound name: an acronym adjacent by whitespace to a
  word starting with an uppercase letter on either side, for example `AI` in `AI Provenance`,
  `API` in `API Compatibility & Versioning Discipline`, `UI` in `Material UI`, or `RMF` in
  `NIST RMF`. Adjacent acronym pairs count as compounds too, so `the REST API` and `NIST RMF`
  stay fully unlinked. Sentence-initial function words such as `The`, `A`, `Every`, and `No` do
  not create compounds - `The PWA` still links.
- Inflected forms keep the suffix inside the link text, for example
  `[SLOs](#slo-service-level-objective)`.

Apply body linking with a scripted pass rather than by hand.

A report can hold hundreds of standalone acronym occurrences,
and the reliable procedure is to walk the body once with the report's own index table and `###`
anchors, skipping the exemptions above, and to rerun the pass after any late content edit.

Hand-linking a long report reliably leaves misses that PAR-10 and `validate-report.py` then surface
one by one.

Three discipline notes keep new prose from reintroducing failures the pass just cleared:

- Prose added after the first pass reintroduces unlinked occurrences, so any new section or
  edited paragraph triggers a rerun of the whole pass, not a spot check.
- An acronym first introduced by new content must exist in the index table before it is linked
  in the body. Adding `SPDX` to a new section, for example, requires a matching index row first.
- `N/A` is itself a glossary term, so a bare `N/A` in prose fails the same check. Prefer the
  words `Not applicable` in sentences where no status token is required.
- The compound-name exemption fails in both directions: a standalone acronym left unlinked is
  flagged, and a linked acronym adjacent to a capitalized compound word is flagged too, so
  `the [VPS](#glossary) deployment` passes while `Traefik [VPS](#glossary)` does not.

**Mechanical traps**

The validator enforces these additional rules that routine drafting tends to violate.

State them here so the prose contract and the mechanical check agree.

- `SLO`, `RPO`, and `RTO` are always indexed. The index table must carry a row for each even
  when the report body never uses them, for example a subject with no service-level vocabulary.
- A spaced slash does not form a compound. `SBOM / Software` still requires `[SBOM](#glossary)`
  on the acronym, only the adjacent form `SBOM/Software` is exempt.
- Machine-readable `* **Field:**` value positions are exempt from linking when the field
  carries a fixed-vocabulary token. The exempt labels are `Pillar`, `Severity`, `Type`,
  `Security`, `Status`, `Change`, `Absence`, `Verified`, `Confidence`, `Class`, `Result`,
  `Priority`, `Likelihood`, `Residual`, `Owner`, and `Exploitability`. The value of such a
  line stays literal even when the token is a glossary term, so `* **Priority:** P2` keeps a
  bare `P2` and `* **Absence:** N/A` keeps a bare `N/A`. A `* **Field:**` label not on this
  list still links normally.
- The status tokens that populate those fields - `N/A`, `PASS`, `FAIL`, `UNKNOWN`,
  `NOT RUN`, `NOT PERFORMED`, `NOT SPECIFIED`, `INSUFFICIENT INFORMATION`, `NO BASELINE`,
  `NO GAPS` - are a fixed vocabulary. They may be indexed as terms when the report uses them
  in prose, but inside the exempt field values above they are data, not glossary terms.
- Parenthesized terms such as `HTTP(S)` cannot carry a `###` description, the term is parsed
  before the parenthesis, keep them index-only.
- A link must point at the term's own anchor: `[SLO](#slo...)` when the term has a `###`
  subsection, `[API](#glossary)` when it does not. Linking a described term to `#glossary`,
  or an index-only term to a `###` slug, both fail.
- References tables are not exempt: standalone publisher cells such as `| ISO |` and
  `| NIST |` link like any other occurrence.
- Link text must be the term or a known variant exactly: `[EVD](#glossary)` passes,
  `[EVD-001](#glossary)` fails because `EVD-001` is not a term, cite the bare `EVD-001`
  unlinked instead, the hyphenated form is already exempt.

**Coverage**

Include every abbreviation and acronym used anywhere in the report body:

- Report-internal identifier prefixes such as `EVD`, `FND`, `RSK`, `REC`, `TDR`, and `PAR`.
- Priority tiers `P1`-`P4` and abbreviation-shaped tokens such as `N/A`.
- Technology and standard names such as `API`, `CWE`, `CVSS`, `OWASP`, `STRIDE`, `SBOM`,
  `SLO`, `RPO`, `RTO`, `PWA`, `SPA`, `CI/CD`, `TOTP`, `HMAC`, `CSP`, and `i18n`.
- Subject-specific terms established by the audited project, such as product or protocol names.

Each definition expands the abbreviation and adds one clause of plain-language meaning or role in
context, as in the SLO, RPO, and RTO examples above.

Do not list ordinary words, brand or product names that are not abbreviations, file extensions,
command names, or fixed vocabulary tokens that are complete words such as `PASS`, `FAIL`, `UNKNOWN`,
or `NOT SPECIFIED`.

Do not invent expansions for product names the audited source does not establish,
describe the term's role instead.

When the report language is not English, keep each term in its original form and write the
definition in the report language, per the matching `translations/` file.
