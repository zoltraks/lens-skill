# Clean-Code Baseline

## Purpose

> **Scope:** Cross-stack clean-code defect classes distilled from the maintainer's general
> engineering standards
> **Key items:** SOLID checks, duplication, naming honesty, function shape, comment and error
> discipline, testability seams

This file is distilled from a maintainer-supplied engineering-standards corpus during skill
upkeep, cross-checked against the canonical sources each stack row of
`references/stack-standards.md` already names.

Snapshot date: 2026-10-27.

Feeds `assessment/code-quality.md`, `assessment/code-style.md`, and
`assessment/maintainability-review.md` for every stack.

## Non-Negotiables

- A critique names the violated principle, not a preference - "this function does two things"
  is a finding, "I would write it differently" is not.
- Two copies of a concept are debt: duplication that can drift is a finding whether or not a
  bug exists today.
- A misleading or cryptic name is a defect - names answer for the code they label.
- When two shapes satisfy the constraints, the smaller and simpler one wins - surplus
  abstraction is a finding.

## Design Rules

- Single responsibility: a module, class, or function has one reason to change - a name that
  needs "and" describes two responsibilities.
- Open/closed: behaviour extends by adding code, not by editing working code - a change list
  that rewrites stable branches signals a missing seam.
- Liskov substitution: a subtype honours the contract of its base - a subclass that weakens
  guarantees or throws where the base does not is a finding.
- Interface segregation: many narrow contracts over one fat one - a consumer forced to depend
  on members it never calls is a finding.
- Dependency inversion: depend on the seam, not the concretion - constructor injection or a
  dispatch seam, never `new` inside logic.

## Duplication And Simplicity

- DRY applies to concepts, not tokens: two snippets that look alike but evolve for different
  reasons are not duplication, and merging them is a finding in the other direction.
- YAGNI: code written for a hypothetical future is a finding - extension points earn their
  cost only where a recorded requirement names the second case.
- KISS: the smallest structure that solves the problem wins; a framework or pattern applied
  beyond its problem is surplus machinery.

## Naming, Functions, And Comments

- Names describe the role, never the type encoding - Hungarian prefixes and container-word
  suffixes that restate the type are findings outside ecosystems that mandate them.
- A function does one thing at one level of abstraction; mixed levels inside one body are a
  cohesion finding.
- Comments carry reasons and references, never restatements of the code - commented-out code
  is a finding (version control already keeps history).

## Error Handling And Testability

- Exceptions are for exceptional paths - using them for expected control flow is a finding,
  and a swallowed `catch` converts a failure into a wrong answer.
- Testable shape is the floor: clock, file system, and network are injected seams, and a unit
  that cannot be exercised in isolation is a design finding, not a test finding.

## Live Check

This digest carries no external links of its own - the per-stack digests and
`references/stack-standards.md` supply the authoritative citations it generalizes.
