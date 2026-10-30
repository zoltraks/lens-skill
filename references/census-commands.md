# Census Commands

## Purpose

> **Scope:** Canonical counting methods for recurring audit censuses
> **Key items:** git history, author concentration, conditional directives, catch clauses,
> test inventory, tracked artifacts

This file defines the standard measurement for each recurring census an audit reports.

Apply the method named here and record the counting rule beside the figure in the evidence ledger,
so a re-audit can reproduce the number instead of re-inventing the method.

A census figure without its counting rule is not comparable across reports.

## Recording Rule

For every census number in a report, the ledger note names the command or pattern and the
denominator.

When the previous report used a different method, restate the figure under the canonical method
and record the change as an evidence correction per `synthesis/report-comparison.md`.

## Snapshot Identity

| Measurement  | Method                                                   |
|--------------|----------------------------------------------------------|
| Commit       | `git rev-parse HEAD` per audited repository root         |
| Branch       | `git branch --show-current`, or detached-HEAD state      |
| Dirty tree   | `git status --porcelain` - clean, or the dirty path list |
| Capture time | The clock reading at intake when no VCS metadata exists  |

These values feed Document Information.

Every claim in the report binds to this snapshot, and a re-audit on a different snapshot is a
different tree until proven otherwise.

## Git History

| Measurement            | Method                                                                                        |
|------------------------|-----------------------------------------------------------------------------------------------|
| Commit count           | `git rev-list --count HEAD` total and `--no-merges` non-merge, report both                    |
| Author concentration   | `git log --no-merges --format="%an"` grouped by name, share of the non-merge total            |
| Tag history            | `git tag` list                                                                                |
| History span           | First and last commit dates                                                                   |
| Revert or fix pairs    | Commit subjects and file stats from `git log` and `git show`                                  |
| Branch topology        | `git merge-base a b`, `git rev-list --count a..b`, `git diff --name-status a b`               |
| Ref-only tree census   | `git ls-tree -r --name-only <ref>`, `git show <ref>:<path>` - no checkout needed              |
| Commit-subject quality | `git log --format="%s"` - share of subjects under a stated word threshold, name the threshold |
| Commit-size outliers   | `git log --name-only` or `git show --shortstat` - files per commit, report the top entries    |
| Branch divergence      | `git rev-list --count a..b` and `b..a` ahead/behind, plus the last-commit date per branch     |
| Merge-noise share      | `git log --format="%s"` - share of self-merge subjects such as `merge remote-tracking`        |

Author concentration uses the non-merge denominator.

State which count a figure uses wherever it appears, the total includes merges.

The subject-quality, commit-size, divergence, and merge-noise censuses feed the History
Hygiene block in `references/delivery-practice.md`.

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

## Identifier Shape Census

The code-style census classifies every declaration in a partition by casing shape, per
`assessment/code-style.md`.

| Step            | Method                                                                                                                                             |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Partitioning    | Group `git ls-files` source paths by language and layer. Drop generated, vendored, minified, and excluded trees                                    |
| Kind patterns   | One declaration-shaped pattern per identifier kind, for example `^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)` for JS/TS functions |
| Shape classes   | `PascalCase`, `camelCase`, `snake_case`, `SCREAMING_SNAKE`, `kebab-case`, prefixed, suffixed, other                                                |
| Dominant share  | Largest shape count over the kind's denominator, reported as n/N and %                                                                             |
| Forced names    | Identifiers mirroring external contracts are excluded from the denominator and disclosed                                                           |
| Trend           | Repeat the dominant-share count on files modified in the last N commits versus the rest, when Git is in scope                                      |
| Mechanical tool | `scripts/style-census.py` produces the same per-partition counts deterministically                                                                 |

Record the exact pattern per kind in the ledger note.

A repeated run on the same snapshot produces identical counts.

## Tracked Artifacts

| Measurement     | Method                                                                 |
|-----------------|------------------------------------------------------------------------|
| Tracked files   | `git ls-files`, not a working-tree listing                             |
| Tracked binary  | `git ls-files` filtered by extension or binary check                   |
| Ignored content | `.gitignore` patterns plus `git check-ignore`, not filesystem presence |

A directory present on disk is not committed content until `git ls-files` or
`git check-ignore` says otherwise.

## Source Probes

These read-only probes answer recurring audit questions.

Each is a search pattern or file enumeration, never an executed build or test.

