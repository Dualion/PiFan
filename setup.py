#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys
import os

# Install
# python setup.py install --record files.txt

# Uninstall
# pip uninstall PiFan

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="PiFan",
    version="0.1.0",
    description="Software to control fan",
    author="Dualion",
    author_email="admin@dualion.com",
    url="http://dualion.com/",
    packages=['pifanpy'],
    include_package_data=True,
    data_files=[('/etc/pifan', ['pifanpy/pifan.conf']), ('/etc/init.d', ['script/pifan'])],
    exclude_package_data={'': ['.gitignore', 'README.md', 'LICENSE']},
    install_requires=[],
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'pifan=pifanpy:fan',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ]
)