"""
Utilities for flattening and filtering heterogeneous iterables.

**Exposed Modules**:
- `list.py` — list flattening and filtering utilities.

**Provides**:

*From* ***list***:
- :func:`to_list` — accepts any mix of scalars, iterables, and
                        mappings and collapses them into a flat ``list``.
- :func:`filter_none` — removes or replaces ``None`` values
                            across one or more flat lists.
"""

# Relative imports
from .list import filter_none as filter_none, to_list as to_list

__all__ = ['filter_none', 'to_list']
