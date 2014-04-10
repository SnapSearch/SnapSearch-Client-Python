# -*- coding: utf-8 -*-
"""
    SnapSearch.api.environ
    ~~~~~~~~~~~~~~~~~~~~~~

    wrapper for CGI-style ``environ`` (``dict`` of HTTP request variables)

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['AnyEnv', ]


import os
import sys
import wsgiref.util

from .._compat import (
    url_parse_qs,
    url_quote,
    url_split,
    url_unquote, )


class AnyEnv(object):
    """
    Wraps a CGI-style ``environ`` (builtin Python ``dict``) with WSGI-defined
    variables and properties in SnapSearch-specified format and encoding.
    """

    @property
    def environ(self):
        """
        underlying CGI-style ``environ`` extended with WSGI-defined variables.
        """
        return self.__environ

    @property
    def GET(self):
        """
        parsed ``QUERY_STRING`` as a multi-``dict`` (i.e. each ``key``
        associated with a ``list`` of values).
        """
        # :PEP:`3333`: ``QUERY_STRING`` MAY be empty or absent.
        if not self.__parsed_qs:
            self.__parsed_qs = url_parse_qs(
                self.environ.get('QUERY_STRING', ""), True)
        return self.__parsed_qs

    @property
    def scheme(self):
        """
        getter of ``environ['wsgi.url_scheme']``.
        """
        # WSGI-defined variable ``wsgi.url_scheme`` MUST present.
        return self.environ['wsgi.url_scheme']

    @property
    def method(self):
        """
        getter of ``environ['REQUEST_METHOD']``, or ``"N/A"`` if absent.
        """
        # :PEP:`3333`: ``REQUEST_METHOD`` MUST present and be non-empty.
        return self.environ['REQUEST_METHOD']

    @property
    def user_agent(self):
        """
        getter of ``environ['HTTP_USER_AGENT']``, or ``""`` if absent.
        """
        # :PEP:`3333`: ``HTTP_USER_AGENT`` MAY be empty or absent.
        return self.environ.get('HTTP_USER_AGENT', "")

    @property
    def path_qs(self):
        """
        relative request URL (without ``HTTP_HOST`` but with ``QUERY_STRING``),
        decoded from :RFC:`3986` percent-encoding (i.e. ``'%20'``-> ``' '``)
        and Google's ``_escaped_fragment_``  `protocol`_.

        .. _`protocol`: http://developers.google.com/webmasters/ajax-crawling/
            docs/specification
        """
        return self._get_decoded_path(True)

    @property
    def url(self):
        """
        full request URL (including ``HTTP_HOST`` and ``QUERY_STRING``),
        encoded to :RFC:`3986` percent-encoding (i.e. ``' '``-> ``'%20'``), but
        decoded from Google's ``_escaped_fragment_`` `protocol`_.

        .. _`protocol`: http://developers.google.com/webmasters/ajax-crawling/
            docs/specification
        """
        # (WSGI) applications are allowed to add new entries to the ``environ``
        # per the WSGI 1.0.1 spec (see :PEP:`3333` Specification Details).
        if "SnapSearch.encoded_url" not in self.environ:
            self.environ['SnapSearch.encoded_url'] = \
                self._get_encoded_url(True)
        return self.environ['SnapSearch.encoded_url']

    # private properties
    __slots__ = ['__parsed_qs', '__environ', ]

    def __init__(self, environ):
        """
        :param environ: CGI-style environment variables
        :type environ: builtin Python ``dict`` (see :PEP:`3333`)
        """
        # add missing CGI-defined variables (see :RFC:`3875).
        environ.setdefault('REQUEST_METHOD', "N/A")
        # add missing WSGI-defined variables (see :PEP:`3333`).
        environ.setdefault('wsgi.version', (1, 0))
        environ.setdefault('wsgi.input',
                           getattr(sys.stdin, 'buffer', sys.stdin))
        environ.setdefault('wsgi.errors', sys.stderr)
        environ.setdefault('wsgi.multithread', False)
        environ.setdefault('wsgi.multiprocess', True)
        environ.setdefault('wsgi.run_once', True)
        environ.setdefault('wsgi.url_scheme',
                           wsgiref.util.guess_scheme(environ))
        # parsed query string
        self.__parsed_qs = {}
        # make a local reference to the raw ``environ``
        self.__environ = environ
        pass  # void return

    def _get_encoded_url(self, include_qs=True):
        # percent-encoded full uri, to be passed to SnapSearch backend.
        if include_qs and "_escaped_fragment_" in self.GET:
            return self._get_encoded_url(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(True)
        return wsgiref.util.request_uri(self.environ, include_qs)

    def _get_decoded_path(self, include_qs=True):
        # un-percent-encoded request uri, relative to site root (/).
        if include_qs and "_escaped_fragment_" in self.GET:
            return self._get_decoded_path(False) + "%(qs)s%(hash)s" % \
                self._get_real_qs_and_hash_fragment(False)
        url = url_split(wsgiref.util.request_uri(self.environ, True))
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
