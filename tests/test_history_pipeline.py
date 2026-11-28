"""End-to-end tests for the reference pipeline in `assets/history-pipeline/`."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS

PIPELINE = SCRIPTS.parent / "assets" / "history-pipeline"
STAGES = ("extract_git.py", "extract_docs.py", "build_history.py")


def git(repo: Path, *args: str) -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME="Example Author", GIT_AUTHOR_EMAIL="a@example.com",
               GIT_COMMITTER_NAME="Example Author", GIT_COMMITTER_EMAIL="a@example.com")
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


def commit(repo: Path, files: dict[str, str], message: str, date: str) -> None:
    for name, text in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, "--date", date)


def make_repo(root: Path) -> Path:
    """A service whose version starts in a sub-package and later moves to the root manifest."""
    repo = root / "service"
    repo.mkdir()
    git(repo, "init", "-q")
    commit(repo, {"server/package.json": json.dumps({"version": "1.0.0", "dependencies":
                                                     {"left-pad": "1.0.0"}}),
                  "server/src/app.ts": "export const a = 1;\n",
                  "README.md": "# Service\n\nAn example service.\n"},
           "feat: initial service", "2025-01-01T10:00:00")
    commit(repo, {"server/src/app.ts": "export const a = 2;\n",
                  "docs/change/1.0.0/change-a.md": "# Change A\n\n**Type:** Fix\n\n## Summary\n\n"
                                                   "Fixes the first value.\n"},
           "fix: correct the value", "2025-01-05T10:00:00")
    commit(repo, {"server/package.json": json.dumps({"version": "1.1.0", "dependencies":
                                                     {"left-pad": "1.1.0"}})},
           "chore(release): bump the version to 1.1.0", "2025-01-10T10:00:00")
    commit(repo, {"package.json": json.dumps({"version": "1.2.0"}),
                  "server/src/app.test.ts": "test('a', () => {});\n"},
           "chore(release): move the version to the root and bump to 1.2.0",
           "2025-02-01T10:00:00")
    commit(repo, {"server/src/app.ts": "export const a = 3;\n",
                  "docs/plan/1.2.0/plan-b.md": "# Plan B\n\nNext steps.\n"},
           "feat: next value", "2025-02-05T10:00:00")
    return repo


def run_pipeline(root: Path, repo: Path, name: str, **config) -> dict:
    workspace = root / name
    scripts = workspace / "gathering" / "scripts"
    scripts.mkdir(parents=True)
    for script in ("common.py", *STAGES):
        shutil.copy(PIPELINE / script, scripts / script)
    (workspace / "gathering" / "config.json").write_text(
        json.dumps({"repo": str(repo), "ref": "HEAD", "prior": "gathering/out/none.json",
                    "categories": [{"id": c, "label": c, "color": "#94a3b8", "order": n * 10}
                                   for n, c in enumerate(["release", "feature", "fix", "chore",
                                                          "change", "merge", "dependency",
                                                          "plan", "docs", "test"])],
                    **config}), encoding="utf-8")
    for stage in STAGES:
        result = subprocess.run([sys.executable, stage], cwd=scripts, capture_output=True,
                                text=True, timeout=120)
        if result.returncode:
            raise AssertionError(result.stderr)
    return json.loads((workspace / "out" / "history.json").read_text(encoding="utf-8"))


class HistoryPipelineTests(unittest.TestCase):
    def test_full_run_follows_a_moving_version_manifest(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            data = run_pipeline(root, make_repo(root), "full")
            self.assertEqual([v["version"] for v in data["versions"]], ["1.0.0", "1.1.0", "1.2.0"])
            self.assertEqual(data["versions"][-1]["kind"], "developing")
            refs = [e.get("ref") for v in data["versions"] for e in v["events"]]
            self.assertIn("docs/change/1.0.0/change-a.md", refs)
            change = next(e for e in data["versions"][0]["events"]
                          if e.get("ref") == "docs/change/1.0.0/change-a.md")
            self.assertEqual(change["type"], "fix")
            validate = subprocess.run([sys.executable, str(SCRIPTS / "validate-history.py"),
                                       str(root / "full" / "out" / "history.json")],
                                      capture_output=True, text=True)
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

    def test_from_version_output_splices_onto_the_prior_dataset(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            repo = make_repo(root)
            prior = run_pipeline(root, repo, "prior")
            prior["view"] = {"layout": "islands", "theme": "dark", "palette": "green"}
            (root / "prior.json").write_text(json.dumps(prior), encoding="utf-8")
            tail = run_pipeline(root, repo, "tail", from_version="1.2.0")
            self.assertEqual([v["version"] for v in tail["versions"]], ["1.2.0"])
            merged = subprocess.run(
                [sys.executable, str(SCRIPTS / "continue-history.py"), "merge", "--prior",
                 str(root / "prior.json"), "--update", str(root / "tail" / "out" / "history.json"),
                 "--out", str(root / "continued.json")], capture_output=True, text=True)
            self.assertEqual(merged.returncode, 0, merged.stderr)
            data = json.loads((root / "continued.json").read_text(encoding="utf-8"))
            self.assertEqual([v["version"] for v in data["versions"]], ["1.0.0", "1.1.0", "1.2.0"])
            self.assertEqual(data["view"]["palette"], "green")


if __name__ == "__main__":
    unittest.main()
