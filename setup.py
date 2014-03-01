#!/usr/bin/env python
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
"""
Setup script for SnapSearch-Client-Python package distribution.
"""

PACKAGE = "SnapSearch-Client-Python"
PY_PACKAGE = "SnapSearch"

import os
import sys

from distutils.core import setup
from glob import glob
from os.path import isfile, join


# auxiliary files for installation
def get_data_files():
    #
    data_files = []
    if sys.platform == "win32":
        datadir = join("doc", PACKAGE)
    else:
        datadir = join("share", "doc", PACKAGE)
    #
    files = ["README.rst", "LICENSE", ]
    if files:
        data_files.append((join(datadir), files))
    #
    files = glob(join("resources", "*.*"))
    if files:
        data_files.append((join(datadir, "resources"), files))
    #
    files = glob(join("tests", "*.py"))
    if files:
        data_files.append((join(datadir, "tests"), files))
    #
    assert data_files
    for install_dir, files in data_files:
        assert files
        for f in files:
            assert isfile(f), (f, install_dir)
    return data_files


# make sure local package overrides installed (old) package
sys.path.append(join('src', ))
import SnapSearch as pkg

setup(
    name=PACKAGE,
    packages=[PY_PACKAGE, ],
    package_dir={PY_PACKAGE: join("src", PY_PACKAGE, ), },
    package_data={PY_PACKAGE: glob(join("resources", "*.*")), },
    data_files=get_data_files(),
    version=".".join(map(str, pkg.__version__)),
    author=pkg.__author__,
    license=pkg.__license__,
    author_email=pkg.__contact__,
    description=pkg.__doc__,
    long_description=open("README.rst").read(),
    keywords=["SnapSearch", "client", "SEO"],
    url="https://github.com/liuyu81/SnapSearch-Client",
    classifiers=[
        "Development Status :: 2 - PreAlpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: "
            "CGI Tools/Libraries",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
