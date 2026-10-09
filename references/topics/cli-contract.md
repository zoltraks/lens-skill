# CLI Contract Baseline

## Purpose

> **Scope:** The checkable contract a command-line tool keeps with scripts, agents, and users
> **Key items:** stdout/stderr separation, exit-code taxonomy, discoverability, machine-readable
> output stability, non-interactive behavior, artifact freshness

This file distills the Command Line Interface Guidelines, POSIX utility conventions, and the
NO_COLOR specification listed in `references/source-catalog.md` into constraints an audit can
verify from repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md`, `assessment/best-practices.md`, and
`assessment/api-contract.md` for subjects classified `cli` in `references/domain-profiles.md`.

## Stream Discipline

From https://clig.dev/ and the POSIX utility conventions
(https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html).

- stdout carries the payload only: data, listings, serialized results. Diagnostics, warnings,
  progress, and usage text belong on stderr - a pipe that emits log noise on stdout corrupts
  every consumer.
- Human-readable formatting is the default output. Machine formats (`--json`, `--csv`) are
  explicit options, and the machine schema is a contract: field names and types never change
  silently, and additions are backward-compatible.
- `--verbose` and `--quiet` adjust the diagnostics channel, never the payload. `-q` suppresses
  progress but still reports errors.

## Exit Codes And Argument Handling

- Exit codes are semantic, documented, and stable: `0` success, nonzero failure classes such as
  `1` general error and `2` usage error. A tool that exits `0` on failure is a defect.
- `--help` and `--version` succeed (exit `0`) and work regardless of argument position or
  other flags. `--version` output that embeds the source revision is stronger evidence than a
  bare number.
- Unknown arguments are rejected with a usage error, never silently ignored. Mutually exclusive
  options (for example two output formats) are detected and reported, not resolved by ordering.
- Argument parsing completes before any side effect: a parse-after-mutation structure makes
  every usage error a partial run.
- Mutating commands offer `--dry-run` where feasible, and irreversible actions carry an
  explicit confirmation flag rather than a prompt in non-interactive use.

## Interaction And Environment

From https://clig.dev/ and https://no-color.org/.

- Non-interactive invocation never blocks on a prompt. Scripts and agents must be able to drive
  every command through flags alone (`--yes`, `--force`, explicit values).
- Color and animation disable cleanly: honor `NO_COLOR`, `TERM=dumb`, and non-tty output.
- stdin input is accepted where the tool's role makes it sensible, keeping the tool composable
  in pipelines.
- Signals end cleanly: `SIGINT`/`SIGTERM` produce a bounded shutdown that reports partial
  results or cleans up, not an abandoned half-write.

## Verification And Freshness

- Smoke tests derive invocations from the tool's own `--help` and `--version` output, so a
  renamed flag breaks the test that advertises it.
- Before diagnosing a built artifact's behavior, prove it is fresh: compare the artifact's
  timestamp and embedded revision against the source tree. A stale binary reproduces old
  defects and hides new ones.
- Documented behavior that only exists in the build output (a help string, a completion
  script) is contract evidence - divergence between docs and `--help` text is a finding.

## Live Check

When web fetch is available, spot-check one convention against https://clig.dev/ and one
exit-code convention against the POSIX utility guidelines.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
