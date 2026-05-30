"""Stub file for the _list.cpp extension module."""

# Standard library imports
from typing import Any, TypeVar, overload

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
