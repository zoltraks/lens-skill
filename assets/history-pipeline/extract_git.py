"""Git extract: commits, version eras, boundary stats, dependency events, per-commit churn.

Target: the repository named in gathering/config.json - edit this line to name it.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict

from common import (CONFIG, OUT, REPO, bucket, classify, counts_loc, git, module, ticket, vkey,
                    write)

REF = CONFIG.get("ref", "HEAD")
SEP, REC = "\x1f", "\x1e"
MANIFEST = re.compile(r"(^|/)(package\.json|Dockerfile[^/]*|compose[^/]*\.ya?ml|docker-compose[^/]*\.ya?ml"
                      r"|\.gitlab-ci\.yml)$")


def commits() -> list[dict]:
    raw = git("log", REF, "--reverse", "--topo-order", "--numstat", "--no-renames",
              f"--format={REC}%H{SEP}%aI{SEP}%an{SEP}%P{SEP}%s")
    out = []
    for chunk in raw.split(REC)[1:]:
        head, _, body = chunk.partition("\n")
        sha, date, author, parents, subject = head.split(SEP, 4)
        files = []
        for line in body.splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                ins = int(parts[0]) if parts[0].isdigit() else 0
                dele = int(parts[1]) if parts[1].isdigit() else 0
                files.append((parts[2], ins, dele))
        out.append({"sha": sha, "date": date, "author": author, "parents": parents.split(),
                    "subject": subject.strip(), "files": files})
    return out


VERSION_FILE = re.compile(r"(^|/)(package\.json|Cargo\.toml|pyproject\.toml|[\w.-]+\.csproj)$")


def discover_manifests() -> list[str]:
    """Every manifest path that ever existed at the ref - a project version can move between
    manifests over time, so the version walk covers all of them."""
    if CONFIG.get("version_manifests"):
        return CONFIG["version_manifests"]
    names = git("log", REF, "--format=", "--name-only", "--diff-filter=AM").split()
    return sorted({n for n in names if VERSION_FILE.search(n) and "node_modules/" not in n})


def read_version(text: str, path: str) -> str | None:
    if path.endswith(".json"):
        try:
            return json.loads(text).get("version")
        except json.JSONDecodeError:
            return None
    if path.endswith(".csproj"):
        match = re.search(r"<Version>([^<]+)</Version>", text)
    else:
        section = re.search(r"(?ms)^\[(?:package|project|tool\.poetry)\]\s*$(.*?)(?=^\[|\Z)", text)
        match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', section.group(1)) if section else None
    return match.group(1) if match else None


VERSION_MANIFESTS: list[str] = []


def manifest_version(sha: str) -> str | None:
    """Highest declared version across the version-bearing manifests at a commit."""
    found = []
    for path in VERSION_MANIFESTS:
        try:
            version = read_version(git("show", f"{sha}:{path}"), path)
        except subprocess.CalledProcessError:
            continue
        if version and re.match(r"^\d+\.\d+\.\d+", version):
            found.append(version)
    return max(found, key=vkey) if found else None


def eras(history: list[dict]) -> list[dict]:
    """Bump commits close the era they complete, strictly increasing versions only."""
    walk = git("log", REF, "--reverse", "--topo-order", "--full-history", "--format=%H",
               "--", *VERSION_MANIFESTS).split()
    index = {c["sha"]: i for i, c in enumerate(history)}
    running, bounds = None, []
    for sha in walk:
        version = manifest_version(sha)
        if not version:
            continue
        if running is None:
            running = version
            continue
        if vkey(version) > vkey(running):
            bounds.append((index[sha], running, sha))
            running = version
    out, start = [], 0
    for position, version, sha in sorted(bounds):
        out.append({"version": version, "kind": "release", "first": start, "last": position})
        start = position + 1
    if start < len(history):
        out.append({"version": running, "kind": "developing", "first": start,
                    "last": len(history) - 1})
    return out


class Blobs:
    """Line and test-case counts per blob, cached across boundaries."""

    def __init__(self) -> None:
        cache_file = OUT / "blob-cache.json"
        self.cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
        self.cache_file = cache_file

    def measure(self, shas: list[str]) -> None:
        todo = [s for s in dict.fromkeys(shas) if s not in self.cache]
        if not todo:
            return
        proc = subprocess.run(["git", "-C", str(REPO), "cat-file", "--batch"],
                              input=("\n".join(todo) + "\n").encode(), capture_output=True,
                              check=True)
        data, pos = proc.stdout, 0
        for sha in todo:
            header_end = data.index(b"\n", pos)
            header = data[pos:header_end].split()
            size = int(header[2]) if len(header) > 2 else 0
            body = data[header_end + 1:header_end + 1 + size]
            pos = header_end + 1 + size + 1
            if b"\0" in body[:8000]:
                self.cache[sha] = [0, 0]
                continue
            text = body.decode("utf-8", errors="replace")
            lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
            cases = len(re.findall(r"(?m)^\s*(?:it|test)(?:\.each\([^)]*\))?\s*\(", text))
            self.cache[sha] = [lines, cases]

    def save(self) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(self.cache), encoding="utf-8")


def tree(sha: str) -> list[tuple[str, str]]:
    out = []
    for line in git("ls-tree", "-r", sha).splitlines():
        meta, _, path = line.partition("\t")
        mode, kind, blob = meta.split()
        if kind == "blob":
            out.append((path, blob))
    return out


def package_deps(sha: str, path: str) -> dict[str, dict[str, str]]:
    try:
        data = json.loads(git("show", f"{sha}:{path}"))
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}
    out = {}
    for key, channel in (("dependencies", "prod"), ("devDependencies", "dev"),
                         ("peerDependencies", "indirect"), ("optionalDependencies", "indirect")):
        for name, version in (data.get(key) or {}).items():
            out[name] = {"version": str(version), "kind": channel}
    return out


def image_deps(sha: str, path: str) -> dict[str, dict[str, str]]:
    try:
        text = git("show", f"{sha}:{path}")
    except subprocess.CalledProcessError:
        return {}
    out = {}
    for match in re.finditer(r"(?im)^\s*(?:FROM\s+|image:\s*)['\"]?([^\s'\"]+)", text):
        ref = re.sub(r"^\$\{[^}]+\}/", "", match.group(1))
        if ref.lower() == "scratch" or ref.startswith("$"):
            continue
        name, _, tag = ref.partition(":")
        out[name] = {"version": tag or "latest", "kind": "build"}
    return out


def deps_of(sha: str, path: str) -> dict[str, dict[str, str]]:
    return package_deps(sha, path) if path.endswith("package.json") else image_deps(sha, path)


def dependency_events(history: list[dict]) -> list[dict]:
    events = []
    for c in history:
        touched = [f for f, _, _ in c["files"] if MANIFEST.search(f)]
        if not touched or not c["parents"]:
            continue
        parent = c["parents"][0]
        for path in touched:
            after, before = deps_of(c["sha"], path), deps_of(parent, path)
            for name in sorted(set(after) | set(before)):
                a, b = after.get(name), before.get(name)
                if a and b and a["version"] == b["version"]:
                    continue
                action = "added" if not b else "removed" if not a else "bumped"
                dep = {"name": name, "manifest": path, "kind": (a or b)["kind"], "action": action}
                if b:
                    dep["from"] = b["version"]
                if a:
                    dep["to"] = a["version"]
                verb = {"added": "add", "removed": "remove", "bumped": "bump"}[action]
                title = f"{verb} {name}" + (f" {b['version']} -> {a['version']}" if a and b else
                                            f" {(a or b)['version']}")
                events.append({"type": "dependency", "title": title, "date": c["date"],
                               "sha": c["sha"], "dep": dep})
    return events


def boundary_stats(sha: str, blobs: Blobs) -> dict:
    files = tree(sha)
    blobs.measure([b for p, b in files if counts_loc(p)])
    loc = Counter()
    count = Counter()
    modules: dict[str, Counter] = defaultdict(Counter)
    sizes = []
    cases = test_files = 0
    for path, blob in files:
        kind = bucket(path)
        lines, case_count = blobs.cache.get(blob, [0, 0]) if counts_loc(path) else (0, 0)
        loc[kind] += lines
        count[kind] += 1
        mod = module(path)
        modules[mod][kind] += lines
        modules[mod]["files"] += 1
        if kind in ("src", "test") and lines:
            sizes.append((lines, path, mod))
        if kind == "test":
            test_files += 1
            cases += case_count
    deps = {"prod": 0, "dev": 0}
    module_deps = {}
    auth = set()
    for path, _ in files:
        if path.endswith("package.json") and "node_modules/" not in path:
            parsed = package_deps(sha, path)
            auth |= {n for n, d in parsed.items() if d["kind"] == "prod" and re.search(
                r"auth|keycloak|jwt|jose|passport|oidc|openid|session|bcrypt|argon|csrf|cookie", n)}
            prod = sum(1 for d in parsed.values() if d["kind"] == "prod")
            dev = sum(1 for d in parsed.values() if d["kind"] == "dev")
            deps["prod"] += prod
            deps["dev"] += dev
            module_deps[module(path)] = {"prod": prod, "dev": dev}
    api = {}
    if any(p == "openapi.yaml" for p, _ in files):
        text = git("show", f"{sha}:openapi.yaml")
        paths = re.findall(r"(?m)^  (/[^:\s]*):\s*$", text)
        ops = re.findall(r"(?m)^    (get|put|post|delete|patch|options|head):\s*$", text)
        schemes = 0
        block = re.search(r"(?m)^(\s*)securitySchemes:\s*\n((?:\1\s+.*\n|\s*\n)*)", text)
        if block:
            indent = len(block.group(1)) + 2
            schemes = len(re.findall(rf"(?m)^ {{{indent}}}[A-Za-z0-9_]+:\s*$", block.group(2)))
        api = {"paths": len(paths), "operations": len(ops), "schemes": schemes}
    sizes.sort(reverse=True)
    totals = lambda c: {k: c.get(k, 0) for k in ("src", "test", "docs", "other")}
    loc_block = totals(loc)
    loc_block["total"] = sum(loc_block.values())
    files_block = totals(count)
    files_block["total"] = sum(files_block.values())
    return {
        "loc": loc_block, "files": files_block, "deps": deps,
        "modules": {m: dict(v) for m, v in modules.items()}, "module_deps": module_deps,
        "largest": [{"path": p, "loc": n, "module": m} for n, p, m in sizes[:12]],
        "all_sizes": [n for n, _, _ in sizes if not _.endswith((".json", ".yaml", ".yml"))],
        "test": {"cases": cases, "files": test_files}, "api": api, "auth_deps": len(auth),
    }


def main() -> None:
    VERSION_MANIFESTS[:] = discover_manifests()
    history = commits()
    era_list = eras(history)
    since = CONFIG.get("from_version")
    if since:
        era_list = [e for e in era_list if vkey(e["version"]) >= vkey(since)]
    blobs = Blobs()
    head = history[-1]["sha"]
    for era in era_list:
        end = head if era["kind"] == "developing" else history[era["last"]]["sha"]
        era["boundary"] = end
        era["stats"] = boundary_stats(end, blobs)
    blobs.save()
    churn = []
    for i, c in enumerate(history):
        per = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        for path, ins, dele in c["files"]:
            if not counts_loc(path):
                continue
            cell = per[module(path)][bucket(path)]
            cell[0] += ins
            cell[1] += dele
        churn.append({m: dict(v) for m, v in per.items()})
    commit_events = []
    for c in history:
        merge = len(c["parents"]) > 1
        kind = "merge" if merge else classify(c["subject"])
        ins = sum(f[1] for f in c["files"] if counts_loc(f[0]))
        dele = sum(f[2] for f in c["files"] if counts_loc(f[0]))
        event = {"type": kind, "title": c["subject"], "date": c["date"], "sha": c["sha"]}
        if ins:
            event["ins"] = ins
        if dele:
            event["del"] = dele
        if merge:
            branch = re.search(r"merge (?:branch )?'?([\w./-]+)'? into", c["subject"], re.I)
            if branch:
                event["branch"] = branch.group(1)
        found = ticket(c["subject"], event.get("branch", ""))
        if found:
            event["ticket"] = found
        commit_events.append(event)
    write("commits.json", [{"sha": c["sha"], "date": c["date"], "author": c["author"],
                            "files": [[f, i, d] for f, i, d in c["files"]]} for c in history])
    write("commit-events.json", commit_events)
    write("eras.json", era_list)
    write("churn.json", churn)
    write("dependencies.json", dependency_events(history))
    write("ref.json", {"ref": REF, "sha": head, "local_head": git("rev-parse", "HEAD").strip(),
                       "commits": len(history), "grouping": "version"})
    print(f"commits={len(history)} eras={len(era_list)} last={era_list[-1]['version']}")


if __name__ == "__main__":
    main()
