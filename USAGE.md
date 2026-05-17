# Using MyTools in Another Project

## Installation

### Full Install From GitHub — (*no* PyPI needed)

```bash
pip install git+https://github.com/cooldood155/mypytools
```

### Optional Dependencies

Some modules require extra packages. Install only what you need:

```bash
pip install "mytools[dev]"   # Dev Tools
```

If a module needs a dependency you haven't installed, `mytools` will tell
you exactly what to run.

### Grabbing Specific Modules — (*no* install at all)

`MyTools` is structured using the common **src layout**. Modules with no
dependencies can be copied directly into your project and used as-is —
check the module's docstring to confirm it has no requirements before doing
this.

If a module *does* have dependencies and you're using it standalone (copied,
not installed), just install the raw dependencies directly:

```bash
pip install pandas numpy    # for example, if the module requires them
```

The module itself will tell you what it needs if you try to import it without
the required packages installed.

---

## Partial Installs

There is no way to install only a specific module or subpackage from `mytools`
via `pip` — you either install the full package (with optional dep groups) or
copy the file(s) you need manually (see above).

If the full install is too heavy for your use case, the copy approach is the
right call — especially since the core of `mytools` has zero dependencies.

---

## Usage

```python
from mytools.log import get_logger
from mytools.ansi_tools import bubble
```
