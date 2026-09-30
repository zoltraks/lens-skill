# OWASP Baselines

## Purpose

> **Scope:** Checkable vocabulary and category anchors from the OWASP flagship documents
> **Key items:** Top 10 and API Top 10 category names, ASVS level structure, LLM Top 10,
> cheat-sheet index, SAMM maturity levels, Secure Headers checklist

This file distills the OWASP sources listed in `references/source-catalog.md` into the
classification anchors an audit uses for security findings.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md`, `assessment/threat-model.md`, and
`references/cwe-analyzer.md`.

## OWASP Top 10 (2021 Edition)

From https://owasp.org/www-project-top-ten/.

| Code | Category                                   |
|------|--------------------------------------------|
| A01  | Broken Access Control                      |
| A02  | Cryptographic Failures                     |
| A03  | Injection                                  |
| A04  | Insecure Design                            |
| A05  | Security Misconfiguration                  |
| A06  | Vulnerable and Outdated Components         |
| A07  | Identification and Authentication Failures |
| A08  | Software and Data Integrity Failures       |
| A09  | Security Logging and Monitoring Failures   |
| A10  | Server-Side Request Forgery                |

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

From https://owasp.org/www-project-application-security-verification-standard/.

- ASVS levels: L1 opportunistic baseline, L2 for applications with sensitive data, L3 highest
  assurance. The audit records which level the subject claims.
- Requirements are organized by verification area (V1 architecture through V14 configuration
  in the 4.x/5.x stream). Individual requirement IDs (`V2.x.y`) are the checkable anchors.
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
