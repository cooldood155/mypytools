"""
Type stubs for the _list C extension module.

to_list(*entries, include_none=False, unwrap_layers=-1,
        unwrap_dict_keys=True, unwrap_dict_vals=False,
        preserve_dict_tuples=True, cast_to=None)

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
"""

# Standard library imports
from typing import Any, TypeVar, overload

__all__ = ['to_list']

TC = TypeVar('TC')
ET = TypeVar('ET')

# —{ to_list() }————————————————————————————————————————————————————————————————
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
