from typing import Any, cast, TypeVar, overload
from collections.abc import Iterable

TC = TypeVar('TC')


@overload
def to_list(
	*entries: Any,
	include_none: bool = False,
	unwrap_layers: int = -1,
	unwrap_dict_keys: bool = True,
	unwrap_dict_vals: bool = False,
	preserve_dict_tuples: bool = True,
	cast_to: type[TC],
) -> list[TC]: ...


ET = TypeVar('ET')


@overload
def to_list(
	*entries: ET,
	include_none: bool = False,
	unwrap_layers: int = -1,
	unwrap_dict_keys: bool = True,
	unwrap_dict_vals: bool = False,
	preserve_dict_tuples: bool = True,
	cast_to: None = None,
) -> list[ET]: ...


def to_list(
	*entries: Any,
	include_none: bool = False,
	unwrap_layers: int = -1,
	unwrap_dict_keys: bool = True,
	unwrap_dict_vals: bool = False,
	preserve_dict_tuples: bool = True,
	cast_to: type[TC] | None = None,
) -> list[Any]:
	"""
	Flattens a tuple composite of Iterable[Any] and/or Any types into a list.
	- Strings are treated as scalar T's, not iterated.
	- Providing `0` to `unwrap_layers` raises a ValueError.

	:param tuple[Any, ...] entries:
	    A comma separated list of varying types of values you wish to flatten
	    into a list.
	:param bool include_none:
	    ``None`` is considered a valid list value if True.
	:param int unwrap_layers:
	    The number of layers you wish to unwrap each entry that was passed in.
	    Providing `-1` unwraps everything into a flat list of values, providing
	    `0` results in a raised `ValueError`.
	:param bool unwrap_dict_keys:
	    Unwraps dictionary keys if True.
	:param bool unwrap_dict_vals:
	    Unwraps dictionary values if True.
	:param bool preserve_dict_tuples:
	    Only applies when both unwrap_dict_keys and unwrap_dict_vals are True.
	    If True, each key-value pair is kept as an intact (key, value) tuple.
	    If False, the tuples are further unwrapped into a flat sequence of
	    alternating keys and values.
	:param type[TC] | None cast_to:
	    If provided, the result is cast to `list[TC]` without runtime
	    conversion of individual items.

	:raises ValueError: If `unwrap_layers` is less than -1 or equal to 0.

	:returns:
	    - ``list[TC]`` if ``cast_to`` is provided ─ entries are flattened and
	    cast to ``list[TC]``.

	    - ``list[ET]`` if all entries share the same type ─ inferred from the
	    input.

	    - ``list[Any]`` otherwise.
	:rtype: list

	.. versionadded:: 0.1.0
	"""

	if unwrap_layers < -1 or unwrap_layers == 0:
		raise ValueError(
			'unwrap_layers must be -1 (infinite) or a positive integer >= 1.'
		)

	def unwrap(entry: Any, depth: int) -> Iterable[Any]:
		"""
		Ensures the given entry is returned as an iterable.
		Strings are treated as plain values despite being iterable, and will
		be wrapped rather than iterated character by character.

		:param Any entry: A single value or an existing iterable to unwrap.
		:param int depth: The number of unwraps to perform on the entry.

		:returns:
		    The original iterable, or the value wrapped in a single-item list.
		:rtype: Iterable[Any]

		Example::

		    # Primitives — wrapped in a list
		    unwrap(6)  # [6]
		    unwrap(42.0)  # [42.0]
		    unwrap(True)  # [True]
		    unwrap(None)  # [None]

		    # Strings — wrapped, not iterated
		    unwrap('hello')  # ["hello"]

		    # Collections — flat iterables unwrap to a list of their items
		    unwrap([1, 2, 3])  # [1, 2, 3]
		    unwrap((1, 2, 3))  # [1, 2, 3]
		    unwrap({1, 2, 3})  # [1, 2, 3]

		    # Dictionaries — behavior depends on outer unwrap_dict_keys / unwrap_dict_vals flags
		    # unwrap_dict_keys=True, unwrap_dict_vals=False (default):
		    unwrap(
		        {'a': 1, 'b': 2}
		    )  # ['a', 'b']

		    # unwrap_dict_keys=False, unwrap_dict_vals=True:
		    unwrap({'a': 1, 'b': 2})  # [1, 2]

		    # unwrap_dict_keys=True, unwrap_dict_vals=True, preserve_dict_tuples=True (default):
		    unwrap(
		        {'a': 1, 'b': 2}
		    )  # [('a', 1), ('b', 2)]

		    # unwrap_dict_keys=True, unwrap_dict_vals=True, preserve_dict_tuples=False:
		    unwrap(
		        {'a': 1, 'b': 2}
		    )  # ['a', 1, 'b', 2]

		    # unwrap_dict_keys=False, unwrap_dict_vals=False:
		    unwrap(
		        {'a': 1, 'b': 2}
		    )  # [{'a': 1, 'b': 2}]

		    # Nested structures — behavior depends on the outer unwrap_layers flag
		    # unwrap_layers=-1 (default, fully unwrapped):
		    unwrap(
		        [[[1, 2], [3, 4]]]
		    )  # [1, 2, 3, 4]

		    # unwrap_layers=1:
		    unwrap(
		        [[[1, 2], [3, 4]]]
		    )  # [[[1, 2], [3, 4]]]

		    # unwrap_layers=2:
		    unwrap(
		        [[[1, 2], [3, 4]]]
		    )  # [[1, 2], [3, 4]]

		    # unwrap_layers=3:
		    unwrap(
		        [[[1, 2], [3, 4]]]
		    )  # [1, 2, 3, 4]

		    # Complex single values — wrapped in a list
		    unwrap(
		        RGB(255, 0, 0)
		    )  # [RGB(255, 0, 0)]

		.. versionadded:: 0.1.0
		"""

		# Base Case 1: Entry is a scalar type or str
		if not isinstance(entry, Iterable) or isinstance(entry, str):
			return [entry]

		# Base Case 2: Entry is a dict
		elif isinstance(entry, dict):
			if depth == 0 or (not unwrap_dict_vals and not unwrap_dict_keys):
				return [entry]

			is_items = unwrap_dict_keys and unwrap_dict_vals
			if is_items:
				target_iterable = entry.items()
			elif unwrap_dict_keys:
				target_iterable = entry.keys()
			else:
				target_iterable = entry.values()

			flattened = []
			next_depth = depth if depth == -1 else depth - 1
			for item in target_iterable:
				if is_items and preserve_dict_tuples:
					flattened.append(item)
				else:
					flattened.extend(unwrap(item, next_depth))
			return flattened

		# Base Case 3: Reached users requested depth
		elif depth == 0:
			return [entry]

		# Recursive Step: Unwrap entries
		flattened = []
		next_depth = depth if depth == -1 else depth - 1
		for item in entry:
			flattened.extend(unwrap(item, next_depth))
		return flattened

	def keep(val: Any) -> bool:
		return include_none or val is not None

	flat_result = [
		item
		for entry in entries
		if keep(entry)
		for item in unwrap(entry, unwrap_layers)
		if keep(item)
	]

	if not flat_result:
		return flat_result
	elif cast_to is not None:
		return cast(list[TC], flat_result)

	first_type = type(flat_result[0])
	all_same_type = all(type(item) is first_type for item in flat_result)

	if all_same_type:
		return cast(Any, flat_result)

	return flat_result
