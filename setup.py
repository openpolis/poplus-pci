#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
from os import path

from setuptools import setup
__author__ = 'guglielmo'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='poplus-pci',
    version='0.1.4',
    description='Generic python bindings to connect to the Poplus components',
    long_description=long_description,
    author='Openpolis',
    author_email='guglielmo@openpolis.it',
    url='https://github.com/openpolis/poplus-pci',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],
    keywords='poplus api wrapper',
    packages=['pci'],
    install_requires=[
        'tortilla'
    ]
)
