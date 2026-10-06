"""Focused contract tests for the lens-skill report-production and maintenance tools.

Each hyphenated script under `scripts/` is loaded from its file path so `unittest`
discovery does not depend on importable module names.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_script(name: str):
    """Load `scripts/<name>` (for example `format-table.py`) as a module."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_").removesuffix(".py"), SCRIPTS / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
