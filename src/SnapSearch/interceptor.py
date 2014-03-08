# -*- coding: utf-8 -*-
"""
    SnapSearch.interceptor
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['Interceptor', ]


from .client import Client
from .detector import Detector


class Interceptor(object):
    """
    Intercepts the incoming HTTP request using an associated ``Detector``
    object to detect for search engine robots. If the request is elegible for
    interception, the other associated ``Client`` object will dispatch the
    requested URL to SnapSearch backend service for scraping.
    """

    @property
    def client(self):
        """
        associated ``Client`` object
        """
        return self.__client

    @property
    def detector(self):
        """
        associated ``Detector`` object
        """
        return self.__detector

    @property
    def before_intercept(self):
        """
        pre-interception callback object
        """
        return self.__start

    @property
    def after_intercept(self):
        """
        post-interception callback object
        """
        return self.__end

    # private properties
    __slots__ = ['__detector', '__client', '__start', '__end', ]

    def __init__(self, client, detector, before_intercept=None,
                 after_intercept=None):
        """
        :param client: initialized ``Client`` object to associate
        :param detector: initialized ``Detector`` object to associate

        Optional arguments:

        :param before_intercept: pre-interception callback object.
        :type before_intercept: ``callable`` with signature
            ``"(url) -> result"``
        :param after_intercept: post-interception callable object
        :type after_intercept: ``callable`` with signature
            ``"(url, response) -> None"``

        :raises AssertionError: if ``client`` is not an instance of ``Client``
        :raises AssertionError: if ``detector`` is not an instance of
            ``Detector``.
        """

        # required arguments
        assert(isinstance(client, Client) and isinstance(detector, Detector))
        self.__client = client
        self.__detector = detector

        # optional arguments
        self.__start = before_intercept if callable(before_intercept) else None
        self.__end = after_intercept if callable(after_intercept) else None

        pass  # void return

    def __call__(self, request):
        """
        :param request: incoming HTTP request
        :type request: ``dict``

        :returns: the response from SnapSearch backend service (or the output
            of ``before_intercept()``, if specified and if it returns a
            ``dict``) . On success, the response is a ``dict`` containing
            search engine optimized representation of the URL's target.
        """

        # check for the eligibility of interception
        raw_current_url = self.detector(request)
        if not raw_current_url:
            return None

        # invoke pre-interception callback
        if callable(self.before_intercept):
            result = self.before_intercept(raw_current_url)
            # allow pre-interception callback to shortcut the interception
            if isinstance(result, dict):
                return result

        # dispatch backend service
        response = self.client(raw_current_url)

        # invoke post-interception callback
        if callable(self.after_intercept):
            # why don't we allow post-interception callback to override the
            # response from the backend service?
            self.after_intercept(raw_current_url, response)

        return response

    pass
