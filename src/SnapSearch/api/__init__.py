# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#
"""
SnapSearch Backend Service Abstraction Layer
"""

__all__ = ['SNAPSEARCH_API_URL',
           'SNAPSEARCH_API_FOLLOW_REDIRECT',
           'SNAPSEARCH_API_TIMEOUT',
           'DEFAULT_CA_BUNDLE_PEM',
           'DEFAULT_EXTENSIONS_JSON',
           'DEFAULT_ROBOTS_JSON',
           'Request',
           'Response',
           'dispatch', ]


import os
import os.path
import sys

# snapsearch api resource bundle

SNAPSEARCH_API_URL = "https://snapsearch.io/api/v1/robot"

SNAPSEARCH_API_FOLLOW_REDIRECT = True
SNAPSEARCH_API_TIMEOUT = 30

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

from .request import Request
from .response import Response

from .backend import dispatch
