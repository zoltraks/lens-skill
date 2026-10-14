"""Finalize a Lens audit report in one command.

Runs the report-production tools in their required order:
``link-glossary.py`` inserts glossary body links, ``link-references.py``
links register identifiers to their definitions, ``format-table.py``
reformats tables, ``validate-report.py`` performs the structural check.
The ordering constraint is enforced here rather than remembered.

Copy into the audited repository's report-production directory as
``finalize-report.tmp.py`` next to the other ``.tmp.`` tool copies;
the script locates its siblings by filename. When the copies are absent, pass
``--skill-root <path>`` (or set ``LENS_SKILL_ROOT``) pointing at the skill
repository so the tools are found in its ``scripts/`` directory instead.

Usage: python finalize-report.py [--polish] [--skill-root <dir>] <report.md>
``--polish`` runs the translated-report gates instead of the English
validator: ``link-glossary.py --lang pl``, ``lint-polish.py --rules``,
``check-translation.py``, then ``map-translation.py`` and the
formatter+validator on the mapped copy, which is removed after a pass.
Exit code 0 means formatting, linting, and validation all pass.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def candidates(directory: Path, base: str) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        candidate
        for candidate in directory.glob(f"*{base}*.py")
        if candidate.resolve() != Path(__file__).resolve()
    )


def locate(directory: Path, base: str, skill_root: Path | None) -> Path:
    matches = candidates(directory, base)
    fallback = ""
    if len(matches) != 1 and skill_root is not None:
        for probe in (skill_root / "scripts", skill_root):
            matches = candidates(probe, base)
            if len(matches) == 1:
                return matches[0]
        fallback = f" or under {skill_root}"
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly one *{base}*.py copy next to {Path(__file__).name}"
            f"{fallback}, found {len(matches)}"
        )
    return matches[0]


def run(tool: Path, target: Path, extra: list[str] | None = None) -> int:
    print(f"--- {tool.name}", flush=True)
    completed = subprocess.run(
        [sys.executable, str(tool), str(target), *(extra or [])],
        check=False,
    )
    return completed.returncode


def polish_rules(skill_root: Path | None) -> Path | None:
    """Locate `translations/polish-language.md` for the `--polish` lint -
    a `.tmp.` copy cannot resolve it relative to its own path."""
    for probe in (skill_root, Path(__file__).resolve().parent.parent):
        if probe is None:
            continue
        candidate = probe / "translations" / "polish-language.md"
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str]) -> int:
    arguments: list[str] = []
    skill_root: Path | None = None
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument == "--skill-root":
            index += 1
            if index >= len(argv):
                print("--skill-root needs a directory")
                return 1
            skill_root = Path(argv[index])
        elif argument.startswith("-"):
            pass
        else:
            arguments.append(argument)
        index += 1
    polish = "--polish" in argv[1:]
    if skill_root is None and os.environ.get("LENS_SKILL_ROOT"):
        skill_root = Path(os.environ["LENS_SKILL_ROOT"])
    if len(arguments) != 1:
        print(
            "Usage: python finalize-report.py [--polish] [--skill-root <dir>] <report.md>"
        )
        return 1
    target = Path(arguments[0])
    if not target.is_file():
        print(f"report not found: {target}")
        return 1
    directory = Path(__file__).resolve().parent
    glossary = locate(directory, "link-glossary", skill_root)
    references = locate(directory, "link-references", skill_root)
    formatter = locate(directory, "format-table", skill_root)
    if not polish:
        steps = [
            (glossary, target, []),
            (references, target, []),
            (formatter, target, []),
            (locate(directory, "validate-report", skill_root), target, []),
        ]
    else:
        rules = polish_rules(skill_root)
        rules_arg = ["--rules", str(rules)] if rules is not None else []
        # The pair contract names the English sibling `*-EN.md`; pass it for
        # positional heading parity when it exists.
        map_arg = list(rules_arg)
        if target.stem.endswith("-PL"):
            sibling = target.with_name(target.stem[:-3] + "-EN.md")
            if sibling.is_file():
                map_arg += ["--en", str(sibling)]
        mapped = target.with_name(target.stem + "-en-mapped.tmp.md")
        steps = [
            (glossary, target, ["--lang", "pl"]),
            (references, target, []),
            (formatter, target, []),
            (locate(directory, "lint-polish", skill_root), target, rules_arg),
            (locate(directory, "check-translation", skill_root), target, rules_arg),
            (
                locate(directory, "map-translation", skill_root),
                target,
                map_arg,
            ),
            (formatter, mapped, []),
            (locate(directory, "validate-report", skill_root), mapped, []),
        ]
    for tool, step_target, extra in steps:
        result = run(tool, step_target, extra)
        if result != 0:
            print(f"STOP {tool.name} reported failures")
            return result
    if polish and mapped.exists():
        mapped.unlink()
    print(f"PASS {target.name} finalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
