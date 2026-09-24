# License Compliance Checklist

## Purpose

> **Scope:** Classifying component licenses from inspected declarations and detecting
> copyleft-versus-distribution conflicts
> **Key items:** license classes, declaration sources, copyleft trap, Unknown handling

This file defines the license-classification pass that runs over the SBOM table
(`references/sbom-schema.md`) and feeds the License & IP Compliance Review section and
`assessment/copyright-review.md` findings.

Apply `principles/evaluation-rules.md` throughout. Only inspected declarations count as license
evidence. Knowing what license a popular package usually carries is not evidence, mark `Unknown`
instead.

## License Classes

Every component in the SBOM table receives exactly one class:

| Class             | Includes                                                               |
|-------------------|------------------------------------------------------------------------|
| `Permissive`      | MIT, BSD-2/3-Clause, ISC, Apache-2.0, Zlib, Unlicense, CC0             |
| `Weak-copyleft`   | LGPL, MPL-2.0, EPL, CDDL                                               |
| `Strong-copyleft` | GPL, AGPL, SSPL                                                        |
| `Proprietary`     | Commercial or custom restrictive terms, license files forbidding reuse |
| `Unknown`         | No inspected declaration                                               |

An SPDX expression resolves to the strictest class it contains: `MIT OR GPL-3.0` is treated as
`Strong-copyleft` until the project's chosen option is documented.

## Declaration Sources

Checked in this order, first inspected declaration wins:

1. A `license` or `licenses` field in the component's own manifest or package metadata committed
   to the repository.
2. A `LICENSE`, `COPYING`, or `NOTICE` file inside the component's vendored or downloaded tree.
3. A lockfile license field, in the rare formats that carry one.
4. Project-level license-policy documents that name the component's license explicitly.

Nothing else counts. Absence of a declaration produces `Unknown`, not a best guess.

## The Copyleft Trap

The finding most likely to force legal remediation is a strong-copyleft component linked into a
work distributed under incompatible terms. Flag a `Conflict` when all of these hold:

- The component classifies as `Strong-copyleft`.
- It is a `direct` or statically linked `transitive` component of the distributed work.
- The project's own license or stated distribution model is proprietary or otherwise
  incompatible with the copyleft terms.

A `Conflict` always produces an `FND-CPR` finding naming the component, its license, the
project's license, and the linkage evidence.

Flag `Review` for weak-copyleft components where the linkage mode is undetermined, for dual or
unusual licenses, and for `Proprietary` third-party code. Flag `Unknown` where no declaration was
found.

## Rules

- License classification runs over every SBOM row, not a sample.
- Undeterminable licenses are a finding input themselves: a high `Unknown` count means the project
  cannot demonstrate license hygiene to a reviewer.
- The audit makes no legal determination. Findings describe the conflict mechanics and cite the
  declarations, remediation owners decide.
- Distinguish declared licenses, observed notices, and reviewed conclusions for the distribution
  model, per `assessment/copyright-review.md`.
