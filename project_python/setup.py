try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    

py_modules = [
    're',
    'numpy',
    'zipfile'
]

setup (name = 'Hanium_BraillePrinter',
       version = '0.1',
       description = 'Hanium_BraillePrinter',
       install_requires = py_modules)