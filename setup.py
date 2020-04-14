import os
from subprocess import call
from setuptools import setup, find_packages
import sys

PACKAGE_NAME = 'sci'

VERSION = '0.1.0'


CONDA_PATH =  os.getenv("CONDA_PREFIX")
INCPATH = os.path.join(CONDA_PATH,"include")
LIBPATH=os.path.join(CONDA_PATH,"lib")


LIBS="-lgsl -lgslcblas -lpthread -L{}".format(LIBPATH)

def compile_line():
    compile_command = ("g++ LINE/line.cpp -I{}  -o LINE/line {}".format(INCPATH,LIBS))
    return_code = call(compile_command.split())
    if return_code != 0:
        sys.exit(("LINE compilation has failed."
                  "Please make sure to install GSL library"))

compile_line()

## Important notes to requirements:
# 1. Last numpy release tosupport Python 2.7: see https://docs.scipy.org/doc/numpy/release.html#numpy-1-16-0-release-notes
# 2. The last SciPy version to do so is SciPy 1.2.x: https://www.scipy.org/scipylib/faq.html#do-numpy-and-scipytill-support-python-2-7 
# 3. Scikit-learn 0.20 was the last version to support Python 2.7 and Python 3.4. Scikit-learn now requires Python 3.5 or newer.
setup(

    name="sci",
    version=0.1,
    author='Haitham Ashoor',
    author_email='haitham.ashoor@jax.org',
    packages=find_packages(),
    install_requires=[
        'numpy<=1.16.0',
        'scipy<=1.2',
        'scikit-learn>=0.19,<=0.20',
        'tqdm'
    ],

    classifiers=(
        "Programming Language :: Python :: 2",
    ),
    zip_safe=False,
    )
