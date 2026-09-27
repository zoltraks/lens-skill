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

Use framed nodes with box-drawing characters for every DFD element.

Each frame must have exactly three content rows: an empty line, a centered label, and an empty line.

Set each frame's interior width to its longest label line plus exactly one space of padding on each
side.

A label must never touch, crowd, or overflow the frame border.

Keep exactly one space between the frame border and the label text on all sides.

Do not use two spaces or asymmetric padding.

Do not enclose labels in brackets.

Write the label as plain centered text without `[..]`, `(..)`, or `{..}`.

Flow arrows (`─>`, `│`) must align with the center of the frame they connect to.

When placing a label above or below a horizontal arrow, the label row must span the exact same width
as the arrow row so the frames above and below remain aligned.

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

Present a table of decisions that should carry an ADR, each marked `Recorded` or `Missing`, anchored
to the code that embodies the decision.

| Decision             | Location                  | ADR Status |
|----------------------|---------------------------|------------|
| Data store choice    | `Cargo.toml`, `src/db.rs` | Missing    |
| Web framework choice | `Cargo.toml`              | Missing    |
| Session state model  | `main.rs`                 | Missing    |

Missing decision rationale limits confidence regardless of origin, do not infer AI authorship or
an AI default from absent ADRs.
