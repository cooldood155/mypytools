# MyTools

My custom Python utility library. Zero core dependencies — install only what you need.

## Requirements

- Python >= 3.12

---

## Development Setup

```bash
git clone https://github.com/cooldood155/mytools
cd mytools
pip install -e ".[dev]"   # installs mytools + dev tools (ruff, pytest, mypy)
pre-commit install        # sets up git commit hooks
```

The `-e` flag installs in **editable mode** — changes you make in `src/` are
immediately reflected without reinstalling.

You can omit this flag if necessary.

---

## Development Workflow

```bash
ruff check src/    # lint
ruff format src/   # format
pytest             # run tests
git add .
git commit -m "..." # pre-commit hooks fire (ruff + pytest)
git push            # CI takes over
```

### Ruff

Ran from the **root** `mytools` directory.

1. **Linting**

    ```bash
    ruff check src/
    ```

    Review everything Ruff has flagged, fix what's needed, then re-run
    with `--fix` once you're happy with what it'll change.

2. **Formatting**

    ```bash
    ruff format src/
    ```

---

## License

MIT