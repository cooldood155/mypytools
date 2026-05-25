# Using MyTools in Another Project

## Full Installation

If you chose to install the entire library via pip, then you can access any package or module within the library via `mypytools.<module/subpackage>...` (see the [import system](https://peps.python.org/pep-0420/) or [packages](https://docs.python.org/3/tutorial/modules.html#packages) Python documentation).

## Partial *Install*

If you chose to grab specific subpackages or modules from the library yourself the import statements in the above documentation may not perfectly represent the import statement you should use.

For example, if you grab the two modules from `mypytools > ansi_tools` independently and not the entire package, the import statements `import mypytools.ansitools`, `import ... from mypytools.ansitools`, and `from mypytools.ansitools import ...` will not work. You must instead import everything directly from the modules using relative imports (e.g. `from ../libs/formatter import ...` or `import ... from ../libs/style_builder`).

- This can be highly customized

---

## Provided Packages

*mypytools*:

- [`ansi_tools`](./packages/ANSI_TOOLS.md) – ANSI terminal text formatting and styling utilities.
- [`flattener`](./packages/FLATTENER.md) – Utilities for flattening and filtering heterogeneous iterables.
- [`log`](./packages/LOG.md) – Developer diagnosic utilities for logging and exception handling.

## Provided Modules

*mypytools > ansi_tools*:

- [`formatter`](./packages/ANSI_TOOLS.md#publically-exposed-modules)
- [`style_builder`](./packages/ANSI_TOOLS.md#publically-exposed-modules)

*mypytools > flattener*:

- [`list`](./packages/FLATTENER.md#publically-exposed-modules)

*mypytools > log*:

- [`log`](./packages/LOG.md#publically-exposed-modules)
