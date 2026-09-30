# Findings And Registers

## Purpose

> **Scope:** Strengths, detailed findings, the debt, risk, and roadmap registers, and the
> recommendation classification
> **Key items:** finding blocks, TDR items, RSK items, REC items, severity and priority
> vocabularies, recommendation classes

## Contents

| Section                        | Line | What it covers                       |
|--------------------------------|------|--------------------------------------|
| Strengths & What's Working     | 21   | Evidence-based positive baselines    |
| Detailed Technical Findings    | 59   | Finding summary and detail blocks    |
| Technical Debt Register        | 232  | Distinct accumulated debt            |
| Unified Risk Register          | 280  | Cross-referenced risks               |
| Actionable Remediation Roadmap | 371  | Prioritized recommendations          |
| Recommendation Classification  | 442  | Recommended/Optional/Not recommended |

## Strengths & What's Working

Add a short section with 5-8 bullet points acknowledging what the system does well.

This balances the tone of the report and anchors the scorecard with positive baselines.

Use a bullet list.

When a strength requires more than one sentence,
start the bullet with a bold heading on its own line, then add an empty line, then the body.

Anchor every claim to a concrete file, pattern, or decision.

Examples:

```markdown
- **TypeScript strict mode is enabled in both backend and frontend**.

`backend/tsconfig.json` and `frontend/tsconfig.app.json` both set `"strict": true`.

This catches a broad class of type errors at compile time.
```

For single-sentence strengths, keep them as plain bullets:

- Dependency injection is consistently applied in `Program.cs`, enabling testable service
  registration.
- Nullable reference types are enabled project-wide, reducing null-reference defects.
- SQL database connection pooling is configured with sensible `MinPoolSize` and `MaxPoolSize`
  values.
- JWT bearer authentication is implemented with standard ASP.NET Core middleware.

Do not invent strengths.

Only list what is evidenced in the provided files.

Use fewer than the suggested count when evidence is thin and state the limitation.

## Detailed Technical Findings

Present all findings grouped under six pillars,
plus the conditional API Compatibility & Versioning Discipline pillar when the subject is a reusable
library or package.

Each finding receives a unique deterministic index.

**Summary table:**

When the report language is not English, apply the heading translation from the matching
`translations/` file.

Present a compact summary of all findings:

| Finding     | Pillar                                    | Severity   | Title   | Result   | Status | Change | Verification |
|-------------|-------------------------------------------|------------|---------|----------|--------|--------|--------------|
| FND-ARC-001 | Architecture & Design                     | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-CQY-001 | Code Quality                              | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-SEC-001 | Security & Compliance                     | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-INF-001 | Infrastructure & CI/CD                    | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-AIP-001 | AI Provenance & Code Origin               | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-CPR-001 | Copyrights & Originality                  | <severity> | <title> | <result> | Open   | New    | <verifier>   |
| FND-API-001 | API Compatibility & Versioning Discipline | <severity> | <title> | <result> | Open   | New    | <verifier>   |

The `Title` column copies the finding's `### FND-…` heading verbatim - the summary never
rephrases a heading.

Column meanings:

- **Finding**: the `FND-XXX` identifier.
- **Result**: the assessment status of the evaluated control,
  `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, or `N/A`.
- **Status**: the finding lifecycle state, `Open`, `Closed`, or `PASS` for a re-verified
  passing control.
- **Change**: how the finding moved since the previous audit - `New`, `Unchanged`,
  `Reopened`, or `Closed`; first-audit findings always carry `New`.
- **Verification**: the evidence qualifier, `Verified`, `Confirmed`, `Reported`, or empty for
  a finding whose `Change` is `New`.

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Pillar abbreviations for IDs:

- `ARC` - Architecture & Design
- `CQY` - Code Quality
- `SEC` - Security & Compliance
- `INF` - Infrastructure & CI/CD
- `AIP` - AI Provenance & Code Origin
- `CPR` - Copyrights & Originality
- `API` - API Compatibility & Versioning Discipline (conditional, libraries and packages only)

When the report language is not English, apply the pillar name translations from the matching
`translations/` file.

Severity values: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
Result values: `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`, `N/A`.
Status values: `Open`, `Closed`, `PASS`.
Change values: `New`, `Unchanged`, `Reopened`, `Closed`.

When the report language is not English, these tokens render in the localized forms defined by
the matching `translations/` file, along with verification qualifiers `Verified`, `Confirmed`,
and `Reported`, and result markers such as `NOT RUN`, `NOT ASSESSED`,
`NOT INSPECTED`, `EXCLUDED BY SCOPE`, and `INSUFFICIENT INFORMATION`.

**Detailed findings**

After the summary table, write one block per finding in the same order.

Use this exact markdown block pattern:

```markdown
### FND-[PILLAR]-[NUMBER]: [Clear, Concise Title of Finding]

