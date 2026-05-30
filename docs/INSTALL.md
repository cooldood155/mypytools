# Installing MyPyTools

A guide for installing MyPyTools, optional dependencies provided by
MyPyTools, and grabbing specific modules/packages. If you are a
developer, refer to [DEV.md](./DEV.md) for a proper installation guide.

## Installation

### Full Install From [GitHub](https://github.com/cooldood155/mypytools)

#### Latest version

```bash
pip install git+https://github.com/cooldood155/mypytools
```

#### Specific version

```bash
pip install git+https://github.com/cooldood155/mypytools@v..
```

---

### Grabbing Specific Modules — (*no* install at all)

This is the **recommended** approach if you only need bits and pieces of
the library and want to avoid the disk cost of installing the entire
package.

`MyPyTools` is structured using the common **src layout**. Modules or
entire packages with no dependencies can be copied directly into your
project and used as-is — check the module's docstring to confirm it has
no requirements before doing this.

> **Note — C++ extension modules**: Some packages (e.g. `flattener`)
> include compiled C++ extensions that must be built before use. These
> **cannot** be copied and used standalone — install the full package
> instead, or build the extension yourself (see [DEV.md](./DEV.md)).

If a pure-Python module *does* have dependencies and you're using it
standalone (copied, not installed), install the raw dependencies
directly:

```bash
pip install pandas numpy    # for example, if the module requires them
```

The module itself will tell you what it needs if you try to import it
without the required packages installed.

---

## Partial Installs

There is no way to install only a specific module or subpackage from
`MyPyTools` via `pip`. You either install the full package or copy the
package(s) and/or module(s) you need from GitHub manually —
[*see above*](#grabbing-specific-modules--no-install-at-all).

If the full install is too heavy for your use case, the copy approach
is the right call — especially since the pure-Python core of `MyPyTools`
has zero dependencies.
