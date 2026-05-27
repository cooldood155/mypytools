# Flattener Package

The packages initializer file ([``__init__.py``](../../src/mypytools/flattener/__init__.py)), the modules, and the functions/methods/classes/etc. themselves have great documentation that explains in detail the functinalities of everything and (in the case of modules and packages) everything that is publically exposed.

## Provided Modules

- [list.py](../../src/mypytools/flattener/list.py) — [Documentation](#list)

---

### ``list``

- Utilities for flattening and filtering heterogeneous lists.

#### *list > filter_none*

```Python
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

- The list(s) of values to filter and remove None from

*``cast_to`` — **type[TC] | None = None***:

- If provided, the resulting list is casted to this type and returned

*``combine`` — **bool = False***:

- If True, all of the lists are combined before being returned

*``replace`` — **Any = None***:

- If anything is provided here, it is used to replace every instance of None instead of removing it

#### *list > to_list*

```Python
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


def to_list(
    *entries: Any,
    include_none: bool = False,
    unwrap_layers: int = -1,
    unwrap_dict_keys: bool = True,
    unwrap_dict_vals: bool = False,
    preserve_dict_tuples: bool = True,
    cast_to: type[TC] | None = None,
) -> list[Any]: ...
```

*``entries`` — **tuple[Any, ...]***:

- The entries to unwrap combine and return as a list

*``include_none`` — **bool = False***:

- If True, ``None`` is included, otherwise it is removed

*``unwrap_layers`` — **int = -1***:

- The number of layers to unwrap from the iterables passed into ``entries``, if ``-1`` is passed in then the iterables are completely flattened

*``unwrap_dict_keys`` — **bool = True***:

- If True, keys from dictionaries passed into ``entries`` are unwrapped from the dictionary and added to the list as a literal

*``unwrap_dict_vals`` — **bool = False***:

- If True, values from dictionaries passed into ``entries`` are unwrapped from the dictionary and added to the list as a literal

*``preserve_dict_tuples`` — **bool = True***:

- If True, keys and values from dictionaries passed into ``entries`` are unwrapped from the dictionary and added to the list as tuples of ``(Key, Value)`` pairs

*``cast_to`` — **type[TC] | None = None***:

- If provided, the flattened list is casted to this type before being returned