* **Pillar:** [Architecture & Design | Code Quality | Security & Compliance | Infrastructure &
  CI/CD | AI Provenance & Code Origin | Copyrights & Originality | API Compatibility &
  Versioning Discipline]
* **Severity:** [Critical | High | Medium | Low]
* **Type:** [Observation | Concern]
* **Security:** [CWE and rationale, CVSS version/vector/score or gap, or N/A]
* **Status:** [Open | Closed | PASS]
* **Change:** [New | Unchanged | Reopened | Closed]
* **Targets:** [Exact paths or components evaluated]
* **Basis:** [Applicable requirement or explicitly optional improvement]
* **Absence:** [No documented rationale | Deliberate - recorded decision | Undetermined |
  N/A] - [one-line evidence basis]
* **Description:** [Detailed technical explanation of the discovered state, architectural
  anti-pattern, or code flaw]
* **Impact:** [Concrete operational, business, or security consequence if left unremediated]
* **Recommendation:** [Step-by-step technical guidance to resolve the finding]
* **Method:** [Specific test, command, or process to confirm the fix is successful]
* **Verified:** [yes | no, with a short qualifier]
* **Confidence:** [HIGH / MEDIUM / LOW with rationale]
* **Mitigating factors:** [Refuting evidence examined and remaining uncertainty]
* **Exploitability:** [Tier + attack-path reasoning, or N/A with reason]
* **Evidence:** [EVD IDs, source lines, and inspected/reported/inferred basis]
```

When the report language is not English, apply the bullet label translations from the matching
`translations/` file.

Each finding must cite concrete evidence: file paths, config keys, commands, or direct quotes.

Do not crowd the bullet list with long prose.

Use short sentences separated by blank lines,
each sentence stands on its own line with an empty line between consecutive sentences.

Every finding must include a detailed Description, Impact, Recommendation,
and Method.

A finding with only a title and status is incomplete.

The Description must explain what the discovered state is,
where it is located (citing file paths and line numbers), and why it constitutes a finding.

The Impact must state the concrete consequence.

The Recommendation must provide step-by-step technical guidance.

The Method must specify a test or command to confirm the fix.

The `Verified` field states whether the current audit verified the claim:
`yes` for a re-derived or confirmed observation, `no` for pending verification,
each with a short qualifier such as `yes - observed in source`.

The `Status` field carries the lifecycle state: `Open`, `Closed`,
or `PASS` for a re-verified passing control.

The `Change` field carries the movement since the previous audit: `New`, `Unchanged`,
`Reopened`, or `Closed` - it records provenance, never a lifecycle state.

The `Type` field separates fact from judgment per `principles/evaluation-rules.md`:
`Observation` for a finding stating an independently re-derivable fact,
`Concern` for a risk judgment built on observations.

The `Absence` field carries the token from `principles/evaluation-rules.md` on every
finding that records an absent capability: `No documented rationale`, `Deliberate -
recorded decision`, or `Undetermined`, each followed by a one-line evidence basis.

Assert intent only when a documented decision or an equivalent record exists -
absence evidence alone never earns the `Deliberate` token.

On every other finding the field reads `N/A` with a one-line reason.

Most findings are `Concern`.

The `Exploitability` field is required on every `HIGH` or `CRITICAL` Security & Compliance
finding, following `references/exploitability-narrative.md`.

On a network-facing surface it carries the tier and attack-path reasoning.

Otherwise it reads `N/A` with a one-line reason.

When referencing secrets, credentials, or keys in the Description or Impact fields, replace exact
values with `[REDACTED]` or generic descriptions such as "plaintext database credentials found in
tracking file".

Keep trade-offs in the standalone section and embed relevant reasoning in the finding.

Every `CRITICAL` or `HIGH` finding needs an explicit counter-check.

For applicable security findings, place full CWE/CVSS rationale and versioned OWASP/ASVS mappings
below the summary table, following `assessment/security-review.md`.

Do not assign a CVSS score or adverse severity to an ordinary positive observation.

Place strengths in Strengths & What's Working rather than using `PASS` as a severity.

In shared sections, qualify IDs with the project identifier, including evidence, debt, risk, and
recommendation links.

## Technical Debt Register

Include this section only when the assessment surfaces structural debt distinct from risks,
per `synthesis/debt-register.md`.

Omit it when no such debt exists.

This register is distinct from the Unified Risk Register: risks describe what could go wrong, debt
describes accumulated cost that is already present.

Use the CISQ categories and SQALE-inspired cost guidance in `synthesis/debt-register.md`, claiming
full method application only when its models were used.

Use this fixed column order:

| Debt    | Item        | Category         | Source   | Cost           | Delay         | Status |
|---------|-------------|------------------|----------|----------------|---------------|--------|
| TDR-001 | <debt item> | <characteristic> | <FND ID> | <range or gap> | <cost or gap> | Open   |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Category is one of the CISQ characteristics: `Reliability`, `Performance Efficiency`, `Security`,
`Maintainability`.

Every item must trace to a `FND-XXX` or be marked `Direct observation` with a cited file.

Do not duplicate security risks here, those belong in the Unified Risk Register.

After the table, write one block per debt item in the same order.

Use this exact markdown block pattern:

```markdown
### TDR-[NUMBER]: [Clear, Concise Title of Debt Item]

