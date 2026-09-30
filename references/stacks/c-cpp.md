# C And C++ Baseline

## Purpose

> **Scope:** Checkable constraints for C and C++ codebases
> **Key items:** C++ Core Guidelines enforceable subset, CERT rule-ID anchors, memory-safety
> and UB review classes

This file distills the C++ Core Guidelines and CERT coding-standard anchors listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

The CERT Coding Standards (SEI) are license-restricted: only rule identifiers and public rule
titles are distilled here, never rule text.

Feeds `assessment/code-quality.md` and `assessment/security-review.md` for native-code
subjects.

## C++ Core Guidelines

From https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines - the mechanically checkable
subset.

- Prefer RAII resource handles over `new`/`delete`: naked `new`/`delete` pairs, `malloc`/`free`
  in C++, and manual ownership are findings (R.11, R.20-R.24).
- `gsl::span`, `string_view`, `unique_ptr`, `shared_ptr`, `weak_ptr` express ownership.
  raw pointers passed across APIs need a stated ownership contract (F.7, I.11).
- Bounds: `at()`, spans, or checked indexing over `operator[]` on untrusted lengths. C-style
  arrays and pointer arithmetic on buffer boundaries are review classes (SL.con, ES.42).
- `const` correctness, `noexcept` on non-throwing moves, and `override` on every virtual
  override are checkable (Con.4, C.128).
- No C-style casts. `static_cast`/`reinterpret_cast`/`const_cast` each carry different risk
  and `reinterpret_cast` is a red-flag token (ES.48-50).
- Compiler warnings as errors (`-Wall -Wextra -Werror`, `/W4 /WX`) are the analysis floor.
  absent warning flags in build config are an observation.

## CERT Anchors

From https://wiki.sei.cmu.edu/confluence/display/c and the C++ space - rule IDs and public
names only.

- C anchor families: `INT30-INT36` integer overflow/UB, `ARR30-ARR39` array bounds,
  `STR30-STR38` string handling, `MEM30-MEM36` memory management, `MSC30-MSC42` miscellaneous
  (RNG, undefined behavior), `SIG30-SIG35` signal safety, `CON30-CON43` concurrency.
- C++ anchor families: `CTR50-CTR59` containers, `EXP50-EXP63` expressions/UB,
  `MEM50-MEM57` memory, `OOP50-OOP58` object model, `ERR50-ERR62` exceptions.
- Use the ID and public title in findings. Cite the rule number, not paraphrased rule text.

## Review Classes

Checkable patterns independent of either source:

- Unsafe string APIs: `strcpy`, `strcat`, `sprintf`, `gets` (removed in C11+). Bounded
  variants still need length-derivation review.
- Format strings: `printf(user)` where user input reaches the format parameter is a finding.
- `sizeof` on pointers, `memcpy` with computed lengths, integer overflow feeding allocations,
  and `signed`/`unsigned` comparisons on bounds are the classic defect surface.
- Sanitizer configuration in CI (`-fsanitize=address,undefined`, ASan/UBSan/MSan) is the
  strongest mechanical signal. Absence is not a defect but means memory-safety claims rest on
  review alone.

## Live Check

When web fetch is available, verify one Core Guidelines rule number against
isocpp.github.io and confirm the CERT rule-ID family letters against the SEI index.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
