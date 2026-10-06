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


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.common = load_script("common.py")

    def test_frontmatter_parses_name(self):
        issues: list[str] = []
        fields, body = self.common.parse_frontmatter(
            "---\nname: lens-skill\ndescription: x\n---\nbody\n", issues
        )
        self.assertEqual(fields.get("name"), "lens-skill")
        self.assertIn("body", body)


if __name__ == "__main__":
    unittest.main()
