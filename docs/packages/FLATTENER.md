# Flattener Package

The package's initializer file ([``__init__.py``](../../src/mypytools/flattener/__init__.py)),
the modules, and the functions/methods/classes/etc. themselves have
great documentation that explains in detail the functionalities of
everything and (in the case of modules and packages) everything that
is publicly exposed.

## Provided Modules

- [list_filter.py](../../src/mypytools/flattener/list_filter.py) — [documentation](#list_filter)
- [\_list.cpp](../../src/mypytools/flattener/_list.cpp) — [documentation](#_list)

---

### ``list_filter``

Utilities for filtering heterogeneous lists.

#### *list_filter > filter_none*

```python
@overload
def filter_none(
    *flattened_lists: list[ET],
    cast_to: None = None,
    combine: Literal[False] = ...,
    replace: ET | None = None,
) -> tuple[list[ET], ...]: ...


@overload
def filter_none(
    *flattened_lists: list[Any],
    cast_to: type[TC],
    combine: Literal[False] = ...,
    replace: TC | None = None,
) -> tuple[list[TC], ...]: ...


@overload
def filter_none(
    *flattened_lists: list[ET],
    cast_to: None = None,
    combine: Literal[True],
    replace: ET | None = None,
) -> list[ET]: ...


@overload
def filter_none(
    *flattened_lists: list[Any],
    cast_to: type[TC],
    combine: Literal[True],
    replace: TC | None = None,
) -> list[TC]: ...


def filter_none(
    *flattened_lists: list[Any],
    cast_to: type[TC] | None = None,
    combine: bool = False,
    replace: Any = None,
) -> Any: ...
```

Remove or replace ``None`` values in one or more flat lists.

*``flattened_lists`` — **tuple[list[Any], ...]***:

- The list(s) of values to filter.

*``cast_to`` — **type[TC] | None = None***:

- If provided, the resulting list is cast to this type before being
  returned.

*``combine`` — **bool = False***:

- If ``True``, all lists are combined into a single list before
  being returned.

*``replace`` — **Any = None***:

- If provided, replaces every ``None`` with this value instead of
  removing it.

---

### ``_list``

Fast list flattening utilities (C++ extension, compiled via pybind11).

#### *_list > to_list*

```python
@overload
def to_list(
    *entries: Any,
    include_none: bool = False,
    unwrap_layers: int = -1,
    unwrap_dict_keys: bool = True,
    unwrap_dict_vals: bool = False,
    preserve_dict_tuples: bool = True,
    cast_to: type[TC],
) -> list[TC]: ...


@overload
def to_list(
    *entries: ET,
    include_none: bool = False,
    unwrap_layers: int = -1,
    unwrap_dict_keys: bool = True,
    unwrap_dict_vals: bool = False,
    preserve_dict_tuples: bool = True,
    cast_to: None = None,
) -> list[ET]: ...
```

Flatten a composite of iterables and scalars into a flat list.
Strings are treated as scalar values and are never iterated.

*``entries`` — **tuple[Any, ...]***:

- Values to flatten. Each may be a scalar, a string, an iterable,
  or a mapping.

*``include_none`` — **bool = False***:

- If ``True``, ``None`` is kept as a valid list value; otherwise it
  is removed.

*``unwrap_layers`` — **int = -1***:

- Depth limit for unwrapping nested iterables. ``-1`` unwraps fully;
  positive integers stop at that depth.

*``unwrap_dict_keys`` — **bool = True***:

- If ``True``, dictionary keys are unwrapped and added to the list.

*``unwrap_dict_vals`` — **bool = False***:

- If ``True``, dictionary values are unwrapped and added to the list.

*``preserve_dict_tuples`` — **bool = True***:

- When both ``unwrap_dict_keys`` and ``unwrap_dict_vals`` are
  ``True``, keeps each key-value pair as an intact ``(key, value)``
  tuple.

*``cast_to`` — **type[TC] | None = None***:

- Static-analysis convenience only; no runtime conversion of
  individual items is performed.

**Raises**:

- ``ValueError`` — if ``unwrap_layers`` is less than ``-1`` or
  equal to ``0``.
