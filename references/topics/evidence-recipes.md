# Evidence Recipes

## Purpose

> **Scope:** Session-proven mechanical evidence patterns that no external source owns
> **Key items:** dispatch enumeration, stub detection, version coherence, artifact sweeps,
> secret-chain tracing, spec-conformance diffs, NOT RUN ledger convention

This file consolidates evidence-gathering recipes proven across the audit sessions recorded in
`work/improvement/` into reusable checklists.

Snapshot date: 2026-09-30.

No external sources. The recipes are distilled from session evidence.

Feeds `references/census-commands.md` consumers and `process/audit-workflow.md` evidence
phases.

## Dispatch Entry Enumeration

List every entry point the subject exposes before judging coverage.

- HTTP routes, CLI commands, queue consumers, cron/scheduler registrations, file watchers.
- Enumerate from registration sites (route tables, `commander`/`cobra`/argparse wiring,
  decorators), not from README claims.
- Cross-check the enumeration against test files: entries with no test or doc reference are
  coverage gaps. Entries in docs but not in the enumeration are doc drift.

## Stub And Simulated Surface Detection

Recognize verification debt disguised as coverage.

- Test doubles returning fixed values for the system's own contract (a stub of the subject
  itself) do not evidence behavior - flag `mock`, `stub`, `fake`, `simulate`, `dummy`,
  `placeholder`, `TODO` in test and source paths.
- Endpoints returning constant payloads or `NotImplementedError`/`throw new Error("not
  implemented")`/`todo!()`/`panic!("unimplemented")` are stub findings.
- A test asserting the stub's own constant is a circularity finding, not a passing test.

## Version Coherence Census

Reconcile declared floors across every surface.

- `package.json` `engines`, `pyproject.toml` `requires-python`, `go.mod` `go`, Dockerfile
  base images, CI matrix minimums, README claims - all must agree.
- The effective floor is the minimum that lets the code actually run. Record each surface's
  claimed floor and the intersecting minimum.
- Syntax features used in code must be legal at that floor (see
  `references/stacks/python.md` for the PEP-585/604 example. Every stack file has its
  equivalent).

## Tracked Artifact Sweeps

Enumerate committed artifacts that should not exist.

- `node_modules`, `__pycache__`, `target/`, `dist/`, `*.log`, `.env`, `*.pem`, `id_rsa`,
  `.DS_Store`, binary blobs, vendored archives.
- Sweep `git ls-files` against the secret and artifact patterns. Each hit is a finding or a
  recorded `Reported` artifact.
- A `.gitignore` that lists a pattern already committed is a coherence finding - the file
  was committed before the ignore rule.

## Secret Resolution Chain Tracing

Trace every secret reference to its source.

- For each credential-shaped reference (`process.env.X`, `os.environ`, `config.get`,
  `Secret.from`), record where the value originates: env var, file, vault, CI secret store.
- Fallback chains (`env || file || default`) silently weaken the boundary. Each fallback is
  a resolution step in the chain.
- A default literal in the chain (`default "changeme"`) is a finding. A chain terminating
  in a committed file is a finding.
- Record the chain in the finding's evidence, not just the leak site.

## Spec-Conformance Diff

Compare the declared contract to the observed surface.

- For documented APIs/commands/config: enumerate the declared surface (spec, README table,
  `--help` strings) and the implemented surface (handlers, flags, parsers).
- Declared-but-unimplemented is `NOT SPECIFIED` coverage drift. Implemented-but-undeclared
  is undocumented surface. Mismatched names/types are contract findings.
- Diff per artifact class (endpoints, flags, env vars, file paths), never prose-generalize.

## NOT RUN Ledger Convention

Record unexecuted verification explicitly rather than implying coverage.

- A check documented in CI/scripts but not run by the auditor is `NOT RUN` in the evidence
  ledger - never `Reported` without a committed result artifact and never `Verified`
  without execution evidence.
- Ledger rows: `check name | artifact observed | status | justification` - the status values
  are the fixed vocabulary (`Verified`, `Reported`, `NOT RUN`, `NOT SPECIFIED`,
  `INSUFFICIENT INFORMATION`).
- `NOT RUN` never weakens a finding based on positive evidence. It only bounds the
  verification claim.

## Live Check

These recipes are session-derived and not backed by a live source. No live check applies.

The file updates when audit sessions produce new mechanical patterns.
