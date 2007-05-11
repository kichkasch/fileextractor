"""
Run
python setup.py install 

to compile the c-module and put it in the right place of the Python installation.
"""

from distutils.core import setup, Extension

module1 = Extension('spam',
                    sources = ['spammodule.c'])

setup (name = 'PackageName',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])

