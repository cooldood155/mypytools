# Working On MyLib

**Authors**: Evan Reumann

**Maintainers**: Evan Reuamnn

## First time setup

```bash
git clone https://github.com/cooldood155/mypytools
cd mytools
pip install -e ".[dev]"   # installs mytools + dev tools (ruff, pytest, mypy)
pre-commit install        # hooks up git commit hooks
```

The `-e` flag installs in **editable mode** — changes you make in `src/` are
immediately reflected without reinstalling.

You can omit this flag if necessary.

## Day-to-day

Commands are ran from the root `mytools` directory.

- All **tests** written in `tests/`
  - Eeach test module name starts with `test_` (i.e. `test_ansi_tools.py`)
- All **source code** written in `src/mytools`
  - Follows the *src layout* convention; packages are initialized using an `__init__.py` initializer file.

```bash
ruff check src/mytools/          # lint
ruff check --fix src/mytools/    # lint (auto fix)
ruff format --check src/mytools/ # format
ruff format src/mytools/         # format (auto fix)
mypy src/mytools/ --strict       # type-check (strict)

pytest                 # run tests
pytest -x              # stop on first failure
pytest -k "test_name"  # run a specific test

git add .
git commit -m "..."    # pre-commit hooks fire (ruff + pytest)
git push               # CI takes over
```

The path you pass to the commands does not have to be `src/mytools/`.

Instead, it is highly recommended to explicitly target the files or package directories you want to evaluate. This avoids the large overhead of running these commands on the entire library.

### Ruff

1. **Linting**

    ```bash
    ruff check src/mytools/
    ```

    Review everything [Ruff](https://docs.astral.sh/ruff/) has flagged, fix what's needed, then re-run *with* `--fix` once you're happy with what it'll change.

    Searches through the code for logical errors, bugs, code smells, and security risks, catching functional mistakes at build time.

2. **Formatting**

    ```bash
    ruff format --check src/mytools/
    ```

    Review everything Ruff has flagged fix what's needed, then re-run *without* the `--check` flag once you're happy with what it'll change.

    Enforces style guidlines; applies [PEP 8](https://peps.python.org/pep-0008/) and Black-compatible [formatting rules](https://docs.astral.sh/ruff/rules/), such as consisten spacing, line-lengths, and quote usage.

3. **Type Checking**

    ```bash
    mypy src/mytools/ --strict
    ```

    Type checks the passed in packages/files that have type annotations conforming to [PEP 484](https://www.python.org/dev/peps/pep-0484/).

    The `--strict` flag is appended every time — a type related error will rarely appear at runtime without a corresponding mypy error, unless you explicitly circumvent mypy somehow (i.e., using a pragma: ``# type: ignore``).

## Release

```bash
# Bump version in pyproject.toml, then:
git tag v<x>.<y>.<z>
git push --tags        # triggers release CI
```
