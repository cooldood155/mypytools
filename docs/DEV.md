# Working On MyPyTools

**Authors**: Evan Reumann

**Maintainers**: Evan Reumann

## First time setup

Clone the repository and change your directory to `mypytools`.

```bash
git clone https://github.com/cooldood155/mypytools
cd mypytools
```

### C++ Compiler

This project includes C++ extension modules built with pybind11. A
C++ compiler must be installed before running `pip install`:

- **Windows** — MSVC via
  [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  — select the **"Desktop development with C++"** workload
- **macOS** — Clang via Xcode Command Line Tools:
  `xcode-select --install`
- **Linux** — GCC via your package manager:
  `sudo apt install build-essential`

### Windows / macOS / Linux

Then run `scripts/dev_deps.py` to install or update the required
dependencies not available through pip (e.g. git, GitHub CLI).

```bash
python3 scripts/dev_deps.py
```

- Optionally, install the dependencies manually:

  - **git** `>=2.54.0` — [installing](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - **github.CLI** (*gh*) `>=2.92.0` — [installing](https://github.com/cli/cli#installation)

Install the library along with the dev dependencies, and hook up the
git commit hooks.

```bash
pip install -e ".[dev]" --no-build-isolation  # installs mypytools + dev tools (ruff, pytest, mypy)
pre-commit install                             # hooks up git commit hooks
```

The `-e` flag installs in **editable mode** — changes you make in
`src/` are immediately reflected without reinstalling.

The `--no-build-isolation` flag is required because the project
includes C++ extension modules built with pybind11, which must be
present in the environment at build time.

You can omit the `-e` flag if necessary, manually updating by
re-running `pip install ".[dev]" --no-build-isolation`.

## Day-to-day

- All **test modules** are written within the `tests/` directory

  - Each test module name starts with `test_` (e.g. `test_ansi_tools.py`)
  - Each test function/method begins with the `test_` prefix
    (e.g. `test_reset_intensity(self): ...`)
  - Each test class begins with the `Test` prefix
    (e.g. `TestANSIFormatterESCAPE`)

- All **Python modules** are written within `src/mypytools/` or any
  of its subdirectories

  - Follows the *src layout* convention; packages are initialized
    using an `__init__.py` initializer file

- All **C++ extension modules** are written within their parent
  package directory alongside their Python siblings

  - Each module name begins with `_` (e.g. `_list.cpp`)
  - Compiled via pybind11; a corresponding `setup.py` at the project
    root registers extensions with setuptools
  - Functions, methods, classes, and variables follow Python
    naming conventions

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

  The path you pass to the commands does not have to be
  `src/mypytools/`. It is *highly* recommended to explicitly target
  the files or package directories you want to evaluate — this avoids
  the overhead of running these commands across the entire library.

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

1. **Import Sorting** — Checks import statements for sorting and formatting errors, catching issues at build time.

```bash
isort src/mypytools/ --check-only --diff
```

- **Manual**: Run `isort <path>` to auto-sort imports in place.

---
<!-- markdownlint-disable MD029 -->
### Ruff

1. **Linting** — Searches through the code for logical errors, bugs, code smells, and security risks, catching functional mistakes at build time.

```bash
ruff check src/mypytools/
```

- **Manual**: Review everything [Ruff](https://docs.astral.sh/ruff/)
  has flagged, fix what's needed, then re-run *with* `--fix` once
  you're happy with what it'll change.

2. **Formatting** — Enforces style guidelines; applies [PEP 8](https://peps.python.org/pep-0008/) and Black-compatible [formatting rules](https://docs.astral.sh/ruff/rules/), such as consistent spacing, line lengths, and quote usage.

```bash
ruff format --check src/mypytools/
```

- **Manual**: Review everything Ruff has flagged, fix what's needed,
  then re-run *without* the `--check` flag once you're happy with
  what it'll change.

---
<!-- markdownlint-enable MD029 -->

### MyPy

- **Type Checking**

```bash
mypy src/mypytools/ --strict
```

  Type checks the passed packages/modules against type annotations
  conforming to [PEP 484](https://www.python.org/dev/peps/pep-0484/).

  The `--strict` flag is always appended — a type-related error will
  rarely appear at runtime without a corresponding mypy error, unless
  you explicitly circumvent mypy (e.g. `# type: ignore`).

---

### Pytest

- **Run Tests**

```bash
pytest -x  # fail/exit on first test failure
```

  Runs all tests prefixed with `test_` within the root `tests/`
  directory, inside modules prefixed with `test_` (e.g.
  `test_custom_compare()` within `tests/test_ansi_tools.py`).

  The `-x` flag causes pytest to exit on the first failed test. To
  run all tests regardless of failures, run `pytest` directly.

  Run a specific test with `pytest -k "test_<name>"` — useful when
  you've fixed a failing test and want to verify just that case.

## Release

### GitHub

1. Go to **Actions → Bump Version → Run workflow**
2. Enter the new version (e.g. `0.1.0a2`)
3. Click **Run** — this bumps `pyproject.toml`, tags the commit, and
   triggers the release CI

### GitHub CLI

```bash
gh workflow run bump.yml --field version=0.1.0a2
```

Optionally watch it run live:

```bash
gh run watch  # choose the most recently triggered workflow
```

---

### Workflow

1. Triggered (via [GitHub](#github) or [GitHub CLI](#github-cli))
2. Bumps `pyproject.toml`
3. Commits
4. Tags
5. Pushes
6. `release.yml` fires
