import os
import sys
import types

import pytest

from src import helpers

# Add the project root to sys.path so `from src.xxx import ...` works.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# src/pass_classes.py does `import nltk` at module level.
# If nltk isn't installed, use a stub so the tests can still run.
try:
    import nltk  # noqa: F401
except ImportError:
    sys.modules["nltk"] = types.ModuleType("nltk")


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    """Point helpers.DATA_PATH to a temporary JSON file (not created yet)."""
    # from src import helpers

    path = tmp_path / "data.json"
    monkeypatch.setattr(helpers, "DATA_PATH", str(path))
    return path

# Add the project root to sys.path so `from src.xxx import ...` works.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# src/pass_classes.py does `import nltk` at module level.
# If nltk isn't installed, use a stub so the tests can still run.
try:
    import nltk  # noqa: F401
except ImportError:
    sys.modules["nltk"] = types.ModuleType("nltk")


# src/main_functions.py uses `import helpers`; alias it to src.helpers so
# both names are the SAME module object (patching DATA_PATH works for both).

# sys.modules.setdefault("helpers", helpers)


@pytest.fixture
def fake_input(monkeypatch):
    """Feed answers to input(): fake_input("1", "abc")."""

    def _set(*answers):
        it = iter(answers)

        def _input(prompt=""):
            try:
                return next(it)
            except StopIteration:
                raise AssertionError(f"Unexpected extra input(): {prompt!r}")

        monkeypatch.setattr("builtins.input", _input)

    return _set


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    """Point helpers.DATA_PATH to a temporary JSON file (not created yet)."""
    from src import helpers

    path = tmp_path / "data.json"
    monkeypatch.setattr(helpers, "DATA_PATH", str(path))
    return path

@pytest.fixture(autouse=True)
def tmp_data(tmp_path, monkeypatch):
    path = tmp_path / "data.json"
    monkeypatch.setattr(helpers, "DATA_PATH", str(path))
    return path