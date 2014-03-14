# -*- coding: utf-8 -*-
"""
    SnapSearch.wsgi
    ~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['InterceptorMiddleware', ]


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


class InterceptorMiddleware(object):
    """
    Wraps a WSGI-defined web application (see :PEP:`3333`) and intercepts
    incoming HTTP requests through the associated ``Interceptor`` object.
    """

    @property
    def application(self):
        """
        associated WSGI application.
        """
        return self.__application

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

    # private members
    __slots__ = ['__application', '__interceptor', '__response_callback', ]

    def __init__(self, application, interceptor, response_callback=None):
        """
        :param application: associated (wrapped) WSGI application object
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
        self.__application = application
        self.__interceptor = interceptor
        self.__response_callback = response_callback \
            if callable(response_callback) else default_response_callback
        pass

    def __call__(self, environ, start_response):
        """
        WSGI-defined web application interface (see :PEP:`3333`).
        """
        # start interception
        response = None
        try:
            response = self.interceptor(environ)
        except:
            # silently resume to non-intercepted response
            pass

        # non-intercepted response
        if not isinstance(response, dict):
            return self.application(environ, start_response)

        # intercepted response
        message = self.response_callback(response)

        # ship out
        start_response(message['status'], message['headers'])
        return message['html']

    pass
