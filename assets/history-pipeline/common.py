"""Shared helpers for the history pipeline shipped with Lens.

Copy the four scripts into `<workspace>/gathering/scripts/` - paths resolve from there.
Target: the repository named in gathering/config.json - edit this line to name it.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
CONFIG = json.loads((WORKSPACE / "gathering" / "config.json").read_text(encoding="utf-8"))
REPO = (WORKSPACE / "gathering" / CONFIG["repo"]).resolve() if not Path(CONFIG["repo"]).is_absolute() \
    else Path(CONFIG["repo"])
OUT = WORKSPACE / "gathering" / "out"
NOTES = WORKSPACE / "gathering" / "notes"

LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json"}
CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".css", ".scss", ".html", ".py", ".sh",
            ".ps1", ".yaml", ".yml", ".json", ".toml", ".sql", ".mts", ".cts", ".vue", ".svg"}
DOC_EXT = {".md", ".mdx", ".txt", ".rst"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".woff", ".woff2", ".ttf", ".zip",
              ".pdf", ".gz", ".db", ".sqlite"}


def git(*args: str, binary: bool = False):
    result = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True)
    return result.stdout if binary else result.stdout.decode("utf-8", errors="replace")


def bucket(path: str) -> str:
    """src, test, docs, or other for a repository path."""
    lower = path.lower()
    name = lower.rsplit("/", 1)[-1]
    ext = "." + name.rsplit(".", 1)[-1] if "." in name else ""
    if ext in DOC_EXT or lower.startswith("docs/"):
        return "docs"
    if re.search(r"(^|/)(__tests__|tests?|e2e|fixtures)/", lower) or re.search(r"\.(test|spec)\.", name):
        return "test"
    if ext in CODE_EXT or name in ("dockerfile", "makefile") or name.startswith("dockerfile"):
        return "src"
    return "other"


def module(path: str) -> str:
    """Top-level directory, `src/` split one level deeper, root files under `root`."""
    parts = path.split("/")
    if len(parts) == 1:
        return "root"
    if parts[0] == "src" and len(parts) > 2:
        return f"src/{parts[1]}"
    return parts[0]


def counts_loc(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return name not in LOCKFILES and ext not in BINARY_EXT


def write(name: str, data) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n",
                            encoding="utf-8", newline="\n")


def read(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def vkey(version: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", version)[:3]) or (0,)


SUBJECT_RULES = [
    ("release", r"^(chore\(release\)|release\b|bump (the )?version|v?\d+\.\d+\.\d+$)"),
    ("merge", r"^(merge\b|chore\(pr\): merge)"),
    ("fix", r"^(fix|hotfix|bugfix)(\(|:|!|\b)"),
    ("refactor", r"^refactor(\(|:|!)"),
    ("test", r"^test(s)?(\(|:|!)"),
    ("docs", r"^docs?(\(|:|!)"),
    ("feature", r"^feat(ure)?(\(|:|!)"),
    ("dependency", r"^(build\(deps\)|chore\(deps\)|deps(\(|:))"),
    ("chore", r"^(chore|build|ci|style|perf)(\(|:|!)"),
    ("change", r"^(change|update|improve|add|remove|rename|move)\b"),
]


def classify(subject: str) -> str:
    lower = subject.strip().lower()
    for kind, pattern in SUBJECT_RULES:
        if re.search(pattern, lower):
            return "chore" if kind == "dependency" else kind
    if re.search(r"\bfix(es|ed)?\b", lower):
        return "fix"
    return "change"


TICKET = re.compile(r"\b(OP#\d+|[A-Z][A-Z0-9]+-\d+|LAB-\d+|#\d+)\b", re.I)


def ticket(*texts: str) -> str | None:
    for text in texts:
        match = TICKET.search(text or "")
        if match:
            return match.group(1).upper() if "-" in match.group(1) else match.group(1)
    return None
