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

### Windows / macOS / Linux

```bash
python3 scripts/dev_deps.py
```

- Optionally, install the dependencies manually:

  #### git `>=2.54.0` — [installing](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

  #### github.CLI (*gh*) `>=2.92.0` — [installing](https://github.com/cli/cli#installation)

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

- All **Python modules** are written within `src/mypytools/` or any of its parent directories

  - Follows the *src layout* convention; packages are initialized using an `__init__.py` initializer file

- All **C extension modules** are written within a `.../c_modules/` directory

  - Each module name begins with `_c_` (e.g. `_c_to_list`)
  - Functions, methods, classes, and variables follow the Python conventions

- All **documentation** is written within the `docs/` directory

  - Each doc file must be markdown

## Commands

### Local (manual)

- **Auto-fix** [ruff](#ruff) — **fail** on [mypy](#mypy)/[pytest](#pytest) errors

  ```bash
  #— Ruff ————————————————————————————————————
  ruff check --fix src/mypytools/  # lint (auto fix)
  ruff format src/mypytools/       # format (auto fix)

  #— MyPy ————————————————————————————————————
  mypy src/mypytools/ --strict  # type-check (strict)

  #— Pytest ——————————————————————————————————
  pytest -x                # stop on first failure
  pytest -k "test_<name>"  # run a specific test
  pytest                   # run all tests
  ```

  The path you pass to the commands does not have to be `src/mypytools/`.

  Instead, it is *highly* recommended to explicitly target the files or package directories you want to evaluate. This avoids the large overhead of running these commands across the entire library.

### Pre-commit hook

- **Auto-fix** [isort](#isort)/[ruff](#ruff) — **fail** on [mypy](#mypy)/[pytest](#pytest) errors

  ```bash
  #— isort ———————————————————————————————————
  isort src/mypytools/  # sort imports (auto fix)

  #— Ruff ————————————————————————————————————
  ruff check --fix src/mypytools/  # lint (auto fix)
  ruff format src/mypytools/       # format (auto fix)

  #— MyPy ————————————————————————————————————
  mypy src/mypytools/ --strict  # type-check (strict)

  #— Pytest ——————————————————————————————————
  pytest -x  # stop on first failure
  ```

### CI

- **Fail** on [isort](#isort)/[ruff](#ruff)/[mypy](#mypy)/[pytest](#pytest) errors

  ```bash
  #— isort ———————————————————————————————————
  isort src/mypytools/ --check-only --diff  # check imports

  #— Ruff ————————————————————————————————————
  ruff check src/mypytools/           # check linting
  ruff format --check src/mypytools/  # check formatting

  #— MyPy ————————————————————————————————————
  mypy src/mypytools/ --strict  # type-check (strict)

  #— Pytest ——————————————————————————————————
  pytest -x  # stop on first failure

  #— GitHub ——————————————————————————————————
  git add .
  git commit -m "..."  # pre-commit hooks fire (isort + ruff + mypy + pytest)
  gh pr create         # CI takes over (isort + ruff + mypy + pytest)
  ```

---

### Isort

1. **Import Sorting**

    ```bash
    isort src/mypytools/ --check-only --diff
    ```

    Looks at import statements for sorting and formatting errors, catching errors at build time.

    - **Manual**:

        Just run `isort <path> --check-only --diff`, imports will be auto-sortted by isort.

---

### Ruff

1. **Linting**

    ```bash
    ruff check src/mypytools/
    ```

    Searches through the code for logical errors, bugs, code smells, and security risks, catching functional mistakes at build time.

    - **Manual**:

        Review everything [Ruff](https://docs.astral.sh/ruff/) has flagged, fix what's needed, then re-run *with* `--fix` once you're happy with what it'll change.

2. **Formatting**

    ```bash
    ruff format --check src/mypytools/
    ```

    Enforces style guidlines; applies [PEP 8](https://peps.python.org/pep-0008/) and Black-compatible [formatting rules](https://docs.astral.sh/ruff/rules/), such as consisten spacing, line-lengths, and quote usage.

    - **Manual**:

        Review everything Ruff has flagged fix what's needed, then re-run *without* the `--check` flag once you're happy with what it'll change.

---

### MyPy

- **Type Checking**

  ```bash
  mypy src/mypytools/ --strict
  ```

  Type checks the passed in packages/modules that have type annotations conforming to [PEP 484](https://www.python.org/dev/peps/pep-0484/).

  The `--strict` flag is appended every time — a type related error will rarely appear at runtime without a corresponding mypy error, unless you explicitly circumvent mypy somehow (i.e., using a pragma: ``# type: ignore``).

---

### Pytest

- **Run Tests**

  ```bash
  pytest -x # Fail/Exit on first test fail
  ```

  Runs all of tests prefixed with `test_` within the root `tests/` directory inside of modules prefixed with `test_` (i.e., the `test_custom_compare()` method within the `tests/test_ansi_tools.py` module).

  - The `-x` flag causes pytest to exit on the first failed test. If you would prefer to run all tests to check everything that is failing, run *`pytest`* directly

  You can also run a specific tests using `pytest -k "test_<name>"`. This can be usefull if you catch a failing test, attempt to resolve the issue, and want to run that specific test again to check if you succeeded.

## Release

### GitHub

1. Go to **Actions → Bump Version → Run workflow**
2. Enter the new version (e.g. `0.3.0`)
3. Click **Run** — this bumps `pyproject.toml`, tags the commit, and triggers the release CI

### GitHub.CLI

``gh workflow run bump.yml --field version=0.3.0``

- You can also watch it run live by running ``gh run watch`` after running the bump workflow via the command above and choosing the most recently ran workflow
  - This is optional and only needed if you want to monitor progress

---

### Workflow

1. triggered (via [GitHub](#github) or [GitHub.CLI](#githubcli))
2. bumps pyproject.toml
3. commits
4. tags
5. pushes
6. release.yml fires
