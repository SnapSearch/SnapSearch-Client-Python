# -*- coding: utf-8 -*-
"""
    SnapSearch.detector
    ~~~~~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""


# future import should come first
from __future__ import with_statement

__all__ = ['Detector', ]


import json
import os
import re
import sys

import SnapSearch.api as api
import SnapSearch.error as error

from ._compat import u


class Detector(object):
    """
    Detects if the incoming HTTP request a) came from a search engine robot
    and b) is eligible for interception. The ``Detector`` inspects the
    following aspects of the incoming HTTP request:

      1. if the request uses HTTP or HTTPS protocol
      2. if the request uses HTTP ``GET`` method
      3. if the request is *not* from any ignored user agenets
         (ignored robots take precedence over matched robots)
      4. if the request is accessing any route *not* matching the whitelist
      5. if the request is *not* accessing any route matching the blacklist
      6. if the request is *not* accessing any resource with an invalid
         file extension
      7. if the request has ``_escaped_fragment_`` query parameter
      8. if the request is from any matched user agents
    """

    @property
    def robots(self):
        """
        ``dict`` of ``list``'s of user agents from search engine robots:

        .. code-block:: json

            {
                "ignore": [
                    # user agents to be ignored
                ]
                "match": [
                    # user agents to be matched
                ]
            }

        Can be changed to customize ignored and matched search engine robots.
        The ``ignore`` list takes precedence over the ``match`` list.
        """
        return self.__robots

    @property
    def extensions(self):
        """
        ``dict`` of ``list``'s of valid file extensions:

        .. code-block:: json

            {
                "generic": [
                    # valid generic extensions
                ],
                "python": [
                    # valid python extensions
                ]
            }

        Can be changed to customize valid file extensions.
        """
        return self.__extensions

    # private properties
    __slots__ = ['__check_file_extensions', '__extensions', '__ignored_routes',
                 '__matched_routes', '__robots', ]

    def __init__(self,
                 ignored_routes=[],
                 matched_routes=[],
                 check_file_extensions=False,
                 robots_json=None,
                 extensions_json=None):
        """
        Optional arguments:

        :param ignored_routes: blacklisted route regular expressions.
        :type ignored_routes: ``list`` or ``tuple``
        :param matched_routes: whitelisted route regular expressions.
        :type matched_routes: ``list`` or ``tuple``
        :param check_file_extensions: to check if the URL is going to a static
            file resource that should not be intercepted.
        :type check_file_extensions: ``bool``
        :param robots_json: absolute path to an external ``robots.json`` file.
        :param extensions_json: absolute path to an external
            ``extensions.json`` file.

        :raises AssertionError: if ``extensions.json`` is specified, yet
            ``check_file_extensions`` is ``False``.
        """

        self.__ignored_routes = set(ignored_routes)
        self.__matched_routes = set(matched_routes)

        # ``extensions.json`` is specified, yet do not require checking file
        # extensions. this probably means a mistake.
        assert(not (not check_file_extensions and extensions_json)), \
            "specified ``extensions_json`` " \
            "yet ``check_file_extensions`` is false"
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

    def __call__(self, request):
        """
        :param request: incoming HTTP request.
        :type request: ``dict``

        :returns: :RFC:`3986` percent-encoded full URL if the incoming HTTP
            request is eligible for interception, or ``None`` otherwise.

        :raises error.SnapSearchError: if the structure of either
            ``robots.json`` or ``extensions.json`` is invalid.
        """

        # wrap the incoming HTTP request (CGI-style environ)
        environ = api.AnyEnv(request)

        # do not intercept protocols other than HTTP and HTTPS
        if environ.scheme not in ("http", "https", ):
            return None

        # do not intercept HTTP methods other than GET
        if environ.method not in ("GET", ):
            return None

        # user agent may not exist in the HTTP request
        user_agent = environ.user_agent

        # request uri with query string
        real_path = environ.path_qs

        # validate ``robots`` since it can be altered from outside
        if not self._validate_robots():
            raise error.SnapSearchError(
                "structure of ``robots`` is invalid")

        # do not intercept requests from ignored robots
        ignore_regex = u("|").join(
            [re.escape(tok) for tok in self.robots.get('ignore', [])])
        if re.match(ignore_regex, user_agent, re.I | re.U):
            return None

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
                return None

        # do not intercept if there exist blacklisted route(s) (ignored_routes)
        # and that the requested route **does** matches one of them.
        if self.__ignored_routes:
            for route in self.__ignored_routes:
                route_regex = u(route)
                if re.match(route_regex, real_path, re.I | re.U):
                    return None

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
                if url_extension not in valid_extensions:
                    return None

        # detect escaped fragment (since the ignored user agents has already
        # been detected, SnapSearch won't continue the interception loop)
        if "_escaped_fragment_" in environ.GET:
            return environ.url

        # intercept requests from matched robots
        matched_regex = u("|").join(
            [re.escape(tok) for tok in self.robots.get('match', [])])
        if re.match(matched_regex, user_agent, re.I | re.U):
            return environ.url

        # do not intercept if no match at all
        return None

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
