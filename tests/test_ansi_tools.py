"""Tests for src/mytools/ansi_tools/formatter.py"""

# Third party imports
import pytest

# Relative imports
from mytools.ansi_tools import ANSIFormatter, StyleBuilder, bubble

ESC = '\x1b['


#——{ ANSIFormatter.escape }————————————————————————————————————————————————————

class TestANSIFormatterESCAPE:

	def test_wraps_string_with_style(self):
		result = ANSIFormatter.escape('1', 'hello')
		assert result == f'{ESC}1mhello{ESC}0m'

	def test_uses_full_reset_by_default(self):
		result = ANSIFormatter.escape('3', 'hi')
		assert result.endswith(f'{ESC}0m')

	def test_uses_custom_reset(self):
		result = ANSIFormatter.escape('3', 'hi', reset='23')
		assert result.endswith(f'{ESC}23m')

	def test_int_style_code(self):
		result = ANSIFormatter.escape(1, 'bold')
		assert result == f'{ESC}1mbold{ESC}0m'

	def test_compound_style_code(self):
		result = ANSIFormatter.escape('1;3', 'text')
		assert result == f'{ESC}1;3mtext{ESC}0m'


#——{ ANSIFormatter constants }—————————————————————————————————————————————————

class TestANSIFormatterConstants:

	def test_reset(self):
		assert ANSIFormatter.RESET == 0

	def test_reset_intensity(self):
		assert ANSIFormatter.RESET_INTENSITY == 22

	def test_b8_color(self):
		assert ANSIFormatter.B8_COLOR == 5

	def test_b24_color(self):
		assert ANSIFormatter.B24_COLOR == 2


#——{ ANSIFormatter.Emphasis }——————————————————————————————————————————————————

class TestEmphasis:

	def test_bold(self):
		assert ANSIFormatter.Emphasis.BOLD == 1

	def test_italic(self):
		assert ANSIFormatter.Emphasis.ITALIC == 3

	def test_underline(self):
		assert ANSIFormatter.Emphasis.UNDERLINE == 4

	def test_strikethrough(self):
		assert ANSIFormatter.Emphasis.STRIKETHROUGH == 9

	def test_double_underline(self):
		assert ANSIFormatter.Emphasis.DOUBLE_UNDERLINE == 21

	def test_reset_italic(self):
		assert ANSIFormatter.Emphasis.reset['RESET_ITALIC'] == 23

	def test_reset_underline(self):
		assert ANSIFormatter.Emphasis.reset['RESET_UNDERLINE'] == 24

	def test_reset_strikethrough(self):
		assert ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH'] == 29


#——{ ANSIFormatter.Effects }———————————————————————————————————————————————————

class TestEffects:

	def test_dim(self):
		assert ANSIFormatter.Effects.DIM == 2

	def test_slow_blink(self):
		assert ANSIFormatter.Effects.SLOW_BLINK == 5

	def test_rapid_blink(self):
		assert ANSIFormatter.Effects.RAPID_BLINK == 6

	def test_bg_fg_swap(self):
		assert ANSIFormatter.Effects.BG_FG_SWAP == 7

	def test_hide(self):
		assert ANSIFormatter.Effects.HIDE == 8

	def test_reset_blink(self):
		assert ANSIFormatter.Effects.reset['RESET_BLINK'] == 25

	def test_bg_fg_unswap(self):
		assert ANSIFormatter.Effects.reset['BG_FG_UNSWAP'] == 27

	def test_show(self):
		assert ANSIFormatter.Effects.reset['SHOW'] == 28


#——{ ANSIFormatter.Foreground / Background }———————————————————————————————————

class TestForeground:

	def test_black(self):
		assert ANSIFormatter.Foreground.BLACK.value == 30

	def test_custom(self):
		assert ANSIFormatter.Foreground.CUSTOM.value == 38

	def test_default(self):
		assert ANSIFormatter.Foreground.DEFAULT.value == 39


class TestBackground:

	def test_black(self):
		assert ANSIFormatter.Background.BLACK.value == 40

	def test_custom(self):
		assert ANSIFormatter.Background.CUSTOM.value == 48

	def test_default(self):
		assert ANSIFormatter.Background.DEFAULT.value == 49


#——{ bubble }——————————————————————————————————————————————————————————————————

