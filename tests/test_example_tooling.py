"""The tooling around the published example still imports.

scripts/gen_example.py and examples/HealthDataset-validation-check.ipynb borrow
helpers from tests/ and scripts/, and nothing in CI runs either: a refactor of
those helpers broke both in 2026-10-21 without a test failing. These checks only
import -- they do not regenerate the example or run the notebook.
"""

import importlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_gen_example_imports():
    module = importlib.import_module("gen_example")
    assert callable(module.main)


def test_validation_notebook_imports_resolve():
    """Run the notebook's import cell (its first code cell) from the examples/ folder."""
    notebook = json.loads((REPO_ROOT / "examples" / "HealthDataset-validation-check.ipynb").read_text(encoding="utf-8"))
    first_code_cell = next(c for c in notebook["cells"] if c["cell_type"] == "code")
    exec(compile("".join(first_code_cell["source"]), "<notebook import cell>", "exec"), {})
