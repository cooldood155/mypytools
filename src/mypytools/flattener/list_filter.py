"""
Utilities for filtering heterogeneous lists.

This module provides:

* :func:`filter_none` — removes or replaces ``None`` values
  across one or more flat lists.

For flattening, see :mod:`mypytools.flattener._list`.

Examples:
    from mytools import filter_none

    # Filter None values from multiple lists
    a, b = filter_none([1, None, 2], [None, 3])
    # ([1, 2], [3])

    # Replace None instead of removing it
    filter_none([1, None, 2], replace=0, combine=True)
    # [1, 0, 2]

Note:
    * Type narrowing via ``cast_to`` is a static-analysis
      convenience; no runtime conversion of individual items is
      performed.
"""

# Standard library imports
from typing import Any, Literal, TypeVar, cast, overload

__all__ = ['filter_none']

TC = TypeVar('TC')
ET = TypeVar('ET')


@overload
def filter_none(
    *flattened_lists: list[ET],
    cast_to: None = ...,
    combine: Literal[False] = ...,
    replace: ET | None = ...,
) -> tuple[list[ET], ...]: ...


@overload
def filter_none(
    *flattened_lists: list[Any],
    cast_to: type[TC],
    combine: Literal[False] = ...,
    replace: TC | None = ...,
) -> tuple[list[TC], ...]: ...


@overload
def filter_none(
    *flattened_lists: list[ET],
    cast_to: None = ...,
    combine: Literal[True],
    replace: ET | None = ...,
) -> list[ET]: ...


@overload
def filter_none(
    *flattened_lists: list[Any],
    cast_to: type[TC],
    combine: Literal[True],
    replace: TC | None = ...,
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
        *flattened_lists (list[Any]):
            One or more flat lists to process.
        cast_to (type[TC] | None):
            When provided, casts the result to ``list[TC]`` without runtime
            conversion. Defaults to ``None``.
        combine (bool):
            When ``True``, merges all filtered lists into a single flat list.
            Defaults to ``False``.
        replace (Any):
            When not ``None``, substitutes ``None`` values with this value
            instead of removing them. Defaults to ``None``.

    Returns:
        tuple[Any] | tuple[list[Any], ...]: The processed result.
            - If ``combine`` is ``True``: A single merged list.
            - If ``combine`` is ``False``: A tuple containing one processed
              list per input list.
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
