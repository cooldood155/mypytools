"""Tests for the ``src/mytools/ansi_tools/`` package."""

# Standard library imports
from importlib import import_module
from sys import stderr, exit as sysexit, modules

# Third party imports
from pytest import raises, fixture, fail

try:
    # Project imports
    import mypytools
except ModuleNotFoundError:
    print(
        'ModuleNotFoundError: mypytools is not installed.\n'
        'Install it from: https://github.com/cooldood155/mypytools/releases',
        file=stderr,
    )
    sysexit(1)


@fixture
def fresh_imports():
    """
    Dynamically imports packages and ensures they are wiped after the test.

    Catches any ModuleNotFoundError's or ImportError's that may occur.
    """
    # Define import targets
    module_names = [
        'mypytools.ansi_tools',
        'mypytools.ansi_tools.formatter',
        'mypytools.ansi_tools.style_builder',
    ]

    # Perform dynamic imports
    imported_modules = {}
    try:
        for name in module_names:
            imported_modules[name] = import_module(name)
    except (ModuleNotFoundError, ImportError) as e:
        fail(f'Setup import failed for {getattr(e, "name", "unknown")}: {e}')

    # YIELD: pass the imported modules to pytest.fixture
    yield imported_modules

    # TEARDOWN: remove the imported modules
    for name in module_names:
        if name in modules:
            del modules[name]


ESC = '\x1b['


# ——{ Imports }————————————————————————————————————————————————————————————————


def test_formatter_classes_exist(fresh_imports):
    """Test that the expected classes exist inside the modules."""
    formatter_mod = fresh_imports['mypytools.ansi_tools.formatter']
    style_mod = fresh_imports['mypytools.ansi_tools.style_builder']

    assert hasattr(formatter_mod, 'ANSIFormatter')
    assert hasattr(style_mod, 'StyleBuilder')
    assert hasattr(style_mod, 'bubble')


def test_package_level_exposure(fresh_imports):
    """Test that the top-level __init__ exposes the sub-tools."""
    ansi_tools = fresh_imports['mypytools.ansi_tools']

    assert hasattr(ansi_tools, 'ANSIFormatter')
    assert hasattr(ansi_tools, 'StyleBuilder')
    assert hasattr(ansi_tools, 'bubble')


# ——{ mypytools.ANSIFormatter.escape }—————————————————————————————————————————


class TestANSIFormatterESCAPE:
    """Test the ``ANSIFormatter.escape()`` class method."""

    def test_wraps_string_with_style(self):
        """
        Escape a string with the style code ``1``.

        Check if the result starts and ends with the correct ESC sequences.
        """
        result = mypytools.ANSIFormatter.escape('1', 'hello')
        assert result == f'{ESC}1mhello{ESC}0m'

    def test_uses_full_reset_by_default(self):
        r"""
        Escape a string.

        Check if the result ends with the default ``\x1b[0m`` reset ESC string.
        """
        result = mypytools.ANSIFormatter.escape('3', 'hi')
        assert result.endswith(f'{ESC}0m')

    def test_uses_custom_reset(self):
        r"""
        Escape a string with a custom ``reset`` argument.

        Check if the result ends with the custom ``\x1b[23m`` reset ESC string.
        """
        result = mypytools.ANSIFormatter.escape('3', 'hi', reset='23')
        assert result.endswith(f'{ESC}23m')

    def test_int_style_code(self):
        """
        Escape a string with the imputted style as an int ``1`` not a str.

        Check if the result starts and ends with the correct ESC sequences.
        """
        result = mypytools.ANSIFormatter.escape(1, 'bold')
        assert result == f'{ESC}1mbold{ESC}0m'

    def test_compound_style_code(self):
        """
        Escape a string with the imputted style being a compound ``1;3``.

        Check if the result contains the correct ESC sequences around the text.
        """
        result = mypytools.ANSIFormatter.escape('1;3', 'text')
        assert result == f'{ESC}1;3mtext{ESC}0m'


# ——{ mypytools.ANSIFormatter constants }——————————————————————————————————————


class TestANSIFormatterConstants:
    """Test ``ANSIFormatter``'s top-level constants."""

    def test_reset(self):
        """Test ``ANSIFormatter.RESET`` **==** ``0``."""
        assert mypytools.ANSIFormatter.RESET == 0

    def test_reset_intensity(self):
        """Test ``ANSIFormatter.RESET_INTENSITY`` **==** ``22``."""
        assert mypytools.ANSIFormatter.RESET_INTENSITY == 22

    def test_b8_color(self):
        """Test ``ANSIFormatter.B8_COLOR`` **==** ``5``."""
        assert mypytools.ANSIFormatter.B8_COLOR == 5

    def test_b24_color(self):
        """Test ``ANSIFormatter.B24_COLOR`` **==** ``2``."""
        assert mypytools.ANSIFormatter.B24_COLOR == 2


# ——{ mypytools.ANSIFormatter.Emphasis }———————————————————————————————————————