* **Category:** [Reliability | Performance Efficiency | Security | Maintainability]
* **Source:** [FND-XXX or Direct observation]
* **Description:** [Detailed technical explanation of the debt, what it is, where it is located,
  and why it constitutes debt]
* **Cost:** [Supported effort range, unit, basis, confidence, or gap token]
* **Delay:** [Supported ongoing cost, horizon, basis, confidence, or gap token]
* **Status:** [Open | In progress | Resolved]
```

When the report language is not English, apply the bullet label translations from the matching
`translations/` file.

## Unified Risk Register

This section builds a cross-referenced risk table from the risks surfaced during assessment.

Every risk must trace back to a specific finding.

**Table format:**

| Risk    | Description     | Source  | Impact        | Likelihood    | Severity   | Mitigation |
|---------|-----------------|---------|---------------|---------------|------------|------------|
| RSK-001 | <concrete risk> | FND-XXX | <consequence> | <probability> | <severity> | <action>   |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Column meanings:

- **Risk**: `RSK-[001]` ascending.
- **Description**: a concrete technical risk, stated neutrally.
- **Source**: the `FND-XXX` identifier that produced this risk.
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

| Impact \ Likelihood | LOW    | MEDIUM   | HIGH     |
|---------------------|--------|----------|----------|
| CRITICAL            | HIGH   | CRITICAL | CRITICAL |
| HIGH                | MEDIUM | HIGH     | CRITICAL |
| MEDIUM              | LOW    | MEDIUM   | HIGH     |
| LOW                 | LOW    | LOW      | MEDIUM   |

When the report language is not English, apply the axis label translations from the matching
`translations/` file.

**Rules**

- One row per distinct risk. Do not merge unrelated risks.
- Every `RSK-XXX` entry must reference its source `FND-XXX`.
- State each risk as a property of the system, never as a fault of a person.
- When a rating is unsupported, use `UNKNOWN`, state the missing evidence, and omit it from
  numeric aggregation and risk-map placement, per `synthesis/risk-register.md`.
- Mitigations are options, not directives. Do not phrase them as commands unless the user asked for
  directives.
- Do not output plaintext secrets, passwords, or cryptographic keys in the Risk column.

After the table, write one block per risk in the same order.

Use this exact markdown block pattern:

```markdown
### RSK-[NUMBER]: [Clear, Concise Title of Risk]

* **Severity:** [LOW | MEDIUM | HIGH | CRITICAL]
* **Likelihood:** [How probable the risk is given the evidence, with justification]
* **Residual:** [Remaining risk after the proposed mitigation, or `UNKNOWN`]
* **Status:** [Open | Accepted | Transferred | Monitoring | Closed]
* **Owner:** [Role or `NOT SPECIFIED`]
* **Description:** [Detailed technical explanation of the risk, what could go wrong, and under
  what conditions]
