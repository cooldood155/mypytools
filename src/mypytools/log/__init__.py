"""
Developer diagnosic utilities for logging and exception handling.

**Exposed Modules**:
- `log.py` — developer diagnostic utilities for logging and exception handling.

**Provides**:
  Requires `StyleBuilder` from `mypytools.ansi_tools.style_builder`.

*From* ***log***:
- :func:`get_logger` — congigure and retrieve a file-backend `Logger` instance.
- :func:`setup_hooks` — install an ANSI-stylized gloabal exception hook.
"""

# Relative imports
from .log import get_logger as get_logger, setup_hooks as setup_hooks

__all__ = ['get_logger', 'setup_hooks']
