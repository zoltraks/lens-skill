# CWE To Analyzer Rule Map

## Purpose

> **Scope:** Cross-reference between CWE identifiers and ecosystem-specific static analyzer rules
> **Key items:** rule IDs per stack, enablement evidence, "not yet enabled" reporting

This file maps CWE identifiers to the static-analysis rules that check for the matching code
pattern in each ecosystem. It is a documentation lookup, not execution: the audit never runs an
analyzer. The map turns a CWE-tagged finding into a concrete, verifiable follow-up action.

Apply `principles/evaluation-rules.md` throughout.

## How To Apply

- For every security finding that carries a CWE classification, look up the CWE in the matching
  stack subsection below.
- When a rule exists, close the finding's classification with the equivalent automated check and
  its enablement state, for example: "The equivalent automated check is `CA5359`, not yet
  enabled."
- Determine enablement from evidence, not assumption. Check the enablement sources listed below
  before writing "not yet enabled". When evidence exists, name it, for example ".editorconfig
  sets `dotnet_diagnostic.CA5359.severity = warning`".
- When no row or rule exists, state it plainly: "No direct analyzer rule exists for CWE-319 in
  this stack." Do not stretch a related rule into coverage it does not claim.
- Mappings are approximate. A rule covers the patterns its own documentation describes, which is
  often a subset of the CWE. State the rule's documented scope when it differs from the CWE.
- Analyzer rules complement, never replace, manual review evidence.

## C# / .NET

Roslyn security rules ship in `Microsoft.CodeAnalysis.NetAnalyzers` and are documented under
[.NET security warnings](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/security-warnings).
Most are disabled by default and require `.editorconfig` or `AnalysisLevel` configuration.

| CWE     | Weakness                                 | Analyzer Rules                                                        |
|---------|------------------------------------------|-----------------------------------------------------------------------|
| CWE-89  | SQL injection                            | `CA2100`, `CA3001`                                                    |
| CWE-79  | Cross-site scripting                     | `CA3002`                                                              |
| CWE-22  | Path traversal / file path injection     | `CA3003`                                                              |
| CWE-611 | XML injection / XXE                      | `CA3009`, `CA3075`, `CA5369`                                          |
| CWE-78  | Process command injection                | `CA3006`                                                              |
| CWE-601 | Open redirect                            | `CA3007`                                                              |
| CWE-502 | Insecure deserialization                 | `CA2300`–`CA2302`, `CA2321`–`CA2335`, `CA5360`, `CA5369`              |
| CWE-327 | Broken or risky cryptographic algorithms | `CA5350` (weak), `CA5351` (broken), `CA5358` (cipher mode)            |
| CWE-295 | Certificate validation disabled          | `CA5359`                                                              |
| CWE-326 | Weak key or TLS protocol version         | `CA5397`, `CA5398`                                                    |
| CWE-338 | Insecure randomness                      | `CA5394`                                                              |
| CWE-352 | Missing antiforgery token                | `CA5391`                                                              |
| CWE-319 | Cleartext transmission                   | None direct                                                           |
| CWE-798 | Hardcoded credentials                    | None direct in NetAnalyzers, third-party Security Code Scan `SCS0015` |
| CWE-400 | Decompression / resource exhaustion      | None direct                                                           |

## Go

