# Architectural Assessment

## Purpose

> **Scope:** The architectural assessment section and its conditional subsections
> **Key items:** design principles, data flow diagram, design patterns, decision records

Provide an architectural critique against industry baselines.

Evaluate coupling, cohesion, state management, separation of concerns,
and pattern consistency against the stated constraints.

Anchor every claim to a concrete file path or design decision.

Do not judge the stack choice itself.

Structure this section with four subsections: `### What Works`, `### What Needs Attention`,
`### Design Principles`, and `### Industry Baseline Comparison`.

Use Title Case for all subsection titles.

Put exactly one empty line after each subsection header before the first sentence.

When listing multiple related items (e.g., typical production practices),
use a bullet list rather than an inline comma-separated paragraph.

Put an empty line between the intro sentence and the first bullet.

The Architectural Assessment may also carry up to three conditional subsections,
included only when their criteria are met.

When included, place them in this order,
after `### Design Principles` and before `### Industry Baseline Comparison`.

## Design Principles

Always include this subsection.

Evaluate the code against the SOLID principles and DRY per `assessment/design-principles.md`.

Present one row per principle:

| Principle             | Status | Evidence |
|-----------------------|--------|----------|
| Single Responsibility |        |          |
| Open/Closed           |        |          |
| Liskov Substitution   |        |          |
| Interface Segregation |        |          |
| Dependency Inversion  |        |          |
| DRY                   |        |          |

Reuse evidence already gathered for other findings instead of re-investigating it.

When a violation was already described elsewhere,
for example a Liskov Substitution breach logged as a contract defect,
name and cross-reference that finding here rather than duplicating the analysis.

Mark each principle `N/A` when no source was inspected for it.

## Data Flow Diagram

Include this subsection only when the system moves data across a trust boundary,
per `assessment/data-flow.md`.

It is the foundation for the Threat Model section.

Present a Level-0 (context) and a Level-1 (decomposition) view.

Use a fenced ASCII block or a flow table.

Then list the trust boundaries.

**Level-0 (context)**

```
    ╭────────────╮         ╭──────────────╮
    │            │         │              │
    │ MCP Client │────────>│ SQLite Index │
    │            │         │              │
    ╰────────────╯         ╰──────────────╯
            │
            │
            v
    ╭─────────────╮         ╭──────────────╮
    │             │         │              │
    │ REST Client │────────>│ Filesystem   │
    │             │         │              │
    ╰─────────────╯         ╰──────────────╯
            ^
            │
    ╭────────────╮
    │            │
    │ Git Remote │
    │            │
    ╰────────────╯
            ^
            │
    ╭──────────────╮
    │              │
    │ Index Server │
    │              │
    ╰──────────────╯
```

**Trust boundaries**

| Boundary        | From    | To         | Crossing Control      |
|-----------------|---------|------------|-----------------------|
| Network ingress | Client  | Auth layer | JWT validation        |
| Storage         | Handler | Filesystem | Path canonicalization |

Use framed nodes with box-drawing characters for every DFD element - `╭` `─` `╮` top
borders, `│` sides, `╰` `─` `╯` bottom borders, and `┌` `┬` `┼` `┐` junction glyphs where a
flow fans out to several targets.

Every row of a frame shares the same left and right border columns: each `│` side sits exactly
under its `╭` or `╮` corner, and `╰` and `╯` close exactly under the sides.

A content or border row shifted even one column off its frame is a defect - redraw the frame
rather than leaving a drifted edge.

Set each frame's interior width to its longest label line plus two - one space of padding on each
side of the longest line.

Widen the frame when a label does not fit - never steal the padding, and never let a label touch,
crowd, or overflow the border.

A frame's first content row is an empty line, so a label never sits directly under the top border.

A frame whose label is a single line also ends with one empty row.

Frames sharing one horizontal row may pad with trailing empty rows to keep their bottom borders
level.

Center every label horizontally inside the frame, placing the extra space on the right when the
padding cannot split evenly.

A label wrapped over several lines forms one block: indent every line to the same left column,
chosen so the longest line sits centered.

A label that stacks several distinct items keeps every item left-aligned with exactly one leading
space.

Do not enclose labels in brackets.

Write the label as plain text without `[..]`, `(..)`, or `{..}`.

Draw a horizontal edge as `─` filling the entire gap between two frames, with `>` touching the
target's left border - no space column between `>` and `│`, and no `>` floating inside the gap.

Draw a vertical edge as `│` rows on the center column of the frames it connects, ending with `v`
on the row directly above the target's top border, or with `^` on the row directly below the
target's bottom border for an upward flow.

When a flow fans out to several side-by-side frames, end the `│` drop in a junction row: `┌`
opens on the leftmost target's center column, `┐` closes on the rightmost, `┬` marks each inner
drop column, `┼` continues the source's center column, and `─` fills between the junction glyphs.

The row below the junction row carries one `v` on every drop column, directly above the target
top borders.

Every vertical drop and every `v` lands on the center column of the frame it enters - shift the
frame or re-space the junction row until they match.

Flow arrows (`─>`, `│`) must align with the center of the frame they connect to.

When placing a label above or below a horizontal arrow, the label row must span the exact same width
as the arrow row so the frames above and below remain aligned.

Before moving on, recount the columns: every `│` sits under its `╭` or `╮`, every `╰` and `╯`
closes under its side, every arrowhead touches or centers on its target, and no label touches a
border.

Anchor every node to a file or module.

## Design Patterns

Include this subsection only when the codebase exhibits recurring structure, per
`assessment/design-patterns.md`.

Present a table of the patterns in use with a fitness verdict, then describe each material pattern
or anti-pattern with evidence.

| Pattern        | Location                   | Assessment | Description                                      |
|----------------|----------------------------|------------|--------------------------------------------------|
| Repository     | `KnowledgeBase` trait      | PASS       | Clean abstraction with injectable implementation |
| Strategy       | hybrid search weighting    | PARTIAL    | Hardcoded, not runtime interchangeable           |
| Factory Method | `build_router` per handler | FAIL       | Duplicated construction logic, anti-pattern      |

Name patterns using their standard GoF or POSA names.

Cross-reference any anti-pattern that is also a code-origin signal to its `FND-AIP-XXX` finding.

## Architecture Decision Records

Include this subsection only when the system is production-bound with significant decisions, per the
ADR gap guidance in `assessment/change-management.md`.

Present a table of decisions that should carry an ADR, each marked `RECORDED` or `MISSING`, anchored
to the code that embodies the decision.

Name each decision by the artifact or mechanism it governs in a few words -
`Schema migration`, not `Automated schema migration` - manner qualifiers that state the obvious
only lengthen the label.

| Decision             | Location                  | ADR Status |
|----------------------|---------------------------|------------|
| Data store choice    | `Cargo.toml`, `src/db.rs` | MISSING    |
| Web framework choice | `Cargo.toml`              | MISSING    |
| Session state model  | `main.rs`                 | MISSING    |

Missing decision rationale limits confidence regardless of origin, do not infer AI authorship or
an AI default from absent ADRs.
