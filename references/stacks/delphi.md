# Delphi, Free Pascal, And Object Pascal Baseline

## Purpose

> **Scope:** Checkable constraints for Delphi and Free Pascal (Object Pascal) projects
> **Key items:** naming and layout conventions, Free Pascal vs Delphi unit naming,
> memory-management model, project file structure, restricted-source handling

This file distills the Embarcadero Object Pascal style guide, Free Pascal reference guide, and
DocWiki anchors listed in `references/source-catalog.md` into constraints an audit can verify
from repository source.

Snapshot date: 2026-09-30.

The DocWiki index (docwiki.embarcadero.com) was unreachable at snapshot time.

This file keeps
the stable conventions distilled from the Embarcadero style guide, Free Pascal documentation,
and ecosystem practice.

Feeds `assessment/best-practices.md`, `assessment/structure-review.md`,
`assessment/code-quality.md`, and `assessment/baseline-conformance.md` for Object Pascal
subjects.

## Naming, Code Division, And Layout

From https://edn.embarcadero.com/article/10280 (the classic Object Pascal style guide) and
https://www.freepascal.org/docs-html/ref/ref.html.

- Type and member prefixes: classes, records, and enums are `T`-prefixed (`TOrder`,
  `TOrderStatus`, `TOrderService`), exception classes `E`-prefixed (`EOrderNotFound`),
  reference-counted interfaces `I`-prefixed (`IOrderRepository`), private class fields
  `F`-prefixed (`FOrders`, `FRepository`), parameters `A`-prefixed (`ACustomerEmail`), and enum
  values prefixed with lowercase type initials (`osPending`, `osPaid`, `osCancelled`).
- Method naming: methods and functions use `PascalCase`. Because `Create` is the standard
  constructor name on `TObject`, domain creation methods on services use a qualified name such
  as `CreateOrder` rather than shadowing `Create`.
- Delphi versus Free Pascal unit layout:
  - **Delphi 11/12** uses dotted `PascalCase` unit filenames (`src/OrderApp.Domain.Order.pas`,
    `src/OrderApp.Services.OrderService.pas`) paired with `.dpr` and `.dproj` project files and
    `tests/*.Tests.*.pas` DUnitX fixtures.
  - **Free Pascal 3.2+** uses lowercase unit filenames matching the `unit` identifier
    (`src/orderdomain.pas`, `src/orderservice.pas`, `{$mode objfpc}{$H+}`) paired with `.lpr`
    (and optional Lazarus `.lpi`) project files and `tests/test*.pas` `fpcunit` runners.
- Each unit strictly divides public declarations in the `interface` section from private
  helpers and bodies in `implementation`, keeping `uses` clauses scoped to the section that
  needs them.
- Indentation is two spaces, `begin`/`end` aligned, `procedure`/`function` signatures
  capitalized per convention.
- `.dpr` (project) and `.dproj` (MSBuild XML) files carry build configuration. `.dfm`/` .fmx`
  pairs hold form layout - missing pairs or orphaned units are structural findings.

## Memory And Resource Model

- `try/finally` protects every heap allocation: `Create` followed by `Free` in a `finally`
  block is the ownership idiom. Leaked objects are the classic defect class.
- Interfaces (`TInterfacedObject`) give reference counting. Mixing interface and object
  references to the same instance double-frees.
- `FreeAndNil` for reusable fields, `Assigned()` checks before dereference, and `nil` cleanup
  in destructors are the checkable patterns.
- Strings and dynamic arrays are managed types. Manual `SetLength` + pointer arithmetic is
  a review surface.

## Project Hygiene

- `ProjectOptions`/`dproj` `UseDebugDCUs`, optimization, and range/overflow checking flags
  (`$R+`, `$Q+`, `$O+/-`) differ between Debug and Release. Shipping a Debug-configured build
  is a finding.
- Third-party units under `vendor/`-style paths should carry license notices. Delphi
  redistributable units have their own terms.
- `resourcestring` for user-visible text is the localization-ready convention.

## UI And Threading Rules

- VCL controls are main-thread only. `TThread.Synchronize`/`Queue` is the checkable boundary -
  direct VCL access from a worker thread is a defect.
- `Application.ProcessMessages` inside a loop is a reentrancy hazard - a real wait uses
  `WaitFor`-style blocking or a message-driven design.
- `with` blocks hide identifier scope - on any block longer than a couple of lines they are a
  maintainability finding.
- Empty `except` blocks swallow every exception including `EOutOfMemory` - an `except` that
  does not re-raise or handle narrowly is a defect.
- Form units hold event wiring only: business logic inside `.dfm`-paired units couples
  behavior to the designer surface and is untestable.

## Database And Tests

- FireDAC pooled connections and explicit transactions are the checkable shape - a
  `TFDConnection` opened per query or SQL built with `Format` interpolation is a finding.
- DUnitX (`TDUnitX`) is the conventional test harness - a test project referencing it
  satisfies the "has tests" floor for Delphi subjects.

## Live Check

When web fetch is available, attempt the DocWiki index.

When it blocks automated fetch, record
the attempt and use this snapshot plus the style-guide anchor.

Record whichever baseline the audit used, and note drift in Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
