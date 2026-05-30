"""
Zero-dependency and third-party wrapper utilities for Python.

A wide range of **Zero-dependency Modules/Packages**, **Single-file Modules**,
and **wrapper/helper** modules and packages for third-party libraries.

**Exposes Packages**:

- :mod:`ansi_tools` — ANSI terminal text formatting and styling utilities.
- :mod:`flattener` — heterogeneous iterable filtering and flattening utilities.
- :mod:`log` — Developer diagnostic utilities for logging and exception
  handling.

---

**Exposed Modules**:

*From* ***ansi_tools***:

- :mod:`~mypytools.ansi_tools.formatter` — low-level ANSI terminal text
  formatting.
- :mod:`~mypytools.ansi_tools.style_builder` — high-level ANSI terminal styling
  and pre-formatted printable styles.

*From* ***flattener***:

- :mod:`~mypytools.flattener.list` — list flattening and filtering utilities.
- :mod:`~mypytools.flattener._list` — C++ list flattening/filtering utilities.

*From* ***log***:

- :mod:`~mypytools.log.log` — configure and retrieve a file-backend `Logger`
  instance and/or install an ANSI-stylized global exception hook.

---

**Exposed Objects**:

*From* ***ansi_tools.formatter***:

- :class:`ANSIFormatter` — constants and a low-level escape-sequence builder.

*From* ***ansi_tools.style_builder***:

- :class:`StyleBuilder` [class] — a fluent builder for composing and applying
  ANSI styles.
- :func:`bubble` [func] — a pre-styled diagnostic string for surfacing
  assertion or validation errors in the terminal.

*From* ***flattener.list***:

- :func:`to_list` — accepts any mix of scalars, iterables, and mappings and
  collapses them into a flat ``list``.

*From* ***log.log***:

- :func:`get_logger` — Congigure and retrieve a file-backend `Logger` instance.
- :func:`setup_hooks` — Install an ANSI-stylized gloabal exception hook.
"""

__version__ = '0.1.0'

# Relative imports
from .ansi_tools import (
    ANSIFormatter as ANSIFormatter,
    StyleBuilder as StyleBuilder,
    bubble as bubble,
)
from .flattener import filter_none as filter_none, to_list as to_list
from .log import get_logger as get_logger, setup_hooks as setup_hooks

__all__ = [
    'ANSIFormatter',
    'StyleBuilder',
    'bubble',
    'filter_none',
    'get_logger',
    'setup_hooks',
    'to_list',
]
