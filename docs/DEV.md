# Working On MyLib

**Authors**: Evan Reumann

**Maintainers**: Evan Reuamnn

## First time setup

Clone the repository and change your directory to `mypytools`.

```bash
git clone https://github.com/cooldood155/mypytools
cd mypytools
```

Then run `scripts/dev_deps.py` to install or update the required dependencies, not available through pip (e.g. git, GitHub.CLI).

***Windows***:

```bash
py scripts/dev_deps.py
```

***macOS / Linux***:

```bash
python3 scripts/dev_deps.py
```

Optionally, install the dependencies manually:

- git `>=2.54.0` — [installing](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- github.CLI `>=2.92.0` — [installing](https://github.com/cli/cli#installation)

Install the library along with the dev dependencies, and hook up the git commit hooks.

```bash
pip install -e ".[dev]"   # installs mypytools + dev tools (ruff, pytest, mypy)
pre-commit install        # hooks up git commit hooks
```

The `-e` flag installs in **editable mode** — changes you make in `src/` are
immediately reflected without reinstalling.

You can omit this flag if necessary, manually updating by re-running `pip install ".[dev]"`.

## Day-to-day

- All **test modules** are written within the `tests/` directory
  - Each test module name starts with `test_` (e.g. `test_ansi_tools.py`)
  - Each test function/method begins with the `test_` prefix (e.g. `test_reset_intensity(self): ...`)
  - Each test class begins with the `Test` prefix (e.g. `TestANSIFormatterESCAPE`)
- All **Python modules** are written within the `src/mypytools/` directory
  - Follows the *src layout* convention; packages are initialized using an `__init__.py` initializer file
- All **C extension modules** are written within the `src/ext_modules/` directory
  - Each module name begins with `_c_` (e.g. `_c_to_list`)
  - Functions, methods, classes, and variables follow the Python conventions
    - If there is a pure Python counterpart to fallback to, ensure they share the same name
- All **documentation** is written within the `docs/` directory
  - Each doc file must be markdown

```bash
ruff check src/mypytools/          # lint
ruff check --fix src/mypytools/    # lint (auto fix)
ruff format --check src/mypytools/ # format
ruff format src/mypytools/         # format (auto fix)
mypy src/mypytools/ --strict       # type-check (strict)

pytest                  # run tests
pytest -x               # stop on first failure
pytest -k "test_<name>" # run a specific test

git add .
git commit -m "..."     # pre-commit hooks fire (ruff + pytest)
gh pr create --base main --head <working_branch> --title "<title>" --body "<body>"                # CI takes over
```

The path you pass to the commands does not have to be `src/mypytools/`.

Instead, it is highly recommended to explicitly target the files or package directories you want to evaluate. This avoids the large overhead of running these commands on the entire library.

### Ruff

1. **Linting**

    ```bash
    ruff check src/mypytools/
    ```

    Review everything [Ruff](https://docs.astral.sh/ruff/) has flagged, fix what's needed, then re-run *with* `--fix` once you're happy with what it'll change.

    Searches through the code for logical errors, bugs, code smells, and security risks, catching functional mistakes at build time.

2. **Formatting**

    ```bash
    ruff format --check src/mypytools/
    ```

    Review everything Ruff has flagged fix what's needed, then re-run *without* the `--check` flag once you're happy with what it'll change.

    Enforces style guidlines; applies [PEP 8](https://peps.python.org/pep-0008/) and Black-compatible [formatting rules](https://docs.astral.sh/ruff/rules/), such as consisten spacing, line-lengths, and quote usage.

3. **Type Checking**

    ```bash
    mypy src/mypytools/ --strict
    ```

    Type checks the passed in packages/modules that have type annotations conforming to [PEP 484](https://www.python.org/dev/peps/pep-0484/).

    The `--strict` flag is appended every time — a type related error will rarely appear at runtime without a corresponding mypy error, unless you explicitly circumvent mypy somehow (i.e., using a pragma: ``# type: ignore``).

## Release

```bash
# Bump version in pyproject.toml, then:
git tag v<x>.<y>.<z>
git push --tags        # triggers release CI
```
