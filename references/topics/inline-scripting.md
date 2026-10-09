# Inline And Glue Scripting Baseline

## Purpose

> **Scope:** Checkable constraints for small glue scripts and shell-embedded code shipped inside
> a repository: batch files, PowerShell helpers, Python one-liners and scripts
> **Key items:** host discovery, quoting and encoding, stream and exit-code discipline,
> scratch conventions, secrets hygiene

This file distills the Microsoft cmd and PowerShell documentation, the Python command-line
documentation, and the SS64 command reference listed in `references/source-catalog.md` into
constraints an audit can verify from repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md` and `assessment/best-practices.md` for subjects
whose repositories ship `.bat`, `.cmd`, `.ps1`, or embedded script invocations.

## Batch Files

From https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd and
https://ss64.com/nt/.

- `@ECHO OFF` is the first line and `SETLOCAL`/`ENDLOCAL` bracket the script - state leaked
  into the caller's session is a defect.
- Exit codes are checked after every external call: `CALL`ed scripts need an explicit
  `IF ERRORLEVEL` check, and the script exits with a meaningful code itself. Chained
  `&&`/`||` on external commands is the failure-class boundary, not decoration.
- Paths are quoted everywhere (`"%~dp0..."` for self-location). `%~dp0` resolves to the
  script's directory so the script works from any working directory.
- `REM`, not `::`, inside parenthesized blocks - a `::` label inside a block can abort the
  whole construct.
- Batch is an orchestration layer, not an implementation language: string math, JSON
  construction, and parsing belong in a real script the batch file invokes.

## PowerShell

From https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/.

- Two hosts coexist and differ: Windows PowerShell 5.1 uses Windows-1252 defaults while
  PowerShell 7+ defaults to UTF-8 (no BOM). A file that emits non-ASCII or is consumed by
  another tool must pin its encoding explicitly.
- The output stream is the return value: any stray `Write-Output`, unswallowed cmdlet return,
  or `Write-Host` on the wrong path pollutes whatever a caller captures. Diagnostics go to
  `Write-Verbose`/`Write-Warning`/`Write-Error`, and `-Verbose` exposes them deliberately.
- `$LASTEXITCODE` reflects only the last native command - check it immediately, because any
  cmdlet in between destroys the value.
- `try/catch` needs `-ErrorAction Stop` on the cmdlet to fire - a default `Continue` swallows
  the failure the catch was written for.
- Machine-readable output pins `-Delimiter`/`-Format`/`InvariantCulture` so the contract
  survives culture and profile differences.
- Shipped invocation form for a script executed by tooling: `powershell -NoProfile
  -ExecutionPolicy Bypass -File`. The execution policy is a convenience gate, not a security
  boundary, and is never the relied-on control.

## Python Glue

From https://docs.python.org/3/using/cmdline.html.

- A real interpreter is verified before use: `python --version` can silently resolve to the
  Windows store stub, and `py -3` is the launcher on Windows.
- `python -c` suits one statement - anything multi-line or non-trivial belongs in a file or a
  here-string, never a `-c` string grown past its quoting budget.
- `sys.exit(n)` is the failure contract: probes exit nonzero on failure and print evidence to
  stdout while diagnostics go to stderr.
- Unicode and encoding are pinned explicitly (`sys.stdout.reconfigure(encoding="utf-8")` or
  file output) when the payload contains non-ASCII - console codepages silently corrupt it.

## Cross-Platform Embedding

- Source never passes through a foreign shell's double quotes: a `.bat` heredoc or a `python
  -c` inside cmd quoting corrupts quotes and escapes. Single-quoted heredocs or temp files are
  the safe carriers.
- Scratch files use a consistent convention (`.tmp.` prefix or a declared scratch directory)
  so cleanup is mechanical and inventory is greppable.
- Credentials and secrets never appear in script source - the environment or a secret store
  supplies them.
- An inline block that grows past a handful of statements earns its own checked-in file
  instead of accumulating as an unmaintainable string.

## Live Check

When web fetch is available, spot-check one invocation convention against the PowerShell or
Python command-line documentation.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
