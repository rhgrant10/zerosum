#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('requirements_dev.txt') as requirements_file:
    dev_requirements = requirements_file.read().splitlines()

setup_requirements = [
    # TODO(rhgrant10): put setup requirements (distutils extensions, etc.) here
]

setup(
    name='zerosum',
    version='0.1.0',
    description="Zero sum algorithms",
    long_description=readme + '\n\n' + history,
    author="Robert Grant",
    author_email='rhgrant10@gmail.com',
    url='https://github.com/rhgrant10/zerosum',
    packages=find_packages(include=['zerosum']),
    entry_points={
        'console_scripts': [
            'zerosum=zerosum.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='zerosum',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
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
    tests_require=dev_requirements,
    setup_requires=setup_requirements,
)