class TestBubble:

	def test_returns_string(self):
		result = bubble(expected='x', at='fn', lvalue='a', rvalue='b')
		assert isinstance(result, str)

	def test_contains_expected_marker(self):
		result = bubble(expected='x', at='fn', lvalue='a', rvalue='b')
		assert 'Expected' in result

	def test_contains_at_value(self):
		result = bubble(expected='x', at='myfunc', lvalue='a', rvalue='b')
		assert 'myfunc' in result

	def test_contains_lvalue_and_rvalue(self):
		result = bubble(expected='x', at='fn', lvalue='myarg', rvalue='True')
		assert 'myarg' in result
		assert 'True' in result

	def test_list_of_expected(self):
		result = bubble(expected=['x', 'y', 'z'], at='fn', lvalue='a', rvalue='b')
		assert isinstance(result, str)
		assert 'Expected' in result

	def test_prepend_why(self):
		result = bubble(
			expected='x', at='fn', lvalue='a', rvalue='b',
			prepend_why=' keyword-argument',
		)
		assert 'keyword-argument' in result

	def test_append_why(self):
		result = bubble(
			expected='x', at='fn', lvalue='a', rvalue='b',
			append_why=' — extra info',
		)
		assert 'extra info' in result

	def test_custom_compare(self):
		result = bubble(expected='x', at='fn', lvalue='a', rvalue='b', compare='!=')
		assert '!=' in result


#——{ StyleBuilder._compute_reset_codes }———————————————————————————————————————

class TestComputeResetCodes:

	def test_bold_returns_reset_intensity(self):
		codes = [str(ANSIFormatter.Emphasis.BOLD)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.RESET_INTENSITY) in result.split(';')

	def test_dim_returns_reset_intensity(self):
		codes = [str(ANSIFormatter.Effects.DIM)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.RESET_INTENSITY) in result.split(';')

	def test_italic_returns_reset_italic(self):
		codes = [str(ANSIFormatter.Emphasis.ITALIC)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']) in result.split(';')

	def test_underline_returns_reset_underline(self):
		codes = [str(ANSIFormatter.Emphasis.UNDERLINE)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Emphasis.reset['RESET_UNDERLINE']) in result.split(';')

	def test_strikethrough_returns_reset_strikethrough(self):
		codes = [str(ANSIFormatter.Emphasis.STRIKETHROUGH)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Emphasis.reset['RESET_STRIKETHROUGH']) in result.split(';')

	def test_slow_blink_returns_reset_blink(self):
		codes = [str(ANSIFormatter.Effects.SLOW_BLINK)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Effects.reset['RESET_BLINK']) in result.split(';')

	def test_rapid_blink_returns_reset_blink(self):
		codes = [str(ANSIFormatter.Effects.RAPID_BLINK)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Effects.reset['RESET_BLINK']) in result.split(';')

	def test_bg_fg_swap_returns_unswap(self):
		codes = [str(ANSIFormatter.Effects.BG_FG_SWAP)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Effects.reset['BG_FG_UNSWAP']) in result.split(';')

	def test_hide_returns_show(self):
		codes = [str(ANSIFormatter.Effects.HIDE)]
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Effects.reset['SHOW']) in result.split(';')

	def test_custom_fg_returns_fg_default(self):
		codes = [f'{ANSIFormatter.Foreground.CUSTOM.value};2;255;0;0']
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Foreground.DEFAULT.value) in result.split(';')

	def test_custom_bg_returns_bg_default(self):
		codes = [f'{ANSIFormatter.Background.CUSTOM.value};2;0;0;255']
		result = StyleBuilder._compute_reset_codes(codes)
		assert str(ANSIFormatter.Background.DEFAULT.value) in result.split(';')

	def test_unknown_codes_return_empty_string(self):
		result = StyleBuilder._compute_reset_codes(['99'])
		assert result == ''

	def test_empty_codes_return_empty_string(self):
		result = StyleBuilder._compute_reset_codes([])
		assert result == ''

	def test_multiple_codes_return_all_resets(self):
		codes = [str(ANSIFormatter.Emphasis.BOLD), str(ANSIFormatter.Emphasis.ITALIC)]
		result = StyleBuilder._compute_reset_codes(codes)
		parts = result.split(';')
		assert str(ANSIFormatter.RESET_INTENSITY) in parts
		assert str(ANSIFormatter.Emphasis.reset['RESET_ITALIC']) in parts


