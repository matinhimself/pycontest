from setuptools import setup
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pycontest',
    version='1.2',
    packages=['pycontest'],
    url='https://github.com/matinhimself/pycontest',
    license='MIT',
    author='Matin Habibi',
    author_email='aktualled@gmail.com',
    description='An easy to use test case generator.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.8",
)
