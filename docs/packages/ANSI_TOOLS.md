# Ansi Tools Package

The packages initializer file ([``__init__.py``](../../src/mypytools/ansi_tools/__init__.py)), the modules, and the functions/methods/classes/etc. themselves have great documentation that explains in detail the functinalities of everything and (in the case of modules and packages) everything that is publically exposed.

## Provided Modules

- [formatter.py](../../src/mypytools/ansi_tools/formatter.py) — [documentation](#formatter)
- [style_builder.py](../../src/mypytools/ansi_tools/style_builder.py) — [documentation](#style_builder)

---

### ``formatter``

- A low-level ANSI terminal formatting utility

#### *formatter > ANSIFormatter*

```python
class ANSIFormatter: ...
```

Low-level ANSI escape-sequence constants and builder.

Typical usage is through ``StyleBuilder``, which wraps these constants in
a fluent API.

### Contains

- ``escape`` — classmethod that wraps a string in an SGR escape sequence.

  ``` Python
  @classmethod
      def escape(
          cls,
          style: str | int,
          string: str,
          *,
          reset: str = ''
      ) -> str: ...
  ```

  Direct use of ``escape`` is useful when you need a one-off
styled string without building up a chain.

- ``Fonts``, ``Emphasis``, ``Effects``, ``Foreground``, ``Background`` —
nested namespaces grouping related SGR codes.

---

### `style_builder`

Fluent builder for composing and applying ANSI styles.

Chain style methods (``bold()``, ``italic()``, ``fg()``, etc.) to
accumulate SGR codes, then call ``apply()`` to wrap text in the
corresponding escape sequence.

**For example**:

```Python
print(
    StyleBuilder()
    .bold()
    .fg(220, 50, 47)
    .apply('Error: ')
    .italic()
    .apply(
        'something went wrong',
        finish=True,
    )
)
```

- Resulting in something similar to:

  **Error:** *Something went wrong*

  - ``'Error'`` would be red here, but markdown does not have built-in syntax for coloring text

***or***:

```Python
print(
    StyleBuilder()
    .bold()
    .apply('Look ', clear_codes=False)
    .italic()
    .apply('here ')
    .add('https://github.com/cooldood155/mypytools', finish=True)
)
```

- Resulting in something similar to:

  **Look** ***here*** https&#8203;://github.com/cooldood155/mypytools
