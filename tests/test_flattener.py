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
        'mypytools.flattener.list_filter',
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


# ——{ Imports }————————————————————————————————————————————————————————————————


def test_flattener_functions_exist(fresh_imports):
    """Test that the expected functions exist inside the modules."""
    _list_mod = fresh_imports['mypytools.flattener._list']
    list_mod = fresh_imports['mypytools.flattener.list_filter']

    assert hasattr(_list_mod, 'to_list')
    assert hasattr(list_mod, 'filter_none')


def test_package_level_exposure(fresh_imports):
    """Test that the top-level __init__ exposes the sub-tools."""
    flattener = fresh_imports['mypytools.flattener']

    assert hasattr(flattener, 'to_list')
    assert hasattr(flattener, 'filter_none')


# ——{ Imports }————————————————————————————————————————————————————————————————


mypytools.to_list()
