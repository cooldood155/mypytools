# Log Package

## Publically Exposed Modules

- `log` – developer diagnostic utilities for logging and exception handling.

### *log > get_logger*

```python
def get_logger(
    log_path: Path | None = None,
    level: int | None = None,
    name: str | None = None,
    env: str | None = None,
) -> Logger: ...
```

Configure and retrieve a file-backend `Logger` instance.

*`log_path`*:

- The directory to save the log file to. Overrides the `'PYTOOLS_LOG_PATH'` environment variable if provided.

  **Defaults to**:

  - Current working directory of the path that called the function.

  **Environment variable**:

  - \<optional\> — `PYTOOLS_LOG_PATH` – *(str)*

*`level`*:

- The logging threshold level (e.g., 'debug', 'info'). Overrides the `'PYTOOLS_LOG_LEVEL'` environment variable if provided.

  **Defaults to**:

  - `'dbug'`, capturing all logs.

  **Environment variable**:

  - \<optional\> — `PYTOOLS_LOG_LEVEL` – *(str)*

    Can be one of five string values:

    1. `'debug'`
    2. `'info'`
    3. `'warning'`
    4. `'error'`
    5. `'critical'`

    Each level captures all logs of its level and above (e.g. `'debug'` captures all logs, `'critical'` only captures critical logs).

*`name`*:

- The explicit name of the logger, as well as the filename of the `.log` file. Overrides the `'PYTOOLS_LOG_SHARED'` environment variable.

  **Defaults to**:

  - The name of the module the function was called within.

  **Environment variable**:

  - \<optional\> — `PYTOOLS_LOG_SHARED` – *(str)*

    This is usefull if you wish to have a single, central log file by using a set `log_path` and `name` through the `PYTOOLS_LOG_DIR` and `PYTOOLS_LOG_SHARED` environment variables respectively.

*`env`*:

- The environment mode to use (development & production). Overrides the `'PYTOOLS_LOG_MODE'` environment variable if provided.

  **Defaults to**:

  - `'dev'`, printing a nicely formatted, human readable string.

  **Environment variable**:

  - \<optional\> — `'PYTOOLS_LOG_MODE'` - *(str)*

    Can be one of two strings:

    1. `'dev'` — pretty printed easy to read logs.
    2. `'prod'` — single line, strictly formatted logs.

### *log > setup_hooks*

```Python
def setup_hooks() -> None: ...
```

Installs an ANSI-stylized global exception hook; overrides `sys.excepthook` with a polished, color-coded trace viewer that extracts source code lines, highlights errors, and formats module paths cleanly within the terminal.

- It is only required to be called once near the top of the main script.
