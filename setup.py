from setuptools import setup, find_packages
from setuptools.command.install import install
import sys
import os

# Install
# python setup.py install --record files.txt

# Uninstall
# pip uninstall microfanPi


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print "Dualion Power!"
        install.run(self)
        # post-processing code
try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

try:
    if not os.path.exists("/etc/pifan"):
        os.makedirs("/etc/pifan")
        os.rename("pifanpy/pifan.conf", "/etc/pifan/pifan.conf")
except:
    print "Config file not created"


setup(
    name="PiFan",
    version="0.1.0",
    description="Software to control fan",
    author="Dualion",
    author_email="admin@dualion.com",
    url="http://dualion.com/",
    packages=['pifanpy'],
    include_package_data=True,
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