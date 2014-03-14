#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch Client Python
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Pythonic HTTP Client and Middleware for `SnapSearch`_.

    .. _`SnapSearch`: https://snapsearch.io/

    :copyright: 2014 by `SnapSearch`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

PACKAGE = "snapsearch-client-python"

import os
import sys

from distutils.core import setup
from glob import glob
from os.path import isfile, join


# auxiliary data files for installation
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
    files = glob(join("docs", "*.rst"))
    if files:
        data_files.append((join(datadir, "docs"), files))
    #
    for example in ("flask", "cgi", ):
        files = glob(join("examples", example, "*.py")) + \
            glob(join("examples", example, "*.rst"))
        if files:
            data_files.append((join(datadir, "examples", example), files))
    #
    files = glob(join("tests", "*.py"))
    if files:
        data_files.append((join(datadir, "tests"), files))
    #
    files = glob(join("tests", "_config", "*.*"))
    if files:
        data_files.append((join(datadir, "tests", "_config"), files))
    #
    assert data_files
    for install_dir, files in data_files:
        assert files
        for f in files:
            assert isfile(f), (f, install_dir)
    return data_files


# make sure local package takes precedence over installed (old) package
sys.path.insert(0, join('src', ))
import SnapSearch as pkg


setup(
    name=PACKAGE,
    packages=["SnapSearch", "SnapSearch.api"],
    package_dir={"SnapSearch": join("src", "SnapSearch", ),
                 "SnapSearch.api": join("src", "SnapSearch", "api"), },
    package_data={"SnapSearch.api": ["*.pem", "*.json", ], },
    data_files=get_data_files(),
    version=".".join(map(str, pkg.__version__)),
    author=pkg.__author__,
    license=pkg.__license__,
    author_email=pkg.__contact__,
    description="Pythonic HTTP Client and Middleware Library for SnapSearch",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 4 - Beta",
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
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["SnapSearch", "client", "SEO"],
    platforms="All",
    provides=["SnapSearch", ],
    requires=["pycurl", ],
    url="https://github.com/liuyu81/SnapSearch-Client-Python",
)
