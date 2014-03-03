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
import sys
import wsgiref.util

from ._config import json, u, unicode_to_wsgi
from ._config import url_parse_qs, url_quote, url_split, url_unquote
from ._config import DEBUG, DEFAULT_ROBOTS_JSON, DEFAULT_EXTENSIONS_JSON


def wsgify_request(request=None):
    """
    Copies and extends an OS / CGI environment with WSGI-defined variables.
    """
    # make a (shallow) copy of the request
    environ = {}
    if isinstance(request, dict):
        environ.update(request)
    # add absent variables from the global OS / CGI environment
    for k, v in os.environ.items():
        environ.setdefault(k, unicode_to_wsgi(v))
    # add absent WSGI-defined variables (see :PEP:`3333`).
    environ.setdefault('wsgi.version', (1, 0))
    environ.setdefault('wsgi.input',
                       getattr(sys.stdin, 'buffer', None) or sys.stdin)
    environ.setdefault('wsgi.errors', sys.stderr)
    environ.setdefault('wsgi.multithread', False)
    environ.setdefault('wsgi.multiprocess', True)
    environ.setdefault('wsgi.run_once', True)
    environ.setdefault('wsgi.url_scheme', wsgiref.util.guess_scheme(environ))
    return environ


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
        :param ignored_routes: ``list|tuple`` of blacklisted route regexes.
        :param matched_routes: ``list|tuple`` of whitelisted route regexes.
        :param request: ``dict`` of HTTP request variables.
        :param check_file_extensions: ``bool`` to check if the url is going to
            a static file resource that should not be intercepted.
        :param robots_json: absolute path to a ``robots.json`` file.
        :param extensions_json: absolute path to an ``extensions.json`` file.
        """

        self.__ignored_routes = set(ignored_routes)
        self.__matched_routes = set(matched_routes)

        # Python does not have a global object for HTTP request, rather, the
        # HTTP request data are available from OS / CGI / WSGI environment.
        self.__request = wsgify_request(request)

        # ``extensions.json`` is specified, yet do not require checking file
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
        Returns ``True`` if the request came from a search engine robot and
        is eligible for interception, ``False`` otherwise.
        """

        # do not intercept protocols other than HTTP and HTTPS
        if not self._get_url_scheme() in ("http", "https", ):
            return False

        # do not intercept HTTP methods other than GET
        if not self._get_http_method() in ("GET", ):
            return False

        # user agent may not exist in the HTTP request
        user_agent = self._get_user_agent() or ""
        real_path = self._get_decoded_path()

        # validate ``robots`` since it is fully exposed to developers
        if not self._validate_robots():
            raise TypeError("structure of ``robots`` is invalid")

        # do not intercept requests from ignored robots
        ignore_regex = u("|").join(
            [re.escape(r) for r in self.robots.get('ignore', [])])
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
            # validate ``extensions`` since it is fully exposed to developers
            if not self._validate_extensions():
                raise TypeError("structure of ``extensions`` is invalid")
            # create a set of file extensions common for HTML resources
            valid_extensions = set(
                [s.lower() for s in self.extensions.get('generic', [])])
            valid_extensions.update(
                [s.lower() for s in self.extensions.get('python', [])])
            # file extension regex
            extension_regex = u(r"""
                ^              # start of the string
                (?:            # begin non-capturing group
                    (?!        # begin negative lookahead
                       [?#]    # question mark '?' or hash character '#'
                       .*      # zero or more wildcard characters
                       /       # literal slash '/'
                       [^/?#]+ # {file} - has one or more of any character
                               #   except '/', '?' or '#'
                       \.      # literal dot '.'
                       [^/?#]+ # {extension} - has one or more of any character
                               #   except '/', '?' or '#'
                    )          # end negative lookahead (prevents any '?' or
                               #   '#' that precedes {file}.{extension} by any
                               #   characters)
                    .          # wildcard character
                )*             # end non-capturing group (captures any number
                               #   of wildcard characters that passes the
                               #   negative lookahead)
                /              # literal slash '/'
                [^/?#]+        # {file} - has one or more of any character
                               # except forward slash, question mark or hash
                \.             # literal dot '.'
                ([^/?#]+)      # {extension} - subgroup has one or more of any
                               #   character except '/', '?' or '#'
            """)
            # match extension regex against decoded path
            matches = re.match(extension_regex, real_path, re.U | re.X)
            if matches:
                url_extension = matches.group(1).lower()
                if not url_extension in valid_extensions:
                    return False
            pass

        # detect escaped fragment (since the ignored user agents has already
        # been detected, SnapSearch won't continue the interception loop)
        if "_escaped_fragment_" in self._get_parsed_qs():
            return True

        # detect requests from matched robots
        matched_regex = u("|").join(
            [re.escape(r) for r in self.robots.get('match', [])])
        if re.match(matched_regex, user_agent, re.I | re.U):
            return True

        #if no match at all, return false
        return False

    def get_encoded_url(self, include_query=True):
        # url_quote()'ed complete uri.
        if include_query and "_escaped_fragment_" in self._get_parsed_qs():
            return self.get_encoded_url(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(True)
        return wsgiref.util.request_uri(self.__request, include_query)

    def _get_decoded_path(self, include_query=True):
        # url_unquote()'ed request path (relative to site root),
        # for matching against the white / black list of routes.
        if include_query and "_escaped_fragment_" in self._get_parsed_qs():
            return self._get_decoded_path(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(False)
        tup = url_split(wsgiref.util.request_uri(self.__request, True))
        path = "?".join([tup.path, tup.query]) if include_query else tup.path
        return url_unquote(path)

    def _get_real_qs_and_hash_fragment(self, encode):
        """
        Gets the real query string and hash fragment by reversing the Google's
        ``_escaped_fragment_``_ protocol to the hash bang mode.

.. _: https://developers.google.com/webmasters/ajax-crawling/docs/specification

        Keyword arguments:
        :param encode: ``bool`` to quote the query string or not

        Returns:
        ``dict`` of query string (``qs``) and hash fragment (``hash``)
        """
        query_parameters = self._get_parsed_qs()
        # compose qs
        qs = []
        for k in query_parameters:
            qs.extend(["{0}={1}".format(k, v) for v in query_parameters[k]
                       if k != "_escaped_fragment_"])
        # compose hash
        hash = query_parameters.get('_escaped_fragment_', [])
        # codec
        f = (lambda s: url_unquote(s)) \
            if encode else (lambda s: url_quote(s))
        return {'qs': f("?{0}".format("&".join(qs)) if qs else ""),
                'hash': f("#!{0}".format("".join(hash)) if hash else "")}

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

    def _get_parsed_qs(self):
        # :PEP:`3333`: ``QUERY_STRING`` MAY be empty or absent.
        return url_parse_qs(self.__request.get('QUERY_STRING', ""), True)

    def _get_url_scheme(self):
        # :PEP:`3333`: WSGI-defined variable ``wsgi.url_scheme`` MUST present.
        return self.__request.get('wsgi.url_scheme', None)

    def _get_http_method(self):
        # :PEP:`3333`: ``REQUEST_METHOD`` MUST present and be non-empty.
        return self.__request.get('REQUEST_METHOD', None)

    def _get_user_agent(self):
        # ``HTTP_USER_AGENT`` MAY be empty or absent.
        return self.__request.get('HTTP_USER_AGENT', None)

    pass
