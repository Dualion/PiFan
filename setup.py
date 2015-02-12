from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="microfanPi",
    version="0.1.0",
    description="Software to control fan",
    author="Dualion",
    packages=['microfanPi'],
    install_requires=[],
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'microfan=microfanPi:fan',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ]



)