class TestEmphasis:
    """Test ``ANSIFormatter.Emphasis`` constants."""

    def test_bold(self):
        """Test ``ANSIFormatter.Emphasis.BOLD`` **==** ``1``."""
        assert mypytools.ANSIFormatter.Emphasis.BOLD == 1

    def test_italic(self):
        """Test ``ANSIFormatter.Emphasis.ITALIC`` **==** ``3``."""
        assert mypytools.ANSIFormatter.Emphasis.ITALIC == 3

    def test_underline(self):
        """Test ``ANSIFormatter.Emphasis.UNDERLINE`` **==** ``4``."""
        assert mypytools.ANSIFormatter.Emphasis.UNDERLINE == 4

    def test_strikethrough(self):
        """Test ``ANSIFormatter.Emphasis.STRIKETHROUGH`` **==** ``9``."""
        assert mypytools.ANSIFormatter.Emphasis.STRIKETHROUGH == 9

    def test_double_underline(self):
        """Test ``ANSIFormatter.Emphasis.DOUBLE_UNDERLINE`` **==** `21`."""
        assert mypytools.ANSIFormatter.Emphasis.DOUBLE_UNDERLINE == 21

    def test_reset_italic(self):
        """Test `ANSIFormatter.Emphasis.reset['RESET_ITALIC']` **==** `23`."""
        assert mypytools.ANSIFormatter.Emphasis.reset['RESET_ITALIC'] == 23

    def test_reset_underline(self):
        """
        Test `ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']` **==** `24`.

        - Same reset code as `double_underline`
        """
        assert mypytools.ANSIFormatter.Emphasis.reset['RESET_UNDERLINE'] == 24

    def test_reset_strikethrough(self):
        """
        Test `ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH']` **==** `29`.

        - Strike through text
        """
        assert (
            mypytools.ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH'] == 29
        )


# ——{ mypytools.ANSIFormatter.Effects }————————————————————————————————————————


class TestEffects:
    """Test ``ANSIFormatter.Effects`` constants."""

    def test_dim(self):
        """Test ``ANSIFormatter.Effects.DIM`` **==** ``2``."""
        assert mypytools.ANSIFormatter.Effects.DIM == 2

    def test_slow_blink(self):
        """Test ``ANSIFormatter.Effects.SLOW_BLINK`` **==** ``5``."""
        assert mypytools.ANSIFormatter.Effects.SLOW_BLINK == 5

    def test_rapid_blink(self):
        """Test ``ANSIFormatter.Effects.RAPID_BLINK`` **==** ``6``."""
        assert mypytools.ANSIFormatter.Effects.RAPID_BLINK == 6

    def test_bg_fg_swap(self):
        """Test ``ANSIFormatter.Effects.BG_FG_SWAP`` **==** ``7``."""
        assert mypytools.ANSIFormatter.Effects.BG_FG_SWAP == 7

    def test_hide(self):
        """Test ``ANSIFormatter.Effects.HIDE`` **==** ``8``."""
        assert mypytools.ANSIFormatter.Effects.HIDE == 8

    def test_reset_blink(self):
        """Test ``ANSIFormatter.Effects.reset['RESET_BLINK']`` **==** `25`."""
        assert mypytools.ANSIFormatter.Effects.reset['RESET_BLINK'] == 25

    def test_bg_fg_unswap(self):
        """Test ``ANSIFormatter.Effects.reset['BG_FG_UNSWAP']`` **==** `27`."""
        assert mypytools.ANSIFormatter.Effects.reset['BG_FG_UNSWAP'] == 27

    def test_show(self):
        """Test ``ANSIFormatter.Effects.reset['SHOW']`` **==** `28`."""
        assert mypytools.ANSIFormatter.Effects.reset['SHOW'] == 28


# ——{ mypytools.ANSIFormatter.Foreground / Background }————————————————————————


class TestForeground:
    """Test ``ANSIFormatter.Foreground`` constants."""

    def test_black(self):
        """Test ``ANSIFormatter.Foreground.BLACK.value`` **==** ``30``."""
        assert mypytools.ANSIFormatter.Foreground.BLACK.value == 30

    def test_red(self):
        """Test ``ANSIFormatter.Foreground.RED.value`` **==** ``31``."""
        assert mypytools.ANSIFormatter.Foreground.RED.value == 31

    def test_green(self):
        """Test ``ANSIFormatter.Foreground.GREEN.value`` **==** ``32``."""
        assert mypytools.ANSIFormatter.Foreground.GREEN.value == 32

    def test_yellow(self):
        """Test ``ANSIFormatter.Foreground.YELLOW.value`` **==** ``33``."""
        assert mypytools.ANSIFormatter.Foreground.YELLOW.value == 33

    def test_blue(self):
        """Test ``ANSIFormatter.Foreground.BLUE.value`` **==** ``34``."""
        assert mypytools.ANSIFormatter.Foreground.BLUE.value == 34

    def test_magenta(self):
        """Test ``ANSIFormatter.Foreground.MAGENTA.value`` **==** ``35``."""
        assert mypytools.ANSIFormatter.Foreground.MAGENTA.value == 35

    def test_cyan(self):
        """Test ``ANSIFormatter.Foreground.CYAN.value`` **==** ``36``."""
        assert mypytools.ANSIFormatter.Foreground.CYAN.value == 36

    def test_white(self):
        """Test ``ANSIFormatter.Foreground.WHITE.value`` **==** ``37``."""
        assert mypytools.ANSIFormatter.Foreground.WHITE.value == 37

    def test_custom(self):
        """Test ``ANSIFormatter.Foreground.CUSTOM.value`` **==** ``38``."""
        assert mypytools.ANSIFormatter.Foreground.CUSTOM.value == 38

    def test_default(self):
        """Test ``ANSIFormatter.Foreground.DEFAULT.value`` **==** ``39``."""
        assert mypytools.ANSIFormatter.Foreground.DEFAULT.value == 39


