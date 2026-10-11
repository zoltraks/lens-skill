"""Contract tests for the skill-maintenance tools in `scripts/`."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests import ROOT, load_script


class TestValidateSkill(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-skill.py")

    def test_frontmatter_requires_name_and_description(self):
        issues: list[str] = []
        self.validator.validate_frontmatter(Path("lens-skill"), {}, issues)
        self.assertTrue(any("name" in item for item in issues))
        self.assertTrue(any("description" in item for item in issues))

    def test_body_line_cap_is_500(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("x\n" * 501, encoding="utf-8")
            issues: list[str] = []
            self.validator.validate_body(root, "body text\n", issues)
            self.assertTrue(any("500" in item for item in issues))

    def test_current_skill_under_cap(self):
        issues: list[str] = []
        self.validator.validate_body(ROOT, "body text\n", issues)
        self.assertFalse(any("maximum is 500" in item for item in issues))


class TestCheckContents(unittest.TestCase):
    def setUp(self):
        self.checker = load_script("check-contents.py")

    def test_tolerance_is_three(self):
        self.assertEqual(self.checker.TOLERANCE, 3)

    def test_fix_snaps_by_name_past_unlisted_section(self):
        # A `##` section inserted without a Contents row must not drag the
        # rows below it onto the wrong heading - the failure mode that made
        # proximity-only snapping corrupt every anchor after an insertion.
        lines = (
            "# Doc\n\n## Contents\n\n"
            "| Section | Line |\n|---|---|\n"
            "| Alpha | 5   |\n"
            "| Beta | 7   |\n\n"
            "## Alpha\n\n## Inserted\n\n## Beta\n"
        ).splitlines()
        fences = self.checker.fenced_flags(lines)
        contents_at = 2
        headings = [
            (index, self.checker.HEADING.match(line).group(1))
            for index, line in enumerate(lines)
            if not fences[index] and self.checker.HEADING.match(line)
        ]
        rows = self.checker.collect_rows(lines, fences, contents_at)
        out = self.checker.fix_rows(lines, rows, headings, contents_at)
        self.assertIn("| Alpha | 10   |", out)
        self.assertIn("| Beta | 14   |", out)

    def test_fix_falls_back_to_nearest_for_unnamed_rows(self):
        lines = (
            "# Doc\n\n## Contents\n\n"
            "| Section | Line |\n|---|---|\n"
            "| Grouped Area | 5    |\n\n"
            "## Alpha\n\n## Beta\n"
        ).splitlines()
        fences = self.checker.fenced_flags(lines)
        contents_at = 2
        headings = [
            (index, self.checker.HEADING.match(line).group(1))
            for index, line in enumerate(lines)
            if not fences[index] and self.checker.HEADING.match(line)
        ]
        rows = self.checker.collect_rows(lines, fences, contents_at)
        out = self.checker.fix_rows(lines, rows, headings, contents_at)
        self.assertIn("| Grouped Area | 9    |", out)


class TestScanStandards(unittest.TestCase):
    def setUp(self):
        self.scanner = load_script("scan-standards.py")

    def test_skeleton_extracts_headings_and_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example-standard.md"
            path.write_text(
                "# Example Standard\n\n**Version:** 1.4\n\n## Scope\n\n## Rules\n",
                encoding="utf-8",
            )
            row = self.scanner.skeleton(path)
            self.assertEqual(row["file"], "example-standard.md")
            self.assertEqual(row["version"], "1.4")
            self.assertEqual(row["headings"], ["Scope", "Rules"])
            self.assertEqual(row["title"], "Example Standard")

    def test_scan_is_sorted_and_markdown_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "b-standard.md").write_text("# B\n", encoding="utf-8")
            (root / "a-standard.md").write_text("# A\n", encoding="utf-8")
            (root / "notes.txt").write_text("not markdown\n", encoding="utf-8")
            rows = self.scanner.scan(root)
            self.assertEqual([row["file"] for row in rows], ["a-standard.md", "b-standard.md"])

    def test_missing_version_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plain.md"
            path.write_text("# Plain\n\n## Body\n", encoding="utf-8")
            self.assertEqual(self.scanner.skeleton(path)["version"], "-")

    def test_main_rejects_non_directory(self):
        self.assertEqual(self.scanner.main(["definitely-missing-dir-xyz"]), 2)


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.common = load_script("common-helpers.py")

    def test_frontmatter_parses_name(self):
        issues: list[str] = []
        fields, body = self.common.parse_frontmatter(
            "---\nname: lens-skill\ndescription: x\n---\nbody\n", issues
        )
        self.assertEqual(fields.get("name"), "lens-skill")
        self.assertIn("body", body)


if __name__ == "__main__":
    unittest.main()
