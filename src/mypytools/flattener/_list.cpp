// """
// * :func:`to_list` — accepts any mix of scalars, iterables, and
//          mappings and collapses them into a flat ``list``.
//
// Fine-grained flags on :func:`to_list` control how deeply nested
// structures are unwrapped and how dictionaries are treated. An
// optional ``cast_to`` parameter on both functions narrows the
// return type at the type-checker level without runtime overhead.
//
// Examples:
// ```
//     from mypytools import filter_none, to_list
//
//     # Flatten nested iterables
//     to_list([1, 2], (3, 4), 5)       # [1, 2, 3, 4, 5]
//
//     # Keep only one level of nesting
//     to_list(
//         [[1, 2], [3, 4]], unwrap_layers=1,
//     )  # [[1, 2], [3, 4]]
//
//     # Filter None values from multiple lists
//     a, b = filter_none([1, None, 2], [None, 3])
//     # ([1, 2], [3])
//
//     # Replace None instead of removing it
//     filter_none([1, None, 2], replace=0, combine=True)
//     # [1, 0, 2]
// ```
//
// Note:
//     * ``unwrap_layers=0`` is explicitly prohibited and raises
//       :exc:`ValueError`.
//     * Type narrowing via ``cast_to`` is a static-analysis
//       convenience; no runtime conversion of individual items is
//       performed.
// """

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// ---------------------------------------------------------------------------
// Forward declaration
// ---------------------------------------------------------------------------
static void unwrap_entry(
    py::handle    entry,
    py::list&     out,
    int           depth,
    bool          include_none,
    bool          dict_keys,
    bool          dict_vals,
    bool          preserve_tuples);

// ---------------------------------------------------------------------------
// unwrap_entry — recursive workhorse
// ---------------------------------------------------------------------------
static void unwrap_entry(
    py::handle entry,
    py::list&  out,
    int        depth,
    bool       include_none,
    bool       dict_keys,
    bool       dict_vals,
    bool       preserve_tuples)
{
    if (py::isinstance<py::str>(entry)) {
        if (include_none || !entry.is_none())
            out.append(entry);
        return;
    }

    if (py::isinstance<py::dict>(entry)) {
        if (depth == 0 || (!dict_keys && !dict_vals)) {
            out.append(entry);
            return;
        }

        auto d = entry.cast<py::dict>();
        bool is_items = dict_keys && dict_vals;
        int  next_depth = (depth == -1) ? -1 : depth - 1;

        if (is_items) {
            for (auto kv : d) {
                if (preserve_tuples) {
                    out.append(py::make_tuple(kv.first, kv.second));
                } else {
                    unwrap_entry(kv.first,  out, next_depth, include_none,
                                 dict_keys, dict_vals, preserve_tuples);
                    unwrap_entry(kv.second, out, next_depth, include_none,
                                 dict_keys, dict_vals, preserve_tuples);
                }
            }
        } else if (dict_keys) {
            for (auto kv : d)
                unwrap_entry(kv.first, out, next_depth, include_none,
                             dict_keys, dict_vals, preserve_tuples);
        } else {
            for (auto kv : d)
                unwrap_entry(kv.second, out, next_depth, include_none,
                             dict_keys, dict_vals, preserve_tuples);
        }
        return;
    }

    py::object iter;
    try {
        iter = py::iter(entry);
    } catch (py::error_already_set&) {
        PyErr_Clear();
        if (include_none || !entry.is_none())
            out.append(entry);
        return;
    }

    if (depth == 0) {
        out.append(entry);
        return;
    }

    int next_depth = (depth == -1) ? -1 : depth - 1;
    for (py::handle item : iter) {
        if (include_none || !item.is_none())
            unwrap_entry(item, out, next_depth, include_none,
                         dict_keys, dict_vals, preserve_tuples);
    }
}

// ---------------------------------------------------------------------------
// to_list — public pybind11 binding
// ---------------------------------------------------------------------------
static py::list to_list(
    py::args     entries,
    bool         include_none         = false,
    int          unwrap_layers        = -1,
    bool         unwrap_dict_keys     = true,
    bool         unwrap_dict_vals     = false,
    bool         preserve_dict_tuples = true,
    py::object   cast_to              = py::none())
{
    if (unwrap_layers < -1 || unwrap_layers == 0)
        throw py::value_error(
            "unwrap_layers must be -1 (infinite) or a positive integer >= 1.");

    py::list out;
    for (py::handle entry : entries) {
        if (!include_none && entry.is_none())
            continue;
        unwrap_entry(entry, out, unwrap_layers, include_none,
                     unwrap_dict_keys, unwrap_dict_vals, preserve_dict_tuples);
    }
    return out;
}

// ---------------------------------------------------------------------------
// Module definition
// ---------------------------------------------------------------------------
PYBIND11_MODULE(_list, m)
{
    m.def(
        "to_list",
        &to_list,
        py::arg("include_none")         = false,
        py::arg("unwrap_layers")        = -1,
        py::arg("unwrap_dict_keys")     = true,
        py::arg("unwrap_dict_vals")     = false,
        py::arg("preserve_dict_tuples") = true,
        py::arg("cast_to")              = py::none(),
        R"doc(
Flatten a composite of iterables and scalars into a list.

Args:
    *entries (Any): Values to flatten. Each may be a scalar,
        a string, an iterable, or a mapping.
    include_none (bool): When ``True``, ``None`` is kept as
        a valid list value. Defaults to ``False``.
    unwrap_layers (int): Depth limit for unwrapping nested
        iterables. ``-1`` unwraps fully; positive integers
        stop at that depth. Defaults to ``-1``.
    unwrap_dict_keys (bool): Include dictionary keys when
        unwrapping a mapping. Defaults to ``True``.
    unwrap_dict_vals (bool): Include dictionary values when
        unwrapping a mapping. Defaults to ``False``.
    preserve_dict_tuples (bool): When both
        ``unwrap_dict_keys`` and ``unwrap_dict_vals`` are
        ``True``, keeps each key-value pair as an intact
        ``(key, value)`` tuple. Defaults to ``True``.
    cast_to (type | None): Static-analysis convenience only;
        no runtime conversion of individual items is
        performed. Defaults to ``None``.

Returns:
    list: Flattened results.

Raises:
    ValueError: If ``unwrap_layers`` is less than ``-1`` or
        equal to ``0``.
)doc");
}