| Probe                  | Method                                                                                                                                                                                    | What it bounds                                                                          |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Import census          | Enumerate `import`/`require`/`use`/`using`/`#include` statements per file, dedupe to the external-module set                                                                              | Which declared dependencies are actually used, and which imports lack a manifest entry  |
| Engines drift          | Compare `engines`, `requires-*`, `go`, or `<TargetFramework>` floors against syntax features used                                                                                         | Whether code can run at the declared floor                                              |
| Secret-shape scan      | Search credential-shaped patterns (`AKIA`, `BEGIN.*PRIVATE KEY`, `password\s*=`, `api[_-]?key\s*[:=]`) across every `git ls-files` path. Count and locate matches, never reproduce values | Candidate secret locations for tracing                                                  |
| Unimplemented-surface  | Declaration-shaped patterns for unimplemented throws (`NotImplementedException`, `NotImplementedError`, `unimplemented!()`, `todo!()`) and empty public type declarations                 | Completeness of the shipped public surface                                              |
| Missing-file checklist | Enumerate expected files per stack (`LICENSE`, `README`, lockfile, CI config, `.gitignore`) against `git ls-files`                                                                        | Absent baseline artifacts                                                               |
| Lockfile census        | Count resolved entries per lockfile (`package-lock.json` `packages` keys, `Cargo.lock` `[[package]]`, `go.sum` module lines)                                                              | Component totals, direct/transitive split                                               |
| Compose-env parity     | Diff `environment`/`env_file` keys in `compose.*` against env vars read by the code                                                                                                       | Undeclared or dead configuration                                                        |
| Dockerfile surface     | Enumerate `FROM`, `USER`, `EXPOSE`, `HEALTHCHECK`, `ADD`/`COPY` sources, and `ENV`/`ARG` literals                                                                                         | Image provenance, privilege, exposed surface                                            |
| Annotation floor       | Count framework attributes/decorators (`@Controller`, `[Route]`, `@app.route`) vs handler declarations                                                                                    | Whether declared surface matches registered surface                                     |
| Workflow pin census    | List every `uses:` ref in workflow files and its pin form (SHA, tag, branch)                                                                                                              | Mutable third-party action references                                                   |
| Registration diff      | Diff shipped files on disk against files registered in `SKILL.md`, manifests, or index files                                                                                              | Unregistered or dangling resources                                                      |
| Derived-literal census | Search literals that duplicate declared configuration (URLs, timeouts, limits hardcoded where a config key exists)                                                                        | Configuration drift candidates                                                          |
| Attribution census     | `git log --no-merges --format="%an <%ae>%n%b"` scanned for the signatures in `references/methodology/ai-provenance.md`                                                                    | Per-tool attributed-commit count and share of the non-merge total                       |
| Dead-comment share     | Count lines inside block comments (`/* */`, `<!-- -->`, `'''`/`"""`) and wholly commented-out files against production line totals                                                        | Share of shipped source that is dead commentary                                         |
| DOM-sink census        | Search markup/execution sinks (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `dangerouslySetInnerHTML`, `document.write`, `eval(`) in client source                                     | Client-side injection surface, per `references/topics/frontend-security.md`             |
| Accessibility markers  | Count `aria-`, `role=`, `tabIndex`, `htmlFor`, `onKeyDown`, `Escape`, `autoFocus` occurrences in UI source                                                                                | Accessibility implementation density, per `references/topics/accessibility-baseline.md` |
| Client-storage census  | Enumerate `localStorage`/`sessionStorage` keys written and the keys cleared at logout                                                                                                     | Sensitive residue surviving logout                                                      |
| Storage-vs-writes diff | Diff the repository's `findById`-style read accessors against entities carrying tombstone flags                                                                                           | Read paths that can serve deleted rows                                                  |

Count what the probe counts and record the pattern beside the figure.

The secret-shape scan sweeps the whole tracked tree regardless of which projects the
inclusion gate selected - exposure in an excluded example, test, or docs directory is still a
finding in the audited tree.

A probe result is a candidate set - each candidate is confirmed by reading the file before it
becomes a finding.

## Attribution Census

The attribution census counts agent-attributed commits, not agent-written code.

Scan author names, author emails, and trailer lines against the signature table in
`references/methodology/ai-provenance.md`, count matches per tool, and report each count
beside the non-merge total.

Merge commits carrying a bot author identity are counted separately - a bot-authored
merge is an attributed integration, not an attributed change.

Author and committer identities outrank trailers when the two disagree.

Squash merges and history rewrites erase trailers, and attribution is opt-out, so the
census is a floor: report attributed counts, never a "percentage human" remainder.

The figure feeds the provenance assessment in `assessment/generated-code.md` and excludes
automation identities (`github-actions[bot]`, `dependabot[bot]`, release bots) that mark
machine-driven changes rather than generative authorship.

## Anchor Precision

Anchor every observation to a file and line range.

When no single line carries the defect, describe the mechanism and give the nearest anchor, an
honest range beats a fabricated line.
