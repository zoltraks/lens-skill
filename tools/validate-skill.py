#!/usr/bin/env python3
"""Validate Lens skill metadata, disclosure limits, and root references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REFERENCE_PATTERN = re.compile(r"(?<![A-Za-z0-9:/])([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+\.(?:md|py|json|txt))(?![A-Za-z0-9])")
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")


def issue(message: str, issues: list[str]) -> None:
    issues.append(message)


def parse_frontmatter(text: str, issues: list[str]) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        issue("SKILL.md has no YAML frontmatter block", issues)
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
            issue(f"frontmatter line {index + 1} is not a simple field: {line}", issues)
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


def validate_frontmatter(root: Path, fields: dict[str, str], issues: list[str]) -> None:
    missing = {"name", "description"} - fields.keys()
    for key in sorted(missing):
        issue(f"frontmatter is missing required field: {key}", issues)

    unexpected = set(fields) - ALLOWED_FIELDS
    for key in sorted(unexpected):
        issue(f"frontmatter has unsupported top-level field: {key}", issues)

    name = fields.get("name", "")
    if name:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            issue("name must contain lowercase letters, digits, and single hyphens only", issues)
        if len(name) > 64:
            issue(f"name is {len(name)} characters, maximum is 64", issues)
        if name != root.name:
            issue(f"name {name!r} does not match directory {root.name!r}", issues)

    description = fields.get("description", "")
    if not description:
        issue("description must not be empty", issues)
    if len(description) > 1024:
        issue(f"description is {len(description)} characters, maximum is 1024", issues)
    if "<" in description or ">" in description:
        issue("description must not contain angle brackets", issues)

    compatibility = fields.get("compatibility", "")
    if compatibility and len(compatibility) > 500:
        issue(f"compatibility is {len(compatibility)} characters, maximum is 500", issues)


def referenced_paths(body: str) -> set[str]:
    references = set(REFERENCE_PATTERN.findall(body))
    references.update(
        match.group(1)
        for match in LINK_PATTERN.finditer(body)
        if not match.group(1).startswith(("http://", "https://", "#", "mailto:"))
    )
    return references


def validate_body(root: Path, body: str, issues: list[str]) -> None:
    lines = body.splitlines()
    total_lines = len((root / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if total_lines > 500:
        issue(f"SKILL.md is {total_lines} lines, maximum is 500", issues)

    for relative in sorted(referenced_paths(body)):
        candidate = Path(relative.replace("\\", "/"))
        if candidate.is_absolute() or ".." in candidate.parts:
            issue(f"root reference escapes the skill directory: {relative}", issues)
            continue
        if len(candidate.parts) > 3:
            issue(f"root reference is deeper than one resource directory: {relative}", issues)
        if not (root / candidate).is_file():
            issue(f"root reference does not resolve: {relative}", issues)

    for path in root.rglob("*.md"):
        if path == root / "SKILL.md":
            continue
        try:
            line_count = len(path.read_text(encoding="utf-8").splitlines())
        except UnicodeDecodeError:
            issue(f"Markdown file is not UTF-8: {path.relative_to(root)}", issues)
            continue
        if line_count > 300:
            content = path.read_text(encoding="utf-8")
            if "## Contents" not in content:
                issue(f"large document has no Contents section: {path.relative_to(root)}", issues)


def validate_evals(root: Path, fields: dict[str, str], issues: list[str]) -> None:
    evals_file = root / "evals" / "evals.json"
    if not evals_file.is_file():
        return
    try:
        data = json.loads(evals_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        issue(f"evals/evals.json is not valid JSON: {error}", issues)
        return
    if not isinstance(data, dict) or not isinstance(data.get("evals"), list):
        issue("evals/evals.json must contain an evals array", issues)
        return
    if data.get("skill_name") != fields.get("name"):
        issue("evals/evals.json skill_name does not match frontmatter name", issues)
    identifiers: set[int] = set()
    for position, item in enumerate(data["evals"], start=1):
        if not isinstance(item, dict):
            issue(f"eval {position} is not an object", issues)
            continue
        identifier = item.get("id")
        if not isinstance(identifier, int) or identifier in identifiers:
            issue(f"eval {position} has a missing or duplicate integer id", issues)
        else:
            identifiers.add(identifier)
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            issue(f"eval {position} has no prompt", issues)
        if not isinstance(item.get("expectations"), list) or not item["expectations"]:
            issue(f"eval {position} has no expectations", issues)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/validate-skill.py <skill-directory>")
        return 1

    root = Path(sys.argv[1]).resolve()
    skill_file = root / "SKILL.md"
    issues: list[str] = []
    if not root.is_dir():
        issue(f"skill directory does not exist: {root}", issues)
    if not skill_file.is_file():
        issue("SKILL.md is missing", issues)
    else:
        text = skill_file.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text, issues)
        validate_frontmatter(root, fields, issues)
        validate_body(root, body, issues)
        validate_evals(root, fields, issues)

    if issues:
        for message in issues:
            print(f"FAIL {message}")
        print(f"{len(issues)} issue(s) found")
        return 1

    print("PASS skill metadata, references, and disclosure limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
