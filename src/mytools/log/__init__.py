"""
Developer diagnosic utilities for logging and exception handling.

Provides:
- :func:`get_logger`  — Congigure and retrieve a file-backend `Logger` instance.
- :func:`setup_hooks` — Install an ANSI-stylized gloabal exception hook.
"""

# Relative imports
from .log import get_logger as get_logger, setup_hooks as setup_hooks

__all__ = ['get_logger', 'setup_hooks']
