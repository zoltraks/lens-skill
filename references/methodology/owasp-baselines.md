# OWASP Baselines

## Purpose

> **Scope:** Checkable vocabulary and category anchors from the OWASP flagship documents
> **Key items:** Top 10 and API Top 10 category names, ASVS level structure, LLM Top 10,
> agentic ASI and AST vocabularies, cheat-sheet index, SAMM maturity levels, Secure Headers
> checklist

This file distills the OWASP sources listed in `references/source-catalog.md` into the
classification anchors an audit uses for security findings.

Snapshot date: 2026-10-09.

Feeds `assessment/security-review.md`, `assessment/threat-model.md`, and
`references/cwe-analyzer.md`.

## OWASP Top 10 (2025 Edition)

From https://owasp.org/www-project-top-ten/ and https://owasp.org/Top10/2025/.

| Code | Category                                   |
|------|--------------------------------------------|
| A01  | Broken Access Control                      |
| A02  | Security Misconfiguration                  |
| A03  | Software Supply Chain Failures             |
| A04  | Cryptographic Failures                     |
| A05  | Injection                                  |
| A06  | Insecure Design                            |
| A07  | Authentication Failures                    |
| A08  | Software or Data Integrity Failures        |
| A09  | Security Logging and Alerting Failures     |
| A10  | Mishandling of Exceptional Conditions      |

The 2025 edition expands 2021's Vulnerable and Outdated Components into Software Supply Chain
Failures (A03), folds Server-Side Request Forgery into Broken Access Control (A01), and adds
Mishandling of Exceptional Conditions (A10).

A finding mapped to a Top 10 category is a vocabulary anchor, not a severity claim. CWE numbers
carry the defect class.

## OWASP API Security Top 10 (2023)

From https://owasp.org/API-Security/ and
https://owasp.org/API-Security/editions/2023/en/0x11-t10/.

| Code  | Category                                        |
|-------|-------------------------------------------------|
| API1  | Broken Object Level Authorization               |
| API2  | Broken Authentication                           |
| API3  | Broken Object Property Level Authorization      |
| API4  | Unrestricted Resource Consumption               |
| API5  | Broken Function Level Authorization             |
| API6  | Unrestricted Access to Sensitive Business Flows |
| API7  | Server Side Request Forgery                     |
| API8  | Security Misconfiguration                       |
| API9  | Improper Inventory Management                   |
| API10 | Unsafe Consumption of APIs                      |

API1 (BOLA/IDOR) and API5 (function-level authorization) are the most-checkable classes from
source: every object-scoped route needs an ownership check, and every admin route needs a role
check.

## ASVS Structure

From https://owasp.org/www-project-application-security-verification-standard/ and
https://asvs.dev/.

- ASVS 5.0.0 (May 2025) is the current release: a full reorganization of the 4.x requirement
  set with renumbered chapters. Version-qualified requirement IDs (`v5.0.0-1.2.5`) are the
  checkable anchors; a v4.x ID and a v5.x ID are different requirements even at the same
  ordinal position.
- ASVS levels: L1 opportunistic baseline, L2 for applications with sensitive data, L3 highest
  assurance. The audit records which level and which major version the subject claims.
- ASVS is a requirements catalog, not a score: "meets ASVS L2" means every applicable L2
  requirement is verified, never a sampling claim.

## LLM Top 10 And Other Vocabularies

From https://genai.owasp.org/llm-top-10/.

- The LLM Top 10 anchors AI-subsystem findings: LLM01 prompt injection, LLM02 sensitive
  information disclosure, LLM05 improper output handling, LLM06 excessive agency - use the
  codes for findings against LLM-integrated subjects only.
- OWASP SAMM (https://owaspsamm.org/) maturity levels (0 implicit, 1-3 defined/measured)
  supply the governance-maturity vocabulary.
- The Cheat Sheet Series index (https://cheatsheetseries.owasp.org/) names every sheet.
  stack-specific rules live in the per-stack digests that link them.

## Agentic Vocabularies

From the OWASP GenAI Security Project - the LLM Top 10 portal at
https://owasp.org/www-project-top-10-for-large-language-model-applications/ points at
genai.owasp.org for all current lists.

The OWASP Top 10 for Agentic Applications 2026 (ASI codes) anchors findings against subjects
that build or orchestrate AI agents:

| Code  | Category                             |
|-------|--------------------------------------|
| ASI01 | Agent Goal Hijack                    |
| ASI02 | Tool Misuse and Exploitation         |
| ASI03 | Identity and Privilege Abuse         |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution            |
| ASI06 | Memory and Context Poisoning         |
| ASI07 | Insecure Inter-Agent Communication   |
| ASI08 | Cascading Failures                   |
| ASI09 | Human-Agent Trust Exploitation       |
| ASI10 | Rogue Agents                         |

ASI04 is the supply-chain class for agent ecosystems - poisoned tool registries, mutable
runtime components, and untrusted dynamic loading.

The OWASP Agentic Skills Top 10 (AST10) anchors findings specifically against Agent Skill
subjects - the skill is the behavior layer between the model and its tools:

| Code  | Risk                            | Severity |
|-------|---------------------------------|----------|
| AST01 | Malicious Skills                | Critical |
| AST02 | Supply Chain Compromise         | Critical |
| AST03 | Over-Privileged Skills          | High     |
| AST04 | Insecure Metadata               | High     |
| AST05 | Untrusted External Instructions | High     |
| AST06 | Weak Isolation                  | High     |
| AST07 | Update Drift                    | Medium   |
| AST08 | Poor Scanning                   | Medium   |
| AST09 | No Governance                   | Medium   |
| AST10 | Cross-Platform Reuse            | Medium   |

Each AST risk maps to the CSA MAESTRO 7-layer threat model, and AST02 maps onward to LLM03,
ASVS V14.2, and CWE-494.

Pick the vocabulary that matches the subject: LLM codes for LLM-integrated systems, ASI codes
for agent-orchestrating systems, AST codes for Agent Skill packages themselves.

## Secure Headers

From https://owasp.org/www-project-secure-headers/.

Response-header floor for browser-facing subjects: `Strict-Transport-Security`,
`X-Content-Type-Options: nosniff`, `Content-Security-Policy`, `X-Frame-Options` or CSP
`frame-ancestors`, `Referrer-Policy`, and `Permissions-Policy`. `X-XSS-Protection` is
deprecated and should be absent or `0`.

## Live Check

When web fetch is available, compare the Top 10 category list against the current edition and
note edition drift.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
