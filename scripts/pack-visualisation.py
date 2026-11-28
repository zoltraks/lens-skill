#!/usr/bin/env python3
"""Pack a `history.json` dataset into the bundled single-file HTML visualisation.

Reads the shipped viewer shell (`assets/visualisation-shell.html`) - a
single-file HTML application carrying a dataset placeholder script tag -
replaces the placeholder with `window.HISTORY_DATA` built from the dataset,
and writes one self-contained artifact that opens over `file://` with no
server and no sibling files.

The shell stays untouched - this produces an output artifact only.
View overrides (`--layout`, `--theme`, `--palette`) stamp into the embedded
copy of the dataset, never back into the source `history.json`.

Usage:
  python scripts/pack-visualisation.py --history path/to/history.json
  python scripts/pack-visualisation.py --history h.json --out build/city.html
  python scripts/pack-visualisation.py --history h.json --layout islands --theme dark --palette green
  python scripts/pack-visualisation.py --history h.json --shim js/history.js
  python scripts/pack-visualisation.py --history h.json --shell alt.html --check
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SHELL = ROOT / "assets" / "visualisation-shell.html"

DATA_TAG = '<script src="history.js"></script>'
PLACEHOLDER = re.compile(r"<!--\s*dataset placeholder[^>]*-->\s*")


def read_dataset(path: Path) -> dict:
    """Load the dataset and refuse shapes the viewer cannot consume."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"pack-visualisation: cannot read dataset {path}: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("versions"), list) \
            or not isinstance(data.get("categories"), list):
        raise SystemExit(
            f"pack-visualisation: {path} is not a history.json dataset "
            "(object with `categories` and `versions` lists expected)")
    return data


def apply_view(data: dict, args) -> dict:
    """Stamp resolved view overrides into the embedded copy of the dataset."""
    view = dict(data.get("view") or {})
    for key in ("layout", "theme", "palette"):
        val = getattr(args, key)
        if val:
            view[key] = val
    if view:
        data["view"] = view
    return data


def data_script(data: dict, source_name: str) -> str:
    """<script> assigning the dataset to window.HISTORY_DATA."""
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    return ("<script>\n\n/* embedded dataset - twin of " + source_name
            + " */\n\nwindow.HISTORY_DATA = " + payload + ";\n\n</script>\n")


def shim_text(data: dict) -> str:
    """The file:// JavaScript twin of the dataset - one line, no banner."""
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    return "window.HISTORY_DATA = " + payload + ";\n"


def pack(html: str, script: str) -> str:
    """Replace the placeholder comment and dataset tag with the inline data."""
    if DATA_TAG not in html:
        raise SystemExit(
            "pack-visualisation: shell carries no " + DATA_TAG
            + " anchor - the bundled viewer asset is stale or not a shell build")
    html = PLACEHOLDER.sub("", html)
    html = html.replace(DATA_TAG, script)
    html = re.sub(r"</head>\s*<body", "</head>\n\n<body", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def output_name(data: dict) -> str:
    """<project>-<version>.html derived from the dataset."""
    proj = (data.get("project") or {}).get("name", "project")
    ver = data["versions"][-1].get("version", "") if data.get("versions") else ""
    return re.sub(r"[^A-Za-z0-9._-]+", "-", proj) + ("-" + ver if ver else "") + ".html"


def enforce_registry_gate(history: Path) -> None:
    """Refuse a dataset that fails the sibling registry validator.

    The Dataset Requirement makes `validate-history.py` clean the entry gate -
    this call is the mechanical half of that contract. A `.tmp.` pack copy with
    no sibling validator warns and proceeds rather than silently dropping the
    gate.
    """
    validator = Path(__file__).resolve().with_name("validate-history.py")
    if not validator.is_file():
        print("pack-visualisation: validate-history.py not beside the packer"
              " - registry gate skipped, run it manually", file=sys.stderr)
        return
    result = subprocess.run(
        [sys.executable, str(validator), str(history)],
        capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        detail = (result.stdout or result.stderr or "").strip()
        raise SystemExit(
            "pack-visualisation: dataset fails validate-history.py"
            " - run scripts/repair-history.py first\n" + detail)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Pack a history.json dataset into the single-file HTML visualisation")
    ap.add_argument("--history", required=True, help="the dataset to embed")
    ap.add_argument("--shell", default=None,
                    help="viewer shell (default assets/visualisation-shell.html)")
    ap.add_argument("--out", default=None,
                    help="output file (default <project>-<version>.html)")
    ap.add_argument("--layout", default=None, help="view layout override")
    ap.add_argument("--theme", default=None, help="view theme override")
    ap.add_argument("--palette", default=None, help="view palette override")
    ap.add_argument("--shim", default=None,
                    help="also emit the file:// JavaScript twin at this path")
    ap.add_argument("--check", action="store_true",
                    help="verify shell anchor and dataset without writing")
    a = ap.parse_args()

    shell = Path(a.shell) if a.shell else DEFAULT_SHELL
    if not shell.is_file():
        raise SystemExit(
            "pack-visualisation: viewer shell not found at " + str(shell)
            + " - pass --shell or refresh the bundled asset")
    html = shell.read_text(encoding="utf-8")

    history = Path(a.history)
    enforce_registry_gate(history)
    data = apply_view(read_dataset(history), a)
    script = data_script(data, history.name)

    if DATA_TAG not in html:
        raise SystemExit(
            "pack-visualisation: shell carries no " + DATA_TAG
            + " anchor - the bundled viewer asset is stale or not a shell build")

    out = Path(a.out) if a.out else Path(output_name(data))
    view = data.get("view") or {}
    note = "view layout=%s theme=%s palette=%s" % (
        view.get("layout", "-"), view.get("theme", "-"), view.get("palette", "-"))

    if a.check:
        print("pack-visualisation: shell anchor present, dataset valid -",
              out, "-", len(data["versions"]), "versions -", note)
        return

    packed = pack(html, script)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(packed, encoding="utf-8")
    kb = out.stat().st_size // 1024
    print("packed -> %s (%d KB, data embedded, %s)" % (out, kb, note))

    if a.shim:
        shim = Path(a.shim)
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text(shim_text(data), encoding="utf-8")
        print("shim ->", shim)


if __name__ == "__main__":
    main()
