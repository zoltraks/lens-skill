# Language Conventions

## Purpose

> **Scope:** Canonical style yardsticks per programming ecosystem for the code-style
> assessment
> **Key items:** casing conventions, unit granularity, naming temperament, primary
> authorities, snapshot date, fallback rule

This reference records the canonical naming and style convention of each supported
ecosystem as a dated snapshot, supplying the T3 yardstick for `assessment/code-style.md`.

Apply `principles/evaluation-rules.md` throughout.

Snapshot date: 2026-10-27.

For the eleven stacks covered by `references/naming-and-layout.md`, that file's per-element
matrices and code-division rules remain the authority, and this file adds temperament and
style-family notes.

For every other ecosystem this file is the yardstick.

## Yardstick Table

| Ecosystem            | Casing (types / functions / vars / constants)                                                                                     | Unit granularity                                               | Temperament and notable rules                                                                                                                              | Primary authority                                                           |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Java                 | `PascalCase` / `camelCase` / `camelCase` / `UPPER_SNAKE`                                                                          | One public top-level type per file, file = type                | Long descriptive names, no `I` prefix on interfaces                                                                                                        | Google Java Style, Oracle conventions, *Effective Java*                     |
| Kotlin               | As Java                                                                                                                           | Several declarations per file allowed                          | Descriptive but concise                                                                                                                                    | Kotlin coding conventions                                                   |
| C#                   | `PascalCase` types, methods, properties, constants / `camelCase` locals, params                                                   | One type per file common, namespace mirrors folders            | `I` prefix and `Async` suffix are idiomatic, private fields commonly `_camelCase`, descriptive                                                             | .NET design guidelines, C# coding conventions, `.editorconfig` naming rules |
| Rust                 | `UpperCamelCase` types, traits, variants / `snake_case` fns, vars, modules                                                        | Module = file, many types per file normal                      | Short idiomatic names accepted (`cfg`, `buf`, `ctx`), no `I` prefix, getters without `get_`, `as_`/`to_`/`into_` conversions                               | Rust API Guidelines, Rust Style Guide, rustc lints                          |
| Go                   | `MixedCaps`, exported capitalized, initialisms all-caps (`ID`, `URL`)                                                             | Package = directory, many types per file, `_test.go`           | Short receivers and locals, short lowercase package names without underscores, avoid stutter, no `Get` prefix, interfaces `-er`                            | Effective Go, Code Review Comments, Google Go style, `gofmt`                |
| Python               | `PascalCase` classes / `snake_case` / `snake_case` / `UPPER_SNAKE`                                                                | Module = file, many classes fine                               | `_` prefix non-public, exceptions end `Error`, medium length                                                                                               | PEP 8, PEP 257                                                              |
| JavaScript           | `PascalCase` classes / `camelCase` / `camelCase` / `UPPER_SNAKE`                                                                  | `kebab-case` files typical, one component per file             | `#privateField` native, framework file naming varies                                                                                                       | Project ESLint or Prettier config, framework guides                         |
| TypeScript           | `PascalCase` classes, types, components / `camelCase` / `camelCase` / `UPPER_SNAKE` or `camelCase`                                | `kebab-case` versus `PascalCase` files, one component per file | `I` prefix on interfaces mostly discouraged but common in legacy - detect, do not assume                                                                   | Google TS style, framework guides, project config                           |
| PHP                  | `StudlyCaps` classes / `camelCase` methods / `UPPER_SNAKE` constants                                                              | One class per file, file = class, namespace mirrors dirs       | Descriptive                                                                                                                                                | PSR-1, PSR-12, PSR-4                                                        |
| C                    | `snake_case`, macros and constants `UPPER_SNAKE`, module prefix for namespacing                                                   | Translation unit plus header pair                              | Short locals, descriptive exports, `_t` suffix and leading or double underscore reserved                                                                   | Linux kernel style or the project's own, MISRA C where adopted              |
| C++                  | Family-dependent: Google `PascalCase`/`snake_case`/`kConst`, std `snake_case`, Qt `camelCase`/`Q`, Unreal `T`/`F`/`U`/`A`/`E`/`I` | Header and implementation pair, one primary class per header   | Detect the family. Mixing families inside one partition is the defect                                                                                      | C++ Core Guidelines NL, Google C++, LLVM                                    |
| Pascal (Delphi, FPC) | `T` types, `I` interfaces, `E` exceptions / `PascalCase` / `camelCase` / `osX`                                                    | Unit file with `interface`/`implementation` sections           | `F` field and `A` parameter prefixes, unit name = file name                                                                                                | Object Pascal Style Guide, Free Pascal reference                            |
| Zig                  | `TitleCase` types / `camelCase` functions / `snake_case` vars, constants                                                          | File may be a struct (`TitleCase` file) else `snake_case`      | Short                                                                                                                                                      | Zig style guide                                                             |
| Swift                | `UpperCamelCase` types / `lowerCamelCase` rest                                                                                    | Several types per file fine                                    | Clarity at point of use, omit needless words, argument labels                                                                                              | Swift API Design Guidelines                                                 |
| Ruby                 | `CamelCase` classes / `snake_case`, `?` predicates, `!` mutators                                                                  | File per class common                                          |                                                                                                                                                            | Community style, RuboCop                                                    |
| Shell                | `snake_case` functions and vars, `UPPER` for exported and constants                                                               |                                                                |                                                                                                                                                            | Google Shell Style                                                          |
| SQL                  | `snake_case`, consistent singular or plural tables, `id`/`<table>_id` keys                                                        |                                                                | Either plural or singular is fine, consistency decides, no reserved words                                                                                  | Project convention                                                          |
| Assembly             | Dialect labels, local-label syntax, consistent mnemonic case, `UPPER` equates                                                     | File per module or segment                                     | Terse names are idiomatic. Readability levers are routine contracts (inputs, outputs, clobbered registers, cycles), named constants, documented memory map | Assembler manual (ca65, DASM, sjasmplus), project convention                |

