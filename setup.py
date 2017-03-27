#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ingestion',
    version='0.1.0',
    description='Ingestion is a Python package for converting data files to other formats',
    author='Kyle Harrison',
    author_email='kyle90adam@hotmail.com',
    url='https://github.com/apoclyps/ingestion',
    packages=[
        'ingestion',
    ],
    package_dir={
        'ingestion': 'ingestion'
    },
    include_package_data=True,
    install_requires=[],
    license="Unlicense",
    zip_safe=False,
    keywords='ingestion',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
