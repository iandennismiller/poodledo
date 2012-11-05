from setuptools import setup, find_packages
import os, shutil

version = '0.1'

setup(name='poodledo',
      version=version,
      description="poodledo",
      scripts=[
            "bin/tdcli", 
            "bin/cycle", 
            ],
      long_description="""toodledo python API""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      install_requires = ['parsedatetime', 'plex'],
      packages = ["poodledo"],
      license='MIT',
      zip_safe=False,
      )
