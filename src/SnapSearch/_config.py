# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['DEFAULT_ROBOTS_JSON', 'DEFAULT_EXTENSIONS_JSON', 'json', ]

import os
import os.path
import sys

# package name unification
try:
    # python 2.6+
    import json
except ImportError:
    # python 2.5
    import simplejson as json


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

# HTTP does not directly support Unicode. So all string variables must either
# be ISO-8859-1 characters, or use RFC 2047 MIME encoding. c.f. PEP-3333 by
# P. J. Eby <pje@telecommunity.com>

# surrogate escape c.f. PEP-383 by Martin v. Löwis <martin@v.loewis.de>
enc, esc = sys.getfilesystemencoding(), 'surrogateescape'


def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode('iso-8859-1')


def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')
