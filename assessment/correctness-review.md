# Functional Correctness

## Purpose

> **Scope:** Logic defects, contract violations, unimplemented surface, boundary and ordering
> errors detectable from source
> **Key items:** defect-pattern census, shipped-surface completeness, read-confirmation
> discipline, reachability

This file guides assessment of whether the code does what it claims to do - the `FNC`
criterion family in `references/criterion-catalogue.md`.

Apply `principles/evaluation-rules.md` throughout.

Architectural fitness is assessed in `assessment/design-principles.md`, code-level hygiene in
`assessment/code-quality.md`, and test adequacy in `assessment/testing-review.md` - this
category hunts concrete defects in the shipped surface itself.

## What To Evaluate

- Whether advertised operations produce their declared behavior or a stub, placeholder, or
  constant result.
- Whether comparisons, indexes, boundaries, and arithmetic compute what the contract requires.
- Whether resource lifecycle - acquisition, use, disposal, cancellation - is correct under
  every inspected path.
- Whether the public surface is complete: no advertised member silently unimplemented.

## Evidence To Look For

| Signal                       | Where It Appears                                                        |
|------------------------------|-------------------------------------------------------------------------|
| Unimplemented throws         | `NotImplementedException`, `NotImplementedError`, `unimplemented!()` and equivalents in shipped code |
| Empty public types           | Type declarations with no members on the public surface                 |
| Constant-return placeholders | Methods returning a fixed success value without doing the advertised work |
| Always-false comparisons     | Non-nullable value types compared to `null`, tautological conditions    |
| Boundary inversions          | `== 0` vs `>= 0` index checks, off-by-one loops, `array[0]` for `array[i]` |
| Discarded configuration      | A constructor or builder that configures a local and leaves the receiver unset |
| Inverted arithmetic          | `end - start` computed as `start - end`, swapped arguments              |
| Wrong-variable checks        | One variable validated while a different one is used                    |
| Overlay hazards              | Explicit memory layout overlapping managed and unmanaged members        |
| Unbounded loops              | Worker loops without a blocking, yield, or backoff call                 |
| Termination APIs             | Thread-kill or forced-abort calls unavailable on declared targets       |
| Dispose-while-in-use         | Resources nulled or disposed while other members still reference them   |
| Undisposed resources         | Handles, streams, and subscriptions never released on an exit path      |
| Overwrite-primitive misuse   | `move`/`rename`/`copy` calls whose replace-existing behavior differs    |
|                              | across platforms, beside a dead `AlreadyExists` guard or catch          |
| Write-before-commit ordering | Side-effecting file or store writes inside a transaction that can roll  |
|                              | back, leaving the durable side ahead of the record                      |
| Dead catch branches          | Exception handlers for types the guarded block cannot raise             |

## Defect-Pattern Census

Run a mechanical census for the patterns above across the in-scope source.

A census hit is a candidate, never a finding - each candidate is confirmed by reading the
mechanism, its guards, and its callers.

Record the census pattern and denominator in the evidence ledger beside the confirmed count,
per `references/census-commands.md`.

Where a defect lives behind a conditional-compilation or target-framework path, name the
target preconditions - a defect masked by an unreachable target stays a finding with its
reachability recorded, not a dismissal.

Where a defect needs runtime confirmation the evidence mode does not permit, the finding
keeps its inspected basis and the verification goes to the Operator Verification Handoff.

## Shipped-Surface Completeness Census

Apply the completeness recipe in `references/topics/evidence-recipes.md` to the public
surface: unimplemented-throw sites counted against declared members, empty public types, and
methods returning constant success without side effects.

A documented capability backed by a stub is a spec violation per
`process/readiness-scoring.md` - an unimplemented public member is the same class of finding.

## Status Criteria

- `PASS`: The inspected surface computes what it advertises, no confirmed defects in the
  census, supported by evidence.
- `PARTIAL`: The surface is largely correct but confirmed defects exist in bounded areas, or
  census coverage was partial.
- `FAIL`: Confirmed defects affect core advertised behavior, or the shipped surface contains
  substantial unimplemented members presented as complete.
- `UNKNOWN`: Source was not provided or could not be inspected.

## Common Risks

- Silent wrong results are worse than crashes - an inverted comparison returns a plausible
  value that corrupts downstream state without raising an error.
- Unimplemented public members surprise consumers at runtime after the package looked
  complete from its surface.
- Defects behind conditional compilation ship silently to the targets where they apply.
- Placeholder methods that return success mask missing behavior from both callers and tests.
- Dispose and lifecycle defects surface only under load or cancellation paths tests miss.

## What Raises Confidence

- Confirmed mechanism and reachability, not a pattern match alone.
- A census denominator stated so the confirmed count is reproducible.
- Defects traced to their observable effect, with counter-evidence checked.
- Executed evidence under a commissioned mode, classified per
  `references/topics/execution-isolation.md`, corroborating an inspected defect.

Mark each missing signal explicitly rather than inferring its presence.
