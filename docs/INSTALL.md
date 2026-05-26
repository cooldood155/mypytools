# Installing MyPyTools

A guide for installing MyPyTools, optional dependencies provided by MyPyTools, and grabbing specific modules/packages. If you are a developer, refer to [DEV.md](./DEV.md) for a proper installation guide.

## Installation

### Full Install From [GitHub](https://github.com/cooldood155/mypytools)

#### Latest version

```bash
pip install git+https://github.com/cooldood155/mypytools
```

#### Specific version

```bash
pip install git+https://github.com/cooldood155/mypytools@v<major>.<minor>.<patch>
```

<!-- ### Optional Dependencies

Some modules require extra packages. Install only what you need:

```bash
pip install "mypytools[dev]"   # Dev Tools
```

If a module needs a dependency you haven't installed, `mytools` will tell you exactly what to run. -->

### Grabbing Specific Modules — (*no* install at all)

This is the **recommended** approach if you plan on only using bits and pieces of the library and want to avoids the disk cost of installing the entire library.

`MyTools` is structured using the common **src layout**. Modules or entire packages with no dependencies can be copied directly into your project and used as-is — check the module's docstring to confirm it has no requirements before doing this.

If a module *does* have dependencies and you're using it standalone (copied, not installed), just install the raw dependencies directly:

```bash
pip install pandas numpy    # for example, if the module requires them
```

The module itself will tell you what it needs if you try to import it without
the required packages installed.

---

## Partial Installs

There is no way to install only a specific module or subpackage from `MyTools` via `pip`. You either install the full package (with optional dep groups) or copy the package(s) and/or module(s) you need from the GitHub manually — [*see above*](#grabbing-specific-modules--no-install-at-all).

If the full install is too heavy for your use case, the copy approach is the right call — especially since the core of `MyTools` has zero dependencies.
