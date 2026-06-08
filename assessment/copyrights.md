# Copyrights & Originality

## Purpose

> **Scope:** Verifying code originality, license compliance, and proper attribution of third-party code and assets
> **Key items:** original code, license headers, dependency licenses, copied snippets, attribution, binary asset rights

This file defines how to assess whether a codebase respects copyright and licensing rules. The assessment is based on the principle that all code should be original or properly licensed, and all third-party content should be documented.

Apply `principles/evaluation-rules.md` throughout. A finding of copied code is a copyright issue, not a code quality issue. Distinguish between legitimate use of open-source libraries (with proper licensing) and unauthorized copying of code snippets or assets.

## What To Look For

**Originality of source code**

- Identical or near-identical code blocks found in public repositories (StackOverflow, GitHub Gists, blog posts) without attribution.
- Files with copyright notices from other authors or organizations that do not match the project.
- Code comments that reference external sources ("from StackOverflow", "copied from X") without license documentation.
- Utility functions that are verbatim copies of well-known library implementations.
- Boilerplate files (license headers, standard config files) that are acceptable if they carry their own license.

**License headers and notices**

- Presence of a `LICENSE` or `COPYING` file at the repository root.
- Presence of license headers in individual source files.
- Consistency between the root license and the licenses of included third-party code.
- Missing license notices in files that contain third-party logic.

**Dependency license compatibility**

- All direct and transitive dependencies have documented licenses.
- No dependencies with licenses incompatible with the project's stated license (for example, GPL in a proprietary project).
- No dependencies with copyleft requirements that are not being honored.
- `SBOM` or `THIRD-PARTY-NOTICES` file present and current.

**Asset and binary rights**

- Images, fonts, icons, or media files without documented source or license.
- Embedded data files (JSON, XML, SQL dumps) from external sources without attribution.
- Certificate files, key files, or proprietary configuration formats that may carry their own licensing.

**Evidence of copying**

- Exact string matches to public code repositories.
- Identical variable names, structure, and comments in code that should be independent.
- Unusual file headers that reference external authors or projects not listed in dependencies.

## Checklist

**License documentation**

- [ ] Is a `LICENSE` file present at the repository root?
- [ ] Does the license match the project's stated ownership?
- [ ] Are license headers present in source files where required by the license?
- [ ] Is there a `NOTICE` or `THIRD-PARTY-NOTICES` file documenting third-party components?

**Code originality**

- [ ] Does the code contain blocks that appear to be copied from external sources without attribution?
- [ ] Are utility functions or algorithms documented as original or attributed?
- [ ] Are there any files with copyright notices from other authors not listed as contributors?

**Dependency compliance**

- [ ] Are all NuGet, npm, or other package dependencies licensed compatibly?
- [ ] Are transitive dependency licenses checked and documented?
- [ ] Is there an SBOM or lockfile that enables license auditing?

**Asset rights**

- [ ] Are all binary assets (images, media, data files) documented with source and license?
- [ ] Are there any assets that appear to be from external sources without permission?

## Status Markers

- `PASS`: All code is original or properly attributed. Licenses are documented, compatible, and complete. No unauthorized copying is evidenced.
- `PARTIAL`: Most code is original. Some minor attribution gaps exist, or some dependency licenses are not fully documented. No evidence of incompatible licenses.
- `FAIL`: Evidence of copied code without attribution, incompatible dependency licenses, or copyrighted material used without permission.
- `UNKNOWN`: The origin of key code blocks cannot be determined from the provided files.
- `N/A`: The system is a personal prototype with no stated intent for distribution or commercial use, and no third-party dependencies.

## Rules

- Do not accuse without evidence. A suspicion of copying is not a finding. Cite the specific file and the probable source.
- Distinguish between copying and legitimate inspiration. A reimplemented pattern with original code is not a copyright violation.
- When a dependency license is incompatible, state the specific dependency, its license, and the project's license so the conflict is clear.
- When marking `FAIL`, list the specific files or assets that violate copyright rules, not a general assertion.
- Never reproduce copyrighted code from external sources in the audit report, even as evidence. Describe the match in general terms.
- Respect fair-use and de minimis principles. Standard boilerplate (empty class templates, common regex patterns) is not a copyright concern.
