# Testing and Testability

## Purpose

> **Scope:** Test pyramid (unit, integration, end-to-end), TDD practice, coverage, CI automation,
> design-for-testability
> **Key items:** test layers, test-driven development, coverage evidence, automated execution, seams
> and injectability

This file guides assessment of how the system verifies its own behavior and how amenable the code is
to testing.

Apply `principles/evaluation-rules.md` throughout. Presence of a test directory is not evidence of
effective testing, inspect content. Design-level testability overlaps with the Dependency Inversion
principle in `assessment/design-principles.md`.

## What To Evaluate

- Unit tests: isolated tests of functions, classes, or modules.
- Integration tests: tests across module or service boundaries, including data stores.
- End-to-end tests: tests that exercise the system through its external interfaces.
- Test pyramid balance: whether the mix is weighted toward fast unit tests with fewer, targeted
  integration and e2e tests, rather than inverted.
- Test-driven development: whether there are signals that tests are written alongside or before
  code, such as commit interleaving, red-green history, or a documented TDD practice.
- Design-for-testability: whether the code exposes seams - dependency injection, interfaces, pure
  functions - that make units testable without heavy mocking.
- CI automation: whether tests run automatically on change, and whether failures block merge or
  release.
- Coverage depth: whether tests verify edge cases, boundary conditions, error paths, and negative
  cases, not just happy-path execution. Counting test lines or test files is not evidence of
  semantic coverage.

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

## Evidence Of Test Effectiveness

Inventory tests per project and distinguish declared, discovered, and documented result counts.

The audit never executes the suite. Executed, passed, failed, and ignored counts exist only when
a committed report or documentation records them, cited as `Reported` evidence.

Classify test layers by the boundaries exercised, not just the directory or test name.

Identify the checks the project documents, for Rust typically `cargo build --locked`,
`cargo test --locked`, `cargo clippy --locked -- -D warnings`, and `cargo fmt --check`, from
build scripts, CI configuration, or contributor documentation. Do not run them.

Judge whether tests run automatically on change and whether failures block merge or release from
pipeline definitions, not from execution.

Keep compilation claims, inspected test counts, and documented passing results separate.

**Coverage**

Treat coverage as evidence only when a committed report, badge source, or documented run supplies
it.

Inspect the report's covered/total counts, line/region/branch metric, exclusions, and critical
modules separately from the project aggregate.

Branch and line coverage measure different things, do not infer one from the other.

Undocumented coverage is `UNKNOWN`, not zero and not a percentage derived from test counts.

**Mutation testing**

Assess mutation testing from committed configuration, harnesses, and reports. Do not run
[cargo-mutants](https://mutants.rs/) or a stack equivalent.

When a mutation score is documented, check whether its numerator, denominator, and excluded
outcomes are defined.

A documented survivor is a review candidate, not automatically proof of a missing assertion,
because equivalent mutations and harness limitations can occur.

Do not infer mutation scores or repository-wide weakness from a selected sample.

**Fuzz and property testing**

Prioritize parsers, path resolution, protocol framing, and serialization boundaries when judging
whether fuzz coverage is warranted.

Assess fuzzing from harness presence, declared scope, invariants, corpus, and committed results.
Do not run fuzzers.

A documented bounded run without crashes is not proof of safety.

**Assertion quality**

When reporting stub or construction-only tests, cite examples and report the reviewed sample size.

Describe what behavior is not checked, recognizing that schema/default-value tests can be useful.

Do not invent a universal behavioral-to-struct-test ratio or coverage target.

Derive acceptance criteria from required behavior, including unauthorized rejection, permitted
success, no unintended side effects, failure handling, and regression coverage.

## Status Criteria

- `PASS`: Tests exist across the layers the system needs in a balanced pyramid, the code is
  structured for testability, CI configuration runs tests on change, and failures block release,
  with evidence.
- `PARTIAL`: Some layers, automation, or testability seams exist but coverage is uneven, the pyramid
  is inverted, gates are missing, or evidence is incomplete.
- `FAIL`: No meaningful tests where the system clearly requires them, with evidence of absence.
- `UNKNOWN`: Testing artifacts were not provided or cannot be inspected.

## Common Risks

- Regressions ship undetected because no automated gate blocks failing changes.
- An inverted pyramid (many slow e2e, few units) makes the suite slow and flaky.
- Tightly coupled code without seams forces brittle, mock-heavy tests or blocks unit testing
  entirely.
- Coverage numbers exist without assertions of behavior, giving false confidence.
- Large test counts mask shallow coverage: edge cases, boundary conditions, and error paths are
  untested.
- Integration paths are untested while units pass in isolation.
- Tests exist but are not run in CI, so they decay.

## What Raises Confidence

- A balanced test pyramid matching the system architecture.
- Evidence of TDD or test-first discipline, such as tests landing with the code that satisfies them.
- Code with injectable dependencies and pure functions that are testable in isolation.
- A CI configuration that runs the suite on every change with an enforced quality gate.
- Tests that assert behavior and outcomes, not just that code executes.
- Tests that cover edge cases, boundary conditions, error paths, and negative cases, evidenced by
  assertion variety.

Mark each missing signal explicitly rather than inferring its presence. Do not infer TDD from the
mere existence of tests, cite a concrete signal.
