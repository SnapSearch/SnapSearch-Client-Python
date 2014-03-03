# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['DEFAULT_ROBOTS_JSON', 'DEFAULT_EXTENSIONS_JSON', 'json', ]

import os
import os.path
import sys

# debugging flag

DEBUG = ('DEBUG' in os.environ) and ('NDEBUG' not in os.environ)

# package names unification

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
    # python 2.6+
    import json
except ImportError:
    # python 2.5
    import simplejson as json

# python 3.2 dropped explicit unicode literal, i.e., u"str" being illegal, so
# we need a helper function u("str") to emulate u"str" (see :PEP:`414`).

if sys.version_info[0] == 2:

    def u(s):
        return unicode(s, "unicode_escape")

    pass

else:

    def u(s):
        return s

    pass

# package data localization

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")


def validated_resource(name):
    """
    Returns validated full path to the specified resource file name.
    """
    path = os.path.abspath(os.path.join(RESOURCES_DIR, name))
    if os.access(path, os.F_OK | os.R_OK):
        return path
    return None


DEFAULT_ROBOTS_JSON = validated_resource("robots.json")
DEFAULT_EXTENSIONS_JSON = validated_resource("extensions.json")

# string encoding utilities

# HTTP does not directly support Unicode. So string variables must either be
# ISO-8859-1 characters, or use :RFC:`2047` MIME encoding (see :PEP:``3333``).

# :PEP:`383`: surrogate escape
enc, esc = sys.getfilesystemencoding(), "surrogateescape"


def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode("iso-8859-1")


def wsgi_to_bytes(s):
    return s.encode("iso-8859-1")
