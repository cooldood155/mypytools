"""
Utilities for flattening and filtering heterogeneous iterables.

**Exposed Modules**:
- `list` — list flattening and filtering utilities.
- `_list` — fast list flattening and filtering utilities (C extension).

**Provides**:

*From* ***list***:
- :func:`filter_none` — removes or replaces ``None`` values
                            across one or more flat lists.

*From* ***_list***:
- :func:`to_list` — accepts any mix of scalars, iterables, and
                        mappings and collapses them into a flat ``list``.
"""

# Relative imports
from ._list import to_list as to_list
from .list import filter_none as filter_none

__all__ = ['filter_none', 'to_list']
