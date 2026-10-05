"""Finalize a Lens audit report in one command.

Runs the report-production tools in their required order:
``link-glossary.py`` inserts glossary body links, ``format-table.py``
reformats tables, ``validate-report.py`` performs the structural check.
The ordering constraint is enforced here rather than remembered.

Copy into the audited repository's report-production directory as
``finalize-report.tmp.py`` next to the other ``.tmp.`` tool copies;
the script locates its siblings by filename. When the copies are absent, pass
``--skill-root <path>`` (or set ``LENS_SKILL_ROOT``) pointing at the skill
repository so the tools are found in its ``scripts/`` directory instead.

Usage: python finalize-report.py [--polish] [--skill-root <dir>] <report.md>
``--polish`` additionally runs ``lint-polish.py`` before validation.
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


def run(tool: Path, target: Path) -> int:
    print(f"--- {tool.name}", flush=True)
    completed = subprocess.run([sys.executable, str(tool), str(target)], check=False)
    return completed.returncode


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
    steps = [
        locate(directory, "link-glossary", skill_root),
        locate(directory, "format-table", skill_root),
    ]
    if polish:
        steps.append(locate(directory, "lint-polish", skill_root))
    steps.append(locate(directory, "validate-report", skill_root))
    for tool in steps:
        result = run(tool, target)
        if result != 0:
            print(f"STOP {tool.name} reported failures")
            return result
    print(f"PASS {target.name} finalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