Every [gosec](https://github.com/securego/gosec/blob/master/RULES.md) rule carries CWE metadata.
The rules below are the ones relevant to common audit findings.

| CWE     | Weakness                              | gosec Rules                    |
|---------|---------------------------------------|--------------------------------|
| CWE-89  | SQL injection                         | `G201`, `G202`                 |
| CWE-79  | Unescaped HTML template output        | `G203`                         |
| CWE-78  | Command injection                     | `G204`                         |
| CWE-22  | Path traversal                        | `G111`, `G304`, `G305`         |
| CWE-295 | TLS certificate verification skipped  | `G402`                         |
| CWE-327 | Blocklisted crypto imports, DES/RC4   | `G405`, `G501`–`G507`          |
| CWE-328 | Weak hash (MD5, SHA1, MD4, RIPEMD160) | `G401`, `G406`                 |
| CWE-330 | Insecure random source                | `G404`                         |
| CWE-409 | Decompression bomb via `io.Copy`      | `G110`                         |
| CWE-798 | Hardcoded credentials                 | `G101`                         |
| CWE-200 | Information exposure                  | `G102`, `G108`, `G117`         |
| CWE-242 | Use of `unsafe`                       | `G103`                         |
| CWE-190 | Integer overflow on conversion        | `G109`, `G115`                 |
| CWE-400 | Missing timeouts / slowloris          | `G112`, `G114`, `G118`, `G120` |
| CWE-88  | SSRF via tainted URL                  | `G107`                         |
| CWE-367 | Race in file permission check         | `G122`                         |

## Java / JVM

[FindSecBugs](https://find-sec-bugs.github.io/bugs.htm) is the SpotBugs plugin for security
patterns and covers Java, Kotlin, Scala, and Groovy bytecode. Core SpotBugs also ships a few
relevant detectors.

| CWE     | Weakness                          | FindSecBugs Patterns                                                         |
|---------|-----------------------------------|------------------------------------------------------------------------------|
| CWE-89  | SQL injection                     | `SQL_INJECTION*` family, SpotBugs `SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE` |
| CWE-79  | Cross-site scripting              | `XSS_*` family                                                               |
| CWE-78  | Command injection                 | `COMMAND_INJECTION`                                                          |
| CWE-22  | Path traversal                    | `PATH_TRAVERSAL_IN`, `PATH_TRAVERSAL_OUT`                                    |
| CWE-295 | Trust-all certificate or hostname | `WEAK_TRUST_MANAGER`, `WEAK_HOSTNAME_VERIFIER`                               |
| CWE-327 | Weak message digest or cipher     | `WEAK_MESSAGE_DIGEST_MD5`, `WEAK_MESSAGE_DIGEST_SHA1`, `DES_USAGE`           |
| CWE-330 | Predictable random                | `PREDICTABLE_RANDOM`                                                         |
| CWE-502 | Deserialization gadget            | `OBJECT_DESERIALIZATION`, `DESERIALIZATION_GADGET`                           |
| CWE-611 | XXE                               | `XXE_*` family                                                               |
| CWE-798 | Hardcoded password or key         | `HARDCODED_PASSWORD*` family                                                 |
| CWE-601 | Unvalidated redirect              | `UNVALIDATED_REDIRECT`                                                       |

## JavaScript / TypeScript

The main rule source is
[`eslint-plugin-security`](https://github.com/eslint-community/eslint-plugin-security). The
`eslint-plugin-no-unsanitized` plugin covers DOM XSS sinks.

| CWE      | Weakness                            | ESLint Rules                                     |
|----------|-------------------------------------|--------------------------------------------------|
| CWE-95   | `eval` with expression              | `security/detect-eval-with-expression`           |
| CWE-78   | Child process with variable         | `security/detect-child-process`                  |
| CWE-22   | Non-literal filesystem path         | `security/detect-non-literal-fs-filename`        |
| CWE-94   | Dynamic property access injection   | `security/detect-object-injection`               |
| CWE-90   | Non-literal `RegExp`                | `security/detect-non-literal-regexp`             |
| CWE-1333 | Inefficient regex (ReDoS)           | `security/detect-unsafe-regex`                   |
| CWE-338  | `crypto.pseudoRandomBytes`          | `security/detect-pseudoRandomBytes`              |
| CWE-352  | Missing CSRF before method override | `security/detect-no-csrf-before-method-override` |
| CWE-208  | Possible timing attack              | `security/detect-possible-timing-attacks`        |
| CWE-79   | DOM XSS                             | `no-unsanitized/*` plugin rules                  |
| CWE-327  | Weak cryptography                   | None direct                                      |
| CWE-295  | Certificate validation disabled     | None direct                                      |

## Python

[Bandit](https://bandit.readthedocs.io/) test IDs carry CWE metadata.

| CWE     | Weakness                               | Bandit Tests                                          |
|---------|----------------------------------------|-------------------------------------------------------|
| CWE-78  | Shell / subprocess injection           | `B601`–`B607`                                         |
| CWE-89  | Hardcoded SQL expressions              | `B608`                                                |
| CWE-502 | Insecure deserialization               | `B301` (pickle), `B506` (yaml.load)                   |
| CWE-295 | Certificate / host-key verification    | `B501`, `B507`                                        |
| CWE-327 | Weak hash, cipher, or TLS version      | `B303`, `B304`, `B305`, `B324`, `B413`, `B502`–`B504` |
| CWE-326 | Weak cryptographic key                 | `B505`                                                |
| CWE-330 | Standard pseudo-random in security use | `B311`                                                |
| CWE-377 | Insecure temp file                     | `B306`                                                |
| CWE-22  | Unsafe archive extraction              | `B202`                                                |
| CWE-798 | Hardcoded password                     | `B105`–`B107`                                         |
| CWE-611 | XML attacks                            | `B313`–`B320`                                         |

## Rust

There is no CWE-mapped lint set for security patterns. Clippy covers correctness and style, not
vulnerability classes. Adjacent tooling addresses different scopes.

| CWE class             | Closest Mechanism                                                    |
|-----------------------|----------------------------------------------------------------------|
| Memory safety, UB     | `#![forbid(unsafe_code)]`, `cargo-geiger` unsafe census, Miri for UB |
| Known vulnerabilities | `cargo audit` against [RustSec](https://rustsec.org/) advisories     |
| Supply-chain policy   | `cargo deny` license and advisory checks                             |
| Other CWEs (CWE-327…) | None direct, assess manually                                         |

## C / C++

Rule IDs are tool-specific rather than ecosystem-standard.

| Tool                | Mapping Approach                                               |
|---------------------|----------------------------------------------------------------|
| clang-tidy `cert-*` | Named after CERT rules, each CERT rule maps to a CWE           |
| MSVC `/analyze`     | `C26xxx`, `C60xx`, `C28xxx` warning families                   |
| cppcheck            | Named checks such as `arrayIndexOutOfBounds`, no CWE-keyed IDs |

For a C or C++ finding, name the concrete tool check that would catch it when one is known.
Otherwise record "no direct analyzer rule" and cite the relevant CERT rule instead.

## Multi-Language

[Semgrep](https://semgrep.dev/) registry rules carry `metadata.cwe`. When a finding's CWE has no
stack-specific rule, a Semgrep rule may exist. Cite the rule path from the registry when one is
identified, and mark the mapping `Reported` from registry metadata.

## Enablement Evidence

Before writing "not yet enabled", check the sources where the rule would be configured.

| Stack   | Enablement Evidence                                                                                                                                                                  |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| .NET    | `.editorconfig` `dotnet_diagnostic.CAxxxx.severity`, `*.ruleset`, `AnalysisLevel`/`AnalysisMode` properties, `Microsoft.CodeAnalysis.NetAnalyzers` package reference, CI build steps |
| Go      | `gosec` flags or config in CI, `.gosec.json`, Makefile targets                                                                                                                       |
| Java    | SpotBugs include/exclude filter files, `findsecbugs-plugin` in `pom.xml` or `build.gradle`, CI steps                                                                                 |
| JS / TS | `eslint.config.*` or `.eslintrc*` plugin list, CI lint steps                                                                                                                         |
| Python  | `bandit` config (`.bandit`, `pyproject.toml [tool.bandit]`), CI steps                                                                                                                |
| Rust    | `deny.toml`, CI steps invoking `cargo audit`/`cargo deny`, Clippy config                                                                                                             |
| C / C++ | `clang-tidy` config (`.clang-tidy`), `CMAKE_CXX_CLANG_TIDY`, CI steps                                                                                                                |

"Not yet enabled" means no evidence of enablement was found in these sources, and the audit says
that, rather than asserting the rule is off.
