"""
ANSI terminal styling utilities.

Provides:
- ``ANSIFormatter`` — constants and a low-level escape-sequence builder.
- ``StyleBuilder``  — a fluent builder for composing and applying ANSI styles.
- ``bubble``        — a pre-styled diagnostic string for surfacing assertion or
					  validation errors in the terminal.
"""

from __future__ import annotations

from enum import Enum
from typing import ClassVar, Literal, Self, overload
import re

__all__ = ['ANSIFormatter', 'StyleBuilder', 'bubble']


# ——{ ANSI Formatter }——————————————————
class ANSIFormatter:
	"""
	Low-level ANSI escape-sequence constants and builder.

	Contains:
	- ``ESCAPE`` — classmethod that wraps a string in an SGR escape sequence.
	- ``Fonts``, ``Emphasis``, ``Effects``, ``Foreground``, ``Background`` —
	nested namespaces grouping related SGR codes.

	Typical usage is through ``StyleBuilder``, which wraps these constants in
	a fluent API. Direct use of ``ESCAPE`` is useful when you need a one-off
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
	def ESCAPE(cls, style: str | int, string: str, *, reset: str = '') -> str:
		"""
		Wrap ``string`` in an SGR escape sequence using ``style``.

		Opens with ``\\x1b[<style>m`` and closes with ``\\x1b[<reset>m``.
		If ``reset`` is omitted the sequence closes with ``\\x1b[0m`` (full
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

		                        ESCAPE(
		                            ANSIFormatter.Emphasis.ITALIC,
		                            'Hello',
		                            reset='23',
		                        )
		                        # -> '\\x1b[3mHello\\x1b[23m'

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
		"""
		SGR codes for text-emphasis styles and their targeted resets.

		Use ``reset`` to undo a specific emphasis without a full ``\\x1b[0m``
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

		``RAPID_BLINK`` (6) is rarely supported by modern terminals.
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


# ——{ Styles }——————————————————————————
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
	style = ANSIFormatter.ESCAPE

	def code(*parts: int | str) -> str:
		return ';'.join(map(str, parts))

	def fg(r: int, g: int, b: int) -> str:
		return f'38;2;{r};{g};{b}'

	def bg(r: int, g: int, b: int) -> str:
		return f'48;2;{r};{g};{b}'

	ITALIC, UNDERLINE = 3, 4

	DARK_BG = bg(55, 65, 81)
	LIGHT_FG = fg(248, 250, 252)

	light_on_dark = code(LIGHT_FG, DARK_BG)
	pink_italic = code(ITALIC, fg(248, 175, 195), DARK_BG)
	muted = code(fg(148, 163, 184), DARK_BG)
	underlit = code(ITALIC, UNDERLINE, light_on_dark)

	pill_fg = fg(55, 65, 81)

	L_CAP = style(pill_fg, '\ue0b6')
	R_CAP = style(pill_fg, '\ue0b4')

	def pill(_style: str, text: str | list[str]) -> str:
		inner = (
			', '.join(style(_style, t) for t in text)
			if isinstance(text, list)
			else style(_style, text)
		)
		return f'{L_CAP}{inner}{R_CAP}'

	def comparison_pill() -> str:
		inner = (
			f'{style(underlit, lvalue)}'
			f'{style(muted, f" {compare} ")}'
			f'{style(underlit, rvalue)}'
		)
		return f'{L_CAP}{inner}{R_CAP}'

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


# ——{ Style Builder }———————————————————
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
		self._codes.append(str(ANSIFormatter.RESET))
		return self

	def bold(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.BOLD))
		return self

	def italic(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.ITALIC))
		return self

	def underline(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.UNDERLINE))
		return self

	def strikethrough(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.STRIKETHROUGH))
		return self

	def double_underline(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE))
		return self

	def dim(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.DIM))
		return self

	def slow_blink(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.SLOW_BLINK))
		return self

	def fast_blink(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.RAPID_BLINK))
		return self

	def bg_fg_swap(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.BG_FG_SWAP))
		return self

	def hide(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.HIDE))
		return self

	def reset_intensity(self) -> Self:
		self._codes.append(str(ANSIFormatter.RESET_INTENSITY))
		return self

	def reset_underline(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']))
		return self

	def reset_italic(self) -> Self:
		self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']))
		return self

	def reset_strikethrough(self) -> Self:
		self._codes.append(
			str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH'])
		)
		return self

	def reset_blink(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.reset['RESET_BLINK']))
		return self

	def bg_fg_reswap(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.reset['BG_FG_UNSWAP']))
		return self

	def show(self) -> Self:
		self._codes.append(str(ANSIFormatter.Effects.reset['SHOW']))
		return self

	def reset_bg(self) -> Self:
		self._codes.append(str(ANSIFormatter.Background.DEFAULT.value))
		return self

	def reset_fg(self) -> Self:
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
		Set the foreground colour.
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
		Set the background colour.
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
		"""
		Compute targeted reset codes for a given style-code set.
		"""
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
		self._codes.clear()

	@overload
	def apply(
		self,
		text: str | list[str],
		*,
		sep: str = ', ',
		sep_end: bool = True,
		finish: Literal[True],
		processed_sep: str = '',
		processed_sep_end: bool = False,
		prepend: str = '',
		append: str = '',
		style: str = '',
	) -> str: ...

	@overload
	def apply(
		self,
		text: str | list[str],
		*,
		sep: str = ', ',
		sep_end: bool = True,
		finish: Literal[False] = False,
		processed_sep: str = '',
		processed_sep_end: bool = False,
		prepend: str = '',
		append: str = '',
		style: str = '',
	) -> Self: ...

	def apply(
		self,
		text: str | list[str],
		*,
		sep: str = ', ',
		sep_end: bool = True,
		finish: bool = False,
		processed_sep: str = '',
		processed_sep_end: bool = False,
		prepend: str = '',
		append: str = '',
		style: str = '',
	) -> str | Self:
		"""
		Apply accumulated style codes to ``text`` and cache the result.

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

		_style = style or ';'.join(active_codes)

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
						ANSIFormatter.ESCAPE(_style, t, reset=reset)
						for t in text
					)
					+ (sep if sep_end else '')
				)
				if isinstance(text, list)
				else ANSIFormatter.ESCAPE(_style, text, reset=reset)
			)
			+ append
		)

		self._formatted.append(processed)

		self._clear_codes()

		if finish:
			result = processed_sep.join(self._formatted) + (
				processed_sep if processed_sep_end else ''
			)
			self._formatted.clear()
			return result

		return self
