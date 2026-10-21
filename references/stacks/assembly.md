# Assembly Baseline

## Purpose

> **Scope:** Checkable constraints for assembly-language source partitions and projects
> **Key items:** file and include conventions, label and equate naming per dialect, routine
> contracts, memory-map documentation, terse-name temperament

This file distills the DASM user guide and the ca65 users guide listed in
`references/source-catalog.md`, plus the assembly row of `references/language-conventions.md`,
into constraints an audit can verify from repository source.

Snapshot date: 2026-10-21.

Feeds `assessment/structure-review.md`, `assessment/code-style.md`, and
`assessment/baseline-conformance.md` for subjects with assembly partitions, including
documentation projects whose fenced examples follow an assembly standard.

## Naming And Layout

From https://dasm-assembler.github.io/ (the DASM user guide,
https://github.com/dasm-assembler/dasm) and https://cc65.github.io/doc/ca65.html.

- Source files use the assembler's own extension set: `.asm`/`.s` for translation units,
  `.inc`/`.mac` for include files holding constants, macros, and data tables. A build entry
  file (`main.asm`, `boot.asm`, or the target's conventional name) assembles the rest through
  `.include`/`.incbin` directives.
- One file per module or address segment: code, data tables, equate blocks, and machine
  definitions split along hardware or build boundaries rather than by declaration count.
- Label casing is dialect- and project-specific and none is universally wrong: `snake_case`,
  `lowercase`, and `camelCase` labels all appear in shipped codebases, and the dominant shape
  inside the partition is the working yardstick. Mixed label families within one file are the
  consistency defect, not the chosen shape.
- Equates and address constants are conventionally `UPPER_SNAKE_CASE` (`SCREEN = $8000`,
  `KERNAL_CHROUT = $FFD2`) across dialects, and machine-register or hardware names keep their
  canonical form (`VIA_PCR`, `PIA1_PORTA`).
- Local labels use the dialect's own scoping syntax and stay terse: DASM accepts `.`-prefixed
  and `name.local` forms, ca65 offers `.proc`-scoped labels, `@`-cheap locals, and `:`
  unnamed labels for tight loops - flagging a `.loop` or `@done` as a noise name is a false
  positive.
- Mnemonic case is a project choice (`lda` versus `LDA`) and must be uniform within a file.
  Directive case (`processor`, `org`, `.byte`, `.INCLUDE`) follows the assembler's documented
  form.

## Readability Levers

- Terse names are idiomatic in assembly: a one-word label naming a hardware address, a jump
  target, or a loop point is acceptable where a higher-level language would want a phrase.
  Readability evidence is structural, not name length.
- Routine contracts are the comprehension aid: entry routines carry a header comment naming
  inputs, outputs, and clobbered registers (`; in: X=len  out: A=status  clobbers: Y`), and
  undocumented leaf calls are an observation only when the surrounding convention documents
  them.
- Named constants replace magic numbers: raw addresses inside instructions (`lda $e810`)
  are a finding when the same address exists as an equate elsewhere in the project, and a
  memory-map table or equates file is strong positive evidence.
- Dynamic alignment of equate columns and comment tab-stops is a common documented style,
  and the yardstick stays the convention the partition declares or practices consistently.

## Live Check

When web fetch is available, verify the dialect's label and directive forms against the
assembler's own manual for the toolchain the subject uses, and record the drift window.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
