# Supported

This document is here to shine light on all of the supported versions
of the required dependencies. For example, this library requires a
Python interpreter, so the supported Python interpreter versions are
listed here. In the future, this document may hold supported dependency
commands (i.e., if some are restricted), and anything else that may be
added in the future!

## Python

- ### Version *(python3)*

  All Python interpreters with a version greater than or equal to
  ``3.11`` are compatible with this library.

## Dependencies — *standard*

There are currently no dependencies for this library.

---

## Dependencies — *build*

> **Note**: Build dependencies are only required when installing from
> source (e.g. cloning the repo and running
> `pip install -e ".[dev]" --no-build-isolation`). They are **not**
> needed when installing a pre-built wheel.

### C++ Compiler *(system)*

Required to compile the C++ extension modules. Install the appropriate
toolchain for your platform:

- **Windows** — MSVC via
  [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  — select the **"Desktop development with C++"** workload
- **macOS** — Clang via Xcode Command Line Tools:
  `xcode-select --install`
- **Linux** — GCC via your package manager, e.g.
  `sudo apt install build-essential`

### pybind11 — build

- #### Version *(pybind11) — build*

  Required to compile the C++ extension modules. Any version greater
  than or equal to ``2.12``.

### setuptools-scm

- #### Version *(setuptools-scm)*

  Any version greater than or equal to ``9.0``.

### setuptools — build

- #### Version *(setuptools) — build*

  Any version greater than or equal to ``82.0``.

### wheel — build

- #### Version *(wheel) — build*

  Any version! This is a thin installer utility with a stable API that
  essentially never breaks.

---

## Dependencies — *dev*

### isort

- #### Version *(isort)*

  Any version greater than or equal to ``5.0`` and less than ``6.0``.

### mypy

- #### Version *(mypy)*

  Any version greater than or equal to ``1.0`` and less than ``2.0``.

### ruff

- #### Version *(ruff)*

  Currently, ruff is still in active development. Due to possible
  changes that could cause issues in future ruff updates, the current
  version is restricted.

  Any version greater than or equal to ``0.1`` and less than ``0.2``.

### pre-commit

- #### Version *(pre-commit)*

  Any version greater than or equal to ``3.0`` and less than ``4.0``.

### pytest

- #### Version *(pytest)*

  Any version greater than or equal to ``7.0`` and less than ``8.0``.

### setuptools

- #### Version *(setuptools)*

  Any version greater than or equal to ``82.0`` and less than ``83.0``.

### wheel

- #### Version *(wheel)*

  Any version! This is a thin installer utility with a stable API that
  essentially never breaks.

### pybind11

- #### Version *(pybind11)*

  Required to compile the C++ extension modules. Any version greater
  than or equal to ``2.12``.
