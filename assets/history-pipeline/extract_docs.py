"""Docs extract: development records with dates, families, era hints, summaries, and report
fields, plus changelog items.

Record families resolve from `docs_families` in gathering/config.json when present, else from
the defaults below - adapt them to the target's documentation layout.
Target: the repository named in gathering/config.json - edit this line to name it.
"""

from __future__ import annotations

import json
import re

from common import CONFIG, NOTES, OUT, REPO, classify, git, read, write

REF = CONFIG.get("ref", "HEAD")
SEP, REC = "\x1f", "\x1e"
VERSION_DIR = re.compile(r"/(\d+\.\d+\.\d+)/")
DATE_DIR = re.compile(r"(?:^|/)(\d{4}-\d{2}-\d{2})(?:/|[-_.])")
COMMENT_DATE = re.compile(r"<!--[^>]*Date:\s*(\d{4}-\d{2}-\d{2})")
FINDING = re.compile(r"\b(?:FND|AUD|HNT|BUG|ISS|RSK)(?:-[A-Z]{2,5})?-\d{2,4}\b")
VERDICTS = ["Production-ready", "Conditionally ready", "Not ready", "Ready", "Blocked", "Pass",
            "Fail", "Approved", "Approve", "Request changes", "Rejected", "Green", "Amber", "Red"]
SUBTYPES = {"fix": "fix", "bugfix": "fix", "bug": "fix", "feature": "feature", "chore": "chore",
            "refactor": "refactor", "improvement": "change", "change": "change", "docs": "change"}
REPORT_FAMILIES = {"audit", "hunt", "review", "assessment", "proposal", "report", "comparison"}
FAMILIES = CONFIG.get("docs_families", {})
ROOT_DOCS = FAMILIES.get("root", {"README.md": "docs", "AGENTS.md": "standard",
                                  "CLAUDE.md": "standard"})
TOP_DOCS = FAMILIES.get("top", {"MANIFEST.md": "spec", "LESSONS.md": "lesson",
                                "DECISIONS.md": "decision"})
DIR_FAMILY = FAMILIES.get("dirs", {
    "standard": "standard", "standards": "standard", "template": "template",
    "templates": "template", "concept": "concept", "concepts": "concept", "discard": "discard",
    "review": "review", "reviews": "review", "audit": "audit", "audits": "audit",
    "change": "change", "changes": "change", "plan": "plan", "plans": "plan",
    "comparison": "comparison", "refactoring": "assessment", "decision": "decision",
    "decisions": "decision", "spec": "spec", "specs": "spec", "report": "report",
    "reports": "report", "proposal": "proposal", "proposals": "proposal", "lesson": "lesson",
    "lessons": "lesson", "prompt": "prompt", "prompts": "prompt"})


def family(path: str) -> str | None:
    if path in ROOT_DOCS:
        return ROOT_DOCS[path]
    if not path.startswith("docs/") or not path.endswith(".md"):
        return None
    parts = path.split("/")
    name = parts[-1].lower()
    if len(parts) == 2:
        return TOP_DOCS.get(parts[1], "standard")
    tree = parts[2] if parts[1] == "archive" and len(parts) > 3 else parts[1]
    base = DIR_FAMILY.get(tree)
    if base is None:
        return None
    if base == "template":
        return "template"
    if base == "assessment":
        return "proposal" if "proposal" in name else "assessment"
    if base == "audit":
        return "hunt" if name.startswith("hunt") else "audit"
    if base in ("decision", "spec", "report", "proposal", "lesson", "prompt"):
        return base
    if base in ("change", "plan"):
        for word, kind in (("audit", "audit"), ("verification", "report"), ("report", "report"),
                           ("review", "review"), ("decision", "decision")):
            if word in name:
                return kind
    return base


def first_adds() -> dict[str, tuple[str, str]]:
    raw = git("log", REF, "--reverse", "--diff-filter=A", "--no-renames", "--name-only",
              f"--format={REC}%H{SEP}%aI", "--", "docs", "README.md", "AGENTS.md", "CLAUDE.md")
    out = {}
    for chunk in raw.split(REC)[1:]:
        head, _, body = chunk.partition("\n")
        sha, date = head.split(SEP)
        for path in body.split():
            out.setdefault(path, (sha, date))
    return out


