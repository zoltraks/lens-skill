# UI Automation Baseline

## Purpose

> **Scope:** Checkable constraints for software that drives or inspects an application a human
> user may be operating at the same time
> **Key items:** control-channel selection, read-only contract, live-user cohabitation, state
> detection, bounded enumeration, calibration discipline

This file distills the Microsoft UI Automation documentation, W3C WebDriver, the ARIA
Authoring Practices Guide, the Chromium and Gecko accessibility architecture documents, and
AT-SPI listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md` and `assessment/best-practices.md` for subjects
classified `automation` in `references/domain-profiles.md`.

## Control Channel Selection

From https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview and
https://w3c.github.io/webdriver/.

- Channels rank by fidelity and fragility: the application's object model or API first, then
  its accessibility tree, then a protocol surface (URI scheme, debugging protocol), then file
  or data exchange, with synthetic input (keys and mouse) and visual capture as last resorts.
- A project that drops a level records the reason. Synthetic input is always state-changing
  and can never be the silent default - visual matching is legitimate only when no semantic
  channel exists, and then it is the channel, not a fallback.
- Channels compose - a reader may use an object model where it exists and fall back to the
  accessibility tree elsewhere - but a single operation never switches channels mid-flight
  without a recorded reason.

## Read-Only And Declared-Effects Contracts

- An inspection utility's read path never invokes, clicks, types, focuses, or otherwise
  mutates the target. Every state-changing operation sits behind an explicit, self-describing
  opt-in (a flag, a dedicated command form) that help text discloses.
- An execution utility performs exactly what its scenario declares and stops on failure by
  default - continue-on-error exists only as an explicit option.
- Every tolerated side effect - launching the target, restoring a window, switching a view,
  filling a search box - emits a warning on the diagnostics channel, never the payload stream.
- Degradation carries data, not silence: unreachable content yields what was obtained plus a
  warning, and an item blocked by security controls lands as a per-item marker plus one
  summary warning rather than failing the run.

## State Detection

- Prefer stable anchors over tree contents: window and document titles and URLs update before
  the accessibility subtree does, and browsers serve stale subtrees for tens of seconds after
  a view swap.
- Never drive state detection from signals that degrade under minimization - an
  `IsOffscreen`-style flag reports everything offscreen on a minimized window.
- Confirm actions by observable effect, not by return value: an invoke or scroll can report
  success while nothing happens, so verification polls a title, document name, or rendered
  change.
- Elements are volatile: re-resolve on each poll round rather than caching, and treat a dead
  element as absent rather than fatal.
- For pixel-channel tools, anchors are captured from the real target at real DPI and locale,
  never synthesized, and the match threshold is a deliberate per-step setting.

## Bounded Enumeration And Virtualization

- Every enumeration is capped by a named element bound and every wait by a named timeout, and a
  bounded walk that stops early reports `truncated` instead of implying completeness.
- Virtualized lists render only the visible window: the total count lives in container text,
  paging works through edge-row scroll-into-view rather than scrolling already-rendered items,
  and a walk goes to the head before paging down because the app preserves scroll position.
- The working scroller is found by verification - scroll each candidate and keep the one that
  changes rendered rows - because framework lists expose scroll surfaces outside the grid's
  ancestry.
- Flattened virtualized trees rebuild hierarchy from `aria-level`, position metadata, or
  automation-id paths, never from parentage.
- Prefer the target's own search or filter when one exists: a filled field replaces a paging
  loop and survives virtualization.

## Machine-Generated Text

- Accessible names and rendered labels are a localized wire format. Parsers are pure functions
  over captured text, backed by verbatim fixtures harvested from the live target - a heuristic
  written against invented strings ships defects.
- Locale markers live in label tables so a new language is a table edit. Prefixes are stripped
  only where the source shape guarantees decoration, separators match literally, and the
  untransformed value survives in a raw field when parsing is partial.
- Third-party software injects markers into accessible text - known injected prefixes are
  stripped and the mutation warned.
- Display names are not keys where the domain permits duplicates: match on name plus a second
  observable field and report surviving ambiguity instead of picking the first row.

## Platform Boundaries

- Desktop automation requires an interactive session, and a service context has no user desktop.
  Integrity-level isolation blocks input from a lower-privilege process to an elevated window -
  a security boundary to design around, not a bug to bypass.
- Window messages to a foreign window must be bounded (`SendMessageTimeout`-class calls), and
  only documented system messages cross processes - control-specific messages can desync or
  crash toolkits that mirror item state.
- Lazy accessibility trees materialize on probe: an empty pane chain means "not activated", not
  "empty", and a sleeping tab exposes no document while its title persists.
- A quit message is a request, not a death certificate - verify the process exited within a
  bound before claiming termination.

## Calibration And Verification

- Calibration precedes implementation: dump the real tree or capture real anchors, pin
  representative names verbatim into fixtures, write the pure parser, then the provider, then
  smoke against the live application, then record target quirks in a calibration reference.
- Providers are verified by live smoke runs - a mocked tree cannot reproduce platform quirks -
  while parsers are unit-testable precisely because parsing is separated from walking.
- A regression earns a verbatim-fixture test before the fix counts as done, and a diff review
  checks that no read path gained an invoke, click, or focus call outside an opt-in.

## Live Check

When web fetch is available, spot-check one control pattern or object identifier against the
UIA documentation and one interactability claim against the WebDriver specification.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