* **Impact:** [Concrete consequence if the risk is realized]
* **Trigger:** [Threat, failure event, or predisposing condition]
* **Controls:** [Present controls and verification state]
* **Mitigation:** [Neutral, optional action that would reduce the risk]
* **Closure:** [Evidence or event that starts re-verification]
* **Source:** [FND-XXX]
* **Confidence:** [HIGH | MEDIUM | LOW with rationale]
```

When the report language is not English, apply the bullet label translations from the matching
`translations/` file.

## Actionable Remediation Roadmap

This section transforms recommendations into a prioritized, traceable remediation plan.

Every recommendation must resolve a specific finding.

**Prioritized matrix**

Present recommendations as a table.

One row per recommendation.

Use this fixed column order:

| Rec     | Priority | Finding | Recommendation | Impact         | Effort         | Complexity     | Verification        |
|---------|----------|---------|----------------|----------------|----------------|----------------|---------------------|
| REC-001 | <P1-P4>  | FND-XXX | <action>       | <High/Med/Low> | <High/Med/Low> | <High/Med/Low> | <verification step> |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Column meanings:

- **Rec**: `REC-[001]` ascending.
- **Priority**: `P1` (immediate), `P2` (short-term), `P3` (medium-term), `P4` (long-term).
- **Finding**: the `FND-XXX` identifier this recommendation resolves.
- **Recommendation**: a concise, actionable technical step.
- **Impact**: the business or technical impact of applying this fix (`High`, `Medium`, `Low`).
- **Effort**: the estimated engineering effort to implement (`High`, `Medium`, `Low`).
- **Complexity**: the architectural or organizational complexity of the change (`High`, `Medium`,
  `Low`).
- **Verification**: a specific test, command, or process to confirm the fix is successful.

**Rules**

- Every `REC-XXX` entry must resolve a specific `FND-XXX`.
- Do not introduce new findings in this section. Recommendations must trace back to gaps in the
  Detailed Technical Findings.
- Keep language neutral and free of blame.
- Do not rank or select a single option unless the user explicitly asks for a recommendation.
- When the user does ask for a single recommendation, state the chosen option, the reason anchored
  to evidence, and the residual risk.
- When a recommendation would require information that was never provided, state the missing
  information rather than assuming it.

After the table, write one block per recommendation in the same order.

Use this exact markdown block pattern:

```markdown
### REC-[NUMBER]: [Clear, Concise Title of Recommendation]

* **Priority:** [P1 | P2 | P3 | P4]
* **Finding:** [FND-XXX]
* **Description:** [Detailed technical explanation of the recommended action, what it changes,
  and how it resolves the finding]
* **Impact:** [Business or technical impact of applying this fix]
* **Effort:** [Estimated engineering effort with one-line justification]
* **Complexity:** [Architectural or organizational complexity with one-line justification]
* **Verification:** [Specific test, command, or process to confirm the fix is successful]
```

When the report language is not English, apply the bullet label translations from the matching
`translations/` file.

For readiness or due diligence, include the supported cost rollup and dependency ordering from
`synthesis/remediation-roadmap.md`, counting shared work only once.

Numeric totals require evidence-based compatible units, unknown work remains visible beside any
known subtotal.

## Recommendation Classification

Include this section when the detail level is `Standard` or `Detailed` and the Actionable
Remediation Roadmap is present.

Omit it at `Brief`, or when improvement suggestions are disabled, and record the omission in
Scope Exclusions.

The section follows the Actionable Remediation Roadmap and precedes Scope Exclusions.

It assigns every recommendation a disposition class so the report can serve directly as a basis
for change documents.

Not every accurate finding warrants action at the current moment, the class records that judgment.

Use this fixed column order:

| Rec     | Recommendation | Class   | Basis          |
|---------|----------------|---------|----------------|
| REC-001 | <action>       | <class> | <short reason> |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Column meanings:

- **Rec**: the `REC-[001]` identifier from the Actionable Remediation Roadmap.
- **Recommendation**: the recommendation summary from the roadmap row.
- **Class**: one of `Recommended`, `Optional`, or `Not recommended`.
- **Basis**: a short reason for the classification, such as `blocks readiness gate`,
  `optional improvement`, or `intent undetermined`.

**Rules**

- Every `REC-XXX` in the roadmap appears exactly once in this table.
- The class complements the P1-P4 priority: priority orders urgency, class records whether the
  report advises acting now given current evidence.
- A `Not recommended` row keeps its priority for the moment its blocking uncertainty resolves.
- After the table, write one paragraph per `Not recommended` entry naming the evidence or decision
  that would reclassify it, using the bold-heading paragraph pattern.
- The section introduces no new findings and no new recommendations.
- In a multi-project report the section is per-project, following that project's roadmap.
