"""Lets pybind11 inject itself into C++ extension modules."""
# Third party imports
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        'mypytools.flattener._list',
        sources=['src/mypytools/flattener/_list.cpp'],
        cxx_std=17,
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
