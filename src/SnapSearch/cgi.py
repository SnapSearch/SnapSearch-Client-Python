# -*- coding: utf-8 -*-
"""
    SnapSearch.cgi
    ~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/09
"""

__all__ = ['InterceptorController', ]


import io
import os
import sys

import SnapSearch.api as api

from .interceptor import Interceptor


@api.response.message_extractor
def default_response_callback(response_body):
    """
    Removes staled HTTP headers from response body
    """
    response_body['headers'] = [
        (key, val) for key, val in response_body['headers']
        if key.lower() in (b"location", b"server", b"status")]
    return response_body


class InterceptorController(object):
    """
    Wraps a CGI script (see :RFC:`3875`) by temporarily buffering its standard
    output, until the incoming HTTP request has been investigated by the
    associated ``Interceptor`` object. In case of interception, the buffered
    data will be replaced with the response from SnapSearch backend service.
    """

    @property
    def interceptor(self):
        """
        associated ``Interceptor`` object.
        """
        return self.__interceptor

    @property
    def response_callback(self):
        """
        associated callback object.
        """
        return self.__response_callback

    __slots__ = ['__interceptor', '__response_callback',
                 '__real_stdout', '__stdout_buffer', ]

    def __init__(self, interceptor, response_callback=None):
        """
        :param interceptor: associated ``Interceptor`` object

        Optional argument(s):

        :param response_callback: callback object for handling the response
            from SnapSearch backend service; the returned ``dict`` should at
            least contain the following three keys:

            - ``status``: full HTTP status with code and string message
            - ``headers``: ``list`` of 2-``tuple`` for HTTP message headers
            - ``html``: HTML content of the scrapped URL

        :type response_callback: ``callable`` with signature ``"(response)->
            dict"``

        :raises AssertionError: if ``interceptor`` is not an instance of
            ``Interceptor``.
        """
        assert(isinstance(interceptor, Interceptor))
        #
        self.__interceptor = interceptor
        self.__response_callback = response_callback \
            if callable(response_callback) else default_response_callback
        self.__real_stdout = None
        self.__stdout_buffer = None
        pass

    def start(self, environ=None):
        """
        Optional argument(s):

        :param environ: incoming HTTP request as a ``dict`` of variables,
            defaults to (a *shallow* copy of) ``os.environ``.
        :type request: ``dict``

        :raises AssertionError: if ``environ`` does not contain CGI-defined\
            variables such as ``GATEWAY_INTERFACE`` (see :RFC:`3875`).
        """
        # make a shallow copy of system environment variables
        if not environ:
            environ = os.environ.copy()

        # :RFC:`3875`: ``GATEWAY_INTERFACE`` MUST be set to the dialect of CGI
        # being used by the server to communicate with the script.
        assert(environ.get('GATEWAY_INTERFACE', "").startswith("CGI/"))

        # redirect standard output stream
        self.__stdout_buffer = io.BytesIO()
        self.__real_stdout, sys.stdout = sys.stdout, self.__stdout_buffer

        # start interception
        response = None
        try:
            response = self.interceptor(environ)
        except:
            pass

        # non-intercepted response
        if not isinstance(response, dict):
            self.stop(True)
            return False

        # intercepted response
        message = self.response_callback(response)
        self.__real_stdout.write(b"Status: ")
        self.__real_stdout.write(message['status'])
        self.__real_stdout.write(b"\r\n")
        for key, val in message['headers']:
            self.__real_stdout.write(key)
            self.__real_stdout.write(b": ")
            self.__real_stdout.write(val)
            self.__real_stdout.write(b"\r\n")
        self.__real_stdout.write(b"\r\n")
        self.__real_stdout.write(message['html'])

        return True

    def stop(self, release=False):
        """
        Optional argument(s):

        :param release: release bufferred data to standard output stream.
        :type release: ``bool``
        """
        # relase buffered data to real stdout
        if release:
            self.__real_stdout.write(self.__stdout_buffer.getvalue())
            self.__stdout_buffer.close()
        # resume standard output stream
        sys.stdout, self.__real_stdout = self.__real_stdout, None
        self.__stdout_buffer = self.__real_stdout = None
        pass  # void return

    pass
