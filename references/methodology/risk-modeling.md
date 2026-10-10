# Risk And Threat Modeling Baseline

## Purpose

> **Scope:** Vocabulary and classification anchors for risk registers, threat models, and
> severity ratings
> **Key items:** NIST risk vocabulary, RMF monitor step, STRIDE categories, CVSS v4 vector
> structure, CWE Top 25 anchors

This file distills the NIST, Microsoft, FIRST, and MITRE sources listed in
`references/source-catalog.md` into the anchors an audit uses for risk and threat findings.

Snapshot date: 2026-10-09.

Feeds `assessment/threat-model.md`, `synthesis/risk-register.md`, and
`references/exploitability-narrative.md`.

## NIST Risk Vocabulary

From NIST SP 800-30 Rev 1 (https://csrc.nist.gov/pubs/sp/800/30/r1/final) and SP 800-37 Rev 2
(https://csrc.nist.gov/pubs/sp/800/37/r2/final, overview:
https://csrc.nist.gov/Projects/risk-management/about-rmf).

- SP 800-30 defines the assessment vocabulary: threat source, threat event, vulnerability,
  predisposing condition, likelihood, impact - the audit's risk model uses these terms
  verbatim.
- Likelihood and impact are rated per the assessing model (qualitative Low/Moderate/High is
  Lens's default). "risk" is the joint function, never likelihood alone.
- SP 800-37 RMF steps: Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor -
  the Monitor step justifies re-audit triggers and remediation verification.
- A "risk" without a threat event and an impact path is an observation, not a register entry.

## STRIDE

From Microsoft's threat-modeling documentation
(https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) and
the OWASP threat-modeling overview (https://owasp.org/www-community/Threat_Modeling).

- The six categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of
  Service, Elevation of Privilege - apply per element of the data-flow model (external
  entity, process, data store, data flow).
- STRIDE applies per trust boundary: enumerate what crosses, then ask which categories apply.
  a threat list not anchored to a boundary is prose, not a model.
- `assessment/threat-model.md` owns the per-element mapping table.

## CVSS v4

From https://www.first.org/cvss/v4-0/specification-document and
https://www.first.org/cvss/v4.0/user-guide.

- CVSS v4 base metrics: AV (attack vector), AC (attack complexity), AT (requirements), PR
  (privileges), UI (user interaction), VC/VI/VA (vulnerable-system impacts), SC/SI/SA
  (subsequent-system impacts). The vector string order is fixed
  (`CVSS:4.0/AV:./AC:./AT:./PR:./UI:./VC:./VI:./VA:./SC:./SI:./SA:. `).
- Base score alone is not a rating of the deployed system - environmental and threat metrics
  adjust it. A report quoting only base scores notes that limitation.
- CVSS measures severity of a vulnerability, not risk posture of a codebase. Findings get a
  severity tier, the register gets the priority decision.

## CWE Anchors

From https://cwe.mitre.org/, https://cwe.mitre.org/top25/, and
https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html.

- The CWE Top 25 is a dated ranking of dangerous weaknesses. The audit cites specific CWE
  numbers (for example CWE-79 XSS, CWE-89 SQLi, CWE-494 unsigned download) rather than the
  ranking itself.
- CWE-494 (https://cwe.mitre.org/data/definitions/494.html) anchors the
  download-without-integrity-check class used by `references/topics/git-integrity.md` and
  Electron distribution findings.
- CWE entries are weaknesses (code-level defect classes), distinct from CVEs (specific
  instances in shipped products) and CAPECs (attack patterns) - findings cite CWE, known
  advisories cite CVE/GHSA/OSV.

## Live Check

When web fetch is available, spot-check the current CVSS vector names against FIRST and the
CWE Top 25 edition year against cwe.mitre.org.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