Also record initialism rules where they differ: Go all-caps (`ID`, `URL`), .NET two-letter
caps with longer acronyms as Pascal words (`IO`, `Html`), and Java or Google style treating
acronyms as words (`Http`).

## Temperament Notes

- **Short-name ecosystems** (Rust, Go, C, small scopes anywhere): `cfg`, `ctx`, `buf`, `i`,
  `err`, `s` receivers are canonical, and judging them as noise names is a false positive.
- **Prefix-idiomatic ecosystems**: C# `I`/`Async`, Delphi `T`/`F`/`A`/`E`, Unreal letter
  prefixes are mandated by the stack, while the same prefixes in TS, Java, or Python are
  foreign holdovers unless a T1 rule declares them.
- **Terse ecosystems** (assembly, shell): readability evidence is contracts, equates, and
  memory-map documentation, not name length.
- **Granularity**: one-type-per-file is a Java, C#, PHP, and Delphi-family expectation, never
  a Rust, Go, Python, Zig, or C expectation.
- **Framework-mandated names** (`Service`, `Controller`, `Repository`, `*Endpoints`) are
  judged by cohesion of responsibility, not by the presence of the word.
- **Full-word ecosystems** (C#, and the maintainer's C# and Java standards): a word the
  ecosystem habitually shortens is still written in full - `Configuration` not `Conf`,
  `Specification` not `Spec`, `Arguments` not `Args` - in file, type, and project names,
  while canonical idioms (`args` locals) stay.
- **Initialism casing is ecosystem-fixed**: Go all-caps (`HTTPClient`, `urlParser`
  unexported), .NET two-letter caps with longer acronyms as Pascal words, Java treating
  acronyms as words - mixing conventions inside one partition is the finding.

## Fallback For Unlisted Ecosystems

For a language not listed, resolve the yardstick by T1, then T2 dominance, then the T4
readability lenses in `assessment/code-style.md`, and record that no T3 baseline applied.

## Authorities

Verify each row against the official guide when refreshing this snapshot and record the new
snapshot date: Google Java Style Guide, Oracle Code Conventions, *Effective Java*, Kotlin
Coding Conventions, .NET Framework Design Guidelines, C# Coding Conventions, Rust API
Guidelines, Rust Style Guide, Effective Go, Go Code Review Comments, Google Go Style Guide,
PEP 8, PEP 257, Google TypeScript Style Guide, PSR-1, PSR-12, PSR-4, Linux Kernel Coding
Style, MISRA C, C++ Core Guidelines section NL, Google C++ Style Guide, LLVM Coding
Standards, Object Pascal Style Guide, Free Pascal Reference, Zig Style Guide, Swift API
Design Guidelines, RuboCop Ruby Style Guide, Google Shell Style Guide, and the target
assembler's manual (ca65, DASM, sjasmplus, or equivalent).