def title_of(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else fallback


def prose_after(text: str, start: int) -> str | None:
    for block in re.split(r"\n\s*\n", text[start:]):
        block = block.strip()
        if not block or block.startswith(("#", "|", "<!--", ">", "```", "-", "*", "!")):
            continue
        return re.sub(r"\s+", " ", block)
    return None


def summary_of(text: str) -> str | None:
    heading = re.search(r"(?mi)^#{2,3}\s+(summary|purpose|overview|analysis)\s*$", text)
    found = prose_after(text, heading.end()) if heading else None
    if not found:
        h1 = re.search(r"(?m)^#\s+.+$", text)
        found = prose_after(text, h1.end() if h1 else 0)
    if not found:
        return None
    if len(found) > 280:
        cut = found[:280].rsplit(". ", 1)[0]
        found = cut + "." if len(cut) > 80 else found[:277].rstrip() + "..."
    return found


def report_fields(text: str, path: str) -> dict:
    out = {}
    score = re.search(r"(\d{1,2}(?:\.\d)?/10)", text)
    if score:
        out["score"] = score.group(1)
    for pattern in (r"\*\*Verdict:\*\*\s*([^\n]+)", r"Readiness:\s*\*\*([^*]+)\*\*",
                    r"(?mi)^#{2,3}\s*Verdict\s*\n+\s*\**([^\n*]+)"):
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip().rstrip(".")
            word = next((v for v in VERDICTS if value.lower().startswith(v.lower())), None)
            if word:
                out["verdict"] = word
                break
    findings = set(FINDING.findall(text))
    if findings:
        out["findings"] = len(findings)
    revision = re.search(r"Report Revision\s*\|\s*([\d.]+)", text) or \
        re.search(r"-(\d+\.\d+)-(?:EN|PL)\.md$", path)
    if revision:
        out["revision"] = revision.group(1)
    subject = re.search(r"Subject (?:Version|Revision)\s*\|[^\n|]*?(\d+\.\d+\.\d+)", text)
    if subject:
        out["subject_version"] = subject.group(1)
    return out


def changelog_items() -> dict[str, list[dict]]:
    try:
        text = git("show", f"{REF}:CHANGELOG.md")
    except Exception:
        return {}
    items: dict[str, list[dict]] = {}
    current = None
    for line in text.splitlines():
        head = re.match(r"^##\s+(?:Version\s+|\[)?v?(\d+\.\d+\.\d+)", line)
        if head:
            current = head.group(1)
            items.setdefault(current, [])
            continue
        bullet = re.match(r"^- \*\*(.+?)\*\*\s*[-:]\s*(.+)$", line)
        plain = re.match(r"^- (.+)$", line)
        if current and bullet:
            items[current].append({"subject": bullet.group(1).strip(),
                                   "text": "- " + bullet.group(2).strip()})
        elif current and plain:
            text = plain.group(1).strip()
            items[current].append({"subject": text.split(" - ")[0][:80], "text": "- " + text})
    return items


def main() -> None:
    adds = first_adds()
    files = [line.split("\t", 1)[1] for line in git("ls-tree", "-r", REF).splitlines()]
    records, skipped = [], []
    for path in files:
        kind = family(path)
        if kind is None:
            if path.startswith("docs/") and path.endswith(".md"):
                skipped.append(path)
            continue
        text = git("show", f"{REF}:{path}")
        sha, committed = adds.get(path, ("", ""))
        date_match = DATE_DIR.search(path) or COMMENT_DATE.search(text)
        record = {"type": kind, "title": title_of(text, path.rsplit("/", 1)[-1]),
                  "date": date_match.group(1) if date_match else committed[:10],
                  "ref": path, "committed": committed, "add_sha": sha}
        if "/archive/" in path:
            record["archived"] = True
        version = VERSION_DIR.search(path)
        if version:
            record["version_dir"] = version.group(1)
        if kind == "change":
            declared = re.search(r"(?mi)^\*\*Type:?\*\*:?\s*([A-Za-z]+)", text)
            subtype = SUBTYPES.get(declared.group(1).lower()) if declared else None
            if subtype:
                record["subtype"] = subtype
            record["type"] = subtype or classify(record["title"])
            if record["type"] in ("merge", "release", "docs", "test"):
                record["type"] = "change"
        if kind in REPORT_FAMILIES | {"report"}:
            record.update(report_fields(text, path))
        if kind in REPORT_FAMILIES | {"change", "plan", "decision", "refactor", "spec", "concept",
                                      "feature", "fix", "chore"} or record["type"] in (
                "feature", "fix", "refactor", "chore"):
            found = summary_of(text)
            if found:
                record["summary"] = found
        records.append(record)
    write("records.json", records)
    write("changelog.json", changelog_items())
    NOTES.mkdir(parents=True, exist_ok=True)
    untracked = git("status", "--porcelain", "--untracked-files=all", "--", "docs").splitlines()
    scratch = sorted(p.name for p in (REPO / "work").iterdir()) if (REPO / "work").is_dir() else []
    (NOTES / "inventory.json").write_text(json.dumps({
        "unclassified_docs": skipped, "uncommitted_docs": untracked, "scratch_trees": scratch},
        indent=1), encoding="utf-8")
    print(f"records={len(records)} skipped={len(skipped)} changelog_versions="
          f"{len(changelog_items())}")


if __name__ == "__main__":
    main()
