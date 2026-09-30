# Supply Chain Baseline

## Purpose

> **Scope:** Checkable anchors for supply-chain integrity and advisory conventions
> **Key items:** SLSA levels, OpenSSF Scorecard checks, provenance vocabulary, GHSA/OSV
> advisory format

This file distills the SLSA, OpenSSF Scorecard, GitHub Advisory Database, and OSV sources
listed in `references/source-catalog.md` into constraints an audit can verify from repository
source.

Snapshot date: 2026-09-30.

Feeds `assessment/dependency-review.md`, `assessment/deployment-review.md`, and
`references/topics/project-health.md`.

## SLSA

From https://slsa.dev/spec/v1.2/ (root and v1.0 URLs are folded into this row).

- SLSA build levels: L1 provenance exists, L2 hosted build on a controlled platform, L3
  hardened builders with isolated provenance. Source-track requirements (version control,
  verified history) sit alongside.
- The checkable artifact is the *provenance statement* (in-toto attestation naming builder,
  materials, and outputs). A release without provenance makes no SLSA claim.
- `npm publish --provenance`, GitHub Artifact Attestations, and `slsa-github-generator`
  workflows are the ecosystem-specific emitters - their presence is a supply-chain strength
  signal.

## OpenSSF Scorecard

From https://github.com/ossf/scorecard and
https://github.com/ossf/scorecard/blob/main/docs/checks.md.

- Check names usable as audit vocabulary: `Binary-Artifacts`, `Branch-Protection`,
  `CI-Tests`, `Code-Review`, `Dangerous-Workflow`, `Dependency-Update-Tool`,
  `Fuzzing`, `License`, `Maintained`, `Packaging`, `Pinned-Dependencies`,
  `Security-Policy`, `Signed-Releases`, `Token-Permissions`, `Vulnerabilities`.
- Source-inspectable equivalents the audit can verify without running Scorecard: presence of
  `SECURITY.md`, `LICENSE`, branch-protection settings are NOT source-visible (record
  `NOT RUN` for API-gated checks), pinned CI actions (see
  `references/stacks/ci-github-actions.md`), checked-in binaries, fuzz harness files.
- Scorecard results in a repo's README badge are `Reported` evidence unless the underlying
  artifact is present.

## Advisories

From https://github.com/advisories, https://osv.dev/, and https://osv.dev/docs/.

- Advisory identifiers: `GHSA-xxxx-xxxx-xxxx` (GitHub), `CVE-YYYY-NNNNN`, `OSV` ecosystem
  IDs (`PYSEC-`, `GO-`, `RUSTSEC-`, `GHSA-` aliases). The report cites the ID, never a
  paraphrased severity.
- OSV schema fields: `id`, `summary`, `affected[].package`, `affected[].ranges` (SEMVER/
  ECOSYSTEM/GIT), `affected[].versions`, `references`, `database_specific` - a repo carrying
  its own advisory file follows this shape.
- `npm audit`/`govulncheck`/`cargo audit`/`composer audit` outputs are the ecosystem surfaces.
  a committed scan artifact is `Reported` evidence unless the audit ran it.

## Live Check

When web fetch is available, spot-check the current SLSA version against slsa.dev and one
Scorecard check name against the checks document.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
