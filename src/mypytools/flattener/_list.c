// """
// * :func:`to_list` — accepts any mix of scalars, iterables, and
//          mappings and collapses them into a flat ``list``.

// Fine-grained flags on :func:`to_list` control how deeply nested
// structures are unwrapped and how dictionaries are treated. An
// optional ``cast_to`` parameter on both functions narrows the
// return type at the type-checker level without runtime overhead.

// Examples:
// ```
//     from mypytools import filter_none, to_list

//     # Flatten nested iterables
//     to_list([1, 2], (3, 4), 5)       # [1, 2, 3, 4, 5]

//     # Keep only one level of nesting
//     to_list(
//         [[1, 2], [3, 4]], unwrap_layers=1,
//     )  # [[1, 2], [3, 4]]

//     # Filter None values from multiple lists
//     a, b = filter_none([1, None, 2], [None, 3])
//     # ([1, 2], [3])

//     # Replace None instead of removing it
//     filter_none([1, None, 2], replace=0, combine=True)
//     # [1, 0, 2]
// ```

// Note:
//     * ``unwrap_layers=0`` is explicitly prohibited and raises
//       :exc:`ValueError`.
//     * Type narrowing via ``cast_to`` is a static-analysis
//       convenience; no runtime conversion of individual items is
//       performed.
// """

#define PY_SSIZE_T_CLEAN
#include <Python.h>

static int unwrap_entry(PyObject *entry, PyObject *out, int depth,
                        int include_none, int dict_keys, int dict_vals,
                        int preserve_tuples);

static PyObject *
to_list(PyObject *self, PyObject *const *args, Py_ssize_t nargs,
        PyObject *kwnames)
{
    static const char * const keywords[] = {
        "include_none", "unwrap_layers", "unwrap_dict_keys",
        "unwrap_dict_vals", "preserve_dict_tuples", "cast_to", NULL
    };

    int    include_none         = 0;
    int    unwrap_layers        = -1;
    int    unwrap_dict_keys     = 1;
    int    unwrap_dict_vals     = 0;
    int    preserve_dict_tuples = 1;
    PyObject *cast_to           = Py_None;

    PyObject *result = PyList_New(0);
    if (!result) return NULL;

    PyObject *args_tuple = PyTuple_New(0);
    if (!args_tuple) { Py_DECREF(result); return NULL; }

    PyObject *kwargs = kwnames ? PyDict_New() : NULL;
    if (kwnames) {
        for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(kwnames); i++) {
            PyDict_SetItem(kwargs,
                PyTuple_GET_ITEM(kwnames, i),
                args[nargs + i]);
        }
    }

    static char *kwlist[] = {
        "include_none", "unwrap_layers", "unwrap_dict_keys",
        "unwrap_dict_vals", "preserve_dict_tuples", "cast_to", NULL
    };
    int ok = PyArg_ParseTupleAndKeywords(
        args_tuple, kwargs, "|bibilO:to_list", kwlist,
        &include_none, &unwrap_layers, &unwrap_dict_keys,
        &unwrap_dict_vals, &preserve_dict_tuples, &cast_to);

    Py_DECREF(args_tuple);
    Py_XDECREF(kwargs);
    if (!ok) return NULL;

    if (unwrap_layers < -1 || unwrap_layers == 0) {
        PyErr_SetString(PyExc_ValueError,
            "unwrap_layers must be -1 (infinite) or a positive integer >= 1.");
        return NULL;
    }

    for (Py_ssize_t i = 0; i < nargs; i++) {
        PyObject *entry = args[i];

        if (!include_none && entry == Py_None)
            continue;

        if (unwrap_entry(entry, result, unwrap_layers,
                         include_none, unwrap_dict_keys,
                         unwrap_dict_vals, preserve_dict_tuples) < 0) {
            Py_DECREF(result);
            return NULL;
        }
    }

    return result;
}


static int
unwrap_entry(PyObject *entry, PyObject *out, int depth,
             int include_none, int dict_keys, int dict_vals,
             int preserve_tuples)
{
    // --- strings: scalar, never iterate
    if (PyUnicode_Check(entry))
        return include_none || entry != Py_None
               ? PyList_Append(out, entry) : 0;

    // --- dicts
    if (PyDict_Check(entry)) {
        if (depth == 0 || (!dict_keys && !dict_vals))
            return PyList_Append(out, entry);

        int is_items = dict_keys && dict_vals;
        PyObject *target = is_items  ? PyDict_Items(entry)
                         : dict_keys ? PyDict_Keys(entry)
                                     : PyDict_Values(entry);
        if (!target) return -1;

        int next_depth = (depth == -1) ? -1 : depth - 1;
        Py_ssize_t n = PyList_GET_SIZE(target);
        for (Py_ssize_t i = 0; i < n; i++) {
            PyObject *item = PyList_GET_ITEM(target, i);
            int ok;
            if (is_items && preserve_tuples) {
                ok = PyList_Append(out, item);
            } else {
                ok = unwrap_entry(item, out, next_depth, include_none,
                                  dict_keys, dict_vals, preserve_tuples);
            }
            if (ok < 0) { Py_DECREF(target); return -1; }
        }
        Py_DECREF(target);
        return 0;
    }

    // --- non-iterable scalars
    PyObject *iter = PyObject_GetIter(entry);
    if (!iter) {
        PyErr_Clear();
        return (include_none || entry != Py_None)
               ? PyList_Append(out, entry) : 0;
    }

    // --- depth limit reached: append as-is
    if (depth == 0) {
        Py_DECREF(iter);
        return PyList_Append(out, entry);
    }

    // --- recurse into iterable
    int next_depth = (depth == -1) ? -1 : depth - 1;
    PyObject *item;
    while ((item = PyIter_Next(iter))) {
        if (include_none || item != Py_None) {
            if (unwrap_entry(item, out, next_depth, include_none,
                             dict_keys, dict_vals, preserve_tuples) < 0) {
                Py_DECREF(item);
                Py_DECREF(iter);
                return -1;
            }
        }
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return PyErr_Occurred() ? -1 : 0;
}

static PyMethodDef _list_methods[] = {
    {
        "to_list",
        (PyCFunction)to_list,
        METH_FASTCALL | METH_KEYWORDS,
        "Flatten a composite of iterables and scalars into a list."
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _list_module = {
    PyModuleDef_HEAD_INIT,
    "_list",
    NULL,
    -1,
    _list_methods
};

PyMODINIT_FUNC
PyInit__list(void)
{
    return PyModule_Create(&_list_module);
}