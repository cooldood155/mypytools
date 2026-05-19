"""
A low-level ANSI terminal text formatting utility.

Provides:
- ``ANSIFormatter`` — constants and a low-level escape-sequence builder.
"""

# Future imports
from __future__ import annotations

# Standard library imports
from enum import Enum
from typing import ClassVar

__all__ = ['ANSIFormatter']


# ——{ ANSI Formatter }——————————————————
class ANSIFormatter:
    """
    Low-level ANSI escape-sequence constants and builder.

    Contains:
    - ``escape`` — classmethod that wraps a string in an SGR escape sequence.
    - ``Fonts``, ``Emphasis``, ``Effects``, ``Foreground``, ``Background`` —
    nested namespaces grouping related SGR codes.

    Typical usage is through ``StyleBuilder``, which wraps these constants in
    a fluent API. Direct use of ``escape`` is useful when you need a one-off
    styled string without building up a chain.

    Note:
        Top-level constants (``RESET``, ``RESET_INTENSITY``, ``B8_COLOR``,
        ``B24_COLOR``) are unannotated class variables. Unlike the ``Emphasis``
        and ``Effects`` inner classes, they carry no ``ClassVar`` annotation.
        They are class-level constants and should not be reassigned or
        instantiated.
    """

    ESCAPE_SEQUENCE = '\x1b['

    @classmethod
    def escape(cls, style: str | int, string: str, *, reset: str = '') -> str:
        r"""
        Wrap ``string`` in an SGR escape sequence using ``style``.

        Opens with ``\x1b[<style>m`` and closes with ``\x1b[<reset>m``.
        If ``reset`` is omitted the sequence closes with ``\x1b[0m`` (full
        reset).

        Args:
            style:
                A semicolon-separated SGR parameter string or a single integer
                code (e.g. ``"1"`` for bold, ``"38;2;255;0;0"`` for 24-bit red
                foreground).
            string:
                The text to wrap.
            reset:
                An SGR code used to close the sequence instead of the default
                full reset (``0``). Useful for targeted resets, e.g. ``"23"``
                to reset italic only::

                                escape(
                                    ANSIFormatter.Emphasis.ITALIC,
                                    'Hello',
                                    reset='23',
                                )
                                # -> '\x1b[3mHello\x1b[23m'

        Returns:
            The escape-coded string.
        """
        end = reset or str(cls.RESET)
        return (
            f'{cls.ESCAPE_SEQUENCE}{style}m{string}{cls.ESCAPE_SEQUENCE}{end}m'
        )

    RESET = 0
    RESET_INTENSITY = 22  # resets both Bold and Dim
    B8_COLOR = 5
    B24_COLOR = 2

    class Fonts(Enum):
        """
        SGR alternate-font codes (10-20).

        ``FRAKTUR`` (20) is rarely supported by modern terminals.
        ``DEFAULT_FONT`` (10) restores the primary font.
        """

        (
            DEFAULT_FONT,
            FONT1,
            FONT2,
            FONT3,
            FONT4,
            FONT5,
            FONT6,
            FONT7,
            FONT8,
            FONT9,
            FRAKTUR,
        ) = range(10, 21)

    class Emphasis:
        r"""
        SGR codes for text-emphasis styles and their targeted resets.

        Use ``reset`` to undo a specific emphasis without a full ``\x1b[0m``
        reset (which would also strip colours and other active effects).

        All attributes are class-level constants and are never meant to be
        instantiated or mutated.
        """

        BOLD: ClassVar[int] = 1
        ITALIC: ClassVar[int] = 3
        UNDERLINE: ClassVar[int] = 4
        STRIKETHROUGH: ClassVar[int] = 9
        DOUBLE_UNDERLINE: ClassVar[int] = 21

        reset: ClassVar[dict[str, int]] = {
            'RESET_ITALIC': 23,
            'RESET_UNDERLINE': 24,
            'RESET_STRIKETHROUGH': 29,
        }

    class Effects:
        """
        SGR codes for visual effects and their targeted resets.

        - ``*_BLINK`` (5 & 6) is rarely supported by modern terminals.
        - ``reset.SHOW``(28) may have side effects

        Use ``reset`` to undo a specific effect without a full reset.

        All attributes are class-level constants and are never meant to be
        instantiated or mutated.
        """

        DIM: ClassVar[int] = 2
        SLOW_BLINK: ClassVar[int] = 5
        RAPID_BLINK: ClassVar[int] = 6  # rarely supported
        BG_FG_SWAP: ClassVar[int] = 7
        HIDE: ClassVar[int] = 8

        reset: ClassVar[dict[str, int]] = {
            'RESET_BLINK': 25,
            'BG_FG_UNSWAP': 27,
            'SHOW': 28,
        }

    class Foreground(Enum):
        """
        SGR foreground-colour codes (30-39).

        Use ``CUSTOM`` for 8-bit or 24-bit colour.
        """

        (
            BLACK,
            RED,
            GREEN,
            YELLOW,
            BLUE,
            MAGENTA,
            CYAN,
            WHITE,
            CUSTOM,
            DEFAULT,
        ) = range(30, 40)

    class Background(Enum):
        """
        SGR background-colour codes (40-49).

        Use ``CUSTOM`` for 8-bit or 24-bit colour.
        """

        (
            BLACK,
            RED,
            GREEN,
            YELLOW,
            BLUE,
            MAGENTA,
            CYAN,
            WHITE,
            CUSTOM,
            DEFAULT,
        ) = range(40, 50)
