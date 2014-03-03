# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

# future import should be the beginning line
from __future__ import with_statement

__all__ = ['Detector', ]

import os
import re
import wsgiref.util

from ._config import DEFAULT_ROBOTS_JSON, DEFAULT_EXTENSIONS_JSON
from ._config import json, unicode_to_wsgi


class Detector(object):
    """
    Detects if the current request is from a search engine robot
    """

    __slots__ = ['__ignored_routes', '__matched_routes', '__request',
                 '__check_file_extensions', 'extensions', 'robots', ]

    def __init__(self,
                 ignored_routes=[],
                 matched_routes=[],
                 request={},
                 check_file_extensions=False,
                 robots_json=None,
                 extensions_json=None):
        """
        The constructor.

        Keyword arguments:
        :param ignored_routes: list of blacklisted route regexes.
        :param matched_routes: list of whitelisted route regexes.
        :param request: mapping object of HTTP request variables.
        :param check_file_extensions: bool to check if the url is going to a
            static file resource that should not be intercepted.
        :param robots_json: absolute path to a `robots.json` file.
        :param extensions_json: absolute path to an `extensions.json` file.
        """

        self.__ignored_routes = ignored_routes
        self.__matched_routes = matched_routes

        # Python does not have a global object for HTTP request, rather, the
        # HTTP request data are available as a CGI/WSGI environment.
        self.__request = request or dict(
            [(k, unicode_to_wsgi(v)) for k, v in os.environ.items()])

        # `extensions.json` is specified, yet do not require checking file
        # extensions. this probably means a misuse.
        assert(not (not check_file_extensions and extensions_json))
        self.__check_file_extensions = check_file_extensions

        # json.load() may raise IOError, TypeError, or ValueError
        with open(robots_json or DEFAULT_ROBOTS_JSON, 'r') as f:
            self.robots = json.load(f)
            f.close()

        # same as above
        with open(extensions_json or DEFAULT_EXTENSIONS_JSON, 'r') as f:
            self.extensions = json.load(f)
            f.close()

        pass  # void return

    def detect(self):
        """
        Returns True if the request came from a search engine robot, and False
        otherwise.
        """

        # TODO

        # detect extensions in order to prevent direct requests to static files
        if self.__check_file_extensions:
            pass

        #if no match at all, return false
        return False

    pass
