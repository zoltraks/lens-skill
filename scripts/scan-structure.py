#!/usr/bin/env python3
"""Deterministic repository-structure scanner for Lens audits.

Walks the audited tree - `git ls-files` when the root is a work tree, a
filesystem walk otherwise - classifies every file into the audit-model
inventory classes, and emits the structure census the organization model
and responsibility inventory are built from.

The scan is read-only: it reads names and sizes, never file contents beyond
what git itself reports, and never builds, tests, or executes the subject.

Usage:
    python scan-structure.py <root> [--json] [--no-git] [--output FILE]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# File classes, per references/evidence-schema.md coverage classification,
# extended with the non-code classes doc, config, asset, and other.
CLASSES = (
    "production", "test", "test-support", "generated", "vendored",
    "example", "script", "doc", "config", "asset", "other",
)

CODE_EXT = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".cs", ".go", ".rs",
    ".java", ".kt", ".kts", ".scala", ".groovy", ".py", ".rb", ".php",
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte",
    ".swift", ".m", ".mm", ".pl", ".pm", ".lua", ".r", ".jl", ".ex",
    ".exs", ".erl", ".hrl", ".hs", ".ml", ".fs", ".fsx", ".vb", ".dart",
    ".zig", ".nim", ".cr", ".d", ".sol", ".move", ".proto", ".thrift",
    ".sql", ".prisma", ".graphql", ".gql",
}
DOC_EXT = {".md", ".markdown", ".rst", ".txt", ".adoc", ".tex", ".pod"}
CONFIG_EXT = {
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".properties",
    ".xml", ".env", ".editorconfig", ".lock", ".gradle", ".props", ".targets",
    ".cmake", ".mk", ".nuspec", ".csproj", ".vbproj", ".fsproj", ".sln",
    ".ipkg", ".podspec", ".gemspec", ".bazel", ".bzl", ".tf", ".tfvars",
    ".hcl", ".plist",
}
ASSET_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".wav",
    ".avi", ".mov", ".webm", ".pdf", ".zip", ".tar", ".gz", ".bz2", ".xz",
    ".7z", ".jar", ".war", ".dll", ".so", ".dylib", ".exe", ".bin", ".dat",
    ".wasm", ".class", ".pyc", ".min",
}
SCRIPT_EXT = {".sh", ".bash", ".zsh", ".ps1", ".psm1", ".bat", ".cmd"}

TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "unittest", "unittests"}
TEST_SUPPORT_DIRS = {
    "fixtures", "fixture", "testdata", "test-data", "mocks", "mock", "__mocks__",
    "fakes", "stubs", "support", "helpers", "factories", "golden",
}
VENDOR_DIRS = {
    "vendor", "vendored", "third_party", "third-party", "node_modules", "bower_components",
    "external", "extern", "deps", "submodules",
}
EXAMPLE_DIRS = {
    "example", "examples", "sample", "samples", "demo", "demos", "playground",
    "tutorial", "tutorials", "showcase",
}
SCRIPT_DIRS = {"scripts", "bin", "tools"}
DOC_DIRS = {"docs", "doc", "documentation", "wiki"}
CONFIG_DIRS = {"config", "configs", "conf", "settings", ".config"}

GENERATED_NAME = re.compile(
    r"(\.generated\.|_generated\.|\.g\.|_pb2\.|_pb\.|\.designer\.|"
    r"autogen|codegen|\.auto\.|\.min\.)",
    re.IGNORECASE,
)
TEST_NAME = re.compile(
    r"(^test_|_test\.|\.test\.|\.spec\.|test_.*\.|.*_tests?\.|.*spec\.)",
    re.IGNORECASE,
)
TEST_SUPPORT_NAME = re.compile(
    r"(^conftest\.|_fixture|fixture_|_mock|mock_|_fake|fake_|_stub|stub_|"
    r"factory|^helpers?\.)",
    re.IGNORECASE,
)
CONFIG_NAME = re.compile(
    r"(^dockerfile|^makefile|^cmakelists\.txt$|^pom\.xml$|^build\.|"
    r"^compose|^docker-compose|^\.env|^\.git|^\.dockerignore|^\.editorconfig|"
    r"^license|^notice|^copying)",
    re.IGNORECASE,
)
DOC_NAME = re.compile(
    r"(^readme|^changelog|^changes|^contributing|^authors|^history|^news|"
    r"^code_of_conduct|^security|^license|^notice|^copying|^install|"
    r"^adr[-_]?\d*)",
    re.IGNORECASE,
)

CASING_KINDS = (
    "PascalCase", "camelCase", "snake_case", "kebab-case",
    "UPPER_SNAKE", "lowercase", "dotted.PascalCase", "other",
)
ABBREVIATED_DIRS = {
    "app", "auth", "cfg", "conf", "config", "configs", "ctrl", "db", "doc",
    "docs", "dto", "dtos", "env", "err", "errs", "exc", "impl", "intf",
    "mgr", "msg", "pkg", "repo", "repos", "req", "res", "resp", "srv",
    "svc", "svcs",
}
CATCH_ALL_NAMES = {
    "misc", "util", "utils", "common", "helper", "helpers", "shared", "general",
}
SINGLE_TYPE_EXT = {".cs", ".java", ".php"}
PUBLIC_TYPE_DECL = re.compile(
    r"^\s*(?:public|internal)\s+"
    r"(?:(?:sealed|static|abstract|readonly|partial|final)\s+)*"
    r"(?:class|interface|struct|enum|record(?:\s+class|\s+struct)?|trait)\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)


def casing_of(stem: str) -> str:
    """Classify an identifier or file/directory stem into a casing bucket."""
    if not stem:
        return "other"
    if "." in stem and all(
        re.fullmatch(r"[A-Z][A-Za-z0-9]*", part) for part in stem.split(".")
    ):
        return "dotted.PascalCase"
    if re.fullmatch(r"[a-z][a-z0-9]*", stem):
        return "lowercase"
    if re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", stem):
        return "snake_case"
    if re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+", stem):
        return "kebab-case"
    if re.fullmatch(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+", stem):
        return "UPPER_SNAKE"
    if re.fullmatch(r"[A-Z][A-Za-z0-9]*", stem) and any(c.islower() for c in stem):
        return "PascalCase"
    if re.fullmatch(r"[a-z][a-z0-9]*[A-Z][A-Za-z0-9]*", stem):
        return "camelCase"
    return "other"


def public_types_in(full_path: str, ext: str) -> list[str]:
    """Return top-level public/internal type names declared in a source file."""
    if ext not in SINGLE_TYPE_EXT:
        return []
    try:
        with open(full_path, encoding="utf-8", errors="replace") as handle:
            text = handle.read(256_000)
    except OSError:
        return []
    # Only count declarations at indent <= 4 (top-level or single namespace block).
    names: list[str] = []
    for line in text.splitlines():
        indent = len(line) - len(line.lstrip(" "))
        if indent > 4 or line.lstrip().startswith(("//", "#", "*", "/*")):
            continue
        match = PUBLIC_TYPE_DECL.match(line)
        if match:
            names.append(match.group(1))
    return names


def tracked_files(root: str) -> list[str]:
    """Return `git ls-files` output, or None when git cannot enumerate."""
    try:
        probe = subprocess.run(
            ["git", "-C", root, "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=30,
        )
        if probe.returncode != 0 or probe.stdout.strip() != "true":
            return None
        listed = subprocess.run(
            ["git", "-C", root, "ls-files", "-z"],
            capture_output=True, text=True, timeout=120,
        )
        if listed.returncode != 0:
            return None
        return sorted(p for p in listed.stdout.split("\0") if p)
    except (OSError, subprocess.SubprocessError):
        return None


NOISE_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", ".tox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".idea", ".vscode",
}


def walked_files(root: str) -> list[str]:
    """Filesystem fallback: skips VCS and cache noise, keeps everything else.

    This mode does not apply .gitignore - the census records `mode: filesystem`
    so the audit can apply exclusions explicitly.
    """
    paths = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in NOISE_DIRS]
        for name in files:
            full = os.path.join(base, name)
            paths.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(paths)


def head_commit(root: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", root, "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=30,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def segments(path: str) -> list[str]:
    return [seg.lower() for seg in path.split("/")]


def classify(path: str) -> str:
    segs = segments(path)
    name = segs[-1]
    dirs = segs[:-1]
    ext = os.path.splitext(name)[1].lower()

    if any(d in VENDOR_DIRS for d in dirs):
        return "vendored"
    if any(d in EXAMPLE_DIRS for d in dirs):
        return "example"
    if GENERATED_NAME.search(name):
        return "generated"
    in_test_dir = any(d in TEST_DIRS for d in dirs)
    if TEST_NAME.search(name):
        return "test"
    if in_test_dir:
        if TEST_SUPPORT_NAME.search(name) or any(d in TEST_SUPPORT_DIRS for d in dirs):
            return "test-support"
        return "test" if ext in CODE_EXT else "test-support"
    if any(d in TEST_SUPPORT_DIRS for d in dirs):
        return "test-support"
    if any(d in DOC_DIRS for d in dirs) or ext in DOC_EXT or DOC_NAME.match(name):
        return "doc"
    if any(d in CONFIG_DIRS for d in dirs) or CONFIG_NAME.match(name) or ext in CONFIG_EXT:
        return "config"
    if ext in SCRIPT_EXT or (dirs and dirs[0] in SCRIPT_DIRS and ext in CODE_EXT | SCRIPT_EXT | {""}):
        return "script"
    if ext in ASSET_EXT or name.endswith((".min.js", ".min.css")):
        return "asset"
    if ext in CODE_EXT:
        return "production"
    return "other"


def module_of(path: str) -> str:
    return path.split("/")[0] if "/" in path else "."


def scan(root: str, use_git: bool) -> dict:
    paths = tracked_files(root) if use_git else None
    mode = "git"
    if paths is None:
        paths = walked_files(root)
        mode = "filesystem"
    entries = []
    classes = {c: 0 for c in CLASSES}
    modules: dict[str, dict] = {}
    extensions: dict[str, int] = {}
    dir_casing = {k: 0 for k in CASING_KINDS}
    file_casing = {k: 0 for k in CASING_KINDS}
    seen_dirs: set[str] = set()
    abbreviated_dirs: set[str] = set()
    catch_all_paths: set[str] = set()
    multi_type_files: list[dict] = []
    for path in paths:
        cls = classify(path)
        mod = module_of(path)
        full = os.path.join(root, path.replace("/", os.sep))
        try:
            size = os.path.getsize(full)
        except OSError:
            size = None
        depth = path.count("/")
        parts = path.split("/")
        for idx in range(len(parts) - 1):
            dpath = "/".join(parts[: idx + 1])
            dname = parts[idx]
            if dpath not in seen_dirs and not dname.startswith("."):
                seen_dirs.add(dpath)
                dir_casing[casing_of(dname)] += 1
                if dname.lower() in ABBREVIATED_DIRS and not (
                    idx == 0 and dname.lower() == "docs"
                ):
                    abbreviated_dirs.add(dpath)
                if dname.lower() in CATCH_ALL_NAMES:
                    catch_all_paths.add(dpath)
        stem, ext = os.path.splitext(parts[-1])
        ext_low = ext.lower()
        is_prod_code = cls == "production" or (
            ext_low in CODE_EXT and cls not in ("test", "test-support", "vendored", "generated", "example")
        )
        if is_prod_code:
            file_casing[casing_of(stem)] += 1
            if stem.lower() in CATCH_ALL_NAMES:
                catch_all_paths.add(path)
            types = public_types_in(full, ext_low)
            if len(types) > 1:
                multi_type_files.append(
                    {"path": path, "count": len(types), "types": types}
                )
        entries.append(
            {"path": path, "class": cls, "module": mod, "depth": depth, "bytes": size}
        )
        classes[cls] += 1
        bucket = modules.setdefault(mod, {"files": 0, "classes": {c: 0 for c in CLASSES}})
        bucket["files"] += 1
        bucket["classes"][cls] += 1
        ext_key = ext_low or "<none>"
        extensions[ext_key] = extensions.get(ext_key, 0) + 1
    return {
        "root": os.path.abspath(root),
        "mode": mode,
        "commit": head_commit(root) if mode == "git" else None,
        "total_files": len(entries),
        "classes": classes,
        "modules": modules,
        "extensions": dict(sorted(extensions.items())),
        "naming": {
            "directory_casing": {k: v for k, v in dir_casing.items() if v},
            "production_file_casing": {k: v for k, v in file_casing.items() if v},
            "abbreviated_dirs": sorted(abbreviated_dirs),
            "catch_all_paths": sorted(catch_all_paths),
            "multi_type_files": multi_type_files,
        },
        "inventory": entries,
    }


def render_text(result: dict) -> str:
    lines = [
        f"root: {result['root']}",
        f"mode: {result['mode']}",
        f"commit: {result['commit'] or 'n/a'}",
        f"total files: {result['total_files']}",
        "",
        "classes:",
    ]
    for cls in CLASSES:
        lines.append(f"  {cls:<14}{result['classes'][cls]}")
    lines.append("")
    lines.append("top-level areas:")
    for mod in sorted(result["modules"]):
        bucket = result["modules"][mod]
        mix = ", ".join(
            f"{c}:{n}" for c, n in bucket["classes"].items() if n
        )
        lines.append(f"  {mod:<30}{bucket['files']:>6}  {mix}")
    lines.append("")
    lines.append("extensions:")
    for ext, count in result["extensions"].items():
        lines.append(f"  {ext:<12}{count}")
    naming = result.get("naming", {})
    if naming:
        lines.append("")
        lines.append("naming signals:")
        dc = ", ".join(f"{k}:{v}" for k, v in naming.get("directory_casing", {}).items())
        fc = ", ".join(f"{k}:{v}" for k, v in naming.get("production_file_casing", {}).items())
        lines.append(f"  directory casing:       {dc or 'none'}")
        lines.append(f"  production file casing: {fc or 'none'}")
        lines.append(
            f"  abbreviated dirs:       {', '.join(naming.get('abbreviated_dirs', [])) or 'none'}"
        )
        lines.append(
            f"  catch-all paths:        {', '.join(naming.get('catch_all_paths', [])) or 'none'}"
        )
        lines.append(
            f"  multi-type files:       {len(naming.get('multi_type_files', []))}"
        )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic repository-structure scanner for Lens audits."
    )
    parser.add_argument("root", help="repository root to scan")
    parser.add_argument(
        "--json", action="store_true",
        help="emit the full machine-readable inventory JSON instead of the summary",
    )
    parser.add_argument(
        "--no-git", action="store_true",
        help="use the filesystem walk even when the root is a git work tree",
    )
    parser.add_argument("--output", help="write to this file instead of stdout")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"scan-structure: no such directory: {args.root}", file=sys.stderr)
        return 2

    result = scan(args.root, use_git=not args.no_git)
    output = (
        json.dumps(result, indent=1, sort_keys=False) + "\n"
        if args.json
        else render_text(result) + "\n"
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
