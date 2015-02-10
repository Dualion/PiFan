from setuptools import setup, find_packages
setup(
    name = "microfan-Pi",
    version = "1.0",
    packages = find_packages(),
    #scripts = ['microfanPi.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    #install_requires = ['docutils>=0.3'],

    #package_data = {
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    #},

	exclude_package_data = { '': ['.gitignore','README.md','LICENSE'] }
	
    # metadata for upload to PyPI
    author = "Dualion",
    author_email = "admin@dualion.com",
    description = "",
    license = "",
    keywords = "",
    url = "http://dualion.com/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)