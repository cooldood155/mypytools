"""
ANSI terminal text formatting and styling utilities.

- Contains printable pre-formatted styles.

**Exposed Modules**:
- :file:`formatter.py` — low-level ANSI terminal text formatting.
- :file:`style_builder.py` — high-level ANSI terminal styling as well as
                             pre-formatted printable styles.

**Provides**:

*From* ***formatter***:
- :class:`ANSIFormatter` — constants and a low-level escape-sequence builder.

*From* ***style_builder***:
- :class:`StyleBuilder` — a fluent builder for composing and applying ANSI
                          styles.
- :func:`bubble` — a pre-styled diagnostic string for surfacing
                   assertion or validation errors in the terminal.
"""

# Relative imports
from .formatter import ANSIFormatter
from .style_builder import StyleBuilder, bubble

__all__ = ['ANSIFormatter', 'StyleBuilder', 'bubble']
