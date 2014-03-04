# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['SNAPSEARCH_API_URL', 'SNAPSEARCH_RES_DIR', 'DEFAULT_CACERT_PEM',
           'DEFAULT_EXTENSIONS_JSON', 'DEFAULT_ROBOTS_JSON', 'DEBUG', ]

import os
import os.path
import sys


# language / package compatibility

try:
    # python 2.6+
    import json
except ImportError:
    # python 2.5
    import simplejson as json

try:
    # python 3.x
    from urllib.parse import parse_qs as url_parse_qs
    from urllib.parse import quote as url_quote
    from urllib.parse import urlsplit as url_split
    from urllib.parse import unquote as url_unquote
except ImportError:
    # python 2.x
    from urlparse import parse_qs as url_parse_qs
    from urllib import quote as url_quote
    from urlparse import urlsplit as url_split
    from urllib import unquote as url_unquote

try:
    # python 3.x
    from io import BytesIO
except ImportError:
    # python 2.x
    from StringIO import StringIO as BytesIO

# string literal utilities

# python 3.2 dropped explicit unicode literal, i.e., u"str" being illegal, so
# we need a helper function u("str") to emulate u"str" (see :PEP:`414`).

if sys.version_info[0] == 2:

    def u(s):
        return unicode(s, "unicode_escape")

else:

    def u(s):
        return s


# HTTP does not directly support Unicode. So string variables must either be
# ISO-8859-1 characters, or use :RFC:`2047` MIME encoding (see :PEP:``3333``).

# :PEP:`383`: surrogate escape
enc, esc = sys.getfilesystemencoding(), "surrogateescape"


def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode("iso-8859-1")


def wsgi_to_bytes(s):
    return s.encode("iso-8859-1")


# snapsearch global data

SNAPSEARCH_API_URL = "https://snapsearch.io/api/v1/robot"

SNAPSEARCH_RES_DIR = os.path.join(os.path.dirname(__file__), "resources")


def confirm_resource(name):
    """
    Returns confirmed full path to the specified resource file name.
    """
    path = os.path.abspath(os.path.join(SNAPSEARCH_RES_DIR, name))
    if os.access(path, os.F_OK | os.R_OK):
        return path
    return None


# default CA certification for SnapSearch client
DEFAULT_CACERT_PEM = confirm_resource("cacert.pem")

# default extensions data for SnapSearch detector
DEFAULT_EXTENSIONS_JSON = confirm_resource("extensions.json")

# default robots data for SnapSearch detector
DEFAULT_ROBOTS_JSON = confirm_resource("robots.json")

# global debugging flag
DEBUG = ('DEBUG' in os.environ) and ('NDEBUG' not in os.environ)
