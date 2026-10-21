# Code Style

## Purpose

> **Scope:** In-code identifier naming, style consistency, naming quality, and readability of
> source code
> **Key items:** convention-tier resolution, dominance censuses, consistency-versus-correctness
> matrix, ecosystem anti-patterns, naming-quality heuristics, craft notes, remediation ladder

This file guides assessment of whether source code follows a coherent convention and whether
its names and structure are readable to a programmer.

Apply `principles/evaluation-rules.md` throughout.

This assessment is mandatory for `audit` and `review` reports on code-bearing subjects and
never loads under `Report Style: hunt`.

A subject with no source code marks the category `N/A` and records the omission in Scope
Exclusions.

## Contents

| Section                          | Line | What it covers                                 |
|----------------------------------|------|------------------------------------------------|
| Boundary                         | 41   | Owned versus delegated concerns                |
| Convention Resolution            | 58   | Tier ordering and the winning-yardstick rule   |
| Consistency And Correctness      | 83   | Status matrix for shape and idiom combinations |
| Ecosystem Anti-Patterns          | 113  | Cross-language style smells                    |
| Assessment Procedure             | 130  | Step-by-step pass order                        |
| What To Evaluate: Lenses         | 170  | SL-1 through SL-8 lens definitions             |
| Naming-Quality Heuristics (SL-3) | 186  | Semantic naming smells and evidence rules      |
| Evidence And Ledger Conventions  | 220  | EVD row requirements and census anchoring      |
| Severity And Confidence          | 231  | Severity guide and naming-confidence cap       |
| Scoring And Dimension            | 253  | Code Style scorecard dimension feeding         |
| Status Criteria                  | 266  | PASS through FAIL verdict definitions          |
| Common Risks                     | 277  | Typical failure modes                          |
| What Raises Confidence           | 288  | Positive evidence signals                      |
| Remediation Ladder               | 300  | Escalation order for style fixes               |
| Craft Notes                      | 317  | Suggestion handling outside findings           |

## Boundary

This assessment owns in-code identifier naming, naming quality, style consistency, and
readability.

| Out of scope                                            | See instead                           |
|---------------------------------------------------------|---------------------------------------|
| Directory layout, file naming, code division, artifacts | `assessment/structure-review.md`      |
| Type safety, lint enforcement, complexity, dead code    | `assessment/code-quality.md`          |
| Runtime idioms and framework pattern correctness        | `assessment/best-practices.md`        |
| Conformance to the project's own documented standards   | `assessment/standards-conformance.md` |
| Directory/namespace mirroring and file-to-type mapping  | `references/naming-and-layout.md`     |

Standards discovered by `assessment/standards-conformance.md` feed this assessment as tier-1
conventions, and formatter or linter enforcement stays a code-quality signal - this file
consumes the configured rules as evidence, never runs the tools.

## Convention Resolution

Resolve the yardstick per language partition - a language and layer pair such as
"`src/` TypeScript" or "`crates/core` Rust" - in this order, and record the winning tier on
every style finding's `Basis` field:

| Tier | Source    | How detected                                                                                                                                                                                                                                                                                                                                                                      |
|------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T1   | Declared  | `STYLE*`, `CONTRIBUTING`, `docs/standard/`, `.editorconfig` naming rules, `.clang-format`, `.clang-tidy`, `rustfmt.toml`, `clippy.toml`, ESLint or Prettier config, `checkstyle` or `pmd`, StyleCop or `.globalconfig`, `pyproject.toml` ruff or black or pylint, `.golangci.yml`, `.rubocop.yml`, `phpcs.xml` or `.php-cs-fixer.php`, `.shellcheckrc`, `.pre-commit-config.yaml` |
| T2   | Observed  | Dominant convention in the code itself, measured by the identifier-shape census                                                                                                                                                                                                                                                                                                   |
| T3   | Ecosystem | Canonical guide for the language or framework in `references/language-conventions.md`, extended by the naming sections of the matching `references/stacks/` digest                                                                                                                                                                                                                |
| T4   | Principle | Language-agnostic readability lenses below                                                                                                                                                                                                                                                                                                                                        |

- T1 wins when present and consistent, and code deviating from T1 is drift.
- When T1 is absent, T2 is the working yardstick once one shape meets `DOMINANCE_PARTIAL`, and
  T3 then judges only whether the dominant style is idiomatic - an Observation, not a defect.
- When T1 and T2 are both absent or split, T3 decides what to recommend.
- When neither the language-conventions yardstick nor a stack digest covers the partition's
  ecosystem, resolve T3 by research: consult the official language style guide or framework
  naming documentation, cite the consulted URL in the report's References, and record an
  unreachable source in Limitations and Unknowns rather than claiming it was read.
- T4 applies to name quality regardless of the casing convention.
- A deliberate deviation from T3 is legitimate when documented under T1 or technically forced,
  and it records as an Observation, never a defect.

