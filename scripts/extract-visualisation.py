#!/usr/bin/env python3
"""Extract the embedded `history.json` dataset from a packed visualisation.

Reads a single-file HTML visualisation - one produced by
`pack-visualisation.py` or the viewer project's own single-file build -
recovers the `window.HISTORY_DATA` payload, and writes it back as a
pretty-printed `history.json` dataset.

The HTML file stays untouched - this produces an output artifact only.

Usage:
  python scripts/extract-visualisation.py --html path/to/city.html
  python scripts/extract-visualisation.py --html city.html --out data/history.json
  python scripts/extract-visualisation.py --html city.html --check
"""
import argparse
import json
from pathlib import Path

MARKER = "window.HISTORY_DATA = "


def find_payload(html: str) -> str:
    """Slice the raw JSON payload out of the embedded assignment.

    Loader code also mentions `window.HISTORY_DATA`, so only a marker
    followed by `{` counts as the embedded dataset."""
    pos = 0
    while True:
        start = html.find(MARKER, pos)
        if start == -1:
            raise SystemExit(
                "extract-visualisation: no '" + MARKER + "{' assignment found"
                " - the file carries no embedded dataset")
        start += len(MARKER)
        if html[start:start + 1] == "{":
            break
        pos = start
    end = html.find("</script>", start)
    if end == -1:
        raise SystemExit(
            "extract-visualisation: closing </script> after the payload not found")
    payload = html[start:end].strip()
    if not payload.endswith(";"):
        raise SystemExit("extract-visualisation: payload does not end with ';'")
    return payload[:-1]


def read_dataset(payload: str, source: Path) -> dict:
    """Parse the payload and refuse shapes the viewer could not consume."""
    try:
        data = json.loads(payload)  # resolves the <\/ escapes natively
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"extract-visualisation: embedded payload in {source} is not JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("versions"), list) \
            or not isinstance(data.get("categories"), list):
        raise SystemExit(
            f"extract-visualisation: payload in {source} is not a history.json "
            "dataset (object with `categories` and `versions` lists expected)")
    return data


def summary(data: dict) -> str:
    proj = (data.get("project") or {}).get("name", "?")
    return ("%s - %d versions, schema %s"
            % (proj, len(data.get("versions", [])), data.get("schema")))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract the embedded history.json dataset "
                    "from a single-file HTML visualisation")
    ap.add_argument("--html", required=True,
                    help="the packed visualisation file to read")
    ap.add_argument("--out", default="history.json",
                    help="output dataset file (default history.json)")
    ap.add_argument("--check", action="store_true",
                    help="report the embedded dataset without writing")
    a = ap.parse_args()

    html_path = Path(a.html)
    if not html_path.is_file():
        raise SystemExit("extract-visualisation: file not found: " + str(html_path))
    data = read_dataset(find_payload(html_path.read_text(encoding="utf-8")),
                        html_path)

    if a.check:
        print("extract-visualisation: embedded dataset found -", summary(data))
        return

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print("extracted -> %s (%s)" % (out, summary(data)))


if __name__ == "__main__":
    main()
