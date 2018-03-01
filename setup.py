from distutils.core import setup

import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Lundy',
    version='0.1dev',
    packages=['lundy',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description="Test",
    install_requires=required
)