## Consistency And Correctness

Consistency and correctness are separate axes: a consistent but misleading scheme is a
naming-quality problem, and an inconsistent but well-named codebase is a consistency problem.

Named thresholds, tuned as constants here:

- `DOMINANCE_PASS` - 90% dominant shape share.
- `DOMINANCE_PARTIAL` - 75% dominant shape share.
- `MIN_PARTITION_SHARE` - a partition below 5% of source lines and 5 files gets a one-line
  note, not a profile.
- `SAMPLE` - the semantic sample holds at most 25 files or 10% of source files, whichever is
  smaller.
- `NAMING_CONFIDENCE_CAP` - naming-quality findings carry confidence `MEDIUM` or lower.
- `CRAFT_NOTES_MAX` - at most 10 craft notes per report.

Apply this matrix per partition:

| Situation                                           | Status           | Treatment                                                                                           |
|-----------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------|
| Consistent, idiomatic for the ecosystem             | `PASS`           | Strength                                                                                            |
| Consistent, non-idiomatic, documented               | `PASS`           | Observation of deliberate deviation, noting onboarding and interop cost only                        |
| Consistent, non-idiomatic, undocumented             | `PARTIAL`        | Low Concern to document it, migration only when cheap, never a purity rename                        |
| One dominant shape above `DOMINANCE_PASS`, outliers | `PARTIAL`        | Outliers are the defect, list them and recommend aligning to the dominant shape                     |
| Dominant shape between the two thresholds           | `PARTIAL`        | As above with higher severity and a drift-trend note                                                |
| No dominant shape below `DOMINANCE_PARTIAL`         | `FAIL`           | Split convention, recommend choosing one by T1, then T3-idiomatic, then majority, scoped per module |
| Consistent but semantically poor names              | `PARTIAL`/`FAIL` | Naming-quality finding, independent of consistency                                                  |
| Mixed style families inside one partition           | `FAIL`           | The mixing is the defect, not either family                                                         |
| Legacy partition beside a modern one                | per partition    | Assess each separately, recommend a ratchet, not a big-bang rename                                  |

## Ecosystem Anti-Patterns

Never flag these ecosystem-idiomatic forms:

- Short names such as `cfg`, `ctx`, `buf`, `i`, `err`, or a receiver `s` in Rust, Go, C, and
  small scopes.
- Missing file-per-class structure in Rust, Go, Python, Zig, or C.
- The `I` prefix on C# interfaces or the `Async` suffix on C# async methods.
- Names a framework mandates, such as `Service`, `Controller`, or `Repository` - judge
  cohesion of responsibility, not the word.
- Names mirroring an external contract: FFI or ABI structs, wire-format or JSON field names
  including serializer renames, OS or hardware API names, memory-map equates, generated code.

The same strictness applies in reverse: classes that are all `Util` are not excused by Java
idiom, and `snake_case` leaking into a `camelCase` JSON boundary without a rename layer is a
defect, not a style choice.

## Assessment Procedure

1. **Partition the source.** Group tracked source files by language and layer (app, library,
   tests, tooling, scripts, config). Exclude and list in the ledger: generated code
   (`@generated`, `Code generated ... DO NOT EDIT`, `<auto-generated>`), vendored or
   third-party trees, minified files, lockfiles, and scope-excluded submodules. Partitions
   under `MIN_PARTITION_SHARE` get a one-line note.
2. **Collect declared conventions (T1).** Read every config and document in the tier table
   above and the standards discovered by `assessment/standards-conformance.md`. Note enforced
   rules, disabled rules, and naming-rule settings. Count suppressions of naming or style
   rules (`#[allow(non_snake_case)]`, `eslint-disable ...naming-convention`, `# noqa: N8..`,
   `#pragma warning disable`, `// NOLINT`, `@SuppressWarnings`) per partition - high density
   signals deliberate deviation or drift.
3. **Identify forced names.** Mark identifiers mandated by external contracts so they leave
   the consistency denominators.
4. **Run the censuses.** Per partition and identifier kind (type, interface or trait,
   function or method, variable or parameter, constant, private member, module or package,
   file name, test name), classify each declaration by shape: `PascalCase`, `camelCase`,
   `snake_case`, `SCREAMING_SNAKE`, `kebab-case`, prefixed (`I*`, `_x`, `m_x`, `k*`), suffixed
   (`*Impl`, `*_t`, `*Async`), plus initialism handling (`Id` versus `ID`, `Url` versus
   `URL`). Use a declaration-shaped pattern per `references/census-commands.md` and record the
   exact regex or command in the ledger row, and `scripts/style-census.py` produces the same
   mechanical count.
5. **Compute dominance and consistency.** Per partition and kind, record the dominant shape,
   its share (n/N and %), and the outlier list of the top 10 by blast radius with `file:line`.
   Apply the matrix above.
