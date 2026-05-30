"""
Utilities for flattening and filtering heterogeneous iterables.

**Exposed Modules**:

- :mod:`~mypytools.flattener.list_filter` — list filtering utilities.
- :mod:`~mypytools.flattener._list` — fast list flattening utilities
  (C extension).

**Provides**:

*From* ***list_filter***:

- :func:`filter_none` — removes or replaces ``None`` values
  across one or more flat lists.

*From* ***_list***:

- :func:`to_list` — accepts any mix of scalars, iterables, and
  mappings and collapses them into a flat ``list``.
"""

# Standard library imports
from typing import Any, TypeVar, overload

# Relative imports
from ._list import to_list as _to_list
from .list_filter import filter_none as filter_none

TC = TypeVar('TC')
ET = TypeVar('ET')


@overload
def to_list(
    *entries: Any,
    include_none: bool = ...,
    unwrap_layers: int = ...,
    unwrap_dict_keys: bool = ...,
    unwrap_dict_vals: bool = ...,
    preserve_dict_tuples: bool = ...,
    cast_to: type[TC],
) -> list[TC]: ...
@overload
def to_list(
    *entries: ET,
    include_none: bool = ...,
    unwrap_layers: int = ...,
    unwrap_dict_keys: bool = ...,
    unwrap_dict_vals: bool = ...,
    preserve_dict_tuples: bool = ...,
    cast_to: None = ...,
) -> list[ET]: ...
def to_list(
    *entries: Any,
    include_none: bool = False,
    unwrap_layers: int = -1,
    unwrap_dict_keys: bool = True,
    unwrap_dict_vals: bool = False,
    preserve_dict_tuples: bool = True,
    cast_to: type[Any] | None = None,
) -> list[Any]:
    """
    Flatten a composite of iterables and scalars into a list.

    - Strings are treated as scalar values and are never iterated.

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

    Added: `v0.1.0a1`
    Updated: `v0.2.0a1
    """
    return _to_list(
        *entries,
        include_none=include_none,
        unwrap_layers=unwrap_layers,
        unwrap_dict_keys=unwrap_dict_keys,
        unwrap_dict_vals=unwrap_dict_vals,
        preserve_dict_tuples=preserve_dict_tuples,
        cast_to=cast_to,
    )


__all__ = ['filter_none', 'to_list']
