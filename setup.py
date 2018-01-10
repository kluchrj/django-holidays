import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-holidays',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='App for managing holidays.',
    long_description=README,
    author='Danny Browne, Christian Klus'
)