6. **Add trend when Git history exists.** Compare the dominant-shape share in recently
   modified files against older files and report `converging`, `stable`, or `decaying`, so a
   fading legacy style separates from a new drift.
7. **Sample for semantics.** Stratified sample for naming quality and readability: every
   top-level module, the public API surface, the largest files, the most-churned files from
   `git log`, and the entry points - capped by `SAMPLE`, with the sampling frame recorded in
   the ledger.
8. **Check enforcement and drift of tooling.** Compare configured rules with sampled code
   (indentation, line length, brace style, import order, EOL, encoding). Config says X but
   code does Y is a finding, a canonical formatter with no config file is not a defect, and CI
   invocation cross-references `FND-INF-001` rather than restating it.
9. **Score and write up** per `process/report-format/code-style.md` and the scoring rules
   below.

## What To Evaluate: Lenses

Each lens yields a status from the shared vocabulary (`PASS`, `PARTIAL`, `FAIL`, `UNKNOWN`,
`N/A`).

| #    | Lens                      | Checks                                                                                                                                                                                                                                                                                                       |
|------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SL-1 | Convention fit            | Which tier applies, whether the dominant style is idiomatic for the ecosystem, whether deviation is documented                                                                                                                                                                                               |
| SL-2 | Consistency               | Casing, prefix, and suffix per kind. Vocabulary consistency (one concept one word: `get`/`fetch`/`load`, `cfg`/`conf`/`config`, `remove`/`delete`, singular/plural). Initialisms, spelling variants, mixed human languages in identifiers or comments                                                        |
| SL-3 | Naming quality            | The heuristics below, each hit with `file:line` examples and confidence at or under `NAMING_CONFIDENCE_CAP`                                                                                                                                                                                                  |
| SL-4 | Structure and granularity | File/module granularity matches the ecosystem, file name matches its primary type where that is the norm, directory/namespace mirroring, size outliers against the project's own distribution, cohesion of dumping-ground modules such as `utils` or `common`                                                |
| SL-5 | Comprehension aids        | Comments explain why not what, public API documented per ecosystem norm, stale or contradictory comments, commented-out code, noise comments, magic numbers versus named constants, `TODO`/`FIXME`/`HACK` density and age                                                                                    |
| SL-6 | Cognitive load            | Nesting depth, function length, parameter count, boolean-flag parameters, branch density, dense chained expressions, duplicated blocks, dead code by call-site search - judged by relative outliers such as three times the project's own 90th percentile plus ecosystem hints, never fixed absolute numbers |
| SL-7 | Idiomatic fluency         | The language's idioms used rather than transliterated from another ecosystem: iterators over index loops in Rust, RAII in C++, context managers in Python, error wrapping in Go, equates and routine contracts in assembly - reported as Observations or Strengths, flagged only when it harms readability   |
| SL-8 | Enforcement               | Convention encoded in tooling and documented, suppression density, config-versus-code drift, CI cross-reference to `FND-INF-001`                                                                                                                                                                             |

## Naming-Quality Heuristics (SL-3)

Apply with ecosystem awareness.

Each hit needs `file:line` examples and carries confidence at
or under `NAMING_CONFIDENCE_CAP`.

- **Noise or placeholder names**: `data`, `info`, `tmp`, `val`, `obj`, `stuff`, `thing`,
  `doIt`, `handle`, `process`, number-suffixed twins (`x1`, `x2`, `final2`), and type names
  carrying no responsibility (`Manager`, `Helper`, `Util`).
- **Misleading names**: `getX` that mutates or does I/O, `isX` not returning a boolean,
  `calculate*` that writes, a plural name holding a single value, `list` holding a map, names
  stale after a refactor, comments contradicting the name.
- **Wrong part of speech**: functions as verbs, types as nouns, predicates as `is`/`has`/`can`/
  `should`, booleans phrased positively rather than `disableX = false` or `isNotReady`.
- **Missing semantics**: quantities without a unit or typed unit - `timeout`, `size`, `length`
  do not say bytes, characters, or elements. A typed unit such as `Duration` makes a suffix
  unnecessary.
- **Scope-proportional length**: short names are fine in a scope of roughly 10-15 lines and
  are defects at module, exported, field, constant, config-key, and public-API level. Long
  names are defects when they restate type or context.
- **Abbreviation classes**: (a) ecosystem-canonical (`ctx`, `cfg`, `err`), (b) domain-canonical
  and defined in a glossary or widely known, (c) project-local but used identically
  everywhere, (d) ad hoc or multiply spelled, (e) cryptic - report the (d) and (e) rate, while
  (a) through (c) are not defects.
- **Typos and near-collisions**: misspelled identifiers, names differing by one character,
  visually ambiguous `l`/`O`/`I`, shadowing of builtins or keywords, reserved identifiers such
  as C `_Foo` or `__foo` or the POSIX `_t` suffix.
