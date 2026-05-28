"""Add C extension modules."""

from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            'mypytools.flattener._list',
            sources=['./src/mypytools/flattener/_list.c'],
        )
    ]
)
