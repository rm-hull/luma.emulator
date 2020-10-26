#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from io import open
from setuptools import setup, find_packages


def read_file(fname, encoding='utf-8'):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding=encoding) as r:
        return r.read()


def find_version(*file_paths):
    fpath = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = read_file(fpath)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    err_msg = 'Unable to find version string in {}'.format(fpath)
    raise RuntimeError(err_msg)


README = read_file('README.rst')
CONTRIB = read_file('CONTRIBUTING.rst')
CHANGES = read_file('CHANGES.rst')
version = find_version('luma', 'emulator', '__init__.py')

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'pytest',
    'pytest-cov',
    'pytest-timeout'
]

setup(
    name="luma.emulator",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("A suite of pseudo-devices for luma.core components"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    long_description_content_type="text/x-rst",
    license="MIT",
    keywords="raspberry orange banana pi rpi opi sbc oled lcd led display screen spi i2c emulator",
    url="https://github.com/rm-hull/luma.emulator",
    download_url="https://github.com/rm-hull/luma.emulator/tarball/" + version,
    namespace_packages=["luma"],
    packages=find_packages(),
    include_package_data=True,
    package_data={"luma.emulator.images": [
        "luma/emulator/images/led_on.png",
        "luma/emulator/images/led_off.png",
        "luma/emulator/images/7-segment.png"
    ]},
    install_requires=[
        "luma.core>=1.14.0",
        "pygame"
    ],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    extras_require={
        'docs': [
            'sphinx >= 1.5.1'
        ],
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': test_deps
    },
    zip_safe=False,
    python_requires='>=3.6, <4',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Libraries :: pygame",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
