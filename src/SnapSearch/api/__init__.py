# -*- coding: utf-8 -*-
"""
    SnapSearch.api
    ~~~~~~~~~~~~~~

    Backend Service Abstraction Layer for `SnapSearch`_.

    .. _`SnapSearch`: https://snapsearch.io/

    :copyright: 2014 by `SnapSearch`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['SNAPSEARCH_API_URL',
           'SNAPSEARCH_API_USER_AGENT',
           'SNAPSEARCH_API_HTTP_LIBRARY',
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

from .. import __version__ as __client_version__

# snapsearch api parameters (can be changed by users)

SNAPSEARCH_API_URL = "https://snapsearch.io/api/v1/robot"
SNAPSEARCH_API_USER_AGENT = "snapsearch-client " \
                            "(python/{0}.{1}.{2})".format(*__client_version__)
SNAPSEARCH_API_FOLLOW_REDIRECT = False
SNAPSEARCH_API_TIMEOUT = 30


# snapsearch api resource bundle

RESOURCE_DIR = os.path.dirname(__file__)


def confirm_resource(name):
    """
    :param name: name of the bundled resource file.
    :returns: confirmed full path to the specified resource file.
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


# snapsearch api constants (should NEVER be changed by users)

SNAPSEARCH_API_HTTP_LIBRARY = __httpinfo[0]
SNAPSEARCH_API_ACCEPT_ENCODING = ", ".join(__httpinfo[2])
