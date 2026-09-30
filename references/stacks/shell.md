# Shell, Batch, And PowerShell Baseline

## Purpose

> **Scope:** Checkable constraints for shell scripts, Windows batch, and PowerShell automation
> **Key items:** ShellCheck rule classes, Google shell style, PSScriptAnalyzer conventions,
> quoting and error-handling review classes

This file distills the ShellCheck wiki, Google Shell Style Guide, and PSScriptAnalyzer sources
listed in `references/source-catalog.md` into constraints an audit can verify from repository
source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/code-quality.md`, and
`assessment/security-review.md` for script-heavy subjects.

## ShellCheck Rule Classes

From https://www.shellcheck.net/wiki/ - rule IDs feed `references/cwe-analyzer.md`.

- Quoting: SC2046/SC2086 (unquoted expansion word-splitting), SC2059 (`printf` with variable
  format strings) - unquoted `$var` in commands is the highest-frequency defect class.
- Safety: SC2115 (`rm -rf "$var/"` empty-var expansion), SC2145 (glob/unquoted mixing),
  SC2181 (`$?` tested after a pipeline instead of `if cmd`).
- Portability: SC2039/SC3010-3037 (`[[`, `local`, arrays in `sh`-declared scripts) - check the
  shebang against the syntax used.
- Input handling: SC2162 (`read` without `-r` mangles backslashes), SC2002 (useless `cat`).
- `# shellcheck disable=SCxxxx` comments are auditable suppressions. Each should carry a
  justification.

## Google Shell Style

From https://google.github.io/styleguide/shellguide.html (CC-BY. Distilled, not copied).

- `#!/bin/bash` for bash features, `#!/bin/sh` only for genuinely portable scripts. `env`-path
  shebangs for user-installed interpreters.
- `set -o errexit -o nounset -o pipefail` (or the `set -euo pipefail` short form) is the
  safety baseline. Scripts without it continue silently past failures.
- `main "$@"` at the end for multi-function scripts. Function names lowercase with
  underscores, constants and environment-derived variables `UPPER_CASE`.
- `$(...)` over backticks. `[[ ]]` over `[ ]` under bash. `readonly`/`declare -r` for
  constants.
- Pipelines default to the last command's exit status. `pipefail` or explicit checks make
  intermediate failures visible.

## PowerShell

From https://github.com/PSScriptAnalyzer (MIT-licensed rule set).

- Approved verbs (`Get-`, `Set-`, `New-`, `Invoke-`...) in function names. Unapproved-verb
  functions are convention findings (PSUseApprovedVerbs).
- `PSAvoidUsingWriteHost` (use `Write-Output`/`Write-Verbose`/`Write-Information`),
  `PSAvoidUsingPlainTextForPassword` (`SecureString`/`PSCredential` parameters),
  `PSUsePSCredentialType`, `PSAvoidUsingInvokeExpression`, `PSAvoidUsingConvertToSecureStringWithPlainText`.
- Error handling: `$ErrorActionPreference = 'Stop'` or per-cmdlet `-ErrorAction`, plus
  `try/catch` around terminating-risk calls.
- Signed-script posture: `Set-ExecutionPolicy` weakening (`Bypass`/`Unrestricted` persisted)
  is a finding. Script signing is evidence of controlled automation.

## Batch And Cross-Cutting

- `.bat`/`.cmd` files lack structured error handling. `if errorlevel` checks and `setlocal`
  scoping are the minimum.
- Secrets on command lines are visible in process lists and logs across every shell: review
  any `-password`, `token`, or key material passed as arguments.
- `curl | sh` install patterns, unchecked `cd` before `rm -rf`, and temp files under
  predictable `/tmp` names are the recurring audit findings.

## Live Check

When web fetch is available, spot-check one SC rule ID against the ShellCheck wiki and one
PS rule name against the PSScriptAnalyzer repository.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