#——{ StyleBuilder.apply }——————————————————————————————————————————————————————

class TestStyleBuilderApply:

	def test_returns_self_when_not_finished(self):
		sb = StyleBuilder()
		result = sb.bold().apply('hello')
		assert result is sb

	def test_returns_string_when_finished(self):
		result = StyleBuilder().bold().apply('hello', finish=True)
		assert isinstance(result, str)

	def test_clears_codes_after_apply(self):
		sb = StyleBuilder()
		sb.bold().apply('hello')
		assert sb._codes == []

	def test_clears_formatted_on_finish(self):
		sb = StyleBuilder()
		sb.bold().apply('hello', finish=True)
		assert sb._formatted == []

	def test_empty_text_raises(self):
		sb = StyleBuilder()
		sb.bold()
		with pytest.raises(ValueError, match='non-empty'):
			sb.apply('')

	def test_no_style_raises(self):
		with pytest.raises(ValueError, match='style'):
			StyleBuilder().apply('hello')

	def test_output_contains_text(self):
		result = StyleBuilder().bold().apply('hello', finish=True)
		assert 'hello' in result

	def test_output_is_escape_coded(self):
		result = StyleBuilder().bold().apply('hello', finish=True)
		assert ESC in result

	def test_list_text_contains_all_items(self):
		result = StyleBuilder().bold().apply(['a', 'b', 'c'], finish=True)
		assert 'a' in result
		assert 'b' in result
		assert 'c' in result

	def test_style_override(self):
		result = StyleBuilder().apply('hello', style='1', finish=True)
		assert 'hello' in result
		assert ESC in result

	def test_style_override_discards_pending_codes(self):
		# Known design behaviour — documented in apply() docstring.
		sb = StyleBuilder()
		sb.bold()
		sb.apply('hello', style='3', finish=True)
		assert sb._codes == []

	def test_prepend(self):
		result = StyleBuilder().bold().apply('world', prepend='>>> ', finish=True)
		assert result.startswith('>>> ')

	def test_append(self):
		result = StyleBuilder().bold().apply('hello', append=' <<<', finish=True)
		assert result.endswith(' <<<')

	def test_falls_back_to_full_reset_for_unknown_codes(self):
		# reset() pushes RESET ("0"); _compute_reset_codes returns '' for it,
		# so apply() must fall back to str(ANSIFormatter.RESET).
		result = StyleBuilder().reset().apply('hello', finish=True)
		assert f'{ESC}0m' in result

	def test_builder_reusable_after_finish(self):
		sb = StyleBuilder()
		first = sb.bold().apply('first', finish=True)
		second = sb.italic().apply('second', finish=True)
		assert 'first' in first
		assert 'second' in second
		assert 'first' not in second

	def test_chaining_multiple_segments(self):
		result = (
			StyleBuilder()
			.bold()
			.apply('Error: ')
			.italic()
			.apply('something went wrong', finish=True)
		)
		assert 'Error: ' in result
		assert 'something went wrong' in result

	def test_sep_between_list_items(self):
		result = StyleBuilder().bold().apply(
			['a', 'b', 'c'], sep=' | ', sep_end=False, finish=True,
		)
		assert ' | ' in result

	def test_processed_sep(self):
		result = (
			StyleBuilder()
			.bold()
			.apply('hello')
			.italic()
			.apply('world', finish=True, processed_sep='\n')
		)
		assert '\n' in result


#——{ StyleBuilder.add }————————————————————————————————————————————————————————

class TestStyleBuilderAdd:

	def test_returns_self_when_not_finished(self):
		sb = StyleBuilder()
		result = sb.add('hello')
		assert result is sb

	def test_returns_string_when_finished(self):
		result = StyleBuilder().add('hello', finish=True)
		assert isinstance(result, str)
		assert 'hello' in result

	def test_clears_formatted_on_finish(self):
		sb = StyleBuilder()
		sb.add('hello', finish=True)
		assert sb._formatted == []

	def test_pending_codes_raises(self):
		sb = StyleBuilder()
		sb.bold()
		with pytest.raises(ValueError, match='Pending style codes'):
			sb.add('hello')

	def test_sep_joins_args(self):
		result = StyleBuilder().add('hello', 'world', sep='-', finish=True)
		assert 'hello-world' in result

	def test_end_sep_appended(self):
		result = StyleBuilder().add('hello', end_sep='!', finish=True)
		assert 'hello!' in result

	def test_add_and_apply_together(self):
		result = (
			StyleBuilder()
			.bold()
			.apply('styled ')
			.add('plain', finish=True)
		)
		assert 'plain' in result


