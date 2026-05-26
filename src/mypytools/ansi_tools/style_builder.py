"""
A high-level ANSI terminal styling utility and pre-formatted printable styles.

Provides:
- ``StyleBuilder``  — a fluent builder for composing and applying ANSI styles.
- ``bubble``        — a pre-styled diagnostic string for surfacing assertion or
                      validation errors in the terminal.
"""

# Standard library imports
import re
from typing import ClassVar, Literal, Self, overload

# Relative imports
from .formatter import ANSIFormatter

__all__ = ['StyleBuilder', 'bubble']


# ——{ Styles }—————————————————————————————————————————————————————————————————
def bubble(
    expected: str | list[str],
    at: str,
    lvalue: str,
    rvalue: str,
    compare: str = '==',
    prepend_why: str = '',
    append_why: str = '',
) -> str:
    """
    Build a pre-styled diagnostic string for surfacing validation errors.

    Renders a compact, colour-coded message of the form::

        Expected <expected> @--> <at> ?--> <lvalue> <compare> <rvalue>

    Intended to be passed directly to ``ValueError`` or similar exceptions.

    Args:
        expected:
            The value(s) that were expected. A list renders each entry as its
            own pill; a string renders as a single pill.
        at:
            The name of the function, argument, or location where the
            expectation was not met.
        lvalue:
            The left-hand side of the comparison expression.
        rvalue:
            The right-hand side of the comparison expression.
        compare:
            The comparison operator displayed between ``lvalue`` and
            ``rvalue``.
        prepend_why:
            Optional text inserted immediately before the comparison pill.
        append_why:
            Optional text appended after the full message.

    Returns:
        A fully escape-coded string ready for display in a terminal.
    """
    style = ANSIFormatter.escape

    def code(*parts: int | str) -> str:
        return ';'.join(map(str, parts))

    def fg(r: int, g: int, b: int) -> str:
        return f'38;2;{r};{g};{b}'

    def bg(r: int, g: int, b: int) -> str:
        return f'48;2;{r};{g};{b}'

    italic = ANSIFormatter.Emphasis.ITALIC
    underline = ANSIFormatter.Emphasis.UNDERLINE

    dark_bg = bg(55, 65, 81)
    light_fg = fg(248, 250, 252)

    light_on_dark = code(light_fg, dark_bg)
    pink_italic = code(italic, fg(248, 175, 195), dark_bg)
    muted = code(fg(148, 163, 184), dark_bg)
    underlit = code(italic, underline, light_on_dark)

    pill_fg = fg(55, 65, 81)

    l_cap = style(pill_fg, '\ue0b6')
    r_cap = style(pill_fg, '\ue0b4')

    def pill(_style: str, text: str | list[str]) -> str:
        inner = (
            ', '.join(style(_style, t) for t in text)
            if isinstance(text, list)
            else style(_style, text)
        )
        return f'{l_cap}{inner}{r_cap}'

    def comparison_pill() -> str:
        inner = (
            f'{style(underlit, lvalue)}'
            f'{style(muted, f" {compare} ")}'
            f'{style(underlit, rvalue)}'
        )
        return f'{l_cap}{inner}{r_cap}'

    exp = (
        ', '.join(pill(light_on_dark, e) for e in expected)
        if isinstance(expected, list)
        else pill(light_on_dark, expected)
    )

    return (
        f'Expected {exp}'
        f' @—> {pill(pink_italic, at)}'
        f' ?—>{prepend_why} {comparison_pill()}'
        f'{append_why}'
    )


# ——{ StyleBuilder }————————————————————————————————————————————————————————————


