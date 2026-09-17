#!/usr/bin/env python3
"""Check relative file references in Lens root navigation documents."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CODE_SPAN = re.compile(r"`([^`]+)`")
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
PATH_SUFFIX = re.compile(r"(?:\.md|\.py|\.json|\.txt)$", re.IGNORECASE)


def candidates(text: str) -> set[str]:
    values: set[str] = set()
    values.update(match.group(1) for match in CODE_SPAN.finditer(text))
    values.update(match.group(1) for match in MARKDOWN_LINK.finditer(text))
    return {
        value.strip()
        for value in values
        if PATH_SUFFIX.search(value.strip())
        and not value.strip().startswith(("http://", "https://", "mailto:", "#", "<"))
        and " " not in value.strip()
        and "<" not in value
        and ">" not in value
    }


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd().resolve()
    issues: list[str] = []
    for name in ("SKILL.md", "README.md"):
        source = root / name
        if not source.is_file():
            issues.append(f"missing navigation document: {name}")
            continue
        text = source.read_text(encoding="utf-8")
        for raw in sorted(candidates(text)):
            value = raw.split("#", 1)[0]
            if not value or value.startswith("<"):
                continue
            if source.name == "SKILL.md" and "/" not in value and not value.startswith("./"):
                continue
            candidate = (source.parent / value).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                issues.append(f"{name}: reference escapes skill directory: {raw}")
                continue
            if not candidate.is_file():
                issues.append(f"{name}: reference does not resolve: {raw}")

    if issues:
        for message in issues:
            print(f"FAIL {message}")
        print(f"{len(issues)} issue(s) found")
        return 1

    print("PASS root navigation references resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