#——{ StyleBuilder style methods }——————————————————————————————————————————————

class TestStyleBuilderStyleMethods:

	def test_bold_appends_code(self):
		sb = StyleBuilder()
		sb.bold()
		assert str(ANSIFormatter.Emphasis.BOLD) in sb._codes

	def test_italic_appends_code(self):
		sb = StyleBuilder()
		sb.italic()
		assert str(ANSIFormatter.Emphasis.ITALIC) in sb._codes

	def test_underline_appends_code(self):
		sb = StyleBuilder()
		sb.underline()
		assert str(ANSIFormatter.Emphasis.UNDERLINE) in sb._codes

	def test_strikethrough_appends_code(self):
		sb = StyleBuilder()
		sb.strikethrough()
		assert str(ANSIFormatter.Emphasis.STRIKETHROUGH) in sb._codes

	def test_double_underline_appends_code(self):
		sb = StyleBuilder()
		sb.double_underline()
		assert str(ANSIFormatter.Emphasis.DOUBLE_UNDERLINE) in sb._codes

	def test_dim_appends_code(self):
		sb = StyleBuilder()
		sb.dim()
		assert str(ANSIFormatter.Effects.DIM) in sb._codes

	def test_slow_blink_appends_code(self):
		sb = StyleBuilder()
		sb.slow_blink()
		assert str(ANSIFormatter.Effects.SLOW_BLINK) in sb._codes

	def test_fast_blink_appends_code(self):
		sb = StyleBuilder()
		sb.fast_blink()
		assert str(ANSIFormatter.Effects.RAPID_BLINK) in sb._codes

	def test_bg_fg_swap_appends_code(self):
		sb = StyleBuilder()
		sb.bg_fg_swap()
		assert str(ANSIFormatter.Effects.BG_FG_SWAP) in sb._codes

	def test_hide_appends_code(self):
		sb = StyleBuilder()
		sb.hide()
		assert str(ANSIFormatter.Effects.HIDE) in sb._codes

	def test_all_methods_return_self(self):
		sb = StyleBuilder()
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
		sb = StyleBuilder()
		sb.bold().italic()
		assert str(ANSIFormatter.Emphasis.BOLD) in sb._codes
		assert str(ANSIFormatter.Emphasis.ITALIC) in sb._codes


#——{ StyleBuilder.fg / bg }————————————————————————————————————————————————————

class TestStyleBuilderFgBg:

	def test_fg_b24_missing_g_and_b_raises(self):
		with pytest.raises(ValueError):
			StyleBuilder().fg(255)

	def test_fg_b24_missing_b_raises(self):
		with pytest.raises(ValueError):
			StyleBuilder().fg(255, 0)

	def test_fg_b24_with_all_channels(self):
		sb = StyleBuilder()
		sb.fg(255, 0, 128)
		assert any(c.startswith(str(ANSIFormatter.Foreground.CUSTOM.value)) for c in sb._codes)

	def test_fg_b8_only_needs_r(self):
		sb = StyleBuilder()
		sb.fg(200, b24=False)
		assert any(c.startswith(str(ANSIFormatter.Foreground.CUSTOM.value)) for c in sb._codes)

	def test_fg_returns_self(self):
		sb = StyleBuilder()
		assert sb.fg(255, 0, 0) is sb

	def test_bg_b24_missing_g_and_b_raises(self):
		with pytest.raises(ValueError):
			StyleBuilder().bg(255)

	def test_bg_b24_missing_b_raises(self):
		with pytest.raises(ValueError):
			StyleBuilder().bg(255, 0)

	def test_bg_b24_with_all_channels(self):
		sb = StyleBuilder()
		sb.bg(0, 128, 255)
		assert any(c.startswith(str(ANSIFormatter.Background.CUSTOM.value)) for c in sb._codes)

	def test_bg_b8_only_needs_r(self):
		sb = StyleBuilder()
		sb.bg(100, b24=False)
		assert any(c.startswith(str(ANSIFormatter.Background.CUSTOM.value)) for c in sb._codes)

	def test_bg_returns_self(self):
		sb = StyleBuilder()
		assert sb.bg(0, 0, 0) is sb