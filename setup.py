import os
from subprocess import call
from setuptools import setup, find_packages
import sys

PACKAGE_NAME = 'sci'

VERSION = '0.1.0'


def compile_line():
    compile_command = ("g++ LINE/line.cpp -o LINE/line"
                       "-lgsl -lgslcblas -lpthread")
    return_code = call(compile_command.split())
    if return_code != 0:
        sys.exit(("LINE compilation has failed."
                  "Please make sure to install GSL library"))

compile_line()

setup(

    name="sci",
    version=0.1,
    author='Haitham Ashoor',
    author_email='haitham.ashoor@jax.org',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'tqdm'
    ],

    classifiers=(
        "Programming Language :: Python :: 2",
    ),
    zip_safe=False,
    )
