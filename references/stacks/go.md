# Go Baseline

## Purpose

> **Scope:** Checkable constraints for Go services, libraries, and CLIs
> **Key items:** module files, version-suffix rules, idiomatic conventions, security tooling,
> CLI structure, crypto primitives

This file distills the Go documentation, module reference, security policy, OWASP Go-SCP, and
tooling sources listed in `references/source-catalog.md` into constraints an audit can verify
from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/dependency-review.md`,
`assessment/security-review.md`, `assessment/api-compatibility.md`, and
`assessment/baseline-conformance.md` for Go subjects.

## Module And Dependency Rules

From https://go.dev/ref/mod, https://go.dev/doc/modules/managing-dependencies, and
https://go.dev/doc/modules/version-numbers.

- `go.mod` declares the module path and Go floor. `go.sum` records content hashes of every
  module and `go.mod` file - both are committed for applications and libraries.
- A missing `go.sum`, or one drifting from `go.mod`, breaks reproducible verification.
  `go mod verify` checks the module cache against `go.sum`.
- Semantic import versioning: a module at v2.0.0 or higher must carry the `/vN` suffix in its
  module path. A `v2.x` tag on a `/v1`-path module is a compatibility defect.
- `replace` directives redirect dependency resolution and bypass the proxy. Each one is a
  reviewable exception, especially `replace` to local paths in published modules.
- `retract` directives mark broken versions. A repo retracting its own releases signals
  maintenance awareness.
- `go` directive version sets language semantics for the module. Toolchains may
  auto-upgrade - check `toolchain` lines for an explicit pin.

## Idiomatic Conventions

From https://go.dev/doc/effective_go and
https://github.com/golang-standards/project-layout (convention, not a standard - treat as
informative).

- Errors are values: functions return `(T, error)`, errors are checked, and
  `fmt.Errorf`/`errors.Is`/`errors.As` wrap chains. Discarding errors with `_` is a finding
  when the error matters.
- Package names are short lowercase single words. `util`, `common`, `misc` grab-bags are a
  design observation.
- Interfaces are defined by the consumer, not exported preemptively from the producer.
- `gofmt`/`goimports` formatting is mechanical. Unformatted source signals missing tooling.
- Exported identifiers carry doc comments starting with the identifier name.
- `internal/` directories enforce compile-time privacy. Code under `internal/` is not
  importable outside the subtree.
- `cmd/<name>/main.go` + library packages is the conventional binary layout.

## Security

From https://go.dev/doc/security/, https://pkg.go.dev/vuln/,
https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck,
https://github.com/OWASP/Go-SCP, and https://github.com/securego/gosec.

- `govulncheck` is the source-aware advisory check: it reports only vulnerabilities whose
  affected symbols are actually reachable, making it stronger evidence than manifest matching.
- `gosec` rule classes feed `references/cwe-analyzer.md`: G101 hardcoded credentials, G102-G106
  binding/crypto/TLS, G201-G203 SQL injection, G204 command execution via `os/exec`, G304 file
  inclusion, G401-G406 weak crypto/TLS settings, G501-G505 deprecated ciphers.
- `crypto/subtle` (https://pkg.go.dev/crypto/subtle) provides `ConstantTimeCompare` for
  secret comparison. `==` on secrets is a timing-side-channel finding.
- `net/http` servers need explicit `ReadTimeout`/`WriteTimeout`/`IdleTimeout`. The zero-value
  server accepts slow-loris-style connections unbounded.
- `html/template` (not `text/template`) is the XSS-safe HTML renderer. `text/template` to HTML
  output is an injection finding.
- `database/sql` queries with `fmt.Sprintf` interpolation instead of placeholders are SQL
  injection findings.
- x/crypto/ssh (https://pkg.go.dev/golang.org/x/crypto/ssh) is the library path for SSH needs.
  shelling out to `ssh`/`scp` binaries is a portability and argument-injection surface.
- CLI secret storage belongs in an OS keychain (for example
  https://github.com/zalando/go-keyring), not plaintext dotfiles.

## CLI Structure

From https://github.com/spf13/cobra and https://clig.dev/.

- Cobra is the conventional command framework: root command plus subcommands, flags via
  `persistent`/`local` scopes, `--help` generated automatically.
- The clig.dev conventions apply: stderr for errors, stdout for output, non-zero exit codes,
  `NO_COLOR` support, stdin where sensible.
- `os.Exit` codes are semantic and documented: usage errors (flag parse failure, missing
  argument) exit `2` under `flag` convention and must not collide with runtime-failure codes.
- Parsing completes before side effects: a `flag.Parse` that runs after a file write makes
  every usage error a partial mutation.
- The full CLI contract lives in `references/topics/cli-contract.md` - this section carries
  the Go-specific shape only.

## Live Check

When web fetch is available, compare the current Go release policy against
https://go.dev/doc/security/ and spot-check one `gosec` rule ID against the source.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
