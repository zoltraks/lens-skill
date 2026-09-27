# Security Policy

## Purpose

> **Scope:** How to report vulnerabilities in the Lens skill and what to expect
> **Key items:** private reporting, covered risks, supported versions, response expectations

Lens is a routed instruction set: its Markdown content becomes agent instructions, so content
integrity issues are security issues.

## Reporting A Vulnerability

Report vulnerabilities privately through GitHub Security Advisories:

- Open a draft advisory at `https://github.com/zoltraks/lens-skill/security/advisories/new`.
- Describe the issue, the affected files or scripts, and a reproduction path.
- Do not file public issues for unresolved vulnerabilities.

## Covered Risks

Reports are welcome for:

- The skill-update path: `scripts/check-update.py` and the `Skill Update Check` flow in
  `SKILL.md`, including tag-integrity and upstream-divergence handling.
- Skill content that could produce unsafe or misleading audit instructions.
- Script behavior that writes files, mutates repositories, or executes commands outside its
  documented contract.

## Supported Versions

The current release line declared in `SKILL.md` `metadata.version` receives fixes.

Older releases are not maintained - update to the latest tag before reporting.

## What To Expect

- The maintainer acknowledges reports as time allows and coordinates a fix before disclosure.
- There is no formal response-time guarantee.
- Accepted fixes land on `main` and ship in the next versioned release.
