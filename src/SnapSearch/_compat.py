# -*- coding: utf-8 -*-
"""
    SnapSearch._compat
    ~~~~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['DEBUG', 'PY2', ]


import os
import sys

# global directives

# debugging mode flag
DEBUG = ('DEBUG' in os.environ) and ('NDEBUG' not in os.environ)

# python 2.x flag
PY2 = (sys.version_info[0] == 2)


# language / package compatibility

try:
    # python 3.x
    from http.client import responses as HTTP_STATUS_CODES
    from urllib.parse import parse_qs as url_parse_qs
    from urllib.parse import quote as url_quote
    from urllib.parse import urlsplit as url_split
    from urllib.parse import unquote as url_unquote
except ImportError:
    # python 2.x
    from httplib import responses as HTTP_STATUS_CODES
    from urlparse import parse_qs as url_parse_qs
    from urllib import quote as url_quote
    from urlparse import urlsplit as url_split
    from urllib import unquote as url_unquote

# string literal utilities

# python 3.2 dropped explicit unicode literal, i.e., u"str" being illegal, so
# we need a helper function u("str") to emulate u"str" (see :PEP:`414`).

if PY2:

    def u(s):
        return unicode(s, "unicode_escape")

else:

    def u(s):
        return s


# HTTP does not directly support Unicode. So string variables must either be
# ISO-8859-1 characters, or use :RFC:`2047` MIME encoding (see :PEP:``3333``).

# :PEP:`383`: surrogate escape
enc, esc = sys.getfilesystemencoding(), "surrogateescape"


def n(u):
    return u.encode(enc, esc).decode("iso-8859-1")


def b(s):
    return s.encode("iso-8859-1")


# other useful helper functions

def identity(any):
    return any
