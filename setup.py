#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="PiFan",
    version="1.0.0",
    description="Software to control Raspberry Pi fan",
    author="Dualion",
    author_email="admin@dualion.com",
    url="http://dualion.com/",
    packages=['pifanpy'],
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