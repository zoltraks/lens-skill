# Testing and Testability

## Purpose

> **Scope:** Test pyramid (unit, integration, end-to-end), TDD practice, coverage, CI automation, design-for-testability
> **Key items:** test layers, test-driven development, coverage evidence, automated execution, seams and injectability

This file guides assessment of how the system verifies its own behavior and how amenable the code is to testing.

Apply `principles/evaluation-rules.md` throughout. Presence of a test directory is not evidence of effective testing, inspect content. Design-level testability overlaps with the Dependency Inversion principle in `assessment/design-principles.md`.

## What To Evaluate

- Unit tests: isolated tests of functions, classes, or modules.
- Integration tests: tests across module or service boundaries, including data stores.
- End-to-end tests: tests that exercise the system through its external interfaces.
- Test pyramid balance: whether the mix is weighted toward fast unit tests with fewer, targeted integration and e2e tests, rather than inverted.
- Test-driven development: whether there are signals that tests are written alongside or before code, such as commit interleaving, red-green history, or a documented TDD practice.
- Design-for-testability: whether the code exposes seams - dependency injection, interfaces, pure functions - that make units testable without heavy mocking.
- CI automation: whether tests run automatically on change, and whether failures block merge or release.
- Coverage depth: whether tests verify edge cases, boundary conditions, error paths, and negative cases, not just happy-path execution. Counting test lines or test files is not evidence of semantic coverage.

## Evidence To Look For

| Signal             | Where It Appears                                                         |
|--------------------|--------------------------------------------------------------------------|
| Unit test files    | Test directories, files named for test frameworks                        |
| Integration tests  | Tests that spin up databases, services, or mocks                         |
| End-to-end tests   | Browser, API, or workflow test suites                                    |
| Test pyramid shape | Ratio of unit to integration to e2e tests                                |
| TDD signals        | Test-and-code commits interleaved, red-green history, contributing guide |
| Testability seams  | Injected dependencies, interfaces, pure functions                        |
| Coverage data      | Coverage reports, badges, config thresholds                              |
| Coverage depth     | Edge-case assertions, boundary tests, error-path coverage                |
| CI configuration   | Pipeline files, workflow definitions                                     |
| Gate on failure    | Required checks, branch protection, pipeline gates                       |

## Execution And Effectiveness Evidence

Inventory tests per project and distinguish declared, discovered, executed, passed, failed, ignored,
and filtered counts, including the command and revision that produced each count.

Classify test layers by the boundaries exercised, not just the directory or test name.

Run documented checks with the approved target and feature set when safe and permitted.

For Rust, typical baseline commands are `cargo build --locked`, `cargo test --locked`,
`cargo clippy --locked -- -D warnings`, and `cargo fmt --check`.

Apply workspace or manifest selection only after verifying the actual workspace structure.

Do not assume `--all-features` is valid when features are mutually exclusive.

Keep compilation-only checks, source test counts, and actual passing test results separate.

**Coverage**

Use existing reports or an approved tool such as
[cargo-llvm-cov](https://github.com/taiki-e/cargo-llvm-cov) to measure coverage.

Record covered/total counts, line/region/branch metric, exclusions, target/features, and critical
modules separately from the project aggregate.

Branch coverage may require nightly and explicit flags, do not infer it from line coverage.

Unmeasured coverage is `UNKNOWN`, not zero and not a percentage derived from test counts.

**Mutation testing**

Use [cargo-mutants](https://mutants.rs/) or a stack equivalent for bounded, high-value modules
when test effectiveness is uncertain and execution is approved.

Require a passing baseline and report generated, tested, caught, missed, unviable, timed-out, and
excluded mutations, using the tool's actual categories.

If a mutation score is reported, define its numerator and denominator and show excluded outcomes.

A survivor is a review candidate, not automatically proof of a missing assertion, because equivalent
mutations and harness limitations can occur.

Do not infer mutation scores or repository-wide weakness from a selected sample.

**Fuzz and property testing**

Prioritize parsers, path resolution, protocol framing, and serialization boundaries.

For [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz), verify nightly, compiler, architecture,
and OS support, native Windows is not supported by the documented libFuzzer setup.

Record harness scope, invariants, corpus, execution budget, and reproducible minimized failures.

Creating a harness changes the project and needs approval beyond simply running existing tests.

No crashes in a bounded run is not proof of safety.

**Assertion quality**

When reporting stub or construction-only tests, cite examples and report the reviewed sample size.

Describe what behavior is not checked, recognizing that schema/default-value tests can be useful.

Do not invent a universal behavioral-to-struct-test ratio or coverage target.

Derive acceptance criteria from required behavior, including unauthorized rejection, permitted
success, no unintended side effects, failure handling, and regression coverage.

## Status Criteria

- `PASS`: Tests exist across the layers the system needs in a balanced pyramid, the code is structured for testability, tests run automatically, and failures block release, with evidence.
- `PARTIAL`: Some layers, automation, or testability seams exist but coverage is uneven, the pyramid is inverted, gates are missing, or evidence is incomplete.
- `FAIL`: No meaningful tests where the system clearly requires them, with evidence of absence.
- `UNKNOWN`: Testing artifacts were not provided or cannot be inspected.

## Common Risks

- Regressions ship undetected because no automated gate blocks failing changes.
- An inverted pyramid (many slow e2e, few units) makes the suite slow and flaky.
- Tightly coupled code without seams forces brittle, mock-heavy tests or blocks unit testing entirely.
- Coverage numbers exist without assertions of behavior, giving false confidence.
- Large test counts mask shallow coverage: edge cases, boundary conditions, and error paths are untested.
- Integration paths are untested while units pass in isolation.
- Tests exist but are not run in CI, so they decay.

## What Raises Confidence

- A balanced test pyramid matching the system architecture.
- Evidence of TDD or test-first discipline, such as tests landing with the code that satisfies them.
- Code with injectable dependencies and pure functions that are testable in isolation.
- A CI configuration that runs the suite on every change with an enforced quality gate.
- Tests that assert behavior and outcomes, not just that code executes.
- Tests that cover edge cases, boundary conditions, error paths, and negative cases, evidenced by assertion variety.

Mark each missing signal explicitly rather than inferring its presence. Do not infer TDD from the mere existence of tests, cite a concrete signal.
