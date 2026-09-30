"""Finalize a Lens audit report in one command.

Runs the report-production tools in their required order:
``link-glossary.py`` inserts glossary body links, ``format-table.py``
reformats tables, ``validate-report.py`` performs the structural check.
The ordering constraint is enforced here rather than remembered.

Copy into the audited repository's report-production directory as
``finalize-report.tmp.py`` next to the other ``.tmp.`` tool copies;
the script locates its siblings by filename.

Usage: python finalize-report.py [--polish] <report.md>
``--polish`` additionally runs ``lint-polish.py`` before validation.
Exit code 0 means formatting, linting, and validation all pass.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def locate(directory: Path, base: str) -> Path:
    matches = sorted(
        candidate
        for candidate in directory.glob(f"*{base}*.py")
        if candidate.resolve() != Path(__file__).resolve()
    )
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly one *{base}*.py copy next to {Path(__file__).name},"
            f" found {len(matches)}"
        )
    return matches[0]


def run(tool: Path, target: Path) -> int:
    print(f"--- {tool.name}", flush=True)
    completed = subprocess.run([sys.executable, str(tool), str(target)], check=False)
    return completed.returncode


def main(argv: list[str]) -> int:
    arguments = [argument for argument in argv[1:] if not argument.startswith("-")]
    polish = "--polish" in argv[1:]
    if len(arguments) != 1:
        print("Usage: python finalize-report.py [--polish] <report.md>")
        return 1
    target = Path(arguments[0])
    if not target.is_file():
        print(f"report not found: {target}")
        return 1
    directory = Path(__file__).resolve().parent
    steps = [locate(directory, "link-glossary"), locate(directory, "format-table")]
    if polish:
        steps.append(locate(directory, "lint-polish"))
    steps.append(locate(directory, "validate-report"))
    for tool in steps:
        result = run(tool, target)
        if result != 0:
            print(f"STOP {tool.name} reported failures")
            return result
    print(f"PASS {target.name} finalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
