# Git And Update Integrity Baseline

## Purpose

> **Scope:** Checkable anchors for commit signing, release provenance, and update-path
> integrity
> **Key items:** signing mechanics, Sigstore keyless model, TUF roles, hash-pinning rule,
> unsigned-update finding class (CWE-494)

This file distills the Git signing chapter, Sigstore, and TUF sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-10-02.

Feeds `assessment/deployment-review.md`, `references/topics/project-health.md`, and the
integrity portions of desktop/release subjects.

## Commit Signing

From https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work.

- `git commit -S`/`tag -s` signs with the configured key. `commit.gpgsign=true` makes it
  habitual. `user.signingkey`/`user.email` binds the signature to an identity.
- Verification (`git verify-tag`, `git log --show-signature`) requires the signer's public
  key - source-only audit records whether signing infrastructure is *configured*, not whether
  signatures verify.
- SSH-based signing (`gpg.format=ssh`, `user.signingkey` to an SSH key, allowed-signers file)
  is the low-friction path since Git 2.34. An `allowed_signers` file in-repo is evidence of
  the intent.

## Sigstore

From https://docs.sigstore.dev/.

- Keyless signing (gitsign, cosign, `npm publish --provenance`) uses OIDC identity + a
  certificate from Fulcio + a Rekor transparency log. No long-lived key material.
- Checkable surface: `cosign`/`gitsign` config or references in CI, `provenance` flags in
  publish steps, `rekor`/`fulcio` mentions in release workflows.
- A repo signing releases but not commits is a consistent state. Claims of signed history
  require per-commit or per-tag evidence.

## TUF And Update Paths

From https://theupdateframework.io/.

- TUF separates roles: root, targets, snapshot, timestamp - each signs its own metadata so a
  compromised role alone can't ship a malicious update.
- For update systems the checkable shape is: signed metadata served from a separate channel
  than payloads, hash verification on download, rollback protection via version monotonicity.
- CWE-494 (download of code without integrity check) anchors the finding class for
  unsigned-update paths: `curl | sh`, unverified binary downloads in installers/CI,
  `autoUpdater` without signature checks, `pip install` of unpinned packages.
- A repo's own updater script that downloads and executes without a signature/hash check is
  a finding, not a missing feature.

## Hash Pinning

From https://shattered.io/.

- SHAttered (2017, CWI Amsterdam + Google) produced the first practical SHA-1 collision: two
  distinct PDFs sharing `38762cf7f55934b34d179ae6a4c80cadccbb7f0a`, at ~9 quintillion SHA-1
  computations (~6,500 CPU-years + 110 GPU-years).
- The follow-on "SHA-1 is a Shambles" chosen-prefix work (2020) cut the cost to roughly $45k;
  NIST formally retired SHA-1 in December 2022 with a 2030 phase-out deadline, and Git added
  collision detection.
- Checkable rule: an update path that pins or merges by an abbreviated hash (short prefix,
  `%h` output) is a weaker integrity pin than the full object name - audit evidence should name
  the full-length pin (`%H`) the merge actually targets.
- A fetch-and-merge update path that never compares the remote tip against a recorded pin
  anchors the CWE-494 finding class alongside unsigned-download cases.

## Live Check

When web fetch is available, spot-check one signing flag against git-scm.com and one TUF role
name against theupdateframework.io.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
