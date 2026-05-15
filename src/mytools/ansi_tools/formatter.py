from typing import Self, Literal, Union, overload
import re


#--{ Styles }--------------------------
def bubble(
    expected: str | list[str],
    at: str,
    lvalue: str,
    rvalue: str,
    compare: str = '==',
    prepend_why: str = '',
    append_why: str = ''
) -> str:
    style = ANSIFormatter.ESCAPE

    def code(*parts: int | str) -> str:
        return ';'.join(map(str, parts))

    def fg(r: int, g: int, b: int) -> str: return f'38;2;{r};{g};{b}'
    def bg(r: int, g: int, b: int) -> str: return f'48;2;{r};{g};{b}'

    ITALIC, UNDERLINE   = 3, 4
    DARK_BG             = bg(55, 65, 81)
    LIGHT_FG            = fg(248, 250, 252)
    light_on_dark       = code(LIGHT_FG, DARK_BG)
    pink_italic         = code(ITALIC, fg(248, 175, 195), DARK_BG)
    muted               = code(fg(148, 163, 184), DARK_BG)
    underlit            = code(ITALIC, UNDERLINE, light_on_dark)

    pill_fg = fg(55, 65, 81)
    L_CAP   = style(pill_fg, '\ue0b6')
    R_CAP   = style(pill_fg, '\ue0b4')

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



#--{ Logging }-------------------------
from pathlib import Path
import logging
LOG_FILEDIR: Path = Path(__file__).parent
LOG_FILENAME: str = 'example.log'
LOG_FILEPATH: Path = Path(f'{LOG_FILEDIR}/{LOG_FILENAME}')
LOG_FILE_ENCODING: str = 'UTF-8'
LOG_LEVEL: int = logging.DEBUG

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILEPATH,
    filemode='w',
    level=LOG_LEVEL,
    format='%(asctime)s @--> %(filename)s %(lineno)d %(funcName)s !--> [%(levelname)s] %(message)s',
    datefmt=r'%m-%d-%Y %H.%M.%S',
    encoding=LOG_FILE_ENCODING
)

#--{ ANSI String-Builder }---
from enum import Enum
class ANSIFormatter():
    ESCAPE_SEQUENCE = '\x1b['
    @classmethod
    def ESCAPE(cls, style: str | int, string: str, *, reset: str = '') -> str:
        """
        Prepends the escape sequence `\\x1b[` -- appends the sequence `\\x1b[0`
        
        ### ` reset `:
        - This will be used to replace the style-code appended to the `string`
         - example-
         ```
         ESCAPE(ANSIFormatter.Emphasis.ITALIC, 'Hello, world.', reset='23')
         # returns -> '\\x1b[3mHello, world.\\x1b[23m
         ```
        """
        end = reset or str(cls.RESET)
        return f'{cls.ESCAPE_SEQUENCE}{style}m{string}{cls.ESCAPE_SEQUENCE}{end}m'
    RESET = 0
    RESET_INTENSITY = 22 # includes Bold and Dim
    B8_COLOR = 5
    B24_COLOR = 2
    class Fonts(Enum): # FRAKTUR rarely supported
        DEFAULT_FONT, FONT1, FONT2, FONT3, FONT4, FONT5, FONT6, FONT7, FONT8, FONT9, FRAKTUR = range(10, 21)
    class Emphasis():
        BOLD = 1
        ITALIC = 3
        UNDERLINE = 4
        STRIKETHROUGH = 9
        DOUBLE_UNDERLINE = 21
        reset: dict[str, int] = {"RESET_ITALIC": 23,
                                 "RESET_UNDERLINE": 24,
                                 "RESET_STRIKETHROUGH": 29}
    class Effects():
        DIM = 2
        SLOW_BLINK = 5
        RAPID_BLINK = 6 #rarely supported
        BG_FG_SWAP = 7
        HIDE = 8
        reset: dict[str, int] = {"RESET_BLINK": 25,
                                 "BG_FG_UNSWAP": 27,
                                 "SHOW": 28}
    class Foreground(Enum):
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, CUSTOM, DEFAULT = range(30, 40)
    class Background(Enum):
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, CUSTOM, DEFAULT = range(40, 50)