class TestBackground:
    """Test ``ANSIFormatter.Background`` constants."""

    def test_black(self):
        """Test ``ANSIFormatter.Background.BLACK.value`` **==** ``40``."""
        assert mypytools.ANSIFormatter.Background.BLACK.value == 40

    def test_red(self):
        """Test ``ANSIFormatter.Background.RED.value`` **==** ``41``."""
        assert mypytools.ANSIFormatter.Background.RED.value == 41

    def test_green(self):
        """Test ``ANSIFormatter.Background.GREEN.value`` **==** ``42``."""
        assert mypytools.ANSIFormatter.Background.GREEN.value == 42

    def test_yellow(self):
        """Test ``ANSIFormatter.Background.YELLOW.value`` **==** ``43``."""
        assert mypytools.ANSIFormatter.Background.YELLOW.value == 43

    def test_blue(self):
        """Test ``ANSIFormatter.Background.BLUE.value`` **==** ``44``."""
        assert mypytools.ANSIFormatter.Background.BLUE.value == 44

    def test_magenta(self):
        """Test ``ANSIFormatter.Background.MAGENTA.value`` **==** ``45``."""
        assert mypytools.ANSIFormatter.Background.MAGENTA.value == 45

    def test_cyan(self):
        """Test ``ANSIFormatter.Background.CYAN.value`` **==** ``46``."""
        assert mypytools.ANSIFormatter.Background.CYAN.value == 46

    def test_white(self):
        """Test ``ANSIFormatter.Background.WHITE.value`` **==** ``47``."""
        assert mypytools.ANSIFormatter.Background.WHITE.value == 47

    def test_custom(self):
        """Test ``ANSIFormatter.Background.CUSTOM.value`` **==** ``48``."""
        assert mypytools.ANSIFormatter.Background.CUSTOM.value == 48

    def test_default(self):
        """Test ``ANSIFormatter.Background.DEFAULT.value`` **==** ``49``."""
        assert mypytools.ANSIFormatter.Background.DEFAULT.value == 49


# ——{ mypytools.StyleBuilder._compute_reset_codes }————————————————————————————


