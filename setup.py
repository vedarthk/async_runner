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
    'django>=1.9.2'
]

setup(
    name='async_runner',
    version='0.1.7',
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
    license="MIT",
    zip_safe=False,
    keywords='async_runner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
