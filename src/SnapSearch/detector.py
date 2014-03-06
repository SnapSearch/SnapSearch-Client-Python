# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

# future import should be the beginning line
from __future__ import with_statement

__all__ = ['Detector', ]

import json
import os
import re
import sys

import SnapSearch.api as api
import SnapSearch.error as error

from ._config import u


class Detector(object):
    """
    Detector detects if the current request is a) from a search engine robot
    and b) is eligible for interception.
    """

    @property
    def robots(self):
        """
        The ``robots`` property is a ``dict`` of user agent lists:

        .. code-block:: json

            {
                "ignore": [
                    # user agents to be ignored
                ]
                "match": [
                    # user agents to be matched
                ]
            }

        The ``ignore`` list takes precedence over the ``match`` list when
        running the detection algorithm. You can change each list to customise
        ignored and matched robots.
        """
        return self.__robots

    @property
    def extensions(self):
        """
        The ``extensions`` property is a ``dict`` of valid extensions lists:

        .. code-block:: json

            {
                "generic": [
                    # valid generic extensions
                ],
                "python": [
                    # valid python extensions
                ]
            }

        You can change each list to customise valid file extensions.
        """
        return self.__extensions

    # private properties
    __slots__ = ['__ignored_routes', '__matched_routes', '__request',
                 '__check_file_extensions', '__extensions', '__robots', ]

    def __init__(self,
                 ignored_routes=[],
                 matched_routes=[],
                 request={},
                 check_file_extensions=False,
                 robots_json=None,
                 extensions_json=None):
        """
        Keyword arguments:

        :param ignored_routes: ``list|tuple`` of blacklisted route regexes.
        :param matched_routes: ``list|tuple`` of whitelisted route regexes.
        :param request: ``dict`` of HTTP request variables.
        :param check_file_extensions: ``bool`` to check if the URL is going to
            a static file resource that should not be intercepted.
        :param robots_json: absolute path to a ``robots.json`` file.
        :param extensions_json: absolute path to an ``extensions.json`` file.
        """

        self.__ignored_routes = set(ignored_routes)
        self.__matched_routes = set(matched_routes)

        # wrap incoming request as a Request object
        self.__request = api.Request(request)

        # ``extensions.json`` is specified, yet do not require checking file
        # extensions. this probably means a mistake.
        assert(not (not check_file_extensions and extensions_json)), \
            "specified ``extensions_json`` " \
            "while ``check_file_extensions`` is false"
        self.__check_file_extensions = check_file_extensions

        # json.load() may raise IOError, TypeError, or ValueError
        with open(robots_json or api.DEFAULT_ROBOTS_JSON) as f:
            self.__robots = json.load(f)
            f.close()

        # same as above
        with open(extensions_json or api.DEFAULT_EXTENSIONS_JSON) as f:
            self.__extensions = json.load(f)
            f.close()

        pass  # void return

    def detect(self):
        """
        Detects if the request came from a search engine robot and is eligible
        for interception. The Detector will intercept in cascading order:

          1. on an HTTP or HTTPS protocol
          2. on an HTTP GET request
          3. not on any ignored robot user agents (ignored robots take
             precedence over matched robots)
          4. not on any route not matching the whitelist
          5. not on any route matching the blacklist
          6. not on any invalid file extensions if there is a file extension
          7. on requests with _escaped_fragment_ query parameter
          8. on any matched robot user agents

        Returns ``True`` if eligible for interception, ``False`` otherwise.
        """

        # do not intercept protocols other than HTTP and HTTPS
        if not self.__request.scheme in ("http", "https", ):
            return False

        # do not intercept HTTP methods other than GET
        if not self.__request.method in ("GET", ):
            return False

        # user agent may not exist in the HTTP request
        user_agent = self.__request.user_agent

        # request uri with query string
        real_path = self.__request.path_qs

        # validate ``robots`` since it can be altered from outside
        if not self._validate_robots():
            raise error.SnapSearchError(
                "structure of ``robots`` is invalid")

        # do not intercept requests from ignored robots
        ignore_regex = u("|").join(
            [re.escape(tok) for tok in self.robots.get('ignore', [])])
        if re.match(ignore_regex, user_agent, re.I | re.U):
            return False

        # do not intercept if there exist whitelisted route(s) (matched_routes)
        # and that the requested route **does not** match any one of them.
        if self.__matched_routes:
            found = False
            for route in self.__matched_routes:
                route_regex = u(route)
                if re.match(route_regex, real_path, re.I | re.U):
                    found = True
                    break
            if not found:
                return False

        # do not intercept if there exist blacklisted route(s) (ignored_routes)
        # and that the requested route **does** matches one of them.
        if self.__ignored_routes:
            for route in self.__ignored_routes:
                route_regex = u(route)
                if re.match(route_regex, real_path, re.I | re.U):
                    return False

        # detect extensions in order to prevent direct requests to static files
        if self.__check_file_extensions:

            # validate ``extensions`` since it can be altered from outside
            if not self._validate_extensions():
                raise error.SnapSearchError(
                    "structure of ``extensions`` is invalid")

            # create a set of file extensions common for HTML resources
            valid_extensions = set(
                [s.lower() for s in self.extensions.get('generic', [])])
            valid_extensions.update(
                [s.lower() for s in self.extensions.get('python', [])])

            # file extension regex. it looks for "/{file}.{ext}" in an URL that
            # is not preceded by '?' (query parameters) or '#' (hash fragment).
            # it will acquire the last extension that is present in the URL so
            # with "/{file1}.{ext1}/{file2}.{ext2}" the ext2 will be the
            # matched extension. furthermore if a file has multiple extensions
            # "/{file}.{ext1}.{ext2}", it will only match extension2 because
            # unix systems don't consider extensions to be metadata, and
            # windows only considers the last extension to be valid metadata.
            # Basically the {file}.{ext1} could actually just be the filename.
            extension_regex = u(r"""
                ^              # start of the string
                (?:            # begin non-capturing group
                    (?!        # begin negative lookahead
                       [?#]    # question mark '?' or hash '#'
                       .*      # zero or more wildcard characters
                       /       # literal slash '/'
                       [^/?#]+ # {file} - has one or more of any character
                               #     except '/', '?' or '#'
                       \.      # literal dot '.'
                       [^/?#]+ # {extension} - has one or more of any character
                               #     except '/', '?' or '#'
                    )          # end negative lookahead (prevents any '?' or
                               #     '#' that precedes {file}.{extension} by
                               #     any characters)
                    .          # one wildcard character
                )*             # end non-capturing group (captures any number
                               #     of wildcard characters that passes the
                               #     negative lookahead)
                /              # literal slash '/'
                [^/?#]+        # {file} - has one or more of any character
                               # except forward slash, question mark or hash
                \.             # literal dot '.'
                ([^/?#]+)      # {extension} - subgroup has one or more of any
                               #     character except '/', '?' or '#'
            """)

            # match extension regex against decoded path
            matches = re.match(extension_regex, real_path, re.U | re.X)
            if matches:
                url_extension = matches.group(1).lower()
                if not url_extension in valid_extensions:
                    return False

        # detect escaped fragment (since the ignored user agents has already
        # been detected, SnapSearch won't continue the interception loop)
        if "_escaped_fragment_" in self.__request.GET:
            return True

        # intercept requests from matched robots
        matched_regex = u("|").join(
            [re.escape(tok) for tok in self.robots.get('match', [])])
        if re.match(matched_regex, user_agent, re.I | re.U):
            return True

        # do not intercept if no match at all
        return False

    def get_encoded_url(self):
        """
        Keyword arguments:

        :param include_qs: ``bool`` to include query string in the URL.

        Returns :RFC:`3986` percent-encoded complete url.
        """
        return self.__request.url

    def _validate_robots(self):
        # ``robots`` should be a ``dict`` object, if keys ``ignore`` and
        # ``match`` exist, the respective values must be ``list`` objects.
        return isinstance(self.robots, dict) and \
            isinstance(self.robots.get('ignore', []), list) and \
            isinstance(self.robots.get('match', []), list)

    def _validate_extensions(self):
        # ``extensions`` should be a ``dict`` object, if keys ``generic`` and
        # ``python`` exist, the respective values must be ``list`` objects.
        return isinstance(self.extensions, dict) and \
            isinstance(self.extensions.get('generic', []), list) and \
            isinstance(self.extensions.get('python', []), list)

    pass
