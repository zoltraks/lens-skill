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

Usage: python finalize-report.py [--polish] [--skill-root <dir>]
     [--model <audit-model.json>] [--state <audit-state.json>] <report.md>
``--gate`` runs the delivery battery after the standard steps - model
parity, declared-artifact reconciliation, git-status parity, and the
timing placeholder check - then prints DELIVERY READY or NOT READY.

``--polish`` runs the translated-report gates instead of the English
validator: ``link-glossary.py --lang pl``, ``lint-polish.py --rules``,
``check-translation.py``, then ``map-translation.py`` and the
formatter+validator on the mapped copy, which is removed after a pass.
``--model`` and ``--state`` pass through to every ``validate-report.py``
invocation for the report-versus-model and run-state consistency checks.
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


def repo_root(path: Path) -> Path | None:
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
    )
    return Path(probe.stdout.strip()) if probe.returncode == 0 else None


def run_gate(
    target: Path,
    model: str | None,
    state: str | None,
    directory: Path,
    skill_root: Path | None,
) -> int:
    """Delivery battery - each check prints a verdict line, then one final
    DELIVERY READY / DELIVERY NOT READY summary."""
    failures = 0
    lines: list[str] = []

    if model is None:
        lines.append("GATE model: SKIPPED (no --model)")
    else:
        result = run(locate(directory, "check-model", skill_root),
                     Path(model), [])
        lines.append(f"GATE model: {'PASS' if result == 0 else 'FAIL'}")
        failures += result != 0

    if state is None:
        lines.append("GATE artifacts: SKIPPED (no --state)")
    else:
        missing: list[str] = []
        try:
            import json
            declared = json.loads(Path(state).read_text()).get("artifacts", [])
        except Exception as exc:
            lines.append(f"GATE artifacts: FAIL ({exc})")
            declared = []
            failures += 1
        for entry in declared:
            path = Path(entry.get("path", ""))
            if not path.exists():
                missing.append(
                    f"{path} ({entry.get('kind','?')}, declared in "
                    f"{entry.get('declared_phase','?')})"
                )
        if missing:
            lines.append("GATE artifacts: FAIL")
            lines += [f"  Missing artifacts: {name}" for name in missing]
            failures += 1
        else:
            lines.append("GATE artifacts: PASS")

    root = repo_root(target.resolve().parent)
    if root is None:
        lines.append("GATE git parity: SKIPPED (not a git repository)")
    else:
        probe = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True, text=True, check=False,
        )
        expected = str(target.resolve().relative_to(root))
        unexpected = [
            line[3:].strip()
            for line in probe.stdout.splitlines()
            if line[3:].strip() != expected
            and not line[3:].strip().startswith("work/")
        ]
        if unexpected:
            lines.append("GATE git parity: WARN")
            lines += [f"  unexpected tree entry: {entry}" for entry in unexpected]
        else:
            lines.append("GATE git parity: PASS")

    if "TT:TT" in target.read_text(encoding="utf-8", errors="replace"):
        lines.append("GATE timing: FAIL (Time taken still TT:TT)")
        failures += 1
    else:
        lines.append("GATE timing: PASS")

    print("\n".join(lines))
    verdict = "DELIVERY READY" if failures == 0 else "DELIVERY NOT READY"
    if failures == 0 and model is None:
        verdict += " (reduced scope - no model parity)"
    print(verdict)
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    arguments: list[str] = []
    skill_root: Path | None = None
    model: str | None = None
    state: str | None = None
    index = 1
    while index < len(argv):
        argument = argv[index]
        if argument in ("--skill-root", "--model", "--state"):
            index += 1
            if index >= len(argv):
                print(f"{argument} needs a path")
                return 1
            if argument == "--skill-root":
                skill_root = Path(argv[index])
            elif argument == "--model":
                model = argv[index]
            else:
                state = argv[index]
        elif argument.startswith("-"):
            pass
        else:
            arguments.append(argument)
        index += 1
    polish = "--polish" in argv[1:]
    gate = "--gate" in argv[1:]
    if gate and polish:
        print("--gate does not apply to the polish path")
        return 1
    if skill_root is None and os.environ.get("LENS_SKILL_ROOT"):
        skill_root = Path(os.environ["LENS_SKILL_ROOT"])
    if len(arguments) != 1:
        print(
            "Usage: python finalize-report.py [--polish] [--gate] [--skill-root <dir>] "
            "[--model <audit-model.json>] [--state <audit-state.json>] <report.md>"
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
    validate_args: list[str] = []
    if model is not None:
        validate_args += ["--model", model]
    if state is not None:
        validate_args += ["--state", state]
    if not polish:
        steps = [
            (glossary, target, []),
            (references, target, []),
            (formatter, target, []),
            (locate(directory, "validate-report", skill_root), target, validate_args),
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
            (locate(directory, "validate-report", skill_root), mapped, validate_args),
        ]
    for tool, step_target, extra in steps:
        result = run(tool, step_target, extra)
        if result != 0:
            print(f"STOP {tool.name} reported failures")
            return result
    if polish and mapped.exists():
        mapped.unlink()
    print(f"PASS {target.name} finalized")
    if gate:
        return run_gate(target, model, state, directory, skill_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
