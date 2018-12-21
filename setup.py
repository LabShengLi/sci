import os
from subprocess import call
from setuptools import setup
import sys

PACKAGE_NAME = 'sci'

VERSION = '0.1.0'

def compile_line():
	os.chdir("bin/LINE")
	compile_command = "g++ line.cpp -o line -lgsl -lgslcblas -lpthread"
	return_code = call(compile_command.split())
	if return_code != 0:
		sys.exit("LINE compilation has failed. Please make sure to install GSL library")



complie_line()

setup(

	name = "sci",
	version = 0.1,
	python_requires = '2.7',
	author = 'Haitham Ashoor',
	author_email = 'haitham.ashoor@jax.org',
	packages=['sci']
	install_requires= [
		'numpy',
		'scikit-learn',
		'tqdm'
	], 

	classifiers=(
        "Programming Language :: Python :: 2",
    ),
    zip_safe = False,



	)