- **Boundary leakage**: one convention's names crossing into another's boundary without a
  mapping layer, such as `snake_case` fields in a `camelCase` API or database column names in
  UI code.
- **Tests**: names state the behavior under test, and file naming matches the ecosystem or
  the project's declared rule.

## Evidence And Ledger Conventions

One `EVD` row per partition census, one per semantic sample with its sampling frame, one for
the T1 configuration inventory, and one for suppression counts.

The subject's linters and formatters are `NOT RUN` rows and may appear only in a finding's
`Method` field as something the reader can run later.

Every census row records the exact pattern or command so a re-audit reproduces the figure,
per `references/census-commands.md`.

## Severity And Confidence

Style findings use the `CQY` pillar and derive severity from the impact-likelihood matrix:

- `Low` by default.
- `Medium` when the split sits in a library's public API, when misleading names sit on
  security or safety-relevant paths, or when more than 25% of identifiers in a core partition
  are affected.
- `High` only with a demonstrated hazard, never `Critical`.

Naming-quality findings are `Concern` with confidence at or under `NAMING_CONFIDENCE_CAP`,
while mechanical census findings may carry `HIGH` confidence.

Every consistency finding quantifies prevalence (n/N and %) and lists at least three
`file:line` examples, or all of them when fewer exist.

The `Basis` field of every style finding opens with the resolved tier, for example
`Tier T2 Observed: 88% snake_case ...`.

Blast radius weighs severity: a bad name in a public API, serialized field, config key, CLI
flag, or database column costs more to fix than a bad local variable.

## Scoring And Dimension

The section's sub-scores feed the `Code Style` scorecard dimension as a separate dimension,
not folded into `Code Quality`.

Suggested caps: dominance under `DOMINANCE_PARTIAL` in the main partition with no T1 caps the
dimension at 5/10, misleading or noise names concentrated in the public API cap it at 6/10,
confidence stays `MEDIUM` unless at least 70% of the score rests on mechanical censuses.

A subject whose only code is generated marks the dimension `N/A` with a Scope Exclusions
entry, and the dimension maps to Maintainability - Analysability and Modifiability - in the
ISO/IEC 25010:2023 crosswalk.

## Status Criteria

- `PASS`: A coherent convention resolved to a named tier, dominance at or above
  `DOMINANCE_PASS`, naming quality clean on the sampled surface, with evidence.
- `PARTIAL`: A mostly coherent convention with bounded outliers, drift, or naming-quality
  issues, or a deliberate undocumented-but-consistent deviation.
- `FAIL`: No dominant convention, mixed style families inside a partition, or pervasive
  misleading naming, with evidence.
- `UNKNOWN`: Source was not provided in inspectable depth.
- `N/A`: The subject carries no source code.

## Common Risks

- A split convention makes every new identifier a coin toss and raises review cost.
- Misleading names on public or security-relevant surfaces cause real misuse, not just
  annoyance.
- Convention drift without tooling enforcement compounds with every commit.
- Renames on serialized fields, config keys, CLI flags, or schema columns break external
  contracts, so their cost is architectural, not cosmetic.
- Enforcing another ecosystem's taste against an idiomatic codebase creates churn without
  quality gain.

## What Raises Confidence

- A declared convention consistent with the code, or a dominant observed shape above
  `DOMINANCE_PASS`.
- Naming rules encoded in `.editorconfig` or linter configuration with low suppression
  density.
- Names that state responsibility and units, and public API surfaces that read fluently.
- Good naming, clear structure, and idiomatic fluency feed the Strengths & What's Working
  section with examples.

Mark each missing signal explicitly rather than inferring its presence.

## Remediation Ladder

Recommendations follow this ladder, preferring the cheapest rung that fixes the problem:

1. **Document** the convention - a `STYLE.md` or a `CONTRIBUTING` section, including accepted
   abbreviations and any deliberate deviation.
2. **Encode** it in tooling: naming rules in `.editorconfig` or the linter, formatter config,
   pre-commit, and CI, with a ratchet that enforces on new and changed code and
   baseline-suppresses the rest.
3. **Align outliers** opportunistically when files are touched.
4. **Rename misleading public names** with a deprecation path - shim, alias, changelog entry -
   because blast radius is high.
5. **Bulk rename** only when it is automated, reviewed, and covered by tests, and only when a
   split convention truly leaves no dominant shape.

Never recommend adopting another ecosystem's convention because it is fashionable.

## Craft Notes

Craft Notes are subjective, non-finding suggestions: elegance, idiom polish, small wins.

Each is one line tagged `Suggestion`, capped by `CRAFT_NOTES_MAX`, and never counted in
findings, risks, or recommendations.

Taste lives here.

Objective defects are findings.
