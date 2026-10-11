#!/usr/bin/env python3
"""Shared helpers for Lens skill-maintenance tools.

Imported by ``validate-skill.py``, ``check-references.py``, and
``check-contents.py``, which always run inside the Lens repository.

Report-production tools (``format-table.py``, ``validate-report.py``) must
stay self-contained: they are copied into audited repositories under a
``.tmp.`` name where this module is not available.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path


def gitignore_patterns(root: Path) -> list[str]:
    patterns: list[str] = []
    ignore_file = root / ".gitignore"
    if not ignore_file.is_file():
        return patterns
    for raw in ignore_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith(("#", "!")):
            patterns.append(line)
    return patterns


def is_ignored(relative: Path, patterns: list[str]) -> bool:
    parts = relative.parts
    posix = relative.as_posix()
    for pattern in patterns:
        anchored = pattern.startswith("/")
        bare = pattern.rstrip("/").lstrip("/")
        if not bare:
            continue
        if "/" in bare:
            if anchored:
                matched = posix == bare or posix.startswith(bare + "/")
            else:
                matched = fnmatch.fnmatch(posix, bare) or fnmatch.fnmatch(posix, bare + "/*")
        elif anchored:
            matched = fnmatch.fnmatch(parts[0], bare)
        else:
            matched = any(fnmatch.fnmatch(part, bare) for part in parts)
        if matched:
            return True
    return False


def resource_files(root: Path, suffix: str) -> list[Path]:
    """Return non-ignored files with the given suffix, honoring the root .gitignore."""
    patterns = gitignore_patterns(root)
    return [
        path
        for path in sorted(root.rglob(f"*{suffix}"))
        if ".git" not in path.parts and not is_ignored(path.relative_to(root), patterns)
    ]


def markdown_files(root: Path) -> list[Path]:
    """Return non-ignored Markdown files under root, honoring the root .gitignore."""
    return resource_files(root, ".md")


def parse_frontmatter(text: str, issues: list[str]) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        issues.append("SKILL.md has no YAML frontmatter block")
        return {}, text

    raw = match.group(1).splitlines()
    fields: dict[str, str] = {}
    index = 0
    while index < len(raw):
        line = raw[index]
        if line.startswith("  "):
            index += 1
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        field_match = re.match(r"^([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?$", line)
        if not field_match:
            issues.append(f"frontmatter line {index + 1} is not a simple field: {line}")
            index += 1
            continue
        key, value = field_match.group(1), field_match.group(2) or ""
        if value in {">-", ">", "|-", "|"}:
            parts: list[str] = []
            index += 1
            while index < len(raw) and (raw[index].startswith("  ") or not raw[index].strip()):
                parts.append(raw[index][2:] if raw[index].startswith("  ") else "")
                index += 1
            separator = " " if value.startswith(">") else "\n"
            fields[key] = separator.join(parts).strip()
            continue
        fields[key] = value.strip().strip('"').strip("'")
        index += 1
    return fields, text[match.end():]


def report(issues: list[str], pass_message: str) -> int:
    """Print FAIL lines or a PASS line and return the exit code."""
    if issues:
        for message in issues:
            print(f"FAIL {message}")
        print(f"{len(issues)} issue(s) found")
        return 1
    print(f"PASS {pass_message}")
    return 0