class TestComputeResetCodes:
    """Test ``StyleBuilder._compute_reset_codes()``."""

    def test_bold_returns_reset_intensity(self):
        """Test ``StyleBuilder._compute_reset_codes('1')`` gives ``22``."""
        codes = [str(mypytools.ANSIFormatter.Emphasis.BOLD)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(mypytools.ANSIFormatter.RESET_INTENSITY) in result.split(';')

    def test_dim_returns_reset_intensity(self):
        """Test ``StyleBuilder._compute_reset_codes('2')`` gives ``22``."""
        codes = [str(mypytools.ANSIFormatter.Effects.DIM)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(mypytools.ANSIFormatter.RESET_INTENSITY) in result.split(';')

    def test_italic_returns_reset_italic(self):
        """Test ``StyleBuilder._compute_reset_codes('3')`` gives ``23``."""
        codes = [str(mypytools.ANSIFormatter.Emphasis.ITALIC)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Emphasis.reset['RESET_ITALIC']
        ) in result.split(';')

    def test_underline_returns_reset_underline(self):
        """Test ``StyleBuilder._compute_reset_codes('4')`` gives ``24``."""
        codes = [str(mypytools.ANSIFormatter.Emphasis.UNDERLINE)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']
        ) in result.split(';')

    def test_strikethrough_returns_reset_strikethrough(self):
        """Test ``StyleBuilder._compute_reset_codes('9')`` gives ``29``."""
        codes = [str(mypytools.ANSIFormatter.Emphasis.STRIKETHROUGH)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH']
        ) in result.split(';')

    def test_slow_blink_returns_reset_blink(self):
        """Test ``StyleBuilder._compute_reset_codes('5')`` gives ``25``."""
        codes = [str(mypytools.ANSIFormatter.Effects.SLOW_BLINK)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Effects.reset['RESET_BLINK']
        ) in result.split(';')

    def test_rapid_blink_returns_reset_blink(self):
        """Test ``StyleBuilder._compute_reset_codes('6')`` gives ``25``."""
        codes = [str(mypytools.ANSIFormatter.Effects.RAPID_BLINK)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Effects.reset['RESET_BLINK']
        ) in result.split(';')

    def test_bg_fg_swap_returns_unswap(self):
        """Test ``StyleBuilder._compute_reset_codes('7')`` gives ``27``."""
        codes = [str(mypytools.ANSIFormatter.Effects.BG_FG_SWAP)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Effects.reset['BG_FG_UNSWAP']
        ) in result.split(';')

    def test_hide_returns_show(self):
        """Test ``StyleBuilder._compute_reset_codes('8')`` gives ``28``."""
        codes = [str(mypytools.ANSIFormatter.Effects.HIDE)]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Effects.reset['SHOW']
        ) in result.split(';')

    def test_custom_fg_returns_fg_default(self):
        """Test ``StyleBuilder._compute_reset_codes('38;2;255;0;0')``."""
        codes = [f'{mypytools.ANSIFormatter.Foreground.CUSTOM.value};2;255;0;0']
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Foreground.DEFAULT.value
        ) in result.split(';')

    def test_custom_bg_returns_bg_default(self):
        """Test ``StyleBuilder._compute_reset_codes('48;2;0;0;255')``."""
        codes = [f'{mypytools.ANSIFormatter.Background.CUSTOM.value};2;0;0;255']
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        assert str(
            mypytools.ANSIFormatter.Background.DEFAULT.value
        ) in result.split(';')

    def test_unknown_codes_return_empty_string(self):
        """Test ``StyleBuilder._compute_reset_codes(['99'])`` gives ``''``."""
        result = mypytools.StyleBuilder._compute_reset_codes(['99'])
        assert result == ''

    def test_empty_codes_return_empty_string(self):
        """Test ``StyleBuilder._compute_reset_codes([])`` gives ``''``."""
        result = mypytools.StyleBuilder._compute_reset_codes([])
        assert result == ''

    def test_multiple_codes_return_all_resets(self):
        """Test `StyleBuilder._compute_reset_codes(['1', '3'])` is correct."""
        codes = [
            str(mypytools.ANSIFormatter.Emphasis.BOLD),
            str(mypytools.ANSIFormatter.Emphasis.ITALIC),
        ]
        result = mypytools.StyleBuilder._compute_reset_codes(codes)
        parts = result.split(';')
        assert str(mypytools.ANSIFormatter.RESET_INTENSITY) in parts
        assert (
            str(mypytools.ANSIFormatter.Emphasis.reset['RESET_ITALIC']) in parts
        )


# ——{ mypytools.StyleBuilder style methods }————————————————————————————————————


