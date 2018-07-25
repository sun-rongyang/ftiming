# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-25 14:45
#  
#  Description: ftiming project. Setup file for `pyftiming` Python package.
# 
from setuptools.command.install import install
from setuptools import setup


setup(
  name = 'pyftiming',
  version = '0.0.9',
  description = 'Python package for `ftiming` project.',
  author = 'Rongyang Sun',
  packages = ['pyftiming'],
  package_dir = {'': 'src'},
  zip_safe = False,
)
