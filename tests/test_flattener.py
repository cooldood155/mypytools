"""Tests for the ``src/mytools/flattener/`` package."""

# Standard library imports
from importlib import import_module
from sys import stderr, exit as sysexit, modules

# Third party imports
from pytest import raises, fixture, fail

try:
    # Project imports
    import mypytools
except ModuleNotFoundError:
    print(
        'ModuleNotFoundError: mypytools is not installed.\n'
        'Install it from: https://github.com/cooldood155/mypytools/releases',
        file=stderr,
    )
    sysexit(1)


@fixture
def fresh_imports():
    """
    Dynamically imports packages and ensures they are wiped after the test.

    Catches any ModuleNotFoundError's or ImportError's that may occur.
    """
    # Define import targets
    module_names = [
        'mypytools.flattener',
        'mypytools.flattener._list',
        'mypytools.flattener.list',
    ]

    # Perform dynamic imports
    imported_modules = {}
    try:
        for name in module_names:
            imported_modules[name] = import_module(name)
    except (ModuleNotFoundError, ImportError) as e:
        fail(f'Setup import failed for {getattr(e, "name", "unknown")}: {e}')

    # YIELD: pass the imported modules to pytest.fixture
    yield imported_modules

    # TEARDOWN: remove the imported modules
    for name in module_names:
        if name in modules:
            del modules[name]
