# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['Request', ]

import os
import sys
import wsgiref.util

from .._config import (url_parse_qs,
                       url_quote,
                       url_split,
                       url_unquote,
                       unicode_to_wsgi, )


class Request(dict):
    """
    Request extends a CGI / WSGI environ with SnapSearch-defined processing.
    """

    @property
    def GET(self):
        """
        Returns parsed ``QUERY_STRING`` as a MultiDict.
        """
        # :PEP:`3333`: ``QUERY_STRING`` MAY be empty or absent.
        if not self.__parsed_qs:
            self.__parsed_qs = url_parse_qs(self.get('QUERY_STRING', ""), True)
        return self.__parsed_qs

    @property
    def scheme(self):
        """
        Returns ``wsgi.url_scheme``
        """
        # WSGI-defined variable ``wsgi.url_scheme`` MUST present.
        return self['wsgi.url_scheme']

    @property
    def method(self):
        """
        Returns ``REQUEST_METHOD`` or ``"N/A"``
        """
        # :PEP:`3333`: ``REQUEST_METHOD`` MUST present and be non-empty.
        return self['REQUEST_METHOD']

    @property
    def user_agent(self):
        """
        Returns ``HTTP_USER_AGENT`` or ``""``
        """
        # :PEP:`3333`: ``HTTP_USER_AGENT`` MAY be empty or absent.
        return self.get('HTTP_USER_AGENT', "")

    @property
    def path_qs(self):
        """
        Relative request URL without ``HTTP_HOST`` but with ``QUERY_STRING``,
        decoded from both :RFC:`3986` percent-encoding (``'%20'``-> ``' '``)
        and Google's ``_escaped_fragment_``__ protocol.

        .. __: http://developers.google.com/webmasters/ajax-crawling/docs
               /specification
        """
        return self._get_decoded_path(True)

    @property
    def url(self):
        """
        Full request URL including ``HTTP_HOST`` and ``QUERY_STRING``, encoded
        to :RFC:`3986` percent-encoding (``' '``-> ``'%20'``), but decoded from
        Google's ``_escaped_fragment_``__ protocol.

        .. __: http://developers.google.com/webmasters/ajax-crawling/docs
               /specification
        """
        return self._get_encoded_url(True)

    # private properties
    __slots__ = ['__parsed_qs', ]

    def __init__(self, environ={}):
        # make a (shallow) copy of the environ
        super(Request, self).__init__(environ)
        # add missing variables from the global OS / CGI environment
        for key, val in os.environ.items():
            self.setdefault(key, unicode_to_wsgi(val))
        # add missing CGI-defined variables (see :RFC:`3875).
        self.setdefault('REQUEST_METHOD', "N/A")
        # add missing WSGI-defined variables (see :PEP:`3333`).
        self.setdefault('wsgi.version', (1, 0))
        self.setdefault('wsgi.input', getattr(sys.stdin, 'buffer', sys.stdin))
        self.setdefault('wsgi.errors', sys.stderr)
        self.setdefault('wsgi.multithread', False)
        self.setdefault('wsgi.multiprocess', True)
        self.setdefault('wsgi.run_once', True)
        self.setdefault('wsgi.url_scheme', wsgiref.util.guess_scheme(self))
        # parsed query string
        self.__parsed_qs = {}
        pass  # void return

    def _get_encoded_url(self, include_qs=True):
        # percent-encoded full uri, to be passed to SnapSearch backend.
        if include_qs and "_escaped_fragment_" in self.GET:
            return self._get_encoded_url(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(True)
        return wsgiref.util.request_uri(self, include_qs)

    def _get_decoded_path(self, include_qs=True):
        # un-percent-encoded request uri, relative to site root (/).
        if include_qs and "_escaped_fragment_" in self.GET:
            return self._get_decoded_path(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(False)
        url = url_split(wsgiref.util.request_uri(self, True))
        path = "?".join([url.path, url.query]) if include_qs else url.path
        return url_unquote(path)

    def _get_real_qs_and_hash_fragment(self, encode):
        # Gets the real query string and hash fragment by reversing Google's
        # ``_escaped_fragment_``__ protocol to the hash bang mode.
        #
        # .. __: http://developers.google.com/webmasters/ajax-crawling/docs
        #        /specification

        # build query parameters and hash fragment. note that ``self.GET`` is a
        # ``MultiDict``, namely, each ``key`` identifies a list of ``val``'s.
        # keep this in mind when trying to enumerate all ``key``-``val`` pairs.
        qs = []
        frag = []
        for key, val_list in self.GET.items():
            if key == "_escaped_fragment_":
                frag.extend(filter(None, val_list))
                continue
            qs.extend(["%s=%s" % (key, val) for val in val_list])

        # apply encoding / decoding filter
        f = url_unquote if encode else url_quote

        return {'qs': f("?{0}".format("&".join(qs)) if qs else ""),
                'hash': f("#!{0}".format("".join(frag)) if frag else "")}

    pass