class StyleBuilder:
    """
    Fluent builder for composing and applying ANSI styles.

    Chain style methods (``bold()``, ``italic()``, ``fg()``, etc.) to
    accumulate SGR codes, then call ``apply()`` to wrap text in the
    corresponding escape sequence.

    Multiple styled segments can be built up and emitted in one shot using
    ``finish=True`` on the final ``apply()`` or ``add()`` call.

    Example::

            result = (
                StyleBuilder()
                .bold()
                .fg(220, 50, 47)
                .apply('Error: ')
                .italic()
                .apply(
                    'something went wrong',
                    finish=True,
                )
            )

    Notes:
        - ``apply()`` clears accumulated codes after each call.
        - ``_compute_reset_codes()`` computes targeted resets where possible.
        - ``add()`` inserts raw unstyled text between styled segments.
    """

    ANSI_ESCAPE_RE: ClassVar[re.Pattern[str]] = re.compile(r'\x1b\[[0-9;]*m')

    def __init__(self) -> None:
        """Initialise an empty builder."""
        self._codes: list[str] = []
        self._formatted: list[str] = []

    @overload
    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: Literal[False] = False,
        processed_sep: str = '',
        processed_sep_end: bool = False,
    ) -> Self: ...

    @overload
    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: Literal[True],
        processed_sep: str = '',
        processed_sep_end: bool = False,
    ) -> str: ...

    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: bool = False,
        processed_sep: str = '',
        processed_sep_end: bool = False,
    ) -> str | Self:
        """
        Append raw (unstyled) text segments to the builder cache.

        Raises:
            ValueError:
                If style codes are pending and ``apply()`` has not yet been
                called.
        """
        if self._codes:
            raise ValueError(
                'Pending style codes exist — call apply() before add() '
                'to consume them, or remove the style calls if unstyled '
                'text was intended.'
            )

        self._formatted.append(sep.join(raw_text) + end_sep)

        if finish:
            result = processed_sep.join(self._formatted) + (
                processed_sep if processed_sep_end else ''
            )
            self._formatted.clear()
            return result

        return self

    def reset(self) -> Self:
        """**Resets text style** — Appends style code `0` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.RESET))
        return self

    def bold(self) -> Self:
        """**Bold text** — Appends style code `1` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Emphasis.BOLD))
        return self

    def italic(self) -> Self:
        """**Italicised text** — Appends style code `3` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Emphasis.ITALIC))
        return self

    def underline(self) -> Self:
        """**Underlined text** — Appends style code `4` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Emphasis.UNDERLINE))
        return self

    def strikethrough(self) -> Self:
        """
        **Strikethrough the text**.

        Appends style code `9` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Emphasis.STRIKETHROUGH))
        return self

    def double_underline(self) -> Self:
        """
        **Double underlined text**.

        Appends style code `21` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE))
        return self

    def dim(self) -> Self:
        """**Dim text** — Appends style code `2` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Effects.DIM))
        return self

    def slow_blink(self) -> Self:
        """
        *(rarely supported)*.

        **Slow blinking text** — Appends style code `5` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Effects.SLOW_BLINK))
        return self

    def fast_blink(self) -> Self:
        """
        *(rarely supported)*.

        **Underlined text** — Appends style code `6` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Effects.RAPID_BLINK))
        return self

    def bg_fg_swap(self) -> Self:
        """
        **Background to foreground** — Appends style code `7` to `self._codes`.

        - Background is set to foreground, foreground is set to background.
        """
        self._codes.append(str(ANSIFormatter.Effects.BG_FG_SWAP))
        return self

    def hide(self) -> Self:
        """**Hide text** — Appends style code `8` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Effects.HIDE))
        return self

    def reset_intensity(self) -> Self:
        """
        **Remove** ***bold*** **and** ***dim*** **codes**.

        Appends style code `22` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.RESET_INTENSITY))
        return self

    def reset_underline(self) -> Self:
        """
        **Remove *underline* code**.

        Appends style code `24` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']))
        return self

    def reset_italic(self) -> Self:
        """
        **Remove *italic* and *Fraktur* codes**.

        Appends style code `23` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']))
        return self

    def reset_strikethrough(self) -> Self:
        """
        **Remove *strikethrough* code**.

        Appends style code `29` to `self._codes`.
        """
        self._codes.append(
            str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH'])
        )
        return self

    def reset_blink(self) -> Self:
        """
        **Remove *slow blink* and *fast blink* codes**.

        Appends style code `25` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Effects.reset['RESET_BLINK']))
        return self

    def bg_fg_reswap(self) -> Self:
        """
        **Swap background with foreground** *(and vice versa)*.

        Appends style code `27` to `self._codes`.

        - *Applied after `bg_fg_swap()` to re-swap.*
        """
        self._codes.append(str(ANSIFormatter.Effects.reset['BG_FG_UNSWAP']))
        return self

    def show(self) -> Self:
        """
        # Construction Needed.

        Do the above instead of appending code `28`.

        Code `28` functions vastly different accross terminals.

        ---

        - *Applied after `hide()`*.

        **Remove *hide* code** *(and possibly others — read above)* —

        Appends style code `28` to `self._codes`.
        """
        # TODO:
        # 1. Copy `<StyleBuilder_obj>._codes` up to the most recent reset (`0`)
        # 2. Remove the `hide` code & append a reset code (`0`) to the back
        # 3. Append the resulting codes back to `<StyleBuilder_obj>._codes`

        self._codes.append(str(ANSIFormatter.Effects.reset['SHOW']))
        return self

    def reset_bg(self) -> Self:
        """
        **Resets text background**.

        Appends style code `49` to `self._codes`.
        """
        self._codes.append(str(ANSIFormatter.Background.DEFAULT.value))
        return self

    def reset_fg(self) -> Self:
        """**Rests text color** — Appends style code `39` to `self._codes`."""
        self._codes.append(str(ANSIFormatter.Foreground.DEFAULT.value))
        return self

    def fg(
        self,
        r: int,
        g: int | None = None,
        b: int | None = None,
        /,
        *,
        b24: bool = True,
    ) -> Self:
        """
        **Set foreground color**.

        Appends style code `39;5;<r>` if *not* `b24`,
        otherwise `39;2;<r>;<g>;<b>` is appended.
        """
        if (g is None or b is None) and b24:
            raise ValueError(
                bubble(
                    expected=['r', 'g', 'b'],
                    at='fg',
                    lvalue='b24',
                    rvalue='True',
                    prepend_why=' keyword-argument',
                )
            )

        self._codes.append(
            f'{ANSIFormatter.Foreground.CUSTOM.value}'
            f';{ANSIFormatter.B24_COLOR if b24 else ANSIFormatter.B8_COLOR}'
            f';{r}{f";{g};{b}" if b24 else ""}'
        )

        return self

    def bg(
        self,
        r: int,
        g: int | None = None,
        b: int | None = None,
        /,
        *,
        b24: bool = True,
    ) -> Self:
        """
        **Set background colour**.

        - Appends style code `49;5;<r>` if *not* `b24`,
        - otherwise `49;2;<r>;<g>;<b>` is appended.
        """
        if (g is None or b is None) and b24:
            raise ValueError(
                bubble(
                    expected=['r', 'g', 'b'],
                    at='bg',
                    lvalue='b24',
                    rvalue='True',
                    prepend_why=' keyword-argument',
                )
            )

        self._codes.append(
            f'{ANSIFormatter.Background.CUSTOM.value}'
            f';{ANSIFormatter.B24_COLOR if b24 else ANSIFormatter.B8_COLOR}'
            f';{r}{f";{g};{b}" if b24 else ""}'
        )

        return self

    @staticmethod
    def _compute_reset_codes(codes: list[str]) -> str:
        """Compute targeted reset codes for a given style-code set."""
        resets: list[str] = []

        if (
            str(ANSIFormatter.Emphasis.BOLD) in codes
            or str(ANSIFormatter.Effects.DIM) in codes
        ):
            resets.append(str(ANSIFormatter.RESET_INTENSITY))

        if (
            str(ANSIFormatter.Emphasis.UNDERLINE) in codes
            or str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE) in codes
        ):
            resets.append(str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']))

        if (
            str(ANSIFormatter.Effects.SLOW_BLINK) in codes
            or str(ANSIFormatter.Effects.RAPID_BLINK) in codes
        ):
            resets.append(str(ANSIFormatter.Effects.reset['RESET_BLINK']))

        if str(ANSIFormatter.Emphasis.ITALIC) in codes:
            resets.append(str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']))

        if str(ANSIFormatter.Emphasis.STRIKETHROUGH) in codes:
            resets.append(
                str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH'])
            )

        if str(ANSIFormatter.Effects.BG_FG_SWAP) in codes:
            resets.append(str(ANSIFormatter.Effects.reset['BG_FG_UNSWAP']))

        if str(ANSIFormatter.Effects.HIDE) in codes:
            resets.append(str(ANSIFormatter.Effects.reset['SHOW']))

        if any(
            c.startswith(str(ANSIFormatter.Background.CUSTOM.value))
            for c in codes
        ):
            resets.append(str(ANSIFormatter.Background.DEFAULT.value))

        if any(
            c.startswith(str(ANSIFormatter.Foreground.CUSTOM.value))
            for c in codes
        ):
            resets.append(str(ANSIFormatter.Foreground.DEFAULT.value))

        return ';'.join(resets)

    def _clear_codes(self) -> None:
        """Removes all cached codes from ``_codes``."""
        self._codes.clear()

    @overload
    def apply(
        self,
        text: str | list[str],
        *,
        sep: str = ', ',
        sep_end_str: str = '',
        sep_end: bool = True,
        finish: Literal[True],
        processed_sep: str = '',
        processed_sep_end_str: str = '',
        processed_sep_end: bool = False,
        prepend: str = '',
        append: str = '',
        style: str = '',
        clear_codes: bool = True,
    ) -> str: ...

    @overload
    def apply(
        self,
        text: str | list[str],
        *,
        sep: str = ', ',
        sep_end_str: str = '',
        sep_end: bool = True,
        finish: Literal[False] = False,
        processed_sep: str = '',
        processed_sep_end_str: str = '',
        processed_sep_end: bool = False,
        prepend: str = '',
        append: str = '',
        style: str = '',
        clear_codes: bool = True,
    ) -> Self: ...

    def apply(
        self,
        text: str | list[str],
        *,
        sep: str = ', ',
        sep_end_str: str = '',
        sep_end: bool = True,
        finish: bool = False,
        processed_sep: str = '',
        processed_sep_end_str: str = '',
        processed_sep_end: bool = False,
        prepend: str = '',
        append: str = '',
        style: str = '',
        clear_codes: bool = True,
    ) -> str | Self:
        """
        Apply accumulated style codes to ``text`` and cache the result.

        Args:
            text (str | list[str]):
                The text you wish to apply the previously accumulated style
                codes to.
            sep (str):
                If `text` was passed as a list, every str within that list
                is styled and joined together using this string.
            sep_end (bool):
                If this boolean is True (*True* by default) and ``text`` was
                passed as a list, the string passed to `sep` is appended to the
                end of joined strings (e.g. ``apply(['1', '4', '2'], sep=' + ',
                sep_end_str=' = ', style=...``); results is: ``"1 + 4 + 2 = "``
                ).
            sep_end_str (str):
                If `text` was passed as a list, every str within that list
                is styled and joined together using the `sep` string and this
                string is then appended. If you pass nothing to `sep_end_str`,
                or a falsy value, and text is a list, then `sep` is appended to
                the result of the joined strings.
            finish (bool):
                If True, all of the cached style strings are joined together
                using the ``processed_sep`` string. The ``processed_sep`` str
                is also appended to the joined strings if ``processed_sep_end``
                is True.
            processed_sep (str):
                The string to use when joining every styled str from cache.
                Only does something when ``finish`` is set to True.
            processed_sep_end (bool):
                If this boolean is True (*False* by default) and ``finish`` is
                True, ``processed_sep`` is appended to the joined cache
                strings if ``processed_sep_end_str`` is not provided, otherwise
                ``processed_sep_end_str`` is appended.
            processed_sep_end_str (str):
                If this string is provided (not falsy) and ``finish`` is True,
                then it is appended to the joined styled strings.
            prepend (str):
                Any raw (or custom styled) string you want to prepend to each
                string passed into ``text``.
            append (str):
                Any raw (or custom styled) string you want to append to each
                string passed into ``text``.
            style (str):
                The raw SGR style codes or fully formated SGR format as a str.
            clear_codes (bool):
                If ``clear_codes`` is True (*True* by default) then all of the
                cached codes are removed after applying them.

        Raises:
            ValueError:
                If ``text`` is empty, or if no style is available.

        Note:
            If ``style`` is provided, any codes accumulated via chained style
            methods (``bold()``, ``fg()``, etc.) are silently discarded and
            cleared. Consume pending codes with a prior ``apply()`` call before
            passing a ``style`` override, or avoid mixing both in the same
            segment.
        """
        if not text:
            raise ValueError('text must be non-empty.')

        active_codes = style.split(';') if style else self._codes.copy()

        _style = style if not active_codes else ';'.join(active_codes)

        if not _style:
            raise ValueError('Expected a style to apply to the text.')

        reset = self._compute_reset_codes(active_codes) or str(
            ANSIFormatter.RESET
        )

        processed = (
            prepend
            + (
                (
                    sep.join(
                        ANSIFormatter.escape(_style, t, reset=reset)
                        for t in text
                    )
                    + (
                        sep
                        if (sep_end and not sep_end_str)
                        else sep_end_str
                        if sep_end
                        else ''
                    )
                )
                if isinstance(text, list)
                else ANSIFormatter.escape(_style, text, reset=reset)
            )
            + append
        )

        self._formatted.append(processed)

        if clear_codes:
            self._clear_codes()

        if finish:
            result = processed_sep.join(self._formatted) + (
                processed_sep
                if (processed_sep_end and not processed_sep_end_str)
                else processed_sep_end_str
                if processed_sep_end
                else ''
            )
            self._formatted.clear()
            return result

        return self