class StyleBuilder:
    def __init__(self):
        self._codes: list[str] = []
        self._formatted: list[str] = [] # list of finished formatted/raw strings

    ANSI_ESCAPE_RE = re.compile(r'\x1b\[[\d;]*m')

    @overload
    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: Literal[False] = False,
        processed_sep: str = '',
        processed_sep_end: bool = False
    ) -> Self:
        ...
    @overload
    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: Literal[True],
        processed_sep: str = '',
        processed_sep_end: bool = False
    ) -> str:
        ...

    def add(
        self,
        *raw_text: str,
        sep: str = '',
        end_sep: str = ' ',
        finish: bool = False,
        processed_sep: str = '',
        processed_sep_end: bool = False
    ) -> str | Self:
        self._formatted.append(sep.join(raw_text) + end_sep)
        return (processed_sep.join([fs for fs in self._formatted]) + (processed_sep if processed_sep_end else '')) if finish else self

    def reset(self)                 -> Self: self._codes.append(str(ANSIFormatter.RESET));                                  return self
    def reset_codes(self)           -> Self: self._codes.append(self._reset_codes);                                         return self
    
    def bold(self)                  -> Self: self._codes.append(str(ANSIFormatter.Emphasis.BOLD));                          return self
    def italic(self)                -> Self: self._codes.append(str(ANSIFormatter.Emphasis.ITALIC));                        return self
    def underline(self)             -> Self: self._codes.append(str(ANSIFormatter.Emphasis.UNDERLINE));                     return self
    def strikethrought(self)        -> Self: self._codes.append(str(ANSIFormatter.Emphasis.STRIKETHROUGH));                 return self
    def doubly_underline(self)      -> Self: self._codes.append(str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE));              return self
    
    def dim(self)                   -> Self: self._codes.append(str(ANSIFormatter.Effects.DIM));                            return self
    def slow_blink(self)            -> Self: self._codes.append(str(ANSIFormatter.Effects.SLOW_BLINK));                     return self
    def fast_blink(self)            -> Self: self._codes.append(str(ANSIFormatter.Effects.RAPID_BLINK));                    return self
    def bg_fg_swap(self)            -> Self: self._codes.append(str(ANSIFormatter.Effects.BG_FG_SWAP));                     return self
    def hide(self)                  -> Self: self._codes.append(str(ANSIFormatter.Effects.HIDE));                           return self
    
    def reset_intensity(self)       -> Self: self._codes.append(str(ANSIFormatter.RESET_INTENSITY));                        return self
    def reset_underline(self)       -> Self: self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']));      return self
    def reset_italic(self)          -> Self: self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']));         return self
    def reset_strikethrough(self)   -> Self: self._codes.append(str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH']));  return self
    def reset_blink(self)           -> Self: self._codes.append(str(ANSIFormatter.Effects.reset['RESET_BLINK']));           return self
    def bg_fg_reswap(self)          -> Self: self._codes.append(str(ANSIFormatter.Effects.reset['BG_FG_RESWAP']));          return self
    def show(self)                  -> Self: self._codes.append(str(ANSIFormatter.Effects.reset['SHOW']));                  return self
    def reset_bg(self)              -> Self: self._codes.append(str(ANSIFormatter.Background.DEFAULT));                     return self
    def reset_fg(self)              -> Self: self._codes.append(str(ANSIFormatter.Foreground.DEFAULT));                     return self
    
    def fg(self, r: int, g: int | None = None, b: int | None = None, *, b24: bool = True) -> Self:
        if (g is None or b is None) and b24:
            raise ValueError(bubble(expected=['r', 'g', 'b'], at='fg', lvalue='b24', rvalue='True', prepend_why=' keyword-argument'))

        self._codes.append(f'{ANSIFormatter.Foreground.CUSTOM.value};{ANSIFormatter.B24_COLOR if b24 else ANSIFormatter.B8_COLOR};{r}{f";{g};{b}" if b24 else ""}')
        return self

    def bg(self, r: int, g: int | None = None, b: int | None = None, /, *, b24: bool = True) -> Self:
        if (g is None or b is None) and b24:
            raise ValueError(bubble(expected=['r', 'g', 'b'], at='bg', lvalue='b24', rvalue='True', prepend_why=' keyword-argument'))
        
        self._codes.append(f'{ANSIFormatter.Background.CUSTOM.value};{ANSIFormatter.B24_COLOR if b24 else ANSIFormatter.B8_COLOR};{r}{f";{g};{b}" if b24 else ""}')
        return self


    @property
    def _reset_codes(self) -> str:
        resets = []
        if str(ANSIFormatter.Emphasis.BOLD)             in self._codes or str(ANSIFormatter.Effects.DIM)               in self._codes: resets.append(str(ANSIFormatter.RESET_INTENSITY))
        if str(ANSIFormatter.Emphasis.UNDERLINE)        in self._codes or str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE) in self._codes: resets.append(str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']))
        if str(ANSIFormatter.Effects.SLOW_BLINK)        in self._codes or str(ANSIFormatter.Effects.RAPID_BLINK)       in self._codes: resets.append(str(ANSIFormatter.Effects.reset['RESET_BLINK']))
        if str(ANSIFormatter.Emphasis.ITALIC)           in self._codes: resets.append(str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']))
        if str(ANSIFormatter.Emphasis.STRIKETHROUGH)    in self._codes: resets.append(str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH']))
        if str(ANSIFormatter.Effects.BG_FG_SWAP)        in self._codes: resets.append(str(ANSIFormatter.Effects.reset['BG_FG_UNSWAP']))
        if str(ANSIFormatter.Effects.HIDE)              in self._codes: resets.append(str(ANSIFormatter.Effects.reset['SHOW']))
        if any(c.startswith(str(ANSIFormatter.Background.CUSTOM.value)) for c in self._codes): resets.append(str(ANSIFormatter.Background.DEFAULT.value))
        if any(c.startswith(str(ANSIFormatter.Foreground.CUSTOM.value)) for c in self._codes): resets.append(str(ANSIFormatter.Foreground.DEFAULT.value))
        return ';'.join(resets)

    def _clear_codes(self) -> None: self._codes.clear()


    @overload
    def apply(self, text: str | list[str], *, sep: str = ', ', sep_end: bool = True, finish: Literal[True], processed_sep: str = '', processed_sep_end: bool = False, prepend: str = '', append: str = '', style: str = '') -> str:
        ... 
    @overload
    def apply(self, text: str | list[str], *, sep: str = ', ', sep_end: bool = True, finish: Literal[False] = False, processed_sep: str = '', processed_sep_end: bool = False, prepend: str = '', append: str = '', style: str = '') -> Self:
        ...

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
        style: str = ''
    ) -> Union[str, Self]:
        """
        Args:
            text (str | list[str]):
                The text that will be formatted.
            sep (str, optional):
                Only used if ``text`` is an instance of a list; defaults to "".
                A string used with the ``.join()`` method to join each ``text``
                entry together.
            sep_end (bool, optional):
                Only used if ``text`` is an instance of a list; defaults to True.
                If True, the ``sep`` parameter is appended to the sep joined,
                formatted text.
            finish (bool, optional):
                Defaults to False;
                If ``True``, joins all of the cached formatted strings using
                the string provided by the ``processed_sep`` parameter and
                returns it.
                If ``False``, appends the formatted string to cache, undoes added
                formatting, and returns ``self``.
            processed_sep (str, optional):
                Defaults to ""; used as the join string to join each cached
                entry together when ``finish`` is set to True; is appended to
                the end of the formatted string result if the
                ``processed_sep_end`` parameter is True.
            processed_sep_end (bool, optional):
                Defaults to False; If true, and ``finish`` is set to True, the
                ``processed_sep`` string is appended to the end of your result
                (will be appended AFTER the ``append`` parameter).
            prepend (str, optional):
                Defaults to ""; Takes a string and prepends it to the result of
                your passed in text (joins all text's, if a list, before prepending)
            append (str, optional):
                Defaults to ""; Takes a string and appends it to the result of
                your passed in text (joins all text's, if a list, before appending)
        """

        _style = style or ';'.join(self._codes)
        reset = self._reset_codes
        if not _style or not reset:
            raise ValueError('Expected a style to apply to the text')

        processed = prepend + (
            (sep.join
                (
                    ANSIFormatter.ESCAPE(_style, t, reset=reset)
                    for t in text
                ) + (sep if sep_end else ''))
            if isinstance(text, list)
            else ANSIFormatter.ESCAPE(_style, text, reset=reset)
        ) + append if text else ''
        
        if processed:
            self._formatted.append(processed)
            self._clear_codes()
            return (processed_sep.join([fs for fs in self._formatted]) + (processed_sep if processed_sep_end else '')) if finish else self
        return processed