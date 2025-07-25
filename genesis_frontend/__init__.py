"""Compatibility wrapper for the genesis_frontend package used in tests."""
import importlib.util
import sys
from pathlib import Path

_package_root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    __name__,
    _package_root / "__init__.py",
    submodule_search_locations=[str(_package_root)],
)
module = importlib.util.module_from_spec(spec)
sys.modules[__name__] = module
spec.loader.exec_module(module)
