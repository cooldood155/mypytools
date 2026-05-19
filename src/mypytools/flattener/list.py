"""
Utilities for flattening and filtering heterogeneous lists.

This module provides two public functions:

* :func:`to_list` — accepts any mix of scalars, iterables, and
  mappings and collapses them into a flat ``list``.
* :func:`filter_none` — removes or replaces ``None`` values
  across one or more flat lists.

Fine-grained flags on :func:`to_list` control how deeply nested
structures are unwrapped and how dictionaries are treated. An
optional ``cast_to`` parameter on both functions narrows the
return type at the type-checker level without runtime overhead.

Examples:
```
    from mypytools import filter_none, to_list

    # Flatten nested iterables
    to_list([1, 2], (3, 4), 5)       # [1, 2, 3, 4, 5]

    # Keep only one level of nesting
    to_list(
        [[1, 2], [3, 4]], unwrap_layers=1,
    )  # [[1, 2], [3, 4]]

    # Filter None values from multiple lists
    a, b = filter_none([1, None, 2], [None, 3])
    # ([1, 2], [3])

    # Replace None instead of removing it
    filter_none([1, None, 2], replace=0, combine=True)
    # [1, 0, 2]
```

Note:
    * Requires Python 3.11+.
    * ``unwrap_layers=0`` is explicitly prohibited and raises
      :exc:`ValueError`.
    * Type narrowing via ``cast_to`` is a static-analysis
      convenience; no runtime conversion of individual items is
      performed.
"""

# Standard library imports
from collections.abc import Iterable
from typing import Any, Literal, TypeVar, cast, overload

__all__ = ['filter_none', 'to_list']

TC = TypeVar('TC')
ET = TypeVar('ET')


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
) -> list[Any]:
    """
    Flatten a composite of iterables and scalars into a list.

    Strings are treated as scalar values and are never iterated.

    Args:
        *entries (Any): Values to flatten. Each may be a scalar,
            a string, an iterable, or a mapping.
        include_none (bool): When ``True``, ``None`` is kept as
            a valid list value. Defaults to ``False``.
        unwrap_layers (int): Depth limit for unwrapping nested
            iterables. ``-1`` unwraps fully; positive integers
            stop at that depth. Defaults to ``-1``.
        unwrap_dict_keys (bool): Include dictionary keys when
            unwrapping a mapping. Defaults to ``True``.
        unwrap_dict_vals (bool): Include dictionary values when
            unwrapping a mapping. Defaults to ``False``.
        preserve_dict_tuples (bool): When both
            ``unwrap_dict_keys`` and ``unwrap_dict_vals`` are
            ``True``, keeps each key-value pair as an intact
            ``(key, value)`` tuple. Defaults to ``True``.
        cast_to (type[TC] | None): When provided, casts the
            result to ``list[TC]`` without runtime conversion of
            individual items. Defaults to ``None``.

    Returns:
        list: Flattened results. The element type is ``TC`` when
            ``cast_to`` is given, ``ET`` when all inputs share a
            type, or ``Any`` otherwise.

    Raises:
        ValueError: If ``unwrap_layers`` is less than ``-1`` or
            equal to ``0``.

    Note:
        Added in version 0.1.0.
    """
    if unwrap_layers < -1 or unwrap_layers == 0:
        raise ValueError(
            'unwrap_layers must be -1 (infinite) or a positive integer >= 1.'
        )

    def unwrap(entry: Any, depth: int) -> Iterable[Any]:
        """
        Return ``entry`` as a flat iterable, respecting depth.

        Strings are treated as plain values and are never
        iterated. Dictionaries are handled according to the
        outer ``unwrap_dict_keys``, ``unwrap_dict_vals``, and
        ``preserve_dict_tuples`` flags.

        Args:
            entry (Any): A single value or iterable to unwrap.
            depth (int): Remaining unwrap depth. ``-1`` means
                unlimited; ``0`` stops unwrapping immediately.

        Returns:
            Iterable[Any]: A flat list of unwrapped items, or
                the original value wrapped in a one-item list.

        Example:
            unwrap(6)            # [6]
            unwrap('hello')      # ['hello']
            unwrap([1, 2, 3])    # [1, 2, 3]
            unwrap({'a': 1})     # ['a']  (keys, default)
            unwrap([[[1, 2]]])   # [1, 2] (depth=-1)
        """
        # Base Case 1: Entry is a scalar type or str
        if not isinstance(entry, Iterable) or isinstance(entry, str):
            return [entry]

        # Base Case 2: Entry is a dict
        elif isinstance(entry, dict):
            if depth == 0 or (not unwrap_dict_vals and not unwrap_dict_keys):
                return [entry]

            is_items = unwrap_dict_keys and unwrap_dict_vals
            if is_items:
                target_iterable: Iterable[Any] = entry.items()
            elif unwrap_dict_keys:
                target_iterable = entry.keys()
            else:
                target_iterable = entry.values()

            flattened = []
            next_depth = depth if depth == -1 else depth - 1
            for item in target_iterable:
                if is_items and preserve_dict_tuples:
                    flattened.append(item)
                else:
                    flattened.extend(unwrap(item, next_depth))
            return flattened

        # Base Case 3: Reached users requested depth
        elif depth == 0:
            return [entry]

        # Recursive Step: Unwrap entries
        flattened = []
        next_depth = depth if depth == -1 else depth - 1
        for item in entry:
            flattened.extend(unwrap(item, next_depth))
        return flattened

    def keep(val: Any) -> bool:
        """Return ``True`` if ``val`` should be included."""
        return include_none or val is not None

    flat_result = [
        item
        for entry in entries
        if keep(entry)
        for item in unwrap(entry, unwrap_layers)
        if keep(item)
    ]

    if not flat_result:
        return flat_result
    elif cast_to is not None:
        return cast(list[TC], flat_result)

    return flat_result


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
) -> Any:
    """
    Remove or replace ``None`` values in one or more flat lists.

    Args:
        *flattened_lists (list[Any]): One or more flat lists to
            process.
        cast_to (type[TC] | None): When provided, casts the
            result to ``list[TC]`` without runtime conversion.
            Defaults to ``None``.
        combine (bool): When ``True``, merges all filtered lists
            into a single flat list. Defaults to ``False``.
        replace (Any): When not ``None``, substitutes ``None``
            values with this value instead of removing them.
            Defaults to ``None``.

    Returns:
        tuple[list[Any], ...]: One filtered list per input,
            when ``combine`` is ``False``.
        list[Any]: All filtered items merged, when ``combine``
            is ``True``.
    """
    if replace is None:
        filtered = [
            [i for i in lst if i is not None] for lst in flattened_lists
        ]
    else:
        filtered = [
            [i if i is not None else replace for i in lst]
            for lst in flattened_lists
        ]

    if combine:
        result = [item for sublist in filtered for item in sublist]
        return cast(list[TC], result) if cast_to is not None else result

    return tuple(
        cast(list[TC], lst) if cast_to is not None else lst for lst in filtered
    )
