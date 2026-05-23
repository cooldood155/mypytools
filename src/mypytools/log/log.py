"""
Developer diagnosic utilities for logging and exception handling.

Provides automated stack-inferred file logging with environment-aware
formatting styles alongside a polished, color-coded global exception hook
for readable terminal tracebacks.

Listed here respectively:
    :func:`get_logger`
    :func:`setup_hooks`
"""

# Standard library imports
import os
import sys
from inspect import getmodule, stack
from logging import FileHandler, Formatter, Logger, getLogger
from pathlib import Path
from traceback import extract_tb
from types import TracebackType

try:
    # Project imports
    from mypytools.ansi_tools import StyleBuilder
except ImportError:
    try:
        # Project imports
        from mypytools.ansi_tools.style_builder import StyleBuilder
    except ImportError as e:
        raise ImportError(
            'Failed to find StyleBuilder from mypytools.ansi_tools '
            'or mypytools.ansi_tools.style_builder'
        ) from e

__all__ = ['get_logger', 'setup_hooks']


# ——{ Helpers }—————————————————————————————————————————————————————————————————


def _load_local_env() -> None:
    r"""
    Looks for `.env` in the current working directory.

    - *the first one discovered is the one that is used*.

    If one is found:

    1. Open it in read (`r`) mode.
    2. Clean up whitespace & skip empty lines/comments.
    3. Split at the first `=` sign only; `<key> = <value>`.
    4. Strips leading/trailing space, newline chars, and single/double quotes.
    """
    env_path = Path.cwd() / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('\'"')


_load_local_env()

# ——{ get-logger }——————————————————————————————————————————————————————————————


def get_logger(
    log_path: Path | None = None,
    level: int | None = None,
    name: str | None = None,
    env: str | None = None,
) -> Logger:
    """
    Configure and retrieve a file-backend `Logger` instance.

    Dynamically inspects the call stack to infer the calling module's name if
    not explicitly provided, sets environment-specific formatting, and attaches
    a single `FileHandler`.

    Args:
        log_path (Path | None):
          The file path where logs will be written. Overrides
          the `'PYTOOLS_LOG_DIR'` environment variable if provided. Defaults
          to the current working directory. Stores the log file with the
          name: `<module_name>.log`.
        level (int | None):
          The logging threshold level (e.g., 'debug', 'info'). Overrides
          the `'PYTOOLS_LOG_LEVEL'` environment variable if provided.
          Defaults to `debug`.
        name (str | None):
          The explicit name for the logger. If omitted, it is inferred from
          the calling module's __name__. Overrides the `PYTOOLS_LOG_SHARED`
          environment variable if provided.
        env (str | None):
          The environment mode ('dev' or 'prod'). Overrides the
          `'PYTOOLS_LOG_MODE'` environment variable if provided. Defaults to
          `dev` if no environment variable is provided.

    Returns:
        A configured `Logger` instance attached to a dedicated `FileHandler`.

    Notes:
        See more details on arguments, specifically environment keys and
        values, at :doc:`/docs/packages/LOG.md`.
    """
    if not name:
        frame = stack()[1]
        module = getmodule(frame[0])
        name = module.__name__ if module else '__main__'

    logger = getLogger(name)

    log_dir = Path(os.environ.get('PYTOOLS_LOG_DIR', 'NONE'))
    logger.setLevel(
        level or os.environ.get('PYTOOLS_LOG_LEVEL', 'debug') or 'debug'
    )
    environment = env or os.environ.get('PYTOOLS_LOG_MODE', 'dev').lower()

    log_path = (
        log_path or log_dir / f'{name}.log'
        if str(log_dir) != 'NONE'
        else Path.cwd() / f'{name}.log'
    )

    if not logger.handlers:
        handler = FileHandler(log_path, mode='w', encoding='UTF-8')

        # ——{ Format Selection }————————————————————————————
        if environment == 'prod':
            # Production: Single-line, tab-separated, strict columns
            fmt = (
                '%(asctime)s\t%(levelname)-8s — PROD\t%(filename)s:%(lineno)d\t'
                '%(funcName)s\t%(message)s'
            )
        elif environment == 'dev':
            # Development: Multi-line, visually spaced, human-readable
            fmt = (
                '%(asctime)s @--> %(filename)s %(lineno)d %(funcName)s '
                '!--> [%(levelname)s — DEV] ::\n\t%(message)s\n'
            )
        else:
            raise OSError(
                "Environment variables 'PYTOOLS_ENV_MODE' is not one of the "
                'allowed environment modes — see here '
                '[https://github.com/cooldood155/mypytools/blob/main/README.md]'
                '(https://github.com/cooldood155/mypytools/blob/main/README.md)'
            )

        handler.setFormatter(
            Formatter(
                fmt=fmt,
                datefmt=r'%m-%d-%Y %H.%M.%S',
            )
        )
        logger.addHandler(handler)

    return logger


# ——{ setup-hooks }—————————————————————————————————————————————————————————————


def setup_hooks() -> None:
    """
    Install an ANSI-stylized global exception hook.

    Overrides `sys.excepthook` with a polished, color-coded trace viewer that
    extracts source code lines, highlights errors, and formats module paths
    cleanly within the terminal.
    """

    # --{ Exception-Hook }---------
    def custom_excepthook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: TracebackType | None,
    ) -> None:
        # -- Header --
        header = (
            StyleBuilder()
            .bold()
            .fg(255, 80, 80)
            .apply(f' {exc_type.__name__} ', finish=True)
        )
        print(f'\n{header}')

        # -- Message --
        exc_msg = str(exc_value)
        if not StyleBuilder.ANSI_ESCAPE_RE.search(exc_msg):
            exc_msg = (
                StyleBuilder().fg(255, 160, 160).apply(exc_msg, finish=True)
            )
        print(f'{exc_msg}\n')

        # -- Traceback frames --
        frames = extract_tb(exc_tb)
        print(
            StyleBuilder()
            .bold()
            .fg(180, 180, 180)
            .apply('Traceback:', finish=True)
        )

        for i, frame in enumerate(frames):
            is_last = i == len(frames) - 1

            path = Path(frame.filename)
            folder = (
                StyleBuilder()
                .dim()
                .fg(120, 120, 120)
                .apply(str(path.parent) + '\\', finish=True)
            )
            file = (
                StyleBuilder()
                .bold()
                .fg(200, 200, 255)
                .apply(path.name, finish=True)
            )

            lineno = (
                StyleBuilder()
                .fg(255, 220, 97)
                .apply(f'line {frame.lineno}', finish=True)
            )

            fn_color = (255, 100, 100) if is_last else (255, 175, 1)
            func = (
                StyleBuilder()
                .italic()
                .fg(*fn_color)
                .apply(frame.name, finish=True)
            )

            prefix = '  └─' if is_last else '  ├─'
            print(f'{prefix} {folder}{file}  {lineno}  in {func}')

            if frame.line:
                src = (
                    StyleBuilder()
                    .dim()
                    .fg(180, 180, 180)
                    .apply(f'       {frame.line.strip()}', finish=True)
                )
                print(src)
        print()

    sys.excepthook = custom_excepthook
