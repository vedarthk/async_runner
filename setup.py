#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'celery>=3.1.20'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='async_runner',
    version='0.1.0',
    description="Async Runner",
    long_description=readme + '\n\n' + history,
    author="Vedarth Kulkarni",
    author_email='vedarthk@vedarthz.in',
    url='https://github.com/vedarthk/async_runner',
    packages=[
        'async_runner',
    ],
    package_dir={'async_runner':
                 'async_runner'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='async_runner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
