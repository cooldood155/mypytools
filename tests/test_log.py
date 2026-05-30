"""Tests for the ``src/mytools/log/`` package."""

# Standard library imports
from importlib import import_module
from sys import stderr, exit as sysexit, modules

# Third party imports
from pytest import fixture, fail

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
        'mypytools.log',
        'mypytools.log.log',
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


def test_log_functions_exist(fresh_imports):
    """Test that the expected functions exist inside the modules."""
    log_mod = fresh_imports['mypytools.log.log']

    assert hasattr(log_mod, 'get_logger')
    assert hasattr(log_mod, 'setup_hooks')


def test_package_level_exposure(fresh_imports):
    """Test that the top-level __init__ exposes the sub-tools."""
    log = fresh_imports['mypytools.log']

    assert hasattr(log, 'get_logger')
    assert hasattr(log, 'setup_hooks')


# Use mypytools module import to avoid ruff error, will add tests soon
mytools = mypytools
