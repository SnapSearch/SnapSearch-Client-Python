# -*- coding: utf-8 -*-
"""
    Backend Service Abstraction Layer for SnapSearch
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['SNAPSEARCH_API_URL',
           'SNAPSEARCH_API_ACCEPT_ENCODING',
           'SNAPSEARCH_API_FOLLOW_REDIRECT',
           'SNAPSEARCH_API_TIMEOUT',
           'DEFAULT_CA_BUNDLE_PEM',
           'DEFAULT_EXTENSIONS_JSON',
           'DEFAULT_ROBOTS_JSON',
           'dispatch',
           'AnyEnv',
           'Response', ]


import os
import os.path
import sys

# snapsearch api parameters

SNAPSEARCH_API_URL = "https://snapsearch.io/api/v1/robot"
SNAPSEARCH_API_FOLLOW_REDIRECT = False
SNAPSEARCH_API_TIMEOUT = 30


# snapsearch api resource bundle

RESOURCE_DIR = os.path.dirname(__file__)


def confirm_resource(name):
    """
    Returns confirmed full path to the specified resource file name.
    """
    path = os.path.abspath(os.path.join(RESOURCE_DIR, name))
    return path if os.access(path, os.F_OK | os.R_OK) else None


# default CA bundle for SnapSearch client
DEFAULT_CA_BUNDLE_PEM = confirm_resource("cacert.pem")

# default extensions data for SnapSearch detector
DEFAULT_EXTENSIONS_JSON = confirm_resource("extensions.json")

# default robots data for SnapSearch detector
DEFAULT_ROBOTS_JSON = confirm_resource("robots.json")


# snapsearch api objects and methods

from .backend import dispatch, httpinfo as __httpinfo
from .environ import AnyEnv
from .response import Response

# snapsearch api constants

SNAPSEARCH_API_ACCEPT_ENCODING = ", ".join(__httpinfo[2])