class TestStyleBuilderStyleMethods:
    """Test `StyleBuilder` style methods."""

    def test_bold_appends_code(self):
        """Test `StyleBuilder().bold()` contains style code `1`."""
        sb = mypytools.StyleBuilder()
        sb.bold()
        assert str(mypytools.ANSIFormatter.Emphasis.BOLD) in sb._codes

    def test_bold_styled_string(self):
        """Test `StyleBuilder().bold()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.bold()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}1mhello{ESC}22m'

    def test_italic_appends_code(self):
        """Test `StyleBuilder().italic()` contains style code `3`."""
        sb = mypytools.StyleBuilder()
        sb.italic()
        assert str(mypytools.ANSIFormatter.Emphasis.ITALIC) in sb._codes

    def test_italic_styled_string(self):
        """Test `StyleBuilder().italic()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.italic()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}3mhello{ESC}23m'

    def test_underline_appends_code(self):
        """Test `StyleBuilder().underline()` constains style code `4`."""
        sb = mypytools.StyleBuilder()
        sb.underline()
        assert str(mypytools.ANSIFormatter.Emphasis.UNDERLINE) in sb._codes

    def test_underline_styled_string(self):
        """Test `StyleBuilder().underline()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.underline()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}4mhello{ESC}24m'

    def test_strikethrough_appends_code(self):
        """Test `StyleBuilder().strikethrough()` contains style code `9`."""
        sb = mypytools.StyleBuilder()
        sb.strikethrough()
        assert str(mypytools.ANSIFormatter.Emphasis.STRIKETHROUGH) in sb._codes

    def test_strikethrough_styled_string(self):
        """Test `StyleBuilder().strikethrough()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.strikethrough()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}9mhello{ESC}29m'

    def test_double_underline_appends_code(self):
        """Test `StyleBuilder().double_underline()` contains code `21`."""
        sb = mypytools.StyleBuilder()
        sb.double_underline()
        assert (
            str(mypytools.ANSIFormatter.Emphasis.DOUBLE_UNDERLINE) in sb._codes
        )

    def test_double_underline_styled_string(self):
        """Test `StyleBuilder().double_underline()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.double_underline()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}21mhello{ESC}24m'

    def test_dim_appends_code(self):
        """Test `StyleBuilder().dim()` contains style code `2`."""
        sb = mypytools.StyleBuilder()
        sb.dim()
        assert str(mypytools.ANSIFormatter.Effects.DIM) in sb._codes

    def test_dim_styled_string(self):
        """Test `StyleBuilder().dim()` is styled correclty."""
        sb = mypytools.StyleBuilder()
        sb.dim()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}2mhello{ESC}22m'

    def test_slow_blink_appends_code(self):
        """Test `StyleBuilder().slow_blink()` contains style code `5`."""
        sb = mypytools.StyleBuilder()
        sb.slow_blink()
        assert str(mypytools.ANSIFormatter.Effects.SLOW_BLINK) in sb._codes

    def test_slow_blink_styled_string(self):
        """Test `StyleBuilder().slow_blink()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.slow_blink()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}5mhello{ESC}25m'

    def test_fast_blink_appends_code(self):
        """Test `StyleBuilder().slow_blink()` contains style code `6`."""
        sb = mypytools.StyleBuilder()
        sb.fast_blink()
        assert str(mypytools.ANSIFormatter.Effects.RAPID_BLINK) in sb._codes

    def test_fast_blink_styled_string(self):
        """Test `StyleBuilder().slow_blink()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.fast_blink()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}6mhello{ESC}25m'

    def test_bg_fg_swap_appends_code(self):
        """Test `StyleBuilder().slow_blink()` contains style code `7`."""
        sb = mypytools.StyleBuilder()
        sb.bg_fg_swap()
        assert str(mypytools.ANSIFormatter.Effects.BG_FG_SWAP) in sb._codes

    def test_bg_fg_swap_styled_string(self):
        """Test `StyleBuilder().slow_blink()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.bg_fg_swap()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}7mhello{ESC}27m'

    def test_hide_appends_code(self):
        """Test `StyleBuilder().slow_blink()` contains style code `8`."""
        sb = mypytools.StyleBuilder()
        sb.hide()
        assert str(mypytools.ANSIFormatter.Effects.HIDE) in sb._codes

    def test_hide_styled_string(self):
        """Test `StyleBuilder().slow_blink()` is styled correctly."""
        sb = mypytools.StyleBuilder()
        sb.hide()
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}8mhello{ESC}28m'

    def test_all_methods_return_self(self):
        """Test that all `StyleBuilder` methods return `self`."""
        sb = mypytools.StyleBuilder()
        assert sb.bold() is sb
        assert sb.italic() is sb
        assert sb.underline() is sb
        assert sb.strikethrough() is sb
        assert sb.double_underline() is sb
        assert sb.dim() is sb
        assert sb.slow_blink() is sb
        assert sb.fast_blink() is sb
        assert sb.bg_fg_swap() is sb
        assert sb.hide() is sb

    def test_multiple_styles_accumulate(self):
        """Test `StyleBuilder().bold().italic()` contains both styles."""
        sb = mypytools.StyleBuilder()
        sb.bold().italic()
        assert str(mypytools.ANSIFormatter.Emphasis.BOLD) in sb._codes
        assert str(mypytools.ANSIFormatter.Emphasis.ITALIC) in sb._codes
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}1;3mhello{ESC}22;23m'


# ——{ mypytools.StyleBuilder.fg / bg }—————————————————————————————————————————


class TestStyleBuilderFgBg:
    """Test `StyleBuilder.fg` and `StyleBuilder.bg`."""

    def test_fg_b24_missing_g_and_b_raises(self):
        """Test `fg(255)` raises `ValueError`, missing `g`, `b` arguments."""
        with raises(ValueError):
            mypytools.StyleBuilder().fg(255)

    def test_fg_b24_missing_b_raises(self):
        """Test `fg(255, 0)` raises `ValueError`, missing `b` argument."""
        with raises(ValueError):
            mypytools.StyleBuilder().fg(255, 0)

    def test_fg_b24_with_all_channels(self):
        """Test `fg(255, 0, 128)` contains style codes."""
        sb = mypytools.StyleBuilder()
        sb.fg(255, 0, 128)
        result = sb.apply('hello', finish=True)
        assert result == f'{ESC}38;2;255;0;128mhello{ESC}39m'

    def test_fg_b8_only_needs_r(self):
        """Test `fg(200, b24=False)` works; b8 only needs `r`."""
        sb = mypytools.StyleBuilder()
        sb.fg(200, b24=False)
        assert any(
            c.startswith(str(mypytools.ANSIFormatter.Foreground.CUSTOM.value))
            for c in sb._codes
        )

    def test_fg_b8_with_g_or_b_raises(self):
        """Test `fg(200, 0, 0, b24=False)` raises, b8 only uses the `r` arg."""
        sb = mypytools.StyleBuilder()
        with raises(ValueError):
            sb.fg(200, 0, b24=False)
        with raises(ValueError):
            sb.fg(200, 0, 0, b24=False)

    def test_fg_returns_self(self):
        """Test `fg()` returns `self`."""
        sb = mypytools.StyleBuilder()
        assert sb.fg(255, 0, 0) is sb

    def test_bg_b24_missing_g_and_b_raises(self):
        """Test `bg(255)` raises `ValueError`, missing `g`, `b` arguments."""
        with raises(ValueError):
            mypytools.StyleBuilder().bg(255)

    def test_bg_b24_missing_b_raises(self):
        """Test `bg(255, 0)` raises `ValueError`, missing `b` argument."""
        with raises(ValueError):
            mypytools.StyleBuilder().bg(255, 0)

    def test_bg_b24_with_all_channels(self):
        """Test `bg(255, 0, 128)` contains style codes."""
        sb = mypytools.StyleBuilder()
        sb.bg(0, 128, 255)
        assert any(
            c.startswith(str(mypytools.ANSIFormatter.Background.CUSTOM.value))
            for c in sb._codes
        )

    def test_bg_b8_only_needs_r(self):
        """Test `bg(200, b24=False)` works; b8 only needs `r`."""
        sb = mypytools.StyleBuilder()
        sb.bg(100, b24=False)
        assert any(
            c.startswith(str(mypytools.ANSIFormatter.Background.CUSTOM.value))
            for c in sb._codes
        )

    def test_bg_b8_with_g_or_b_raises(self):
        """Test `bg(200, 0, 0, b24=False)` raises, b8 only uses the `r` arg."""
        sb = mypytools.StyleBuilder()
        with raises(ValueError):
            sb.bg(200, 0, b24=False)
        with raises(ValueError):
            sb.bg(200, 0, 0, b24=False)

    def test_bg_returns_self(self):
        """Test `bg()` returns `self`."""
        sb = mypytools.StyleBuilder()
        assert sb.bg(0, 0, 0) is sb


# ——{ mypytools.StyleBuilder.apply }———————————————————————————————————————————


class TestStyleBuilderApply:
    """Test ``StyleBuilder.apply()``."""

    def test_returns_self_when_not_finished(self):
        """Test ``apply`` returns *`self`* when not `finish` **==** `True`."""
        sb = mypytools.StyleBuilder()
        result = sb.bold().apply('hello')
        assert result is sb

    def test_returns_string_when_finished(self):
        """Test `apply` returns styled *`str`* when `finish` **==** `True`."""
        result = mypytools.StyleBuilder().bold().apply('hello', finish=True)
        assert isinstance(result, str)

    def test_clears_codes_after_apply(self):
        """Test `apply` clears `_codes` list after called if `clear_codes`."""
        sb = mypytools.StyleBuilder()
        sb.bold().apply('hello')
        assert sb._codes == []

    def test_keeps_codes_after_apply(self):
        """Test `apply` keeps `_codes` after called if not `clear_codes`."""
        sb = mypytools.StyleBuilder()
        sb.bold().apply('hello', clear_codes=False)
        assert sb._codes == ['1']

    def test_clears_formatted_on_finish(self):
        """Test `apply` clears `_formatted` list if `finish` **==** `True`."""
        sb = mypytools.StyleBuilder()
        sb.bold().apply('hello', finish=True)
        assert sb._formatted == []

    def test_empty_text_raises(self):
        """Test supplying no/falsy str to `apply` raises `ValueError`."""
        sb = mypytools.StyleBuilder()
        sb.bold()
        with raises(ValueError, match='non-empty'):
            sb.apply('')

    def test_no_style_raises(self):
        """Test `apply` raises `ValueError` if no style methods were called."""
        with raises(ValueError, match='style'):
            mypytools.StyleBuilder().apply('hello')

    def test_output_contains_text(self):
        """Test output from `apply` contains inputted text."""
        result = mypytools.StyleBuilder().bold().apply('hello', finish=True)
        assert 'hello' in result

    def test_output_is_escape_coded(self):
        """Test output from `apply` is ESC coded."""
        result = mypytools.StyleBuilder().bold().apply('hello', finish=True)
        assert ESC in result

    def test_list_text_contains_all_items(self):
        """Test `apply(['a', 'b', 'c'], finish=True) contains `a`, `b`, `c`."""
        sb = mypytools.StyleBuilder()
        sb.bold()
        result = sb.apply(['a', 'b', 'c'], finish=True)
        assert f'{ESC}1m' in result
        assert f'{ESC}22m' in result
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_text_styled(self):
        """Test `apply('hello', style='1', finish=True)` styled correctly."""
        sb = mypytools.StyleBuilder()
        result = sb.apply('hello', style='1', finish=True)
        assert result == f'{ESC}1mhello{ESC}22m'

    def test_style_override_discards_pending_codes(self):
        """
        Test `apply(..., finish=True)' discards pending style codes.

        - Known design behavior — documented in `apply()` docstring
        """
        sb = mypytools.StyleBuilder()
        sb.bold()
        sb.apply('hello', style='3', finish=True)
        assert sb._codes == []

    def test_prepend(self):
        """Test `apply(..., prepend='>>> ', ...)` prepends the str."""
        sb = mypytools.StyleBuilder()
        result = sb.bold().apply('world', prepend='>>> ', finish=True)
        assert result.startswith('>>> ')

    def test_append(self):
        """Test `apply(..., append=' <<<', ...)` appends the str."""
        sb = mypytools.StyleBuilder()
        result = sb.bold().apply('hello', append=' <<<', finish=True)
        assert result.endswith(' <<<')

    def test_falls_back_to_full_reset_for_unknown_codes(self):
        """
        Test `StyleBuilder().reset().apply(...)` defaults to full reset code.

        reset() pushes RESET ("0"); _compute_reset_codes returns '' for it,
        so apply() must fall back to str(mypytools.ANSIFormatter.RESET).
        """
        result = mypytools.StyleBuilder().reset().apply('hello', finish=True)
        assert f'{ESC}0m' in result

    def test_builder_reusable_after_finish(self):
        """Test `StyleBuilder` is reusable after `apply(..., finish=True)`."""
        sb = mypytools.StyleBuilder()
        first = sb.bold().apply('first', finish=True)
        second = sb.italic().apply('second', finish=True)
        assert first == f'{ESC}1mfirst{ESC}22m'
        assert second == f'{ESC}3msecond{ESC}23m'

    def test_codes_reusable_after_finish_if_not_apply_clear_codes(self):
        """
        Test `StyleBuilder` codes from the first apply add to the second.

        - Only applicaple if `StyleBulider()...apply(..., clear_codes=False)`
        """
        sb = mypytools.StyleBuilder()
        first = sb.bold().apply('first', finish=True, clear_codes=False)
        second = sb.italic().apply('second', finish=True)
        assert first == f'{ESC}1mfirst{ESC}22m'
        assert second == f'{ESC}1;3msecond{ESC}22;23m'

    def test_chaining_multiple_segments(self):
        """Test `StyleBuilder` double `apply()` chaining."""
        result = (
            mypytools.StyleBuilder()
            .bold()
            .apply('Error: ')
            .italic()
            .apply('something went wrong', finish=True)
        )
        assert result.startswith(f'{ESC}1mError: {ESC}22m')
        assert result.endswith(f'{ESC}3msomething went wrong{ESC}23m')

    def test_sep_between_list_items(self):
        """Test `apply`'s `sep` argument is between each `text` list entry."""
        result = (
            mypytools.StyleBuilder()
            .bold()
            .apply(
                ['a', 'b', 'c'],
                sep=' | ',
                sep_end=False,
                finish=True,
            )
        )
        bold = f'{ESC}1m'
        reset_bold = f'{ESC}22m'

        def style_bold(string: str):
            return f'{bold}{string}{reset_bold}'

        assert result == (
            f'{style_bold("a")} | {style_bold("b")} | {style_bold("c")}'
        )

    def test_processed_sep(self):
        """Test `apply`'s `processed_sep` argument seperates styled strings."""
        result = (
            mypytools.StyleBuilder()
            .bold()
            .apply('hello')
            .italic()
            .apply('world', finish=True, processed_sep='\n')
        )
        assert result == f'{ESC}1mhello{ESC}22m\n{ESC}3mworld{ESC}23m'


# ——{ mypytools.StyleBuilder.add }—————————————————————————————————————————————


class TestStyleBuilderAdd:
    """Test ``StyleBuilder.add()``."""

    def test_returns_self_when_not_finished(self):
        """Test `add` returns *`self`* when not `finish` **==** `True`."""
        sb = mypytools.StyleBuilder()
        result = sb.add('hello')
        assert result is sb

    def test_returns_string_when_finished(self):
        """Test `add` returns *`str`* when `finish` **==** `True`."""
        result = mypytools.StyleBuilder().add('hello', finish=True)
        assert isinstance(result, str)

    def test_clears_formatted_on_finish(self):
        """Test `add` clears `_formatted` list when `finish` **==** `True`."""
        sb = mypytools.StyleBuilder()
        sb.add('hello', finish=True)
        assert sb._formatted == []

    def test_pending_codes_raises(self):
        """Test `add` raises `ValueError` if `StyleBuilder` pending codes."""
        sb = mypytools.StyleBuilder()
        sb.bold()
        with raises(ValueError, match='Pending style codes'):
            sb.add('hello')

    def test_sep_joins_args(self):
        """Test `add`'s `sep` argument used to join each `raw_text` entry."""
        result = mypytools.StyleBuilder().add(
            'hello', 'world', sep='-', finish=True
        )
        assert result == 'hello-world'

    def test_end_sep_appended(self):
        """Test `add`'s `end_sep` argument appended to `raw_text` entry."""
        result = mypytools.StyleBuilder().add('hello', end_sep='!', finish=True)
        assert result == 'hello!'

    def test_add_and_apply_together(self):
        """Test `add` and `apply` chained together within `StyleBuilder`."""
        result = (
            mypytools.StyleBuilder()
            .bold()
            .apply('styled ')
            .add('plain', finish=True)
        )
        assert result == f'{ESC}1mstyled {ESC}22mplain'


# ——{ mypytools.bubble }———————————————————————————————————————————————————————


class TestBubble:
    """Test ansi_tools ``bubble()`` function."""

    @fixture
    def default_args(self):
        """Provide standard minimum arguments for the ``bubble`` function."""
        return {'expected': 'x', 'at': 'myfunc', 'lvalue': 'a', 'rvalue': 'b'}

    def test_returns_string(self, default_args):
        """Test ``bubble(...)`` returns a string."""
        result = mypytools.bubble(**default_args)
        assert isinstance(result, str)

    def test_contains_expected_marker(self, default_args):
        """Test ``bubble(...)`` contains the **'Expected'** marker."""
        result = mypytools.bubble(**default_args)
        assert f'Expected {ESC}38;2;55;65;81m\ue0b6{ESC}0m' in result

    def test_contains_expected_value(self, default_args):
        """Test ``bubble(expected='x', ...)`` contains the **'x'** str."""
        result = mypytools.bubble(**default_args)
        assert f'{ESC}38;2;248;250;252;48;2;55;65;81mx{ESC}0m' in result

    def test_contains_expected_right_pill_cap(self, default_args):
        """Test ``bubble(expected='x', ...)`` contains the right pill cap."""
        result = mypytools.bubble(**default_args)
        assert f'81mx{ESC}0m{ESC}38;2;55;65;81m\ue0b4{ESC}0m' in result

    def test_contains_at_marker(self, default_args):
        """Test ``bubble(...)`` contains the **'@—>'** marker."""
        result = mypytools.bubble(**default_args)
        assert f'@—> {ESC}38;2;55;65;81m\ue0b6{ESC}0m' in result

    def test_contains_at_value(self, default_args):
        """Test ``bubble(at='myfunc', ...)`` contains the **'myfunc'** str."""
        result = mypytools.bubble(**default_args)
        assert f'{ESC}3;38;2;248;175;195;48;2;55;65;81mmyfunc{ESC}0m' in result

    def test_contains_at_right_pill_cap(self, default_args):
        """Test ``bubble(at='myfunc', ...)`` contains the right pill cap."""
        result = mypytools.bubble(**default_args)
        assert f'mmyfunc{ESC}0m{ESC}38;2;55;65;81m\ue0b4{ESC}0m' in result

    def test_contains_why_marker(self, default_args):
        """Test ``bubble(...)`` contains the **'?—>'** marker."""
        result = mypytools.bubble(**default_args)
        assert '?—>' in result

    def test_contains_lvalue_and_rvalue(self, default_args):
        """Test ``bubble(lvalue='a', rvalue='b', ...)`` has 'a' and 'b'."""
        result = mypytools.bubble(**default_args)
        assert f'{ESC}3;4;38;2;248;250;252;48;2;55;65;81ma{ESC}0m' in result
        assert f'{ESC}3;4;38;2;248;250;252;48;2;55;65;81mb{ESC}0m' in result

    def test_contains_comparison_value(self, default_args):
        """Test ``bubble(...)`` contains the **'=='** default `compare` str."""
        result = mypytools.bubble(**default_args)
        assert f'{ESC}38;2;148;163;184;48;2;55;65;81m == {ESC}0m' in result

    def test_custom_compare(self, default_args):
        """Test ``bubble(compare='!=', ...)`` contains the **'!='** str."""
        default_args['compare'] = '!='
        result = mypytools.bubble(**default_args)
        assert f'{ESC}38;2;148;163;184;48;2;55;65;81m != {ESC}0m' in result

    def test_list_of_expected(self):
        """
        Test ``bubble(expected=['x', 'y', 'z'], ...)``.

        - Check if result is an instance of a ``str``
        - Check if result contains the ``Expected`` marker
        - Check if result contains 'x', 'y', and 'z' pills
        """
        expected = ['x', 'y', 'z']
        result = mypytools.bubble(
            expected=expected, at='fn', lvalue='a', rvalue='b'
        )
        assert isinstance(result, str)
        for val in expected:
            assert (
                f'{ESC}38;2;55;65;81m\ue0b6{ESC}0m'
                f'{ESC}38;2;248;250;252;48;2;55;65;81m{val}{ESC}0m'
                f'{ESC}38;2;55;65;81m\ue0b4{ESC}0m'
            ) in result

    def test_prepend_why(self, default_args):
        """Test `bubble(..., prepend_why='keyword-argument')` prepends str."""
        default_args['prepend_why'] = 'keyword-argument'
        result = mypytools.bubble(**default_args)
        assert '?—> keyword-argument ' in result

    def test_append_why(self, default_args):
        """Test ``bubble(..., append_why='— extra info')`` appends str."""
        default_args['append_why'] = '— extra info'
        result = mypytools.bubble(**default_args)
        assert ' — extra info' in result
