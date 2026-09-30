# Accessibility Baseline

## Purpose

> **Scope:** The source-inspectable subset of WCAG 2.2 and WAI-ARIA practice
> **Key items:** checkable conformance criteria, keyboard and focus rules, ARIA discipline,
> media and form requirements

This file distills the WCAG 2.2, WAI overview, ARIA Authoring Practices, and MDN sources
listed in `references/source-catalog.md` into the constraints an audit can verify from markup
and script source.

Snapshot date: 2026-09-30.

Screen-reader behavior and rendered contrast are not source-verifiable. This file covers only
what markup and scripts prove.

Feeds `assessment/best-practices.md` and the accessibility pillar of
`references/stacks/web.md` subjects.

## WCAG 2.2 Source-Inspectable Criteria

From https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/standards-guidelines/wcag/ -
the Level A/AA subset checkable from source.

- 1.1.1 Non-text Content: `<img>` needs `alt`. Decorative images use empty `alt=""`. Missing
  `alt` is a defect.
- 1.2.x Media: `<video>` carries `track kind="captions"`/`subtitles` for prerecorded
  audio content. `<audio>` equivalents for speech.
- 1.3.1 Info and Relationships: form controls have associated `<label>` or
  `aria-label`/`aria-labelledby`. `<table>` data cells associate via `<th>`/`scope`/`headers`.
- 1.4.1 Use of Color: color-only signals (red/green status without text or icon) are
  findings when visible in source.
- 2.1.x Keyboard: `tabindex`, `keydown`/`keyup` handlers, and no keyboard traps
  (`tabindex="-1"` containers that swallow focus). `onclick`-only divs with no keyboard path
  are defects.
- 2.4.x Navigable: `<title>` per page, visible focus indicator must not be removed
  (`outline: none` without an alternative), skip links for keyboard users when heavy nav
  precedes content.
- 3.1.1 Language of Page: `<html lang>` present (stack-level check in
  `references/stacks/web.md`).
- 3.3.x Input Assistance: error identification text near the field, `aria-invalid` +
  `aria-describedby` for programmatic association.
- 4.1.2 Name/Role/Value: custom controls expose name, role, and state - div-buttons without
  `role="button"`/`tabindex`/`aria-*` are defects.

## ARIA Discipline

From https://www.w3.org/WAI/ARIA/apg/.

- First rule of ARIA: use native HTML before ARIA. `role`/`aria-*` on elements that already
  carry the semantics (`<button role="button">`) is redundancy, on `div`+`onclick` it's the
  defect fix.
- `role="dialog"` needs `aria-modal`, focus management, and `aria-labelledby`. `role="alert"`
  announces without focus.
- ARIA must not conflict with native semantics (`<a href>` gets no `role="button"` need).
  hidden content (`display:none`) must not carry ARIA-focusable children.
- `aria-live` regions announce async updates. Their absence on status feeds is an
  observation, their misuse (live on rapidly-changing regions) is too.

## MDN Practical Anchors

From https://developer.mozilla.org/en-US/docs/Web/Accessibility.

- Focus order follows DOM order. Reordering with CSS `order`/`float` while DOM order differs
  creates a focus/source mismatch.
- `prefers-reduced-motion` media query is the vestibular-safety hook. Animations that ignore
  it are an observation.
- Touch targets and `pointer` events need pointer-type alternatives beyond hover-only
  interaction.

## Live Check

When web fetch is available, spot-check one criterion number against the WCAG 2.2 text and one
pattern name against the ARIA APG.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
