# Working On MyLib

**Authors**: Evan Reumann

**Maintainers**: Evan Reuamnn

## First time setup

```bash
git clone https://github.com/you/mytools
cd mytools
pip install -e ".[dev]"   # installs mytools + dev tools (ruff, pytest, mypy)
pre-commit install        # hooks up git commit hooks
```

## Day-to-day

- All **tests** written in `tests/`
- All **source code** written in `src/`

```bash
ruff check src/        # lint
ruff format src/       # format
pytest                 # run tests
git add .
git commit -m "..."    # pre-commit hooks fire (ruff + pytest)
git push               # CI takes over
```
