import sys
from traceback import extract_tb
from types import TracebackType
from logging import DEBUG, Logger, getLogger, FileHandler, Formatter
from pathlib import Path
from mytools.ansi_tools.formatter import StyleBuilder
from inspect import stack, getmodule


def get_logger(
	log_path: Path | None = None, level: int = DEBUG, name: str | None = None
) -> Logger:
	frame = stack()[1]
	module = getmodule(frame[0])
	name = module.__name__ if module else '__main__'

	log_path = log_path or Path.cwd() / f'{name}.log'
	logger = getLogger(name)
	logger.setLevel(level)

	if not logger.handlers:
		handler = FileHandler(log_path, mode='w', encoding='UTF-8')
		handler.setFormatter(
			Formatter(
				fmt='%(asctime)s @--> %(filename)s %(lineno)d %(funcName)s !--> [%(levelname)s] %(message)s',
				datefmt=r'%m-%d-%Y %H.%M.%S',
			)
		)
		logger.addHandler(handler)

	return logger


def setup_hooks() -> None:
	"""Call this in your project to install the custom excepthook."""

	# --{ Exception-Hook }---------
	def custom_excepthook(
		exc_type: type[BaseException],
		exc_value: BaseException,
		exc_tb: TracebackType | None,
	) -> None:
		# -- Header --
		header = (
			StyleBuilder()
			.bold()
			.fg(255, 80, 80)
			.apply(f' {exc_type.__name__} ', finish=True)
		)
		print(f'\n{header}')

		# -- Message --
		exc_msg = str(exc_value)
		if not StyleBuilder.ANSI_ESCAPE_RE.search(exc_msg):
			exc_msg = (
				StyleBuilder().fg(255, 160, 160).apply(exc_msg, finish=True)
			)
		print(f'{exc_msg}\n')

		# -- Traceback frames --
		frames = extract_tb(exc_tb)
		print(
			StyleBuilder()
			.bold()
			.fg(180, 180, 180)
			.apply('Traceback:', finish=True)
		)

		for i, frame in enumerate(frames):
			is_last = i == len(frames) - 1

			path = Path(frame.filename)
			folder = (
				StyleBuilder()
				.dim()
				.fg(120, 120, 120)
				.apply(str(path.parent) + '\\', finish=True)
			)
			file = (
				StyleBuilder()
				.bold()
				.fg(200, 200, 255)
				.apply(path.name, finish=True)
			)

			lineno = (
				StyleBuilder()
				.fg(255, 220, 97)
				.apply(f'line {frame.lineno}', finish=True)
			)

			fn_color = (255, 100, 100) if is_last else (255, 175, 1)
			func = (
				StyleBuilder()
				.italic()
				.fg(*fn_color)
				.apply(frame.name, finish=True)
			)

			prefix = '  └─' if is_last else '  ├─'
			print(f'{prefix} {folder}{file}  {lineno}  in {func}')

			if frame.line:
				src = (
					StyleBuilder()
					.dim()
					.fg(180, 180, 180)
					.apply(f'       {frame.line.strip()}', finish=True)
				)
				print(src)
		print()

	sys.excepthook = custom_excepthook
