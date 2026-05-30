# Log Package

Developer diagnostic utilities for logging and exception handling.

## Provided Modules

- [log.py](#log)
  - [get_logger()](#log--get_logger)
  - [setup_hooks()](#log--setup_hooks)

---

### `log`

Developer diagnostic utilities for logging and exception handling.

#### *log > get_logger*

```python
def get_logger(
    log_path: Path | None = None,
    level: int | None = None,
    name: str | None = None,
    env: str | None = None,
) -> Logger: ...
```

Configure and retrieve a file-backed ``Logger`` instance.

*`log_path`*:

- The directory to save the log file to. Overrides the
  ``PYTOOLS_LOG_PATH`` environment variable if provided.

  **Defaults to**: the current working directory of the calling module.

  **Environment variable**: `PYTOOLS_LOG_PATH` *(str, optional)*

*`level`*:

- The logging threshold level. Overrides the ``PYTOOLS_LOG_LEVEL``
  environment variable if provided.

  **Defaults to**: ``'debug'``, capturing all logs.

  **Environment variable**: `PYTOOLS_LOG_LEVEL` *(str, optional)*

  Can be one of five values:

  1. `'debug'`
  2. `'info'`
  3. `'warning'`
  4. `'error'`
  5. `'critical'`

  Each level captures all logs at its level and above (e.g. `'debug'`
  captures everything, `'critical'` captures only critical logs).

*`name`*:

- The explicit name of the logger and the filename of the `.log`
  file. Overrides the ``PYTOOLS_LOG_SHARED`` environment variable
  if provided.

  **Defaults to**: the name of the module the function was called
  within.

  **Environment variable**: `PYTOOLS_LOG_SHARED` *(str, optional)*

  Useful for centralising all logs into a single file by pairing a
  fixed ``log_path`` and ``name`` via ``PYTOOLS_LOG_PATH`` and
  ``PYTOOLS_LOG_SHARED``.

*`env`*:

- The environment mode (development or production). Overrides the
  ``PYTOOLS_LOG_MODE`` environment variable if provided.

  **Defaults to**: ``'dev'``, printing a nicely formatted,
  human-readable string.

  **Environment variable**: `PYTOOLS_LOG_MODE` *(str, optional)*

  Can be one of two values:

  1. `'dev'` — pretty-printed, easy-to-read logs.
  2. `'prod'` — single-line, strictly formatted logs.

#### *log > setup_hooks*

```python
def setup_hooks() -> None: ...
```

Installs an ANSI-stylized global exception hook; overrides
``sys.excepthook`` with a polished, color-coded trace viewer that
extracts source code lines, highlights errors, and formats module
paths cleanly within the terminal.

Only needs to be called once, near the top of the main script.
