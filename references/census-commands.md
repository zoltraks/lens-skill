# Census Commands

## Purpose

> **Scope:** Canonical counting methods for recurring audit censuses
> **Key items:** git history, author concentration, conditional directives, catch clauses,
> test inventory, tracked artifacts

This file defines the standard measurement for each recurring census an audit reports. Apply
the method named here and record the counting rule beside the figure in the evidence ledger, so
a re-audit can reproduce the number instead of re-inventing the method.

A census figure without its counting rule is not comparable across reports.

## Recording Rule

For every census number in a report, the ledger note names the command or pattern and the
denominator.

When the previous report used a different method, restate the figure under the canonical method
and record the change as an evidence correction per `synthesis/report-comparison.md`.

## Git History

| Measurement          | Method                                                                             |
|----------------------|------------------------------------------------------------------------------------|
| Commit count         | `git rev-list --count HEAD` total and `--no-merges` non-merge, report both         |
| Author concentration | `git log --no-merges --format="%an"` grouped by name, share of the non-merge total |
| Tag history          | `git tag` list                                                                     |
| History span         | First and last commit dates                                                        |
| Revert or fix pairs  | Commit subjects and file stats from `git log` and `git show`                       |

Author concentration uses the non-merge denominator.

State which count a figure uses wherever it appears, the total includes merges.

## Conditional Directives

Count `#if`-family directives with a stated inclusion rule.

| Directive | Include rule                      |
|-----------|-----------------------------------|
| `#if`     | Always counted                    |
| `#elif`   | State whether counted             |
| `#else`   | State whether counted             |
| `#endif`  | Never counted as a directive site |

The reported figure names the directives included, for example
"167 `#if` plus 19 `#elif`/`#else`".

## Catch Clauses

Keep these distinct counts separate.

| Count               | Definition                                  |
|---------------------|---------------------------------------------|
| Keyword occurrences | Every `catch` keyword, including comments   |
| Clauses             | `catch` clauses with a body block           |
| Empty bodies        | Clauses whose body contains only whitespace |
| Comment-only bodies | Clauses whose body contains only comments   |

An "empty catch" means a whitespace-only body.

Comment-only bodies are counted separately and checked for a documented justification such as an
intentional-swallow note or a refactoring record.

A keyword count is not a clause count, never substitute one for the other.

## Test Inventory

| Measurement       | Method                                                             |
|-------------------|--------------------------------------------------------------------|
| Test classes      | Files or classes carrying the framework's test-class attribute     |
| Test methods      | Members carrying the test-method attribute, name the attribute     |
| Test source files | All source files under the test project excluding generated output |

Distinguish attributed test classes from all source files, they are different counts.

## Declaration Census

Count declarations, not keyword mentions.

A keyword such as `interface`, `class`, or `public` appears in comments, strings, and member
names besides declarations.

Use a declaration-shaped pattern or an explicit enumeration of declaring lines.

## Tracked Artifacts

| Measurement     | Method                                                                 |
|-----------------|------------------------------------------------------------------------|
| Tracked files   | `git ls-files`, not a working-tree listing                             |
| Tracked binary  | `git ls-files` filtered by extension or binary check                   |
| Ignored content | `.gitignore` patterns plus `git check-ignore`, not filesystem presence |

A directory present on disk is not committed content until `git ls-files` or
`git check-ignore` says otherwise.

## Anchor Precision

Anchor every observation to a file and line range.

When no single line carries the defect, describe the mechanism and give the nearest anchor, an
honest range beats a fabricated line.
